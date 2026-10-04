"""CG-04b: separación de gradientes; diagnóstico sin aceptación ni optimización del lote."""
import os
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG",":4096:8")
import argparse,json,subprocess,sys
from pathlib import Path
import torch
import ejecutar_ajuste_cgan as e
from diagnosticar_recuperacion_cgan import fingerprint,pack
from datos_ajuste import atomic_json,digest
from losses import critic_score,gradient_penalty

KINDS=("original","repetida","total","wasserstein","penalizacion")

def exact_values(a,b):
    if set(a)!=set(b):return False
    for k in a:
        x,y=a[k],b[k]
        if isinstance(x,dict) and x.get("kind")=="tensor":
            if not isinstance(y,dict) or any(x[t]!=y.get(t) for t in ("sha256","shape","dtype","finite")):return False
        elif x!=y:return False
    return True

def terms(D,x,y,fake,weight):
    real=critic_score(D,x,y).mean()
    generated=critic_score(D,x,fake).mean()
    gp=gradient_penalty(D,x,y,fake)
    w=generated-real
    penalty=weight*gp
    return {"wasserstein":w,"penalizacion":penalty,"total":w+penalty}

def vectors(D):
    result={};unused=[]
    for name,p in D.named_parameters():
        if p.grad is None:unused.append(name);v=torch.zeros_like(p)
        else:v=p.grad
        if not torch.isfinite(v).all():raise ValueError("Gradiente no finito: "+name)
        result[name]=v.detach().cpu().clone()
    return result,unused

def difference(x,y):
    if set(x)!=set(y):raise ValueError("Parámetros diferentes")
    rows=[]
    for k in x:
        if x[k].shape!=y[k].shape or x[k].dtype!=y[k].dtype:raise ValueError("Contrato de tensor distinto")
        if not torch.isfinite(x[k]).all() or not torch.isfinite(y[k]).all():raise ValueError("No finito")
        d=(x[k].double()-y[k].double()).abs()
        rows.append({"parameter":k,"exact":torch.equal(x[k],y[k]),
          "max_abs":float(d.max()),"l2_difference":float(torch.linalg.vector_norm(d)),
          "reference_l2":float(torch.linalg.vector_norm(x[k].double()))})
    return {"exact":all(r["exact"] for r in rows),"max_abs":max(r["max_abs"] for r in rows),"parameters":rows}

def probe(G,D,og,od,batch,cfg,kind,device):
    G.train();D.train()
    before=fingerprint(pack(G,D,og,od,device))
    og.zero_grad(set_to_none=True);od.zero_grad(set_to_none=True)
    x,y,_,_=batch
    with torch.no_grad():fake=G(x)
    forwards=[]
    def hook(module,inputs,output):
        forwards.append(fingerprint({"inputs":inputs,"output":output}))
    handle=D.register_forward_hook(hook)
    rng_before=fingerprint(e.rng_state(device))
    try:
        if kind in ("original","repetida"):
            loss,parts=e.critic_loss(D,x,y,fake,cfg["lambda_gp"])
            values={"total":float(loss.detach()),"reported_parts":parts}
        else:
            t=terms(D,x,y,fake,cfg["lambda_gp"])
            loss=t[kind];values={k:float(v.detach()) for k,v in t.items()}
        if not torch.isfinite(loss):raise ValueError("Pérdida no finita")
        loss.backward()
        grad,unused=vectors(D)
    finally:handle.remove()
    after=fingerprint(pack(G,D,og,od,device))
    unchanged=exact_values({k:v for k,v in before.items() if not k.startswith("/rng")},
                           {k:v for k,v in after.items() if not k.startswith("/rng")})
    if not unchanged:raise ValueError("El diagnóstico modificó redes u optimizadores")
    return grad,{"kind":kind,"input":fingerprint({"batch":batch,"fake":fake}),
       "forwards":forwards,"rng_before":rng_before,"rng_after":fingerprint(e.rng_state(device)),
       "losses":values,"unused_parameters":unused,"models_optimizers_unchanged":unchanged}

def child(a):
    a.salida.mkdir(parents=True,exist_ok=False);e.configure()
    if not a.cpu_test and not torch.cuda.is_available():raise RuntimeError("CUDA no disponible")
    device=torch.device("cpu" if a.cpu_test else "cuda:0")
    cfg=e.spec(a.rama);store=e.Store(a.datos,a.mascaras)
    initial=e.load_initial(a.pesos,cfg,store)
    identity,train,val=e.identity(cfg,a.rama,"tecnica",store,device,initial)
    identity["probe_sha256"]=digest(Path(__file__))
    identity["fingerprint_source_sha256"]=digest(Path(__file__).with_name("diagnosticar_recuperacion_cgan.py"))
    e.seed_all(cfg["seed"]);G,D,og,od=e.build(cfg,initial,device);del initial
    if a.temperatura=="continua":
        G.train();D.train()
        order=torch.randperm(len(train),generator=torch.Generator().manual_seed(cfg["seed"]+1)).tolist()
        for pos in range(0,len(order),cfg["batch"]):
            e.train_step(G,D,og,od,store.batch([train[i] for i in order[pos:pos+cfg["batch"]]],device),store,cfg)
        metrics,_,_=e.evaluate(G,store,val,device)
        atomic_json(a.salida/"epoch1-validation.json",metrics)
    else:
        c=torch.load(a.checkpoint,map_location="cpu",weights_only=True)
        if c["identity"]!=identity:raise ValueError("Checkpoint de otro código, entorno o variante")
        state=c["state"]
        G.load_state_dict(state["generator"]);D.load_state_dict(state["critic"])
        og.load_state_dict(state["opt_g"]);od.load_state_dict(state["opt_d"])
        e.restore_rng(state["rng"],device)
        if not exact_values(fingerprint(state),fingerprint(pack(G,D,og,od,device))):raise ValueError("Restauración inexacta")
        del c,state
    boundary=fingerprint(pack(G,D,og,od,device))
    if a.temperatura=="continua" and a.componente=="original":
        e.atomic_checkpoint(a.salida/"epoch1.pt",{"identity":identity,"state":pack(G,D,og,od,device)})
    order=torch.randperm(len(train),generator=torch.Generator().manual_seed(cfg["seed"]+2)).tolist()
    rows=[train[i] for i in order[:cfg["batch"]]]
    grad,report=probe(G,D,og,od,store.batch(rows,device),cfg,a.componente,device)
    e.atomic_checkpoint(a.salida/"gradientes.pt",grad)
    atomic_json(a.salida/"resultado.json",{"identity":identity,"boundary":boundary,
        "rows":rows,"temperature":a.temperatura,**report,"gpu_accepted":False,
        "gradients_sha256":digest(a.salida/"gradientes.pt")})

def compare_all(root):
    reports={};grads={}
    for temp in ("continua","nueva"):
        for kind in KINDS:
            key=temp+"/"+kind
            r=json.loads((root/key/"resultado.json").read_text())
            if digest(root/key/"gradientes.pt")!=r["gradients_sha256"]:raise ValueError("Gradientes alterados")
            reports[key]=r
            grads[key]=torch.load(root/key/"gradientes.pt",map_location="cpu",weights_only=True)
    ref=reports["continua/original"]
    for key,r in reports.items():
        if r["identity"]!=ref["identity"] or r["rows"]!=ref["rows"]:raise ValueError("Identidad/lote distinto")
        for field in ("boundary","input","rng_before","rng_after"):
            if not exact_values(ref[field],r[field]):raise ValueError("Comparación no pareada: "+key+"/"+field)
        if r["forwards"]!=ref["forwards"]:raise ValueError("Los forwards difieren: "+key)
        if r["losses"]["total"]!=ref["losses"]["total"]:raise ValueError("Pérdida total distinta: "+key)
    cross={k:difference(grads["continua/"+k],grads["nueva/"+k]) for k in KINDS}
    controls={};reconstruction={}
    for temp in ("continua","nueva"):
        controls[temp]={k:difference(grads[temp+"/original"],grads[temp+"/"+k]) for k in ("repetida","total")}
        # Suma sobre CPU de componentes medidos en procesos independientes.
        w=grads[temp+"/wasserstein"];gp=grads[temp+"/penalizacion"]
        added={k:w[k]+gp[k] for k in w}
        added64={k:w[k].double()+gp[k].double() for k in w}
        reconstruction[temp]={"sum_float32":difference(grads[temp+"/total"],added),
          "sum_float64":difference({k:v.double() for k,v in grads[temp+"/total"].items()},added64)}
    return {"schema":"oe2-cg04b-gradients-v1","gpu_accepted":False,
      "identity":ref["identity"],"paired_states_inputs_rng_forwards":True,
      "controls":controls,"continuous_vs_new":cross,"reconstruction":reconstruction,
      "limitation":"La suma offline no reproduce el orden interno de acumulación CUDA. No aplica tolerancia de aceptación."}

def run(a):
    a.salida.mkdir(parents=True,exist_ok=False)
    atomic_json(a.salida/"request.json",{"argv":sys.argv,"gpu_accepted":False})
    for temp in ("continua","nueva"):
        for kind in KINDS:
            out=a.salida/temp/kind
            cmd=[sys.executable,str(Path(__file__).resolve()),"--rama",a.rama,
                 "--temperatura",temp,"--componente",kind,"--salida",str(out.resolve())]
            for k in ("datos","mascaras","pesos"):cmd+=["--"+k,str(getattr(a,k).resolve())]
            if a.cpu_test:cmd.append("--cpu-test")
            if temp=="nueva":cmd+=["--checkpoint",str((a.salida/"continua/original/epoch1.pt").resolve())]
            atomic_json(a.salida/(temp+"-"+kind+"-command.json"),cmd)
            with (a.salida/(temp+"-"+kind+".log")).open("w") as log:
                result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
            atomic_json(a.salida/(temp+"-"+kind+"-exit.json"),{"exit_code":result.returncode})
            if result.returncode:raise RuntimeError("Falló "+temp+"/"+kind+"; conservar registros")
            print(temp+"/"+kind+": completada",flush=True)
    report=compare_all(a.salida);atomic_json(a.salida/"comparacion.json",report)
    atomic_json(a.salida/"archivos.json",[{"path":p.relative_to(a.salida).as_posix(),"bytes":p.stat().st_size,"sha256":digest(p)}
        for p in sorted(a.salida.rglob("*")) if p.is_file() and p.name!="archivos.json"])
    print(json.dumps({"gpu_accepted":False,"comparisons":{k:v["max_abs"] for k,v in report["continuous_vs_new"].items()}}))

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rama",choices=["C0","C1"],required=True)
    for k in ("datos","mascaras","pesos","salida"):p.add_argument("--"+k,type=Path,required=True)
    p.add_argument("--cpu-test",action="store_true")
    p.add_argument("--temperatura",choices=["continua","nueva"])
    p.add_argument("--componente",choices=KINDS);p.add_argument("--checkpoint",type=Path)
    a=p.parse_args()
    if bool(a.temperatura)!=bool(a.componente):raise ValueError("Modo interno incompleto")
    if a.temperatura=="nueva" and not a.checkpoint:raise ValueError("Falta checkpoint")
    if a.temperatura:child(a)
    else:run(a)

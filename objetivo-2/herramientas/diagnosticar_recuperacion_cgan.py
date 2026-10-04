"""Diagnóstico independiente de reanudación cGAN; nunca concede aceptación GPU."""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
import numpy as np
import torch
import ejecutar_ajuste_cgan as engine
from datos_ajuste import atomic_json, digest
from revisar_ajuste import equal_state

MODES = ("continua", "repetida", "recarga", "reanudada")

def fingerprint(value):
    """Huellas por hoja: valores separados de metadatos de ubicación y disposición."""
    leaves = {}
    def walk(x, path):
        if isinstance(x, torch.Tensor):
            a = x.detach().cpu().contiguous()
            leaves[path] = dict(kind="tensor", dtype=str(a.dtype), shape=list(a.shape),
                stride=list(x.stride()), device=str(x.device),
                sha256=hashlib.sha256(a.numpy().tobytes()).hexdigest(),
                finite=bool(torch.isfinite(a).all()))
        elif isinstance(x, dict):
            for k in sorted(x, key=str): walk(x[k], path+"/"+str(k))
        elif isinstance(x, (tuple, list)):
            leaves[path+"/@container"] = type(x).__name__
            for k,v in enumerate(x): walk(v, path+"/"+str(k))
        else: leaves[path] = x
    walk(value, "")
    return leaves

def compare(a, b):
    keys = sorted(set(a)|set(b))
    values, metadata = [], []
    for k in keys:
        x,y=a.get(k),b.get(k)
        if x == y: continue
        if isinstance(x,dict) and isinstance(y,dict) and x.get("kind")==y.get("kind")=="tensor":
            if any(x.get(t)!=y.get(t) for t in ("sha256","shape","dtype","finite")): values.append(k)
            if any(x.get(t)!=y.get(t) for t in ("device","stride")): metadata.append(k)
        else: values.append(k)
    return {"values_equal":not values,"different_values":values,
            "metadata_equal":not metadata,"different_metadata":metadata}

def pack(G,D,og,od,device):
    return dict(generator=G.state_dict(),critic=D.state_dict(),
                opt_g=og.state_dict(),opt_d=od.state_dict(),rng=engine.rng_state(device))

class Trace:
    def __init__(self, path):
        self.path=path
        self.events=[]
        self.prefix=""
    def emit(self,label,value):
        event={"event":self.prefix+label,"leaves":fingerprint(value)}
        self.events.append(event)
        # Registro incremental: la evidencia sobrevive a un error posterior.
        with self.path.open("a",encoding="utf-8") as f: f.write(json.dumps(event,allow_nan=False)+"\n")

def instrument(trace,G,D,og,od,device):
    original=engine.checked_step
    handles=[]
    def checked(loss,model,opt):
        name="G" if model is G else "D"
        trace.emit(name+"/loss",loss)
        step=opt.step
        def observed_step(*args,**kwargs):
            trace.emit(name+"/gradients",{n:p.grad for n,p in model.named_parameters()})
            result=step(*args,**kwargs)
            trace.emit(name+"/updated",{"model":model.state_dict(),"optimizer":opt.state_dict()})
            return result
        opt.step=observed_step
        try: return original(loss,model,opt)
        finally: opt.step=step
    engine.checked_step=checked
    def hook(name):
        def observe(module,inputs,output):
            trace.emit(name+"/forward",{"inputs":inputs,"output":output})
        return observe
    for name,model in (("G",G),("D",D)):
        handles.append(model.register_forward_hook(hook(name)))
    return original,handles

def child(a):
    out=a.salida
    out.mkdir(parents=True,exist_ok=False)
    engine.configure()
    if not a.cpu_test and not torch.cuda.is_available(): raise RuntimeError("CUDA no disponible")
    device=torch.device("cpu" if a.cpu_test else "cuda:0")
    cfg=engine.spec(a.rama)
    store=engine.Store(a.datos,a.mascaras)
    initial=engine.load_initial(a.pesos,cfg,store)
    identity,train,val=engine.identity(cfg,a.rama,"tecnica",store,device,initial)
    identity["diagnostic_sha256"]=digest(Path(__file__))
    atomic_json(out/"identity.json",identity)
    engine.seed_all(cfg["seed"])
    G,D,og,od=engine.build(cfg,initial,device)
    del initial
    trace=Trace(out/"trace.jsonl")
    if a.modo!="reanudada":
        G.train();D.train()
        order=torch.randperm(len(train),generator=torch.Generator().manual_seed(cfg["seed"]+1)).tolist()
        for pos in range(0,len(order),cfg["batch"]):
            engine.train_step(G,D,og,od,store.batch([train[k] for k in order[pos:pos+cfg["batch"]]],device),store,cfg)
        metrics,_,_=engine.evaluate(G,store,val,device)
        atomic_json(out/"epoch1-validation.json",metrics)
        saved=pack(G,D,og,od,device)
        atomic_json(out/"boundary-saved.json",fingerprint(saved))
        engine.atomic_checkpoint(out/"epoch1.pt",saved)
        del saved
    if a.modo in ("reanudada","recarga"):
        source=a.checkpoint if a.modo=="reanudada" else out/"epoch1.pt"
        c=torch.load(source,map_location="cpu",weights_only=True)
        G.load_state_dict(c["generator"]);D.load_state_dict(c["critic"])
        og.load_state_dict(c["opt_g"]);od.load_state_dict(c["opt_d"])
        engine.restore_rng(c["rng"],device)
        restored=pack(G,D,og,od,device)
        check=compare(fingerprint(c),fingerprint(restored))
        # CPU del archivo frente a CUDA vivo: ubicación distinta es esperable.
        atomic_json(out/"restore-check.json",check)
        if not check["values_equal"]: raise ValueError("El estado cambia inmediatamente al cargar; consultar restore-check.json")
        del c,restored
    atomic_json(out/"boundary-live.json",fingerprint(pack(G,D,og,od,device)))
    G.train();D.train()
    original,handles=instrument(trace,G,D,og,od,device)
    order=torch.randperm(len(train),generator=torch.Generator().manual_seed(cfg["seed"]+2)).tolist()
    try:
        for step,pos in enumerate(range(0,len(order),cfg["batch"])):
            trace.prefix="epoch2/batch"+str(step)+"/"
            rr=[train[k] for k in order[pos:pos+cfg["batch"]]]
            batch=store.batch(rr,device)
            trace.emit("start",{"indices":rr,"batch":batch,"rng":engine.rng_state(device)})
            parts,_=engine.train_step(G,D,og,od,batch,store,cfg)
            trace.emit("end",{"parts":parts,"rng":engine.rng_state(device)})
    finally:
        engine.checked_step=original
        for h in handles:h.remove()
    metrics,pred,keys=engine.evaluate(G,store,val,device)
    atomic_json(out/"validation.json",metrics)
    np.save(out/"predicciones-val.npy",pred)
    atomic_json(out/"indices-val.json",keys)
    engine.atomic_checkpoint(out/"epoch2.pt",pack(G,D,og,od,device))
    atomic_json(out/"completed.json",{"completed":True,"gpu_accepted":False,
        "mode":a.modo,"arm":a.rama,"trace_events":len(trace.events)})

def compare_runs(left,right):
    def read(p):return json.loads(p.read_text(encoding="utf-8"))
    if read(left/"identity.json")!=read(right/"identity.json"):raise ValueError("Identidades no pareadas")
    boundary=compare(read(left/"boundary-live.json"),read(right/"boundary-live.json"))
    x=[json.loads(s) for s in (left/"trace.jsonl").read_text().splitlines()]
    y=[json.loads(s) for s in (right/"trace.jsonl").read_text().splitlines()]
    if len(x)!=len(y) or [e["event"] for e in x]!=[e["event"] for e in y]:raise ValueError("Trazas incompletas o desalineadas")
    first=None; differing=0
    for index,(a,b) in enumerate(zip(x,y)):
        d=compare(a["leaves"],b["leaves"])
        if not d["values_equal"]:
            differing+=1
            if first is None:first={"index":index,"event":a["event"],**d}
    z0=np.load(left/"predicciones-val.npy",allow_pickle=False)
    z1=np.load(right/"predicciones-val.npy",allow_pickle=False)
    delta=np.abs(z0.astype(np.float64)-z1.astype(np.float64))
    return dict(boundary=boundary,first_difference=first,differing_events=differing,
                prediction_max_abs=float(delta.max()),prediction_mean_abs=float(delta.mean()),
                validation_left=read(left/"validation.json"),validation_right=read(right/"validation.json"))

def orchestrate(a):
    a.salida.mkdir(parents=True,exist_ok=False)
    atomic_json(a.salida/"request.json",{"argv":sys.argv,"cpu_test":a.cpu_test,"gpu_accepted":False})
    for mode in MODES:
        cmd=[sys.executable,str(Path(__file__).resolve()),"--modo",mode,"--rama",a.rama]
        for key in ("datos","mascaras","pesos"):
            cmd+=["--"+key,str(getattr(a,key).resolve())]
        cmd+=["--salida",str((a.salida/mode).resolve())]
        if a.cpu_test:cmd+=["--cpu-test"]
        if mode=="reanudada":cmd+=["--checkpoint",str((a.salida/"continua/epoch1.pt").resolve())]
        atomic_json(a.salida/(mode+"-command.json"),cmd)
        with (a.salida/(mode+".log")).open("w",encoding="utf-8") as log:
            r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
        atomic_json(a.salida/(mode+"-exit.json"),{"exit_code":r.returncode})
        if r.returncode:raise RuntimeError("Falló "+mode+"; conservar toda la salida y consultar el log")
        print(mode+": completada",flush=True)
    comparisons={m:compare_runs(a.salida/"continua",a.salida/m) for m in MODES[1:]}
    report={"schema":"oe2-cgan-resume-diagnostic-v1","arm":a.rama,"cpu_test":a.cpu_test,
            "gpu_accepted":False,"comparisons":comparisons,
            "limitation":"Instrumentación con copias CPU/sincronización; no sustituye la prueba técnica original ni demuestra una causa CUDA."}
    atomic_json(a.salida/"diagnostico.json",report)
    paths=sorted(p for p in a.salida.rglob("*") if p.is_file())
    atomic_json(a.salida/"archivos.json",[{"path":p.relative_to(a.salida).as_posix(),
        "bytes":p.stat().st_size,"sha256":digest(p)} for p in paths])
    print(json.dumps(report),flush=True)

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rama",choices=["C0","C1"],required=True)
    p.add_argument("--modo",choices=MODES)
    for n in ("datos","mascaras","pesos","salida"):p.add_argument("--"+n,type=Path,required=True)
    p.add_argument("--checkpoint",type=Path)
    p.add_argument("--cpu-test",action="store_true")
    return p

if __name__=="__main__":
    a=parser().parse_args()
    if a.modo=="reanudada" and a.checkpoint is None:raise ValueError("Falta checkpoint")
    if a.modo:child(a)
    else:orchestrate(a)

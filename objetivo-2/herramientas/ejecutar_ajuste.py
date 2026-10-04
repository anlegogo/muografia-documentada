"""Ejecutor separado A/B. CPU solo prueba técnica; piloto requiere validación GPU."""
import os
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import argparse,json,sys,time,platform,io
from pathlib import Path
import numpy as np
import torch
from filelock import FileLock
from datos_ajuste import ROOT,Store,spec,sources,canonical,digest,atomic_json,read_json,MANIFEST_SHA
from perdida_cuentas_regionales import combined_loss
sys.path.insert(0,str(ROOT/'objetivo-2/implementacion/models'))
sys.path.insert(0,str(ROOT/'objetivo-2/implementacion/scripts/evaluation'))
from unet_generator import build_generator
from metrics import compute_ssim,compute_psnr

def environment(device):
    return {'python':platform.python_version(),'numpy':np.__version__,'torch':str(torch.__version__),'cuda':torch.version.cuda,'device':str(device),'gpu':torch.cuda.get_device_name(device) if device.type=='cuda' else None,'threads':2,'deterministic':True}

def load_initial(path,configuration,store):
    if digest(path)!=configuration['initial_checkpoint_sha256']:raise ValueError('Pesos iniciales distintos')
    safe=[np._core.multiarray._reconstruct,np.ndarray,np.dtype,np.dtypes.UInt32DType]
    with torch.serialization.safe_globals(safe):c=torch.load(io.BytesIO(Path(path).read_bytes()),map_location='cpu',weights_only=True)
    if c['data_manifest_sha256']!=MANIFEST_SHA or c['normalization']!=store.manifest['normalization'] or c['epoch']!=5:raise ValueError('Checkpoint inicial incompatible')
    return c['generator']

def atomic_checkpoint(path,state):
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('wb') as f:
        torch.save(state,f);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

def export_predictions(out,net,store,rows,device,last):
    val,pred,keys=evaluate(net,store,rows,device)
    tmp=out/'predicciones-val.tmp.npy';np.save(tmp,pred);os.replace(tmp,out/'predicciones-val.npy')
    atomic_json(out/'indices-val.json',[list(x) for x in keys])
    atomic_json(out/'exports.json',{'predictions_sha256':digest(out/'predicciones-val.npy'),'indices_sha256':digest(out/'indices-val.json'),'checkpoint_sha256':digest(last),'validation':val})

def state_digest(state):
    import hashlib
    h=hashlib.sha256()
    for k,v in sorted(state.items()):
        h.update(k.encode());h.update(v.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()

@torch.no_grad()
def evaluate(net,store,rows,device):
    net.eval();ss=[];ps=[];pred=[];keys=[]
    for i in range(0,len(rows),4):
        rr=rows[i:i+4];x,y,_,_=store.batch(rr,device);z=net(x)
        if not torch.isfinite(z).all() or torch.any((z<0)|(z>=1)):raise ValueError('Predicción no finita o fuera de rango')
        z=z[:,0].cpu().numpy();yy=y[:,0].cpu().numpy()
        for k in range(len(rr)):
            ss.append(compute_ssim(z[k],yy[k]));ps.append(compute_psnr(yy[k],z[k]))
        pred.append(z);keys.extend(rr)
    return {'n':len(rows),'ssim':float(np.mean(ss)),'psnr':float(np.mean(ps))},np.concatenate(pred),keys

def gate_check(path,identity,store):
    from revisar_ajuste import audit_technical
    gate=read_json(path)
    if gate.get('schema')!='oe2-ajuste-technical-gate-v1' or not gate.get('gpu_accepted'):raise ValueError('No hay aceptación técnica GPU')
    paths={k:Path(v) for k,v in gate['runs'].items()}
    # Se reevalúan checkpoints, no se confía únicamente en una bandera JSON.
    current=audit_technical(paths,require_gpu=True,expected_sources=identity['sources'])
    if not current['gpu_accepted']:raise ValueError('Prueba GPU no válida')
    if current['checkpoint_sha256']!=gate['checkpoint_sha256']:raise ValueError('Cambió la evidencia GPU')
    for item in current['identities']:
        if item['cache_sha256']!=store.identity or item['environment']!=identity['environment']:raise ValueError('Entorno/datos distintos de la prueba GPU')

def run(args):
    if args.exportar and (args.reanudar or args.parar_tras is not None):raise ValueError('Exportar no se combina con reanudar o parar')
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True
    torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    if args.cpu_test and args.etapa!='tecnica':raise ValueError('CPU autorizado solo para comprobación técnica')
    if not args.cpu_test and not torch.cuda.is_available():raise RuntimeError('CUDA no disponible; no se cambia a CPU')
    device=torch.device('cpu' if args.cpu_test else 'cuda:0')
    configuration=spec(args.rama);store=Store(args.datos,args.mascaras)
    epochs=2 if args.etapa=='tecnica' else 5
    if args.parar_tras is not None and not 1<=args.parar_tras<=epochs:raise ValueError('Época de parada inválida')
    train_rows=store.indices('train',configuration,args.etapa);val_rows=store.indices('val',configuration,args.etapa)
    identity={'schema':'oe2-ajuste-run-v1','arm':args.rama,'stage':args.etapa,'config':configuration,'data_manifest_sha256':MANIFEST_SHA,'cache_sha256':store.identity,'sources':sources(),'environment':environment(device),'train_indices_sha256':canonical(train_rows),'val_indices_sha256':canonical(val_rows),'epochs':epochs,'initial_checkpoint_sha256':configuration['initial_checkpoint_sha256']}
    if args.etapa=='piloto':
        if args.aceptacion_gpu is None:raise ValueError('Falta informe de aceptación GPU')
        gate_check(args.aceptacion_gpu,identity,store)
    initial=load_initial(args.pesos,configuration,store)
    seed=configuration['seed'];torch.manual_seed(seed)
    if device.type=='cuda':torch.cuda.manual_seed_all(seed)
    net=build_generator(configuration['generator']).to(device);net.load_state_dict(initial,strict=True)
    opt=torch.optim.Adam(net.parameters(),lr=configuration['optimizer']['lr'],betas=tuple(float(x) for x in configuration['optimizer']['betas']),foreach=False)
    # El generador de orden es independiente del RNG de dropout.
    torch.manual_seed(seed)
    if device.type=='cuda':torch.cuda.manual_seed_all(seed)
    identity['initial_generator_sha256']=state_digest(net.state_dict())
    out=args.salida;out.mkdir(parents=True,exist_ok=True)
    with FileLock(str(out/'run.lock'),timeout=0):
        last=out/'last.pt';history=[];start=0;resume_count=0;sessions=[]
        if args.exportar:
            c=torch.load(last,map_location='cpu',weights_only=True)
            if c['identity']!=identity or c['epoch']!=epochs:raise ValueError('Solo se exporta una ejecución final compatible')
            net.load_state_dict(c['generator'],strict=True)
            atomic_json(out/'history.json',c['history'])
            atomic_json(out/'summary.json',{'identity':identity,'completed':True,'epoch':epochs,'selected_epoch':epochs,'resume_count':c['resume_count'],'history':c['history'],'sessions':c['sessions'],'last_checkpoint_sha256':digest(last)})
            export_predictions(out,net,store,val_rows,device,last)
            print(json.dumps({'exported':True,'optimizer_steps':0}));return
        if args.reanudar:
            if not last.exists():raise ValueError('No existe checkpoint para reanudar')
            c=torch.load(last,map_location='cpu',weights_only=True)
            if c['identity']!=identity:raise ValueError('Identidad distinta: no se mezcla rama/configuración/entorno')
            start=c['epoch'];history=c['history'];sessions=c['sessions'];resume_count=c['resume_count']+1
            if len(history)!=start or [r['epoch'] for r in history]!=list(range(1,start+1)):raise ValueError('Historial incoherente')
            if start>=epochs:raise ValueError('La ejecución ya terminó')
            net.load_state_dict(c['generator'],strict=True);opt.load_state_dict(c['optimizer'])
            torch.set_rng_state(c['rng_cpu'])
            if device.type=='cuda':torch.cuda.set_rng_state_all(c['rng_cuda'])
        elif last.exists() or (out/'identity.json').exists():raise FileExistsError('Usar directorio nuevo o reanudación explícita')
        atomic_json(out/'identity.json',identity)
        if device.type=='cuda':torch.cuda.reset_peak_memory_stats()
        session_start=time.perf_counter()
        for epoch in range(start+1,epochs+1):
            if (out/'STOP').exists():raise RuntimeError('Retirar STOP para continuar; no se modifica automáticamente')
            net.train();order=torch.randperm(len(train_rows),generator=torch.Generator().manual_seed(seed+epoch)).tolist()
            if device.type=='cuda':torch.cuda.synchronize()
            t=time.perf_counter();totals={'l1':0.,'regional':0.,'total':0.};family_sum={};family_n={};gn=[];valid_regions=0
            for pos in range(0,len(order),4):
                rr=[train_rows[i] for i in order[pos:pos+4]];x,y,counts,mm=store.batch(rr,device)
                opt.zero_grad(set_to_none=True);z=net(x)
                loss,parts=combined_loss(z,y,counts,mm,store.families,store.scale,configuration['lambda_regional'])
                if not torch.isfinite(loss):raise ValueError('Pérdida no finita')
                loss.backward();norm2=0.
                for p in net.parameters():
                    if p.grad is None or not torch.isfinite(p.grad).all():raise ValueError('Gradiente no finito')
                    norm2+=float(p.grad.detach().double().square().sum())
                gn.append(norm2**.5);opt.step()
                if any(not torch.isfinite(p).all() for p in net.parameters()):raise ValueError('Parámetro no finito')
                totals['l1']+=float(parts['l1'].detach());totals['regional']+=float(parts['regional'].detach());totals['total']+=float(loss.detach())
                for support in parts['support']:
                    valid_regions+=len(support['valid_regions'])
                    for f,value in support['family_losses'].items():family_sum[f]=family_sum.get(f,0.)+value;family_n[f]=family_n.get(f,0)+1
            val,pred,keys=evaluate(net,store,val_rows,device)
            if device.type=='cuda':torch.cuda.synchronize()
            record={'epoch':epoch,'steps':len(gn),'order_sha256':canonical([train_rows[i] for i in order]),'losses':{k:v/len(gn) for k,v in totals.items()},'family_losses':{k:family_sum[k]/family_n[k] for k in family_sum},'family_samples':family_n,'valid_regions_total':valid_regions,'gradient_norm_mean':float(np.mean(gn)),'gradient_norm_max':max(gn),'validation':val,'epoch_compute_seconds':time.perf_counter()-t,'generator_sha256':state_digest(net.state_dict())}
            history.append(record)
            elapsed=time.perf_counter()-session_start
            current_sessions=sessions+[{'first_epoch':start+1,'last_epoch':epoch,'compute_elapsed_seconds':elapsed,'peak_cuda_allocated_bytes':torch.cuda.max_memory_allocated() if device.type=='cuda' else None}]
            state={'identity':identity,'epoch':epoch,'generator':net.state_dict(),'optimizer':opt.state_dict(),'rng_cpu':torch.get_rng_state(),'rng_cuda':torch.cuda.get_rng_state_all() if device.type=='cuda' else [],'history':history,'resume_count':resume_count,'sessions':current_sessions}
            save_start=time.perf_counter();atomic_checkpoint(last,state)
            # Historial del checkpoint es canónico: si falla esta exportación,
            # reanudar no duplica épocas ni usa un registro adelantado al modelo.
            atomic_json(out/'history.json',history)
            complete=epoch==epochs
            atomic_json(out/'summary.json',{'identity':identity,'completed':complete,'epoch':epoch,'selected_epoch':epochs,'resume_count':resume_count,'history':history,'sessions':current_sessions,'last_checkpoint_sha256':digest(last),'last_save_seconds':time.perf_counter()-save_start})
            print(json.dumps({'arm':args.rama,'epoch':epoch,'loss':record['losses'],'val':val,'completed':complete}),flush=True)
            if complete:
                tmp=out/'predicciones-val.tmp.npy';np.save(tmp,pred);os.replace(tmp,out/'predicciones-val.npy')
                atomic_json(out/'indices-val.json',[list(x) for x in keys])
                atomic_json(out/'exports.json',{'predictions_sha256':digest(out/'predicciones-val.npy'),'indices_sha256':digest(out/'indices-val.json'),'checkpoint_sha256':digest(last)})
                break
            if args.parar_tras==epoch or (out/'STOP').exists():break
        atomic_json(out/'last-session.json',{'wall_seconds_including_exports':time.perf_counter()-session_start,'epoch':history[-1]['epoch'],'resumed':args.reanudar})

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rama',choices=['A','B'],required=True);p.add_argument('--etapa',choices=['tecnica','piloto'],required=True)
    for n in ['datos','mascaras','pesos','salida']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--cpu-test',action='store_true');p.add_argument('--reanudar',action='store_true');p.add_argument('--parar-tras',type=int);p.add_argument('--aceptacion-gpu',type=Path)
    p.add_argument('--exportar',action='store_true',help='Recuperar exportaciones de un checkpoint final sin entrenar')
    return p

if __name__=='__main__':run(parser().parse_args())

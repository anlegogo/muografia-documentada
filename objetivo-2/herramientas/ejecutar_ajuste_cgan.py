"""Continuación pareada cGAN C0/C1; piloto exclusivamente tras aceptación GPU."""
import os
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
import argparse,io,json,random,time,sys
from pathlib import Path
import numpy as np
import torch
from filelock import FileLock
from datos_ajuste import ROOT,Store,canonical,digest,atomic_json,read_json,sources as base_sources,MANIFEST_SHA
from ejecutar_ajuste import atomic_checkpoint,evaluate,state_digest,environment,build_generator
from perdida_cuentas_regionales import regional_log_count_loss
sys.path.insert(0,str(ROOT/'objetivo-2/implementacion/models'))
sys.path.insert(0,str(ROOT/'objetivo-2/implementacion/scripts/training'))
from patch_critic import build_critic
from losses import critic_loss,generator_loss
from gradientes_critico import GRADIENT_POLICY,critic_components,separated_critic_step

CONFIG_SHA={'C0':'f3aed36bd5e23d76630501e0851a0e88b44d4023520850c67a2eb730c7b1effc','C1':'ab6d32814c92221da9fbe47fd54eb517e2136b36676efc2f10fea9762b635ee9'}

PAIR_SEEDS={'R1':2026100401,'R2':2026100402,'R3':2026100403}

def spec(arm,pair=None):
    c=read_json(ROOT/'objetivo-2/configuraciones/ajuste-cgan-v1'/f'{arm}.json')
    if canonical(c)!=CONFIG_SHA[arm]:raise ValueError('Configuración cGAN alterada o desconocida')
    if pair is None:return c
    if pair not in PAIR_SEEDS:raise ValueError('Pareja desconocida')
    expected={**c,'pair':pair,'seed':PAIR_SEEDS[pair],'run_id':f'oe2-cgan-repeticion-f05-{pair}-{arm}-s{PAIR_SEEDS[pair]}'}
    candidate=read_json(ROOT/'objetivo-2/configuraciones/repeticion-cgan-f05'/f'{pair}-{arm}.json')
    if canonical(candidate)!=canonical(expected):raise ValueError('Configuración de repetición alterada')
    return candidate

def sources():
    import hashlib
    result=base_sources()
    files=['herramientas/ejecutar_ajuste.py','herramientas/revisar_ajuste.py',
           'herramientas/evaluar_ajuste.py','herramientas/ejecutar_ajuste_cgan.py',
           'herramientas/revisar_ajuste_cgan.py','herramientas/evaluar_ajuste_cgan.py',
           'herramientas/gradientes_critico.py',
           'implementacion/models/patch_critic.py','implementacion/scripts/training/losses.py']
    for name in files:
        p='objetivo-2/'+name
        result[p]=hashlib.sha256((ROOT/p).read_text(encoding='utf-8').encode()).hexdigest()
    return result

def configure():
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True
    torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False

def seed_all(seed):
    random.seed(seed);np.random.seed(seed%(2**32));torch.manual_seed(seed)
    if torch.cuda.is_available():torch.cuda.manual_seed_all(seed)

def rng_state(device):
    n=np.random.get_state()
    return {'torch':torch.get_rng_state(),'cuda':torch.cuda.get_rng_state_all() if device.type=='cuda' else [],
            'numpy':[n[0],n[1].tolist(),n[2],n[3],n[4]],'python':random.getstate()}

def restore_rng(r,device):
    torch.set_rng_state(r['torch'])
    if device.type=='cuda':torch.cuda.set_rng_state_all(r['cuda'])
    n=r['numpy'];np.random.set_state((n[0],np.array(n[1],dtype=np.uint32),n[2],n[3],n[4]))
    random.setstate(r['python'])

def load_initial(path,cfg,store):
    if digest(path)!=cfg['initial_checkpoint_sha256']:raise ValueError('Checkpoint cGAN inicial distinto')
    safe=[np._core.multiarray._reconstruct,np.ndarray,np.dtype,np.dtypes.UInt32DType]
    with torch.serialization.safe_globals(safe):
        c=torch.load(io.BytesIO(Path(path).read_bytes()),map_location='cpu',weights_only=True)
    if c['epoch']!=5 or c['data_manifest_sha256']!=MANIFEST_SHA or c['normalization']!=store.manifest['normalization']:raise ValueError('Identidad inicial incompatible')
    if not c.get('critic'):raise ValueError('Falta el crítico entrenado')
    return c['generator'],c['critic']

def build(cfg,initial,device):
    G=build_generator(cfg['generator']).to(device);D=build_critic(cfg['critic']).to(device)
    G.load_state_dict(initial[0],strict=True);D.load_state_dict(initial[1],strict=True)
    kw={'lr':cfg['optimizer']['lr'],'betas':tuple(float(x) for x in cfg['optimizer']['betas']),'foreach':False}
    return G,D,torch.optim.Adam(G.parameters(),**kw),torch.optim.Adam(D.parameters(),**kw)

def checked_step(loss,model,opt):
    if not torch.isfinite(loss):raise ValueError('Pérdida no finita')
    loss.backward();s=0.
    for p in model.parameters():
        if p.grad is None or not torch.isfinite(p.grad).all():raise ValueError('Gradiente ausente o no finito')
        s+=float(p.grad.detach().double().square().sum())
    opt.step()
    if any(not torch.isfinite(p).all() for p in model.parameters()):raise ValueError('Parámetro no finito')
    return s**.5

def generator_objective(D,x,z,y,counts,masks,families,scale,cfg):
    base,parts=generator_loss(D,x,z,y,lambda_l1=cfg['lambda_l1'],lambda_adv=cfg['lambda_adv'])
    regional,support=regional_log_count_loss(z,counts,masks,families,scale)
    # C0 preserva exactamente la pérdida original y su grafo.
    total=base if cfg['lambda_regional']==0 else base+cfg['lambda_regional']*regional
    return total,{**parts,'regional':float(regional.detach()),'total_g':float(total.detach())},support

def train_step(G,D,og,od,batch,store,cfg,observer=None):
    x,y,counts,masks=batch;og.zero_grad(set_to_none=True)
    # Se conserva la política del piloto: una muestra G sin gradiente para D.
    with torch.no_grad():fake=G(x)
    if not torch.isfinite(fake).all():raise ValueError('Salida no finita')
    acc={'d_real':0.,'d_fake':0.,'w_est':0.,'gp':0.,'total_d':0.,'grad_d':0.}
    for _ in range(cfg['n_critic']):
        od.zero_grad(set_to_none=True)
        wasserstein,penalty,parts=critic_components(D,x,y,fake,cfg['lambda_gp'])
        loss=wasserstein+penalty
        norm=separated_critic_step(wasserstein,penalty,D,od)
        for k,v in {**parts,'total_d':float(loss.detach()),'grad_d':norm}.items():acc[k]+=v/cfg['n_critic']
    if observer:observer('after_d',G,D,og,od)
    # D participa en el gradiente respecto a fake, pero no acumula gradientes D.
    od.zero_grad(set_to_none=True)
    for p in D.parameters():p.requires_grad_(False)
    try:
        z=G(x);loss,parts,support=generator_objective(D,x,z,y,counts,masks,store.families,store.scale,cfg)
        norm=checked_step(loss,G,og)
    finally:
        for p in D.parameters():p.requires_grad_(True)
    if observer:observer('after_g',G,D,og,od)
    return {**acc,**parts,'grad_g':norm},support

def identity(cfg,arm,stage,store,device,initial):
    env=environment(device)
    env.update(cudnn=torch.backends.cudnn.version(),cublas_workspace=os.environ['CUBLAS_WORKSPACE_CONFIG'],
               tf32=False,numpy_rng='MT19937',python_rng='MT19937')
    train=store.indices('train',cfg,stage);val=store.indices('val',cfg,stage)
    i={'schema':'oe2-cgan-ajuste-run-v1','critic_gradient_policy':GRADIENT_POLICY,'arm':arm,'stage':stage,'config':cfg,
       'pair':cfg.get('pair'),'seed':cfg['seed'],'sources':sources(),'environment':env,'data_manifest_sha256':MANIFEST_SHA,
       'cache_sha256':store.identity,'train_indices_sha256':canonical(train),'val_indices_sha256':canonical(val),
       'initial_checkpoint_sha256':cfg['initial_checkpoint_sha256'],
       'initial_generator_sha256':state_digest(initial[0]),'initial_critic_sha256':state_digest(initial[1]),
       'epochs':2 if stage=='tecnica' else 5}
    return i,train,val

def snapshot(out,c,save_seconds=0.):
    atomic_json(out/'identity.json',c['identity']);atomic_json(out/'history.json',c['history'])
    atomic_json(out/'summary.json',{'identity':c['identity'],'completed':c['epoch']==c['identity']['epochs'],
                'epoch':c['epoch'],'selected_epoch':c['identity']['epochs'],'resume_count':c['resume_count'],
                'history':c['history'],'sessions':c['sessions'],'last_checkpoint_sha256':digest(out/'last.pt'),
                'last_save_seconds':save_seconds})

def export(out,pred,keys,last):
    temp=out/'predicciones-val.tmp.npy';np.save(temp,pred);os.replace(temp,out/'predicciones-val.npy')
    atomic_json(out/'indices-val.json',[list(x) for x in keys])
    atomic_json(out/'exports.json',{'predictions_sha256':digest(out/'predicciones-val.npy'),
                'indices_sha256':digest(out/'indices-val.json'),'checkpoint_sha256':digest(last)})

def gate_check(path,i):
    from revisar_ajuste_cgan import audit_technical
    gate=read_json(path)
    if gate.get('schema')!='oe2-cgan-ajuste-gate-v1' or not gate.get('gpu_accepted'):raise ValueError('Falta aceptación GPU cGAN')
    if gate.get('pair')!=i.get('pair') or gate.get('seed')!=i['seed']:raise ValueError('Aceptación de otra pareja/semilla')
    current=audit_technical(gate['runs'],require_gpu=True,pair=i.get('pair'))
    if current['checkpoint_sha256']!=gate['checkpoint_sha256']:raise ValueError('Cambió evidencia GPU')
    for item in current['identities']:
        for key in ['pair','seed','environment','cache_sha256','sources','initial_checkpoint_sha256']:
            if item[key]!=i[key]:raise ValueError('Evidencia GPU incompatible: '+key)

def run(args):
    configure()
    if args.exportar and (args.reanudar or args.parar_tras is not None):raise ValueError('Exportar no se combina con reanudar/parar')
    if args.cpu_test and args.etapa!='tecnica':raise ValueError('CPU solo para etapa técnica')
    if not args.cpu_test and not torch.cuda.is_available():raise RuntimeError('CUDA no disponible')
    device=torch.device('cpu' if args.cpu_test else 'cuda:0')
    cfg=spec(args.rama,getattr(args,'pareja',None));store=Store(args.datos,args.mascaras)
    initial=load_initial(args.pesos,cfg,store);i,train,val=identity(cfg,args.rama,args.etapa,store,device,initial)
    epochs=i['epochs']
    if args.parar_tras is not None and not 1<=args.parar_tras<=epochs:raise ValueError('Época de parada inválida')
    if args.etapa=='piloto':
        if args.aceptacion_gpu is None:raise ValueError('Falta aceptación GPU cGAN')
        gate_check(args.aceptacion_gpu,i)
    out=Path(args.salida);out.mkdir(parents=True,exist_ok=True);last=out/'last.pt'
    with FileLock(str(out/'.run.lock'),timeout=0):
        if not args.reanudar and not args.exportar and (last.exists() or (out/'identity.json').exists()):raise FileExistsError('Usar salida nueva o reanudar')
        seed_all(cfg['seed']);G,D,og,od=build(cfg,initial,device);del initial
        start=0;history=[];sessions=[];resumes=0
        if args.reanudar or args.exportar:
            c=torch.load(last,map_location='cpu',weights_only=True)
            if c['identity']!=i:raise ValueError('Reanudación incompatible: rama, datos, código o entorno')
            from revisar_ajuste_cgan import validate_state
            validate_state(c)
            if args.exportar:
                if c['epoch']!=epochs:raise ValueError('Exportar requiere última época completa')
                G.load_state_dict(c['generator'],strict=True)
                metrics,pred,keys=evaluate(G,store,val,device)
                if metrics!=c['history'][-1]['validation']:raise ValueError('Exportación no reproduce validación')
                snapshot(out,c);export(out,pred,keys,last);print('Exportaciones recuperadas sin entrenar',flush=True);return
            start=c['epoch']
            if start>=epochs:raise ValueError('Ejecución ya completa')
            G.load_state_dict(c['generator'],strict=True);D.load_state_dict(c['critic'],strict=True)
            og.load_state_dict(c['opt_g']);od.load_state_dict(c['opt_d'])
            restore_rng(c['rng'],device)
            history=c['history'];sessions=c['sessions'];resumes=c['resume_count']+1;del c
        atomic_json(out/'identity.json',i)
        if device.type=='cuda':torch.cuda.reset_peak_memory_stats()
        session_start=time.perf_counter()
        for epoch in range(start+1,epochs+1):
            if (out/'STOP').exists():raise RuntimeError('Retirar STOP para continuar')
            G.train();D.train();acc={};family_sum={};family_n={};valid_regions=0
            order=torch.randperm(len(train),generator=torch.Generator().manual_seed(cfg['seed']+epoch)).tolist()
            if device.type=='cuda':torch.cuda.synchronize()
            t=time.perf_counter();steps=0
            for pos in range(0,len(order),cfg['batch']):
                rr=[train[k] for k in order[pos:pos+cfg['batch']]]
                parts,support=train_step(G,D,og,od,store.batch(rr,device),store,cfg)
                for key,value in parts.items():acc[key]=acc.get(key,0.)+value
                for sp in support:
                    valid_regions+=len(sp['valid_regions'])
                    for f,v in sp['family_losses'].items():family_sum[f]=family_sum.get(f,0.)+v;family_n[f]=family_n.get(f,0)+1
                steps+=1
            metrics,pred,keys=evaluate(G,store,val,device)
            if device.type=='cuda':torch.cuda.synchronize()
            record={'epoch':epoch,'steps_g':steps,'steps_d':steps*cfg['n_critic'],
                    'order_sha256':canonical([train[k] for k in order]),'losses':{k:v/steps for k,v in acc.items()},
                    'family_losses':{k:v/family_n[k] for k,v in family_sum.items()},'family_samples':family_n,
                    'valid_regions_total':valid_regions,'validation':metrics,
                    'generator_sha256':state_digest(G.state_dict()),'critic_sha256':state_digest(D.state_dict()),
                    'epoch_compute_seconds':time.perf_counter()-t}
            history.append(record)
            c={'identity':i,'epoch':epoch,'generator':G.state_dict(),'critic':D.state_dict(),
               'opt_g':og.state_dict(),'opt_d':od.state_dict(),'rng':rng_state(device),'history':history,
               'resume_count':resumes,'sessions':sessions+[{'first_epoch':start+1,'last_epoch':epoch,
                 'compute_seconds':time.perf_counter()-session_start,
                 'peak_cuda_allocated_bytes':torch.cuda.max_memory_allocated() if device.type=='cuda' else None}]}
            st=time.perf_counter();atomic_checkpoint(last,c);snapshot(out,c,time.perf_counter()-st)
            print(json.dumps({'arm':args.rama,'epoch':epoch,'steps_g':steps,'steps_d':steps*cfg['n_critic'],'validation':metrics}),flush=True)
            if epoch==epochs:export(out,pred,keys,last);break
            if args.parar_tras==epoch or (out/'STOP').exists():break
        atomic_json(out/'last-session.json',{'resumed':args.reanudar,'epoch':history[-1]['epoch'],
                    'wall_seconds_including_exports':time.perf_counter()-session_start})

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pareja',choices=list(PAIR_SEEDS))
    p.add_argument('--rama',choices=['C0','C1'],required=True);p.add_argument('--etapa',choices=['tecnica','piloto'],required=True)
    for n in ['datos','mascaras','pesos','salida']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--cpu-test',action='store_true');p.add_argument('--reanudar',action='store_true')
    p.add_argument('--parar-tras',type=int);p.add_argument('--aceptacion-gpu',type=Path);p.add_argument('--exportar',action='store_true')
    return p
if __name__=='__main__':run(parser().parse_args())


"""Auditoría de estados completos y recuperación del ajuste cGAN."""
import argparse,json
from pathlib import Path
import numpy as np
import torch
from datos_ajuste import read_json,digest,canonical,atomic_json
from ejecutar_ajuste import state_digest
from ejecutar_ajuste_cgan import spec,sources,configure,GRADIENT_POLICY
from revisar_ajuste import finite,equal_state

def validate_state(c):
    i=c['identity'];cfg=spec(i['arm']);epochs=2 if i['stage']=='tecnica' else 5
    if i.get('critic_gradient_policy')!=GRADIENT_POLICY:raise ValueError('Política de gradiente incompatible')
    if i['schema']!='oe2-cgan-ajuste-run-v1' or i['stage'] not in ('tecnica','piloto') or i['config']!=cfg or i['epochs']!=epochs or i['sources']!=sources():raise ValueError('Identidad cGAN incompatible')
    n=2 if i['stage']=='tecnica' else 360
    if not 1<=c['epoch']<=epochs or [h['epoch'] for h in c['history']]!=list(range(1,c['epoch']+1)):raise ValueError('Historial incompleto')
    if not finite(c):raise ValueError('Estado no finito')
    for h in c['history']:
        if h['steps_g']!=n or h['steps_d']!=n*5 or h['validation']['n']!=(8 if i['stage']=='tecnica' else 360):raise ValueError('Número de actualizaciones/muestras incorrecto')
    for model in ['generator','critic']:
        if state_digest(c[model])!=c['history'][-1][model+'_sha256']:raise ValueError('Huella del modelo incorrecta')
    for key,steps in [('opt_g',n*c['epoch']),('opt_d',5*n*c['epoch'])]:
        o=c[key]
        if not o['state'] or len(o['param_groups'])!=1:raise ValueError('Optimizador vacío o alterado')
        group=o['param_groups'][0]
        if group['lr']!=cfg['optimizer']['lr'] or tuple(group['betas'])!=tuple(cfg['optimizer']['betas']):raise ValueError('Optimizador incompatible')
        if set(o['state'])!=set(group['params']) or any(float(v['step'])!=steps for v in o['state'].values()):raise ValueError('Pasos del optimizador incorrectos')
    if set(c['rng'])!={'torch','cuda','numpy','python'}:raise ValueError('Falta un estado aleatorio')
    if i['environment']['device'].startswith('cuda') and not c['rng']['cuda']:raise ValueError('Falta RNG CUDA')
    return c

def load_completed(path,arm,stage):
    path=Path(path);c=torch.load(path/'last.pt',map_location='cpu',weights_only=True);validate_state(c)
    i=c['identity']
    if i['arm']!=arm or i['stage']!=stage or c['epoch']!=i['epochs']:raise ValueError('Rama/etapa incorrecta o incompleta')
    s=read_json(path/'summary.json')
    if not s['completed'] or s['identity']!=i or s['epoch']!=c['epoch'] or s['history']!=c['history'] or s['last_checkpoint_sha256']!=digest(path/'last.pt') or s['resume_count']!=c['resume_count']:raise ValueError('Resumen incompatible')
    ex=read_json(path/'exports.json')
    for key,name in [('checkpoint_sha256','last.pt'),('predictions_sha256','predicciones-val.npy'),('indices_sha256','indices-val.json')]:
        if ex[key]!=digest(path/name):raise ValueError('Archivo de exportación alterado')
    keys=read_json(path/'indices-val.json')
    if canonical(keys)!=i['val_indices_sha256']:raise ValueError('Índices incorrectos')
    if stage=='tecnica' and keys!=spec(arm)['stages']['technical']['val_indices']:raise ValueError('Muestras técnicas incorrectas')
    z=np.load(path/'predicciones-val.npy',mmap_mode='r',allow_pickle=False)
    if z.shape!=(8 if stage=='tecnica' else 360,256,256) or z.dtype!=np.float32 or not np.isfinite(z).all() or np.any((z<0)|(z>=1)):raise ValueError('Predicciones fuera de contrato')
    return c

def audit_technical(paths,require_gpu=False):
    expected={a+'-'+mode for a in ['C0','C1'] for mode in ['continua','recuperada']}
    if set(paths)!=expected:raise ValueError('Se requieren cuatro ejecuciones cGAN')
    states={k:load_completed(v,k.split('-')[0],'tecnica') for k,v in paths.items()}
    identities=[v['identity'] for v in states.values()]
    for key in ['initial_checkpoint_sha256','initial_generator_sha256','initial_critic_sha256','sources','environment','cache_sha256','data_manifest_sha256','train_indices_sha256','val_indices_sha256']:
        if any(i[key]!=identities[0][key] for i in identities):raise ValueError('Pruebas no pareadas: '+key)
    for arm in ['C0','C1']:
        x=states[arm+'-continua'];y=states[arm+'-recuperada']
        if x['resume_count']!=0 or y['resume_count']!=1 or x['identity']!=y['identity']:raise ValueError('Interrupción/identidad incorrecta')
        for key in ['generator','critic','opt_g','opt_d','rng']:
            if not equal_state(x[key],y[key]):raise ValueError('Recuperación distinta: '+key)
        for xx,yy in zip(x['history'],y['history']):
            if {k:v for k,v in xx.items() if k!='epoch_compute_seconds'}!={k:v for k,v in yy.items() if k!='epoch_compute_seconds'}:raise ValueError('Historial numérico distinto')
        if not np.array_equal(np.load(Path(paths[arm+'-continua'])/'predicciones-val.npy'),np.load(Path(paths[arm+'-recuperada'])/'predicciones-val.npy')):raise ValueError('Predicciones distintas')
    if [x['order_sha256'] for x in states['C0-continua']['history']]!=[x['order_sha256'] for x in states['C1-continua']['history']]:raise ValueError('Orden C0/C1 distinto')
    gpu=all(i['environment']['device'].startswith('cuda') and i['environment']['gpu'] for i in identities)
    if require_gpu and not gpu:raise ValueError('La evidencia CPU no acepta GPU')
    return {'schema':'oe2-cgan-ajuste-gate-v1','technical_checks_passed':True,'gpu_accepted':bool(gpu),'exact_recovery':True,
            'runs':{k:str(Path(v).resolve()) for k,v in paths.items()},'identities':identities,
            'checkpoint_sha256':{k:digest(Path(v)/'last.pt') for k,v in paths.items()}}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for arm in ['C0','C1']:
        for mode in ['continua','recuperada']:p.add_argument('--'+arm+'-'+mode,type=Path,required=True)
    p.add_argument('--exigir-gpu',action='store_true');p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args();configure()
    paths={arm+'-'+mode:getattr(a,arm+'_'+mode) for arm in ['C0','C1'] for mode in ['continua','recuperada']}
    r=audit_technical(paths,a.exigir_gpu);a.salida.parent.mkdir(parents=True,exist_ok=True);atomic_json(a.salida,r)
    print(json.dumps({'passed':True,'gpu_accepted':r['gpu_accepted'],'exact_recovery':True}))


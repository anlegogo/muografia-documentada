"""Auditoría de recuperación A/B y aceptación técnica explícita CPU/GPU."""
import argparse,json,math
from pathlib import Path
import numpy as np
import torch
from datos_ajuste import spec,sources,digest,atomic_json,canonical,read_json

def equal_state(a,b):
    if isinstance(a,torch.Tensor):return isinstance(b,torch.Tensor) and torch.equal(a,b)
    if isinstance(a,dict):return isinstance(b,dict) and a.keys()==b.keys() and all(equal_state(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)):return type(a)==type(b) and len(a)==len(b) and all(equal_state(x,y) for x,y in zip(a,b))
    return type(a)==type(b) and a==b

def finite(x):
    if isinstance(x,torch.Tensor):return bool(torch.isfinite(x).all())
    if isinstance(x,dict):return all(finite(v) for v in x.values())
    if isinstance(x,(list,tuple)):return all(finite(v) for v in x)
    if isinstance(x,float):return math.isfinite(x)
    return True

def load_completed(path,arm,stage,expected_sources):
    path=Path(path);cp=path/'last.pt';c=torch.load(cp,map_location='cpu',weights_only=True)
    i=c['identity'];cfg=spec(arm);epochs=2 if stage=='tecnica' else 5
    if i['arm']!=arm or i['stage']!=stage or i['config']!=cfg or i['sources']!=expected_sources:raise ValueError('Identidad de ejecución incompatible')
    if c['epoch']!=epochs or len(c['history'])!=epochs or [r['epoch'] for r in c['history']]!=list(range(1,epochs+1)):raise ValueError('Épocas incompletas o duplicadas')
    if not finite(c):raise ValueError('Valores no finitos')
    summary=read_json(path/'summary.json')
    if not summary['completed'] or summary['identity']!=i or summary['history']!=c['history'] or summary['last_checkpoint_sha256']!=digest(cp):raise ValueError('Resumen no corresponde al checkpoint')
    ex=read_json(path/'exports.json')
    if ex['checkpoint_sha256']!=digest(cp) or ex['predictions_sha256']!=digest(path/'predicciones-val.npy') or ex['indices_sha256']!=digest(path/'indices-val.json'):raise ValueError('Exportación alterada o incompleta')
    pred=np.load(path/'predicciones-val.npy',allow_pickle=False,mmap_mode='r')
    n=8 if stage=='tecnica' else 360
    if pred.shape!=(n,256,256) or pred.dtype!=np.float32 or not np.isfinite(pred).all() or np.any((pred<0)|(pred>=1)):raise ValueError('Predicciones incompatibles')
    indices=read_json(path/'indices-val.json')
    if canonical(indices)!=i['val_indices_sha256']:raise ValueError('Orden de inferencia incompatible')
    if stage=='tecnica' and indices!=cfg['stages']['technical']['val_indices']:raise ValueError('Muestras distintas')
    for r in c['history']:
        if r['steps']!=(2 if stage=='tecnica' else 360) or r['validation']['n']!=n:raise ValueError('Pasos/muestras incorrectos')
    return c

def audit_technical(paths,require_gpu=False,expected_sources=None):
    expected_sources=expected_sources or sources()
    wanted={'A-continua','A-recuperada','B-continua','B-recuperada'}
    if set(paths)!=wanted:raise ValueError('Se requieren cuatro ejecuciones técnicas')
    states={k:load_completed(v,k[0],'tecnica',expected_sources) for k,v in paths.items()}
    identities=[c['identity'] for c in states.values()]
    for field in ['initial_generator_sha256','initial_checkpoint_sha256','data_manifest_sha256','cache_sha256','train_indices_sha256','val_indices_sha256','environment']:
        if any(i[field]!=identities[0][field] for i in identities):raise ValueError('Las ramas no comparten '+field)
    for arm in ['A','B']:
        x=states[arm+'-continua'];y=states[arm+'-recuperada']
        if x['resume_count']!=0 or y['resume_count']!=1:raise ValueError('No consta la interrupción/reanudación prevista')
        if x['identity']!=y['identity']:raise ValueError('Identidades distintas')
        for key in ['generator','optimizer','rng_cpu','rng_cuda']:
            if not equal_state(x[key],y[key]):raise ValueError('Recuperación diferente: '+key)
        for xx,yy in zip(x['history'],y['history']):
            for key in ['epoch','steps','order_sha256','losses','family_losses','family_samples','valid_regions_total','gradient_norm_mean','gradient_norm_max','validation','generator_sha256']:
                if xx[key]!=yy[key]:raise ValueError('Registro numérico no reproducido: '+key)
        p=np.load(Path(paths[arm+'-continua'])/'predicciones-val.npy')
        q=np.load(Path(paths[arm+'-recuperada'])/'predicciones-val.npy')
        if not np.array_equal(p,q):raise ValueError('Inferencia continua/recuperada distinta')
    # Orden común A/B por época.
    if [r['order_sha256'] for r in states['A-continua']['history']]!=[r['order_sha256'] for r in states['B-continua']['history']]:raise ValueError('Orden A/B distinto')
    gpu=all(i['environment']['device'].startswith('cuda') and i['environment']['gpu'] for i in identities)
    if require_gpu and not gpu:raise ValueError('Evidencia CPU: no acredita GPU')
    return {'schema':'oe2-ajuste-technical-gate-v1','technical_checks_passed':True,'gpu_accepted':bool(gpu),'exact_recovery':True,'runs':{k:str(Path(v).resolve()) for k,v in paths.items()},'checkpoint_sha256':{k:digest(Path(v)/'last.pt') for k,v in paths.items()},'identities':identities}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['A-continua','A-recuperada','B-continua','B-recuperada']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--exigir-gpu',action='store_true');p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args();paths={n:getattr(a,n.replace('-','_')) for n in ['A-continua','A-recuperada','B-continua','B-recuperada']}
    r=audit_technical(paths,a.exigir_gpu);atomic_json(a.salida,r);print(json.dumps({'passed':True,'gpu_accepted':r['gpu_accepted'],'exact_recovery':True}))

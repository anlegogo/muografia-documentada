"""Regresión del evaluador con predicciones antiguas, no resultados del nuevo ensayo."""
import argparse,json
from pathlib import Path
import numpy as np
from datos_ajuste import ROOT,Store,read_json,digest,atomic_json
from evaluar_ajuste import analyze_predictions
p=argparse.ArgumentParser(description=__doc__)
for n in ['datos','mascaras','predicciones-previas','salida']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();store=Store(a.datos,a.mascaras)
paths={'A':a.predicciones_previas/'unet-predicciones.npy','B':a.predicciones_previas/'cgan-predicciones.npy'}
expected={'A':'c4e35ef07c46974b4847ec46ea60173c6f1a44e1c6f33f0639f2aea2e58ec9fc','B':'39d087f7eaa93cc85c874adfc84b6fffdd061c60e1f619842b09cd941ac8d091'}
for k,path in paths.items():
    if digest(path)!=expected[k]:raise ValueError('La regresión requiere las predicciones CPU previamente verificadas')
keys=[[g,v,k] for g in store.manifest['splits']['val'] for v in range(6) for k in range(20)]
values={k:np.load(v,mmap_mode='r') for k,v in paths.items()}
r=analyze_predictions(store,keys,values,'piloto')
old=read_json(ROOT/'objetivo-2/evidencias/evaluacion-regiones-geometricas-v1.json')
mapping={'unet':'A','cgan':'B','entrada':'entrada'}
new={(x['geometry'],x['view'],x['region'],x['model']):x for x in r['regions']}
errors=[]
for x in old['regions']:
    if 'model' not in x:continue
    y=new[(x['geometry'],x['view'],x['region'],mapping[x['model']])]
    for k,kk in [('bias_relative','bias'),('mae_relative','mae')]:
        errors.append(abs(x[k]['mean']-y[kk]['mean']))
assert max(errors)<1e-12
contrasts={(x['geometry'],x['view'],x['region']):x for x in r['contrasts']}
for x in old['contrasts']:
    y=contrasts[(x['geometry'],x['view'],x['region'])]
    assert y['reference_contrast']==x['reference_contrast']
    for k,v in x['models'].items():
        other=y['models'][mapping[k]]
        assert other['valid_realizations']==v['valid_realizations']
        assert abs(other['error']['mean_absolute']-v['absolute_error']['mean'])<1e-12
assert r['summary']['A']['common_contrasts']==23
assert abs(r['summary']['A']['ssim']-.8436712357269776)<1e-12
assert abs(r['summary']['B']['ssim']-.8227914467544925)<1e-12
rejected=0
for bad in [keys[:-1],keys[1:]+keys[:1]]:
    try:analyze_predictions(store,bad,values,'piloto')
    except ValueError:rejected+=1
assert rejected==2
atomic_json(a.salida,{'schema':'oe2-adjustment-evaluator-regression-v1','passed':True,'regional_values_compared':len(errors),'max_difference':max(errors),'contrast_cases_compared':len(contrasts),'common_contrasts':23,'prediction_images_compared':720,'invalid_indices_rejected':2,'input_sha256':expected,'new_pilot_run':False,'heldout_opened':False,'note':'A/B labels used internally as fixtures for old U-Net/cGAN arrays; no new training result or selection is claimed'})
print(json.dumps({'passed':True,'regional_values':len(errors),'max_difference':max(errors),'new_pilot_run':False}))

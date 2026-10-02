"""Contrasta borde e interior frente a la referencia ideal tabulada, con N fijo.

15 regiones predefinidas: 5 columnas por lado (cielo 30-42 grados), 5 filas altas.
Intervalos simultáneos conservadores; no usa una dispersión entre píxeles como error.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from diagnosticar_observable_angular import matrix
from estadistica_control_angular import binomial_interval, classify


def regions(sky):
    if sky.shape != (256,256) or sky.dtype != bool: raise ValueError('máscara inválida')
    el=np.linspace(2,47,256); middle=(el>=30)&(el<=42)
    interior=sky.copy();interior[~middle]=False;interior[:,:20]=False;interior[:,236:]=False
    result={'interior':interior}
    for j in list(range(5))+list(range(251,256)):
        mask=np.zeros_like(sky);mask[:,j]=sky[:,j]&middle;result[f'column_{j}']=mask
    for i in range(251,256):
        mask=np.zeros_like(sky);mask[i]=sky[i];result[f'row_{i}']=mask
    if any(not v.any() for v in result.values()):raise ValueError('región sin soporte')
    return result


def evaluate(counts, events, sky, reference, alpha=.05, tolerance=.01):
    if type(events) is not int or events<=0 or counts.shape!=(256,256) or not np.issubdtype(counts.dtype,np.integer) or np.any(counts<0) or int(counts.sum())>events:
        raise ValueError('se requieren conteos enteros y máximo un registro por primario')
    if not 0<alpha<1 or not 0<tolerance<1:raise ValueError('criterio inválido')
    masks=regions(sky)
    pnom=np.broadcast_to(np.asarray(reference['nominal_probability_per_pixel_by_row'])[:,None],(256,256))
    pideal=np.broadcast_to(np.asarray(reference['ideal_selected_probability_per_pixel_by_row'])[:,None],(256,256))
    if not np.isfinite(pnom).all() or not np.isfinite(pideal).all() or np.any(pnom<=0) or np.any(pideal<0) or np.any(pideal>pnom) or pnom.sum()>1+1e-12:
        raise ValueError('probabilidades inválidas')
    values={}
    for name, mask in masks.items():
        nom=float(pnom[mask].sum());ideal=float(pideal[mask].sum());k=int(counts[mask].sum())
        interval=binomial_interval(k,events,alpha/len(masks))
        values[name]={'counts':k,'nominal_probability':nom,'ideal_probability':ideal,
                      'residual':(k/events-ideal)/nom,
                      'interval':[(v-ideal)/nom for v in interval]}
    baseline=values.pop('interior');result=[]
    for name,v in values.items():
        lo=v['interval'][0]-baseline['interval'][1];hi=v['interval'][1]-baseline['interval'][0]
        result.append(dict(v,name=name,difference_pp=100*(v['residual']-baseline['residual']),
                           difference_interval_pp=[100*lo,100*hi],decision=classify(lo,hi,-tolerance,tolerance)))
    return {'schema':'oe1-border-response-v1','physical_validation':False,'events':events,
            'alpha_family':alpha,'tolerance_pp':100*tolerance,'baseline':baseline,'regions':result,
            'all_equivalent':all(r['decision']=='equivalent' for r in result),
            'limits':['Tests nonuniform response relative to ideal no-transport source; does not isolate migration from air transport.',
                      'Existing-run results are retrospective diagnostics. Freeze masks, recipe and N before confirmatory runs.',
                      'Marginal binomial coverage assumes independent primary histories and one recorded arrival per primary.']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('histograma',type=Path);p.add_argument('--eventos',type=int,required=True)
    p.add_argument('--cielo-npy',type=Path,required=True);p.add_argument('--referencia',type=Path,required=True)
    p.add_argument('--alpha',type=float,default=.05,help='usar 0.008333333333333333 para familia de seis vistas')
    p.add_argument('--salida',type=Path,required=True);a=p.parse_args()
    result=evaluate(matrix(a.histograma),a.eventos,np.load(a.cielo_npy,allow_pickle=False),json.loads(a.referencia.read_text(encoding='utf-8')),alpha=a.alpha)
    result['sha256']={k:hashlib.sha256(v.read_bytes()).hexdigest() for k,v in {'counts':a.histograma,'sky_mask':a.cielo_npy,'reference':a.referencia}.items()}
    with a.salida.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,allow_nan=False)

"""Probabilidades exactas del algoritmo de tablas/margen; no calibra flujo físico."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np

MASS = .1056583745


def extended_rows(elevations, weights, margin):
    elevations=np.asarray(elevations,float);weights=np.asarray(weights,float)
    if elevations.shape!=(256,) or weights.shape!=(256,) or not np.isfinite(weights).all() or np.any(weights<0) or weights.sum()<=0:
        raise ValueError('tabla inválida')
    if not np.allclose(elevations,np.linspace(2,47,256),atol=5e-7,rtol=0):raise ValueError('malla no admitida')
    if not math.isfinite(margin) or margin<0:raise ValueError('margen inválido')
    step=float(elevations[1]-elevations[0]);extra=math.ceil(margin/step);idx=np.arange(-extra,256+extra)
    centers=elevations.copy() if margin==0 else elevations[0]+idx*step;out=np.zeros(len(idx))
    def fit(start):
        x=elevations[start:start+8];y=weights[start:start+8]
        b=(8*np.dot(x,y)-x.sum()*y.sum())/(8*np.dot(x,x)-x.sum()**2)
        return (y.sum()-b*x.sum())/8,b
    low,high=fit(0),fit(248)
    for j,k in enumerate(idx):
        if 0<=k<256:out[j]=weights[k]
        elif centers[j]>=.1:
            a,b=low if k<0 else high;out[j]=max(0,a+b*centers[j])
    return centers,out,idx


def above_quantile(q, momentum):
    q=np.asarray(q,float)
    if q.ndim!=1 or len(q)<2 or not np.isfinite(q).all() or np.any(np.diff(q)<0):raise ValueError('cuantiles inválidos')
    if momentum<q[0]:return 1.
    if momentum>=q[-1]:return 0.
    i=np.searchsorted(q,momentum,side='right')-1
    return float(1-(i+(momentum-q[i])/(q[i+1]-q[i]))/(len(q)-1))


def audit(tables, margin=5):
    tables=Path(tables);el,w=np.loadtxt(tables/'row_weights_30d.txt',unpack=True)
    centers,ext,idx=extended_rows(el,w,margin);step=float(el[1]-el[0])
    window_lo,window_hi=2-45/510,47+45/510
    nominal_mass=0.
    lines=(tables/'p_cdf.txt').read_text().splitlines()
    band_edges=np.array([float(x) for x in next(s for s in lines if s.startswith('# band_edges_deg:')).split(':')[1].split()])
    quantiles=np.array([[float(x) for x in s.split()] for s in lines if s.strip() and not s.startswith('#')])
    if len(band_edges)!=len(quantiles)+1 or np.any(np.diff(band_edges)<=0):raise ValueError('bandas inválidas')
    outside=0.;above3=0.;nominal_above3=0.
    momentum3=math.sqrt((3+MASS)**2-MASS**2)
    for center,weight,k in zip(centers,ext,idx):
        lo,hi=center-step/2,center+step/2
        nominal_mass+=weight*max(0,min(hi,window_hi)-max(lo,window_lo))/step
        outside+=weight*(max(0,min(hi,band_edges[0])-lo)+max(0,hi-max(lo,band_edges[-1])))/step
        cuts=sorted(set([lo,hi]+[float(e) for e in band_edges if lo<e<hi]))
        for a,b in zip(cuts[:-1],cuts[1:]):
            band=int(np.clip(np.searchsorted(band_edges,(a+b)/2,side='right')-1,0,len(quantiles)-1))
            term=weight*(b-a)/step*above_quantile(quantiles[band],momentum3)
            above3+=term
            overlap=max(0,min(b,window_hi)-max(a,window_lo))
            nominal_above3+=term*overlap/(b-a)
    f=float(nominal_mass/ext.sum()*30/(30+margin))
    half=np.deg2rad(step/2);angles=np.deg2rad(el)
    mean_cos=np.cos(angles)*math.sin(half)/half
    projected=float(np.dot(w,mean_cos)/w.sum()*math.sin(math.pi/6)/(math.pi/6))
    return {'schema':'oe1-source-probability-v1','physical_validation':False,'margin_deg':margin,
       'nominal_rate_convention_30d':float(w.sum()),'extended_elevation_weight_sum':float(ext.sum()),
       'probability_generated_inside_nominal_window':f,
       'elevation_mass_extrapolated':float(ext[(idx<0)|(idx>=256)].sum()/ext.sum()),
       'momentum_spectrum_clamped_outside_band_range_probability':float(outside/ext.sum()),
       'probability_generated_kinetic_above_3gev':float(above3/ext.sum()),
       'probability_kinetic_above_3gev_given_nominal_window':float(nominal_above3/nominal_mass),
       'vertical_area_over_normal_area_nominal_convention':projected,
       'candidate_total_events_per_view':{str(k):round(k*float(w.sum())/f) for k in [1,10]},
       'table_sha256':{n:hashlib.sha256((tables/n).read_bytes()).hexdigest() for n in ['meta.json','row_weights_30d.txt','p_cdf.txt']},
       'limits':['Probabilities of the implemented sampler, not validation of extrapolated physical flux.',
                 'Generated energy probability is not detected-energy acceptance after rock.',
                 'Area ratio is a convention comparison, not an applied correction.']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('tablas',type=Path)
    p.add_argument('--margen',type=float,default=5);p.add_argument('--salida',required=True,type=Path);a=p.parse_args()
    if a.salida.exists():raise FileExistsError(a.salida)
    r=audit(a.tablas,a.margen)
    with a.salida.open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
    print(json.dumps(r,indent=2))

"""Reproduce la preparación local de cielo, bordes y presupuesto C3 sobre 01a9871.

Usa exclusivamente datos existentes; no ejecuta transporte ni envía trabajos.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys
import numpy as np
import scipy
from scipy.stats import beta
from referencia_cielo_angular import reference
from evaluar_bordes_angular import evaluate
from estadistica_control_angular import plan_equal_counts, evaluate_c3, binomial_interval
from diagnosticar_observable_angular import matrix


def write(path,data):
    with path.open('x',encoding='utf-8') as f:json.dump(data,f,indent=2,allow_nan=False,ensure_ascii=False)


def analyze(delivery,tables,originals,out):
    out.mkdir(parents=True,exist_ok=False)
    helper=delivery/'scripts/comun.py'
    spec=importlib.util.spec_from_file_location('sky_review_helper',helper)
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    c.GEOMETRIAS=originals/'simulation/geometry_catalog/geometries'
    geo=c.GEOMETRIAS/'geo-train-01.json'
    el=np.linspace(2,47,256);azedges=np.linspace(-30,30,257);az=(azedges[1:]+azedges[:-1])/2
    x=c.opacidad_vista(json.loads(geo.read_text()),0,el,az)
    silhouette=np.array([el[x[:,j]>0].max() if (x[:,j]>0).any() else -99 for j in range(256)])
    sky=(x==0)&(el[:,None]>silhouette[None,:]+1)
    np.save(out/'cielo-geo-train-01-view0.npy',sky,allow_pickle=False)
    root=delivery/'datos/sc3/controles-30626/resultados'
    expected={name.removeprefix('./'):h for h,name in (line.split() for line in (root/'salidas.sha256').read_text().splitlines())}
    sources=[]
    def checked(path):
        data=path.read_bytes();actual=hashlib.sha256(data).hexdigest()
        if actual!=expected[path.relative_to(root).as_posix()]:raise ValueError('se requieren bytes SC3 exactos: '+str(path))
        sources.append({'file':path.relative_to(delivery).as_posix(),'sha256':actual});return path
    summary={}
    for run,margin,N in [('c01-anidado-cono',0,20000000),('c02-cono-margen-5deg',5,2000000)]:
        r=reference(tables,margin);write(out/f'cielo-ideal-margen-{margin}.json',r)
        stem='geo-train-01_view0';suffix='_hist_sub300_ecut3.csv' if margin==0 else '_hist_ecut3.csv'
        d=root/run;counts=matrix(checked(d/(stem+suffix)));gen=matrix(checked(d/(stem+'_gen.csv')))
        m=json.loads(checked(d/(stem+'.meta.json')).read_text())
        if m['events_transported']!=N or m['oe1_controles']['margin_deg']!=margin:raise ValueError('configuración inesperada')
        border=evaluate(counts,N,sky,r);write(out/f'bordes-{run}.json',border)
        observed=np.array([counts[i][sky[i]].sum()/gen[i][sky[i]].sum() if gen[i][sky[i]].sum()>0 else np.nan for i in range(256)])
        supported=np.isfinite(observed);old=np.interp(el,el[supported],observed[supported])
        ideal=np.array(r['ideal_selected_given_nominal_by_row'])
        extrap=(el<el[supported].min())[:,None]&np.ones_like(sky)
        mask=(x>=1e4)&extrap
        # Holding epsilon fixed isolates the change of denominator (not noisy counts).
        denominator_ratio=np.broadcast_to((old/ideal)[:,None],x.shape)
        expected_counts=np.asarray(r['ideal_selected_probability_per_pixel_by_row'])[:,None]*N
        normalized=counts/expected_counts
        np.savez_compressed(out/f'respuesta-ideal-{run}.npz',response=normalized,sky=sky,opacity=x,elevation_centers_deg=el,azimuth_centers_deg=az)
        summary[run]={'N':N,'margin':margin,'ideal_q_range':[float(ideal.min()),float(ideal.max())],
                      'sky_min_elevation_deg':float(el[supported].min()),'extrapolated_rock_pixels':int(mask.sum()),
                      'denominator_only_new_over_old_response_in_extrapolated_rock':{'min':float(denominator_ratio[mask].min()),'median':float(np.median(denominator_ratio[mask])),'max':float(denominator_ratio[mask].max())},
                      'edge_decisions':{k:sum(v['decision']==k for v in border['regions']) for k in ('equivalent','inconclusive','outside_tolerance')},
                      'max_abs_edge_point_estimate_pp':max(abs(v['difference_pp']) for v in border['regions']),
                      'ideal_sky_is_physical_reference':False}
    # Dimensioning is conditional and deliberately does not use the unverified angular shortcut.
    design=plan_equal_counts();target=design['expected_counts_each_arm_each_band']
    minimum_rate=1620/20000000 # smallest of the FOUR declared bands, source c01, full nominal window
    costs=[]
    for g in (5,10,20,50):
        f=1.44/(2*g)**2;np_events=math.ceil(target/minimum_rate);ng_events=math.ceil(target/(minimum_rate*f))
        costs.append({'source_half_m':g,'N_P':np_events,'N_G':ng_events,'core_hours_both_arms':(np_events+ng_events)*.0005324969/3600})
    # Monte Carlo checks the PLANNING approximation, not physical equivalence.
    trials=20000;rng=np.random.default_rng(2026100207);f=1.44/100
    nP=costs[0]['N_P'];nG=costs[0]['N_G'];alpha_arm=.05/(2*4)
    cc=rng.binomial(nP,minimum_rate,trials);dd=rng.binomial(nG,minimum_rate*f,trials)
    cl=beta.ppf(alpha_arm/2,cc,nP-cc+1);ch=beta.isf(alpha_arm/2,cc+1,nP-cc)
    dl=beta.ppf(alpha_arm/2,dd,nG-dd+1);dh=beta.isf(alpha_arm/2,dd+1,nG-dd)
    passed=(dl/ch/f>=.95)&(dh/cl/f<=1.05);successes=int(passed.sum())
    low_power=binomial_interval(successes,trials,.05)[0]
    design.update(bands_g_cm2=[[1e4,3e4],[3e4,6e4],[6e4,1e5],[1e5,2e5]],
                  no_angular_restriction_assumed=True,cost_scenarios=costs,
                  rates_from='c01; margin=0, so cost is illustrative and NOT final recipe budget',
                  power_check={'synthetic_trials':trials,'seed':2026100207,'one_band_successes':successes,
                               'one_band_power':successes/trials,'joint_power_union_lower_from_95pct_MC_lower':max(0.,1-4*(1-low_power))},
                  further_requirements=['source-domain and injection definition','matched same angular law in both arms','rates under final recipe','fixed N and no optional stopping'])
    write(out/'diseno-c3-condicional.json',design)
    example={'one_record_per_primary':True,'fixed_n_before_run':True,'bands':[{'name':str(i),'C':1600,'D':1600,'N_P':100000000,'N_G':10000000000,'panel_over_source_area':.01} for i in range(4)]}
    write(out/'c3-1600-ejemplo-sintetico.json',dict(evaluate_c3(example),synthetic_example_not_SC3=True))
    result={'schema':'oe1-seven-activities-analysis-v1','student_commit':'01a98718ba381797f6d4616e25d42ad533cad6f1',
            'runs':summary,'sources':sources,'geometry_sha256':hashlib.sha256(geo.read_bytes()).hexdigest(),
            'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'physical_validation':False,'production_authorized':False}
    write(out/'resumen.json',result)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('entrega','tablas','originales','salida'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();print(json.dumps(analyze(a.entrega,a.tablas,a.originales,a.salida),indent=2))

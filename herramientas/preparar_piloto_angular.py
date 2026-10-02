"""Diseño condicional del piloto de seis vistas; no envía trabajos.

Dimensiona respuesta de borde alrededor de diferencia verdadera cero, usando
una cota normal conservadora. No garantiza que la física cumpla la tolerancia.
"""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from statistics import NormalDist
import numpy as np
from referencia_cielo_angular import reference
from evaluar_bordes_angular import regions


def design(tables,geometry,helper,out):
    out.mkdir(parents=True,exist_ok=False)
    spec=importlib.util.spec_from_file_location('pilot_geometry_helper',helper)
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    geo=json.loads(geometry.read_text(encoding='utf-8'));r=reference(tables,5.,3.)
    pn=np.broadcast_to(np.array(r['nominal_probability_per_pixel_by_row'])[:,None],(256,256))
    pi=np.broadcast_to(np.array(r['ideal_selected_probability_per_pixel_by_row'])[:,None],(256,256))
    el=np.linspace(2,47,256);a=np.linspace(-30,30,257);az=(a[:-1]+a[1:])/2
    z=NormalDist().inv_cdf(1-.05/(2*16*6));zp=NormalDist().inv_cdf(1-.2/(2*15*6))
    views=[];files={}
    for view in range(6):
        opacity=c.opacidad_vista(geo,view,el,az)
        silhouette=np.array([el[opacity[:,j]>0].max() if (opacity[:,j]>0).any() else -99 for j in range(256)])
        sky=(opacity==0)&(el[:,None]>silhouette[None,:]+1)
        masks=regions(sky);sig={}
        for name,m in masks.items():
            nominal=float(pn[m].sum());selected=float(pi[m].sum())
            sig[name]=math.sqrt(selected*(1-selected))/nominal
        n=math.ceil(max(((z+zp)*(s+sig['interior'])/.01)**2 for name,s in sig.items() if name!='interior'))
        name=f'cielo-geo-train-06-view{view}.npy';np.save(out/name,sky,allow_pickle=False)
        files[name]=hashlib.sha256((out/name).read_bytes()).hexdigest()
        roi_column=c.opacidad_vista(geo,view,el.reshape(64,4).mean(1),az.reshape(64,4).mean(1))
        roi=(roi_column>=3e4)&(roi_column<1e5)
        roi_name=f'roi-roca-geo-train-06-view{view}.npy';np.save(out/roi_name,roi,allow_pickle=False)
        files[roi_name]=hashlib.sha256((out/roi_name).read_bytes()).hexdigest()
        views.append({'view':view,'events_normal_bound':n,'sky_mask':name,'rock_roi_mask':roi_name,'rock_roi_count':int(roi.sum())})
    N=math.ceil(max(v['events_normal_bound'] for v in views)/1000000)*1000000
    block_count=math.ceil(N/40000000);block_size=math.ceil(N/block_count)
    rows=[]
    for v in range(6):
        remaining=N
        for b in range(block_count):
            take=min(remaining,block_size);remaining-=take
            rows.append({'fila':len(rows),'geometria':'geo-train-06','vista':v,'bloque':b,'semilla':20261002400000+v*1000+b,'eventos':take})
    manifest=out/'manifiesto-piloto-propuesto.csv'
    with manifest.open('x',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    result={'schema':'oe1-pilot-design-v1','status':'proposed_not_authorized_for_submission','geometry':'geo-train-06',
            'events_per_view':N,'events_total':N*6,'blocks_per_view':block_count,'views':views,
            'alpha_all_six_views':.05,'alpha_per_view':.05/6,'tolerance_pp':1.,'target_joint_power_approx':.8,
            'assumed_true_border_difference_pp':0.,'planning':'normal approximation with marginal CP and Cauchy upper bound on contrast SD',
            'core_hours_illustrative_c01_rate':N*6*.0005324969/3600,
            'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
            'roi_definition':'4x4 center ray, homogeneous edifice column only, 2 m ray-march; anomalies ignored for selection, retained in transport',
            'geometry_sha256':hashlib.sha256(geometry.read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),
            'mask_sha256':files,'source_table_sha256':r['table_sha256'],
            'limits':['Conservative statistical design around ideal response; requires scientific agreement before transport.',
                      'N does not guarantee equivalence if the true response difference approaches or exceeds 1 pp.',
                      'Timing uses homogeneous c01, not measured pilot geometry performance.',
                      'No adaptive continuation until passing. One evaluation after all fixed blocks.']}
    with (out/'diseno-piloto.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('tablas','geometria','helper','salida'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();print(json.dumps(design(a.tablas,a.geometria,a.helper,a.salida),indent=2))

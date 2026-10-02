"""Reanaliza cuadrados anidados y bordes con/sin corte en la entrega f9a77ef.

Usa comun.py de esa entrega solo para calcular la columna geométrica de roca.
No ejecuta Geant4 ni declara equivalencia con un detector físico.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np
from preparar_imagen_angular_v1 import coordinates

BANDS = [(1e4,3e4),(3e4,6e4),(6e4,1e5),(1e5,2e5),(2e5,1e7)]


def digest(data): return hashlib.sha256(data).hexdigest()


def matrix(path):
    rows = path.read_text().splitlines()
    cells = [line.split(',') for line in rows]
    if len(cells)!=256 or any(len(row)!=256 for row in cells):
        raise ValueError('matriz distinta de 256x256')
    if any(not x.strip().isdigit() for row in cells for x in row):
        raise ValueError('conteo no entero o negativo')
    return np.array(cells,dtype=np.int64)


def containment(small, medium, large, opacity):
    if not (small.shape==medium.shape==large.shape==opacity.shape):
        raise ValueError('formas incompatibles')
    if np.any(small<0) or np.any(small>medium) or np.any(medium>large):
        raise ValueError('conteos no anidados')
    result=[]
    for lo,hi in BANDS:
        mask=(opacity>=lo)&(opacity<hi)
        a,b,n=(int(h[mask].sum()) for h in (small,medium,large))
        result.append({'rock_column_g_cm2':[lo,hi],'panel_1_2m':a,'plane_100m':b,'plane_600m':n,
                       'panel_over_600':a/n if n else None,'plane100_over_600':b/n if n else None})
    return result


def edges(counts, nominal, elevations, sky):
    if counts.shape!=nominal.shape or sky.shape!=counts.shape:
        raise ValueError('formas incompatibles')
    rows=(elevations>=30)&(elevations<=42)
    den=(nominal[rows]*sky[rows]).sum(0)
    if np.any(den<=0):raise ValueError('sin soporte en alguna columna')
    ratio=(counts[rows]*sky[rows]).sum(0)/den
    interior=float(ratio[20:-20].mean())
    residual=np.r_[ratio[:5],ratio[-5:]]-interior
    # Same descriptive linear extrapolation as student C4, not a physical reference.
    drow=(nominal*sky).sum(1); available=drow>0
    perrow=np.divide((counts*sky).sum(1),drow,out=np.full(256,np.nan),where=available)
    fit=available&rows
    if fit.sum()<3 or not available[-5:].all():raise ValueError('sin soporte para diagnóstico de filas')
    trend=np.polyfit(elevations[fit],perrow[fit],1)
    top=perrow[-5:]-np.polyval(trend,elevations[-5:])
    return {'interior_ratio':interior,'column_edge_residual_pp':(100*residual).tolist(),
            'column_edge_max_abs_pp':float(100*np.abs(residual).max()),
            'top_row_residual_pp':(100*top).tolist(),
            'combined_max_abs_pp':float(100*max(np.abs(top).max(),np.abs(residual).max())),
            'interpretation':'descriptive ratios; migration prevents treating these as binomial efficiencies',
            'acceptance_decision':None}


def analyze(delivery, originals):
    delivery=Path(delivery);originals=Path(originals)
    helper=delivery/'scripts/comun.py'
    spec=importlib.util.spec_from_file_location('student_geometry_helper',helper)
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    c.GEOMETRIAS=originals/'simulation/geometry_catalog/geometries'
    geom=c.GEOMETRIAS/'geo-train-01.json'
    el=np.linspace(2,47,256);az=np.linspace(-30,30,257);az=(az[1:]+az[:-1])/2
    opacity=c.opacidad_vista(json.loads(geom.read_text()),0,el,az)
    silhouette=np.array([el[opacity[:,j]>0].max() if (opacity[:,j]>0).any() else -99 for j in range(256)])
    sky=(opacity==0)&(el[:,None]>silhouette[None,:]+1)
    root=delivery/'datos/sc3/controles-30626/resultados'
    manifest={}
    for line in (root/'salidas.sha256').read_text().splitlines():
        h,p=line.split();manifest[p.removeprefix('./')]=h
    sources=[]
    def verified(p):
        raw=p.read_bytes();expected=manifest[p.relative_to(root).as_posix()]
        exact=digest(raw)==expected;lf=digest(raw.replace(b'\r\n',b'\n'))==expected
        if not exact and not lf:raise ValueError('SHA no verificable: '+str(p))
        sources.append({'file':p.relative_to(delivery).as_posix(),'received_sha256':digest(raw),
                        'sc3_sha256':expected,'crlf_to_lf_needed':not exact})
        return p
    stem='geo-train-01_view0';data={};diagnostics={}
    for run in ['c01-anidado-cono','c02-cono-margen-5deg']:
        d=root/run;meta=json.loads(verified(d/(stem+'.meta.json')).read_text());coordinates(meta)
        if meta['geometry_id']!='geo-train-01' or meta['view_index']!=0 or meta['oe1_controles']['inject']!='cone':
            raise ValueError('fuera del alcance de este diagnóstico')
        g=matrix(verified(d/(stem+'_gen.csv')))
        suffix='_hist_sub300_ecut' if run.startswith('c01') else '_hist_ecut'
        allname=stem+suffix+'0.csv' if run.startswith('c01') else stem+'_hist.csv'
        full=matrix(verified(d/allname));cut=matrix(verified(d/(stem+suffix+'3.csv')))
        if np.any(cut>full) or g.sum()>meta['events_transported']:raise ValueError('conteos incoherentes')
        data[run]=(full,cut,g)
        diagnostics[run]={'events':meta['events_transported'],'margin_deg':meta['oe1_controles']['margin_deg'],
                          'all_energies':edges(full,g,el,sky),'cut_3gev':edges(cut,g,el,sky)}
    d=root/'c01-anidado-cono'
    small=matrix(verified(d/(stem+'_hist_sub0.6_ecut3.csv')))
    medium=matrix(verified(d/(stem+'_hist_sub50_ecut3.csv')))
    large=data['c01-anidado-cono'][1]
    return {'schema':'oe1-observable-diagnostic-v1','physical_validation':False,
            'geometry':'geo-train-01','view':0,'containment_cut_3gev':containment(small,medium,large,opacity),
            'edges':diagnostics,'sources':sources,'geometry_helper_sha256':digest(helper.read_bytes()),
            'geometry_sha256':digest(geom.read_bytes()),'opacity_mask_sha256':digest(opacity.tobytes()),
            'limits':['Restricted nominal source: small-panel fraction is NOT physical detector transmission.',
                      'Margins have unequal sample sizes; no paired confidence interval or pass decision.',
                      'Ratios use arrival bins over nominal bins, with migration between bins.',
                      'No new normalization rate or physical exposure is inferred.']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('entrega',type=Path)
    p.add_argument('--originales',type=Path,default=Path(__file__).resolve().parents[1]/'objetivo-1/originales/scripts')
    p.add_argument('--salida',type=Path,required=True);a=p.parse_args()
    if a.salida.exists():raise FileExistsError(a.salida)
    result=analyze(a.entrega,a.originales)
    with a.salida.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'containment':result['containment_cut_3gev'],
                      'edges':{k:{q:v[q]['combined_max_abs_pp'] for q in ['all_energies','cut_3gev']} for k,v in result['edges'].items()}},indent=2))

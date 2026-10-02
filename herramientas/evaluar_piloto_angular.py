"""Evalúa las seis vistas fusionadas contra el diseño congelado; no habilita P1."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from preparar_imagen_angular_v1 import read_image
from evaluar_bordes_angular import evaluate
from fusionar_bloques_angular import manifest_rows


def review(fusion,design_path,reference_path):
    plan=json.loads(design_path.read_text(encoding='utf-8'));ref=json.loads(reference_path.read_text(encoding='utf-8'))
    manifest=design_path.parent/'manifiesto-piloto-propuesto.csv'
    if hashlib.sha256(manifest.read_bytes()).hexdigest()!=plan['manifest_sha256']:raise ValueError('manifiesto del diseño alterado')
    planned_rows=manifest_rows(manifest)
    if ref['margin_deg']!=5 or ref['kinetic_cut_gev']!=3 or ref['table_sha256']!=plan['source_table_sha256']:
        raise ValueError('referencia distinta del diseño')
    if sorted(v['view'] for v in plan['views'])!=list(range(6)):raise ValueError('diseño no tiene seis vistas')
    reports=[];seeds=set()
    for v in plan['views']:
        hist=fusion/plan['geometry']/f"{plan['geometry']}_view{v['view']}_hist.csv"
        _,counts,_,meta,hashes=read_image(hist)
        if meta['events_transported']!=plan['events_per_view'] or meta['geometry_sha256']!=plan['geometry_sha256'] or meta['table_sha256']!=ref['table_sha256']:
            raise ValueError('presupuesto, geometría o tablas distintos del diseño')
        if meta.get('oe1_controles')!={'inject':'cone','plane_half_m':300,'edifice_margin_m':50,'margin_deg':5,'ecuts_gev':[3],'subplanes_half_m':[]} or meta.get('reference_histogram')!='kinetic energy at the counting plane > 3 GeV':
            raise ValueError('observable distinto del diseño')
        block_seeds=meta.get('block_seeds',[])
        if len(block_seeds)!=plan['blocks_per_view'] or len(set(block_seeds))!=len(block_seeds) or seeds.intersection(block_seeds):raise ValueError('semillas ausentes o reutilizadas')
        expected_seeds={r['semilla'] for r in planned_rows if r['geometria']==plan['geometry'] and r['vista']==v['view']}
        if set(block_seeds)!=expected_seeds:raise ValueError('semillas distintas del manifiesto congelado')
        seeds.update(block_seeds)
        masks={}
        for key in ('sky_mask','rock_roi_mask'):
            p=design_path.parent/v[key]
            if hashlib.sha256(p.read_bytes()).hexdigest()!=plan['mask_sha256'][p.name]:raise ValueError('máscara alterada')
            masks[key]=np.load(p,allow_pickle=False)
        result=evaluate(counts,plan['events_per_view'],masks['sky_mask'],ref,alpha=plan['alpha_per_view'])
        roi=masks['rock_roi_mask']
        if roi.shape!=(64,64) or roi.dtype!=bool or not roi.any():raise ValueError('ROI inválida')
        values=counts.reshape(64,4,64,4).sum(axis=(1,3))[roi]
        result.update(view=v['view'],source_hashes=hashes,nominal_in_window=meta.get('nominal_in_window'),
                      conventional_exposure_days=meta.get('conventional_exposure_days'),
                      rock_roi={'definition':plan['roi_definition'],'count':int(roi.sum()),'median_counts':float(np.median(values)),
                                'q10_counts':float(np.quantile(values,.1)),'fraction_at_least_100':float(np.mean(values>=100))})
        reports.append(result)
    return {'schema':'oe1-pilot-review-v1','views':reports,'all_border_regions_equivalent':all(r['all_equivalent'] for r in reports),
            'physical_validation':False,'production_authorized':False,
            'next':'Review source/reference limitations, rock statistics and observed timing before deciding production; no automatic P1.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('fusion','diseno','referencia','salida'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();result=review(a.fusion,a.diseno,a.referencia)
    with a.salida.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,allow_nan=False)

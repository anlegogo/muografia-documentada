"""Auditoría de campaña fija; nunca autoriza producción ni cambia N."""
import argparse
import json
from pathlib import Path
import numpy as np
from preparar_campana_114 import sha
from preparar_campana_angular import preflight
from fusionar_bloques_angular import manifest_rows
from preparar_imagen_angular_v1 import read_image
from configuracion_angular import configuration
from evaluar_bordes_angular import evaluate

def review(fusion, plan_path, recipe_path, reference_path):
    plan=json.loads(plan_path.read_text(encoding='utf-8'));base=plan_path.parent
    recipe=json.loads(recipe_path.read_text(encoding='utf-8'));reference=json.loads(reference_path.read_text(encoding='utf-8'))
    manifest=base/'manifiesto-114-344M.csv'
    if sha(manifest)!=plan['manifest_sha256'] or sha(recipe_path)!=plan['recipe_sha256']:
        raise ValueError('Manifiesto o receta distintos del plan')
    scope=[g['geometry'] for g in plan['geometries']]
    pf=preflight(manifest,scope)
    if not pf['technical_manifest_complete'] or len(pf['views'])!=114 or any(v['events']!=plan['events_per_view'] for v in pf['views']):
        raise ValueError('Plan incompleto o presupuesto distinto')
    if reference['table_sha256']!=recipe['table_sha256'] or reference['margin_deg']!=5 or reference['kinetic_cut_gev']!=3:
        raise ValueError('Referencia incompatible')
    rows=manifest_rows(manifest); reports=[];missing=[];errors=[];signatures=set()
    for g in plan['geometries']:
        masks={}
        for key in ('sky','rock_roi'):
            path=base/g[key]
            if sha(path)!=plan['masks_sha256'][g[key]]:raise ValueError('Máscara alterada')
            masks[key]=np.load(path,allow_pickle=False)
        for view in range(6):
            key=f"{g['geometry']}_view{view}";path=fusion/g['geometry']/(key+'_hist.csv')
            if not path.exists():missing.append(key);continue
            try:
                _,counts,_,meta,hashes=read_image(path)
                expected=[r['semilla'] for r in rows if r['geometria']==g['geometry'] and r['vista']==view]
                if meta['events_transported']!=plan['events_per_view'] or meta['geometry_sha256']!=g['geometry_sha256']:
                    raise ValueError('Geometría o N distintos')
                if sorted(meta.get('block_seeds',[]))!=sorted(expected):raise ValueError('Semillas distintas')
                for field,expected_value in [('binary_sha256',recipe['reported_binary_sha256']),('table_sha256',recipe['table_sha256']),('oe1_controles',recipe['oe1_controles']),('source_definition',recipe['source_definition']),('normalization',recipe['normalization']),('reference_histogram',recipe['reference_histogram'])]:
                    if meta.get(field)!=expected_value:raise ValueError('Receta distinta: '+field)
                signatures.add(json.dumps(configuration(meta),sort_keys=True))
                border=evaluate(counts,plan['events_per_view'],masks['sky'],reference,alpha=plan['alpha_per_view'],tolerance=plan['border_tolerance'])
                roi=counts.reshape(64,4,64,4).sum(axis=(1,3))[masks['rock_roi']]
                fraction=float(np.mean(roi>=plan['rock_min_counts']))
                reports.append({'geometry':g['geometry'],'view':view,'source_hashes':hashes,'borders':border,
                    'rock':{'roi_count':len(roi),'median':float(np.median(roi)),'q10':float(np.quantile(roi,.1)),
                    'fraction_ge100':fraction,'descriptive_criterion_met':fraction>=plan['rock_min_fraction']}})
            except (ValueError,KeyError,TypeError,OSError) as exc:errors.append({'view':key,'error':str(exc)})
    if len(signatures)>1:errors.append({'error':'Configuraciones incompatibles entre vistas'})
    expected_files={f"{g['geometry']}_view{v}_hist.csv" for g in plan['geometries'] for v in range(6)}
    if any(p.name not in expected_files for p in fusion.rglob('*_hist.csv')):errors.append({'error':'Histogramas fuera del alcance'})
    complete=len(reports)==114 and not missing and not errors
    return {'schema':'oe1-campaign-114-review-v1','technical_complete':complete,'missing':missing,'errors':errors,'views':reports,
        'all_border_criteria_met':complete and all(v['borders']['all_equivalent'] for v in reports),
        'all_rock_descriptive_criteria_met':complete and all(v['rock']['descriptive_criterion_met'] for v in reports),
        'physical_validation':False,'production_authorized':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('fusion','plan','receta','referencia','salida'):p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();result=review(a.fusion,a.plan,a.receta,a.referencia)
    with a.salida.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='views'},indent=2))
    raise SystemExit(0 if result['technical_complete'] else 1)

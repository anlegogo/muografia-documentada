"""Preparación offline del candidato 344 M; no envía trabajos ni autoriza SC3."""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import numpy as np
from preparar_campana_angular import preflight
from evaluar_bordes_angular import regions

ROOT = Path(__file__).resolve().parents[1]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def prepare(helper, out):
    out.mkdir(parents=True, exist_ok=False)
    spec = importlib.util.spec_from_file_location('geometry_helper', helper)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    catalog = ROOT/'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries'
    recipe_path = ROOT/'objetivo-1/contratos/receta-operativa-siete-actividades.json'
    recipe = json.loads(recipe_path.read_text(encoding='utf-8'))
    el = np.linspace(2,47,256); edges = np.linspace(-30,30,257); az = (edges[:-1]+edges[1:])/2
    rows = []; geometries = []; masks = {}; events = 344_000_000
    for gi, path in enumerate(sorted(catalog.glob('*.json'))):
        geo = json.loads(path.read_text(encoding='utf-8')); gid = geo['geometry_id']
        assert sha(path) == recipe['geometry_sha256'][path.name]
        # Cono homogéneo circular: estas máscaras son invariantes por rotación.
        opacity = module.opacidad_vista(geo,0,el,az)
        silhouette = np.array([el[opacity[:,j]>0].max() if (opacity[:,j]>0).any() else -99 for j in range(256)])
        sky = (opacity==0)&(el[:,None]>silhouette[None,:]+1)
        regions(sky)  # no permitir regiones de borde sin soporte
        columns = module.opacidad_vista(geo,0,el.reshape(64,4).mean(1),az.reshape(64,4).mean(1))
        roi = (columns>=30000)&(columns<100000)
        if not roi.any(): raise ValueError('Sin ROI: '+gid)
        paths = {}
        for name, data in [('sky',sky),('rock_roi',roi)]:
            filename = gid+'-'+name+'.npy'; np.save(out/filename,data,allow_pickle=False)
            masks[filename] = sha(out/filename); paths[name] = filename
        rock = columns[columns>0]
        geometries.append({'geometry':gid,'geometry_sha256':sha(path),**paths,
            'edifice':geo['edifice'],'anomalies':len(geo['anomalies']),
            'anomaly_density_range':[min([a['density_g_cm3'] for a in geo['anomalies']],default=geo['edifice']['rock_density_g_cm3']),max([a['density_g_cm3'] for a in geo['anomalies']],default=geo['edifice']['rock_density_g_cm3'])],
            'rock_roi_count':int(roi.sum()),'nominal_rock_q90_g_cm2':float(np.quantile(rock,.9)),
            'nominal_rock_max_g_cm2':float(rock.max()),'nominal_rock_fraction_above_100k':float(np.mean(rock>=100000))})
        for view in range(6):
            remaining = events
            for block in range(9):
                take = min(remaining,math.ceil(events/9)); remaining -= take
                rows.append(dict(fila=len(rows),geometria=gid,vista=view,bloque=block,
                    semilla=20261002600000+gi*10000+view*100+block,eventos=take))
    if len(geometries)!=19: raise ValueError('Catálogo distinto de 19')
    manifest = out/'manifiesto-114-344M.csv'
    with manifest.open('x',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    check=preflight(manifest,[g['geometry'] for g in geometries]);assert check['technical_manifest_complete']
    (out/'preflight.json').write_text(json.dumps(check,indent=2)+'\n',encoding='utf-8')
    result={'schema':'oe1-campaign-114-v1','status':'prepared_candidate_not_submission_authorization',
        'events_per_view':events,'expected_views':114,'expected_pairs':9120,'blocks_per_view':9,
        'events_total':sum(r['eventos'] for r in rows),'manifest_sha256':sha(manifest),
        'recipe_sha256':sha(recipe_path),'helper_sha256':sha(helper),'masks_sha256':masks,'geometries':geometries,
        'alpha_all_114_views':.05,'alpha_per_view':.05/114,'border_tolerance':.01,
        'rock_min_counts':100,'rock_min_fraction':.9,
        'rock_criterion_interpretation':'Observed descriptive sufficiency in 4x4 nominal 30k-100k ROI, not confidence on latent rates or per-pixel accuracy.',
        'mask_definition':'Homogeneous cone only; 2 m ray march; circular symmetry used for six views; anomalies retained in actual transport but ignored in masks.',
        'pilot_reuse':False,'physical_validation':False,'production_authorized':False,
        'limitations':['344 M does not guarantee rock criterion across geometries.',
            'Do not increase N until pass; retain and report failures.',
            'Pilot is separate. Fresh campaign avoids changing its receipts, seeds or output roots.']}
    (out/'plan.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--helper',type=Path,required=True);p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args();r=prepare(a.helper,a.salida);print(json.dumps({k:r[k] for k in ['expected_views','events_total','production_authorized']}))

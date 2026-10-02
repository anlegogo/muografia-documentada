"""Preflight offline: alcance, presupuestos e integridad de bloques existentes.

No consulta colas, no lanza trabajos y nunca autoriza producción física.
"""
import argparse
import hashlib
import json
from pathlib import Path
from fusionar_bloques_angular import manifest_rows,validate_block


def preflight(manifest,geometries,blocks=None,accept_crlf=False):
    rows=manifest_rows(manifest)
    if not geometries or len(set(geometries))!=len(geometries):raise ValueError('alcance vacío o repetido')
    canonical=json.dumps(rows,sort_keys=True,separators=(',',':')).encode()
    campaign=hashlib.sha256(canonical).hexdigest()
    report={'schema':'oe1-offline-preflight-v1','campaign_id':campaign,'submission_authorized':False,
       'physical_validation':False,'queue_inspected':False,'scope':sorted(geometries),'errors':[],
       'views':[],'blocks':[],'manifest_sha256':hashlib.sha256(Path(manifest).read_bytes()).hexdigest()}
    groups={};signatures={}
    for r in rows:
        key=(r['geometria'],r['vista']);groups.setdefault(key,[]).append(r)
        if key[0] not in geometries:report['errors'].append('geometría fuera del alcance: '+key[0])
        state='not_inspected'
        if blocks is not None:
            d=Path(blocks)/key[0]/f'view{key[1]}'/f"block{r['bloque']:04d}"
            if not d.exists():state='absent'
            else:
                try:
                    block=validate_block(r,blocks,accept_crlf)
                    state='verified'
                    signatures.setdefault(key[0],set()).add(block['signature'])
                except (OSError,ValueError,KeyError,TypeError) as exc:
                    state='invalid';report['errors'].append(f"fila {r['fila']}: {exc}")
        report['blocks'].append({'row':r['fila'],'state':state,'suggested_job_name':f"oe1-{campaign[:12]}-{r['fila']}"})
    for geo,sigs in signatures.items():
        if len(sigs)>1:report['errors'].append('configuración mezclada: '+geo)
    for (geo,view),rr in sorted(groups.items()):
        indices=sorted(r['bloque'] for r in rr)
        if indices!=list(range(len(rr))):report['errors'].append(f'{geo}/{view}: secuencia de bloques incompleta')
        report['views'].append({'geometry':geo,'view':view,'blocks':len(rr),'events':sum(r['eventos'] for r in rr)})
    missing=[{'geometry':g,'view':v} for g in sorted(geometries) for v in range(6) if (g,v) not in groups]
    totals={v['events'] for v in report['views']}
    if len(totals)>1:report['errors'].append('presupuestos por vista diferentes: requieren alcance separado')
    report.update(missing_views=missing,total_blocks=len(rows),total_events=sum(r['eventos'] for r in rows),
                  technical_manifest_complete=not missing and not report['errors'])
    report['all_blocks_verified']=report['technical_manifest_complete'] and all(b['state']=='verified' for b in report['blocks'])
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifiesto',type=Path)
    p.add_argument('--geometrias',nargs='+');p.add_argument('--bloques',type=Path)
    p.add_argument('--aceptar-crlf',action='store_true');p.add_argument('--informe',type=Path,required=True);a=p.parse_args()
    if a.informe.exists():raise FileExistsError(a.informe)
    scope=a.geometrias or sorted(x.stem for x in (Path(__file__).resolve().parents[1]/'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries').glob('*.json'))
    result=preflight(a.manifiesto,scope,a.bloques,a.aceptar_crlf)
    with a.informe.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ['blocks','views']},indent=2))
    raise SystemExit(0 if result['technical_manifest_complete'] else 1)

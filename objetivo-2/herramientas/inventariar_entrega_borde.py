"""Inventario reproducible de la entrega E1; los binarios grandes permanecen fuera de Git."""
import argparse,json
from pathlib import Path
from datos_ajuste import digest,read_json,atomic_json
from revisar_borde_cgan import audit_technical,load_completed
from ejecutar_borde_cgan import PAIR_SEEDS,configure
from resumir_borde_cgan import run as summarize
from types import SimpleNamespace

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['raiz','mascaras','salida']:p.add_argument('--'+n,type=Path,required=True)
 p.add_argument('--etapa',choices=['tecnica','piloto'],required=True)
 a=p.parse_args();configure()
 if a.salida.exists():raise FileExistsError('Inventario requiere archivo nuevo')
 files=[];gates={};mask_identity=digest(a.mascaras/'manifest.json')
 def add(path,logical):
  if not path.is_file():raise FileNotFoundError(path)
  files.append({'path':logical,'bytes':path.stat().st_size,'sha256':digest(path),'storage':'drive' if logical.startswith('mascaras-ajuste-v1/') or path.suffix in ('.pt','.npy','.npz') else 'git'})
 for pair in PAIR_SEEDS:
  paths={arm+'-'+mode:a.raiz/pair/'tecnica'/(arm+'-'+mode) for arm in ['C0','C1'] for mode in ['continua','recuperada']}
  gate=audit_technical(paths,require_gpu=a.etapa=='piloto',pair=pair);gates[pair]={'exact_recovery':gate['exact_recovery'],'gpu_accepted':gate['gpu_accepted']}
  if any(i['cache_sha256']!=mask_identity for i in gate['identities']):raise ValueError('Caché distinta de la usada en la prueba')
  for arm in ['C0','C1']:
   if a.etapa=='piloto':load_completed(a.raiz/pair/'piloto'/arm,arm,'piloto',pair)
  for stage in ['tecnica']+(['piloto'] if a.etapa=='piloto' else []):
   for folder in sorted((a.raiz/pair/stage).iterdir()):
    if not folder.is_dir():continue
    for name in ['last.pt','predicciones-val.npy','indices-val.json','identity.json','history.json','summary.json','exports.json','last-session.json']:
     path=folder/name;add(path,path.relative_to(a.raiz).as_posix())
  evaluation=a.raiz/pair/'evaluacion'
  for name in ['comparacion-cgan.json','anomalias-cgan.json','predicciones-cgan-inicial.npy']+([f'geo-val-{i:02}.png' for i in range(1,4)] if a.etapa=='piloto' else []):
   add(evaluation/name,(evaluation/name).relative_to(a.raiz).as_posix())
  acceptance=a.raiz/pair/('aceptacion-gpu.json' if a.etapa=='piloto' else 'aceptacion-cpu.json')
  saved=read_json(acceptance)
  if saved['checkpoint_sha256']!=gate['checkpoint_sha256'] or saved['gpu_accepted']!=gate['gpu_accepted']:raise ValueError('Aceptación guardada distinta de los artefactos')
  add(acceptance,acceptance.relative_to(a.raiz).as_posix())
 # Recompute decision and all source/checkpoint checks; output kept next to inventory.
 derived=a.salida.with_name(a.salida.stem+'-sintesis.json')
 summarize(SimpleNamespace(raiz=a.raiz,etapa=a.etapa,salida=derived))
 cache=read_json(a.mascaras/'manifest.json')
 add(a.mascaras/'manifest.json','mascaras-ajuste-v1/manifest.json')
 for value in cache['geometries'].values():
  path=a.mascaras/value['mask_file']
  if digest(path)!=value['mask_sha256']:raise ValueError('Máscara alterada')
  add(path,'mascaras-ajuste-v1/'+path.name)
 for path in sorted((a.raiz/'logs').glob('*.log')):add(path,'logs/'+path.name)
 for path in sorted(a.raiz.glob('*.log')):add(path,'logs-locales/'+path.name)
 report={'schema':'oe2-edge-delivery-inventory-v1','stage':a.etapa,'physical_acceptance':False,'technical_gates':gates,'files':files,'binary_files':sum(x['storage']=='drive' for x in files),'total_bytes':sum(x['bytes'] for x in files),'instructions':'Preserve relative paths; upload Drive binaries and add accessible links without changing SHA256. Commit text, logs, inventory and report to delivery branch.'}
 a.salida.parent.mkdir(parents=True,exist_ok=True);atomic_json(a.salida,report)
 print(json.dumps({'files':len(files),'binary_files':report['binary_files'],'bytes':report['total_bytes']}))
if __name__=='__main__':main()


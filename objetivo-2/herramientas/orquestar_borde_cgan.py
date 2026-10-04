"""Orquestación acotada E1. No contrata GPU ni cambia el protocolo."""
import argparse,json,subprocess,sys
from pathlib import Path
import ejecutar_borde_cgan as e
import revisar_borde_cgan as review
from datos_ajuste import read_json,atomic_json

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--fase',choices=['tecnica','piloto','evaluacion','sintesis'],required=True)
 p.add_argument('--pareja',choices=list(e.PAIR_SEEDS))
 for n in ['datos','mascaras','pesos','raiz']:p.add_argument('--'+n,type=Path,required=True)
 p.add_argument('--cpu-test',action='store_true')
 a=p.parse_args()
 if a.cpu_test and a.fase not in ['tecnica']:raise ValueError('CPU-test solo para prueba técnica; evaluación técnica se reproduce con el evaluador directamente')
 if a.fase!='sintesis' and a.pareja is None:raise ValueError('Falta pareja')
 e.configure();h=Path(e.__file__).parent
 common=['--datos',str(a.datos),'--mascaras',str(a.mascaras),'--pesos',str(a.pesos)]
 pair=a.pareja;root=a.raiz.resolve()
 def call(tool,args,label):
  logs=root/'logs';logs.mkdir(parents=True,exist_ok=True)
  n=0;path=logs/(label+'.log')
  while path.exists():n+=1;path=logs/(label+f'-intento{n}.log')
  with path.open('w',encoding='utf-8') as f:
   result=subprocess.run([sys.executable,str(h/tool)]+args,stdout=f,stderr=subprocess.STDOUT)
  if result.returncode:raise RuntimeError(f'Fallo en {label}; detenerse y revisar {path}')
  print(label+' completado',flush=True)
 if a.fase=='tecnica':
  folder=root/pair/'tecnica'
  if folder.exists():raise FileExistsError('La prueba técnica requiere una carpeta nueva; conservar el fallo previo y reportarlo')
  (root/pair).mkdir(parents=True,exist_ok=True)
  for arm in ['C0','C1']:
   base=common+['--pareja',pair,'--rama',arm,'--etapa','tecnica']+(['--cpu-test'] if a.cpu_test else [])
   for mode in ['continua','recuperada']:
    dst=folder/(arm+'-'+mode)
    call('ejecutar_borde_cgan.py',base+['--salida',str(dst)]+(['--parar-tras','1'] if mode=='recuperada' else []),pair+'-'+arm+'-'+mode+'-inicio')
    if mode=='recuperada':call('ejecutar_borde_cgan.py',base+['--salida',str(dst),'--reanudar'],pair+'-'+arm+'-recuperada-fin')
  paths={arm+'-'+mode:folder/(arm+'-'+mode) for arm in ['C0','C1'] for mode in ['continua','recuperada']}
  gate=review.audit_technical(paths,require_gpu=not a.cpu_test,pair=pair)
  atomic_json(root/pair/('aceptacion-cpu.json' if a.cpu_test else 'aceptacion-gpu.json'),gate)
 elif a.fase=='piloto':
  # Las tres parejas deben superar su prueba antes del primer piloto.
  reference_identity=None
  for other in e.PAIR_SEEDS:
   gate=read_json(root/other/'aceptacion-gpu.json')
   if gate.get('schema')!='oe2-cgan-borde-gate-v1' or not gate.get('gpu_accepted') or gate.get('pair')!=other:raise ValueError('Aceptación GPU nueva ausente o incompatible')
   actual=review.audit_technical(gate['runs'],require_gpu=True,pair=other)
   if actual['checkpoint_sha256']!=gate['checkpoint_sha256']:raise ValueError('Evidencia técnica alterada')
   current=actual['identities'][0]
   if reference_identity is None:reference_identity=current
   for key in ['sources','environment','cache_sha256','data_manifest_sha256','initial_checkpoint_sha256']:
    if current[key]!=reference_identity[key]:raise ValueError('Parejas con entorno/datos/fuentes distintos: '+key)
  (root/pair).mkdir(parents=True,exist_ok=True)
  for arm in ['C0','C1']:
   dst=root/pair/'piloto'/arm;extra=[]
   if (dst/'last.pt').exists():
    import torch
    state=torch.load(dst/'last.pt',map_location='cpu',weights_only=True);review.validate_state(state)
    if state['epoch']==5:
     review.load_completed(dst,arm,'piloto',pair);print(pair+' '+arm+' ya completo y verificado',flush=True);continue
    extra=['--reanudar']
   call('ejecutar_borde_cgan.py',common+['--pareja',pair,'--rama',arm,'--etapa','piloto','--salida',str(dst),'--aceptacion-gpu',str(root/pair/'aceptacion-gpu.json')]+extra,pair+'-'+arm+'-piloto')
 elif a.fase=='evaluacion':
  call('evaluar_borde_cgan.py',common+['--pareja',pair,'--etapa','piloto','--dispositivo','cuda','--control',str(root/pair/'piloto/C0'),'--regional',str(root/pair/'piloto/C1'),'--salida',str(root/pair/'evaluacion'),'--figuras'],pair+'-evaluacion')
 else:
  call('resumir_borde_cgan.py',['--raiz',str(root),'--etapa','piloto','--salida',str(root/'sintesis-borde.json')],'sintesis-borde')
if __name__=='__main__':main()


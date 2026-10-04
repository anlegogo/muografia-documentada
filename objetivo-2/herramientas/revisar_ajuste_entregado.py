"""Revisión independiente de binarios e inferencia del ajuste A/B; no entrena."""
import argparse,json,sys,time,hashlib,copy
from pathlib import Path
import numpy as np
import torch
p=argparse.ArgumentParser()
for n in ['repo','datos','mascaras','entrega','salida']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();a.salida.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(a.repo/'objetivo-2/herramientas'))
from datos_ajuste import Store,sources,spec,read_json,digest,atomic_json
from revisar_ajuste import audit_technical,load_completed
from ejecutar_ajuste import build_generator,evaluate,state_digest,environment
from evaluar_ajuste import analyze_predictions
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
torch.backends.mkldnn.enabled=True
store=Store(a.datos,a.mascaras)
reported=read_json(a.entrega/'manifiesto-mascaras.json')
local=copy.deepcopy(store.manifest);remote=copy.deepcopy(reported)
for obj in [local,remote]:
 for v in obj['geometries'].values():v.pop('mask_sha256')
if local!=remote:raise ValueError('Máscaras no equivalentes')
report={'schema':'oe2-independent-adjustment-review-v1','heldout_opened':False,'training_performed':False,'environment':environment(torch.device('cpu')),'local_mask_manifest_sha256':store.identity,'reported_mask_manifest_sha256':digest(a.entrega/'manifiesto-mascaras.json'),'mask_content_identical':True,'mask_npz_bytes_identical':False,'source_sha256':sources(),'inference':{}}
gate=audit_technical({k:a.entrega/'tecnica'/k for k in ['A-continua','A-recuperada','B-continua','B-recuperada']},require_gpu=True)
report['gpu_artifacts_audited']={k:gate[k] for k in ['technical_checks_passed','gpu_accepted','exact_recovery','checkpoint_sha256']}
atomic_json(a.salida/'revision.json',report)
print('Cuatro checkpoints técnicos: recuperación exacta verificada.',flush=True)
preds={};keys=None
for arm in ['A','B']:
 run=a.entrega/'piloto'/arm;c=load_completed(run,arm,'piloto',sources())
 if c['identity']['cache_sha256']!=report['reported_mask_manifest_sha256']:raise ValueError('Manifiesto entregado distinto del checkpoint')
 if state_digest(c['generator'])!=c['history'][-1]['generator_sha256']:raise ValueError('Digest del generador incorrecto')
 net=build_generator(spec(arm)['generator']);net.load_state_dict(c['generator'],strict=True)
 rows=store.indices('val',spec(arm),'piloto');t=time.perf_counter()
 metrics,pred,rows=evaluate(net,store,rows,torch.device('cpu'))
 published=np.load(run/'predicciones-val.npy',allow_pickle=False)
 delta=np.abs(pred.astype(float)-published.astype(float))
 info={'checkpoint_sha256':digest(run/'last.pt'),'published_predictions_sha256':digest(run/'predicciones-val.npy'),'images':len(rows),'metrics':metrics,'seconds':time.perf_counter()-t,'max_abs_pixel_difference':float(delta.max()),'mean_abs_pixel_difference':float(delta.mean()),'ssim_difference':metrics['ssim']-c['history'][-1]['validation']['ssim'],'psnr_difference':metrics['psnr']-c['history'][-1]['validation']['psnr'],'pixel_tolerance':1e-5,'ssim_tolerance':1e-6,'psnr_tolerance':1e-4}
 info['within_tolerance']=info['max_abs_pixel_difference']<=1e-5 and abs(info['ssim_difference'])<=1e-6 and abs(info['psnr_difference'])<=1e-4
 if not info['within_tolerance']:raise ValueError('Inferencia fuera de tolerancia: '+str(info))
 np.save(a.salida/f'{arm}-predicciones-cpu.npy',pred);preds[arm]=pred
 report['inference'][arm]=info;atomic_json(a.salida/'revision.json',report);print(json.dumps({arm:info}),flush=True)
 keys=[list(x) for x in rows];del net,c,published,delta
published_preds={arm:np.load(a.entrega/'piloto'/arm/'predicciones-val.npy',allow_pickle=False,mmap_mode='r') for arm in ['A','B']}
recomputed=analyze_predictions(store,keys,published_preds,'piloto')
original=read_json(a.entrega/'comparacion-piloto.json')
diffs=[]
def compare(x,y,path=''):
 if isinstance(x,dict):
  if x.keys()!=y.keys():raise ValueError('Campos distintos '+path)
  for k in x:compare(x[k],y[k],path+'/'+k)
 elif isinstance(x,list):
  if len(x)!=len(y):raise ValueError('Longitud distinta '+path)
  for i,(xx,yy) in enumerate(zip(x,y)):compare(xx,yy,path+'/'+str(i))
 elif isinstance(x,(int,float)) and not isinstance(x,bool):
  diffs.append(abs(x-y))
 elif x!=y:raise ValueError('Valor distinto '+path)
for key in ['images','regions','contrasts','summary','decision_checks','decision']:compare(recomputed[key],original[key],key)
report['published_evaluation_recalculation']={'numeric_values':len(diffs),'max_difference':max(diffs),'within_tolerance':max(diffs)<=1e-12,'decision':recomputed['decision']}
if max(diffs)>1e-12:raise ValueError('Evaluación publicada no reproducida')
atomic_json(a.salida/'evaluacion-predicciones-publicadas.json',recomputed)
cpu=analyze_predictions(store,keys,preds,'piloto');atomic_json(a.salida/'evaluacion-predicciones-cpu.json',cpu)
report['cpu_decision']=cpu['decision']
report['published_summary']=recomputed['summary']
atomic_json(a.salida/'revision.json',report)
print(json.dumps({'evaluation_max_difference':max(diffs),'decision':cpu['decision'],'complete':True}),flush=True)


"""Revisión descriptiva, sin inferencia ni selección de pesos."""
import argparse,ast,csv,json,math,hashlib
from pathlib import Path
from collections import defaultdict
import numpy as np
ROOT=Path(__file__).parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--reported',type=Path,default=ROOT/'descarga/informe')
p.add_argument('--reproduced',type=Path,default=ROOT/'reproduccion')
p.add_argument('--output',type=Path,default=ROOT/'publicacion')
p.add_argument('--config',type=Path,required=True)
args=p.parse_args()
def read(p):return json.loads(p.read_bytes())
def csvread(p):
 with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
reported=args.reported; reproduced=args.reproduced
differences=[];equal=0
def compare(a,b,path=''):
 global equal
 if isinstance(a,dict) and isinstance(b,dict):
  assert set(a)==set(b),path
  for k in a:
   if k=='environment':continue
   compare(a[k],b[k],path+'/'+k)
 elif isinstance(a,list) and isinstance(b,list):
  assert len(a)==len(b),path
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
 elif isinstance(a,(float,int)) and not isinstance(a,bool) and isinstance(b,(float,int)):
  assert math.isfinite(a) and math.isfinite(b),path
  d=abs(a-b)
  assert d<=1e-10+1e-10*abs(a),(path,a,b)
  if d: differences.append({'path':path,'absolute_difference':d,'scaled_difference':d/max(1,abs(a))})
  else:equal+=1
 else:assert a==b,(path,a,b)
for name in ['resultado.json','contrastes.json','snr_repeticiones.json']:
 compare(read(reported/name),read(reproduced/name),name)
for name in ['imagenes.csv','regiones.csv','metricas_locales.csv']:
 a,b=csvread(reported/name),csvread(reproduced/name)
 assert len(a)==len(b),name
 for i,(x,y) in enumerate(zip(a,b)):
  assert x.keys()==y.keys()
  for k in x:
   try:v,w=float(x[k]),float(y[k])
   except ValueError:
    if x[k].startswith('[') and y[k].startswith('['):v,w=ast.literal_eval(x[k]),ast.literal_eval(y[k])
    else:v,w=x[k],y[k]
   compare(v,w,name+'/'+str(i)+'/'+k)
out=args.output;out.mkdir(parents=True,exist_ok=True)
report={'delivery_commit':'5c3b0ee6cc305d13b34f70b19c82c63489794206','code_commit':'39d8fd3e398a540ea42e025fce8c42fa25986dfa','numeric_tolerance':{'absolute':1e-10,'relative':1e-10},'tolerance_purpose':'comparación numérica entre entornos; no aceptación científica','all_tables_and_json_match':True,'numeric_equal':equal,'numeric_different':len(differences),'maximum_absolute_difference':max((x['absolute_difference'] for x in differences),default=0),'maximum_scaled_difference':max((x['scaled_difference'] for x in differences),default=0),'largest_differences':sorted(differences,key=lambda x:x['absolute_difference'],reverse=True)[:10],'reported_environment':read(reported/'resultado.json')['environment'],'reproduced_environment':read(reproduced/'resultado.json')['environment'],'new_inference_performed':False,'new_training_performed':False}
(out/'reproduccion.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
result=read(reproduced/'resultado.json');local=csvread(reproduced/'metricas_locales.csv')
for r in local:
 r['fraction']=float(r['fraction']);r['view']=int(r['view'])
key=lambda r:(r['geometry'],r['view'],r['region'])
ref={key(r):r for r in local if r['model']=='referencia' and r['fraction']==.05}
models=list(result['summary']['0.05']['test'])
summary=[]
metrics=['snr_local_intensity','cnr_local_signed','contrast_counts']
for fraction in result['fractions']:
 for split in ['test','generalization']:
  for model in models:
   row={'fraction':fraction,'split':split,'model':model}
   for metric in metrics:
    support={tuple(k) for k in result['common_local_support'][metric]}
    groups=defaultdict(list)
    for r in local:
     if r['fraction']!=fraction or r['model']!=model or key(r) not in support:continue
     if ('test' in r['geometry'])!=(split=='test'):continue
     value=float(r[metric]);truth=float(ref[key(r)][metric]);groups[key(r)].append((value,truth))
    bygeo=defaultdict(list)
    for k,values in groups.items():
     assert len(values)==20
     a=np.array(values);bygeo[k[0]].append({'mean':float(a[:,0].mean()),'mae_reference':float(np.abs(a[:,0]-a[:,1]).mean()),'opposite_sign_fraction':float(np.mean(a[:,0]*a[:,1]<0))})
    row[metric+'_support']=len(groups)
    for field in ['mean','mae_reference','opposite_sign_fraction']:
     row[metric+'_'+field]=float(np.mean([np.mean([v[field] for v in vv]) for vv in bygeo.values()]))
   agg=result['summary'][str(fraction)][split][model]
   for metric in ['ssim_macro','psnr_macro','Q_macro']:row[metric]=agg[metric]
   summary.append(row)
with (out/'sintesis_metricas.csv').open('w',encoding='utf-8',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
metadata={'aggregation':'media de 20 realizaciones por región/vista; media por geometría; media equiponderada de geometrías por partición','common_support_per_metric':result['common_local_support'],'reference_fraction_used':.05,'reference_note':'la imagen de referencia es idéntica en las cuatro fracciones; se cuenta una sola vez','sign_rule':'producto de contraste/CNR predicho y referencia estrictamente negativo; no se usa margen post-hoc','interpretation':'SNR espacial y CNR son descriptivos; mayor cociente no acredita detección ni opacidad. Error de contraste adimensional. No se seleccionan modelos.'}
(out/'metodo_sintesis.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
config=read(args.config)
assert hashlib.sha256(args.config.read_bytes()).hexdigest()==result['complement_sha256']
imagegroups=defaultdict(list)
for r in csvread(reproduced/'imagenes.csv'):
 if r['model']!='entrada':imagegroups[(float(r['fraction']),r['geometry'],r['model'],int(r['view']))].append(r)
checks=[]
for (fraction,geometry,model,view),rr in sorted(imagegroups.items()):
 assert len(rr)==20
 threshold=config['image_benchmark_thresholds'][geometry][str(view)]
 row={'fraction':fraction,'geometry':geometry,'model':model,'view':view}
 for metric in ['ssim','psnr']:
  row[metric]=float(np.mean([float(r[metric]) for r in rr]));row[metric+'_threshold']=threshold[metric]
 row['passes_both']=all(row[m]+1e-12>=threshold[m] for m in ['ssim','psnr']);checks.append(row)
assert len(checks)==768
with (out/'benchmark_por_vista.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
report['benchmark_model_fraction_views']=len(checks);report['views_passing_both']=sum(r['passes_both'] for r in checks)
(out/'reproduccion.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
print(json.dumps([r for r in summary if r['model'] in ['entrada','cgan_original'] and r['fraction'] in [.01,.05,.5]],ensure_ascii=False))

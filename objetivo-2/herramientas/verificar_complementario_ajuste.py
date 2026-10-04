"""Contraste independiente del CSV y sus intervalos descriptivos."""
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser()
for n in ['repo','datos','mascaras','entrega','salida']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();sys.path.insert(0,str(a.repo/'objetivo-2/herramientas'))
from datos_ajuste import Store,read_json,atomic_json
store=Store(a.datos,a.mascaras)
rows=list(csv.DictReader((a.entrega/'analisis-complementario/cuentas-por-imagen.csv').open(encoding='utf-8')))
lookup={(r['geometry'],int(r['view']),int(r['realization']),r['model']):r for r in rows}
keys=read_json(a.entrega/'piloto/A/indices-val.json')
pred={m:np.load(a.entrega/'piloto'/m/'predicciones-val.npy',mmap_mode='r') for m in ['A','B']}
diffs=[]
for i,(g,v,k) in enumerate(keys):
 ref,low=store.load(g);ref=ref[v].astype(float)
 info=store.manifest['geometries'][g];families={}
 for j,f in enumerate(info['families']):families.setdefault(f,np.zeros((256,256),bool));families[f]|=store.masks[g][v,j]
 for m in ['entrada','A','B']:
  if m=='entrada':c=low[v,k].astype(float)/.05
  else:
   z=pred[m][i].astype(float);c=np.expm1(store.scale*z/(1-z))
  calculated={'total_rel_error':float((c.sum()-ref.sum())/ref.sum())}
  for f,name in enumerate(['cielo','roca','borde','anomalias']):
   mask=families[f];calculated['rel_error_'+name]=float((c[mask].sum()-ref[mask].sum())/ref[mask].sum())
  diffs.extend(abs(value-float(lookup[g,v,k,m][key])) for key,value in calculated.items())
report=read_json(a.entrega/'analisis-complementario/cuentas-complementario.json')
metrics=['total_rel_error','rel_error_cielo','rel_error_roca','rel_error_borde','rel_error_anomalias','ssim','psnr']
rng=np.random.default_rng(20261004);bootdiff=[];summarydiff=[]
for model in ['entrada','inicial','A','B']:
 rr=[r for r in rows if r['model']==model]
 for met in metrics:
  values=np.array([float(r[met]) for r in rr]);v=report['summary'][model][met]
  for key,got in {'n':len(values),'mean':values.mean(),'sd':values.std(ddof=1),'mean_abs':np.abs(values).mean(),'p5':np.percentile(values,5),'p95':np.percentile(values,95)}.items():summarydiff.append(abs(float(got)-v[key]))
for met in metrics:
 clusters={}
 for g in sorted({x[0] for x in keys}):
  clusters[g]=[]
  for v in range(6):
   aa=np.array([float(lookup[g,v,k,'A'][met]) for k in range(20)]);bb=np.array([float(lookup[g,v,k,'B'][met]) for k in range(20)])
   dd=np.abs(bb)-np.abs(aa) if met.startswith(('total','rel_error')) else bb-aa
   clusters[g].append(float(dd.mean()))
 geos=sorted(clusters);samples=[]
 for _ in range(10000):
  vals=[]
  for g in rng.choice(geos,size=len(geos),replace=True):vals.extend(rng.choice(clusters[g],size=6,replace=True))
  samples.append(float(np.mean(vals)))
 ci=np.percentile(samples,[2.5,97.5]);published=report['paired_B_minus_A'][met]
 bootdiff.extend(abs(float(x)-y) for x,y in zip(ci,published['ci95']))
 bootdiff.append(abs(float(np.mean([v for g in geos for v in clusters[g]]))-published['mean']))
result={'schema':'oe2-complementary-independent-check-v1','raw_count_values_checked':len(diffs),'raw_max_difference':max(diffs),'summary_values_checked':len(summarydiff),'summary_max_difference':max(summarydiff),'bootstrap_values_checked':len(bootdiff),'bootstrap_max_difference':max(bootdiff),'passed':max(diffs+summarydiff+bootdiff)<1e-12,'initial_csv_recomputed_from_pixels':False,'note':'Initial model CSV summaries checked arithmetically; prior initial CPU predictions examined separately. Bootstrap is descriptive, not training variability.'}
atomic_json(a.salida,result);print(json.dumps(result),flush=True)


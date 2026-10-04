"""Diagnóstico exploratorio; no modifica pérdidas, pesos ni decisiones prospectivas."""
import argparse, csv, hashlib, json, platform
from pathlib import Path
import numpy as np
from datos_ajuste import Store, digest, read_json
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['datos','binarios','entrega','auditoria','salida']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();a.salida.mkdir(parents=True,exist_ok=False)
 proof=read_json(a.auditoria)
 assert proof['complete'] and proof['delivery_commit']=='f6518ff2aceb695129bfd8773ce58f6479395def'
 hashes={x['path']:x['sha256'] for x in proof['integrity']['manifest']}
 store=Store(a.datos,a.binarios/'mascaras-ajuste-v1')
 assert store.identity==proof['cache_sha256']
 rows=[];summaries={};input_hashes={}
 for pair in ['R1','R2','R3']:
  report_path=a.entrega/pair/'evaluacion/comparacion-cgan.json'
  report=read_json(report_path);input_hashes[str(report_path.relative_to(a.entrega))]=digest(report_path)
  indices=read_json(a.binarios/pair/'piloto/C0/indices-val.json')
  expected=[[g,v,k] for g in store.manifest['splits']['val'] for v in range(6) for k in range(20)]
  assert indices==expected
  preds={}
  for arm in ['C0','C1']:
   file=a.binarios/pair/'piloto'/arm/'predicciones-val.npy';rel=file.relative_to(a.binarios).as_posix()
   assert digest(file)==hashes[rel]
   preds[arm]=np.load(file,mmap_mode='r',allow_pickle=False)
   assert preds[arm].shape==(360,256,256)
  for gid in store.manifest['splits']['val']:
   refs,_=store.load(gid)
   for v in range(6):
    ids=[i for i,(g,vv,k) in enumerate(indices) if g==gid and vv==v]
    family=store.manifest['geometries'][gid]['families'];names=store.manifest['geometries'][gid]['names']
    for arm,pred in preds.items():
     z=np.asarray(pred[ids],dtype=np.float64)
     assert np.isfinite(z).all() and np.all((z>=0)&(z<1))
     c=np.expm1(store.scale*z/(1-z));ref=refs[v].astype(float)
     for j,f in enumerate(family):
      m=store.masks[gid][v,j];n=int(m.sum());r=ref[m];base=float(r.sum())
      assert n>=20 and base>0
      err=c[:,m]-r
      signed=err.sum(1)/base;absolute=np.abs(err).sum(1)/base
      net=np.abs(signed)
      cancel=absolute-net
      assert cancel.min()>-1e-12
      loss=np.abs(np.log1p(c[:,m].mean(1))-np.log1p(r.mean()))
      declared=next(q for q in report['regions'] if q['geometry']==gid and q['view']==v and q['model']==arm and q['region']==names[j])
      assert abs(absolute.mean()-declared['mae']['mean'])<1e-12
      assert abs(signed.mean()-declared['bias']['mean'])<1e-12
      rows.append(dict(pair=pair,arm=arm,geometry=gid,view=v,region=names[j],family=f,pixels=n,reference_sum=base,
        signed_bias_mean=float(signed.mean()),absolute_net_bias_mean=float(net.mean()),pixel_error_mean=float(absolute.mean()),
        cancellation_gap_mean=float(cancel.mean()),regional_log_loss_mean=float(loss.mean())))
  rr=[x for x in rows if x['pair']==pair and x['family']==2]
  stats={}
  for arm in ['C0','C1']:
   subset=[x for x in rr if x['arm']==arm]
   stats[arm]={k:float(np.mean([x[k] for x in subset])) for k in ['absolute_net_bias_mean','pixel_error_mean','cancellation_gap_mean','regional_log_loss_mean']}
   assert abs(stats[arm]['pixel_error_mean']-proof['evaluation'][pair]['summary'][arm]['edge_mae'])<1e-12
  counts={k:0 for k in ['pixel_error_worse','net_bias_better_pixel_worse','regional_loss_better_pixel_worse']}
  for c0 in [x for x in rr if x['arm']=='C0']:
   c1=next(x for x in rr if x['arm']=='C1' and (x['geometry'],x['view'])==(c0['geometry'],c0['view']))
   worse=c1['pixel_error_mean']>c0['pixel_error_mean']
   counts['pixel_error_worse']+=int(worse)
   counts['net_bias_better_pixel_worse']+=int(worse and c1['absolute_net_bias_mean']<c0['absolute_net_bias_mean'])
   counts['regional_loss_better_pixel_worse']+=int(worse and c1['regional_log_loss_mean']<c0['regional_log_loss_mean'])
  summaries[pair]={'edge':stats,'delta_C1_minus_C0':{k:stats['C1'][k]-stats['C0'][k] for k in stats['C0']},'views':counts}
 # Counterexample invokes the actual regional loss, not a rewritten imitation.
 import torch
 from perdida_cuentas_regionales import regional_log_count_loss
 ref=torch.tensor([1.]*10+[9.]*10,dtype=torch.float64).reshape(1,1,4,5)
 swapped=torch.flip(ref,dims=[2,3]);scale=store.scale
 norm=lambda c: torch.log1p(c)/(scale+torch.log1p(c))
 mask=torch.ones((1,1,4,5),dtype=torch.bool)
 l0,_=regional_log_count_loss(norm(ref),ref,mask,[2],scale)
 l1,_=regional_log_count_loss(norm(swapped),ref,mask,[2],scale)
 error=float((swapped-ref).abs().sum()/ref.sum())
 assert abs(float(l0))<1e-12 and abs(float(l1))<1e-12 and abs(error-1.6)<1e-12
 result={'schema':'oe2-spatial-diagnosis-v1','review_date':'2026-10-04','base_commit':'866e286ae0b1aa59c17f5ae46cd248a75305e19a',
  'exploratory':True,'training_performed':False,'weights_modified':False,'heldout_opened':False,'physical_acceptance':False,
  'causal_attribution_established':False,'rows':len(rows),'views_per_pair':18,'realizations_per_view':20,
  'definitions':{'absolute_net_bias':'mean_k(abs(sum_p residual_kp)/sum_p reference_p)',
  'pixel_error':'mean_k(sum_p abs(residual_kp)/sum_p reference_p)',
  'cancellation_gap':'pixel_error - absolute_net_bias; equals 2*mean_k(min(positive_sum_k,negative_magnitude_sum_k))/reference_sum',
  'regional_log_loss':'mean_k(abs(log1p(mean_p prediction_kp)-log1p(mean_p reference_p)))'},
  'summary':summaries,'counterexample':{'reference':[1]*10+[9]*10,'prediction':[9]*10+[1]*10,'exact_loss':float(l0),'permuted_loss':float(l1),'relative_pixel_error':error,'same_total_counts':True},
  'audit_sha256':digest(a.auditoria),'comparison_sha256':input_hashes,'script_sha256':digest(Path(__file__)),
  'loss_source_sha256':digest(Path(__file__).with_name('perdida_cuentas_regionales.py')),
  'environment':{'python':platform.python_version(),'numpy':np.__version__,'torch':torch.__version__,'device':'cpu'},
  'limits':['Post hoc diagnosis on repeatedly used validation set; no new acceptance thresholds.','Regional loss invariance does not establish the cause of the complete adversarial optimization.','Views and thinnings share geometries and references; not independent replication.']}
 with (a.salida/'diagnostico-espacial.json').open('w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
 with (a.salida/'diagnostico-espacial.csv').open('w',encoding='utf-8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 print(json.dumps({'rows':len(rows),'summary':summaries,'counterexample':result['counterexample']}))
if __name__=='__main__':main()


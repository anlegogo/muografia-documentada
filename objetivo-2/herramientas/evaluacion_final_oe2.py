"""Evaluación congelada al 5 %: preflight, inferencia por modelo y evaluación conjunta."""
import os
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import argparse,hashlib,json,sys,time,platform,csv
from pathlib import Path
import numpy as np

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 temp=p.with_suffix(p.suffix+'.tmp');temp.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8');os.replace(temp,p)
def check(ok,msg):
 if not ok:raise ValueError(msg)
def normalize(c,s):
 l=np.log1p(np.asarray(c,dtype=np.float64));return l/(s+l)
def invert(z,s):
 check(np.isfinite(z).all() and np.all((z>=0)&(z<1)),'Predicciones fuera de rango')
 q=s*z.astype(np.float64)/(1-z.astype(np.float64));check(np.max(q)<np.log(np.finfo(float).max)-1,'Inversión fuera de rango')
 return np.expm1(q)
def mean(v):return float(np.mean(v)) if len(v) else None
def contract(repo):
 p=repo/'objetivo-2/configuraciones/evaluacion-final-v1.json';s=read(p)
 for rel,h in s['source_sha256'].items():check(sha(repo/rel)==h,'Fuente modificada: '+rel)
 check(sha(Path(__file__))==s['runner_sha256'],'Ejecutor modificado')
 return s,sha(p)
def preflight(repo,data,weights,s):
 check(set(weights)==set(s['models']),'Se requieren exactamente los ocho modelos congelados')
 for rel,h in s['data_sha256'].items():check(sha(data/rel)==h,'Datos distintos: '+rel)
 for m,info in s['models'].items():check(sha(Path(weights[m]))==info['sha256'],'Pesos distintos: '+m)
 return {'data_files':len(s['data_sha256']),'models':len(weights),'arrays_opened':False,'passed':True}
def package(data,gid,s):
 p=data/f'dataset-v2/shards/{gid}.npz'
 check(sha(p)==s['data_sha256'][f'dataset-v2/shards/{gid}.npz'],'Shard alterado')
 with np.load(p,allow_pickle=False) as z:
  ref=z['ref_counts'];low=z['low_counts'];f=z['fractions']
  check(ref.shape==(6,256,256) and ref.dtype==np.uint32,'Referencia incompatible')
  check(low.shape==(6,4,20,256,256) and low.dtype==np.uint16,'Pares incompatibles')
  check(np.allclose(f,[.5,.1,.05,.01],atol=1e-8,rtol=0),'Fracciones incompatibles')
  check(np.all(low<=ref[:,None,None]),'Conteos bajos mayores que referencia')
  coords={k:z[k].copy() for k in ['az_centers_deg','el_centers_deg','az_edges_deg','el_edges_deg']}
  check(coords['az_centers_deg'].shape==(256,) and coords['el_centers_deg'].shape==(256,),'Coordenadas incompatibles')
  return ref.copy(),low[:,2].copy(),coords
def load_net(path,name,s,repo):
 import torch
 sys.path.insert(0,str(repo/'objetivo-2/implementacion/models'))
 from unet_generator import build_generator
 check(sha(path)==s['models'][name]['sha256'],'Peso incorrecto')
 safe=[np._core.multiarray._reconstruct,np.ndarray,np.dtype,np.dtypes.UInt32DType]
 with torch.serialization.safe_globals(safe):c=torch.load(path,map_location='cpu',weights_only=True)
 check(c['epoch']==5,'Época diferente')
 net=build_generator('unet_dc_5');net.load_state_dict(c['generator'],strict=True);del c
 return net.eval()
def env():
 import torch,skimage
 return {'python':platform.python_version(),'numpy':np.__version__,'torch':torch.__version__,'skimage':skimage.__version__,'cuda':torch.version.cuda}
def infer(a,s,signature):
 import torch
 check(a.model in s['models'],'Modelo no permitido')
 weights=read(a.weights);preflight(a.repo,a.data,weights,s)
 torch.set_num_threads(2);torch.use_deterministic_algorithms(True);torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True
 torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 device=torch.device(a.device);check(device.type!='cuda' or torch.cuda.is_available(),'CUDA no disponible')
 net=load_net(Path(weights[a.model]),a.model,s,a.repo).to(device)
 root=a.output/a.model;root.mkdir(parents=True,exist_ok=True)
 identity={'protocol_sha256':signature,'model':a.model,'checkpoint_sha256':s['models'][a.model]['sha256'],'environment':env(),'device':str(device),'gpu_name':torch.cuda.get_device_name(device) if device.type=='cuda' else None,'batch_size':4,'fraction':.05}
 if (root/'identity.json').exists():check(read(root/'identity.json')==identity,'Salida de otra identidad o entorno')
 else:
  check(not any(root.iterdir()),'Directorio no vacío sin identidad');write(root/'identity.json',identity)
 files=[];start=time.monotonic()
 for gid in s['geometry_order']:
  path=root/(gid+'.npy');receipt=root/(gid+'.json')
  if receipt.exists():
   r=read(receipt);check(r['identity']==identity and r['geometry']==gid and sha(path)==r['sha256'],'Exportación previa incompatible');files.append(r);continue
  ref,low,_=package(a.data,gid,s);x=normalize(low.reshape(120,256,256)/.05,s['normalization_scale']).astype(np.float32)
  pred=np.empty_like(x)
  with torch.inference_mode():
   for i in range(0,120,4):pred[i:i+4]=net(torch.from_numpy(x[i:i+4,None]).to(device)).cpu().numpy()[:,0]
  invert(pred,s['normalization_scale'])
  tmp=path.with_suffix('.npy.tmp')
  with tmp.open('wb') as f:np.save(f,pred,allow_pickle=False)
  os.replace(tmp,path);r={'geometry':gid,'identity':identity,'sha256':sha(path),'shape':list(pred.shape),'dtype':str(pred.dtype),'order':'view 0..5, realization 0..19'};write(receipt,r);files.append(r)
  print(a.model,gid,'120 predicciones',flush=True)
 write(root/'completed.json',{'identity':identity,'files':files,'images':480,'elapsed_seconds_this_invocation':time.monotonic()-start,'training_performed':False})
def analyze_view(ref,low,preds,geometry,coords,view,cfg,scale):
 from evaluar_regiones_geometricas import rays,masks,match_controls,morphology
 from metrics import compute_ssim,compute_psnr
 counts={'entrada':low.astype(float)/.05};counts.update({k:invert(v,scale) for k,v in preds.items()})
 target=normalize(ref,scale).astype(np.float32);im=[];rr=[];cc=[]
 for name,c in counts.items():
  zz=normalize(c,scale).astype(np.float32) if name=='entrada' else preds[name]
  for k,z in enumerate(zz):
   ss=compute_ssim(z,target);ps=float('inf') if np.array_equal(target,z) else compute_psnr(target,z)
   check(np.isfinite(ss) and not np.isnan(ps),'Métricas no finitas')
   im.append({'model':name,'realization':k,'ssim':ss,'psnr':float(ps) if np.isfinite(ps) else None,'perfect_match':bool(np.array_equal(target,z))})
 o,d=rays(coords['az_centers_deg'],coords['el_centers_deg'],view,cfg);L,aa,regions=masks(geometry,o,d,cfg)
 for ri,(name,m) in enumerate(regions.items()):
  den=float(ref[m].sum());n=int(m.sum());family=min(ri,3);valid=n>=20 and den>0
  for model,c in counts.items():
   row={'model':model,'region':name,'family':family,'pixels':n,'reference_sum':den,'status':'ok' if valid else 'reference_or_geometry_insufficient'}
   if valid:
    error=c[:,m]-ref[m];bias=error.sum(1)/den;mae=np.abs(error).sum(1)/den
    row.update(bias_mean=mean(bias),bias_mean_absolute=mean(np.abs(bias)),spatial_mae=mean(mae),bias_by_realization=bias.tolist())
   rr.append(row)
 for ai,an in enumerate(geometry['anomalies']):
  name=f"anomalia_{ai}_{an['kind']}";m=regions[name].copy()
  for j,ll in enumerate(aa):
   if j!=ai:m&=~morphology(ll>0,cfg['rock_sky_margin_pixels'],False)
  t,donors=match_controls(m,regions['roca_sin_anomalia'],L,cfg);coverage=len(t)/int(m.sum()) if m.any() else 0
  row={'region':name,'matched_pixels':len(t),'match_fraction':coverage,'status':'insufficient_geometry','models':{}}
  if len(t)>=cfg['min_matched_pixels'] and coverage>=cfg['min_match_fraction']:
   def contrast(c):
    c=c.reshape(-1,65536);den=c[:,donors].mean((1,2));return np.divide(c[:,t].mean(1),den,out=np.full(len(c),np.nan),where=den>0)-1
   cr=contrast(ref)[0];row['status']='zero_reference_control'
   if np.isfinite(cr):
    row.update(status='estimable',reference_contrast=float(cr))
    for name,c in counts.items():
     v=contrast(c);ok=np.isfinite(v);valid=v[ok]
     row['models'][name]={'valid_realizations':int(ok.sum()),'invalid_realizations':int((~ok).sum()),'contrast_mean':mean(valid),'absolute_error':mean(np.abs(valid-cr)),'sign_inversions':int(np.sum(valid*cr<0))}
  cc.append(row)
 return im,rr,cc
def summarize(images,regions,contrasts,models,gids):
 result={}
 common=[x for x in contrasts if x['status']=='estimable' and all(x['models'][m]['valid_realizations']==20 for m in models)]
 for m in models:
  by={}
  for g in gids:
   ii=[x for x in images if x['model']==m and x['geometry']==g];rr=[x for x in regions if x['model']==m and x['geometry']==g];valid=[x for x in rr if x['status']=='ok']
   rock=[abs(x['bias_mean']) for x in valid if x['family']==1]
   anomalies=[[abs(x['bias_mean']) for x in valid if x['family']==3 and x['view']==v] for v in range(6)]
   expected_anomalies=[sum(x['family']==3 and x['view']==v for x in rr) for v in range(6)]
   complete=len(rock)==6 and all(len(anomalies[v])==expected_anomalies[v] and expected_anomalies[v]>0 for v in range(6))
   by[g]={'images':len(ii),'ssim':mean([x['ssim'] for x in ii]),'psnr':mean([x['psnr'] for x in ii]) if all(x['psnr'] is not None for x in ii) else None,'perfect_matches':sum(x['perfect_match'] for x in ii),'rock_abs_bias':mean(rock),'Q':(mean(rock)+mean([mean(v) for v in anomalies]))/2 if complete else None,'Q_status':'complete' if complete else 'not_applicable_or_incomplete','invalid_regions':len(rr)-len(valid)}
   gc=[x for x in common if x['geometry']==g]
   by[g]['common_contrasts']=len(gc);by[g]['contrast_absolute_error']=mean([x['models'][m]['absolute_error'] for x in gc])
   for fam,key in [(0,'sky_mae'),(2,'edge_mae')]:
    rows=[x['spatial_mae'] for x in valid if x['family']==fam];by[g][key]=mean(rows) if len(rows)==6 else None
  result[m]={'by_geometry':by,'common_contrasts':len(common),'contrast_absolute_error':mean([x['models'][m]['absolute_error'] for x in common]),'ssim_macro':mean([x['ssim'] for x in by.values()]),'psnr_macro':mean([x['psnr'] for x in by.values()]) if all(x['psnr'] is not None for x in by.values()) else None,'Q_macro':mean([x['Q'] for x in by.values()]) if all(x['Q'] is not None for x in by.values()) else None}
 return result
def evaluate(a,s,signature):
 weights=read(a.weights);preflight(a.repo,a.data,weights,s)
 a.report.mkdir(parents=True,exist_ok=False)
 for model in s['models']:
  root=a.output/model;c=read(root/'completed.json');check(c['identity']['protocol_sha256']==signature and c['identity']['model']==model and c['identity']['checkpoint_sha256']==s['models'][model]['sha256'] and c['images']==480,'Entrega incompleta')
  check([x['geometry'] for x in c['files']]==s['geometry_order'],'Índices incompletos')
  for x in c['files']:check(x['identity']==c['identity'] and sha(root/(x['geometry']+'.npy'))==x['sha256'],'Predicciones alteradas')
 images=[];regions=[];contrasts=[]
 for gid in s['geometry_order']:
  ref,low,coords=package(a.data,gid,s);geometry=read(a.repo/s['geometry_files'][gid]);preds={m:np.load(a.output/m/(gid+'.npy'),allow_pickle=False,mmap_mode='r') for m in s['models']}
  for m,z in preds.items():check(z.shape==(120,256,256) and z.dtype==np.float32,'Forma de predicciones incompatible')
  for v in range(6):
   im,rr,cc=analyze_view(ref[v].astype(float),low[v],{m:z[v*20:(v+1)*20] for m,z in preds.items()},geometry,coords,v,s['regional_protocol'],s['normalization_scale'])
   for records,dest in [(im,images),(rr,regions),(cc,contrasts)]:dest.extend([{'geometry':gid,'view':v,**x} for x in records])
  print('Evaluada',gid,flush=True)
 models=['entrada']+list(s['models']);summaries={}
 for split,gids in s['splits'].items():summaries[split]=summarize([x for x in images if x['geometry'] in gids],[x for x in regions if x['geometry'] in gids],[x for x in contrasts if x['geometry'] in gids],models,gids)
 pairs=[('cgan_original','entrada'),('unet_original','entrada'),('cgan_original','unet_original')]+[(f'B{i}_C1',f'B{i}_C0') for i in [1,2,3]]
 comparisons={}
 for split,summary in summaries.items():
  comparisons[split]={}
  for candidate,baseline in pairs:
   if candidate not in summary or baseline not in summary:continue
   checks={};deltas={}
   for gid in s['splits'][split]:
    ca=summary[candidate]['by_geometry'][gid];ba=summary[baseline]['by_geometry'][gid];checks[gid]={};deltas[gid]={}
    for metric,sign in [('ssim',1),('psnr',1),('Q',-1),('sky_mae',-1),('edge_mae',-1),('contrast_absolute_error',-1)]:
     valid=ca[metric] is not None and ba[metric] is not None
     delta=ca[metric]-ba[metric] if valid else None;deltas[gid][metric]=delta;checks[gid][metric]=sign*delta>=0 if valid else None
   values=[v for g in checks.values() for v in g.values()]
   comparisons[split][candidate+'_vs_'+baseline]={'deltas_candidate_minus_baseline':deltas,'not_worse_descriptive':checks,'classification':'incomplete' if None in values else 'no_deterioration_in_listed_metrics' if all(values) else 'tradeoff_or_deterioration','statistical_superiority':False}
 result={'protocol_sha256':signature,'runner_sha256':sha(__file__),'environment':env(),'models':s['models'],'summary':summaries,'predeclared_comparisons':comparisons,'images':images,'regions':regions,'contrasts':contrasts,'heldout_opened':True,'training_performed':False,'physical_acceptance':False,'automatic_model_selection':False,'equivalence_claim':False,'scope':s['scope']}
 write(a.report/'evaluacion-final.json',result)
 for name,rows in [('imagenes',images),('regiones',regions)]:
  keys=sorted(set().union(*(x.keys() for x in rows)))
  with (a.report/(name+'.csv')).open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
 inventory=[{'path':str(p.relative_to(a.output)).replace('\\','/'),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(a.output.rglob('*')) if p.is_file()]
 write(a.report/'inventario-predicciones.json',inventory)
 print('Evaluación completa; no implica aceptación física',flush=True)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('phase',choices=['preflight','infer','evaluate'])
 p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2]);p.add_argument('--data',type=Path,required=True);p.add_argument('--weights',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--model');p.add_argument('--device',default='cuda');p.add_argument('--report',type=Path)
 a=p.parse_args();sys.path.insert(0,str(a.repo/'objetivo-2/herramientas'));sys.path.insert(0,str(a.repo/'objetivo-2/implementacion/scripts/evaluation'));s,signature=contract(a.repo)
 if a.phase=='preflight':
  result=preflight(a.repo,a.data,read(a.weights),s);write(a.output/'preflight.json',{'protocol_sha256':signature,**result});print(json.dumps(result))
 elif a.phase=='infer':
  from filelock import FileLock
  check(a.model in s['models'],'Modelo no permitido');a.output.mkdir(parents=True,exist_ok=True)
  with FileLock(str(a.output/('.'+a.model+'.lock')),timeout=0):infer(a,s,signature)
 else:
  check(a.report is not None,'Falta --report');evaluate(a,s,signature)
if __name__=='__main__':main()

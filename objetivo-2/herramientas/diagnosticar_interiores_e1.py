"""Diagnóstico descriptivo E1 desde predicciones verificadas; sin entrenar ni abrir reservas."""
import argparse,json,hashlib,os,csv
from pathlib import Path
import numpy as np
from scipy.ndimage import distance_transform_edt
from datos_ajuste import Store,digest

def run(a):
 a.salida.mkdir(parents=True,exist_ok=False)
 os.environ['MPLCONFIGDIR']=str(a.salida/'mpl-cache')
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.colors import SymLogNorm
 audit=json.loads(a.auditoria.read_text(encoding='utf-8'))
 assert audit['complete'] and audit['delivery_commit']=='804ce85f1bcb1e00d0956ae6bef26e69dd50130a'
 store=Store(a.datos,a.binarios/'mascaras-ajuste-v1')
 rows=[];distrows=[];sources={};maps={};checks=0
 for pair in ['B1','B2','B3']:
  summary=json.loads((a.entrega/'datos/ensayo-borde-e1'/pair/'evaluacion/comparacion-cgan.json').read_text(encoding='utf-8'))
  arrays={}
  for arm in ['C0','C1']:
   p=a.binarios/pair/'piloto'/arm/'predicciones-val.npy'
   h=digest(p);assert h==next(x['sha256'] for x in audit['integrity']['manifest'] if x['path']==f'{pair}/piloto/{arm}/predicciones-val.npy')
   sources[f'{pair}/{arm}']=h;arrays[arm]=np.load(p,mmap_mode='r',allow_pickle=False)
  for gi,gid in enumerate(store.manifest['splits']['val']):
   refs,_=store.load(gid);info=store.manifest['geometries'][gid]
   for vi in range(6):
    ref=refs[vi].astype(float);ms=store.masks[gid][vi]
    means={arm:np.expm1(store.scale*arrays[arm][gi*120+vi*20:gi*120+(vi+1)*20].astype(float)/(1-arrays[arm][gi*120+vi*20:gi*120+(vi+1)*20].astype(float))).mean(axis=0) for arm in arrays}
    if gid=='geo-val-01':maps[pair,vi]=(ref,means,ms)
    distance=distance_transform_edt(~ms[2])
    for ri,(name,family) in enumerate(zip(info['names'],info['families'])):
     if family not in [1,3]:continue
     m=ms[ri];den=ref[m].sum();assert den>0
     rr={'pair':pair,'geometry':gid,'view':vi,'region':name,'family':family,'pixels':int(m.sum()),'reference_sum':float(den)}
     for arm in arrays:
      err=means[arm]-ref
      bias=float(err[m].sum()/den)
      expected=next(x['bias']['mean'] for x in summary['regions'] if (x['geometry'],x['view'],x['region'],x['model'])==(gid,vi,name,arm))
      assert abs(bias-expected)<1e-12;checks+=1
      rr[arm]={'bias':bias,'positive_excess':float(np.maximum(err[m],0).sum()/den),'negative_deficit':float(np.minimum(err[m],0).sum()/den),'positive_pixel_fraction':float(np.mean(err[m]>0))}
      assert abs(rr[arm]['positive_excess']+rr[arm]['negative_deficit']-bias)<1e-12
     rows.append(rr)
     for label,sel in [('0-2px',distance<=2),('2-8px',(distance>2)&(distance<=8)),('>8px',distance>8)]:
      mm=m&sel
      distrows.append({'pair':pair,'geometry':gid,'view':vi,'region':name,'band':label,'pixels':int(mm.sum()),'reference_sum':float(ref[mm].sum()),'C0_bias_contribution':float((means['C0'][mm]-ref[mm]).sum()/den),'C1_bias_contribution':float((means['C1'][mm]-ref[mm]).sum()/den)})
    print(pair,gid,vi,flush=True)
  del arrays
 geo1=[r for r in rows if r['geometry']=='geo-val-01']
 aggregate={}
 for pair in ['B1','B2','B3']:
  aggregate[pair]={}
  for reg in sorted({r['region'] for r in geo1}):
   rr=[r for r in geo1 if r['pair']==pair and r['region']==reg]
   aggregate[pair][reg]={'views':6,'C0_mean_bias':float(np.mean([r['C0']['bias'] for r in rr])),'C1_mean_bias':float(np.mean([r['C1']['bias'] for r in rr])),'worse_absolute_bias_views':sum(abs(r['C1']['bias'])>abs(r['C0']['bias']) for r in rr),'C1_positive_bias_views':sum(r['C1']['bias']>0 for r in rr),'bands':{}}
   for label in ['0-2px','2-8px','>8px']:
    dd=[r for r in distrows if r['geometry']=='geo-val-01' and r['pair']==pair and r['region']==reg and r['band']==label]
    aggregate[pair][reg]['bands'][label]={k:float(np.mean([r[k] for r in dd])) for k in ['pixels','reference_sum','C0_bias_contribution','C1_bias_contribution']}
 for pair in ['B1','B2','B3']:
  fig,axes=plt.subplots(6,4,figsize=(13,16),layout='constrained')
  maxref=max(float(np.log1p(maps[pair,v][0]).max()) for v in range(6))
  limit=max([float(np.max(np.abs(maps[pair,v][1][arm]-maps[pair,v][0]))) for v in range(6) for arm in ['C0','C1']]+[float(np.max(np.abs(maps[pair,v][1]['C1']-maps[pair,v][1]['C0']))) for v in range(6)])
  norm=SymLogNorm(linthresh=1,vmin=-limit,vmax=limit,base=10)
  for v in range(6):
   ref,means,ms=maps[pair,v]
   refim=axes[v,0].imshow(np.log1p(ref),origin='lower',vmin=0,vmax=maxref,cmap='viridis')
   for col,z in enumerate([means['C0']-ref,means['C1']-ref,means['C1']-means['C0']],1):
    im=axes[v,col].imshow(z,origin='lower',norm=norm,cmap='RdBu_r')
    axes[v,col].contour(ms[3].astype(float),levels=[.5],colors=['black'],linewidths=.6)
   axes[v,0].set_ylabel(f'Vista {v}\nFila angular')
   for ax in axes[v]:ax.set_xticks([0,128,255]);ax.set_yticks([0,128,255])
  for ax,title in zip(axes[0],['Referencia: log(1+cuentas)','Error medio C0','Error medio C1','Cambio C1 − C0']):ax.set_title(title)
  fig.colorbar(refim,ax=axes[:,0],label='log(1 + cuentas de referencia)',shrink=.4)
  fig.colorbar(im,ax=axes[:,1:],label='Cuentas equivalentes · escala simétrica logarítmica (tramo lineal ±1) ',shrink=.55)
  fig.suptitle(f'E1 · {pair} · geometría 1 · promedio de 20 realizaciones\nRojo: exceso de cuentas; azul: déficit. Contorno negro: conducto. Sin recorte de datos.',fontsize=13)
  fig.savefig(a.salida/f'mapas-{pair}-geo1.png',dpi=125)
  fig.savefig(a.salida/f'mapas-{pair}-geo1.jpg',dpi=100,pil_kwargs={'quality':85});plt.close(fig)
 out={'schema':'oe2-e1-interior-diagnostic-v1','delivery_commit':audit['delivery_commit'],'source_predictions':sources,'script_sha256':digest(Path(__file__)),'regions_checked':checks,'regions':rows,'distance_bands':distrows,'geo1_summary':aggregate,'heldout_opened':False,'training_performed':False,'selection_performed':False,'interpretation':'Post hoc descriptivo. Distancia euclidiana en pixeles de la malla angular, no distancia fisica. Bandas 2/8 px para localizacion, no criterios de aceptacion ni ajuste de hiperparametros. Sesgo del promedio, no MAE promedio por realizacion. No prueba mecanismo causal.'}
 (a.salida/'diagnostico-interiores.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 with (a.salida/'bandas.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(distrows[0]));w.writeheader();w.writerows(distrows)
 print(json.dumps({'checks':checks,'geo1_summary':aggregate}),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['auditoria','entrega','binarios','datos','salida']:p.add_argument('--'+n,type=Path,required=True)
 run(p.parse_args())

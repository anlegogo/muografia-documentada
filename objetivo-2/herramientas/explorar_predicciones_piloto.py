from pathlib import Path
import sys,os,json
import argparse
p=argparse.ArgumentParser(description='Exploración regional, no confirmatoria, de los checkpoints seleccionados')
p.add_argument('--datos',type=Path,required=True)
p.add_argument('--predicciones',type=Path,required=True)
p.add_argument('--salida',type=Path,required=True)
p.add_argument('--dependencias',type=Path)
a=p.parse_args()
out=a.salida;out.mkdir(parents=True,exist_ok=True)
if a.dependencias:sys.path.insert(0,str(a.dependencias))
os.environ['MPLCONFIGDIR']=str(out/'mpl-cache')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=a.datos
scale=8.239329427901795
pred={n:np.load(a.predicciones/f'{n}-predicciones.npy') for n in ('unet','cgan')}
rows=[]
for gi in range(3):
 gid=f'geo-val-{gi+1:02d}'
 with np.load(root/f'dataset-v2/shards/{gid}.npz') as z:
  refs=z['ref_counts'].astype(float); az=z['az_edges_deg'];el=z['el_edges_deg']
  targets=np.log1p(refs)/(scale+np.log1p(refs))
  extent=[float(az[0]),float(az[-1]),float(el[0]),float(el[-1])]
 fig,axes=plt.subplots(6,5,figsize=(15,15),constrained_layout=True)
 for vi in range(6):
  rr=targets[vi]
  panels=[rr];means={}
  for name in ('unet','cgan'):
   zz=pred[name][gi*120+vi*20:gi*120+(vi+1)*20]
   means[name]=zz.mean(0);panels.append(means[name])
   counts=np.expm1(scale*zz.astype(float)/(1-zz))
   # Cuatro bandas fijas de elevación, no regiones físicas de anomalía.
   for band in range(4):
    sl=slice(band*64,(band+1)*64)
    err=zz[:,sl]-rr[None,sl]
    base=refs[vi,sl].sum()
    rows.append({'geometry':gid,'view':vi,'model':name,'elevation_quarter':band,
       'elevation_bounds_deg':[float(el[band*64]),float(el[(band+1)*64])],
       'normalized_mae':float(np.abs(err).mean()),'normalized_bias':float(err.mean()),
       'counts_relative_sum_bias':float((counts[:,sl].sum(axis=(1,2)).mean()-base)/base)})
  panels.extend([means['unet']-rr,means['cgan']-rr])
  for col,img in enumerate(panels):
   ax=axes[vi,col]
   im=ax.imshow(img,origin='lower',extent=extent,cmap='viridis' if col<3 else 'RdBu_r',vmin=0 if col<3 else -.08,vmax=.55 if col<3 else .08,aspect='auto')
   if vi==0:ax.set_title(['Referencia','U-Net media (20)','cGAN media (20)','Residuo U-Net','Residuo cGAN'][col])
   if col==0:ax.set_ylabel(f'Vista {vi}\nElevación (°)')
   if vi==5:ax.set_xlabel('Azimut (°)')
 fig.suptitle(f'{gid} · checkpoints de época 5 · exploración de validación',fontsize=15)
 fig.colorbar(im,ax=axes[:,3:].ravel().tolist(),label='Predicción − referencia (normalizada)',shrink=.5)
 fig.savefig(out/f'{gid}-revision.png',dpi=130)
 plt.close(fig)
# La zona candidata se fija a partir del aviso visual previo, no como prueba confirmatoria.
# Centro aproximado: columna 132, fila 62, índices desde cero, origen inferior.
rr,cc=np.indices((256,256));radius=np.hypot(rr-62,cc-132)
center=radius<=4;ring=(radius>=8)&(radius<=12)
with np.load(root/'dataset-v2/shards/geo-val-01.npz') as z:
 ref=z['ref_counts'][0].astype(float)
 yy=np.log1p(ref)/(scale+np.log1p(ref))
probe={'location':'geo-val-01/view0','center_row_col':[62,132],'core_radius':4,'ring_radii':[8,12],
 'status':'exploratorio seleccionado a partir de figura previa; no es ROI física validada',
 'reference_contrast':float(yy[center].mean()-yy[ring].mean())}
for name in pred:
 zz=pred[name][:20]
 contrasts=zz[:,center].mean(1)-zz[:,ring].mean(1)
 probe[name]={'contrast_mean':float(contrasts.mean()),'contrast_min':float(contrasts.min()),'contrast_max':float(contrasts.max()),'negative_realizations':int((contrasts<0).sum())}
result={'bands':rows,'candidate_spot':probe,'note':'Métricas exploratorias en val; no certifican densidad ni preservación de anomalías.','test_opened':False}
(out/'revision-regional.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(probe,indent=2))

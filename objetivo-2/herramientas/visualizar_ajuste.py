"""Figuras de todas las vistas disponibles; promedios solo para inspección."""
import argparse,os
from pathlib import Path
import numpy as np
from datos_ajuste import ROOT,Store,sources,read_json
from revisar_ajuste import load_completed
p=argparse.ArgumentParser(description=__doc__)
for n in ['datos','mascaras','control','regional','salida']:p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--etapa',choices=['tecnica','piloto'],required=True)
a=p.parse_args();store=Store(a.datos,a.mascaras)
for name,path in [('A',a.control),('B',a.regional)]:load_completed(path,name,a.etapa,sources())
keys=read_json(a.control/'indices-val.json')
if keys!=read_json(a.regional/'indices-val.json'):raise ValueError('Orden diferente')
pred={name:np.load(path/'predicciones-val.npy',mmap_mode='r') for name,path in [('A',a.control),('B',a.regional)]}
a.salida.mkdir(parents=True,exist_ok=False)
os.environ['MPLCONFIGDIR']=str(a.salida/'mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
for gid in sorted({g for g,v,k in keys}):
    views=sorted({v for g,v,k in keys if g==gid});ref,low=store.load(gid)
    with np.load(a.datos/f'dataset-v2/shards/{gid}.npz') as z:extent=[float(z['az_edges_deg'][0]),float(z['az_edges_deg'][-1]),float(z['el_edges_deg'][0]),float(z['el_edges_deg'][-1])]
    fig,axes=plt.subplots(len(views),6,figsize=(17,3*len(views)+.6),squeeze=False,constrained_layout=True)
    for row,vi in enumerate(views):
        ii=[j for j,(g,v,k) in enumerate(keys) if (g,v)==(gid,vi)];kk=[keys[j][2] for j in ii]
        target=np.log1p(ref[vi].astype(float));target=target/(store.scale+target)
        x=np.log1p(low[vi,kk].astype(float)/.05);x=x/(store.scale+x)
        A=pred['A'][ii].mean(0);B=pred['B'][ii].mean(0)
        panels=[target,x.mean(0),A,B,A-target,B-target]
        for col,img in enumerate(panels):
            ax=axes[row,col];im=ax.imshow(img,origin='lower',extent=extent,aspect='auto',cmap='viridis' if col<4 else 'RdBu_r',vmin=0 if col<4 else -.08,vmax=.55 if col<4 else .08)
            if row==0:ax.set_title(['Referencia','Entrada media','A: control medio','B: regional medio','Residuo A','Residuo B'][col])
            if col==0:ax.set_ylabel(f'Vista {vi}\nElevación (°)')
            if row==len(views)-1:ax.set_xlabel('Azimut (°)')
    fig.colorbar(im,ax=axes[:,4:].ravel().tolist(),label='Predicción − referencia, normalizada',shrink=.6)
    fig.suptitle(f'{gid} · etapa {a.etapa} · medias de imágenes normalizadas\n'+('Comprobación reducida: no evaluar calidad del ensayo' if a.etapa=='tecnica' else '20 realizaciones por vista; las métricas se calculan por imagen'),fontsize=12)
    fig.savefig(a.salida/f'{gid}.png',dpi=120);plt.close(fig)
print('Figuras exportadas en '+str(a.salida))

"""Figuras descriptivas desde matrices auditadas; no ejecuta redes ni selecciona pesos."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=argparse.ArgumentParser()
p.add_argument('--datos',type=Path,required=True)
p.add_argument('--predicciones',type=Path,required=True)
p.add_argument('--resultados',type=Path,required=True)
p.add_argument('--salida',type=Path,required=True)
a=p.parse_args();a.salida.mkdir(parents=True,exist_ok=True)
s=8.239329427901795
def norm(c):
    l=np.log1p(np.asarray(c,dtype=np.float64));return l/(s+l)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
results=json.loads(a.resultados.read_text(encoding='utf-8'))
geos=['geo-test-01','geo-test-02','geo-test-03','geo-gen-01']
models=['unet_original','cgan_original','B1_C0','B1_C1','B2_C0','B2_C1','B3_C0','B3_C1']
sources={};cases=[]
def get(g,v=0,r=0):
    path=a.datos/(g+'.npz');sources['datos/'+g+'.npz']=sha(path)
    with np.load(path) as d:
        fi=int(np.flatnonzero(np.isclose(d['fractions'],.05))[0])
        refs=norm(d['ref_counts'][v]);low=norm(d['low_counts'][v,fi,r]/.05)
    out={'referencia':refs,'entrada':low}
    for m in models:
        path=a.predicciones/m/(g+'.npy');sources['predicciones/'+m+'/'+g+'.npy']=sha(path)
        arr=np.load(path,mmap_mode='r');assert arr.shape==(120,256,256)
        out[m]=np.asarray(arr[v*20+r],dtype=np.float64)
        assert np.isfinite(out[m]).all() and (out[m]>=0).all() and (out[m]<1).all()
    cases.append({'geometry':g,'view':v,'realization':r,'prediction_index':v*20+r,'fraction':.05})
    return out
data={g:get(g) for g in geos}
columns=['referencia','entrada','unet_original','cgan_original']
labels=['Referencia alta estadística','Entrada al 5 %','U-Net original','cGAN original']
fig,ax=plt.subplots(4,4,figsize=(11,10),layout='constrained')
for i,g in enumerate(geos):
    for j,m in enumerate(columns):
        im=ax[i,j].imshow(data[g][m],vmin=0,vmax=1,cmap='viridis',origin='lower',interpolation='nearest')
        if i==0:ax[i,j].set_title(labels[j],fontsize=10)
        if j==0:ax[i,j].set_ylabel(g+'\nFila angular')
        ax[i,j].set_xticks([0,128,255]);ax[i,j].set_yticks([0,128,255])
        if i==3:ax[i,j].set_xlabel('Columna angular')
fig.colorbar(im,ax=ax,shrink=.65,label='T(c), escala común [0, 1]')
fig.suptitle('Comparación fija: vista 0, realización 0 de cada geometría',fontsize=13)
fig.savefig(a.salida/'comparacion-fija.png',dpi=155);plt.close(fig)
# Caso desfavorable definido por Q agregado, sin buscar la imagen visualmente peor.
worst=max(geos,key=lambda g:results['summary']['generalization' if g=='geo-gen-01' else 'test']['cgan_original']['by_geometry'][g]['Q'])
out=data[worst];display=['entrada']+models
fig,ax=plt.subplots(2,9,figsize=(19,5),layout='constrained')
lim=max(float(np.max(np.abs(out[m]-out['referencia']))) for m in display)
for j,m in enumerate(display):
    ax[0,j].imshow(out[m],vmin=0,vmax=1,cmap='viridis',origin='lower',interpolation='nearest')
    im=ax[1,j].imshow(out[m]-out['referencia'],vmin=-lim,vmax=lim,cmap='RdBu_r',origin='lower',interpolation='nearest')
    ax[0,j].set_title(m.replace('_original','').replace('_',' '),fontsize=9)
    for i in range(2):ax[i,j].set_xticks([]);ax[i,j].set_yticks([])
ax[0,0].set_ylabel('T(c), escala [0, 1]');ax[1,0].set_ylabel('Residuo en T(c)')
fig.colorbar(im,ax=ax[1,:],orientation='horizontal',shrink=.65,label='Predicción o entrada menos referencia; escala común y simétrica')
fig.suptitle('Caso desfavorable: '+worst+'; mayor Q de cGAN original entre las cuatro geometrías\nVista 0 y realización 0 fijas; se muestran las seis continuaciones, sin seleccionar una semilla ganadora',fontsize=12)
fig.savefig(a.salida/'caso-desfavorable.png',dpi=155);plt.close(fig)
evidence={'selection':'vista 0 y realización 0 de cada geometría; caso desfavorable por mayor Q agregado de cGAN original', 'cases':cases,'worst_geometry':worst,'normalization_scale':s,'residual_limit':lim,'sources_sha256':sources,'results_sha256':sha(a.resultados),'script_sha256':sha(Path(__file__)),'note':'Figuras descriptivas posteriores a la evaluación. Índices de píxel angular; sin remuestreo. Los residuos se expresan en T(c), no en cuentas ni densidad.'}
(a.salida/'procedencia-figuras.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'worst_geometry':worst,'figures':2,'sources':len(sources)},ensure_ascii=False))

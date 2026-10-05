"""Figura descriptiva: no interpola factores ni combina particiones."""
import argparse,csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,default=Path(__file__).parent/'publicacion');ROOT=p.parse_args().directory
with (ROOT/'sintesis_metricas.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(2,3,figsize=(14,8),layout='constrained')
metrics=[('ssim_macro','SSIM ↑'),('psnr_macro','PSNR (dB) ↑'),('contrast_counts_mae_reference','Error absoluto de contraste ↓')]
models=['entrada','unet_original','cgan_original','B1_C0','B1_C1','B2_C0','B2_C1','B3_C0','B3_C1']
for i,split in enumerate(['test','generalization']):
 for j,(metric,label) in enumerate(metrics):
  ax=axs[i,j]
  for model in models:
   rr=sorted([r for r in rows if r['split']==split and r['model']==model],key=lambda r:float(r['fraction']))
   x=[100*float(r['fraction']) for r in rr];y=[float(r[metric]) for r in rr]
   color={'entrada':'#111111','unet_original':'#1778ad','cgan_original':'#ce462a'}.get(model,'#999999')
   legend={'entrada':'Entrada sin red','unet_original':'U-Net original','cgan_original':'cGAN original','B1_C0':'Continuaciones (6)'}.get(model,'_nolegend_')
   ax.plot(x,y,'o--' if model.startswith('B') else 'o-',color=color,alpha=.65 if model.startswith('B') else 1,linewidth=1 if model.startswith('B') else 2,label=legend,zorder=1 if model.startswith('B') else 3)
  ax.set_xscale('log');ax.set_xticks([1,5,10,50],['1','5','10','50']);ax.set_xlabel('Conteos de entrada (%)');ax.set_ylabel(label);ax.grid(alpha=.2)
  ax.set_title(('Prueba: 3 geometrías' if i==0 else 'Generalización: 1 geometría'))
axs[0,0].legend(fontsize=9)
fig.suptitle('OE3-C1 · Modelos congelados entrenados al 5 %',fontsize=16)
fig.savefig(ROOT/'curvas-complemento.svg');fig.savefig(ROOT/'curvas-complemento.png',dpi=150)
print('Figura SVG y PNG guardada')

import json,argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator,FixedFormatter
p=argparse.ArgumentParser()
p.add_argument('--curves',type=Path,required=True);p.add_argument('--models',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True)
a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
d=json.loads(a.curves.read_text(encoding='utf-8'));c=json.loads(a.models.read_text(encoding='utf-8'))
models=list(c['summary']['test']);models.remove('entrada')
fig,axes=plt.subplots(2,3,figsize=(13,8))
colors=plt.get_cmap('tab10').colors
for row,split in enumerate(['test','generalization']):
 for col,(metric,label,scale) in enumerate([('ssim_macro','SSIM (mayor es mejor)',1),('psnr_macro','PSNR [dB] (mayor es mejor)',1),('Q_macro','Q [%] (menor es mejor)',100)]):
  ax=axes[row,col];fractions=d['fractions']
  ax.plot([100*f for f in fractions],[d['curves'][split][str(f)][metric]*scale for f in fractions],'-ok',label='Entrada sin red',lw=1.7)
  for i,m in enumerate(models):ax.scatter(5,c['summary'][split][m][metric]*scale,color=colors[i],marker=['s','D','^','v','<','>','P','X'][i],s=48,label=m,zorder=3)
  ax.set_xscale('log');ax.xaxis.set_major_locator(FixedLocator([1,5,10,50]));ax.xaxis.set_major_formatter(FixedFormatter(['1','5','10','50']));ax.minorticks_off()
  ax.set_xlabel('Fracción de conteos de entrada [%]');ax.set_ylabel(label);ax.grid(alpha=.2)
  ax.set_title(('Prueba: 3 geometrías' if row==0 else 'Generalización: 1 geometría'))
handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=5,bbox_to_anchor=(.5,.015),fontsize=9)
fig.suptitle('Curvas descriptivas de exposición y redes evaluadas solo al 5 %',fontsize=15)
fig.text(.5,.085,'Líneas: guía entre puntos medidos, sin interpolación para estimar tiempos. Q no es error de densidad.',ha='center',fontsize=10)
fig.tight_layout(rect=[0,.11,1,.95]);fig.savefig(a.output_dir/'curvas-exposicion.svg',metadata={'Date':None});fig.savefig(a.output_dir/'curvas-exposicion.png',dpi=160)
print('Figura guardada')

import argparse,csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('--vistas',type=Path,required=True);p.add_argument('--salida',type=Path,required=True);a=p.parse_args();a.salida.mkdir(parents=True,exist_ok=True)
with a.vistas.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
geos=['geo-test-01','geo-test-02','geo-test-03','geo-gen-01'];fig,axes=plt.subplots(3,2,figsize=(13,9),layout='constrained')
for j,f in enumerate([.1,.5]):
 r=sorted([r for r in rows if r['model']=='cgan_original' and float(r['fraction_raw'])==f],key=lambda r:(geos.index(r['geometry']),int(r['view'])))
 assert len(r)==24
 for i,(metric,label,scale) in enumerate([('ssim','Diferencia SSIM (positivo: mejora)',1),('psnr','Diferencia PSNR [dB] (positivo: mejora)',1),('Q','Diferencia Q [puntos porcentuales]\n(negativo: menor sesgo)',100)]):
  ax=axes[i,j];ys=[float(x[metric+'_delta'])*scale for x in r];ax.bar(range(24),ys,color=['#197e6e' if (y>=0 if i<2 else y<=0) else '#b95344' for y in ys]);ax.axhline(0,color='black',lw=.8)
  for x in [5.5,11.5,17.5]:ax.axvline(x,color='grey',lw=.6,ls='--')
  ax.set_xticks([2.5,8.5,14.5,20.5],['test-01','test-02','test-03','gen-01']);ax.set_ylabel(label);ax.grid(axis='y',alpha=.2)
  if i==0:ax.set_title(f'cGAN 5 % menos entrada {int(f*100)} %; razón nominal {f/.05:.0f}')
  if i==2:ax.set_xlabel('Seis vistas por geometría, orden 0 a 5')
fig.suptitle('OE3: diferencias por vista de la cGAN original\nPromedios de 20 realizaciones; comparación descriptiva, sin margen de equivalencia',fontsize=13)
fig.savefig(a.salida/'diferencias-vistas.svg',metadata={'Date':None});fig.savefig(a.salida/'diferencias-vistas.png',dpi=150)
print('Figura generada')

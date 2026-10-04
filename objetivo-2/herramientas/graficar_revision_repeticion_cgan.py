import argparse,json,os
from pathlib import Path
import numpy as np
parser=argparse.ArgumentParser(description='Figura descriptiva de la repetición cGAN verificada')
parser.add_argument('--evidencia',type=Path,required=True)
parser.add_argument('--salida',type=Path,required=True)
args=parser.parse_args()
r=args.salida;r.mkdir(parents=True,exist_ok=False)
os.environ['MPLCONFIGDIR']=str(r/'mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
 proof=json.loads(args.evidencia.read_text(encoding='utf-8'))
 assert proof['complete'],'La figura requiere auditoria completa'
 pairs=['R1','R2','R3'];summaries=[proof['evaluation'][p]['summary'] for p in pairs]
 fig,axes=plt.subplots(1,3,figsize=(13.8,4.6),layout='constrained')
 x=np.arange(3);w=.34
 ax=axes[0]
 for label,off,color in [('C0',-w/2,'#657a8e'),('C1',w/2,'#247c9b')]:
  vals=[100*s[label]['Q'] for s in summaries];bars=ax.bar(x+off,vals,w,label=label,color=color)
  ax.bar_label(bars,fmt='%.2f',padding=3,fontsize=9)
 ax.axhline(100*summaries[0]['entrada']['Q'],color='#73583b',linestyle=':',label='Entrada')
 ax.set_ylim(0,16);ax.set_ylabel('Q regional (%)');ax.set_title('Sesgo regional: menor es mejor');ax.legend(fontsize=9)
 for ax,metric,factor,title,ylabel,goodnegative in [(axes[1],'edge_mae',100,'C1 aumenta el error de borde','C1 − C0 (puntos porcentuales)',True),(axes[2],'ssim',1,'SSIM: el signo cambia en R3','SSIM de C1 − SSIM de C0',False)]:
  vals=[factor*(s['C1'][metric]-s['C0'][metric]) for s in summaries]
  colors=['#247c9b' if (v<0 if goodnegative else v>0) else '#b05b42' for v in vals]
  bars=ax.bar(x,vals,.55,color=colors);ax.axhline(0,color='#555555',linewidth=.8)
  ax.bar_label(bars,labels=[f'{v:+.3f}' if factor==100 else f'{v:+.5f}' for v in vals],padding=4,fontsize=9)
  ax.margins(y=.3);ax.set_title(title);ax.set_ylabel(ylabel)
 for ax in axes:ax.set_xticks(x,pairs);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
 fig.suptitle('Repetición cGAN al 5 % · tres semillas de continuación\nMismo checkpoint inicial · ninguna pareja satisface los ocho criterios',fontsize=13)
 fig.savefig(r/'sintesis-repeticion-verificada.png',dpi=160)
 fig.savefig(r/'sintesis-repeticion-verificada.pdf')
 plt.close(fig)
if __name__=='__main__':main()


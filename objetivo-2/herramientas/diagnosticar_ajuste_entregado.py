"""Diagnóstico por geometría/vista; conserva criterios fijados, no entrena."""
import argparse,json,sys,os,hashlib
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser()
for n in ['repo','datos','mascaras','entrega','predicciones_iniciales','salida']:p.add_argument('--'+n.replace('_','-'),type=Path,required=True)
a=p.parse_args();a.salida.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(a.salida/'mpl-cache')
sys.path.insert(0,str(a.repo/'objetivo-2/herramientas'))
from datos_ajuste import Store,read_json,digest,atomic_json
from evaluar_ajuste import analyze_predictions
store=Store(a.datos,a.mascaras)
if digest(a.predicciones_iniciales)!='c4e35ef07c46974b4847ec46ea60173c6f1a44e1c6f33f0639f2aea2e58ec9fc':raise ValueError('Predicciones iniciales distintas')
keys=read_json(a.entrega/'piloto/A/indices-val.json')
initial=np.load(a.predicciones_iniciales,allow_pickle=False,mmap_mode='r')
# Dos copias de la misma referencia solo permiten reutilizar el cálculo de métricas.
# No constituye un ensayo A/B adicional ni una regla nueva de selección.
base=analyze_predictions(store,keys,{'A':initial,'B':initial},'piloto')
current=read_json(a.entrega/'comparacion-piloto.json')
datasets={'inicial':base,'A':current,'B':current}
rows=[]
for model,data in datasets.items():
 key='A' if model=='inicial' else model
 for r in data['regions']:
  if r['model']==key:rows.append(dict(r,model=model))
summary={'initial':base['summary']['A'],'A':current['summary']['A'],'B':current['summary']['B']}
diagnostic={'schema':'oe2-adjustment-regional-diagnostic-v1','initial_predictions_sha256':digest(a.predicciones_iniciales),'initial_predictions_source':'Inferencia CPU verificada del checkpoint U-Net de época 5; reutilizada sin entrenamiento','heldout_opened':False,'summary':summary,'families':{},'by_view':[]}
for model in datasets:
 rr=[r for r in rows if r['model']==model]
 diagnostic['families'][model]={str(f):{'signed_bias_mean':float(np.mean([r['bias']['mean'] for r in rr if r['family']==f])),'absolute_mean_bias':float(np.mean([abs(r['bias']['mean']) for r in rr if r['family']==f])),'mae_mean':float(np.mean([r['mae']['mean'] for r in rr if r['family']==f]))} for f in range(4)}
for g,v in sorted({(r['geometry'],r['view']) for r in rows}):
 item={'geometry':g,'view':v,'models':{}}
 for model in datasets:
  rr=[r for r in rows if r['model']==model and r['geometry']==g and r['view']==v]
  item['models'][model]={'Q':float(.5*(np.mean([abs(r['bias']['mean']) for r in rr if r['family']==1])+np.mean([abs(r['bias']['mean']) for r in rr if r['family']==3]))),'edge_mae':next(r['mae']['mean'] for r in rr if r['family']==2),'anomalies':{r['region']:r['bias']['mean'] for r in rr if r['family']==3}}
 diagnostic['by_view'].append(item)
diagnostic['views_Q_improved_B_vs_A']=sum(x['models']['B']['Q']<x['models']['A']['Q'] for x in diagnostic['by_view'])
diagnostic['views_edge_worse_B_vs_A']=sum(x['models']['B']['edge_mae']>x['models']['A']['edge_mae'] for x in diagnostic['by_view'])
atomic_json(a.salida/'diagnostico-regional.json',diagnostic)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(2,1,figsize=(12,7),constrained_layout=True)
x=np.arange(18);labels=[r['geometry'].replace('geo-val-','G')+' / '+str(r['view']) for r in diagnostic['by_view']]
for model,color,label in [('inicial','#777777','U-Net inicial (época 5)'),('A','#176b9d','A: continuación original'),('B','#d06a13','B: ajuste regional')]:
 for ax,key in zip(axes,['Q','edge_mae']):ax.plot(x,[100*r['models'][model][key] for r in diagnostic['by_view']],marker='o',ms=4,color=color,label=label)
axes[0].set_ylabel('Sesgo regional Q por vista (%)');axes[1].set_ylabel('Error absoluto de borde (%)')
for ax in axes:
 ax.set_xticks(x,labels,rotation=45,ha='right');ax.grid(alpha=.2);ax.axvline(5.5,color='gray',lw=.6);ax.axvline(11.5,color='gray',lw=.6)
axes[0].legend(ncol=3,fontsize=9);fig.suptitle('Ajuste de cuentas: mejora regional y costo en los bordes\nValidación exploratoria · 3 geometrías, 6 vistas por geometría · menor es mejor')
fig.savefig(a.salida/'diagnostico-regional.png',dpi=150);fig.savefig(a.salida/'diagnostico-regional.pdf');fig.savefig(a.salida/'diagnostico-regional.svg');plt.close(fig)
print(json.dumps({'summary':summary,'families':diagnostic['families'],'views_Q_improved':diagnostic['views_Q_improved_B_vs_A'],'views_edge_worse':diagnostic['views_edge_worse_B_vs_A']},indent=2),flush=True)

"""Resumen descriptivo y figura; las vistas no se tratan como independientes."""
import argparse,json,sys,os
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--evaluacion',type=Path,required=True)
p.add_argument('--salida',type=Path,required=True)
p.add_argument('--dependencias',type=Path)
a=p.parse_args()
if a.dependencias:sys.path.insert(0,str(a.dependencias))
import numpy as np
a.salida.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(a.salida/'mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
j=json.loads(a.evaluacion.read_text());rows=j['regions'];contrasts=j['contrasts']
keys=['cielo','borde_cono','roca_sin_anomalia','anomalia_0_conduit','anomalia_0_cavity','anomalia_1_dense_body']
labels=['Cielo','Borde del cono','Roca sin anomalía','Conductos','Cavidad','Cuerpo denso']
methods=['entrada','unet','cgan'];result={'aggregation':'mean of view-level means, unweighted; descriptive, no independent-view CI','regions':{},'contrast':{}}
for k in keys:
    result['regions'][k]={}
    for m in methods:
        v=[x for x in rows if x['region']==k and x.get('model')==m]
        result['regions'][k][m]={'views':len(v),'bias_percent':float(np.mean([x['bias_relative']['mean'] for x in v])*100),'mae_percent':float(np.mean([x['mae_relative']['mean'] for x in v])*100),'mean_absolute_bias_percent':float(np.mean([abs(x['bias_relative']['mean']) for x in v])*100)}
for m in methods:
    v=[x['models'][m] for x in contrasts if x['status']=='estimable']
    # Para comparar los tres métodos, se conserva también el subconjunto con 20 cocientes válidos en todos.
    complete=[x['models'][m] for x in contrasts if x['status']=='estimable' and all(y['valid_realizations']==20 for y in x['models'].values())]
    result['contrast'][m]={'regions':len(v),'zero_control_realizations':sum(x['zero_control_realizations'] for x in v),'mean_absolute_error_pp':float(np.mean([x['absolute_error']['mean'] for x in v])*100),'complete_regions':len(complete),'complete_mean_absolute_error_pp':float(np.mean([x['absolute_error']['mean'] for x in complete])*100),'mean_contrast_same_sign_regions':sum(np.sign(x['models'][m]['contrast']['mean'])==np.sign(x['reference_contrast']) for x in contrasts if x['status']=='estimable')}
fig,axes=plt.subplots(1,2,figsize=(12,5),constrained_layout=True)
colors=['#687787','#267bbd','#ce702f'];y=np.arange(6)
for i,(m,label,color) in enumerate(zip(methods,['Entrada n/f','U-Net L1','cWGAN-GP'],colors)):
    for ax,metric in zip(axes,['bias_percent','mae_percent']):
        ax.barh(y+(i-1)*.23,[result['regions'][k][m][metric] for k in keys],height=.22,label=label,color=color)
for ax in axes:
    ax.set_yticks(y,labels);ax.invert_yaxis();ax.axvline(0,color='#333333',linewidth=.7);ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
axes[0].set_title('Sesgo de las cuentas');axes[0].set_xlabel('Sesgo relativo de la suma de cuentas (%)')
axes[1].set_title('Error absoluto por píxel, agregado');axes[1].set_xlabel('Suma |error| / suma referencia (%)');axes[1].legend(loc='upper center',bbox_to_anchor=(.5,-.15),ncol=3,fontsize=9)
fig.suptitle('Validación al 5 % · regiones geométricas · promedio entre vistas\n18 vistas en cielo/roca/borde; 12 en conductos; 6 en cavidad/cuerpo denso',fontsize=11)
fig.savefig(a.salida/'balance-regiones.svg');fig.savefig(a.salida/'balance-regiones.png',dpi=140)
(a.salida/'resumen-regiones.json').write_text(json.dumps(result,indent=2,default=int)+'\n',encoding='utf-8')
print(json.dumps(result['contrast'],indent=2,default=int))

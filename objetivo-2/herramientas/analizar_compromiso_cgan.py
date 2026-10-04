"""Análisis descriptivo por vista y anomalía; no entrena ni acepta física."""
import argparse,csv,json,os
from pathlib import Path
import numpy as np
from datos_ajuste import Store,read_json,digest,atomic_json
from evaluar_ajuste import analyze_predictions

def main(a):
    a.salida.mkdir(parents=True,exist_ok=False)
    e=read_json(a.comparacion);an=read_json(a.anomalias)
    if digest(a.predicciones_iniciales)!=e['initial_predictions_sha256']:raise ValueError('Predicciones iniciales distintas')
    store=Store(a.datos,a.mascaras)
    keys=[[g,v,k] for g in store.manifest['splits']['val'] for v in range(6) for k in range(20)]
    z=np.load(a.predicciones_iniciales,allow_pickle=False)
    base=analyze_predictions(store,keys,{'A':z,'B':z},'piloto')
    for k,v in base['summary']['A'].items():
        if isinstance(v,(int,float)):assert np.isclose(v,e['summary']['inicial_cgan'][k],rtol=0,atol=1e-12),k
        elif isinstance(v,dict):
            for g,x in v.items():assert abs(x-e['summary']['inicial_cgan'][k][g])<1e-12
    images=e['images']+[{**r,'model':'inicial_cgan'} for r in base['images'] if r['model']=='A']
    regions=e['regions']+[{**r,'model':'inicial_cgan'} for r in base['regions'] if r['model']=='A']
    methods=['entrada','inicial_cgan','C0','C1'];views=[]
    for g in store.manifest['splits']['val']:
        for v in range(6):
            row={'geometry':g,'view':v}
            for m in methods:
                rr=[r for r in regions if (r['geometry'],r['view'],r['model'])==(g,v,m)]
                ii=[r for r in images if (r['geometry'],r['view'],r['model'])==(g,v,m)]
                row[m]={'Q':float((np.mean([abs(r['bias']['mean']) for r in rr if r['family']==1])+np.mean([abs(r['bias']['mean']) for r in rr if r['family']==3]))/2),
                        'ssim':float(np.mean([r['ssim'] for r in ii])),'psnr':float(np.mean([r['psnr'] for r in ii])),
                        'sky_mae':next(r['mae']['mean'] for r in rr if r['family']==0),'edge_mae':next(r['mae']['mean'] for r in rr if r['family']==2)}
            views.append(row)
    for m in methods:
        for metric in ['Q','ssim','psnr','sky_mae','edge_mae']:
            assert abs(np.mean([r[m][metric] for r in views])-e['summary'][m][metric])<1e-12,(m,metric)
    counts={}
    for baseline in ['C0','inicial_cgan','entrada']:
        counts[baseline]={k:{'better':sum((r['C1'][k]-r[baseline][k])*direction<0 for r in views),
                            'worse':sum((r['C1'][k]-r[baseline][k])*direction>0 for r in views),
                            'equal':sum(r['C1'][k]==r[baseline][k] for r in views)} for k,direction in [('Q',1),('ssim',-1),('psnr',-1),('sky_mae',1),('edge_mae',1)]}
    anomalies=[]
    for row in an['rows']:
        c=next(x for x in e['contrasts'] if (x['geometry'],x['view'],x['region'])==(row['geometry'],row['view'],row['region']))
        b=next(x for x in base['contrasts'] if (x['geometry'],x['view'],x['region'])==(row['geometry'],row['view'],row['region']))
        merged={**c.get('models',{}),'inicial_cgan':b.get('models',{}).get('A')}
        contrast={'status':c['status'],'reference':c.get('reference_contrast'),'common':c['status']=='estimable' and all(x and x['valid_realizations']==20 for x in merged.values()),'models':merged}
        anomalies.append({**row,'contrast':contrast})
    result={'schema':'oe2-cgan-tradeoff-v1','date':'2026-10-04','sources':{str(p.name):digest(p) for p in [a.comparacion,a.anomalias,a.predicciones_iniciales]},'views':views,'view_counts':counts,'anomalies':anomalies,'summary':e['summary'],'existing_decision':e['decision'],'physical_acceptance':False,'heldout_opened':False,'training_repeated':False}
    result['worst_anomalies_C1']=sorted([{'geometry':r['geometry'],'view':r['view'],'region':r['region'],'pixels':r['pixels'],'reference_sum':r['reference_sum'],'signed_bias':r['models']['C1']['signed_bias'],'delta_absolute_bias_vs_C0':r['models']['C1']['absolute_mean_bias']-r['models']['C0']['absolute_mean_bias'],'delta_absolute_bias_vs_initial':r['models']['C1']['absolute_mean_bias']-r['models']['inicial_cgan']['absolute_mean_bias']} for r in anomalies],key=lambda x:abs(x['signed_bias']),reverse=True)
    common=[r for r in anomalies if r['contrast']['common']]
    result['contrast_counts']={b:{'common':len(common),'better':sum(r['contrast']['models']['C1']['error']['mean_absolute']<r['contrast']['models'][b]['error']['mean_absolute'] for r in common),'worse':sum(r['contrast']['models']['C1']['error']['mean_absolute']>r['contrast']['models'][b]['error']['mean_absolute'] for r in common)} for b in ['C0','inicial_cgan']}
    result['contrast_sign_inversions_C1']=[{'geometry':r['geometry'],'view':r['view'],'region':r['region'],'reference':r['contrast']['reference'],'predicted_mean':r['contrast']['models']['C1']['contrast']['mean']} for r in common if r['contrast']['reference']*r['contrast']['models']['C1']['contrast']['mean']<0]
    result['script_sha256']=digest(Path(__file__))
    atomic_json(a.salida/'compromiso-cgan.json',result)
    with (a.salida/'vistas.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['geometry','view','model','Q','ssim','psnr','sky_mae','edge_mae'];w=csv.DictWriter(f,fields);w.writeheader()
        for r in views:
            for m in methods:w.writerow({'geometry':r['geometry'],'view':r['view'],'model':m,**r[m]})
    os.environ['MPLCONFIGDIR']=str(a.salida/'mpl-cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(3,2,figsize=(12,10),layout='constrained')
    labels=[r['geometry'].replace('geo-val-','G')+'/V'+str(r['view']) for r in views]
    for col,b in enumerate(['C0','inicial_cgan']):
        for row,(metric,factor,label) in enumerate([('Q',100,'ΔQ (puntos porcentuales; negativo mejora)'),('ssim',1,'ΔSSIM (positivo mejora)'),('edge_mae',100,'ΔMAE borde (puntos porcentuales; negativo mejora)')]):
            ax=axes[row,col];vals=[factor*(r['C1'][metric]-r[b][metric]) for r in views]
            ax.bar(range(18),vals,color=['#236f9d' if (v>=0 if metric=='ssim' else v<=0) else '#b04f39' for v in vals]);ax.axhline(0,color='black',linewidth=.7)
            ax.set_ylabel(label);ax.set_xticks(range(18),labels,rotation=90,fontsize=7);ax.grid(axis='y',alpha=.2)
            if row==0:ax.set_title('C1 menos '+b)
    fig.suptitle('cGAN al 5 % · compromiso por las 18 vistas\nUna semilla de continuación; azul mejora, naranja empeora; sin aceptación física')
    fig.savefig(a.salida/'compromiso-vistas.png',dpi=150);fig.savefig(a.salida/'compromiso-vistas.pdf');plt.close(fig)
    print(json.dumps({'view_counts':counts,'worst_anomalies':result['worst_anomalies_C1'][:8]},ensure_ascii=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['comparacion','anomalias','predicciones-iniciales','datos','mascaras','salida']:p.add_argument('--'+n,type=Path,required=True)
    main(p.parse_args())

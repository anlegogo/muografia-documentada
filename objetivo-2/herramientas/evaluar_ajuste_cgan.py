"""Evaluación C0/C1 con referencia cGAN inicial y tabla por anomalía."""
import argparse,json,os
from pathlib import Path
import numpy as np
import torch
from datos_ajuste import Store,read_json,atomic_json,digest,canonical
from ejecutar_ajuste_cgan import configure,spec,load_initial,build_generator,evaluate,PAIR_SEEDS,sources
from revisar_ajuste_cgan import load_completed
from evaluar_ajuste import analyze_predictions

def relabel(value):
    if isinstance(value,dict):return {{'A':'C0','B':'C1'}.get(k,k):relabel(v) for k,v in value.items()}
    if isinstance(value,list):return [relabel(x) for x in value]
    return {'A':'C0','B':'C1'}.get(value,value) if isinstance(value,str) else value

def tables(store,keys,pred,initial,stage):
    main=relabel(analyze_predictions(store,keys,{'A':pred['C0'],'B':pred['C1']},stage))
    baseline=analyze_predictions(store,keys,{'A':initial,'B':initial},stage)
    main['schema']='oe2-cgan-ajuste-comparison-v1'
    main['summary']['inicial_cgan']=baseline['summary']['A']
    rows=[]
    for r in main['regions']:
        if r['family']!=3 or r['model']!='C0':continue
        match=lambda x:x['geometry']==r['geometry'] and x['view']==r['view'] and x['region']==r['region']
        selected={m:next(x for x in main['regions'] if match(x) and x['model']==m) for m in ['entrada','C0','C1']}
        selected['inicial_cgan']=next(x for x in baseline['regions'] if match(x) and x['model']=='A')
        row={k:r[k] for k in ['geometry','view','region','pixels','reference_sum']}
        row['models']={m:{'signed_bias':x['bias']['mean'],'absolute_mean_bias':abs(x['bias']['mean']),
                           'mean_absolute_bias':x['bias']['mean_absolute'],'spatial_mae':x['mae']['mean']} for m,x in selected.items()}
        row['C1_bias_worse_than_C0']=row['models']['C1']['absolute_mean_bias']>row['models']['C0']['absolute_mean_bias']
        row['C1_bias_worse_than_initial']=row['models']['C1']['absolute_mean_bias']>row['models']['inicial_cgan']['absolute_mean_bias']
        rows.append(row)
    main['anomaly_diagnostics']={'rows':len(rows),'worse_bias_vs_C0':sum(x['C1_bias_worse_than_C0'] for x in rows),
                                'worse_bias_vs_initial':sum(x['C1_bias_worse_than_initial'] for x in rows),
                                'physical_acceptance':False,'note':'Salvaguarda descriptiva; no cambia retrospectivamente la regla de decisión ni acredita calidad en etapa técnica.'}
    return main,rows

def figures(store,keys,pred,initial,out,stage):
    os.environ['MPLCONFIGDIR']=str(out/'mpl-cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    for gid in sorted({g for g,v,k in keys}):
        views=sorted({v for g,v,k in keys if g==gid});ref,low=store.load(gid)
        with np.load(store.data/f'dataset-v2/shards/{gid}.npz') as z:
            extent=[float(z['az_edges_deg'][0]),float(z['az_edges_deg'][-1]),float(z['el_edges_deg'][0]),float(z['el_edges_deg'][-1])]
        fig,axes=plt.subplots(len(views),7,figsize=(20,3*len(views)+.7),squeeze=False,constrained_layout=True)
        for row,vi in enumerate(views):
            ii=[j for j,(g,v,k) in enumerate(keys) if (g,v)==(gid,vi)];kk=[keys[j][2] for j in ii]
            y=np.log1p(ref[vi].astype(float));y=y/(store.scale+y)
            x=np.log1p(low[vi,kk].astype(float)/.05);x=x/(store.scale+x)
            c0=pred['C0'][ii].mean(0);c1=pred['C1'][ii].mean(0)
            panels=[y,x.mean(0),initial[ii].mean(0),c0,c1,c0-y,c1-y]
            for col,data in enumerate(panels):
                ax=axes[row,col]
                im=ax.imshow(data,origin='lower',extent=extent,aspect='auto',cmap='viridis' if col<5 else 'RdBu_r',vmin=0 if col<5 else -.08,vmax=.55 if col<5 else .08)
                if row==0:ax.set_title(['Referencia','Entrada','cGAN inicial','C0: control','C1: regional','Residuo C0','Residuo C1'][col])
                if col==0:ax.set_ylabel(f'Vista {vi}\nElevación (°)')
                if row==len(views)-1:ax.set_xlabel('Azimut (°)')
        fig.colorbar(im,ax=axes[:,5:].ravel().tolist(),shrink=.6,label='Predicción − referencia normalizada')
        fig.suptitle(f'{gid} · cGAN · etapa {stage} · medias por vista\n'+('Prueba técnica: no concluir calidad' if stage=='tecnica' else '20 realizaciones por vista; métricas por imagen'),fontsize=12)
        fig.savefig(out/f'{gid}.png',dpi=120);plt.close(fig)

def run(a):
    configure();store=Store(a.datos,a.mascaras)
    paths={'C0':a.control,'C1':a.regional}
    pair=getattr(a,'pareja',None)
    cfg=spec('C0',pair)
    states={arm:load_completed(path,arm,a.etapa,pair) for arm,path in paths.items()}
    for key in ['pair','seed','environment','sources','cache_sha256','data_manifest_sha256','train_indices_sha256','val_indices_sha256','initial_generator_sha256','initial_critic_sha256']:
        if states['C0']['identity'][key]!=states['C1']['identity'][key]:raise ValueError('Comparación no pareada: '+key)
    if states['C0']['identity']['cache_sha256']!=store.identity:raise ValueError('Caché distinta de la usada en entrenamiento')
    keys=read_json(a.control/'indices-val.json')
    expected=store.indices('val',cfg,a.etapa)
    if keys!=[list(x) for x in expected] or keys!=read_json(a.regional/'indices-val.json'):raise ValueError('Muestras incorrectas')
    device=torch.device(a.dispositivo)
    if device.type=='cuda' and not torch.cuda.is_available():raise RuntimeError('CUDA no disponible')
    initial_states=load_initial(a.pesos,cfg,store)
    G=build_generator(cfg['generator']).to(device);G.load_state_dict(initial_states[0],strict=True)
    _,initial,_=evaluate(G,store,expected,device);del G,initial_states,states
    pred={arm:np.load(path/'predicciones-val.npy',mmap_mode='r',allow_pickle=False) for arm,path in paths.items()}
    result,rows=tables(store,keys,pred,initial,a.etapa)
    result['pair']=pair;result['seed']=cfg['seed'];result['sources']=sources()
    result['environment']=read_json(a.control/'identity.json')['environment']
    result['run_paths']={arm:str(path.resolve()) for arm,path in paths.items()}
    result['checkpoint_sha256']={arm:digest(path/'last.pt') for arm,path in paths.items()}
    result['initial_checkpoint_sha256']=digest(a.pesos)
    result['initial_inference_device']=str(device)
    a.salida.mkdir(parents=True,exist_ok=False)
    np.save(a.salida/'predicciones-cgan-inicial.npy',initial)
    result['initial_predictions_sha256']=digest(a.salida/'predicciones-cgan-inicial.npy')
    atomic_json(a.salida/'comparacion-cgan.json',result)
    atomic_json(a.salida/'anomalias-cgan.json',{'stage':a.etapa,'quality_evaluation':a.etapa=='piloto','rows':rows,'physical_acceptance':False})
    if a.figuras:figures(store,keys,pred,initial,a.salida,a.etapa)
    print(json.dumps({'stage':a.etapa,'decision':result['decision'],'anomaly_diagnostics':result['anomaly_diagnostics'],'summary':result['summary']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pareja',choices=list(PAIR_SEEDS))
    for n in ['datos','mascaras','pesos','control','regional','salida']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--etapa',choices=['tecnica','piloto'],required=True);p.add_argument('--dispositivo',choices=['cpu','cuda'],default='cpu')
    p.add_argument('--figuras',action='store_true');run(p.parse_args())


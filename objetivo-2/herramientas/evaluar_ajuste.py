"""Comparación A/B completa o comprobación reducida; no selecciona épocas."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from datos_ajuste import ROOT,Store,sources,read_json,atomic_json,digest
from revisar_ajuste import load_completed
from evaluar_regiones_geometricas import rays,masks,match_controls,morphology
sys.path.insert(0,str(ROOT/'objetivo-2/implementacion/scripts/evaluation'))
from metrics import compute_ssim,compute_psnr

def stat(v):
    v=np.asarray(v,dtype=float)
    return {'mean':float(v.mean()),'mean_absolute':float(np.abs(v).mean()),'min':float(v.min()),'max':float(v.max())} if len(v) else None

def compare(args):
    store=Store(args.datos,args.mascaras);runs={'A':args.control,'B':args.regional};checkpoints={}
    for name,path in runs.items():checkpoints[name]=load_completed(path,name,args.etapa,sources())
    for key in ['stage','cache_sha256','environment','initial_generator_sha256','initial_checkpoint_sha256','train_indices_sha256','val_indices_sha256']:
        if checkpoints['A']['identity'][key]!=checkpoints['B']['identity'][key]:raise ValueError('Comparación no pareada: '+key)
    keys=read_json(args.control/'indices-val.json')
    if keys!=read_json(args.regional/'indices-val.json'):raise ValueError('Orden de predicciones diferente')
    predictions={k:np.load(v/'predicciones-val.npy',mmap_mode='r',allow_pickle=False) for k,v in runs.items()}
    output=analyze_predictions(store,keys,predictions,args.etapa)
    output['checkpoint_sha256']={k:digest(v/'last.pt') for k,v in runs.items()}
    atomic_json(args.salida,output)
    print(json.dumps({'stage':args.etapa,'images':len(output['images']),'decision':output['decision'],'summary':output['summary']},indent=2))
    return output

def analyze_predictions(store,keys,predictions,stage):
    if stage not in ('tecnica','piloto'):raise ValueError('Etapa inválida')
    if stage=='piloto':
        expected=[[g,v,k] for g in store.manifest['splits']['val'] for v in range(6) for k in range(20)]
        if keys!=expected:raise ValueError('El análisis completo requiere los 360 pares ordenados de val')
    if set(predictions)!={'A','B'}:raise ValueError('Se requieren dos arreglos pareados')
    for values in predictions.values():
        if values.shape!=(len(keys),256,256) or not np.isfinite(values).all() or np.any((values<0)|(values>=1)):raise ValueError('Predicción fuera de contrato')
    output={'schema':'oe2-ajuste-comparison-v1','stage':stage,'quality_evaluation':stage=='piloto','heldout_opened':False,'mask_manifest_sha256':store.identity,'images':[],'regions':[],'contrasts':[]}
    cfg=store.manifest['geometry_protocol'];scale=store.scale
    for gid,vi in sorted({(g,v) for g,v,k in keys}):
        indices=[i for i,(g,v,k) in enumerate(keys) if (g,v)==(gid,vi)]
        realizations=[keys[i][2] for i in indices];refs,low=store.load(gid);ref=refs[vi].astype(float)
        counts={'entrada':low[vi,realizations].astype(float)/.05};norm={}
        for name,p in predictions.items():
            z=p[indices].astype(float);exponent=scale*z/(1-z)
            if np.any(exponent>np.log(np.finfo(float).max)-1):raise ValueError('Salida no invertible a cuentas')
            counts[name]=np.expm1(exponent);norm[name]=z
        l=np.log1p(counts['entrada']);norm['entrada']=l/(scale+l)
        l=np.log1p(ref);target=l/(scale+l)
        for name,z in norm.items():
            for j,k in enumerate(realizations):
                output['images'].append({'geometry':gid,'view':vi,'realization':k,'model':name,'ssim':compute_ssim(z[j].astype(np.float32),target.astype(np.float32)),'psnr':compute_psnr(target.astype(np.float32),z[j].astype(np.float32))})
        geometry=read_json(ROOT/f'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries/{gid}.json')
        with np.load(store.data/f'dataset-v2/shards/{gid}.npz') as z:o,d=rays(z['az_centers_deg'],z['el_centers_deg'],vi,cfg)
        L,aa,reg=masks(geometry,o,d,cfg)
        cached=store.masks[gid][vi]
        for j,(name,m) in enumerate(reg.items()):
            if not np.array_equal(cached[j],m):raise ValueError('Máscara recomputada distinta del caché')
            base=ref[m].sum()
            if base<=0:raise ValueError('Referencia regional vacía; se requiere revisión')
            for method,value in counts.items():
                err=value[:,m]-ref[m]
                output['regions'].append({'geometry':gid,'view':vi,'region':name,'family':store.manifest['geometries'][gid]['families'][j],'model':method,'pixels':int(m.sum()),'reference_sum':float(base),'bias':stat(err.sum(1)/base),'mae':stat(np.abs(err).sum(1)/base)})
        for i,an in enumerate(geometry['anomalies']):
            name=f"anomalia_{i}_{an['kind']}";m=reg[name].copy()
            for j,ll in enumerate(aa):
                if i!=j:m&=~morphology(ll>0,cfg['rock_sky_margin_pixels'],False)
            t,donors=match_controls(m,reg['roca_sin_anomalia'],L,cfg)
            coverage=len(t)/int(m.sum()) if m.any() else 0
            item={'geometry':gid,'view':vi,'region':name,'matched_pixels':len(t),'match_fraction':coverage,'status':'insufficient_geometry'}
            if len(t)>=cfg['min_matched_pixels'] and coverage>=cfg['min_match_fraction']:
                def contrast(x):
                    x=x.reshape(-1,65536);den=x[:,donors].mean((1,2))
                    return np.divide(x[:,t].mean(1),den,out=np.full(len(x),np.nan),where=den>0)-1
                cr=contrast(ref)[0]
                if np.isfinite(cr):
                    item.update(status='estimable',reference_contrast=float(cr),models={})
                    for name,cc in counts.items():
                        c=contrast(cc);valid=np.isfinite(c);values=c[valid]
                        item['models'][name]={'valid_realizations':int(valid.sum()),'zero_control_realizations':int((~valid).sum()),'contrast':stat(values),'error':stat(values-cr)}
            output['contrasts'].append(item)
    summary={}
    for name in counts:
        data=[x for x in output['images'] if x['model']==name]
        regional=[x for x in output['regions'] if x['model']==name]
        by_geometry={}
        for gid in sorted({x['geometry'] for x in regional}):
            rr=[x for x in regional if x['geometry']==gid]
            rock=[abs(x['bias']['mean']) for x in rr if x['family']==1]
            # Igual peso por vista y anomalía dentro de cada vista.
            anomaly_by_view=[np.mean([abs(x['bias']['mean']) for x in rr if x['family']==3 and x['view']==v]) for v in sorted({x['view'] for x in rr})]
            by_geometry[gid]=float((np.mean(rock)+np.mean(anomaly_by_view))/2)
        complete=[x for x in output['contrasts'] if x['status']=='estimable' and all(y['valid_realizations']==(20 if stage=='piloto' else len([k for k in keys if (k[0],k[1])==(x['geometry'],x['view'])])) for y in x['models'].values())]
        summary[name]={'ssim':float(np.mean([x['ssim'] for x in data])),'psnr':float(np.mean([x['psnr'] for x in data])),'Q_by_geometry':by_geometry,'Q':float(np.mean(list(by_geometry.values()))),'sky_mae':float(np.mean([x['mae']['mean'] for x in regional if x['family']==0])),'edge_mae':float(np.mean([x['mae']['mean'] for x in regional if x['family']==2])),'common_contrasts':len(complete),'contrast_absolute_error':float(np.mean([x['models'][name]['error']['mean_absolute'] for x in complete])) if complete else None}
    # Estas magnitudes técnicas no son el Q completo de seis vistas.
    output['summary']=summary
    if stage=='piloto':
        A,B=summary['A'],summary['B']
        checks={'Q_reduced':B['Q']<A['Q'],'each_geometry_not_worse':all(B['Q_by_geometry'][g]<=A['Q_by_geometry'][g] for g in A['Q_by_geometry']),'sky_not_worse':B['sky_mae']<=A['sky_mae'],'edge_not_worse':B['edge_mae']<=A['edge_mae'],'contrast_support_unchanged':A['common_contrasts']==B['common_contrasts']==23,'contrast_not_worse':B['contrast_absolute_error'] is not None and B['contrast_absolute_error']<=A['contrast_absolute_error'],'ssim_not_worse':B['ssim']>=A['ssim'],'psnr_not_worse':B['psnr']>=A['psnr']}
        output['decision_checks']=checks
        output['decision']='mejora_concordante_descriptiva' if all(checks.values()) else 'compromiso' if checks['Q_reduced'] else 'sin_mejora_del_indicador_principal'
    else:output['decision']='solo_comprobacion_tecnica_no_decision_de_calidad'
    output['physical_acceptance']=False
    return output

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['datos','mascaras','control','regional','salida']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--etapa',choices=['tecnica','piloto'],required=True)
    compare(p.parse_args())

"""Complemento multifracción OE3. Pesos congelados; sin entrenamiento."""
import os
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import argparse,csv,json,sys,time,shutil
from pathlib import Path
import numpy as np
from metricas_locales_oe3 import local_metrics,repeated_contrast_signal,assessed_fraction

INDEX={.5:0,.1:1,.05:2,.01:3}
def tag(f):return {0.01:'f001',0.05:'f005',0.1:'f010',0.5:'f050'}[f]
def setup(a):
    sys.path.insert(0,str(a.repo/'objetivo-2/herramientas'))
    sys.path.insert(0,str(a.repo/'objetivo-2/implementacion/scripts/evaluation'))
    import evaluacion_final_oe2 as e
    s,signature=e.contract(a.repo);p=e.read(a.spec)
    e.check(p['ef01_sha256']==signature,'Contrato EF01 distinto')
    e.check(p['fractions']==[.01,.05,.1,.5] and p['new_fractions']==[.01,.1,.5],'Fracciones distintas')
    e.check(p['models']==list(s['models']),'Modelos distintos')
    for name,h in p['tool_sha256'].items():e.check(e.sha(Path(__file__).parent/name)==h,'Herramienta modificada '+name)
    e.check(e.sha(a.registry)==p['registry_sha256'],'Registro C2 distinto')
    return e,s,signature,p
def old_predictions(e,s,signature,root):
    for m in s['models']:
        done=e.read(root/m/'completed.json');identity=done['identity']
        e.check(identity['protocol_sha256']==signature and identity['checkpoint_sha256']==s['models'][m]['sha256'] and identity['model']==m and identity['fraction']==.05,'Entrega f05 incompatible')
        e.check(done['images']==480 and [r['geometry'] for r in done['files']]==s['geometry_order'],'Entrega f05 incompleta')
        for r in done['files']:
            path=root/m/(r['geometry']+'.npy');e.check(r['identity']==identity and e.sha(path)==r['sha256'],'Predicción f05 alterada')
            z=np.load(path,mmap_mode='r',allow_pickle=False)
            e.check(z.shape==(120,256,256) and z.dtype==np.float32 and np.isfinite(z).all() and np.all((z>=0)&(z<1)),'NPY f05 incompatible')
def preflight(a,e,s,signature,p):
    result=e.preflight(a.repo,a.data,e.read(a.weights),s)
    old_predictions(e,s,signature,a.existing)
    from controles_contraste_v2 import Registry
    Registry(signature,e.read(a.registry))
    e.check(p['geometry_order']==s['geometry_order'],'Geometrías distintas')
    return {**result,'existing_f05_images':3840,'reused_f05':True,'registry_verified':True,'complement_sha256':e.sha(a.spec),'new_images_planned':11520}
def configure(device):
    import torch
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True
    torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    if device.startswith('cuda') and not torch.cuda.is_available():raise ValueError('CUDA no disponible')
    return torch.device(device)
def identity(a,e,s,signature,model,f):
    import torch
    return {'complement_sha256':e.sha(a.spec),'ef01_sha256':signature,'model':model,'fraction':f,'checkpoint_sha256':s['models'][model]['sha256'],
        'batch_size':4,'environment':e.env(),'device':str(a.device),'gpu_name':torch.cuda.get_device_name(a.device) if str(a.device).startswith('cuda') else None}
def fraction_input(a,e,s,gid,f):
    e.package(a.data,gid,s)
    with np.load(a.data/f'dataset-v2/shards/{gid}.npz',allow_pickle=False) as z:
        low=z['low_counts'][:,INDEX[f]].copy()
    return e.normalize(low.reshape(120,256,256).astype(np.float64)/f,s['normalization_scale']).astype(np.float32)
def smoke(a,e,s,signature,p):
    import torch
    preflight(a,e,s,signature,p);device=configure(a.device)
    net=e.load_net(Path(e.read(a.weights)[a.model]),a.model,s,a.repo).to(device)
    gid=s['geometry_order'][0];x=fraction_input(a,e,s,gid,.05)[:4]
    with torch.inference_mode():
        t=torch.from_numpy(x[:,None]).to(device);y=net(t).cpu().numpy()[:,0];repeat=net(t).cpu().numpy()[:,0]
    e.check(np.array_equal(y,repeat),'Inferencia continua no determinista')
    old=np.load(a.existing/a.model/(gid+'.npy'),mmap_mode='r')[:4]
    maximum=float(np.max(np.abs(y-old)));e.check(maximum<=p['smoke_max_abs_error'],'Prueba f05 distinta de entrega')
    shapes=[]
    for f in p['new_fractions']:
        x=fraction_input(a,e,s,gid,f)[:4]
        with torch.inference_mode():y=net(torch.from_numpy(x[:,None]).to(device)).cpu().numpy()[:,0]
        e.invert(y,s['normalization_scale']);shapes.append({'fraction':f,'shape':list(y.shape),'finite':True})
    report={'passed':True,'identity':identity(a,e,s,signature,a.model,.05),'max_abs_error_f05':maximum,'new_fraction_shape_checks':shapes,'science_metrics_computed':False}
    e.write(a.output/('smoke-'+a.model+'.json'),report);print(json.dumps(report))
def infer(a,e,s,signature,p):
    import torch
    from filelock import FileLock
    e.check(a.model in s['models'],'Modelo no permitido');preflight(a,e,s,signature,p)
    device=configure(a.device);expected=identity(a,e,s,signature,a.model,.05)
    gate=e.read(a.output/('smoke-'+a.model+'.json'))
    e.check(gate['passed'] and gate['identity']==expected,'Falta smoke del mismo modelo y entorno')
    with FileLock(str(a.output/('.'+a.model+'.lock')),timeout=0):
        net=e.load_net(Path(e.read(a.weights)[a.model]),a.model,s,a.repo).to(device)
        for f in p['new_fractions']:
            root=a.output/tag(f)/a.model;root.mkdir(parents=True,exist_ok=True);ident=identity(a,e,s,signature,a.model,f)
            if (root/'identity.json').exists():e.check(e.read(root/'identity.json')==ident,'Identidad de salida distinta')
            else:e.check(not any(root.iterdir()),'Directorio sin identidad no vacío');e.write(root/'identity.json',ident)
            receipts=[];start=time.monotonic()
            for gid in s['geometry_order']:
                path=root/(gid+'.npy');receipt=root/(gid+'.json')
                if receipt.exists():
                    r=e.read(receipt);e.check(r['identity']==ident and r['geometry']==gid and e.sha(path)==r['sha256'],'Archivo previo incompatible');receipts.append(r);continue
                x=fraction_input(a,e,s,gid,f);z=np.empty_like(x)
                with torch.inference_mode():
                    for i in range(0,120,4):z[i:i+4]=net(torch.from_numpy(x[i:i+4,None]).to(device)).cpu().numpy()[:,0]
                e.invert(z,s['normalization_scale']);tmp=path.with_suffix('.npy.tmp')
                with tmp.open('wb') as file:np.save(file,z,allow_pickle=False)
                os.replace(tmp,path);r={'geometry':gid,'identity':ident,'sha256':e.sha(path),'shape':list(z.shape),'dtype':str(z.dtype),'order':'view*20+realization'}
                e.write(receipt,r);receipts.append(r);print(a.model,f,gid,'120 imágenes',flush=True)
            e.write(root/'completed.json',{'identity':ident,'files':receipts,'images':480,'elapsed_seconds_this_invocation':time.monotonic()-start,'training_performed':False})
def prediction_paths(a,e,s,signature,p,f):
    root=a.existing if f==.05 else a.output/tag(f)
    for m in s['models']:
        done=e.read(root/m/'completed.json');ident=done['identity']
        e.check(ident['model']==m and ident['checkpoint_sha256']==s['models'][m]['sha256'] and ident['fraction']==f,'Identidad incorrecta')
        e.check(ident.get('protocol_sha256')==signature if f==.05 else ident.get('complement_sha256')==e.sha(a.spec),'Protocolo de predicción distinto')
        e.check(done['images']==480 and [x['geometry'] for x in done['files']]==s['geometry_order'],'Entrega incompleta')
        for x in done['files']:e.check(x['identity']==ident and e.sha(root/m/(x['geometry']+'.npy'))==x['sha256'],'NPY alterado')
    return root
def evaluate(a,e,s,signature,p,baseline=False):
    import evaluar_regiones_geometricas as g
    from controles_contraste_v2 import Registry
    preflight(a,e,s,signature,p)
    fractions=[.05] if baseline else p['fractions']
    roots={f:prediction_paths(a,e,s,signature,p,f) for f in fractions}
    a.report.mkdir(parents=True,exist_ok=False);images=[];regions=[];contrasts=[];locals_rows=[];repeat_rows=[]
    original=g.match_controls
    try:
      for f in fractions:
        registry=Registry(signature,e.read(a.registry));g.match_controls=registry
        for gid in s['geometry_order']:
            ref,_,coords=e.package(a.data,gid,s)
            with np.load(a.data/f'dataset-v2/shards/{gid}.npz',allow_pickle=False) as z:low=z['low_counts'][:,INDEX[f]].copy()
            geometry=e.read(a.repo/s['geometry_files'][gid]);preds={m:np.load(roots[f]/m/(gid+'.npy'),allow_pickle=False,mmap_mode='r') for m in s['models']}
            for m,z in preds.items():e.check(z.shape==(120,256,256) and z.dtype==np.float32,'Forma de predicción incompatible')
            for view in range(6):
                start=len(registry.entries);pp={m:z[view*20:(view+1)*20] for m,z in preds.items()}
                ii,rr,cc=e.analyze_view(ref[view].astype(float),low[view].astype(float)*(.05/f),pp,geometry,coords,view,s['regional_protocol'],s['normalization_scale'])
                prefix={'fraction':f,'geometry':gid,'view':view}
                for rows,dest in [(ii,images),(rr,regions),(cc,contrasts)]:dest.extend([{**prefix,**row} for row in rows])
                counts={'referencia':ref[view][None].astype(float),'entrada':low[view].astype(float)/f,**{m:e.invert(z,s['normalization_scale']) for m,z in pp.items()}}
                entries=registry.entries[start:];e.check(len(entries)==len(cc),'Desalineación de controles')
                for item,entry in zip(cc,entries):
                    t=np.asarray(entry['targets'],dtype=int);d=np.asarray(entry['donors'],dtype=int).reshape(-1,5)
                    geometry_ok=len(t)>=s['regional_protocol']['min_matched_pixels'] and item['match_fraction']>=s['regional_protocol']['min_match_fraction']
                    for model,stack in counts.items():
                        rows=[]
                        for k,im in enumerate(stack):
                            row=local_metrics(im,t,d) if geometry_ok else {'status':'insufficient_geometry'}
                            rows.append(row);locals_rows.append({**prefix,'region':item['region'],'model':model,'realization':k,**row})
                        repeat_rows.append({**prefix,'region':item['region'],'model':model,**repeated_contrast_signal(rows)})
            print('Evaluación',f,gid,flush=True)
        e.check(len(registry.entries)==54,'Registro incompleto')
    finally:g.match_controls=original
    summaries={}
    for f in fractions:
        summaries[str(f)]={}
        for split,gids in s['splits'].items():
            filt=lambda records:[x for x in records if x['fraction']==f and x['geometry'] in gids]
            summaries[str(f)][split]=e.summarize(filt(images),filt(regions),filt(contrasts),['entrada']+list(s['models']),gids)
    # Soporte común local explícito entre todas las fracciones y modelos,
    # sin retirar casos de las tablas completas ni inventar ceros.
    universe={(x['geometry'],x['view'],x['region']) for x in locals_rows};common={}
    for metric in ['snr_local_intensity','cnr_local_signed','contrast_counts']:
        common[metric]=[]
        for key in sorted(universe):
            rows=[x for x in locals_rows if (x['geometry'],x['view'],x['region'])==key]
            expected=len(fractions)*(20*9+1)
            if len(rows)==expected and all(x.get(metric) is not None for x in rows):common[metric].append(key)
    benchmark=None
    if not baseline:
        benchmark={split:assessed_fraction(images,p['image_benchmark_thresholds'],fractions,list(s['models']),gids) for split,gids in s['splits'].items()}
    result={'complement_sha256':e.sha(a.spec),'ef01_sha256':signature,'baseline_only':baseline,'fractions':fractions,'environment':e.env(),'summary':summaries,'image_benchmark':benchmark,
        'common_local_support':common,'all_local_keys':sorted(universe),'no_training':True,'physical_equivalence':False,'opacity_reconstructed':False,
        'rows':{'images':len(images),'regions':len(regions),'contrasts':len(contrasts),'local_metrics':len(locals_rows),'repeated_signal':len(repeat_rows)}}
    e.write(a.report/'resultado.json',result);e.write(a.report/'contrastes.json',contrasts);e.write(a.report/'snr_repeticiones.json',repeat_rows)
    for name,rows in [('imagenes',images),('regiones',regions),('metricas_locales',locals_rows)]:
        with (a.report/(name+'.csv')).open('w',encoding='utf-8',newline='') as file:
            w=csv.DictWriter(file,fieldnames=sorted(set().union(*(r.keys() for r in rows))));w.writeheader();w.writerows(rows)
    e.write(a.report/'inventario.json',[{'path':f.name,'sha256':e.sha(f),'bytes':f.stat().st_size} for f in sorted(a.report.iterdir()) if f.is_file()])
    print(json.dumps(result['rows']),flush=True)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('phase',choices=['preflight','smoke','infer','baseline','evaluate'])
    for n in ['repo','data','weights','existing','registry','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--spec',type=Path,default=Path(__file__).resolve().parents[1]/'configuraciones/complemento-v1.json')
    p.add_argument('--model',default='cgan_original');p.add_argument('--device',default='cuda');p.add_argument('--report',type=Path)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);e,s,signature,c=setup(a)
    if a.phase=='preflight':e.write(a.output/'preflight.json',preflight(a,e,s,signature,c));print('Preflight satisfactorio')
    elif a.phase=='smoke':smoke(a,e,s,signature,c)
    elif a.phase=='infer':infer(a,e,s,signature,c)
    else:
        e.check(a.report is not None,'Falta --report');evaluate(a,e,s,signature,c,a.phase=='baseline')
if __name__=='__main__':main()

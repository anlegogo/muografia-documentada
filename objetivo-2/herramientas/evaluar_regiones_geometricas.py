"""Diagnóstico geométrico de val; no reconstruye densidad ni certifica detector."""
import argparse, hashlib, json, platform
from pathlib import Path
import numpy as np

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def solid_interval(o,d,A,B,C,zlim=None,max_t=3000.):
    """Intersección de un sólido convexo cuadrático, con recorte axial opcional.

    Se prueban intervalos entre raíces: admite A negativo y caso lineal.
    La validez del uso min/max requiere convexidad del sólido recortado.
    """
    A,B,C=np.broadcast_arrays(A,B,C)
    shape=A.shape
    lo=np.zeros(shape); hi=np.full(shape,max_t)
    if zlim is not None:
        dz=d[...,2]; nonzero=np.abs(dz)>1e-14
        t0=(zlim[0]-o[2])/np.where(nonzero,dz,1.)
        t1=(zlim[1]-o[2])/np.where(nonzero,dz,1.)
        inside=zlim[0]<=o[2]<=zlim[1]
        lo=np.maximum(lo,np.where(nonzero,np.minimum(t0,t1),0 if inside else max_t))
        hi=np.minimum(hi,np.where(nonzero,np.maximum(t0,t1),max_t if inside else 0))
    quadratic=np.abs(A)>1e-14
    disc=B*B-4*A*C
    root=np.sqrt(np.maximum(disc,0))
    den=np.where(quadratic,2*A,1.)
    r1=(-B-root)/den;r2=(-B+root)/den
    linear=(~quadratic)&(np.abs(B)>1e-14)
    r1=np.where(linear,-C/np.where(linear,B,1),r1)
    real=quadratic&(disc>=0)
    r1=np.where(real|linear,r1,lo);r2=np.where(real,r2,lo)
    knots=np.sort(np.stack([lo,hi,np.clip(r1,lo,np.maximum(lo,hi)),np.clip(r2,lo,np.maximum(lo,hi))]),axis=0)
    lower=np.full(shape,np.inf); upper=np.full(shape,-np.inf)
    for k in range(3):
        a,b=knots[k],knots[k+1]; t=(a+b)/2
        valid=(hi>lo)&(b>a)&(A*t*t+B*t+C<=1e-8)
        lower=np.minimum(lower,np.where(valid,a,np.inf))
        upper=np.maximum(upper,np.where(valid,b,-np.inf))
    return lower,upper

def cone_interval(o,d,R,H,top=.1):
    k=(R-top)/H; rad=R-k*o[2]
    A=np.sum(d[...,:2]**2,axis=-1)-(k*d[...,2])**2
    B=2*(np.sum(o[:2]*d[...,:2],axis=-1)+rad*k*d[...,2])
    C=np.sum(o[:2]**2)-rad**2
    return solid_interval(o,d,A,B,C,(0,H))

def anomaly_interval(o,d,an):
    p=an['params']
    if an['kind']=='conduit':
        q=o[:2]-[p['cx_m'],p['cy_m']]
        return solid_interval(o,d,np.sum(d[...,:2]**2,axis=-1),2*np.sum(q*d[...,:2],axis=-1),np.sum(q*q)-p['radius_m']**2,(p['z0_m'],p['z1_m']))
    center=np.array([p[k] for k in ('cx_m','cy_m','cz_m')])
    axes=np.repeat(p['radius_m'],3) if an['kind']=='cavity' else np.array([p[k] for k in ('ax_m','ay_m','az_m')])
    q=(o-center)/axes;v=d/axes
    return solid_interval(o,d,np.sum(v*v,axis=-1),2*np.sum(q*v,axis=-1),np.sum(q*q)-1)

def length(interval):
    return np.maximum(0,interval[1]-interval[0])

def clipped_length(a,b):
    return np.maximum(0,np.minimum(a[1],b[1])-np.maximum(a[0],b[0]))

def morphology(mask,n,erode):
    pad=np.pad(mask,n,constant_values=False)
    shifted=[pad[i:i+mask.shape[0],j:j+mask.shape[1]] for i in range(2*n+1) for j in range(2*n+1)]
    return np.logical_and.reduce(shifted) if erode else np.logical_or.reduce(shifted)

def rays(az,el,view,cfg):
    a=np.deg2rad(view*60);o=np.array([cfg['detector_distance_m']*np.cos(a),cfg['detector_distance_m']*np.sin(a),cfg['detector_height_m']])
    az=np.deg2rad(az)[None,:]+a+np.pi;el=np.deg2rad(el)[:,None]
    x=np.cos(el)*np.cos(az);y=np.cos(el)*np.sin(az)
    return o,np.stack([x,y,np.broadcast_to(np.sin(el),x.shape)],axis=-1)

def masks(g,o,d,cfg):
    ed=g['edifice'];con=cone_interval(o,d,ed['base_radius_m'],ed['height_m'],cfg['cone_top_radius_m'])
    L=length(con);aa=[clipped_length(con,anomaly_interval(o,d,a)) for a in g['anomalies']]
    any_an=np.logical_or.reduce([x>0 for x in aa]) if aa else np.zeros_like(L,dtype=bool)
    margin=cfg['rock_sky_margin_pixels'];cone=L>0
    regions={'cielo':morphology(~cone,margin,True),'roca_sin_anomalia':morphology(cone,margin,True)&~morphology(any_an,margin,False), 'borde_cono':morphology(cone,margin,False)&~morphology(cone,margin,True)}
    for i,(a,l) in enumerate(zip(g['anomalies'],aa)):
        regions[f"anomalia_{i}_{a['kind']}"]=morphology(l>=cfg['anomaly_min_length_m'],cfg['core_erosion_pixels'],True)
    return L,aa,regions

def match_controls(mask,control,L,cfg):
    targets=[];donors=[]
    for y,x in zip(*np.where(mask)):
        candidates=np.where(control[y])[0]
        dif=np.abs(L[y,candidates]-L[y,x])/L[y,x]
        ok=candidates[dif<=cfg['control_cone_length_relative_tolerance']]
        order=np.argsort(np.abs(L[y,ok]-L[y,x]),kind='stable')
        ok=ok[order][:cfg['control_donors_per_pixel']]
        if len(ok)==cfg['control_donors_per_pixel']:
            targets.append(y*256+x);donors.append(y*256+ok)
    return np.asarray(targets,dtype=int),np.asarray(donors,dtype=int)

def summary(v):
    if len(v)==0:return {'mean':None,'min':None,'max':None}
    return {'mean':float(np.mean(v)),'min':float(np.min(v)),'max':float(np.max(v))}

def run(a):
    cfg=json.loads(a.protocolo.read_text(encoding='utf-8'));contract=json.loads(a.contrato.read_text(encoding='utf-8'));recipe=json.loads(a.receta.read_text(encoding='utf-8'))
    assert cfg['split']=='val' and cfg['fraction']==.05 and cfg['ray_max_m']==3000
    assert cfg['normalization_scale']==contract['normalization']['scale']
    a.salida.mkdir(parents=True,exist_ok=False)
    report={'schema':cfg['schema'],'protocol_sha256':sha(a.protocolo),'source_code_sha256':sha(__file__),'python':platform.python_version(),'numpy':np.__version__,'heldout_opened':False,'inputs':{},'regions':[],'contrasts':[],'masks':[]}
    report['inputs'].update(data_contract_sha256=sha(a.contrato),recipe_sha256=sha(a.receta))
    pred={k:np.load(a.predicciones/f'{k}-predicciones.npy',mmap_mode='r') for k in ('unet','cgan')}
    for k,p in pred.items():
        assert p.shape==(360,256,256) and np.isfinite(p).all() and np.all((p>=0)&(p<1))
        report['inputs'][k+'-predicciones.npy']=sha(a.predicciones/f'{k}-predicciones.npy')
    for gi in range(3):
        gid=f'geo-val-{gi+1:02d}';gp=a.geometrias/f'{gid}.json'
        assert sha(gp)==recipe['geometry_sha256'][gp.name]
        g=json.loads(gp.read_text(encoding='utf-8'));report['inputs'][gp.name]=sha(gp)
        sp=a.datos/f'dataset-v2/shards/{gid}.npz';mp=sp.with_suffix('.meta.json')
        for p in (sp,mp):
            key=p.relative_to(a.datos).as_posix();assert sha(p)==contract['files'][key];report['inputs'][key]=sha(p)
        meta=json.loads(mp.read_text(encoding='utf-8'));assert meta['geometry_sha256']==sha(gp)
        with np.load(sp) as z:
            assert np.array_equal(z['az_centers_deg'],(z['az_edges_deg'][:-1]+z['az_edges_deg'][1:])/2)
            assert np.allclose(z['el_centers_deg'],np.linspace(2,47,256),rtol=0,atol=1e-12)
            fi=int(np.where(z['fractions']==.05)[0][0])
            for vi in range(6):
                ref=z['ref_counts'][vi].astype(float);o,d=rays(z['az_centers_deg'],z['el_centers_deg'],vi,cfg)
                L,aa,regions=masks(g,o,d,cfg)
                maps={'entrada':z['low_counts'][vi,fi].astype(float)/.05}
                for name in pred:
                    zz=pred[name][gi*120+vi*20:gi*120+(vi+1)*20].astype(float)
                    maps[name]=np.expm1(cfg['normalization_scale']*zz/(1-zz))
                    assert np.isfinite(maps[name]).all()
                np.savez_compressed(a.salida/f'{gid}-view{vi}-mascaras.npz',**regions,cone_length_m=L,**{f'anomaly_{i}_length_m':v for i,v in enumerate(aa)},az_centers_deg=z['az_centers_deg'],el_centers_deg=z['el_centers_deg'])
                report['masks'].append({'geometry':gid,'view':vi,'pixels':{k:int(v.sum()) for k,v in regions.items()},'mask_content_sha256':{k:hashlib.sha256(v.tobytes()).hexdigest() for k,v in regions.items()}})
                for region,mask in regions.items():
                    base=ref[mask].sum()
                    if not mask.any() or base<=0:
                        report['regions'].append({'geometry':gid,'view':vi,'region':region,'status':'empty_or_zero_reference'});continue
                    for name,counts in maps.items():
                        err=counts[:,mask]-ref[mask]
                        report['regions'].append({'geometry':gid,'view':vi,'region':region,'model':name,'pixels':int(mask.sum()),'reference_sum':float(base),'bias_relative':summary(err.sum(1)/base),'mae_relative':summary(np.abs(err).sum(1)/base)})
                for i,an in enumerate(g['anomalies']):
                    key=f"anomalia_{i}_{an['kind']}";mask=regions[key].copy()
                    # Excluir rayos que también atraviesan otra anomalía.
                    for j,l in enumerate(aa):
                        if i!=j:mask&=~morphology(l>0,cfg['rock_sky_margin_pixels'],False)
                    t,donors=match_controls(mask,regions['roca_sin_anomalia'],L,cfg)
                    coverage=len(t)/int(mask.sum()) if mask.any() else 0
                    item={'geometry':gid,'view':vi,'region':key,'candidate_pixels':int(mask.sum()),'matched_pixels':len(t),'match_fraction':coverage,'matched_indices_sha256':hashlib.sha256(t.astype('<i8').tobytes()+donors.astype('<i8').tobytes()).hexdigest(),'status':'not_estimable'}
                    if len(t)>=cfg['min_matched_pixels'] and coverage>=cfg['min_match_fraction']:
                        def contrast(x):
                            x=x.reshape(-1,65536);den=x[:,donors].mean((1,2))
                            return np.divide(x[:,t].mean(1),den,out=np.full(len(x),np.nan),where=den>0)-1
                        cr=float(contrast(ref)[0])
                        if not np.isfinite(cr):
                            item['status']='zero_reference_control';report['contrasts'].append(item);continue
                        item.update(status='estimable',reference_contrast=cr,models={})
                        for name,counts in maps.items():
                            c=contrast(counts)
                            valid=np.isfinite(c);c=c[valid]
                            item['models'][name]={'valid_realizations':int(valid.sum()),'zero_control_realizations':int((~valid).sum()),'contrast':summary(c),'error':summary(c-cr),'absolute_error':summary(np.abs(c-cr)),'same_sign_realizations':int(np.sum(np.sign(c)==np.sign(cr)))}
                    report['contrasts'].append(item)
    (a.salida/'evaluacion-regiones.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'region_rows':len(report['regions']),'contrasts_estimable':sum(x['status']=='estimable' for x in report['contrasts']),'contrasts_total':len(report['contrasts'])}))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('protocolo','contrato','receta','geometrias','datos','predicciones','salida'):p.add_argument('--'+n,type=Path,required=True)
    run(p.parse_args())

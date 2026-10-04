"""Curvas de entradas sin red; análisis descriptivo posterior a EF-01-C2."""
import argparse,json,sys,csv,hashlib
from pathlib import Path
import numpy as np

FRACTIONS=[.01,.05,.1,.5]
INDEX={.5:0,.1:1,.05:2,.01:3}

def crossing(fractions,values,target):
    """Cruce de la tabla discreta; no interpola ni declara equivalencia temporal."""
    if not np.isfinite(values).all() or not np.isfinite(target):
        return {'status':'not_estimable'}
    if any(b<a for a,b in zip(values,values[1:])):
        return {'status':'nonmonotonic_no_bracket'}
    for i,v in enumerate(values):
        if v>=target:
            return {'status':'within_grid' if i else 'below_or_at_grid_minimum',
                    'lower_grid_fraction':fractions[i-1] if i else None,
                    'upper_grid_fraction':fractions[i],
                    'lower_nominal_ratio_to_f05':fractions[i-1]/.05 if i else None,
                    'upper_nominal_ratio_to_f05':fractions[i]/.05}
    return {'status':'above_grid_maximum','lower_grid_fraction':fractions[-1],'upper_grid_fraction':None}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['repo','data','registry','c2-report','out']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    sys.path.insert(0,str(a.repo/'objetivo-2/herramientas'))
    sys.path.insert(0,str(a.repo/'objetivo-2/implementacion/scripts/evaluation'))
    import evaluacion_final_oe2 as e
    import evaluar_regiones_geometricas as g
    from controles_contraste_v2 import Registry
    spec,sig=e.contract(a.repo);registry=e.read(a.registry);c2=e.read(a.c2_report)
    assert e.sha(a.registry)==c2['numerical_correction']['registry_sha256']
    assert c2['protocol_sha256']==sig
    for path,h in spec['data_sha256'].items():assert e.sha(a.data/path)==h,path
    all_images=[];all_regions=[];all_contrasts=[];curves={};raw={}
    original=g.match_controls
    try:
        for fraction in FRACTIONS:
            matcher=Registry(sig,registry);g.match_controls=matcher
            images=[];regions=[];contrasts=[]
            for gid in spec['geometry_order']:
                ref,_,coords=e.package(a.data,gid,spec)
                with np.load(a.data/f'dataset-v2/shards/{gid}.npz',allow_pickle=False) as z:
                    low=z['low_counts'][:,INDEX[fraction]].copy()
                geometry=e.read(a.repo/spec['geometry_files'][gid])
                for view in range(6):
                    # El evaluador original divide por .05. Este adaptador equivale
                    # algebraicamente a low/f, sin generar datos ni cambiar referencias.
                    adapter=low[view].astype(np.float64)*(.05/fraction)
                    assert np.allclose(adapter/.05,low[view].astype(float)/fraction,rtol=1e-15,atol=1e-12)
                    ii,rr,cc=e.analyze_view(ref[view].astype(float),adapter,{},geometry,coords,view,spec['regional_protocol'],spec['normalization_scale'])
                    for items,dest in [(ii,images),(rr,regions),(cc,contrasts)]:
                        dest.extend([{'geometry':gid,'view':view,**x} for x in items])
            assert len(matcher.entries)==54
            raw[str(fraction)]={'images':images,'regions':regions,'contrasts':contrasts}
            all_images.extend([{'fraction':fraction,**x} for x in images]);all_regions.extend([{'fraction':fraction,**x} for x in regions]);all_contrasts.extend([{'fraction':fraction,**x} for x in contrasts])
            print('Fracción',fraction,'480 imágenes',flush=True)
    finally:g.match_controls=original
    key=lambda x:(x['geometry'],x['view'],x['region'])
    common={key(x) for x in c2['contrasts'] if x['status']=='estimable' and all(v['valid_realizations']==20 for v in x['models'].values())}
    for v in raw.values():common&={key(x) for x in v['contrasts'] if x['status']=='estimable' and x['models']['entrada']['valid_realizations']==20}
    common=sorted(common)
    for split,gids in spec['splits'].items():
        curves[split]={}
        for f,v in raw.items():
            cc=[x for x in v['contrasts'] if x['geometry'] in gids and key(x) in common]
            curves[split][f]=e.summarize([x for x in v['images'] if x['geometry'] in gids],[x for x in v['regions'] if x['geometry'] in gids],cc,['entrada'],gids)['entrada']
    # Control positivo: toda la entrada f05 debe coincidir con la evaluación C2.
    for split in curves:
        for metric in ['ssim_macro','psnr_macro','Q_macro']:
            assert abs(curves[split]['0.05'][metric]-c2['summary'][split]['entrada'][metric])<1e-12,(split,metric)
    brackets={}
    for split,models in c2['summary'].items():
        brackets[split]={}
        for model,summary in models.items():
            if model=='entrada':continue
            result={}
            for metric in ['ssim','psnr']:
                result[metric+'_macro']=crossing(FRACTIONS,[curves[split][str(f)][metric+'_macro'] for f in FRACTIONS],summary[metric+'_macro'])
                result[metric+'_by_geometry']={gid:crossing(FRACTIONS,[curves[split][str(f)]['by_geometry'][gid][metric] for f in FRACTIONS],v[metric]) for gid,v in summary['by_geometry'].items()}
            brackets[split][model]=result
    cc_models={split:{model:{'common_contrasts':sum(x['geometry'] in gids and key(x) in common for x in c2['contrasts']),
        'contrast_absolute_error':e.mean([x['models'][model]['absolute_error'] for x in c2['contrasts'] if x['geometry'] in gids and key(x) in common])}
        for model in c2['summary'][split]} for split,gids in spec['splits'].items()}
    result={'analysis':'post-hoc descriptive exposure grid','protocol_sha256':sig,'script_sha256':e.sha(__file__),'registry_sha256':e.sha(a.registry),'c2_report_sha256':e.sha(a.c2_report),'environment':e.env(),'data_sha256':spec['data_sha256'],'fractions':FRACTIONS,'curves':curves,'model_comparisons_on_common_contrast_support':cc_models,'common_contrast_keys':common,'grid_crossings':brackets,'validation':{'f05_matches_c2':True,'image_records':len(all_images),'region_records':len(all_regions),'contrast_records':len(all_contrasts)},'no_interpolation':True,'no_training':True,'no_new_simulation':True,'effective_time_reduction_demonstrated':False,'limitations':['Known synthetic catalog; historical exposure; descriptive only','Repeated realizations are not independent geometries','Finite noisy high-count reference; low counts derived from that reference','Crossings depend on metric and sampled grid; not a physical equivalence margin','f05 models only; no inference at other fractions']}
    e.write(a.out/'curvas.json',result)
    for name,rows in [('imagenes',all_images),('regiones',all_regions)]:
        keys=sorted(set().union(*(x.keys() for x in rows)))
        with (a.out/(name+'.csv')).open('w',newline='',encoding='utf-8') as file:
            writer=csv.DictWriter(file,fieldnames=keys);writer.writeheader();writer.writerows(rows)
    e.write(a.out/'contrastes.json',all_contrasts)
    e.write(a.out/'inventario.json',[{'path':x.name,'sha256':e.sha(x),'bytes':x.stat().st_size} for x in sorted(a.out.iterdir()) if x.is_file()])
    print(json.dumps(result['validation']))

if __name__=='__main__':main()

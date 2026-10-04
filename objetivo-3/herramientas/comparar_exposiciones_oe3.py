"""Desglose descriptivo OE3. Reutiliza métricas verificadas; no ejecuta modelos."""
import argparse,csv,hashlib,json,math,statistics,sys
from pathlib import Path
TOL=1e-12  # Tolerancia de aritmética; no margen científico de equivalencia.
FRACTIONS=(.01,.05,.1,.5)
MODELS=('unet_original','cgan_original','B1_C0','B1_C1','B2_C0','B2_C1','B3_C0','B3_C1')
def mean(xs):
    xs=list(xs)
    if not xs or not all(math.isfinite(x) for x in xs):raise ValueError('media sin soporte finito')
    return statistics.mean(xs)
def unique(rows,key):
    out={}
    for r in rows:
        k=key(r)
        if k in out:raise ValueError('clave duplicada: '+str(k))
        out[k]=r
    return out
def relation(a,b,higher=True):
    if not math.isfinite(a) or not math.isfinite(b):raise ValueError('comparación no finita')
    d=(a-b)*(1 if higher else -1)
    return 'better' if d>TOL else ('worse' if d<-TOL else 'numerical_tie')
def image_key(r):return (r['geometry'],int(r['view']),int(r['realization']))
def region_key(r):return (r['geometry'],int(r['view']),r['region'])
def read_csv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def read_json(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_csv(p,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['c2','curvas','salida']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();a.salida.mkdir(parents=True,exist_ok=False)
    inputs={'c2_report':a.c2/'evaluacion-final.json','c2_images':a.c2/'imagenes.csv','c2_regions':a.c2/'regiones.csv','curves':a.curvas/'curvas.json','raw_images':a.curvas/'imagenes.csv','raw_regions':a.curvas/'regiones.csv','raw_contrasts':a.curvas/'contrastes.json'}
    c=read_json(inputs['c2_report']);e=read_json(inputs['curves'])
    assert c['protocol_sha256']==e['protocol_sha256']
    assert c['numerical_correction']['registry_sha256']==e['registry_sha256']
    ci=read_csv(inputs['c2_images']);cr=read_csv(inputs['c2_regions']);ri=read_csv(inputs['raw_images']);rr=read_csv(inputs['raw_regions']);rc=read_json(inputs['raw_contrasts'])
    assert (len(ci),len(cr),len(ri),len(rr),len(rc))==(4320,1134,1920,504,216)
    images={m:unique([r for r in ci if r['model']==m],image_key) for m in ('entrada',)+MODELS}
    raw_images={f:unique([r for r in ri if float(r['fraction'])==f],image_key) for f in FRACTIONS}
    regions={m:unique([r for r in cr if r['model']==m],region_key) for m in ('entrada',)+MODELS}
    raw_regions={f:unique([r for r in rr if float(r['fraction'])==f],region_key) for f in FRACTIONS}
    expected=set(images['entrada']);assert len(expected)==480
    for d in [*images.values(),*raw_images.values()]:assert set(d)==expected
    rkeys=set(regions['entrada']);assert len(rkeys)==126
    for d in [*regions.values(),*raw_regions.values()]:assert set(d)==rkeys
    for k in expected:
        for metric in ['ssim','psnr']:assert abs(float(images['entrada'][k][metric])-float(raw_images[.05][k][metric]))<=TOL
    for k in rkeys:
        for metric in ['bias_mean','bias_mean_absolute','spatial_mae']:assert abs(float(regions['entrada'][k][metric])-float(raw_regions[.05][k][metric]))<=TOL
        for d in [*regions.values(),*raw_regions.values()]:
            assert d[k]['status']=='ok'
            for field in ['family','pixels','reference_sum']:assert d[k][field]==regions['entrada'][k][field]
    views=sorted({k[:2] for k in expected});assert len(views)==24
    contrast=unique(c['contrasts'],region_key)
    raw_contrast={f:unique([r for r in rc if r['fraction']==f],region_key) for f in FRACTIONS}
    common=set(tuple(k) for k in e['common_contrast_keys'])
    calculated={k for k,x in contrast.items() if x['status']=='estimable' and all(v['valid_realizations']==20 for v in x['models'].values())}
    for d in raw_contrast.values():calculated&={k for k,x in d.items() if x['status']=='estimable' and x['models']['entrada']['valid_realizations']==20}
    assert common==calculated and len(common)==32
    def vm(d,rd,g,v):
        keys=[k for k in expected if k[:2]==(g,v)];assert len(keys)==20
        rows=[rd[k] for k in rkeys if k[:2]==(g,v)]
        byfam={f:[r for r in rows if int(r['family'])==f] for f in range(4)}
        assert all(byfam.values())
        out={met:mean(float(d[k][met]) for k in keys) for met in ['ssim','psnr']}
        out['Q']=.5*(mean(abs(float(r['bias_mean'])) for r in byfam[1])+mean(abs(float(r['bias_mean'])) for r in byfam[3]))
        for f,name in enumerate(['sky','rock','edge','anomalies']):out['spatial_'+name]=mean(float(r['spatial_mae']) for r in byfam[f])
        return out
    # Validación independiente del resumen: recuperar los valores publicados
    # desde los CSV por imagen y región antes de construir comparaciones nuevas.
    aggregation_checks=0
    for split,models in c['summary'].items():
        gids=list(models['entrada']['by_geometry'])
        for m in ('entrada',)+MODELS:
            vals=[vm(images[m],regions[m],g,v) for g,v in views if g in gids]
            for metric,key in [('ssim','ssim_macro'),('psnr','psnr_macro'),('Q','Q_macro')]:
                assert abs(mean(x[metric] for x in vals)-models[m][key])<TOL
                aggregation_checks+=1
        for f in FRACTIONS:
            vals=[vm(raw_images[f],raw_regions[f],g,v) for g,v in views if g in gids]
            for metric,key in [('ssim','ssim_macro'),('psnr','psnr_macro'),('Q','Q_macro')]:
                assert abs(mean(x[metric] for x in vals)-e['curves'][split][str(f)][key])<TOL
                aggregation_checks+=1
    viewrows=[];regionrows=[];contrastrows=[]
    for f in FRACTIONS:
      for m in MODELS:
        for g,v in views:
            x=vm(images[m],regions[m],g,v);y=vm(raw_images[f],raw_regions[f],g,v)
            row={'fraction_raw':f,'nominal_ratio':f/.05,'model':m,'geometry':g,'view':v,'split':'generalization' if g.startswith('geo-gen') else 'test'}
            for met in x:row.update({met+'_model':x[met],met+'_raw':y[met],met+'_delta':x[met]-y[met],met+'_relation':relation(x[met],y[met],met in ['ssim','psnr'])})
            row['both_image_metrics_no_worse']=all(row[k+'_relation']!='worse' for k in ['ssim','psnr'])
            row['Q_and_all_spatial_no_worse']=all(row[k+'_relation']!='worse' for k in ['Q','spatial_sky','spatial_rock','spatial_edge','spatial_anomalies'])
            row['realizations_both_image_no_worse']=sum(all(relation(float(images[m][k][met]),float(raw_images[f][k][met]))!='worse' for met in ['ssim','psnr']) for k in expected if k[:2]==(g,v))
            ck=sorted(k for k in common if k[:2]==(g,v));row['common_contrasts']=len(ck)
            if ck:
                ca=mean(contrast[k]['models'][m]['absolute_error'] for k in ck);cb=mean(raw_contrast[f][k]['models']['entrada']['absolute_error'] for k in ck)
                row.update(contrast_model=ca,contrast_raw=cb,contrast_delta=ca-cb,contrast_relation=relation(ca,cb,False))
            else:row.update(contrast_model=None,contrast_raw=None,contrast_delta=None,contrast_relation='not_estimable')
            row['all_listed_no_worse']=row['both_image_metrics_no_worse'] and row['Q_and_all_spatial_no_worse'] and row['contrast_relation'] in ['better','numerical_tie']
            viewrows.append(row)
        for k in sorted(rkeys):
            x=regions[m][k];y=raw_regions[f][k]
            row={'fraction_raw':f,'model':m,'geometry':k[0],'view':k[1],'region':k[2],'family':x['family'],'pixels':x['pixels'],'reference_sum':x['reference_sum']}
            for met in ['bias_mean','bias_mean_absolute','spatial_mae']:
                u=float(x[met]);v=float(y[met]);row.update({met+'_model':u,met+'_raw':v,met+'_delta':u-v,met+'_relation':relation(abs(u),abs(v),False) if met=='bias_mean' else relation(u,v,False)})
            regionrows.append(row)
        for k in sorted(common):
            x=contrast[k]['models'][m];y=raw_contrast[f][k]['models']['entrada'];assert abs(contrast[k]['reference_contrast']-raw_contrast[f][k]['reference_contrast'])<TOL
            contrastrows.append({'fraction_raw':f,'model':m,'geometry':k[0],'view':k[1],'region':k[2],'reference_contrast':contrast[k]['reference_contrast'],'error_model':x['absolute_error'],'error_raw':y['absolute_error'],'error_relation':relation(x['absolute_error'],y['absolute_error'],False),'sign_inversions_model':x['sign_inversions'],'sign_inversions_raw':y['sign_inversions'],'realizations':20})
    summary=[]
    for f in FRACTIONS:
      for m in MODELS:
       for split in ['test','generalization']:
        rows=[r for r in viewrows if r['fraction_raw']==f and r['model']==m and r['split']==split]
        summary.append({'fraction_raw':f,'nominal_ratio':f/.05,'model':m,'split':split,'views':len(rows),'both_image_no_worse':sum(r['both_image_metrics_no_worse'] for r in rows),'realizations_both_no_worse':sum(r['realizations_both_image_no_worse'] for r in rows),'Q_no_worse':sum(r['Q_relation']!='worse' for r in rows),'regional_spatial_no_worse':sum(r['Q_and_all_spatial_no_worse'] for r in rows),'contrast_no_worse':sum(r['contrast_relation'] in ['better','numerical_tie'] for r in rows),'contrast_estimable_views':sum(r['common_contrasts']>0 for r in rows),'all_listed_no_worse':sum(r['all_listed_no_worse'] for r in rows),'min_ssim_delta':min(r['ssim_delta'] for r in rows),'min_psnr_delta':min(r['psnr_delta'] for r in rows)})
    excluded=[{'geometry':k[0],'view':k[1],'region':k[2],'c2_status':x['status'],'reason':'outside common complete support across all fractions and models'} for k,x in contrast.items() if k not in common]
    result={'analysis':'post-hoc descriptive comparisons; no equivalence test','models':list(MODELS),'fractions':FRACTIONS,'numerical_tolerance':TOL,'summary':summary,'common_contrast_keys':sorted(common),'excluded_contrasts':excluded,'validation':{'f05_control':True,'aggregation_checks':aggregation_checks,'unique_complete_image_support':480,'unique_complete_region_support':126,'view_rows':len(viewrows),'region_rows':len(regionrows),'contrast_rows':len(contrastrows),'common_contrast_support':32},'sources':{k:{'file':str(v.name),'sha256':sha(v)} for k,v in inputs.items()},'script_sha256':sha(Path(__file__)),'python':sys.version,'effective_time_reduction_demonstrated':False,'no_new_training':True,'no_new_inference':True,'no_interpolation':True}
    for name,rows in [('vistas',viewrows),('regiones',regionrows),('contrastes',contrastrows),('resumen',summary)]:write_csv(a.salida/(name+'.csv'),rows)
    (a.salida/'resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['validation']))
    for x in summary:
        if x['model']=='cgan_original' and x['fraction_raw'] in [.1,.5]:print(json.dumps(x))
if __name__=='__main__':main()

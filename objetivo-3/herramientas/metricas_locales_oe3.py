"""Convenciones descriptivas del complemento OE3; no reconstruye opacidad."""
import numpy as np

def divide_or_none(a,b):
    return float(a/b) if np.isfinite(a) and np.isfinite(b) and b>0 else None

def local_metrics(counts,targets,donors):
    """Una imagen; soporte C2 fijo. Donantes únicos para estimar dispersión."""
    c=np.asarray(counts,dtype=np.float64).ravel()
    t=np.asarray(targets,dtype=np.int64);d=np.asarray(donors,dtype=np.int64)
    if t.ndim!=1 or d.ndim!=2 or d.shape[0]!=len(t) or d.shape[1]!=5:
        raise ValueError('Índices incompatibles')
    if len(t)<20:return {'status':'insufficient_support'}
    if np.any(t<0) or np.any(d<0) or np.any(t>=len(c)) or np.any(d>=len(c)):
        raise ValueError('Índices fuera de imagen')
    u=np.unique(d)
    if len(u)<2:return {'status':'insufficient_background'}
    if not np.isfinite(c).all() or np.any(c<0):raise ValueError('Cuentas inválidas')
    a=c[t];b=c[d].mean(axis=1);background=c[u]
    mu_a=float(a.mean());mu_b=float(b.mean());sigma_a=float(a.std(ddof=1));sigma_b=float(background.std(ddof=1))
    contrast=divide_or_none(mu_a,mu_b)
    if contrast is not None:contrast-=1
    return {'status':'ok','target_pixels':len(t),'unique_background_pixels':len(u),
        'mean_anomaly':mu_a,'mean_control_matched':mu_b,'sigma_anomaly_spatial':sigma_a,
        'sigma_background_unique':sigma_b,'snr_local_intensity':divide_or_none(mu_a,sigma_a),
        'cnr_local_signed':divide_or_none(mu_a-mu_b,sigma_b),'contrast_counts':contrast,
        'snr_status':'ok' if sigma_a>0 else 'zero_spatial_variance',
        'cnr_status':'ok' if sigma_b>0 else 'zero_background_variance',
        'contrast_status':'ok' if mu_b>0 else 'zero_control'}

def repeated_contrast_signal(rows):
    """Variabilidad entre realizaciones de diferencia de medias, sin sqrt(K)."""
    if len(rows)<2 or any(r.get('status')!='ok' for r in rows):return {'status':'insufficient_support'}
    delta=np.array([r['mean_anomaly']-r['mean_control_matched'] for r in rows])
    sd=float(delta.std(ddof=1))
    return {'status':'ok' if sd>0 else 'zero_between_realization_variance','mean_difference':float(delta.mean()),
        'sd_between_realizations':sd,'snr_contrast_repeated_signed':divide_or_none(float(delta.mean()),sd),'realizations':len(rows)}

def assessed_fraction(rows,thresholds,fractions,models,geometries,tolerance=1e-12):
    """Mínimo de rejilla con ambas métricas en cada vista. No interpola."""
    result={}
    for model in models:
        tested=[]
        for f in fractions:
            checks=[]
            for g in geometries:
                for view in range(6):
                    rr=[r for r in rows if r['model']==model and r['fraction']==f and r['geometry']==g and r['view']==view]
                    if len(rr)!=20:raise ValueError('Vista incompleta para umbral')
                    for metric in ['ssim','psnr']:
                        vals=[r[metric] for r in rr]
                        if any(v is None or not np.isfinite(v) for v in vals):raise ValueError('Métrica no finita para umbral')
                        checks.append(float(np.mean(vals))+tolerance>=thresholds[g][str(view)][metric])
            tested.append({'fraction':f,'passes_image_benchmark_all_views':bool(all(checks))})
        good=[r['fraction'] for r in tested if r['passes_image_benchmark_all_views']]
        minimum=min(good) if good else None
        result[model]={'tested':tested,'minimum_sampled_fraction':minimum,
            'nominal_ratio_reference_fraction_to_input':.5/minimum if minimum is not None else None,
            'physical_equivalence':False,'maximum_continuous_factor':None}
    return result

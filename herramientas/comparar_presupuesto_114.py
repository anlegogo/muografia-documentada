"""Sensibilidad 211/344 M desde el piloto; no predice otras geometrías."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.stats import beta, binom
from preparar_imagen_angular_v1 import read_image
from evaluar_bordes_angular import evaluate
from evaluar_piloto_angular import review

ROOT=Path(__file__).resolve().parents[1]

def analyze(fusion):
    base=ROOT/'objetivo-1/evidencias/piloto-propuesto-siete-actividades'
    design_path=base/'diseno-piloto.json';design=json.loads(design_path.read_text(encoding='utf-8'))
    ref_path=ROOT/'objetivo-1/evidencias/preparacion-siete-actividades/cielo-ideal-margen-5.json'
    ref=json.loads(ref_path.read_text(encoding='utf-8'))
    # Verificar hashes de máscaras, receta, N y semillas antes del análisis.
    review(fusion,design_path,ref_path)
    masks=[np.load(base/v['rock_roi_mask'],allow_pickle=False) for v in design['views']]
    tests=sum(int(m.sum()) for m in masks);results=[];N=design['events_per_view']
    for v,mask in zip(design['views'],masks):
        hist=fusion/design['geometry']/f"{design['geometry']}_view{v['view']}_hist.csv"
        _,counts,_,_,hashes=read_image(hist)
        k=counts.reshape(64,4,64,4).sum(axis=(1,3))[mask];rate=k/N
        lower=np.where(k==0,0,beta.ppf(.05/(2*tests),k,N-k+1))
        upper=np.where(k==N,1,beta.ppf(1-.05/(2*tests),k+1,N-k))
        alternatives=[]
        for n in (211000000,344000000):
            alternatives.append({'N':n,'scaled_fraction_ge100':float(np.mean(k*n/N>=100)),
                'future_fraction_mean_plugin':float(binom.sf(99,n,rate).mean()),
                'future_fraction_mean_simultaneous_rate_bounds':[float(binom.sf(99,n,lower).mean()),float(binom.sf(99,n,upper).mean())]})
        border=evaluate(counts,N,np.load(base/v['sky_mask'],allow_pickle=False),ref,alpha=.05/114)
        results.append({'view':v['view'],'source_hashes':hashes,'alternatives':alternatives,
            'retrospective_border_114_equivalent_regions':sum(r['decision']=='equivalent' for r in border['regions'])})
    return {'views':results,'family_roi_count':tests,'limits':[
        'Plug-in means treat estimated rates as fixed; CP envelope propagates simultaneous marginal rate bounds at family alpha 0.05.',
        'These bound expected fraction, not future realized fraction, and do not guarantee 90 percent.',
        'Alpha114 recalculation is retrospective sensitivity, not a change to pilot acceptance.'],
        'physical_validation':False,'production_authorized':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fusion',required=True,type=Path);p.add_argument('--salida',required=True,type=Path)
    a=p.parse_args();result=analyze(a.fusion)
    with a.salida.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)

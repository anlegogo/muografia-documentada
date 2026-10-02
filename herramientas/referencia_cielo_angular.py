"""Referencia ideal sin transporte, integrada sobre el muestreador angular v3.

No es una simulación de cielo abierto ni una calibración instrumental.
Probabilidades por primario generado, con jitter, margen y cuantiles tabulados.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from auditar_fuente_angular import MASS, above_quantile, extended_rows


def reference(tables, margin=5., cut=3.):
    tables = Path(tables)
    if not math.isfinite(cut) or cut < 0:
        raise ValueError('corte inválido')
    el, weights = np.loadtxt(tables/'row_weights_30d.txt', unpack=True)
    centers, weights_ext, _ = extended_rows(el, weights, margin)
    lines = (tables/'p_cdf.txt').read_text().splitlines()
    bands = np.array([float(v) for v in next(x for x in lines if x.startswith('# band_edges_deg:')).split(':')[1].split()])
    quantiles = np.array([[float(v) for v in x.split()] for x in lines if x.strip() and not x.startswith('#')])
    if len(bands) != len(quantiles)+1 or np.any(np.diff(bands) <= 0):
        raise ValueError('bandas inválidas')
    q = np.array([above_quantile(row, math.sqrt(cut*(cut+2*MASS))) for row in quantiles])
    step = float(el[1]-el[0])
    nominal_edges = np.linspace(2-45/510, 47+45/510, 257)
    nominal = np.zeros(256); selected = np.zeros(256)
    for center, weight in zip(centers, weights_ext):
        lo, hi = center-step/2, center+step/2
        for i in range(256):
            a, b = max(lo, nominal_edges[i]), min(hi, nominal_edges[i+1])
            if b <= a: continue
            nominal[i] += weight*(b-a)/step
            cuts = [a]+[float(t) for t in bands if a < t < b]+[b]
            for left, right in zip(cuts[:-1], cuts[1:]):
                band = int(np.clip(np.searchsorted(bands,(left+right)/2,side='right')-1,0,len(q)-1))
                selected[i] += weight*(right-left)/step*q[band]
    az_bin_probability = (60/256)/(60+2*margin)
    nominal *= az_bin_probability/weights_ext.sum()
    selected *= az_bin_probability/weights_ext.sum()
    return {'schema':'oe1-ideal-sky-v1', 'physical_validation':False,
            'margin_deg':margin,'kinetic_cut_gev':cut,
            'nominal_probability_per_pixel_by_row':nominal.tolist(),
            'ideal_selected_probability_per_pixel_by_row':selected.tolist(),
            'ideal_selected_given_nominal_by_row':(selected/nominal).tolist(),
            'nominal_window_probability':float(256*nominal.sum()),
            'ideal_selected_window_probability':float(256*selected.sum()),
            'elevation_centers_deg':np.linspace(2,47,256).tolist(),
            'table_sha256':{n:hashlib.sha256((tables/n).read_bytes()).hexdigest() for n in ('meta.json','row_weights_30d.txt','p_cdf.txt')},
            'limits':['No rock, air energy loss, decay, scattering or angular migration.',
                      'Reference for the implemented hybrid source, not a measured physical sky.',
                      'C/(N_generated*p_ideal) is a normalized synthetic response; it need not be <=1.']}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('tablas',type=Path);p.add_argument('--margen',type=float,default=5.)
    p.add_argument('--corte',type=float,default=3.);p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args();r=reference(a.tablas,a.margen,a.corte)
    with a.salida.open('x',encoding='utf-8') as f: json.dump(r,f,indent=2,allow_nan=False)

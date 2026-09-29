"""Comparación descriptiva del piloto OE1; sin umbral automático de aprobación."""
import argparse, json
from pathlib import Path
import numpy as np

def compare(root):
    rows=[]
    for seed in (2026092801,2026092802,2026092803):
        runs=[]
        for variant in ('original','corregida'):
            folder=root/variant/str(seed)
            meta=json.loads((folder/'geo-train-06_view0.meta.json').read_text())
            hist=np.loadtxt(folder/'geo-train-06_view0_hist.csv',delimiter=',')
            if hist.shape!=(256,256) or not np.isfinite(hist).all() or (hist<0).any() or (hist!=np.floor(hist)).any():
                raise ValueError(f'Histograma inválido: {folder}')
            if meta['seed']!=seed or meta['view_index']!=0 or meta['geometry_id']!='geo-train-06':
                raise ValueError(f'Identidad inesperada: {folder}')
            n=meta['events_transported']; detected=meta['detected_in_bins']
            if n!=1000000 or hist.sum()!=detected or not 0<=detected<=n:
                raise ValueError(f'Presupuesto o conteos inconsistentes: {folder}')
            runs.append((hist,meta))
        a,ma=runs[0]; b,mb=runs[1]
        for key in ('threads','grid','detector','sampling','physics_note','engine'):
            if ma[key]!=mb[key]: raise ValueError(f'Variante cambia {key}; documentar y revisar antes de comparar.')
        n=ma['events_transported']; ea=float(a.sum()/n); eb=float(b.sum()/n)
        rows.append({'semilla':seed,'eficiencia_original':ea,'eficiencia_corregida':eb,'delta_eficiencia':eb-ea,
                     'cambio_relativo_global':(eb-ea)/ea if ea else None,
                     'diferencia_absoluta_media_pixel_por_evento':float(np.abs(b-a).mean()/n),
                     'nota_espacial':'Incluye fluctuaciones Monte Carlo; no es por sí sola cambio físico.'})
    d=np.array([r['delta_eficiencia'] for r in rows])
    return {'corridas_pareadas':rows,'media_delta_eficiencia':float(d.mean()),'desviacion_entre_replicas':float(d.std(ddof=1)),
            'error_estandar_media_delta':float(d.std(ddof=1)/np.sqrt(len(d))),
            'limites':'Tres pares son piloto. Semilla compartida no asegura trayectorias idénticas. Sin criterio automático de equivalencia; revisar mapas, geometría e incertidumbre local.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('carpeta',type=Path); p.add_argument('--out',type=Path,required=True); args=p.parse_args()
    result=compare(args.carpeta)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2); f.write('\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

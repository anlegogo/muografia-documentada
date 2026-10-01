"""Plan fijo OE1 etapa 2 v1.1 y cálculo conservador del intervalo pareado.

No ejecuta Geant4. Requiere scipy. --out crea una carpeta NUEVA con el plan.
--counts n00 n01 n10 n11 calcula un diagnóstico; no verifica contratos de datos.
"""
import argparse
import csv
import json
import math
from pathlib import Path
from scipy.stats import beta

MARGIN = math.sqrt(98) / 36174382
TARGET_N = 24000000


def cp(k, n, alpha=.025):
    if not isinstance(n, int) or n <= 0 or not isinstance(k, int) or not 0 <= k <= n:
        raise ValueError('Se requieren enteros 0 <= k <= n y n > 0')
    return (0.0 if k == 0 else float(beta.ppf(alpha/2, k, n-k+1)),
            1.0 if k == n else float(beta.ppf(1-alpha/2, k+1, n-k)))


def interval(counts):
    if len(counts) != 4 or any(type(k) is not int or k < 0 for k in counts):
        raise ValueError('Se requieren cuatro conteos enteros no negativos')
    n00, n01, n10, n11 = counts
    n = sum(counts)
    lo01, hi01 = cp(n01, n)
    lo10, hi10 = cp(n10, n)
    low, high = lo01-hi10, hi01-lo10
    decision = ('dentro_del_margen' if low > -MARGIN and high < MARGIN else
                'diferencia_relevante' if low > MARGIN or high < -MARGIN else 'inconcluso')
    return {'N': n, 'counts_00_01_10_11': list(counts), 'delta_per_million': (n01-n10)/n*1e6,
            'interval95_conservative_per_million': [low*1e6, high*1e6],
            'margin_per_million': MARGIN*1e6, 'decision_numerica': decision,
            'N_principal_completo': n == TARGET_N,
            'advertencia': 'La decisión numérica no valida primarios, fuente, independencia, contratos ni integridad. No autoriza inferencia sobre toda la imagen o el catálogo.'}


def manifest():
    rows = []
    for case, count, events, base, repbase in [('geo-train-06', 24, 1000000, 2026100100, 100), ('geo-train-01', 3, 100000, 2026100200, 200)]:
        for i in range(1, count+1):
            for variant in ('A', 'B'):
                rows.append(dict(run_id=f'{case}-r{repbase+i}-{variant}', geometry_id=case,
                                 case_code=int(case[-2:]), view=0, replica=repbase+i, n=events,
                                 source_seed=base+i, transport_seed=base+i-1000000000,
                                 variant=variant, repeat_of=''))
    repeat = next(r.copy() for r in rows if r['run_id']=='geo-train-01-r201-A')
    repeat.update(run_id='geo-train-01-r201-AA', repeat_of='geo-train-01-r201-A')
    rows.append(repeat)
    return rows


def write_plan(out):
    out.mkdir(parents=True, exist_ok=False)
    rows = manifest()
    with (out/'corridas.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    ntransport = sum(r['n'] for r in rows)
    nlists = sum(r['n'] for r in rows if r['variant']=='B')
    plan = {'version': '1.1', 'fecha_diseno': '2026-10-01', 'N_principal': TARGET_N,
            'corridas': len(rows), 'transportes': ntransport, 'primarios_distintos': nlists,
            'margen': MARGIN, 'alpha_familia_principal': .05, 'alpha_por_proporcion': .025,
            'min_N_cero_discordancias': math.floor(math.log(.0125)/math.log1p(-MARGIN))+1,
            'escenarios_sinteticos_no_resultados': [interval([TARGET_N-a-b, a, b, 0]) for a,b in [(0,0),(1,0),(0,1),(1,1),(2,0),(5,0),(20,0)]],
            'recursos_estimados_no_medidos_etapa2': {
                'cpu_horas_media': ntransport*84.6/100000/3600,
                'cpu_horas_rango': [ntransport*v/100000/3600 for v in (58.5,91.3)],
                'registros_GB_decimal': ntransport*326.87/1e9,
                'registros_gzip_GB_decimal': ntransport*101.7/1e9,
                'listas_GB_decimal': nlists*145.6/1e9,
                'reserva_minima_GiB': 30},
            'restricciones': ['No ampliar N tras ver resultados', 'No combinar desarrollo con confirmación', 'A/A y control no aumentan N principal', 'Verificar almacenamiento y contratos antes de lanzar']}
    (out/'dimensionamiento.json').write_text(json.dumps(plan, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'corridas':len(rows), 'transportes':ntransport, 'margen_por_millon':MARGIN*1e6}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--counts', nargs=4, type=int, metavar=('N00','N01','N10','N11'))
    args = parser.parse_args()
    if (args.out is None) == (args.counts is None):
        parser.error('Usar exactamente uno de --out o --counts')
    if args.out is not None:
        write_plan(args.out)
    else:
        print(json.dumps(interval(args.counts), indent=2, ensure_ascii=False))

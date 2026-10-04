"""Tabula las 54 comparaciones por vista y las 72 filas de anomalías de E1 (B1-B3) sin recalcular métricas.

Uso: python tabular_vistas_anomalias.py --vistas objetivo-2/evidencias/vistas-e1.json
       --entrega <entrega 804ce85>/objetivo-2/entregas/2026-10-04-borde-cgan-f05 --salida <carpeta>
Lee vistas-e1.json (revisión de la dirección) y anomalias-cgan.json de cada pareja (entrega 804ce85).
"""
import argparse, csv, json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
for n in ['vistas', 'entrega', 'salida']:
    p.add_argument('--' + n, type=Path, required=True)
a = p.parse_args()
a.salida.mkdir(parents=True, exist_ok=True)
vistas = json.loads(a.vistas.read_text(encoding='utf-8'))['views']
assert len(vistas) == 54
with (a.salida / 'vistas-e1.csv').open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['pareja', 'geometria', 'vista', 'Q_C0_pct', 'Q_C1_pct', 'delta_Q_pp', 'borde_C0_pct', 'borde_C1_pct', 'delta_borde_pp'])
    for v in sorted(vistas, key=lambda x: (x['pair'], x['geometry'], x['view'])):
        w.writerow([v['pair'], v['geometry'], v['view'], 100 * v['C0_Q'], 100 * v['C1_Q'], v['delta_Q_pp'],
                    100 * v['C0_edge'], 100 * v['C1_edge'], v['delta_edge_pp']])
filas = []
for par in ['B1', 'B2', 'B3']:
    an = json.loads((a.entrega / 'datos/ensayo-borde-e1' / par / 'evaluacion/anomalias-cgan.json').read_text(encoding='utf-8'))
    rows = an['rows'] if isinstance(an, dict) and 'rows' in an else an
    assert len(rows) == 24
    for r in rows:
        m = r['models']
        filas.append([par, r['geometry'], r['view'], r['region'], r['pixels'], r['reference_sum'],
                      100 * m['inicial_cgan']['signed_bias'], 100 * m['C0']['signed_bias'], 100 * m['C1']['signed_bias'],
                      int(abs(m['C1']['signed_bias']) > abs(m['C0']['signed_bias'])),
                      int(abs(m['C1']['signed_bias']) > abs(m['inicial_cgan']['signed_bias']))])
with (a.salida / 'anomalias-e1.csv').open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['pareja', 'geometria', 'vista', 'region', 'pixeles', 'cuentas_referencia', 'sesgo_inicial_pct', 'sesgo_C0_pct',
                'sesgo_C1_pct', 'C1_mayor_magnitud_que_C0', 'C1_mayor_magnitud_que_inicial'])
    w.writerows(filas)
print(json.dumps({'vistas': len(vistas), 'anomalias': len(filas),
                  'peor_que_C0': {p: sum(f[9] for f in filas if f[0] == p) for p in ['B1', 'B2', 'B3']},
                  'peor_que_inicial': {p: sum(f[10] for f in filas if f[0] == p) for p in ['B1', 'B2', 'B3']}}))

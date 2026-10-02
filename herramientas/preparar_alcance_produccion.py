"""Inventario de decisión, sin lanzar simulaciones ni modificar originales.

Uso: python herramientas/preparar_alcance_produccion.py --salida DIRECTORIO
Solo biblioteca estándar. Requiere restaurar los NPZ originales.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AFECTADAS = {'geo-gen-01', 'geo-test-01', 'geo-test-03',
             'geo-train-06', 'geo-train-08', 'geo-train-11'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    original = ROOT / 'objetivo-1/originales'
    catalog = original / 'scripts/simulation/geometry_catalog/geometries'
    rows = []
    for geometry in sorted(catalog.glob('*.json')):
        gid = geometry.stem
        for view in range(6):
            base = original / 'data/campaign-geant4' / gid / f'{gid}_view{view}'
            meta_path = base.with_suffix('.meta.json')
            npz = base.with_suffix('.npz')
            meta = json.loads(meta_path.read_text(encoding='utf-8'))
            digest = sha(npz)
            if (meta['geometry_id'] != gid or meta['view_index'] != view
                    or digest != meta['npz_sha256']):
                raise ValueError(f'Identidad o huella discrepante: {base}')
            rows.append(dict(geometria=gid, vista=view,
                decision_provisional=('regeneracion_candidata' if gid in AFECTADAS
                                      else 'reutilizacion_condicionada'),
                pares_derivados=80, primarios_historicos=meta['events_transported'],
                detectados_historicos=meta['detected_in_bins'],
                geometria_sha256=sha(geometry), npz_sha256=digest,
                meta_sha256=sha(meta_path)))
    if len(rows) != 114 or len({r['geometria'] for r in rows}) != 19:
        raise ValueError('El catálogo no corresponde a las 19 geometrías esperadas')
    selected = [r for r in rows if r['geometria'] in AFECTADAS]
    if len(selected) != 36:
        raise ValueError('No se encontraron las seis geometrías afectadas')
    tables = original / 'scripts/simulation/geant4_app/tables'
    weights = [list(map(float, line.split())) for line in
               (tables / 'row_weights_30d.txt').read_text().splitlines()
               if line.strip() and not line.startswith('#')]
    meta = json.loads((tables / 'meta.json').read_text())
    total = sum(w for _, w in weights)
    declared = meta['total_open_sky_counts_30days_per_view']
    if len(weights) != 256 or not all(w > 0 for _, w in weights):
        raise ValueError('Pesos inválidos')
    if abs(total / declared - 1) > 1e-6:
        raise ValueError('Total tabulado inconsistente con metadatos')
    summary = dict(estado='plan_condicionado_no_orden_de_ejecucion',
        vistas=114, npz_verificados=114, pares=9120,
        vistas_regeneracion_candidata=36, pares_regeneracion_candidata=2880,
        vistas_reutilizacion_condicionada=78, pares_reutilizacion_condicionada=6240,
        primarios_historicos_36=sum(r['primarios_historicos'] for r in selected),
        normalizacion=dict(total_tabla_30d=total, total_meta_30d=declared,
            diferencia_relativa=total/declared-1,
            alcance='consistencia numerica; no valida exposicion fisica',
            sha256={name: sha(tables/name) for name in
                    ['row_weights_30d.txt', 'p_cdf.txt', 'meta.json']}))
    args.salida.mkdir(parents=True, exist_ok=True)
    with (args.salida/'alcance-produccion.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (args.salida/'preparacion-produccion.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

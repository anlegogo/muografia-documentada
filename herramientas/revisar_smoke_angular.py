"""Revisa la entrega angular de 1000 primarios; no valida física ni procedencia del binario.

python herramientas/revisar_smoke_angular.py ENTREGA --salida informe.json
ENTREGA: geo-train-01_view0.meta.json, geo-train-01_view0_hist.csv,
run.log y exit_code.txt (código real del proceso, capturado al terminar).
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re


def review(directory):
    directory = Path(directory)
    checks, hashes = [], {}
    def check(name, ok):
        checks.append({'control': name, 'ok': bool(ok)})
    def read(name):
        data = (directory/name).read_bytes()
        hashes[name] = hashlib.sha256(data).hexdigest()
        return data.decode('utf-8-sig')
    stem = 'geo-train-01_view0'
    try:
        meta = json.loads(read(stem+'.meta.json'))
        rows = list(csv.reader(read(stem+'_hist.csv').splitlines()))
        log = read('run.log')
        status = read('exit_code.txt').strip()
        check('codigo_real_reportado_cero', status == '0')
        check('geometria', meta.get('geometry_id') == 'geo-train-01')
        check('vista', type(meta.get('view_index')) is int and meta['view_index'] == 0)
        for field, expected in [('events_transported',1000), ('ecomug_draws_total',1000),
                                ('seed',2026100107), ('threads',1)]:
            check(field, type(meta.get(field)) is int and meta[field] == expected)
        check('sin_exposicion_temporal_asignada', meta.get('exposure_days') == -1)
        grid = meta.get('grid', {})
        for key, value in {'azimuth_convention':'az-edges-v1', 'n_az':256, 'n_el':256,
                           'az_edges_deg':[-30,30], 'az_step_deg':60/256,
                           'az_first_center_deg':-29.8828125,
                           'az_half_deg':30, 'el_min_deg':2, 'el_max_deg':47,
                           'elevation_convention':'legacy-centers-2-47'}.items():
            check('malla_'+key, grid.get(key) == value)
        shape = len(rows)==256 and all(len(row)==256 for row in rows)
        check('histograma_256x256', shape)
        integers = shape and all(re.fullmatch(r'[0-9]+', v.strip()) for row in rows for v in row)
        check('conteos_enteros_no_negativos', integers)
        total = sum(int(v) for row in rows for v in row) if integers else None
        detected = meta.get('detected_in_bins')
        check('detectados_coinciden_con_histograma', integers and type(detected) is int and detected == total)
        check('detectados_dentro_presupuesto', total is not None and 0 <= total <= 1000)
        check('marca_final_log', re.search(r'RUN DONE\s+geo-train-01\s+view\s+0\b', log) is not None)
        check('sin_errores_conocidos_en_log', re.search(
            r'G4Exception|GeomVol1002|FatalException|Segmentation fault|Traceback', log, re.I) is None)
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError) as exc:
        checks.append({'control':'lectura_de_entrega', 'ok':False, 'detalle':str(exc)})
    return {'estado':'conforme_control_tecnico' if all(c['ok'] for c in checks) else 'requiere_revision',
            'alcance':'coherencia de archivos; no valida aceptacion fisica, version real de Geant4 ni origen del binario',
            'nota':'Un log sin patrones de error no garantiza ausencia de todos los fallos. Revisar entorno y procedencia aparte.',
            'sha256':hashes, 'controles':checks}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('entrega', type=Path)
    p.add_argument('--salida', type=Path, required=True)
    a = p.parse_args()
    report = review(a.entrega)
    # New report only: never overwrite a delivery file or an earlier review.
    with a.salida.open('x', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write('\n')
    failed = sum(not c['ok'] for c in report['controles'])
    print(f"{report['estado']}: {len(report['controles'])} controles, {failed} fallidos")
    return int(failed > 0)


if __name__ == '__main__':
    raise SystemExit(main())

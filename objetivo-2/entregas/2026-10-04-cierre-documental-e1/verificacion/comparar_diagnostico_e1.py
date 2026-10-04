"""Compara una reproducción del diagnóstico interior E1 con la evidencia publicada por la dirección.

Uso: python comparar_diagnostico_e1.py --referencia JSON --referencia-csv CSV
       --reproduccion JSON --reproduccion-csv CSV --salida JSON
Tolerancia: diferencia absoluta 1e-12 en cada valor numérico (instrucciones de cierre E1).
"""
import argparse, csv, json, math
from pathlib import Path

TOL = 1e-12


def comparar(a, b, ruta, difs, stats):
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            difs.append({'ruta': ruta, 'motivo': 'claves distintas', 'solo_referencia': sorted(set(a) - set(b)), 'solo_reproduccion': sorted(set(b) - set(a))})
            return
        for k in a:
            comparar(a[k], b[k], f'{ruta}/{k}', difs, stats)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            difs.append({'ruta': ruta, 'motivo': f'longitud {len(a)} frente a {len(b)}'})
            return
        for i, (x, y) in enumerate(zip(a, b)):
            comparar(x, y, f'{ruta}[{i}]', difs, stats)
    elif isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or a is None:
        stats['no_numericos'] += 1
        if a != b:
            difs.append({'ruta': ruta, 'referencia': a, 'reproduccion': b})
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        stats['numericos'] += 1
        d = abs(float(a) - float(b))
        stats['max_dif'] = max(stats['max_dif'], d)
        if not (d <= TOL) or math.isnan(d):
            difs.append({'ruta': ruta, 'referencia': a, 'reproduccion': b, 'diferencia': d})
    else:
        difs.append({'ruta': ruta, 'motivo': f'tipos {type(a).__name__} frente a {type(b).__name__}'})


def leer_csv(p):
    with open(p, encoding='utf-8', newline='') as f:
        filas = list(csv.DictReader(f))
    for fila in filas:
        for k, v in fila.items():
            try:
                fila[k] = int(v)
            except ValueError:
                try:
                    fila[k] = float(v)
                except ValueError:
                    pass
    return filas


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for n in ['referencia', 'referencia-csv', 'reproduccion', 'reproduccion-csv', 'salida']:
        p.add_argument('--' + n, type=Path, required=True)
    a = p.parse_args()
    ref = json.loads(a.referencia.read_text(encoding='utf-8'))
    rep = json.loads(a.reproduccion.read_text(encoding='utf-8'))
    informe = {'tolerancia_absoluta': TOL, 'secciones': {}}
    # Campos científicos; script_sha256 se informa aparte porque depende del archivo del script.
    for clave in ['delivery_commit', 'source_predictions', 'regions_checked', 'regions', 'distance_bands', 'geo1_summary',
                  'heldout_opened', 'training_performed', 'selection_performed', 'interpretation']:
        difs, stats = [], {'numericos': 0, 'no_numericos': 0, 'max_dif': 0.0}
        comparar(ref.get(clave), rep.get(clave), clave, difs, stats)
        informe['secciones'][clave] = {**stats, 'diferencias': len(difs), 'ejemplos': difs[:10]}
    difs, stats = [], {'numericos': 0, 'no_numericos': 0, 'max_dif': 0.0}
    comparar(leer_csv(a.referencia_csv), leer_csv(a.reproduccion_csv), 'bandas.csv', difs, stats)
    informe['secciones']['bandas.csv'] = {**stats, 'diferencias': len(difs), 'ejemplos': difs[:10]}
    informe['conteos'] = {'sesgos_comprobados': rep['regions_checked'], 'filas_regionales': len(rep['regions']),
                          'filas_por_banda': len(rep['distance_bands'])}
    informe['script_sha256'] = {'referencia': ref.get('script_sha256'), 'reproduccion': rep.get('script_sha256')}
    informe['concordante'] = all(s['diferencias'] == 0 for s in informe['secciones'].values()) \
        and informe['conteos'] == {'sesgos_comprobados': 252, 'filas_regionales': 126, 'filas_por_banda': 378}
    a.salida.write_text(json.dumps(informe, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'concordante': informe['concordante'], 'conteos': informe['conteos'],
                      'max_dif': max(s['max_dif'] for s in informe['secciones'].values()),
                      'diferencias': {k: s['diferencias'] for k, s in informe['secciones'].items()}}, ensure_ascii=False))


if __name__ == '__main__':
    main()

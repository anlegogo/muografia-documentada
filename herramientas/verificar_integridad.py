"""Comprueba el material OE1 recibido sin modificar originales (solo stdlib)."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / 'objetivo-1/originales'


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    errors = []
    inventory = json.loads((ROOT / 'objetivo-1/inventario/archivos.json').read_text(encoding='utf-8'))
    hashes = {}
    for item in inventory['archivos']:
        p = ROOT / item['destino']
        if not p.is_file():
            errors.append(f"Ausente: {item['destino']}")
            continue
        actual = sha256(p)
        hashes[p] = actual
        if actual != item['sha256'] or p.stat().st_size != item['bytes']:
            errors.append(f"Contenido diferente: {item['destino']}")

    splits = json.loads((ORIG / 'results/dataset/splits.json').read_text(encoding='utf-8'))
    ids = [g for group in splits['splits'].values() for g in group]
    if len(ids) != 19 or len(set(ids)) != 19:
        errors.append('Particiones: geometrías ausentes o repetidas.')
    for gid, expected in splits['shard_sha256'].items():
        if hashes.get(ORIG / f'dataset/shards/{gid}.npz') != expected:
            errors.append(f'Shard distinto del manifiesto: {gid}')
    rows = list(csv.DictReader((ORIG / 'results/dataset/campaign-manifest.csv').open(encoding='utf-8')))
    if len(rows) != 114 or len({(r['geometry'], r['view']) for r in rows}) != 114:
        errors.append('Campaña: número de vistas incorrecto o claves repetidas.')
    expected_views = {(g, str(v)) for g in ids for v in range(6)}
    if {(r['geometry'], r['view']) for r in rows} != expected_views:
        errors.append('Campaña: no coincide con seis vistas por geometría.')
    for row in rows:
        stem = ORIG / 'data/campaign-geant4' / row['geometry'] / (row['geometry'] + '_view' + row['view'])
        meta_path = stem.with_suffix('.meta.json')
        if not meta_path.exists():
            errors.append(f'Metadato ausente: {meta_path.name}')
            continue
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        if hashes.get(stem.with_suffix('.npz')) != meta['npz_sha256']:
            errors.append(f'NPZ de vista distinto del metadato: {stem.name}')
        if (row['hist_sha256'] != meta['hist_sha256']
            or int(row['events_transported']) != meta['events_transported']
            or int(row['detected']) != meta['detected_in_bins']):
            errors.append(f'Manifiesto y metadato discrepan: {stem.name}')
    totals = {'transportados':sum(int(r['events_transported']) for r in rows),
              'detectados':sum(int(r['detected']) for r in rows)}
    if totals != {'transportados':4124005421,'detectados':3025131757}:
        errors.append('Totales diferentes de los documentados.')
    result = {'fecha_utc':datetime.now(timezone.utc).isoformat(),'revision_fuente':inventory['revision_fuente'],
              'ok':not errors,'archivos_verificados':len(hashes),'archivos_esperados':len(inventory['archivos']),
              'shards':len(splits['shard_sha256']),'vistas':len(rows),'geometrias':len(ids),
              'totales':totals,'errores':errors,
              'limite':'Integridad y consistencia documental; no valida física ni ejecuta Geant4.'}
    out = ROOT / 'objetivo-1/evidencias/verificacion-local.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())

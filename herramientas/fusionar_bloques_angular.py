"""Fusión local estricta de bloques SC3 (alternativa a fusionar_v1.py de f9a77ef).

python herramientas/fusionar_bloques_angular.py --manifiesto MAN.csv --salida BLOQUES --destino NUEVO
--aceptar-crlf admite exclusivamente CRLF->LF cuando reproduce el SHA de SC3.
Nunca altera entradas. Valida todo el lote antes de crear el destino.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import numpy as np
from configuracion_angular import configuration
from preparar_imagen_angular_v1 import read_image


def sha(data):
    return hashlib.sha256(data).hexdigest()


def manifest_rows(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        required = ['fila', 'geometria', 'vista', 'bloque', 'semilla', 'eventos']
        if reader.fieldnames != required:
            raise ValueError('columnas de manifiesto inválidas')
        rows = list(reader)
    if not rows:
        raise ValueError('manifiesto vacío')
    seen_ids, seen_blocks, seen_seeds = set(), set(), set()
    for r in rows:
        if None in r or any(v is None for v in r.values()):
            raise ValueError('fila incompleta')
        if not re.fullmatch(r'geo-(train|val|test|gen)-\d{2}', r['geometria']):
            raise ValueError('geometría inválida')
        for k in ('fila', 'vista', 'bloque', 'semilla', 'eventos'):
            if not re.fullmatch(r'\d+', r[k]):
                raise ValueError('entero inválido: '+k)
            r[k] = int(r[k])
        if r['vista'] >= 6 or r['eventos'] <= 0:
            raise ValueError('vista o eventos inválidos')
        block = (r['geometria'], r['vista'], r['bloque'])
        if r['fila'] in seen_ids or block in seen_blocks or r['semilla'] in seen_seeds:
            raise ValueError('fila, bloque o semilla repetidos')
        seen_ids.add(r['fila']); seen_blocks.add(block); seen_seeds.add(r['semilla'])
    return rows


def verify_outputs(directory, stem, accept_crlf):
    p = directory/'salida.sha256'
    entries = {}
    for line in p.read_text().splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or not re.fullmatch('[0-9a-f]{64}', parts[0]):
            raise ValueError('manifiesto SHA inválido')
        name = parts[1].strip().lstrip('*').replace('\\', '/').split('/')[-1]
        if name in entries or name in ('', '.', '..'):
            raise ValueError('nombre repetido o inválido en SHA')
        entries[name] = parts[0]
    if not {stem+'_hist.csv', stem+'.meta.json'} <= entries.keys():
        raise ValueError('faltan huellas obligatorias')
    records = []
    for name, expected in entries.items():
        data = (directory/name).read_bytes()
        raw = sha(data)
        canonical = sha(data.replace(b'\r\n', b'\n'))
        conversion = raw != expected
        if conversion and not (accept_crlf and b'\r\n' in data and canonical == expected):
            raise ValueError('huella no coincide: '+name)
        records.append({'name': name, 'received_sha256': raw, 'expected_sha256': expected,
                        'crlf_to_lf_verified': conversion})
    return records


def input_entries(path):
    result = {}
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) != 2 or not re.fullmatch('[0-9a-f]{64}', parts[0]):
            raise ValueError('entradas.sha256 inválido')
        name = parts[1].replace('\\', '/')
        if name in result:
            raise ValueError('entrada repetida')
        result[name] = parts[0]
    if not result:
        raise ValueError('manifiesto de entradas vacío')
    return result


def validate_block(r, source, accept_crlf=False):
    source = Path(source)
    geo, view = r['geometria'], r['vista']
    d = source/geo/f'view{view}'/f"block{r['bloque']:04d}"
    stem = f'{geo}_view{view}'
    if (d/'exit_code.txt').read_text().strip() != '0':
        raise ValueError('bloque fallido: '+str(d))
    hashes = verify_outputs(d, stem, accept_crlf)
    _, counts, _, meta, _ = read_image(d/(stem+'_hist.csv'))
    for key, expected in [('seed', r['semilla']), ('view_index', view),
                          ('events_transported', r['eventos'])]:
        if type(meta.get(key)) is not int or meta[key] != expected:
            raise ValueError('manifiesto contradice '+key)
    if meta['geometry_id'] != geo or meta.get('exposure_days') != -1:
        raise ValueError('geometría o exposición incompatible; se requieren bloques N fijo')
    inputs = input_entries(d/'entradas.sha256')
    config = configuration(meta)
    signature = json.dumps({'config': config, 'inputs': inputs, 'threads': meta.get('threads')}, sort_keys=True, allow_nan=False)
    wall = meta.get('wall_seconds')
    if type(wall) not in (float, int) or not math.isfinite(wall) or wall < 0:
        raise ValueError('tiempo inválido')
    all_count = meta.get('detected_all_energies', meta['detected_in_bins'])
    if type(all_count) is not int or not meta['detected_in_bins'] <= all_count <= r['eventos']:
        raise ValueError('conteo sin corte incoherente')
    if 'reference_histogram' in meta and 'detected_all_energies' not in meta:
        raise ValueError('falta conteo de todas las energías')
    mean = meta.get('mean_ekin_detected_gev')
    if mean is not None and (type(mean) not in (float, int) or not math.isfinite(mean) or mean < 0):
        raise ValueError('media energética inválida')
    draws = meta.get('ecomug_draws_total')
    if type(draws) is not int or draws < r['eventos']:
        raise ValueError('contador de generación inválido')
    entry = {'row': r, 'meta': meta, 'counts': counts, 'hashes': hashes,
             'all_count': all_count, 'mean': mean, 'directory': d, 'signature': signature}
    return entry


def merge(manifest, source, destination, accept_crlf=False):
    source, destination = Path(source), Path(destination)
    if destination.exists():
        raise FileExistsError(destination)
    rows = manifest_rows(manifest)
    groups = {}
    for r in rows:
        entry = validate_block(r, source, accept_crlf)
        groups.setdefault((r['geometria'], r['vista']), []).append(entry)
    prepared = []
    geometry_signatures = {}
    for (geo, view), blocks in sorted(groups.items()):
        if len({b['signature'] for b in blocks}) != 1:
            raise ValueError('bloques con entradas o configuración distintas')
        if geo in geometry_signatures and geometry_signatures[geo] != blocks[0]['signature']:
            raise ValueError('vistas de una geometría con entradas o configuración distintas')
        geometry_signatures[geo] = blocks[0]['signature']
        counts = sum((b['counts'].astype(np.uint64) for b in blocks), np.zeros((256, 256), np.uint64))
        if int(counts.max()) >= 2**32:
            raise ValueError('conteos exceden uint32')
        meta = dict(blocks[0]['meta'])
        for key in ('events_transported', 'ecomug_draws_total', 'wall_seconds'):
            meta[key] = sum(b['meta'][key] for b in blocks)
        meta['seconds_per_event'] = meta['wall_seconds']/meta['events_transported']
        meta['wall_seconds_semantics'] = 'sum of block wall times; not campaign elapsed time'
        meta['detected_in_bins'] = int(counts.sum())
        meta['detected_all_energies'] = sum(b['all_count'] for b in blocks)
        meta.pop('mean_ekin_detected_gev', None)
        if all(b['mean'] is not None for b in blocks) and meta['detected_all_energies']:
            meta['mean_ekin_all_energies_gev'] = sum(b['mean']*b['all_count'] for b in blocks)/meta['detected_all_energies']
        meta['energy_mean_note'] = 'all-energy weighted mean when available; selected-energy mean unavailable'
        meta.pop('seed', None)
        meta['block_seeds'] = [b['row']['semilla'] for b in blocks]
        meta['merged_blocks'] = len(blocks)
        meta['merge_contract'] = 'oe1-strict-block-merge-v1'
        prepared.append((geo, view, counts, meta, blocks))
    # All validation above; interruption below can leave an incomplete directory.
    destination.mkdir(parents=True, exist_ok=False)
    report = {'schema': 'oe1-strict-block-merge-v1', 'physical_validation': False,
              'manifest_sha256': sha(Path(manifest).read_bytes()), 'accept_crlf': accept_crlf, 'views': []}
    for geo, view, counts, meta, blocks in prepared:
        d = destination/geo; d.mkdir(exist_ok=True)
        stem = f'{geo}_view{view}'
        hist = d/(stem+'_hist.csv'); mp = d/(stem+'.meta.json')
        hist.write_bytes(('\n'.join(','.join(map(str, row)) for row in counts)+'\n').encode())
        mp.write_bytes((json.dumps(meta, indent=2)+'\n').encode())
        # Per-geometry manifest shared by all its views must agree.
        provenance = blocks[0]['directory']/'entradas.sha256'
        manifest_out = d/'entradas.sha256'
        if manifest_out.exists() and input_entries(manifest_out) != input_entries(provenance):
            raise ValueError('vistas de una geometría con entradas distintas')
        manifest_out.write_bytes(provenance.read_bytes())
        _, reread, _, _, _ = read_image(hist)
        if not np.array_equal(reread, counts):
            raise RuntimeError('fallo de relectura')
        report['views'].append({'geometry': geo, 'view': view, 'events': meta['events_transported'],
             'counts': meta['detected_in_bins'], 'all_energy_counts': meta['detected_all_energies'],
             'hist_sha256': sha(hist.read_bytes()), 'meta_sha256': sha(mp.read_bytes()),
             'blocks': [{'manifest_row': b['row'], 'outputs': b['hashes'],
                         'input_manifest_sha256': sha((b['directory']/'entradas.sha256').read_bytes())} for b in blocks]})
    (destination/'revision-fusion.json').write_bytes((json.dumps(report, indent=2)+'\n').encode())
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifiesto', type=Path, required=True)
    parser.add_argument('--salida', type=Path, required=True)
    parser.add_argument('--destino', type=Path, required=True)
    parser.add_argument('--aceptar-crlf', action='store_true')
    args = parser.parse_args()
    print(json.dumps(merge(args.manifiesto, args.salida, args.destino, args.aceptar_crlf), indent=2))

"""Comprueba una descarga OE1 contra inventarios congelados, sin modificar datos."""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def content_hash(array):
    h = hashlib.sha256()
    h.update(array.dtype.str.encode())
    h.update(str(array.shape).encode())
    h.update(np.ascontiguousarray(array).tobytes())
    return h.hexdigest()


def verify(download, reference, inventory=None):
    results = {'timestamp_utc': datetime.now(timezone.utc).isoformat(),
               'python': platform.python_version(), 'numpy': np.__version__,
               'checks': [], 'inventory': []}
    def check(name, actual, expected):
        results['checks'].append({'name': name, 'actual': actual,
                                  'expected': expected, 'ok': actual == expected})
    for path in sorted(download.rglob('*')):
        if path.is_file():
            results['inventory'].append({'path': path.relative_to(download).as_posix(),
                                         'bytes': path.stat().st_size, 'sha256': sha(path)})
    if inventory is not None:
        expected_inventory = json.loads(inventory.read_text(encoding='utf-8'))
        check('remote_inventory/paths_and_sizes',
              {e['path']: e['bytes'] for e in results['inventory']},
              {e['relative']: e['bytes'] for e in expected_inventory})
    for folder in ('fusion', 'imagenes'):
        expected_paths = set()
        for line in (reference / 'posproceso' / (folder + '.sha256')).read_text().splitlines():
            expected, relative = line.split(maxsplit=1)
            relative = relative.removeprefix('./')
            expected_paths.add(relative)
            path = download / folder / relative
            check(folder + '/' + relative, sha(path) if path.is_file() else None, expected)
        actual_paths = {p.relative_to(download / folder).as_posix()
                        for p in (download / folder).rglob('*') if p.is_file()}
        check(folder + '/file_set', sorted(actual_paths), sorted(expected_paths))
    hashes = json.loads((reference / 'huellas-contenido.json').read_text())
    coordinates = ['az_centers_deg', 'az_edges_deg', 'el_centers_deg', 'el_edges_deg']
    for section, folder in (('pairs', 'pares'), ('dataset_v2_shards', 'dataset-v2/shards')):
        check(folder + '/npz_file_set', sorted(p.name for p in (download / folder).glob('*.npz')),
              sorted(hashes[section]))
        for filename, arrays in hashes[section].items():
            path = download / folder / filename
            if not path.is_file():
                check(folder + '/' + filename, None, 'present')
                continue
            with np.load(path, allow_pickle=False) as package:
                check(folder + '/' + filename + '/keys', sorted(package.files),
                      sorted(list(arrays) + coordinates))
                for key, expected in arrays.items():
                    check(folder + '/' + filename + '/' + key,
                          content_hash(package[key]) if key in package else None, expected)
                source_names = ([filename.replace('_pairs.npz', '.npz')] if section == 'pairs'
                                else [filename.replace('.npz', f'_view{v}.npz') for v in range(6)])
                for source_name in source_names:
                    with np.load(download / 'imagenes' / source_name, allow_pickle=False) as source:
                        for key in coordinates:
                            check(folder + '/' + filename + '/' + source_name + '/' + key,
                                  content_hash(package[key]), content_hash(source[key]))
    manifest = json.loads((download / 'pares/manifest.json').read_text())
    check('pairs/files', len(manifest['files']), 114)
    for entry in manifest['files']:
        for name_key, hash_key in (('name', 'sha256'), ('metadata_name', 'metadata_sha256')):
            check('manifest/' + entry[name_key], sha(download / 'pares' / entry[name_key]), entry[hash_key])
        check('reference/' + entry['name'], sha(download / 'imagenes' /
              f"{entry['geometry_id']}_view{entry['view']}.npz"), entry['reference_sha256'])
    splits = json.loads((download / 'dataset-v2/splits.json').read_text())
    check('splits/source_manifest', sha(download / 'pares/manifest.json'),
          splits['source_package_manifest_sha256'])
    for gid, expected in splits['shard_sha256'].items():
        check('shard-manifest/' + gid, sha(download / 'dataset-v2/shards' / (gid + '.npz')), expected)
    original_splits = json.loads((reference / 'dataset-v2/splits.json').read_text())
    check('splits/geometries', splits['splits'], original_splits['splits'])
    check('splits/counts', splits['pairs_per_split'],
          {'train': 5760, 'val': 1440, 'test': 1440, 'generalization': 480})
    results['summary'] = {'files': len(results['inventory']),
                          'bytes': sum(e['bytes'] for e in results['inventory']),
                          'checks': len(results['checks']),
                          'failed': sum(not e['ok'] for e in results['checks'])}
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--descarga', type=Path, required=True)
    parser.add_argument('--referencia', type=Path, required=True)
    parser.add_argument('--salida', type=Path, required=True)
    parser.add_argument('--inventario-remoto', type=Path)
    args = parser.parse_args()
    report = verify(args.descarga, args.referencia, args.inventario_remoto)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    with args.salida.open('x', encoding='utf-8') as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
        output.write('\n')
    print(json.dumps(report['summary']))
    raise SystemExit(1 if report['summary']['failed'] else 0)

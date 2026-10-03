"""Contrato OE2 v1: datos explícitos, huellas fijadas y escala solo de train.

Sustituye el lector histórico; no modifica los paquetes de los estudiantes.
"""
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset

INPUT_SCALINGS = ('train_log_bounded_v1',)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read_verified(root, name, expected):
    root = Path(root).resolve()
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Ruta fuera del conjunto')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f'Huella de datos diferente: {name}')
    return raw


def normalize_counts(counts, scale):
    counts = np.asarray(counts, dtype=np.float64)
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError('Escala inválida')
    if not np.isfinite(counts).all() or (counts < 0).any():
        raise ValueError('Se requieren conteos finitos no negativos')
    log_counts = np.log1p(counts)
    return (log_counts / (log_counts + scale)).astype(np.float32)


def normalize_input(low, fraction, scale):
    if not np.isfinite(fraction) or not 0 < fraction <= 1:
        raise ValueError('Fracción fuera de (0,1]')
    return normalize_counts(np.asarray(low, dtype=np.float64) / fraction, scale)


def inverse_counts(values, scale):
    z = np.asarray(values, dtype=np.float64)
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError('Escala inválida')
    if not np.isfinite(z).all() or (z < 0).any() or (z >= 1).any():
        raise ValueError('La inversión requiere 0 <= z < 1; no se recorta silenciosamente')
    exponent = scale * z / (1-z)
    if (exponent > np.log(np.finfo(np.float64).max) - 1).any():
        raise ValueError('Predicción fuera del rango numérico invertible')
    return np.expm1(exponent)


def checked_arrays(z):
    ref, low, fractions = z['ref_counts'], z['low_counts'], z['fractions']
    if ref.shape != (6,256,256) or low.shape != (6,4,20,256,256):
        raise ValueError('Dimensiones incompatibles con campaña OE1')
    if ref.dtype != np.uint32 or low.dtype != np.uint16:
        raise ValueError('Tipos de conteo incompatibles')
    if fractions.shape != (4,) or not np.allclose(fractions,[.5,.1,.05,.01],rtol=0,atol=1e-8):
        raise ValueError('Fracciones incompatibles')
    if (low.astype(np.uint32) > ref[:,None,None,:,:]).any():
        raise ValueError('Conteos de baja estadística superiores a su referencia')
    return ref, low, fractions


def prepare_manifest(root, output):
    """Congela train/val y comprueba conversión directamente contra pares."""
    root, output = Path(root), Path(output)
    splits = json.loads((root/'dataset-v2/splits.json').read_text())
    groups = splits['splits']
    if set(groups) != {'train','val','test','generalization'}:
        raise ValueError('Particiones incompletas')
    ids = sum(groups.values(), [])
    if len(ids) != len(set(ids)) or any(not v for v in groups.values()):
        raise ValueError('Particiones vacías o solapadas')
    files = {}
    for name in ['dataset-v2/splits.json','dataset-v2/conversion-report.json','pares/manifest.json']:
        files[name] = digest(root/name)
    maximum, views = 0, 0
    for split in ('train','val'):
        for gid in groups[split]:
            name = f'dataset-v2/shards/{gid}.npz'
            meta_name = f'dataset-v2/shards/{gid}.meta.json'
            files[name], files[meta_name] = digest(root/name), digest(root/meta_name)
            meta = json.loads(read_verified(root,meta_name,files[meta_name]))
            if meta['geometry_id'] != gid or sorted(s['view'] for s in meta['source_views']) != list(range(6)):
                raise ValueError('Metadatos de geometría/vistas incompatibles')
            with np.load(io.BytesIO(read_verified(root,name,files[name])),allow_pickle=False) as z:
                ref, low, fractions = checked_arrays(z)
                if split == 'train':
                    maximum = max(maximum, int(ref.max()))
                for source in meta['source_views']:
                    vi = source['view']
                    pair_name = 'pares/' + source['pairs_file']
                    files[pair_name] = digest(root/pair_name)
                    with np.load(io.BytesIO(read_verified(root,pair_name,files[pair_name])),allow_pickle=False) as q:
                        if not np.array_equal(ref[vi],q['counts_ref']) or not np.array_equal(low[vi],q['low_counts']):
                            raise ValueError('La conversión no conserva los conteos')
                    views += 1
    manifest = {'contract':'oe2-v1', 'files':files, 'splits':groups,
                'normalization':{'name':INPUT_SCALINGS[0], 'fit_split':'train',
                                 'train_max':maximum, 'scale':float(np.log1p(max(1,maximum)))},
                'source_views_compared':views}
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists():
        raise FileExistsError('El manifiesto es inmutable: elegir otra salida')
    output.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    return digest(output)


class DataContract:
    def __init__(self, root, manifest_path, expected_sha):
        self.root = Path(root)
        raw = Path(manifest_path).read_bytes()
        if not expected_sha or hashlib.sha256(raw).hexdigest() != expected_sha:
            raise ValueError('Huella del manifiesto distinta de la fijada')
        self.identity = expected_sha
        self.manifest = json.loads(raw)
        if self.manifest['contract'] != 'oe2-v1':
            raise ValueError('Contrato desconocido')
        self.scale = self.manifest['normalization']['scale']
        for name, expected in self.manifest['files'].items():
            # Huellas de fuentes además de los shards consumidos; no se abre
            # ninguna imagen de test/generalization.
            if digest(self.root/name) != expected:
                raise ValueError(f'Huella de datos diferente: {name}')

    def arrays(self, gid):
        name = f'dataset-v2/shards/{gid}.npz'
        raw = read_verified(self.root,name,self.manifest['files'][name])
        with np.load(io.BytesIO(raw),allow_pickle=False) as z:
            return checked_arrays(z)


class MuographyPairs(Dataset):
    def __init__(self, contract, split, fraction, hflip=False, seed=0, limit=None):
        if split not in ('train','val'):
            raise ValueError('Este contrato de entrenamiento no abre conjuntos reservados')
        if not np.isfinite(fraction) or not 0 < fraction <= 1:
            raise ValueError('Fracción inválida')
        if limit is not None and (not isinstance(limit,int) or limit <= 0):
            raise ValueError('Límite de prueba inválido')
        self.scale, self.fraction = contract.scale, fraction
        self.hflip, self.seed, self.epoch = hflip, seed, 0
        self.cache, self.index = {}, []
        for gid in contract.manifest['splits'][split]:
            ref, low, fractions = contract.arrays(gid)
            matches = np.flatnonzero(np.isclose(fractions,fraction,rtol=0,atol=1e-8))
            if len(matches) != 1:
                raise ValueError('Fracción ausente o ambigua')
            self.cache[gid] = ref, low[:,matches[0]]
            self.index.extend((gid,vi,k) for vi in range(6) for k in range(20))
            if limit and len(self.index) >= limit:
                self.index = self.index[:limit]
                break

    def set_epoch(self, epoch):
        self.epoch = epoch

    def __len__(self):
        return len(self.index)

    def __getitem__(self, i):
        gid,vi,k = self.index[i]
        ref,low = self.cache[gid]
        x = normalize_input(low[vi,k],self.fraction,self.scale)
        y = normalize_counts(ref[vi],self.scale)
        if self.hflip and np.random.default_rng(self.seed+self.epoch*1000003+i).random() < .5:
            x,y = np.flip(x,-1).copy(), np.flip(y,-1).copy()
        return torch.from_numpy(x).unsqueeze(0),torch.from_numpy(y).unsqueeze(0)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Preparar manifiesto OE2 sin entrenar')
    p.add_argument('--data-root',required=True)
    p.add_argument('--output',required=True)
    args = p.parse_args()
    print(prepare_manifest(args.data_root,args.output))

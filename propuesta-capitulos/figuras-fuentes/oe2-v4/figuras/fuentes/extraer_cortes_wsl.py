"""Extrae, de las matrices auditadas de la evaluación final, los cortes que usan las
figuras de imágenes del OE2 (vista 0, realización 0 de las cuatro geometrías
reservadas), con la misma regla de selección del informe de la dirección
(objetivo-2/herramientas/figuras_cierre_oe2.py, revisión 166be6f).

Se ejecuta en WSL, donde están los datos (no descarga nada, no ejecuta redes):
    ~/cierre-e1/venv/bin/python extraer_cortes_wsl.py \
        --datos ~/evalfinal/insumos/dataset-v2/shards \
        --predicciones ~/evalfinal/drive/oe2-evaluacion-final-f05 \
        --procedencia <procedencia-figuras.json de la dirección> \
        --salida <carpeta>/cortes_oe2.npz
Antes de leer, cada archivo se contrasta con la huella SHA-256 registrada por la
dirección; si alguna difiere, se detiene. Guarda conteos de referencia, entrada
(C_low/f) y predicciones normalizadas, sin recortes ni remuestreo.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

GEOS = ['geo-test-01', 'geo-test-02', 'geo-test-03', 'geo-gen-01']
MODELOS = ['unet_original', 'cgan_original', 'B1_C0', 'B1_C1', 'B2_C0', 'B2_C1', 'B3_C0', 'B3_C1']
V, R, F = 0, 0, 0.05


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


a = argparse.ArgumentParser()
a.add_argument('--datos', type=Path, required=True)
a.add_argument('--predicciones', type=Path, required=True)
a.add_argument('--procedencia', type=Path, required=True)
a.add_argument('--salida', type=Path, required=True)
a = a.parse_args()
esperadas = json.loads(a.procedencia.read_text(encoding='utf-8'))['sources_sha256']
out, verif = {}, {}
for g in GEOS:
    p = a.datos / f'{g}.npz'
    assert sha(p) == esperadas[f'datos/{g}.npz'], p
    verif[f'datos/{g}.npz'] = True
    with np.load(p) as d:
        fi = int(np.flatnonzero(np.isclose(d['fractions'], F))[0])
        out[f'{g}/ref'] = d['ref_counts'][V].astype(np.float64)
        out[f'{g}/low'] = d['low_counts'][V, fi, R].astype(np.float64) / F
        for k in d.files:
            if k not in ('ref_counts', 'low_counts') and d[k].ndim <= 2 and d[k].size <= 1024:
                out[f'{g}/meta/{k}'] = d[k]
    for m in MODELOS:
        p = a.predicciones / m / f'{g}.npy'
        assert sha(p) == esperadas[f'predicciones/{m}/{g}.npy'], p
        verif[f'predicciones/{m}/{g}.npy'] = True
        z = np.load(p, mmap_mode='r')
        assert z.shape == (120, 256, 256)
        zz = np.asarray(z[V * 20 + R], dtype=np.float64)
        assert np.isfinite(zz).all() and (zz >= 0).all() and (zz < 1).all()
        out[f'{g}/{m}'] = zz
a.salida.parent.mkdir(parents=True, exist_ok=True)
np.savez_compressed(a.salida, **out)
print(json.dumps({'verificados': len(verif), 'esperados': len(esperadas), 'claves': len(out),
                  'meta': sorted({k.split('/meta/')[1] for k in out if '/meta/' in k})}))

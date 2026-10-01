"""Revisión independiente de R2-01: integridad, primarios, materiales y detección.

Uso: python herramientas/revisar_complemento_r201.py --entrega DIR --inputs DIR
     --reproduccion DIR --out JSON
Requiere numpy/pandas y revisar_etapa1_oe1.py del mismo directorio.
No ejecuta transporte Geant4.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from revisar_etapa1_oe1 import sha, table, primary_hashes


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ('entrega', 'inputs', 'reproduccion', 'out'):
        p.add_argument('--'+key, type=Path, required=True)
    a = p.parse_args()
    checks = []
    def check(name, ok):
        checks.append({'control': name, 'ok': bool(ok)})
    for line in (a.entrega/'MANIFIESTO.sha256').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        path = a.entrega/name.lstrip('*')
        if name == '.gitattributes':
            # Git archive en Windows aplica CRLF a este archivo de texto.
            check('sha256:LF-normalized:'+name, hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() == digest)
        else:
            check('sha256:'+name, sha(path) == digest)
    lp = a.inputs/'geo-train-06_v0_r10_r201.primarios.csv'
    prim = table(lp)
    hashes = primary_hashes(prim)
    runs = {}
    for variant in ('A', 'B'):
        for seed in (1026093011, 1026093012, 1026093013):
            root = a.entrega/f'corridas/intento-01/{variant}/{seed}'
            t = table(root/'geo-train-06_view0_muones.csv').sort_values('id').reset_index(drop=True)
            key = f'{variant}/{seed}'
            check(key+':ids', list(t.id) == list(range(12)))
            check(key+':primary_hash', np.array_equal(t.prim_fnv, hashes))
            check(key+':list_hash', (t.list_sha256 == sha(lp)).all())
            check(key+':crossed', (t.crossed == 1).all())
            h = np.loadtxt(root/'geo-train-06_view0_hist.csv', delimiter=',', dtype=int)
            reconstructed = np.zeros_like(h)
            det = t[t.detected == 1]
            np.add.at(reconstructed, (det.iel.to_numpy(), det.iaz.to_numpy()), 1)
            check(key+':histogram', np.array_equal(h, reconstructed))
            check(key+':material', np.allclose(t.lz_m, t.lz_a1_m if variant == 'B' else np.where(t.id < 6, t.lz_a0_m, t.lz_a1_m), rtol=0, atol=1e-6))
            runs[(variant, seed)] = t
    changes, energies = [], []
    for seed in (1026093011, 1026093012, 1026093013):
        x, y = runs[('A', seed)], runs[('B', seed)]
        check(str(seed)+':rng0', (x.rng0 == y.rng0).all())
        check(str(seed)+':detection', (x.detected == y.detected).all())
        cols = [c for c in x if c != 'variant']
        check(str(seed)+':dense_controls_equal', x.loc[6:, cols].equals(y.loc[6:, cols]))
        for i in range(6):
            energies.append({'seed': seed, 'id': i, 'delta_exit_GeV': float(y.e_out_gev[i]-x.e_out_gev[i]), 'delta_loss_GeV': float((y.e_in_gev[i]-y.e_out_gev[i])-(x.e_in_gev[i]-x.e_out_gev[i]))})
            if (x.iel[i], x.iaz[i]) != (y.iel[i], y.iaz[i]):
                changes.append({'seed': seed, 'id': i, 'A': [int(x.iel[i]), int(x.iaz[i])], 'B': [int(y.iel[i]), int(y.iaz[i])]})
    for name in ('pares-r201.csv', 'trayectorias-r201.csv'):
        check('reproduction:'+name, sha(a.entrega/'analisis'/name) == sha(a.reproduccion/name))
    original = json.loads((a.entrega/'analisis/resumen-r201.json').read_text(encoding='utf-8'))
    reproduced = json.loads((a.reproduccion/'resumen-r201.json').read_text(encoding='utf-8'))
    check('reproduction:coverage', original['cobertura'] == reproduced['cobertura'])
    result = {'date': '2026-10-01', 'delivery': 'a4d7b79', 'checks': checks, 'passed': sum(c['ok'] for c in checks), 'failed': sum(not c['ok'] for c in checks), 'pixel_changes': changes, 'energy_pairs': energies, 'lower_exit_B': sum(e['delta_exit_GeV'] < 0 for e in energies), 'higher_loss_B': sum(e['delta_loss_GeV'] > 0 for e in energies), 'limitation': 'Registros agregados; no reconstruyen trayectoria completa ni frecuencia bajo la fuente original.'}
    a.out.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('checks','energy_pairs')}, ensure_ascii=False))
    raise SystemExit(bool(result['failed']))


if __name__ == '__main__':
    main()

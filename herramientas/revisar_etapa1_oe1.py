"""Auditoría independiente de archivos OE1 etapa 1; no ejecuta Geant4.

Python 3.11+, numpy y pandas. No importa módulos de los estudiantes.
Uso y versiones: objetivo-1/REVISION_ETAPA_1_2026-09-30.md.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def table(path):
    return pd.read_csv(path, float_precision='round_trip', keep_default_na=False)


def primary_hashes(t):
    """FNV del primario normalizado según contrato documentado del binario."""
    rec = np.zeros(len(t), dtype=[('values', '<f8', (7,)), ('pdg', '<i4')])
    d = t[['dx', 'dy', 'dz']].to_numpy(dtype=float)
    inv = 1.0 / np.sqrt(d[:, 0]**2 + d[:, 1]**2 + d[:, 2]**2)
    rec['values'][:, :3] = t[['x_m', 'y_m', 'z_m']].to_numpy(dtype=float) * 1000
    rec['values'][:, 3:6] = d * inv[:, None]
    rec['values'][:, 6] = t['ekin_gev'].to_numpy(dtype=float) * 1000
    rec['pdg'] = t['pdg']
    octets = rec.view(np.uint8).reshape(len(t), 60)
    h = np.full(len(t), 0xcbf29ce484222325, dtype=np.uint64)
    for i in range(60):
        h = (h ^ octets[:, i].astype(np.uint64)) * np.uint64(0x100000001b3)
    return np.array([f'{v:016x}' for v in h])


def straight_lengths(t, geometry, details=False):
    """Intersección de semirrectas con cilindro finito y elipsoide originales.

    Control de líneas ideales; NO reconstruye la trayectoria de transporte.
    Los casos de esta entrega tienen dirección transversal y vertical no nula.
    """
    p = t[['x_m', 'y_m', 'z_m']].to_numpy(dtype=float)
    d = t[['dx', 'dy', 'dz']].to_numpy(dtype=float)
    c, e = [a['params'] for a in geometry['anomalies']]

    def roots(q, v):
        aa = np.sum(v*v, axis=1)
        bb = 2*np.sum(q*v, axis=1)
        cc = np.sum(q*q, axis=1)-1
        assert np.all(aa > 0)
        disc = bb*bb-4*aa*cc
        r = np.sqrt(np.maximum(0, disc))
        return (-bb-r)/(2*aa), (-bb+r)/(2*aa), disc >= 0

    lo_c, hi_c, ok_c = roots((p[:, :2]-[c['cx_m'], c['cy_m']])/c['radius_m'], d[:, :2]/c['radius_m'])
    centre = [e['cx_m'], e['cy_m'], e['cz_m']]
    axes = [e['ax_m'], e['ay_m'], e['az_m']]
    lo_e, hi_e, ok_e = roots((p-centre)/axes, d/axes)
    assert np.all(d[:, 2] != 0)
    z0 = (c['z0_m']-p[:, 2])/d[:, 2]
    z1 = (c['z1_m']-p[:, 2])/d[:, 2]
    lo = np.maximum.reduce([np.zeros(len(t)), lo_c, lo_e, np.minimum(z0, z1)])
    hi = np.minimum.reduce([hi_c, hi_e, np.maximum(z0, z1)])
    lengths = np.where(ok_c & ok_e, np.maximum(0, hi-lo)*np.linalg.norm(d, axis=1), 0)
    if details:
        # For this catalog, away from a simultaneous boundary, lo_e means
        # entering the ellipsoid while already inside the finite cylinder.
        from_conduit = (lengths > 2e-6) & (lo_e > lo_c+1e-7) & (lo_e > np.minimum(z0,z1)+1e-7)
        from_ellipsoid = (lengths > 2e-6) & (lo_c > lo_e+1e-7) & (lo_c > np.minimum(z0,z1)+1e-7)
        return lengths, from_conduit, from_ellipsoid
    return lengths


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ('entrega', 'datos', 'codigo', 'reproduccion', 'out'):
        ap.add_argument('--'+key, required=True, type=Path)
    args = ap.parse_args()
    ent, data, code = args.entrega, args.datos, args.codigo
    prod = data/'produccion/intento-01'
    tech = data/'tecnicas/tecnicas-01'
    result = {'revision_entrega': '3a49770', 'codigo_estudiantes': '3315f82',
              'entorno': {'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__},
              'alcance': 'Archivos descargados, comparación independiente y reproducción del análisis; sin nueva ejecución Geant4.',
              'checks': [], 'corridas': [], 'pares': []}

    def check(name, ok, evidence=None):
        result['checks'].append({'control': name, 'ok': bool(ok), 'evidencia': evidence})

    def manifest(path, base, label):
        failures = []
        lines = [s for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
        for line in lines:
            expected, name = line.split(None, 1)
            p = (base/name.lstrip('*')).resolve()
            assert p.is_relative_to(base.resolve())
            if not p.is_file() or sha(p) != expected:
                failures.append(name)
        check(label, not failures, {'entradas': len(lines), 'fallos': failures})

    manifest(ent/'MANIFIESTO.sha256', ent, 'manifiesto_versionados')
    manifest(ent/'datos-compartidos/SHA256SUMS.txt', data, 'descarga_drive')
    manifest(ent/'pruebas/crudos-tecnicos-01.tar.gz.sha256', ent/'pruebas', 'archivo_pruebas_tecnicas')
    for suffix in ('crudos', 'gz'):
        manifest(prod/f'SHA256SUMS-{suffix}.txt', prod, 'produccion_'+suffix)

    mask = np.array([[int(c) for c in s] for s in (ent/'analisis/roi/R_int.mask.txt').read_text().splitlines()], dtype=bool)
    check('mascara_256x256_195', mask.shape == (256, 256) and mask.sum() == 195)
    runs = table(ent/'analisis/etapa1-01/tabla-corridas.csv')
    geometry = json.loads((code/'scripts/simulation/geometry_catalog/geometries/geo-train-06.json').read_text(encoding='utf-8'))
    pairs = {}
    for row in runs.to_dict('records'):
        case, seed, var = row['caso'], str(row['s_src']), row['variante']
        variant_dir = 'A-repeticion' if row['corrida'].endswith('-rep') else var
        run = prod/case/variant_dir/seed
        logpath = run/(case+'_view0_muones.csv')
        mu = table(logpath)
        lp = data/'listas'/f'{case}_v0_r{row["replica"]}_s{seed}.primarios.csv'
        initial = table(lp)
        check(row['corrida']+':ids', len(mu) == 100000 and np.array_equal(mu.id, np.arange(100000)))
        check(row['corrida']+':lista_ids', np.array_equal(initial.id, mu.id))
        check(row['corrida']+':primarios', np.array_equal(mu.prim_fnv, primary_hashes(initial)))
        check(row['corrida']+':lista_sha', (mu.list_sha256 == sha(lp)).all())
        check(row['corrida']+':estado', not mu.status.isin(['ABORTED', 'OTHER', 'STOPPED']).any())
        check(row['corrida']+':deteccion_estado', np.array_equal(mu.detected == 1, mu.status == 'DET'))
        det = mu.detected == 1
        hist = np.zeros((256, 256), dtype=np.int64)
        np.add.at(hist, (mu.loc[det, 'iel'].astype(int), mu.loc[det, 'iaz'].astype(int)), 1)
        check(row['corrida']+':histograma', np.array_equal(hist, np.loadtxt(run/(case+'_view0_hist.csv'), delimiter=',', dtype=int)))
        y = np.zeros(len(mu), dtype=bool)
        y[det] = mask[mu.loc[det, 'iel'].astype(int), mu.loc[det, 'iaz'].astype(int)]
        check(row['corrida']+':ROI', np.array_equal(y, mu.in_rint == 1))
        check(row['corrida']+':tabla', int(det.sum()) == row['detectados'] and int(y.sum()) == row['sumY_R_int'])
        summary = {'corrida': row['corrida'], 'N': len(mu), 'detectados': int(det.sum()), 'ROI': int(y.sum()),
                   'cruces': int((mu.crossed == 1).sum()), 'IDs_cruce': mu.loc[mu.crossed == 1, 'id'].tolist()}
        if case == 'geo-train-06':
            lengths = straight_lengths(initial, geometry)
            summary['rectas_iniciales_cruzan'] = int((lengths > 2e-6).sum())
            summary['rectas_alta_energia_cruzan'] = int(((lengths > 2e-6) & (initial.ekin_gev >= 1000)).sum())
            summary['registros_cruce'] = mu.loc[mu.crossed == 1].to_dict('records')
        result['corridas'].append(summary)
        if variant_dir != 'A-repeticion':
            pairs.setdefault((case, row['replica']), {})[var] = mu
        else:
            base = prod/case/'A'/seed/(case+'_view0_muones.csv')
            check('repeticion_AA_bytes', sha(base) == sha(logpath))
        print('VERIFICADA', row['corrida'], flush=True)

    for (case, rep), variants in pairs.items():
        a, b = variants['A'], variants['B']
        changed = {c: int((a[c] != b[c]).sum()) for c in a.columns if c != 'variant'}
        check(f'{case}:{rep}:primarios_rng0', changed['prim_fnv'] == changed['rng0'] == 0)
        # Comparing every column also checks final states, bins, energies and recorded lengths.
        check(f'{case}:{rep}:registros_iguales', not any(changed.values()), {k:v for k,v in changed.items() if v})
        ya, yb = a.in_rint.to_numpy(), b.in_rint.to_numpy()
        n = [int(((ya == i) & (yb == j)).sum()) for i,j in [(0,0),(0,1),(1,0),(1,1)]]
        result['pares'].append({'caso': case, 'replica': rep, 'N':len(a), 'n00_n01_n10_n11':n})

    tslist = table(tech/'listas/sintetico/geo-train-06_v0_r9_sintetico.primarios.csv')
    expected_length, from_conduit, from_ellipsoid = straight_lengths(tslist, geometry, details=True)
    result['sinteticos'] = []
    for var in ('A2', 'B2'):
        mu = table(tech/f'corridas/ts/{var}/geo-train-06_view0_muones.csv')
        crosses = expected_length > 2e-6
        check('TS_'+var+':clasificacion_rectas', np.array_equal(crosses, mu.crossed == 1))
        relative = np.abs(mu.loc[crosses, 'lz_m'].to_numpy()/expected_length[crosses]-1)
        check('TS_'+var+':longitudes_1pct', np.all(relative < .01))
        material_ok = np.allclose(mu.lz_m, mu.lz_a0_m+mu.lz_a1_m, atol=1e-6, rtol=0)
        if var == 'B2':
            material_ok = material_ok and (mu.lz_a0_m <= 1e-6).all()
        check('TS_'+var+':materiales', material_ok and (mu.lz_rock_m <= 1e-6).all() and (mu.lz_other_m <= 1e-6).all())
        result['sinteticos'].append({'variante':var, 'N':len(mu), 'cruzan':int(crosses.sum()),
            'error_relativo_max':float(relative.max()), 'con_LZ_en_conducto':int((mu.lz_a0_m > 1e-6).sum()),
            'material_entrada':mu.loc[crosses, 'mat_in'].value_counts().to_dict(),
            'rectas_entran_desde_conducto':int(from_conduit.sum()),
            'rectas_entran_desde_elipsoide':int(from_ellipsoid.sum())})
    # Check technical invariance directly from their raw files.
    full = tech/'tf/geo-train-06/B/2026092990/geo-train-06_view0_muones.csv'
    ref = table(full)
    for mode, folder in [('TR','tr/min'), ('TM','tm/shifted'), ('TP','tp/derivada')]:
        candidates = list((tech/('corridas/'+folder.split('/')[0])).rglob('*_muones.csv'))
        assert len(candidates) == 1, candidates
        other = table(candidates[0])
        cols = ['id','prim_fnv','rng0','rng1','detected','iel','iaz','in_rint','status','n_steps']
        start = 100 if mode == 'TP' else 0
        check(mode+':invariancia', ref.loc[start:,cols].equals(other.loc[start:,cols]))
        if mode == 'TP': check('TP:100_primarios_sustituidos', (ref.prim_fnv.iloc[:100] != other.prim_fnv.iloc[:100]).all())
    for var in ('A', 'B'):
        hists = list((tech/'corridas/tl').rglob('geo-train-06_view0_hist.csv'))
        pilot = next(p for p in hists if p.parent.name == 'pilot-'+var)
        new = next(p for p in hists if p.parent.name == var+'2')
        check('TL_'+var+':histogramas', sha(pilot) == sha(new))

    for p in (ent/'analisis/etapa1-01').glob('*.csv'):
        check('reproduccion:'+p.name, p.read_bytes() == (args.reproduccion/p.name).read_bytes())
    with np.load(ent/'analisis/etapa1-01/mapas-etapa1.npz') as a, np.load(args.reproduccion/'mapas-etapa1.npz') as b:
        check('reproduccion:mapas', set(a.files) == set(b.files) and all(np.array_equal(a[k], b[k]) for k in a.files))
    contracts = json.loads((args.reproduccion/'contratos.json').read_text(encoding='utf-8'))
    check('reproduccion:contratos', contracts['estado'] == 'OK' and not contracts['bloqueantes_fallidos'] and not contracts['no_bloqueantes_fallidos'])
    result['ok'] = all(c['ok'] for c in result['checks'])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('CONTROLES', len(result['checks']), 'FALLOS', [c['control'] for c in result['checks'] if not c['ok']])
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

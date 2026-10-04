"""Complementary count-conservation analysis of the A/B adjustment trial.

Outside the director's decision rule (evaluar_ajuste.py). Per validation image
and model (input, initial epoch-5 U-Net, A control, B regional) it computes the
relative error of total counts over the whole image and per region family
(sky, rock without anomaly, edge, anomalies), plus SSIM/PSNR with the
director's metric functions. Paired B-A differences get 95 % percentile
intervals from a two-level bootstrap (geometries, then views within each
geometry), which is descriptive and conditional on a single training run.
Reuses Store, the count inversion of evaluar_ajuste.py and the U-Net builder;
opens only the validation split. Run from the repository root:
  python analizar_cuentas.py --datos D --mascaras M --pesos best.pt \
      --control A_DIR --regional B_DIR --salida OUT
"""
import argparse
import csv
import io
import json
import os
import sys
from pathlib import Path

os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
import numpy as np
import torch

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT/'objetivo-2/herramientas'))
sys.path.insert(0, str(ROOT/'objetivo-2/implementacion/models'))
sys.path.insert(0, str(ROOT/'objetivo-2/implementacion/scripts/evaluation'))
from datos_ajuste import Store, digest, read_json  # noqa: E402
from metrics import compute_psnr, compute_ssim  # noqa: E402
from unet_generator import build_generator  # noqa: E402

FAMILIES = {0: 'cielo', 1: 'roca', 2: 'borde', 3: 'anomalias'}
N_BOOT, SEED = 10000, 20261004
INITIAL_SHA = '734bc5dc1aa4cdc16a3fa0b6de2d58da7575c5bd0b1fe342bc266283f0e8e57a'


def initial_predictions(store, keys, path, device):
    if digest(path) != INITIAL_SHA:
        raise ValueError('Pesos iniciales distintos')
    safe = [np._core.multiarray._reconstruct, np.ndarray, np.dtype, np.dtypes.UInt32DType]
    with torch.serialization.safe_globals(safe):
        c = torch.load(io.BytesIO(Path(path).read_bytes()), map_location='cpu', weights_only=True)
    net = build_generator('unet_dc_5').to(device)
    net.load_state_dict(c['generator'], strict=True)
    net.eval()
    out = []
    with torch.no_grad():
        for i in range(0, len(keys), 4):
            x, _, _, _ = store.batch([tuple(k) for k in keys[i:i+4]], device)
            out.append(net(x)[:, 0].cpu().numpy())
    return np.concatenate(out)


def to_counts(z, scale):
    z = z.astype(np.float64)
    return np.expm1(scale*z/(1-z))


def boot(diff_by_cluster, rng):
    """diff_by_cluster: {geometry: [per-view mean differences]}."""
    geos = sorted(diff_by_cluster)
    means = []
    for _ in range(N_BOOT):
        sample = []
        for g in rng.choice(geos, size=len(geos), replace=True):
            views = diff_by_cluster[g]
            sample.extend(rng.choice(views, size=len(views), replace=True))
        means.append(np.mean(sample))
    lo, hi = np.percentile(means, [2.5, 97.5])
    point = float(np.mean([v for g in geos for v in diff_by_cluster[g]]))
    return {'mean': point, 'ci95': [float(lo), float(hi)]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for n in ['datos', 'mascaras', 'pesos', 'control', 'regional', 'salida']:
        p.add_argument('--'+n, type=Path, required=True)
    a = p.parse_args()
    torch.use_deterministic_algorithms(True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    store = Store(a.datos, a.mascaras)
    keys = read_json(a.control/'indices-val.json')
    if keys != read_json(a.regional/'indices-val.json'):
        raise ValueError('Orden de predicciones diferente')
    preds = {'A': np.load(a.control/'predicciones-val.npy'),
             'B': np.load(a.regional/'predicciones-val.npy'),
             'inicial': initial_predictions(store, keys, a.pesos, device)}
    scale = store.scale
    rows = []
    for i, (gid, vi, k) in enumerate(keys):
        ref_all, low = store.load(gid)
        ref = ref_all[vi].astype(np.float64)
        lr = np.log1p(ref)
        target = (lr/(scale+lr)).astype(np.float32)
        counts = {'entrada': low[vi, k].astype(np.float64)/.05}
        li = np.log1p(counts['entrada'])
        norm = {'entrada': (li/(scale+li)).astype(np.float32)}
        for name, arr in preds.items():
            norm[name] = arr[i].astype(np.float32)
            counts[name] = to_counts(arr[i], scale)
        info = store.manifest['geometries'][gid]
        masks = store.masks[gid][vi][:len(info['names'])]
        fam_masks = {}
        for j, f in enumerate(info['families']):
            fam_masks.setdefault(FAMILIES[f], np.zeros((256, 256), bool))
            fam_masks[FAMILIES[f]] |= masks[j]
        for name, c in counts.items():
            row = {'geometry': gid, 'view': vi, 'realization': k, 'model': name,
                   'ssim': float(compute_ssim(norm[name], target)),
                   'psnr': float(compute_psnr(target, norm[name])),
                   'total_rel_error': float((c.sum()-ref.sum())/ref.sum())}
            for fam, m in fam_masks.items():
                base = ref[m].sum()
                row[f'rel_error_{fam}'] = float((c[m].sum()-base)/base) if base > 0 else float('nan')
            rows.append(row)
    a.salida.mkdir(parents=True, exist_ok=True)
    with open(a.salida/'cuentas-por-imagen.csv', 'w', newline='\n', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    metrics = ['total_rel_error'] + [f'rel_error_{x}' for x in FAMILIES.values()] + ['ssim', 'psnr']
    models = ['entrada', 'inicial', 'A', 'B']
    summary = {}
    for m in models:
        rr = [r for r in rows if r['model'] == m]
        summary[m] = {}
        for met in metrics:
            v = np.array([r[met] for r in rr if np.isfinite(r[met])])
            summary[m][met] = {'n': int(len(v)), 'mean': float(v.mean()), 'sd': float(v.std(ddof=1)),
                               'mean_abs': float(np.abs(v).mean()),
                               'p5': float(np.percentile(v, 5)), 'p95': float(np.percentile(v, 95))}
    rng = np.random.default_rng(SEED)
    diffs = {}
    by = {(r['geometry'], r['view'], r['realization'], r['model']): r for r in rows}
    for met in metrics:
        use_abs = met.startswith('total') or met.startswith('rel_error')
        clusters = {}
        for gid in sorted({k[0] for k in keys}):
            per_view = []
            for vi in sorted({k[1] for k in keys if k[0] == gid}):
                d = []
                for kk in sorted({k[2] for k in keys if k[0] == gid and k[1] == vi}):
                    xa, xb = by[(gid, vi, kk, 'A')][met], by[(gid, vi, kk, 'B')][met]
                    if np.isfinite(xa) and np.isfinite(xb):
                        d.append(abs(xb)-abs(xa) if use_abs else xb-xa)
                if d:
                    per_view.append(float(np.mean(d)))
            if per_view:
                clusters[gid] = per_view
        diffs[met] = {'statistic': '|B|-|A|' if use_abs else 'B-A', **boot(clusters, rng)}
    report = {'schema': 'oe2-ajuste-cuentas-complementario-v1', 'split': 'val', 'n_images': len(keys),
              'part_of_director_decision': False,
              'bootstrap': {'levels': ['geometry', 'view'], 'replicates': N_BOOT, 'seed': SEED,
                            'note': 'Descriptivo; una sola ejecución por rama, sin variabilidad entre entrenamientos'},
              'checkpoints': {'A': digest(a.control/'last.pt'), 'B': digest(a.regional/'last.pt'),
                              'inicial': INITIAL_SHA},
              'summary': summary, 'paired_B_minus_A': diffs}
    (a.salida/'cuentas-complementario.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'summary_abs': {m: {k: round(v['mean_abs'], 4) for k, v in summary[m].items()} for m in models},
                      'paired': diffs}, indent=1))


if __name__ == '__main__':
    main()

"""Per-image validation analysis of the OE2 pilot (descriptive, no re-selection).

Loads best.pt of both pilot runs with the director's code (DataContract,
MuographyPairs, build_generator, compute_ssim/compute_psnr), scores the 360
validation pairs for U-Net, cGAN and the unprocessed input, and reports paired
differences with 95 % intervals from a cluster bootstrap over the 18
(geometry, view) references. Only the validation split is opened; nothing is
written inside the run directories.

Usage (repository root):
  python analizar_piloto_val.py --data-root D --out-root R --output DIR
"""
import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
import numpy as np
import torch

IMPL = Path('objetivo-2/implementacion').resolve()
for sub in ('', 'scripts/analysis', 'scripts/evaluation', 'scripts/training'):
    sys.path.insert(0, str(IMPL/sub))
from metrics import compute_psnr, compute_ssim  # noqa: E402
from models import build_generator  # noqa: E402
from muography_dataset import DataContract, MuographyPairs  # noqa: E402

MANIFEST = Path('objetivo-2/evidencias/contrato-datos-v1.json')
MANIFEST_SHA = '80db70d75e5ef2c40955881a87dd46b767137c24cb72dc1aa458a71c1efd8b03'
RUNS = {'unet': 'oe2-v1-piloto-f05-unet-s2026100301',
        'cgan': 'oe2-v1-piloto-f05-cgan-s2026100301'}
N_BOOT, BOOT_SEED = 10000, 20261003


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def predict(run_dir, loader, device):
    ckpt = run_dir/'checkpoints'/'best.pt'
    payload = torch.load(ckpt, map_location='cpu', weights_only=False)
    if payload['data_manifest_sha256'] != MANIFEST_SHA:
        raise ValueError(f'{ckpt}: contrato de datos distinto')
    gen = build_generator(payload['config']['generator']).to(device)
    gen.load_state_dict(payload['generator'])
    gen.eval()
    out = []
    with torch.no_grad():
        for cond, _ in loader:
            out.append(gen(cond.to(device)).cpu().numpy()[:, 0])
    return np.concatenate(out), {'checkpoint': str(ckpt), 'sha256': sha256(ckpt),
                                 'best_epoch': payload['best_epoch'],
                                 'best_ssim': payload['best_ssim']}


def cluster_bootstrap(diff, clusters, rng):
    keys = sorted(set(clusters))
    means = np.array([diff[[c == k for c in clusters]].mean() for k in keys])
    idx = rng.integers(0, len(keys), size=(N_BOOT, len(keys)))
    boot = means[idx].mean(axis=1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {'mean': float(diff.mean()), 'ci95': [float(lo), float(hi)],
            'cluster_mean_sd': float(means.std(ddof=1)), 'n_clusters': len(keys),
            'clusters_positive': int((means > 0).sum())}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data-root', required=True)
    p.add_argument('--out-root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    torch.use_deterministic_algorithms(True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    contract = DataContract(a.data_root, str(MANIFEST), MANIFEST_SHA)
    val = MuographyPairs(contract, 'val', 0.05)
    loader = torch.utils.data.DataLoader(val, batch_size=4, shuffle=False, num_workers=0)
    x = np.stack([val[i][0][0].numpy() for i in range(len(val))])
    y = np.stack([val[i][1][0].numpy() for i in range(len(val))])
    preds, ckpts = {'input': x}, {}
    for name, run in RUNS.items():
        preds[name], ckpts[name] = predict(a.out_root/run, loader, device)
    rows = []
    for i, (gid, vi, k) in enumerate(val.index):
        row = {'i': i, 'geometry': gid, 'view': vi, 'realization': k}
        for name, img in preds.items():
            row[f'ssim_{name}'] = float(compute_ssim(img[i], y[i]))
            row[f'psnr_{name}'] = float(compute_psnr(y[i], img[i]))
        rows.append(row)
    a.output.mkdir(parents=True, exist_ok=True)
    with open(a.output/'metricas-por-imagen-val.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    clusters = [f"{r['geometry']}/v{r['view']}" for r in rows]
    rng = np.random.default_rng(BOOT_SEED)
    report = {'split': 'val', 'n_images': len(rows), 'fraction': 0.05,
              'bootstrap': {'unit': 'reference (geometry, view)', 'replicates': N_BOOT,
                            'seed': BOOT_SEED, 'interval': 'percentile 95 %'},
              'checkpoints': ckpts, 'means': {}, 'paired_differences': {}, 'by_geometry': {}}
    for metric in ('ssim', 'psnr'):
        v = {n: np.array([r[f'{metric}_{n}'] for r in rows]) for n in preds}
        report['means'][metric] = {n: cluster_bootstrap(v[n], clusters, rng) for n in v}
        report['paired_differences'][metric] = {
            'unet_minus_input': cluster_bootstrap(v['unet'] - v['input'], clusters, rng),
            'cgan_minus_input': cluster_bootstrap(v['cgan'] - v['input'], clusters, rng),
            'cgan_minus_unet': cluster_bootstrap(v['cgan'] - v['unet'], clusters, rng)}
        for gid in sorted(set(r['geometry'] for r in rows)):
            m = np.array([r['geometry'] == gid for r in rows])
            report['by_geometry'].setdefault(gid, {})[metric] = {
                n: float(v[n][m].mean()) for n in v}
    (a.output/'analisis-val.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('means', 'paired_differences')}, indent=2))


if __name__ == '__main__':
    main()

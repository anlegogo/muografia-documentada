"""Vector PDF training curves of the OE2 pilot from metrics.jsonl.

Matplotlib PGF backend compiled with pdfLaTeX: Latin Modern, decimal comma,
Paul Tol "bright" colours. Reads only the delivered records.
  python figuras_piloto.py DATOS_DIR FIGURAS_DIR
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt  # noqa: E402

matplotlib.rcParams.update({
    'pgf.texsystem': 'pdflatex',
    'pgf.rcfonts': False,
    'pgf.preamble': '\n'.join([r'\usepackage[T1]{fontenc}', r'\usepackage{lmodern}',
                               r'\usepackage{icomma}']),
    'font.family': 'serif', 'font.size': 8, 'axes.labelsize': 8,
    'legend.fontsize': 7.5, 'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5,
    'axes.formatter.use_locale': False, 'lines.linewidth': 1.0,
})
TOL = {'unet': '#4477AA', 'cgan': '#EE6677', 'input': '#BBBBBB'}
NAMES = {'unet': 'U-Net (L1)', 'cgan': 'cWGAN-GP'}
RUN = 'oe2-v1-piloto-f05-{}-s2026100301'


def comma(ax):
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_formatter(matplotlib.ticker.FuncFormatter(
            lambda v, _: f'{v:g}'.replace('.', '{,}')))


def load(datos, m):
    run = Path(datos)/RUN.format(m)
    rows = [json.loads(x) for x in (run/'metrics.jsonl').read_text().splitlines()]
    base = json.loads((run/'baseline-entrada.json').read_text())
    summ = json.loads((run/'summary.json').read_text())
    return rows, base, summ


def main(datos, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    data = {m: load(datos, m) for m in NAMES}
    w = 15 / 2.54
    fig, axes = plt.subplots(1, 2, figsize=(w, 0.4 * w))
    for key, ax, label, base_key in (('val_ssim', axes[0], 'SSIM de validación', 'ssim_mean'),
                                     ('val_psnr', axes[1], 'PSNR de validación (dB)', 'psnr_mean')):
        for m, (rows, base, summ) in data.items():
            ep = [r['epoch'] for r in rows]
            ax.plot(ep, [r[key] for r in rows], color=TOL[m], label=NAMES[m])
            best = summ['best_epoch']
            ax.plot([best], [rows[best - 1][key]], 'o', color=TOL[m], ms=3)
        ax.axhline(data['unet'][1][base_key], color=TOL['input'], ls='--',
                   label='Entrada sin red')
        ax.set_xlabel('Época')
        ax.set_ylabel(label)
        comma(ax)
    axes[0].legend(frameon=False, loc='lower right')
    fig.tight_layout()
    fig.savefig(out/'curvas-validacion.pdf')
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(w, 0.4 * w))
    for m, (rows, _, _) in data.items():
        axes[0].plot([r['epoch'] for r in rows], [r['l1'] for r in rows], color=TOL[m],
                     label=NAMES[m])
    axes[0].set_xlabel('Época')
    axes[0].set_ylabel('Pérdida L1 media de entrenamiento')
    axes[0].legend(frameon=False)
    rows = data['cgan'][0]
    ep = [r['epoch'] for r in rows]
    axes[1].plot(ep, [r['w_est'] for r in rows], color=TOL['cgan'], label='Estimación de Wasserstein')
    axes[1].plot(ep, [r['gp'] for r in rows], color='#228833', label='Penalización de gradiente')
    axes[1].set_xlabel('Época')
    axes[1].set_ylabel('Términos del crítico (cWGAN-GP)')
    axes[1].legend(frameon=False)
    for ax in axes:
        comma(ax)
    fig.tight_layout()
    fig.savefig(out/'curvas-perdidas.pdf')
    plt.close(fig)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

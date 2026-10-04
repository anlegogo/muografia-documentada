"""Vector PDF figures of the A/B count-adjustment trial.

Matplotlib PGF backend compiled with pdfLaTeX: Latin Modern, decimal comma,
Paul Tol "bright" colours. Reads only delivered files:
  DATOS/piloto/{A,B}/history.json, DATOS/comparacion-piloto.json,
  DATOS/analisis-complementario/cuentas-por-imagen.csv
  python figuras_ajuste.py DATOS FIGURAS
"""
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

matplotlib.rcParams.update({
    'pgf.texsystem': 'pdflatex', 'pgf.rcfonts': False,
    'pgf.preamble': '\n'.join([r'\usepackage[T1]{fontenc}', r'\usepackage{lmodern}',
                               r'\usepackage{icomma}']),
    'font.family': 'serif', 'font.size': 8, 'axes.labelsize': 8, 'legend.fontsize': 7.5,
    'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'lines.linewidth': 1.0,
})
COLOR = {'entrada': '#BBBBBB', 'inicial': '#CCBB44', 'A': '#4477AA', 'B': '#EE6677'}
LABEL = {'entrada': 'Entrada sin red', 'inicial': 'U-Net inicial (época 5)',
         'A': 'A: control', 'B': 'B: ajuste regional'}
W = 15/2.54


def comma(ax, axis='both'):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:g}'.replace('.', '{,}').replace('-', '$-$'))
    if axis in ('both', 'y'):
        ax.yaxis.set_major_formatter(fmt)
    if axis in ('both', 'x'):
        ax.xaxis.set_major_formatter(fmt)


def curves(datos, out):
    hist = {m: json.loads((datos/f'piloto/{m}/history.json').read_text()) for m in 'AB'}
    fig, axes = plt.subplots(2, 2, figsize=(W, 0.62*W))
    panels = [(lambda r: r['losses']['l1'], 'Pérdida L1 de entrenamiento'),
              (lambda r: r['losses']['regional'], r'$L_{\mathrm{reg}}$ de entrenamiento'),
              (lambda r: r['validation']['ssim'], 'SSIM de validación'),
              (lambda r: r['validation']['psnr'], 'PSNR de validación (dB)')]
    for ax, (get, label) in zip(axes.ravel(), panels):
        for m, rows in hist.items():
            ax.plot([r['epoch'] for r in rows], [get(r) for r in rows], 'o-', ms=2.5,
                    color=COLOR[m], label=LABEL[m])
        ax.set_xlabel('Época adicional')
        ax.set_ylabel(label)
        ax.set_xticks(range(1, 6))
        comma(ax)
    axes[0, 0].legend(frameon=False)
    fig.tight_layout()
    fig.savefig(out/'curvas-ajuste.pdf')
    plt.close(fig)


def count_errors(datos, out):
    rows = list(csv.DictReader(open(datos/'analisis-complementario/cuentas-por-imagen.csv', encoding='utf-8')))
    models = ['entrada', 'inicial', 'A', 'B']
    metrics = [('rel_error_roca', 'Roca sin anomalía'), ('rel_error_anomalias', 'Anomalías'),
               ('rel_error_borde', 'Borde'), ('total_rel_error', 'Imagen completa')]
    fig, axes = plt.subplots(1, 4, figsize=(W, 0.42*W), sharey=False)
    for ax, (met, title) in zip(axes, metrics):
        data = [[100*float(r[met]) for r in rows if r['model'] == m and r[met] not in ('nan', '')]
                for m in models]
        bp = ax.boxplot(data, widths=0.6, showfliers=False, patch_artist=True,
                        medianprops={'color': 'black', 'linewidth': 0.8})
        for patch, m in zip(bp['boxes'], models):
            patch.set_facecolor(COLOR[m])
            patch.set_linewidth(0.6)
        ax.axhline(0, color='black', lw=0.5, ls=':')
        ax.set_xticks(range(1, 5), ['E', 'I', 'A', 'B'])
        ax.set_title(title, fontsize=8)
        comma(ax, 'y')
    axes[0].set_ylabel('Error relativo de cuentas (\\%)')
    handles = [matplotlib.patches.Patch(color=COLOR[m], label=LABEL[m]) for m in models]
    fig.legend(handles=handles, loc='lower center', ncol=4, frameon=False)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(out/'error-cuentas.pdf')
    plt.close(fig)


def metric_comparison(datos, out):
    comp = json.loads((datos/'comparacion-piloto.json').read_text())
    s = comp['summary']
    models = [m for m in ['entrada', 'A', 'B'] if m in s]
    geos = sorted(s['A']['Q_by_geometry'])
    fig, axes = plt.subplots(1, 3, figsize=(W, 0.45*W))
    x = np.arange(len(geos)+1)
    for j, m in enumerate(models):
        vals = [100*s[m]['Q_by_geometry'][g] for g in geos] + [100*s[m]['Q']]
        axes[0].plot(x+(j-1)*0.15, vals, 'o', ms=3.5, color=COLOR[m], label=LABEL[m])
    axes[0].set_xticks(x, [g.replace('geo-', '') for g in geos] + ['Q'])
    axes[0].set_ylabel(r'$Q_g$ (\%)')
    comma(axes[0], 'y')
    keys = [('sky_mae', 'Cielo'), ('edge_mae', 'Borde'), ('contrast_absolute_error', 'Contraste')]
    xx = np.arange(len(keys))
    for j, m in enumerate(models):
        axes[1].plot(xx+(j-1)*0.15, [100*(s[m][k] or np.nan) for k, _ in keys], 'o', ms=3.5, color=COLOR[m])
    axes[1].set_xticks(xx, [lbl for _, lbl in keys])
    axes[1].set_ylabel('Error (\\%)')
    comma(axes[1], 'y')
    ax2 = axes[2].twinx()
    for j, m in enumerate(models):
        axes[2].plot([0+(j-1)*0.15], [s[m]['ssim']], 'o', ms=3.5, color=COLOR[m])
        ax2.plot([1+(j-1)*0.15], [s[m]['psnr']], 's', ms=3.5, color=COLOR[m])
    axes[2].set_xticks([0, 1], ['SSIM', 'PSNR'])
    axes[2].set_ylabel('SSIM')
    ax2.set_ylabel('PSNR (dB)')
    comma(axes[2], 'y')
    comma(ax2, 'y')
    handles = [matplotlib.lines.Line2D([], [], marker='o', ls='', color=COLOR[m], label=LABEL[m]) for m in models]
    fig.legend(handles=handles, loc='lower center', ncol=3, frameon=False)
    axes[1].set_title('MAE regional y error de contraste', fontsize=8)
    axes[0].set_title('Indicador principal', fontsize=8)
    axes[2].set_title('Calidad de imagen', fontsize=8)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(out/'comparacion-metricas.pdf')
    plt.close(fig)


if __name__ == '__main__':
    datos, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    curves(datos, out)
    count_errors(datos, out)
    metric_comparison(datos, out)

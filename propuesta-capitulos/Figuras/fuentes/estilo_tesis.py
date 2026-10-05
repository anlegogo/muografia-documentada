"""Shared figure style for the whole thesis document.

One sober palette (Paul Tol "muted" plus three Tol "bright/vibrant" tones),
one meaning per colour across every figure, Latin Modern through the PGF
backend compiled with pdfLaTeX, decimal comma, vector PDF output.

Colour meanings (never reuse a colour for anything else):
  OE1 / data generation ........ C['oe1']   indigo
  OE2 / learning ............... C['oe2']   green
  OE3 / evaluation ............. C['oe3']   wine
  sky region ................... C['cielo'] cyan
  rock without anomaly ......... C['roca']  olive
  cone edge region ............. C['borde'] sand
  anomaly region ............... C['anomalia'] rose
  contrast control pixels ...... C['control'] teal
  input without network ........ C['entrada'] grey
  U-Net (L1) ................... C['unet']  blue
  cGAN / cWGAN-GP (all variants) C['cgan']  orange
Reserved partitions (test / generalization) are drawn in black with hatching,
never with a colour. Count images always use COUNT_CMAP with a colour bar.
Variants of one model family (C0/C1, B1-B3) differ by line style or marker,
not by colour.
"""
import os
from pathlib import Path

import matplotlib

matplotlib.use('pgf')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import ticker  # noqa: E402

C = {
    'oe1': '#332288', 'oe2': '#117733', 'oe3': '#882255',
    'cielo': '#88CCEE', 'roca': '#999933', 'borde': '#DDCC77',
    'anomalia': '#CC6677', 'control': '#44AA99',
    'entrada': '#BBBBBB', 'unet': '#4477AA', 'cgan': '#EE7733',
    'texto': '#000000', 'neutro': '#DDDDDD', 'linea': '#555555',
}
COUNT_CMAP = 'cividis'          # sequential, colour-blind safe, monotone in grey
TEXTWIDTH_CM = 15.0             # thesis text width (A4 template)
TEXTWIDTH_IN = TEXTWIDTH_CM / 2.54
# Figuras/fuentes/ -> Figuras/
FIG_DIR = Path(os.environ.get('FIGURAS_DIR', Path(__file__).resolve().parents[1]))

matplotlib.rcParams.update({
    'pgf.texsystem': 'pdflatex',
    'pgf.rcfonts': False,
    'pgf.preamble': '\n'.join([
        r'\usepackage[T1]{fontenc}', r'\usepackage[utf8]{inputenc}',
        r'\usepackage{lmodern}', r'\usepackage{icomma}', r'\usepackage{amsmath}']),
    'font.family': 'serif',
    'font.size': 8, 'axes.labelsize': 8, 'axes.titlesize': 8.5,
    'legend.fontsize': 7.5, 'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5,
    'lines.linewidth': 1.0, 'axes.linewidth': 0.6,
    'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
    'savefig.facecolor': 'white', 'figure.facecolor': 'white',
    'axes.formatter.use_locale': False,
})


def comma_formatter():
    """Decimal comma and true minus sign for numeric tick labels."""
    def fmt(v, _):
        s = f'{v:g}'.replace('.', '{,}')
        return s.replace('-', '$-$')
    return ticker.FuncFormatter(fmt)


def apply_comma(ax, axis='both'):
    if axis in ('both', 'x'):
        ax.xaxis.set_major_formatter(comma_formatter())
    if axis in ('both', 'y'):
        ax.yaxis.set_major_formatter(comma_formatter())


def figure(height_ratio=0.5, width_cm=TEXTWIDTH_CM, **kw):
    w = width_cm / 2.54
    return plt.subplots(figsize=(w, w * height_ratio), **kw)


def save(fig, name):
    """Write Figuras/<name>.pdf as vector PDF (no rasterization)."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FIG_DIR / f'{name}.pdf'
    fig.savefig(path, bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)
    return path

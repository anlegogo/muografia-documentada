"""Vector PDF writer for figures with tens of thousands of polygons.

The pgf backend of estilo_tesis exhausts pdfTeX memory on 256x256 cell meshes
(one pgf path per cell). Importing this module (AFTER estilo_tesis) switches to
real LaTeX text (usetex, Latin Modern) and the native PDF backend, so cells stay
exact vector polygons. Output goes to the same Figuras/<name>.pdf location.
"""
import matplotlib
import matplotlib.pyplot as plt

from estilo_tesis import FIG_DIR

matplotlib.rcParams.update({
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage[T1]{fontenc}\usepackage{lmodern}\usepackage{icomma}\usepackage{amsmath}',
    'font.family': 'serif',
    'pdf.fonttype': 42,
})


def save_native(fig, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FIG_DIR / f'{name}.pdf'
    fig.savefig(path, backend='pdf', bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)
    return path

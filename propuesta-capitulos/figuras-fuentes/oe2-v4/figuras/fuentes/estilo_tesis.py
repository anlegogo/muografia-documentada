"""Estilo común de las figuras de datos del libro de tesis.

Las figuras se generan con el backend PGF de Matplotlib y se compilan con
pdfLaTeX, de modo que todo el texto (rótulos, números y fórmulas) lo compone
LaTeX con la misma tipografía del documento (Latin Modern, codificación T1).
La salida es un PDF vectorial con fuentes incrustadas; los mapas de conteo o
densidad, que son datos por píxel, se incrustan a su resolución nativa sin
interpolación.

Colores: mapas científicos de Crameri (perceptualmente uniformes y aptos para
daltonismo; Crameri et al., 2020, Nat. Commun. 11, 5444).
"""
from __future__ import annotations

import matplotlib

matplotlib.use("pgf")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

CM = 1 / 2.54                 # pulgadas por centímetro
ANCHO_TEXTO_CM = 15.0         # ancho de texto de la plantilla (A4, márgenes 3,2 y 2,8 cm)


def aplicar_estilo() -> None:
    plt.rcParams.update({
        "pgf.texsystem": "pdflatex",
        "pgf.rcfonts": False,
        "pgf.preamble": "\n".join([
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{lmodern}",
            r"\usepackage{amsmath}",
            r"\usepackage{xcolor}",
        ]),
        "font.family": "serif",
        "font.size": 8.5,
        "axes.titlesize": 8.5,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "axes.linewidth": 0.5,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })


def _coma(x: float, decimales: int | None = None) -> str:
    """Número con coma decimal y signo menos tipográfico, en modo matemático."""
    if decimales is None:
        s = f"{x:g}"
    else:
        s = f"{x:.{decimales}f}"
    return "$" + s.replace("-", "-").replace(".", "{,}") + "$"


def formato_coma(decimales: int | None = None) -> FuncFormatter:
    return FuncFormatter(lambda x, _pos: _coma(x, decimales))

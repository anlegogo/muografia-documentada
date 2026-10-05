"""Matrices de conteo como celdas vectoriales y guardado en PDF con texto LaTeX.

Cada píxel se dibuja como un rectángulo con sus bordes angulares reales. Para reducir el
tamaño del PDF, en cada fila se unen los píxeles contiguos que comparten exactamente el
mismo color de la tabla del mapa (cmap.N niveles): la imagen resultante es idéntica a la
de celdas individuales con ese mapa, sigue siendo 100 % vectorial y no contiene imágenes
incrustadas ni interpolación. La barra de color también se construye con rectángulos.

El backend PGF excede la memoria de pdfTeX con cientos de miles de rectángulos; por eso
estas figuras se guardan con el backend PDF nativo y texto compuesto por LaTeX (usetex),
con Latin Modern T1, igual que el resto del libro.
"""
from __future__ import annotations

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle


def usar_latex_pdf() -> None:
    plt.rcParams.update({
        "text.usetex": True,
        "text.latex.preamble": r"\usepackage[T1]{fontenc}\usepackage{lmodern}\usepackage{amsmath}",
        "font.family": "serif",
        "pdf.fonttype": 42,
    })


def indices_color(matriz: np.ndarray, norm, n: int) -> np.ndarray:
    z = np.ma.filled(norm(matriz), 0.0)
    return np.clip((np.asarray(z) * n).astype(int), 0, n - 1)


def dibujar_celdas(ax, matriz: np.ndarray, x_bordes: np.ndarray, y_bordes: np.ndarray, cmap, norm) -> int:
    """Dibuja la matriz (fila 0 = y_bordes[0]) y devuelve el número de rectángulos."""
    n = cmap.N
    idx = indices_color(matriz, norm, n)
    colores = cmap(np.arange(n) / max(n - 1, 1))
    polis, caras = [], []
    for i in range(idx.shape[0]):
        fila = idx[i]
        cortes = np.flatnonzero(np.diff(fila)) + 1
        inicios = np.r_[0, cortes]
        finales = np.r_[cortes, fila.size]
        y0, y1 = y_bordes[i], y_bordes[i + 1]
        for a, b in zip(inicios, finales):
            x0, x1 = x_bordes[a], x_bordes[b]
            polis.append([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
            caras.append(colores[fila[a]])
    pc = PolyCollection(polis, facecolors=caras, edgecolors=caras, linewidths=0.08, antialiaseds=False)
    pc.set_rasterized(False)
    ax.add_collection(pc)
    ax.set_xlim(x_bordes[0], x_bordes[-1])
    ax.set_ylim(min(y_bordes[0], y_bordes[-1]), max(y_bordes[0], y_bordes[-1]))
    return len(polis)


def barra_vectorial(fig, ejes, cmap, norm, etiqueta: str, **kw):
    """Barra de color con rectángulos vectoriales (sin degradado raster)."""
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, ax=ejes, **kw)
    if cb.solids is not None:
        cb.solids.remove()
    bordes = norm.inverse(np.linspace(0, 1, cmap.N + 1))
    vertical = kw.get("orientation", "vertical") == "vertical"
    for k in range(cmap.N):
        c = cmap(k / max(cmap.N - 1, 1))
        a, b = float(bordes[k]), float(bordes[k + 1])
        r = Rectangle((0, a), 1, b - a) if vertical else Rectangle((a, 0), b - a, 1)
        r.set_facecolor(c); r.set_edgecolor(c); r.set_linewidth(0.15)
        cb.ax.add_patch(r)
    cb.set_label(etiqueta)
    cb.outline.set_linewidth(0.4)
    return cb

"""res_06 — Comparación de referencia, entrada y modelos originales en casos fijados por índice.

Recupera la composición de fig4-7_comparacion_fija sin cambiar la selección: filas
geo-test-01, geo-test-02, geo-test-03 y geo-gen-01 (separada visualmente); columnas
referencia, entrada al 5 %, U-Net y cGAN; vista 0 y realización 0 en todas. Datos:
cortes_oe2.npz, extraído de las matrices auditadas de EF-01 tras comprobar las 36 huellas
del registro de procedencia de la dirección; aquí se verifica su huella antes de usarlo.
Las 256 x 256 celdas se representan sin interpolación como polígonos vectoriales (sin
imshow ni rasterized), con escala T común de 0 a 0,52, barra única y acimut y elevación en
grados tomados de las coordenadas. No se reajustan escalas por modelo.
Salida: ../res_06_comparacion_vector.pdf.
Uso: python res_06_comparacion_vector.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import cmcrameri.cm as cmc
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from estilo_res import CM, ANCHO_TEXTO_CM
from celdas_vectoriales import usar_latex_pdf, dibujar_celdas, barra_vectorial

from imagenes_oe2 import cortes, escala_comun, GEOS  # noqa: E402  (verifica la huella de cortes_oe2.npz)

SALIDA = Path(__file__).resolve().parent.parent / "res_06_comparacion_vector.pdf"
COLUMNAS = [("referencia", "Referencia"), ("entrada", r"Entrada, $f=0{,}05$"),
            ("unet_original", "U-Net"), ("cgan_original", "cGAN")]


def main() -> None:
    d = cortes()
    vmax = escala_comun(d)
    assert abs(vmax - 0.52) < 1e-12, vmax
    norm = Normalize(vmin=0.0, vmax=vmax)
    cmap = cmc.batlow

    usar_latex_pdf()
    plt.rcParams.update({"font.size": 8, "axes.labelsize": 7.5, "xtick.labelsize": 6.8, "ytick.labelsize": 6.8,
                         "axes.linewidth": 0.5})
    fig = plt.figure(figsize=(ANCHO_TEXTO_CM * CM, 12.6 * CM))
    gs = fig.add_gridspec(5, 4, height_ratios=[1, 1, 1, 0.16, 1], wspace=0.06, hspace=0.12,
                          left=0.12, right=0.88, top=0.95, bottom=0.08)
    filas = [0, 1, 2, 4]
    ejes = np.empty((4, 4), dtype=object)
    total = 0
    for i, g in enumerate(GEOS):
        x0, x1, y0, y1 = d[g]["extent"]
        for j, (m, titulo) in enumerate(COLUMNAS):
            ax = fig.add_subplot(gs[filas[i], j])
            ejes[i, j] = ax
            img = d[g]["img"][m]
            az = np.linspace(x0, x1, img.shape[1] + 1)
            el = np.linspace(y0, y1, img.shape[0] + 1)
            total += dibujar_celdas(ax, img, az, el, cmap, norm)
            ax.set_aspect("equal")
            ax.set_xticks([-20, 0, 20]); ax.set_yticks([10, 25, 40])
            if i == 0:
                ax.set_title(titulo, fontsize=7.5, pad=3)
            if j == 0:
                ax.set_ylabel(f"{g}\n" + r"Elevaci\'on ($^{\circ}$)", fontsize=6.8)
            else:
                ax.set_yticklabels([])
            if i == 3:
                ax.set_xlabel(r"Acimut relativo ($^{\circ}$)", fontsize=6.8)
            else:
                ax.set_xticklabels([])
    fig.text(0.5, ejes[3, 0].get_position().y1 + 0.012, r"\textit{Generalizaci\'on}", ha="center", fontsize=7.2)
    fig.text(0.5, ejes[0, 0].get_position().y1 + 0.035, r"\textit{Prueba}", ha="center", fontsize=7.2) if False else None
    cax = fig.add_axes([0.9, 0.08, 0.018, 0.87])
    barra = barra_vectorial(fig, None, cmap, norm, r"$T(C)$, escala com\'un", cax=cax, orientation="vertical")
    barra.set_ticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    barra.ax.set_yticklabels([f"{t:.1f}".replace(".", "{,}") for t in [0, 0.1, 0.2, 0.3, 0.4, 0.5]])
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pdf")
    print("escrito", SALIDA, "| rectángulos:", total, "| escala:", vmax)


if __name__ == "__main__":
    main()

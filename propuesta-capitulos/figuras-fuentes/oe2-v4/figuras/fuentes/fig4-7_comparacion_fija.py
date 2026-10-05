"""Figura — Comparación fija de imágenes en las cuatro geometrías reservadas.

Entrada: cortes_oe2.npz (verificado; ver imagenes_oe2.py). Regla de selección de
la dirección (informe del OE2, revisión 166be6f): vista 0 y realización 0 de cada
geometría, fijadas por índice. Columnas: referencia, entrada al 5 %, U-Net y
cGAN originales, todas en el dominio normalizado T(c) con una escala común a los
dieciséis paneles (máximo de T entre paneles; ver escala_comun).
Salida: pdf/fig4-7_comparacion_fija.pdf (ejes, rótulos y barra de color
vectoriales; las matrices de 256 x 256 se incrustan a resolución nativa, sin
interpolación).
Uso: python fig4-7_comparacion_fija.py
"""
from __future__ import annotations

from pathlib import Path

import cmcrameri.cm as cmc
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from estilo_tesis import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from imagenes_oe2 import cortes, escala_comun, GEOS, ROTULO

SALIDA = Path(__file__).resolve().parent.parent / "pdf" / "fig4-7_comparacion_fija.pdf"
COLUMNAS = ["referencia", "entrada", "unet_original", "cgan_original"]


def main() -> None:
    d = cortes()
    aplicar_estilo()
    vmax = escala_comun(d)
    print("escala común de T:", vmax)
    norma = Normalize(vmin=0.0, vmax=vmax)
    fig, ejes = plt.subplots(4, 4, figsize=(ANCHO_TEXTO_CM * CM, 11.6 * CM), sharex=True, sharey=True,
                             gridspec_kw={"wspace": 0.06, "hspace": 0.10})
    for i, g in enumerate(GEOS):
        for j, m in enumerate(COLUMNAS):
            ax = ejes[i, j]
            im = ax.imshow(d[g]["img"][m], origin="lower", extent=d[g]["extent"], cmap=cmc.batlow,
                           norm=norma, interpolation="none", aspect="equal")
            if i == 0:
                ax.set_title(ROTULO[m], pad=3)
            if j == 0:
                ax.set_ylabel(f"{g}\n" + r"Elevación ($^{\circ}$)", fontsize=7.5)
            if i == 3:
                ax.set_xlabel(r"Acimut relativo ($^{\circ}$)", fontsize=7.5)
            ax.set_xticks([-20, 0, 20])
            ax.set_yticks([10, 25, 40])
            ax.xaxis.set_major_formatter(formato_coma())
            ax.yaxis.set_major_formatter(formato_coma())
    cb = fig.colorbar(im, ax=ejes, orientation="vertical", fraction=0.025, pad=0.015)
    cb.set_label(r"$T(C)$, escala común")
    cb.ax.yaxis.set_major_formatter(formato_coma(1))
    cb.outline.set_linewidth(0.4)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()

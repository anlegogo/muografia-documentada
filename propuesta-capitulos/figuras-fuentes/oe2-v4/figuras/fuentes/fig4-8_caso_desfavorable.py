"""Figura — Caso desfavorable: imágenes y residuos de todos los modelos congelados.

Entradas: cortes_oe2.npz (verificado; ver imagenes_oe2.py) y los resultados C2
(datos_oe2.py). Regla de la dirección (informe del OE2, revisión 166be6f): la
geometría con mayor Q de la cGAN original entre las cuatro reservadas, con la
vista 0 y la realización 0 fijas; se muestran la entrada y las ocho redes, sin
seleccionar semillas. Filas 1-2: imágenes en T(c), con la escala común de la comparación fija; filas 3-4:
residuos (método menos referencia) en T(c), con escala común y simétrica igual
al máximo absoluto entre los nueve métodos.
Salida: pdf/fig4-8_caso_desfavorable.pdf (ejes y barras vectoriales; matrices a
resolución nativa, sin interpolación).
Uso: python fig4-8_caso_desfavorable.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import cmcrameri.cm as cmc
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from estilo_tesis import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from imagenes_oe2 import cortes, escala_comun, GEOS, MODELOS, ROTULO
from datos_oe2 import resultados_c2

SALIDA = Path(__file__).resolve().parent.parent / "pdf" / "fig4-8_caso_desfavorable.pdf"


def main() -> None:
    s = resultados_c2()["summary"]
    q = {g: s["generalization" if g == "geo-gen-01" else "test"]["cgan_original"]["by_geometry"][g]["Q"] for g in GEOS}
    peor = max(GEOS, key=q.get)
    todos = cortes()
    vmax = escala_comun(todos)
    d = todos[peor]
    img, ext = d["img"], d["extent"]
    metodos = ["entrada"] + MODELOS
    lim = max(float(np.max(np.abs(img[m] - img["referencia"]))) for m in metodos)
    print(f"geometría: {peor}; Q cGAN = {100 * q[peor]:.3f} %; límite de residuo = {lim:.6f}")

    aplicar_estilo()
    fig, ejes = plt.subplots(4, 5, figsize=(ANCHO_TEXTO_CM * CM, 11.0 * CM), sharex=True, sharey=True,
                             gridspec_kw={"wspace": 0.06, "hspace": 0.22})
    paneles_img = ["referencia"] + metodos            # 10 paneles de imagen
    for k, m in enumerate(paneles_img):
        ax = ejes[k // 5, k % 5]
        im1 = ax.imshow(img[m], origin="lower", extent=ext, cmap=cmc.batlow, norm=Normalize(0.0, vmax),
                        interpolation="none", aspect="equal")
        ax.set_title(ROTULO[m], pad=2, fontsize=7.5)
    for k, m in enumerate(metodos):                   # 9 paneles de residuo
        pos = k + 1
        ax = ejes[2 + pos // 5, pos % 5]
        im2 = ax.imshow(img[m] - img["referencia"], origin="lower", extent=ext, cmap=cmc.vik,
                        norm=Normalize(-lim, lim), interpolation="none", aspect="equal")
        ax.set_title(ROTULO[m], pad=2, fontsize=7.5)
    ejes[2, 0].axis("off")
    for ax in ejes.flat:
        ax.set_xticks([-20, 0, 20])
        ax.set_yticks([10, 25, 40])
        ax.xaxis.set_major_formatter(formato_coma())
        ax.yaxis.set_major_formatter(formato_coma())
        ax.tick_params(labelsize=6.5)
    for i in range(4):
        ejes[i, 0].set_ylabel(r"Elev.~($^{\circ}$)", fontsize=7)
    ejes[2, 1].set_ylabel(r"Elev.~($^{\circ}$)", fontsize=7)
    ejes[2, 1].tick_params(labelleft=True)
    for j in range(5):
        ejes[3, j].set_xlabel(r"Acimut ($^{\circ}$)", fontsize=7)
    cb1 = fig.colorbar(im1, ax=ejes[:2, :], orientation="vertical", fraction=0.025, pad=0.015)
    cb1.set_label(r"$T(C)$", fontsize=7.5)
    cb1.ax.yaxis.set_major_formatter(formato_coma(1))
    cb2 = fig.colorbar(im2, ax=ejes[2:, :], orientation="vertical", fraction=0.025, pad=0.015)
    cb2.set_label(r"Residuo en $T(C)$", fontsize=7.5)
    cb2.ax.yaxis.set_major_formatter(formato_coma(2))
    for cb in (cb1, cb2):
        cb.outline.set_linewidth(0.4)
        cb.ax.tick_params(labelsize=6.5)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()

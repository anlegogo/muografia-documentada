"""Figura 3.4 — Referencia y realizaciones de menor conteo de una vista.

Entrada: datos/geo-train-08_view0_pairs.npz, verificado por huella de contenido
contra huellas-contenido.json de la campaña de 114 vistas. Se muestran la
referencia y la primera realización (k = 1) de cada fracción, en la escala
común log(1 + C), sin renormalizar por la fracción.
Salida: pdf/fig3-4_ejemplo_pares.pdf (vectorial; las matrices de conteo se
incrustan a su resolución nativa de 256 x 256 píxeles, sin interpolación).
Uso: python fig3-4_ejemplo_pares.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import cmcrameri.cm as cmc

from estilo_tesis import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from datos_campana import pares, orientar

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

SALIDA = Path(__file__).resolve().parent.parent / "pdf" / "fig3-4_ejemplo_pares.pdf"
REALIZACION = 0                      # índice base cero (k = 1 en el texto)


def main() -> None:
    d = pares("geo-train-08_view0_pairs.npz")
    el = d["el_edges_deg"]
    ref = orientar(d["counts_ref"].astype(float), el)
    low = [orientar(d["low_counts"][i, REALIZACION].astype(float), el) for i in range(4)]
    fracciones = [float(f) for f in d["fractions"]]
    assert ref[-20:].mean() > ref[:20].mean(), "orientación de filas inesperada"
    assert all((l <= ref).all() for l in low), "conteo reducido mayor que la referencia"

    aplicar_estilo()
    norma = Normalize(vmin=0.0, vmax=np.log1p(ref.max()))
    paneles = [(ref, "Referencia")] + [
        (low[i], rf"$f={f:.2f}$".replace(".", "{,}")) for i, f in enumerate(fracciones)]

    fig, ejes = plt.subplots(1, 5, figsize=(ANCHO_TEXTO_CM * CM, 4.2 * CM),
                             sharey=True, gridspec_kw={"wspace": 0.08})
    extent = (float(d["az_edges_deg"][0]), float(d["az_edges_deg"][-1]), float(min(el)), float(max(el)))
    for ax, (img, titulo) in zip(ejes, paneles):
        im = ax.imshow(np.log1p(img), origin="lower", extent=extent, cmap=cmc.batlow,
                       norm=norma, interpolation="none", aspect="equal")
        ax.set_title(titulo, pad=3)
        ax.set_xticks([-20, 0, 20])
        ax.set_yticks([2, 20, 40])
        ax.xaxis.set_major_formatter(formato_coma())
        ax.yaxis.set_major_formatter(formato_coma())
    ejes[0].set_ylabel(r"Elevación ($^{\circ}$)")
    ejes[2].set_xlabel(r"Acimut relativo ($^{\circ}$)")
    cb = fig.colorbar(im, ax=ejes, orientation="vertical", fraction=0.025, pad=0.015)
    cb.set_label(r"$\log(1+C)$")
    cb.ax.yaxis.set_major_formatter(formato_coma(0))
    cb.outline.set_linewidth(0.4)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA, "| huellas de contenido verificadas")


if __name__ == "__main__":
    main()

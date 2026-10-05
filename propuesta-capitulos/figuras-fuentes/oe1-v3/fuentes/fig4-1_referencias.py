"""Figura 4.1 — Seis referencias de la campaña de 114 vistas.

Entrada: datos/imagenes/<geometría>_view<v>.npz, cada una verificada contra
imagenes.sha256. Las vistas se eligieron para mostrar el control homogéneo,
los tres tipos de anomalía, una combinación de tres tipos y dos vistas por
debajo de la meta descriptiva de roca; no constituyen una muestra estadística.
Escala común log(1 + C), sin suavizado.
Salida: pdf/fig4-1_referencias.pdf (vectorial; matrices de 256 x 256 a su
resolución nativa, sin interpolación).
Uso: python fig4-1_referencias.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import cmcrameri.cm as cmc

from estilo_tesis import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from datos_campana import imagen, orientar

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

SALIDA = Path(__file__).resolve().parent.parent / "pdf" / "fig4-1_referencias.pdf"
VISTAS = [
    ("geo-train-01", 0, "geo-train-01, vista 0\ncontrol homogéneo"),
    ("geo-train-03", 0, "geo-train-03, vista 0\ncavidad"),
    ("geo-train-04", 0, "geo-train-04, vista 0\ncuerpo denso"),
    ("geo-train-08", 0, "geo-train-08, vista 0\ntres tipos de anomalía"),
    ("geo-train-06", 3, "geo-train-06, vista 3\nbajo la meta de roca"),
    ("geo-train-09", 5, "geo-train-09, vista 5\nbajo la meta de roca"),
]


def main() -> None:
    datos = []
    for g, v, titulo in VISTAS:
        d = imagen(g, v)
        c = orientar(d["counts_ref"].astype(float), d["el_edges_deg"])
        assert c[-20:].mean() > c[:20].mean(), f"orientación inesperada en {g} v{v}"
        datos.append((c, titulo, d))
    vmax = max(np.log1p(c.max()) for c, _, _ in datos)

    aplicar_estilo()
    norma = Normalize(vmin=0.0, vmax=vmax)
    fig, ejes = plt.subplots(2, 3, figsize=(ANCHO_TEXTO_CM * CM, 8.4 * CM),
                             sharex=True, sharey=True, gridspec_kw={"wspace": 0.08, "hspace": 0.42})
    for ax, (c, titulo, d) in zip(ejes.flat, datos):
        extent = (float(d["az_edges_deg"][0]), float(d["az_edges_deg"][-1]),
                  float(d["el_edges_deg"].min()), float(d["el_edges_deg"].max()))
        im = ax.imshow(np.log1p(c), origin="lower", extent=extent, cmap=cmc.batlow,
                       norm=norma, interpolation="none", aspect="equal")
        ax.set_title(titulo, pad=3, fontsize=7, linespacing=1.15)
        ax.set_xticks([-20, 0, 20])
        ax.set_yticks([5, 25, 45])
        ax.xaxis.set_major_formatter(formato_coma())
        ax.yaxis.set_major_formatter(formato_coma())
    for ax in ejes[:, 0]:
        ax.set_ylabel(r"Elevación ($^{\circ}$)")
    for ax in ejes[1, :]:
        ax.set_xlabel(r"Acimut relativo ($^{\circ}$)")
    cb = fig.colorbar(im, ax=ejes, orientation="vertical", fraction=0.025, pad=0.02)
    cb.set_label(r"$\log(1+C)$")
    cb.ax.yaxis.set_major_formatter(formato_coma(0))
    cb.outline.set_linewidth(0.4)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA, "| 6 huellas verificadas")


if __name__ == "__main__":
    main()

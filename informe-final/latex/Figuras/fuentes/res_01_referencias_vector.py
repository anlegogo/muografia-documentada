"""res_01 — Referencias del conjunto corregido en escenarios y vistas seleccionados.

Reexportación vectorial de 01-referencias del cierre OE1 (herramientas/figuras_cierre_oe1.py)
desde las matrices originales de la campaña de 114 vistas (f395570). Casos exactos de
datos-figuras.json -> selected_examples, verificados antes de dibujar. Dos filas por tres
columnas, acimut y elevación en grados, escala común de conteos logarítmica y lineal entre
cero y una cuenta (SymLogNorm, linthresh = 1, base 10, como la herramienta del director) y
barra única. Sin normalización de la red ni escala por panel. Se señalan las vistas bajo la
meta descriptiva de roca. Celdas vectoriales (ver celdas_vectoriales.py).
Las imágenes se verifican con imagenes.sha256 de la campaña (datos/oe1).
Salida: ../res_01_referencias_vector.pdf.
Uso: python res_01_referencias_vector.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

from estilo_res import CM, ANCHO_TEXTO_CM
from celdas_vectoriales import usar_latex_pdf, dibujar_celdas, barra_vectorial
from datos_res import datos_figuras_oe1

from datos_campana import imagen, orientar  # noqa: E402  (verifica imagenes.sha256)

SALIDA = Path(__file__).resolve().parent.parent / "res_01_referencias_vector.pdf"
ESPERADOS = ["geo-train-01_view0", "geo-train-06_view3", "geo-test-03_view5",
             "geo-gen-01_view0", "geo-val-01_view0", "geo-train-09_view1"]


def coma(x):
    return f"{x:g}".replace(".", "{,}")


def main() -> None:
    d = datos_figuras_oe1()
    casos = d["selected_examples"]
    assert casos == ESPERADOS, casos
    bajo_meta = {(m["geometry"], m["view"]) for m in d["metrics"] if m["fraction_ge100"] < 0.90}
    datos = []
    for c in casos:
        g, v = c.rsplit("_view", 1); v = int(v)
        im = imagen(g, v)
        cuentas = orientar(im["counts_ref"].astype(float), im["el_edges_deg"])
        el = np.sort(im["el_edges_deg"]); az = im["az_edges_deg"]
        assert cuentas[-20:].mean() > cuentas[:20].mean(), c
        datos.append((g, v, cuentas, az, el))
    vmax = max(x[2].max() for x in datos)
    norm = SymLogNorm(linthresh=1, vmin=0, vmax=vmax, base=10)
    cmap = plt.get_cmap("viridis")

    usar_latex_pdf()
    plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
                         "axes.linewidth": 0.5})
    fig, ejes = plt.subplots(2, 3, figsize=(ANCHO_TEXTO_CM * CM, 8.6 * CM), sharex=True, sharey=True,
                             gridspec_kw={"wspace": 0.08, "hspace": 0.42})
    total = 0
    for ax, (g, v, cuentas, az, el) in zip(ejes.flat, datos):
        total += dibujar_celdas(ax, cuentas, az, el, cmap, norm)
        nota = "\n" + r"\textit{bajo la meta de roca}" if (g, v) in bajo_meta else "\n" + r"\phantom{x}"
        ax.set_title(f"{g}, vista {v}{nota}", fontsize=6.8, pad=2, linespacing=1.1)
        ax.set_aspect("equal")
        ax.set_xticks([-20, 0, 20]); ax.set_yticks([10, 25, 40])
    for ax in ejes[:, 0]:
        ax.set_ylabel(r"Elevaci\'on ($^{\circ}$)")
    for ax in ejes[1, :]:
        ax.set_xlabel(r"Acimut relativo ($^{\circ}$)")
    ticks = [t for t in [0, 1, 10, 100, 1000] if t <= vmax]
    cb = barra_vectorial(fig, ejes, cmap, norm, "Cuentas por p\\'ixel (escala com\\'un)", orientation="vertical",
                         fraction=0.025, pad=0.015)
    cb.set_ticks(ticks); cb.ax.set_yticklabels([coma(t) for t in ticks])
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pdf")
    print("escrito", SALIDA, "| rectángulos:", total, "| vmax:", vmax, "| bajo meta:", sorted(bajo_meta & {(x[0], x[1]) for x in datos}))


if __name__ == "__main__":
    main()

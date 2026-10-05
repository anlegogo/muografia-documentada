"""Figura 4.3 — Indicador descriptivo de suficiencia de conteo en roca.

Entrada: datos/evaluacion-114-344M.json. (a) Porcentaje de las ROI de roca de
4 x 4 píxeles con al menos 100 cuentas, por geometría y vista; las vistas por
debajo de la meta del 90 % se marcan con un círculo. (b) El mismo porcentaje
frente al número de ROI de la vista, con la línea de la meta.
Salida: pdf/fig4-3_roca.pdf (vectorial; el mapa de 19 x 6 celdas es un dato
por celda y se incrusta sin interpolación).
Uso: python fig4-3_roca.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import cmcrameri.cm as cmc

from estilo_tesis import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from datos_campana import evaluacion

import matplotlib.pyplot as plt

SALIDA = Path(__file__).resolve().parent.parent / "pdf" / "fig4-3_roca.pdf"
COLOR_PARTICION = {"train": "#4477AA", "val": "#228833", "test": "#EE6677", "gen": "#AA3377"}
NOMBRE_PARTICION = {"train": "entrenamiento", "val": "validación", "test": "prueba", "gen": "generalización"}


def particion(g: str) -> str:
    return g.split("-")[1]


def main() -> None:
    vistas = evaluacion()
    geos = sorted({v["geometry"] for v in vistas},
                  key=lambda g: (["train", "val", "test", "gen"].index(particion(g)), g))
    M = np.full((len(geos), 6), np.nan)
    puntos = []
    for v in vistas:
        r = v["rock"]
        M[geos.index(v["geometry"]), v["view"]] = 100 * r["fraction_ge100"]
        puntos.append((r["roi_count"], 100 * r["fraction_ge100"], particion(v["geometry"]),
                       r["descriptive_criterion_met"]))
    roi = sum(v["rock"]["roi_count"] for v in vistas)
    ok = sum(round(v["rock"]["fraction_ge100"] * v["rock"]["roi_count"]) for v in vistas)
    cumplen = sum(p[3] for p in puntos)

    aplicar_estilo()
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(ANCHO_TEXTO_CM * CM, 8.0 * CM),
                                   gridspec_kw={"width_ratios": [1.0, 1.35], "wspace": 0.42})
    im = axa.imshow(M, cmap=cmc.batlow, vmin=88, vmax=100, aspect="auto", interpolation="none")
    for i in range(len(geos)):
        for j in range(6):
            if M[i, j] < 90:
                axa.plot(j, i, marker="o", ms=4.2, mfc="none", mec="white", mew=0.9)
    axa.set_xticks(range(6))
    axa.set_xlabel("Vista")
    axa.set_yticks(range(len(geos)))
    axa.set_yticklabels(geos, fontsize=6.5)
    axa.tick_params(length=0)
    axa.set_title("(a)", pad=3)
    cb = fig.colorbar(im, ax=axa, orientation="horizontal", fraction=0.05, pad=0.13)
    cb.set_label(r"ROI con $\geq100$ cuentas (\%)")
    cb.set_ticks([88, 90, 92, 94, 96, 98, 100]); cb.ax.xaxis.set_major_formatter(formato_coma(0))
    cb.outline.set_linewidth(0.4)

    for clave in ["train", "val", "test", "gen"]:
        xs = [p[0] for p in puntos if p[2] == clave]
        ys = [p[1] for p in puntos if p[2] == clave]
        axb.scatter(xs, ys, s=7, color=COLOR_PARTICION[clave], lw=0, label=NOMBRE_PARTICION[clave], alpha=0.85)
    fx = [p[0] for p in puntos if not p[3]]
    fy = [p[1] for p in puntos if not p[3]]
    axb.scatter(fx, fy, s=26, facecolors="none", edgecolors="black", lw=0.6, label="bajo la meta")
    axb.axhline(90, color="0.35", lw=0.6, ls="--")
    axb.set_xlabel("ROI de roca por vista")
    axb.set_ylabel(r"ROI con $\geq100$ cuentas (\%)")
    axb.yaxis.set_major_formatter(formato_coma(0))
    axb.set_ylim(88, 100.8)
    axb.set_title("(b)", pad=3)
    axb.legend(loc="upper right", fontsize=6.5, frameon=False, handletextpad=0.3, borderaxespad=0.2)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA, f"| {cumplen}/114 vistas cumplen; {ok}/{roi} ROI ({100*ok/roi:.3f} %)")


if __name__ == "__main__":
    main()

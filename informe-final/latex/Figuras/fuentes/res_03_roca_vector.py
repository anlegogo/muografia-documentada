"""res_03 — Suficiencia de conteo en roca por geometría y vista.

Fuente: datos-figuras.json del cierre OE1 (objetivo-1/figuras/cierre-2026-10-03, campaña
f395570), campos metrics[].roi, roi_ge100 y fraction_ge100. Adaptación de fig4-3_roca.
(a) Mapa de 19 geometrías por seis vistas con F, el porcentaje de ROI de roca de 4x4
píxeles con al menos 100 cuentas; cada celda es un rectángulo vectorial con su valor y se
marcan las siete vistas bajo la meta del 90 %. (b) F frente al número de ROI de la vista,
para distinguir proporción y tamaño del soporte, con el umbral explícito. No se infiere
precisión por píxel a partir de la suma en ROI. No se ejecuta simulación.
Salida: ../res_03_roca_vector.pdf (vectorial).
Uso: python res_03_roca_vector.py
"""
from __future__ import annotations

from pathlib import Path

import cmcrameri.cm as cmc
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import Rectangle

from estilo_res import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from datos_res import datos_figuras_oe1

SALIDA = Path(__file__).resolve().parent.parent / "res_03_roca_vector.pdf"
PART = {"train": "entrenamiento", "val": "validación", "test": "prueba", "gen": "generalización"}
MARC = {"train": "o", "val": "s", "test": "^", "gen": "D"}
META = 90.0


def particion(g: str) -> str:
    return g.split("-")[1]


def main() -> None:
    d = datos_figuras_oe1()
    vistas = d["metrics"]
    assert len(vistas) == 114
    roi = sum(v["roi"] for v in vistas); ok = sum(v["roi_ge100"] for v in vistas)
    assert (roi, ok) == (d["global_roi"], d["global_roi_ge100"]) == (21816, 20713)
    geos = sorted({v["geometry"] for v in vistas}, key=lambda g: (["train", "val", "test", "gen"].index(particion(g)), g))
    F = {(v["geometry"], v["view"]): 100 * v["fraction_ge100"] for v in vistas}
    exc = sorted((g, w) for (g, w), f in F.items() if f < META)
    assert len(exc) == 7, exc
    print("excepciones:", exc, f"| global {ok}/{roi} = {100 * ok / roi:.3f} %")

    aplicar_estilo()
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(ANCHO_TEXTO_CM * CM, 10.5 * CM),
                                   gridspec_kw={"width_ratios": [1.05, 1.0], "wspace": 0.38})
    norma = Normalize(vmin=88, vmax=100)
    cmap = cmc.batlow
    for i, g in enumerate(geos):
        for w in range(6):
            f = F[(g, w)]
            y = len(geos) - 1 - i
            axa.add_patch(Rectangle((w - 0.5, y - 0.5), 1, 1, facecolor=cmap(norma(f)), edgecolor="white", lw=0.4))
            claro = norma(f) < 0.55
            axa.text(w, y, f"{f:.1f}".replace(".", "{,}"), ha="center", va="center", fontsize=5.4,
                     color="white" if claro else "black")
            if f < META:
                axa.add_patch(Rectangle((w - 0.47, y - 0.47), 0.94, 0.94, facecolor="none", edgecolor="#EE6677", lw=1.1))
    axa.set_xlim(-0.5, 5.5); axa.set_ylim(-0.5, len(geos) - 0.5)
    axa.set_xticks(range(6)); axa.set_xlabel("Vista")
    axa.set_yticks(range(len(geos))); axa.set_yticklabels(geos[::-1], fontsize=6.2)
    axa.tick_params(length=0)
    for s in axa.spines.values(): s.set_visible(False)
    axa.set_title(r"(a) $F$ por geometría y vista (\%)", pad=3, fontsize=7.5)
    sm = plt.cm.ScalarMappable(norm=norma, cmap=cmap)
    cb = fig.colorbar(sm, ax=axa, orientation="horizontal", fraction=0.04, pad=0.13)
    if cb.solids is not None:       # sustituir el degradado raster por rectángulos vectoriales
        cb.solids.remove()
    for k in range(120):
        v0 = 88 + k * 0.1
        cb.ax.add_patch(Rectangle((v0, 0), 0.1, 1, facecolor=cmap(norma(v0 + 0.05)), edgecolor=cmap(norma(v0 + 0.05)),
                                  lw=0.2, transform=cb.ax.transData))
    cb.set_label(r"ROI con $\geq100$ cuentas (\%); recuadro: bajo la meta del 90\,\%", fontsize=6.5)
    cb.set_ticks([88, 90, 92, 94, 96, 98, 100]); cb.ax.xaxis.set_major_formatter(formato_coma(0))
    cb.ax.axvline(META, color="#EE6677", lw=1.0)
    cb.outline.set_linewidth(0.4)

    for clave in ["train", "val", "test", "gen"]:
        pts = [(v["roi"], 100 * v["fraction_ge100"]) for v in vistas if particion(v["geometry"]) == clave]
        axb.scatter([p[0] for p in pts], [p[1] for p in pts], s=9, marker=MARC[clave], facecolor="0.35",
                    edgecolor="none", label=PART[clave], alpha=0.85)
    ex = [(v["roi"], 100 * v["fraction_ge100"]) for v in vistas if 100 * v["fraction_ge100"] < META]
    axb.scatter([p[0] for p in ex], [p[1] for p in ex], s=34, facecolors="none", edgecolors="#EE6677", lw=0.9,
                label="bajo la meta (7 vistas)")
    axb.axhline(META, color="#EE6677", lw=0.8, ls="--")
    axb.text(axb.get_xlim()[0] if False else min(v["roi"] for v in vistas), META + 0.15, r"meta: 90\,\%", fontsize=6.2,
             color="#EE6677", va="bottom")
    axb.set_xlabel("ROI de roca por vista")
    axb.set_ylabel(r"$F$: ROI con $\geq100$ cuentas (\%)")
    axb.yaxis.set_major_formatter(formato_coma(0))
    axb.set_ylim(88, 100.8)
    axb.set_title(r"(b) Proporción frente a tamaño del soporte", pad=3, fontsize=7.5)
    axb.grid(color="0.92", lw=0.4); axb.set_axisbelow(True)
    axb.legend(loc="upper right", fontsize=6.2, frameon=True, framealpha=0.9, edgecolor="none", handletextpad=0.3)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()

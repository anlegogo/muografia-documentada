"""Figura 4.2 — Intervalos simultáneos de las 1 710 regiones de borde.

Entrada: datos/evaluacion-114-344M.json (evaluación de la campaña). Para cada
una de las 15 regiones de borde de cada vista se dibuja el intervalo de la
diferencia de respuesta frente a la región interior, en puntos porcentuales,
junto con la tolerancia de +-1 pp. Las vistas se distribuyen horizontalmente
dentro de cada región.
Salida: pdf/fig4-2_bordes.pdf (vectorial).
Uso: python fig4-2_bordes.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from estilo_tesis import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from datos_campana import evaluacion

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

SALIDA = Path(__file__).resolve().parent.parent / "pdf" / "fig4-2_bordes.pdf"
ORDEN = [f"column_{i}" for i in range(5)] + [f"column_{i}" for i in range(251, 256)] + \
        [f"row_{i}" for i in range(251, 256)]
ETIQUETA = {**{f"column_{i}": f"C{i}" for i in list(range(5)) + list(range(251, 256))},
            **{f"row_{i}": f"F{i}" for i in range(251, 256)}}
COLOR = {"col_izq": "#4477AA", "col_der": "#EE6677", "fila": "#228833"}


def main() -> None:
    vistas = evaluacion()
    assert len(vistas) == 114
    segmentos, colores, centros = [], [], []
    for j, nombre in enumerate(ORDEN):
        regiones = [r for v in vistas for r in v["borders"]["regions"] if r["name"] == nombre]
        assert len(regiones) == 114 and all(r["decision"] == "equivalent" for r in regiones)
        xs = j + np.linspace(-0.38, 0.38, len(regiones))
        clase = "fila" if nombre.startswith("row") else ("col_izq" if int(nombre.split("_")[1]) < 5 else "col_der")
        for x, r in zip(xs, regiones):
            lo, hi = r["difference_interval_pp"]
            segmentos.append([(x, lo), (x, hi)])
            colores.append(COLOR[clase])
            centros.append((x, r["difference_pp"]))
    extremo = max(max(abs(a[1]), abs(b[1])) for a, b in segmentos)

    aplicar_estilo()
    fig, ax = plt.subplots(figsize=(ANCHO_TEXTO_CM * CM, 5.6 * CM))
    ax.axhspan(-1, 1, color="0.92", zorder=0)
    ax.axhline(1, color="0.35", lw=0.6, ls="--", zorder=1)
    ax.axhline(-1, color="0.35", lw=0.6, ls="--", zorder=1)
    ax.axhline(0, color="0.55", lw=0.4, zorder=1)
    ax.add_collection(LineCollection(segmentos, colors=colores, linewidths=0.35, zorder=2))
    xc, yc = zip(*centros)
    ax.scatter(xc, yc, s=0.6, c="black", lw=0, zorder=3)
    ax.set_xlim(-0.6, len(ORDEN) - 0.4)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xticks(range(len(ORDEN)))
    ax.set_xticklabels([ETIQUETA[n] for n in ORDEN])
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.yaxis.set_major_formatter(formato_coma(1))
    ax.set_ylabel("Diferencia de respuesta (pp)")
    ax.set_xlabel("Región de borde (C: columna; F: fila)")
    ax.text(len(ORDEN) - 0.45, 1.06, "tolerancia $\\pm1$ pp", ha="right", va="bottom", fontsize=7)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA, f"| 1710 regiones equivalentes; extremo máximo {extremo:.3f} pp")


if __name__ == "__main__":
    main()

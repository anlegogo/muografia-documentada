"""Figura 4.5 — Error espacial de borde por geometría en la evaluación final.

Entrada: oe2_evidencias_ef01-c2_resultados.json (valores por geometría).
Para cada geometría reservada se muestran la entrada sin red, la U-Net y la
cGAN originales y, para cada pareja B1–B3, la variante C0 unida por un
segmento a su variante C1, de modo que la pendiente indica el efecto del
término espacial de borde.
Salida: pdf/fig4-5_borde.pdf (vectorial).
Uso: python fig4-5_borde.py
"""
from __future__ import annotations

from pathlib import Path

from estilo_res import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from datos_oe2 import resultados_c2, GEOMETRIAS

import matplotlib.pyplot as plt

SALIDA = Path(__file__).resolve().parent.parent / "res_05_borde.pdf"


def main() -> None:
    s = resultados_c2()["summary"]
    filas = [(part, g) for part in ["test", "generalization"] for g in GEOMETRIAS[part]]
    aplicar_estilo()
    fig, ax = plt.subplots(figsize=(ANCHO_TEXTO_CM * CM, 7.0 * CM))
    ancho = 0.8
    for i, (part, g) in enumerate(filas):
        val = {m: 100 * s[part][m]["by_geometry"][g]["edge_mae"] for m in s[part]}
        x0 = i - ancho / 2
        ax.scatter(x0 + 0.06, val["entrada"], marker="s", s=20, color="black", zorder=3)
        ax.scatter(x0 + 0.18, val["unet_original"], marker="D", s=18, color="#4477AA", zorder=3)
        ax.scatter(x0 + 0.30, val["cgan_original"], marker="o", s=22, color="#EE6677", zorder=3)
        for j, b in enumerate(["B1", "B2", "B3"]):
            xa, xb = x0 + 0.44 + 0.13 * j, x0 + 0.50 + 0.13 * j
            ax.plot([xa, xb], [val[f"{b}_C0"], val[f"{b}_C1"]], color="0.55", lw=0.6, zorder=2)
            ax.scatter(xa, val[f"{b}_C0"], marker="o", s=14, facecolors="none", edgecolors="#228833", lw=0.8, zorder=3)
            ax.scatter(xb, val[f"{b}_C1"], marker="^", s=16, color="#AA3377", lw=0, zorder=3)
            print(g, b, round(val[f"{b}_C0"], 2), "->", round(val[f"{b}_C1"], 2),
                  f"({100 * (val[f'{b}_C1'] / val[f'{b}_C0'] - 1):.1f} %)")
        if i == 2:
            ax.axvline(i + 0.5, color="0.6", lw=0.5, ls="--")
    ax.set_xticks(range(len(filas)))
    ax.set_xticklabels([g for _, g in filas])
    ax.set_xlim(-0.55, len(filas) - 0.45)
    ax.set_ylabel(r"Error espacial de borde (\%)")
    ax.yaxis.set_major_formatter(formato_coma(0))
    ax.grid(axis="y", color="0.88", lw=0.4)
    ax.set_axisbelow(True)
    ax.text(1.55 / 4.1, 1.02, "prueba", transform=ax.transAxes, ha="center", va="bottom")
    ax.text(3.55 / 4.1, 1.02, "generalización", transform=ax.transAxes, ha="center", va="bottom")
    manejadores = [
        plt.scatter([], [], marker="s", s=20, color="black", label="Entrada sin red"),
        plt.scatter([], [], marker="D", s=18, color="#4477AA", label="U-Net original"),
        plt.scatter([], [], marker="o", s=22, color="#EE6677", label="cGAN original"),
        plt.scatter([], [], marker="o", s=14, facecolors="none", edgecolors="#228833", lw=0.8, label="E1, C0"),
        plt.scatter([], [], marker="^", s=16, color="#AA3377", lw=0, label="E1, C1"),
    ]
    ax.legend(handles=manejadores, loc="upper center", ncol=5, frameon=False, fontsize=7,
              bbox_to_anchor=(0.5, -0.12), handletextpad=0.2, columnspacing=1.0)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()

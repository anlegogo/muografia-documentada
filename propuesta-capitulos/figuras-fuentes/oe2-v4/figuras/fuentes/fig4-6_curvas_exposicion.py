"""Figura 4.6 — Curvas descriptivas de exposición de la entrada sin red.

Entradas: oe3_evidencias_curvas-v1_curvas.json (entrada sin red al 1, 5, 10 y
50 % de los conteos) y oe2_evidencias_ef01-c2_resultados.json (las ocho redes,
evaluadas solo al 5 %). Filas: prueba y generalización; columnas: SSIM, PSNR y
Q. Las líneas discontinuas unen valores medidos como guía visual; no se usan
para interpolar factores de adquisición. Todos los símbolos de redes se ubican
en la fracción 0,05, la única evaluada para ellas.
Salida: pdf/fig4-6_curvas_exposicion.pdf (vectorial).
Uso: python fig4-6_curvas_exposicion.py
"""
from __future__ import annotations

from pathlib import Path

from estilo_tesis import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from datos_oe2 import curvas, resultados_c2

import matplotlib.pyplot as plt

SALIDA = Path(__file__).resolve().parent.parent / "pdf" / "fig4-6_curvas_exposicion.pdf"
FRACS = ["0.01", "0.05", "0.1", "0.5"]
METRICAS = [("ssim_macro", "SSIM", 1.0, 2), ("psnr_macro", "PSNR (dB)", 1.0, 0), ("Q_macro", r"$Q$ (\%)", 100.0, 0)]
TITULO = {"test": "Prueba", "generalization": "Generalización"}
RED = {"unet_original": dict(marker="D", s=16, color="#4477AA"),
       "cgan_original": dict(marker="o", s=18, color="#EE6677"),
       "C0": dict(marker="o", s=12, facecolors="none", edgecolors="#228833", lw=0.7),
       "C1": dict(marker="^", s=13, color="#AA3377", lw=0)}


def main() -> None:
    c = curvas()["curves"]
    s = resultados_c2()["summary"]
    aplicar_estilo()
    fig, ejes = plt.subplots(2, 3, figsize=(ANCHO_TEXTO_CM * CM, 9.5 * CM), sharex=True,
                             gridspec_kw={"hspace": 0.15, "wspace": 0.42})
    letras = iter("abcdef")
    for i, part in enumerate(["test", "generalization"]):
        for j, (clave, nombre, esc, dec) in enumerate(METRICAS):
            ax = ejes[i, j]
            xs = [float(f) for f in FRACS]
            ys = [esc * c[part][f][clave] for f in FRACS]
            ax.plot(xs, ys, ls="--", lw=0.6, color="0.45", zorder=1)
            ax.scatter(xs, ys, marker="s", s=16, color="black", zorder=3)
            for m, v in s[part].items():
                if m == "entrada":
                    continue
                grupo = m.split("_")[1] if m.startswith("B") else m
                ax.scatter(0.05, esc * v[clave], zorder=4, **RED[grupo])
            ax.set_xscale("log")
            ax.set_xticks(xs)
            ax.set_xticklabels([r"$1$", r"$5$", r"$10$", r"$50$"])
            ax.minorticks_off()
            ax.yaxis.set_major_formatter(formato_coma(dec))
            ax.grid(color="0.9", lw=0.4)
            ax.set_axisbelow(True)
            ax.set_title(f"({next(letras)}) {TITULO[part]}", fontsize=7.5, pad=2)
            ax.set_ylabel(nombre)
            if i == 1:
                ax.set_xlabel(r"Conteos conservados (\%)")
            print(part, clave, [round(y, 4) for y in ys])
    manejadores = [plt.scatter([], [], marker="s", s=16, color="black", label="Entrada sin red"),
                   plt.scatter([], [], label="U-Net original al 5\\,\\%", **RED["unet_original"]),
                   plt.scatter([], [], label="cGAN original al 5\\,\\%", **RED["cgan_original"]),
                   plt.scatter([], [], label="E1, C0", **RED["C0"]),
                   plt.scatter([], [], label="E1, C1", **RED["C1"])]
    fig.legend(handles=manejadores, loc="upper center", ncol=5, frameon=False,
               bbox_to_anchor=(0.5, 1.0), fontsize=7, handletextpad=0.2, columnspacing=0.9)
    fig.subplots_adjust(top=0.88)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()

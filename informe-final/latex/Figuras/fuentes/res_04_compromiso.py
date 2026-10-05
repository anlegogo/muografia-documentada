"""Figura 4.4 — Compromiso entre similitud de imagen y conservación de cuentas.

Entrada: oe2_evidencias_ef01-c2_resultados.json (EF-01 con corrección C2).
Macropromedios por partición: SSIM (fila superior) y PSNR (fila inferior)
frente al indicador regional Q, para la entrada sin red y las ocho redes.
Columnas: (a, c) prueba; (b, d) generalización.
Salida: pdf/fig4-4_compromiso.pdf (vectorial).
Uso: python fig4-4_compromiso.py
"""
from __future__ import annotations

from pathlib import Path

from estilo_res import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from datos_oe2 import resultados_c2

import matplotlib.pyplot as plt

SALIDA = Path(__file__).resolve().parent.parent / "res_04_compromiso.pdf"
ESTILO = {
    "entrada": dict(marker="s", s=22, color="black", label="Entrada sin red"),
    "unet_original": dict(marker="D", s=20, color="#4477AA", label="U-Net original"),
    "cgan_original": dict(marker="o", s=24, color="#EE6677", label="cGAN original"),
    "C0": dict(marker="o", s=16, facecolors="none", edgecolors="#228833", lw=0.8, label="E1, C0 (B1--B3)"),
    "C1": dict(marker="^", s=18, color="#AA3377", lw=0, label="E1, C1 (B1--B3)"),
}
TITULO = {"test": "prueba", "generalization": "generalización"}


def main() -> None:
    s = resultados_c2()["summary"]
    aplicar_estilo()
    fig, ejes = plt.subplots(2, 2, figsize=(ANCHO_TEXTO_CM * CM, 10.5 * CM), sharex="col",
                             gridspec_kw={"hspace": 0.12, "wspace": 0.28})
    letras = iter("abcd")
    for fila, (clave, nombre, dec) in enumerate([("ssim_macro", "SSIM", 2), ("psnr_macro", "PSNR (dB)", 0)]):
        for col, part in enumerate(["test", "generalization"]):
            ax = ejes[fila, col]
            for m, v in s[part].items():
                grupo = m.split("_")[1] if m.startswith("B") else m
                est = dict(ESTILO[grupo])
                est.pop("label")
                ax.scatter(100 * v["Q_macro"], v[clave], zorder=3, **est)
            ax.yaxis.set_major_formatter(formato_coma(dec))
            ax.xaxis.set_major_formatter(formato_coma(0))
            ax.grid(color="0.88", lw=0.4)
            ax.set_axisbelow(True)
            ax.text(0.97, 0.06, f"({next(letras)}) {TITULO[part]}", transform=ax.transAxes,
                    ha="right", va="bottom")
            if col == 0:
                ax.set_ylabel(nombre)
            if fila == 1:
                ax.set_xlabel(r"Indicador regional $Q$ (\%)")
            ax.set_xlim(-1, 29)
    manejadores = [plt.scatter([], [], **ESTILO[k]) for k in ESTILO]
    fig.legend(handles=manejadores, loc="upper center", ncol=5, frameon=False,
               bbox_to_anchor=(0.5, 1.0), fontsize=7, handletextpad=0.2, columnspacing=1.0)
    fig.subplots_adjust(top=0.90)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    for part in ["test", "generalization"]:
        for m, v in s[part].items():
            print(part, m, round(v["ssim_macro"], 4), round(v["psnr_macro"], 3), round(100 * v["Q_macro"], 3))
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()

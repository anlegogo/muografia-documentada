"""res_07 — Similitud y sesgo regional de los modelos en las cuatro fracciones.

Fuente única: sintesis_metricas.csv (revisión OE3-C1 del director, 72 filas: cuatro
fracciones, dos particiones y nueve métodos). Seis paneles: SSIM, PSNR y Q en columnas;
prueba y generalización en filas. Entrada, U-Net y cGAN con estilos distinguibles; las
seis continuaciones con líneas finas (B1-B3 por marcador, C0 discontinua y C1 continua),
sin promediar semillas. Eje horizontal logarítmico con marcas 1, 5, 10 y 50 %. Q se
convierte de fracción a porcentaje solo al representar. Las líneas unen puntos medidos
como guía visual; no interpolan factores. Todas las redes se entrenaron al 5 %.
Salida: ../res_07_multifraccion_vector.pdf (vectorial).
Uso: python res_07_multifraccion_vector.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from estilo_res import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from datos_res import sintesis

SALIDA = Path(__file__).resolve().parent.parent / "res_07_multifraccion_vector.pdf"
FRACS = [0.01, 0.05, 0.10, 0.50]
PRINC = {
    "entrada": dict(color="black", marker="s", ls="-", lw=1.1, ms=3.6, label="Entrada sin red"),
    "unet_original": dict(color="#4477AA", marker="D", ls="-", lw=1.1, ms=3.4, label="U-Net original"),
    "cgan_original": dict(color="#EE6677", marker="o", ls="-", lw=1.1, ms=3.6, label="cGAN original"),
}
MARC_PAREJA = {"B1": "^", "B2": "v", "B3": "P"}
COLOR_CONT = {"B1": "#228833", "B2": "#AA3377", "B3": "#BB7700"}
METRICAS = [("ssim_macro", "SSIM", 1.0, 2), ("psnr_macro", "PSNR (dB)", 1.0, 0), ("Q_macro", r"$Q$ (\%)", 100.0, 0)]
TITULO = {"test": "Prueba", "generalization": "Generalización"}


def main() -> None:
    filas = sintesis()
    assert len(filas) == 72, len(filas)
    v = {(float(r["fraction"]), r["split"], r["model"]): r for r in filas}
    modelos = sorted({r["model"] for r in filas})
    assert len(modelos) == 9 and sorted({float(r["fraction"]) for r in filas}) == FRACS
    aplicar_estilo()
    plt.rcParams["pgf.preamble"] += r"\AtBeginDocument{\pagestyle{empty}}"
    fig, ejes = plt.subplots(2, 3, figsize=(ANCHO_TEXTO_CM * CM, 12.0 * CM), sharex=True,
                             gridspec_kw={"hspace": 0.18, "wspace": 0.40})
    letras = iter("abcdef")
    for i, part in enumerate(["test", "generalization"]):
        for j, (clave, nombre, esc, dec) in enumerate(METRICAS):
            ax = ejes[i, j]
            ax.axvline(0.05, color="0.75", lw=0.6, ls=":", zorder=0)
            for m in modelos:
                ys = [esc * float(v[(f, part, m)][clave]) for f in FRACS]
                if m in PRINC:
                    est = dict(PRINC[m]); est.pop("label")
                    ax.plot(FRACS, ys, zorder=3, **est)
                else:
                    pareja, brazo = m.split("_")
                    ax.plot(FRACS, ys, color=COLOR_CONT[pareja], lw=0.85, ls="--" if brazo == "C0" else "-",
                            marker=MARC_PAREJA[pareja], ms=3.5, mfc="white" if brazo == "C0" else COLOR_CONT[pareja],
                            mec=COLOR_CONT[pareja], mew=0.5, zorder=2)
            ax.set_xscale("log")
            ax.set_xticks(FRACS)
            ax.set_xticklabels([r"$1$", r"$5$", r"$10$", r"$50$"])
            ax.minorticks_off()
            ax.yaxis.set_major_formatter(formato_coma(dec))
            ax.grid(color="0.92", lw=0.4)
            ax.set_axisbelow(True)
            ax.set_title(f"({next(letras)}) {TITULO[part]}", fontsize=7.5, pad=2)
            ax.set_ylabel(nombre)
            if i == 1:
                ax.set_xlabel(r"Conteos de entrada (\%)")
    ejes[0, 0].text(0.052, 0.035, "entrenamiento\nal 5\\,\\%", transform=ejes[0, 0].get_xaxis_transform(),
                    fontsize=6, color="0.45", va="bottom")
    manejadores = [Line2D([], [], **PRINC[k]) for k in PRINC]
    for pareja, mk in MARC_PAREJA.items():
        manejadores.append(Line2D([], [], color=COLOR_CONT[pareja], lw=0.85, ls="--", marker=mk, ms=3.5, mfc="white",
                                  mec=COLOR_CONT[pareja], label=f"{pareja} -- C0"))
        manejadores.append(Line2D([], [], color=COLOR_CONT[pareja], lw=0.85, ls="-", marker=mk, ms=3.5, mfc=COLOR_CONT[pareja],
                                  mec=COLOR_CONT[pareja], label=f"{pareja} -- C1"))
    fig.legend(handles=manejadores, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.01),
               fontsize=7.5, handletextpad=0.3, columnspacing=0.9, handlelength=2.2)
    fig.subplots_adjust(top=0.80, bottom=0.13)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()

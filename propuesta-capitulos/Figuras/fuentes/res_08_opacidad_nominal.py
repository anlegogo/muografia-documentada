"""res_08 — Contribuciones nominales de densidad y longitud en los controles geométricos.

Fuente: opacidad_nominal.csv (diagnóstico de opacidad nominal del director, 54 filas;
definiciones en objetivo-3/OPACIDAD_NOMINAL_Y_ALCANCE.md). Para las 48 filas elegibles
se representan, por geometría, anomalía y vista, el término de densidad
100 (rho_a - rho_r) l, el término de diferencia de longitud del control
100 rho_r (L_A - L_B) y su suma, en tres paneles alineados (g/cm2, línea de cero).
Las seis filas de geo-gen-01 anomalía 2 (sustitución por G4_AIR en el constructor) se
marcan con símbolo hueco. Las seis filas no elegibles se registran aparte, sin asignar
cero. Es opacidad nominal del catálogo, no opacidad reconstruida ni error de la red.
Salida: ../res_08_opacidad_nominal.pdf (vectorial).
Uso: python res_08_opacidad_nominal.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from estilo_res import CM, ANCHO_TEXTO_CM, aplicar_estilo
from datos_res import opacidad

SALIDA = Path(__file__).resolve().parent.parent / "res_08_opacidad_nominal.pdf"
ORDEN_GEO = ["geo-test-01", "geo-test-02", "geo-test-03", "geo-gen-01"]
TIPO = {"conduit": "conducto", "cavity": "cavidad", "dense": "cuerpo denso", "dense_body": "cuerpo denso"}
COLORES = {"delta_X_density_g_cm2": "#4477AA", "delta_X_control_length_g_cm2": "#CCBB44", "delta_X_matched_g_cm2": "#AA3377"}
PANELES = [("delta_X_density_g_cm2", r"(a) Densidad"),
           ("delta_X_control_length_g_cm2", r"(b) Longitud del control"),
           ("delta_X_matched_g_cm2", r"(c) Suma")]


def miles(x: float, _pos=None) -> str:
    s = f"{x:,.0f}".replace(",", "\\,")
    return "$" + s.replace("-", "-") + "$"


def rotulo(r: dict) -> str:
    _, idx, tipo = r["region"].split("_", 2)
    return f"{r['geometry']} · v{r['view']} · A{idx} ({TIPO.get(tipo, tipo)})"


def main() -> None:
    filas = opacidad()
    assert len(filas) == 54, len(filas)
    eleg = [r for r in filas if r["eligible_C2"] == "True"]
    no_eleg = [r for r in filas if r["eligible_C2"] != "True"]
    assert len(eleg) == 48 and len(no_eleg) == 6
    for r in eleg:
        s = float(r["delta_X_density_g_cm2"]) + float(r["delta_X_control_length_g_cm2"])
        assert abs(s - float(r["delta_X_matched_g_cm2"])) < 1e-6, r["region"]
    eleg.sort(key=lambda r: (ORDEN_GEO.index(r["geometry"]), r["region"], int(r["view"])))
    n = len(eleg)
    aire = [r["material_override_G4_AIR_in_repository"] == "True" for r in eleg]
    assert sum(aire) == 6
    print("término de densidad: min", min(float(r["delta_X_density_g_cm2"]) for r in eleg),
          "max", max(float(r["delta_X_density_g_cm2"]) for r in eleg))

    aplicar_estilo()
    fig, ejes = plt.subplots(1, 3, figsize=(ANCHO_TEXTO_CM * CM, 19.5 * CM), sharey=True,
                             gridspec_kw={"wspace": 0.10})
    ys = list(range(n))[::-1]
    for ax, (clave, titulo) in zip(ejes, PANELES):
        ax.axvline(0, color="0.35", lw=0.6)
        for y, r, a in zip(ys, eleg, aire):
            x = float(r[clave])
            ax.plot([0, x], [y, y], color=COLORES[clave], lw=0.6, alpha=0.6)
            ax.plot(x, y, marker="o", ms=3.0, mew=0.8, mec=COLORES[clave],
                    mfc="white" if a else COLORES[clave], ls="none")
        ax.set_title(titulo, fontsize=7.5, pad=3)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(miles))
        ax.tick_params(axis="x", labelsize=6.2, rotation=30)
        ax.set_xlabel(r"$\Delta X$ (g\,cm$^{-2}$)", fontsize=7)
        ax.grid(axis="x", color="0.92", lw=0.4)
        ax.set_axisbelow(True)
        # separadores entre geometrías
        for k in range(1, n):
            if eleg[k]["geometry"] != eleg[k - 1]["geometry"]:
                ax.axhline(ys[k] + 0.5, color="0.7", lw=0.5, ls="--")
    ejes[0].set_yticks(ys)
    ejes[0].set_yticklabels([rotulo(r) for r in eleg], fontsize=5.6)
    ejes[0].set_ylim(-0.8, n - 0.2)
    leyenda = [Line2D([], [], marker="o", ls="none", ms=3.0, mec="0.3", mfc="0.3", label="Fila elegible del soporte C2"),
               Line2D([], [], marker="o", ls="none", ms=3.0, mec="0.3", mfc="white",
                      label=r"geo-gen-01, anomalía 2: densidad nominal 0{,}048 g\,cm$^{-3}$; el constructor usa G4\_AIR")]
    fig.legend(handles=leyenda, loc="upper center", ncol=1, frameon=False, bbox_to_anchor=(0.6, 1.0), fontsize=6.5)
    no = "; ".join(f"{r['geometry']} v{r['view']} A{r['region'].split('_')[1]}" for r in
                   sorted(no_eleg, key=lambda r: (ORDEN_GEO.index(r["geometry"]), r["region"], int(r["view"]))))
    fig.text(0.6, 0.004, "Opacidad nominal del catálogo, no reconstruida por la red.\n"
             "Filas no elegibles, sin valor asignado: " + no, ha="center", va="bottom", fontsize=5.8)
    fig.subplots_adjust(top=0.935, bottom=0.115, left=0.30, right=0.985)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA, "| no elegibles:", no)


if __name__ == "__main__":
    main()

"""Tablas 4.x del OE2 y del OE3 generadas desde las evidencias del repositorio.

Entradas verificadas por huella (datos_oe2.py): resultados EF-01 con corrección
C2, comparación antes/después de C2 y curvas descriptivas del OE3.
Salida: ../tablas/*.tex (filas LaTeX con coma decimal) y una comprobación
impresa contra las cifras publicadas por la dirección.
Uso: python tablas_cap4.py
"""
from __future__ import annotations

import json
from pathlib import Path

from datos_oe2 import resultados_c2, curvas, DATOS, _leer

SALIDA = Path(__file__).resolve().parent.parent / "tablas"
NOMBRE = {"entrada": "Entrada sin red", "unet_original": "U-Net original", "cgan_original": "cGAN original",
          "B1_C0": "B1 -- C0", "B1_C1": "B1 -- C1", "B2_C0": "B2 -- C0", "B2_C1": "B2 -- C1",
          "B3_C0": "B3 -- C0", "B3_C1": "B3 -- C1"}
COMP = {"cgan_original_vs_entrada": "cGAN frente a entrada", "unet_original_vs_entrada": "U-Net frente a entrada",
        "cgan_original_vs_unet_original": "cGAN frente a U-Net", "B1_C1_vs_B1_C0": "B1: C1 frente a C0",
        "B2_C1_vs_B2_C0": "B2: C1 frente a C0", "B3_C1_vs_B3_C0": "B3: C1 frente a C0"}
PART = {"test": "Prueba", "generalization": "Generalización"}


def c(x: float, d: int) -> str:
    return f"{x:.{d}f}".replace(".", "{,}")


def media(v):
    return sum(v) / len(v)


def main() -> None:
    SALIDA.mkdir(exist_ok=True)
    r = resultados_c2()
    s = r["summary"]
    # ---- Tabla global EF-01 --------------------------------------------------
    filas = []
    for part in ["test", "generalization"]:
        filas.append(rf"\multicolumn{{6}}{{@{{}}l}}{{\emph{{{PART[part]}}}}} \\")
        for m, v in s[part].items():
            g = v["by_geometry"].values()
            cielo = 100 * media([x["sky_mae"] for x in g])
            borde = 100 * media([x["edge_mae"] for x in g])
            filas.append(f"{NOMBRE[m]} & {c(v['ssim_macro'], 4)} & {c(v['psnr_macro'], 3)} & "
                         f"{c(100 * v['Q_macro'], 3)} & {c(cielo, 2)} & {c(borde, 2)} \\\\")
        if part == "test":
            filas.append(r"\midrule")
    (SALIDA / "tab_ef01_global.tex").write_text("\n".join(filas) + "\n", encoding="utf-8", newline="\n")
    # ---- Tabla de contraste antes y después de C2 ----------------------------------
    comp = _leer("oe2_evidencias_ef01-c2_comparacion.json")
    print("claves comparacion:", list(comp.keys()))
    orig = json.loads((DATOS / "oe2_evaluacion-final-v1.json").read_text(encoding="utf-8"))["summary"]
    filas = []
    for m in s["test"]:
        a, b = orig["test"][m], s["test"][m]
        ga, gb = orig["generalization"][m], s["generalization"][m]
        filas.append(f"{NOMBRE[m]} & {c(a['contrast_absolute_error'], 6)} & {c(b['contrast_absolute_error'], 6)} & "
                     f"{c(ga['contrast_absolute_error'], 6)} & {c(gb['contrast_absolute_error'], 6)} \\\\")
        print("contraste", m, round(a['contrast_absolute_error'], 6), round(b['contrast_absolute_error'], 6),
              round(ga['contrast_absolute_error'], 6), round(gb['contrast_absolute_error'], 6),
              "soporte", b["common_contrasts"], gb["common_contrasts"])
        for k in ["ssim_macro", "psnr_macro", "Q_macro"]:
            assert abs(a[k] - b[k]) < 1e-12 and abs(ga[k] - gb[k]) < 1e-12, (m, k)
    (SALIDA / "tab_contraste_c2.tex").write_text("\n".join(filas) + "\n", encoding="utf-8", newline="\n")
    # ---- Tabla de comparaciones predeclaradas --------------------------------------
    met = ["ssim", "psnr", "Q", "sky_mae", "edge_mae", "contrast_absolute_error"]
    filas = []
    total = 0
    for part in ["test", "generalization"]:
        filas.append(rf"\multicolumn{{8}}{{@{{}}l}}{{\emph{{{PART[part]}}}}} \\")
        for k, v in r["predeclared_comparisons"][part].items():
            nw = v["not_worse_descriptive"]
            n = len(nw)
            celdas = " & ".join(f"{sum(nw[g][x] for g in nw)}/{n}" for x in met)
            clase = {"tradeoff_or_deterioration": "Compromiso o deterioro",
                     "no_deterioration_in_listed_metrics": "Sin deterioro",
                     "incomplete": "Incompleta"}[v["classification"]]
            filas.append(f"{COMP[k]} & {celdas} & {clase} \\\\")
            total += 1
        if part == "test":
            filas.append(r"\midrule")
    print("comparaciones:", total)
    (SALIDA / "tab_comparaciones.tex").write_text("\n".join(filas) + "\n", encoding="utf-8", newline="\n")
    # ---- Tabla de curvas OE3 -----------------------------------------------------------
    cu = curvas()
    filas = []
    for part in ["test", "generalization"]:
        filas.append(rf"\multicolumn{{5}}{{@{{}}l}}{{\emph{{{PART[part]}}}}} \\")
        for f, et in [("0.01", "1"), ("0.05", "5"), ("0.1", "10"), ("0.5", "50")]:
            v = cu["curves"][part][f]
            filas.append(f"Entrada sin red, {et}\\,\\% & {c(v['ssim_macro'], 4)} & {c(v['psnr_macro'], 3)} & "
                         f"{c(100 * v['Q_macro'], 3)} & {c(v['contrast_absolute_error'], 3)} \\\\")
        mc = cu["model_comparisons_on_common_contrast_support"][part]
        for m in ["unet_original", "cgan_original"]:
            v = s[part][m]
            filas.append(f"{NOMBRE[m]}, 5\\,\\% & {c(v['ssim_macro'], 4)} & {c(v['psnr_macro'], 3)} & "
                         f"{c(100 * v['Q_macro'], 3)} & {c(mc[m]['contrast_absolute_error'], 3)} \\\\")
        e1 = [k for k in s[part] if k.startswith("B")]
        rng = lambda key, esc=1: (min(esc * s[part][k][key] for k in e1), max(esc * s[part][k][key] for k in e1))
        a1, b1 = rng("ssim_macro"); a2, b2 = rng("psnr_macro"); a3, b3 = rng("Q_macro", 100)
        a4 = min(mc[k]["contrast_absolute_error"] for k in e1); b4 = max(mc[k]["contrast_absolute_error"] for k in e1)
        filas.append(f"E1, seis variantes, 5\\,\\% & {c(a1, 4)}--{c(b1, 4)} & {c(a2, 3)}--{c(b2, 3)} & "
                     f"{c(a3, 3)}--{c(b3, 3)} & {c(a4, 3)}--{c(b4, 3)} \\\\")
        print(part, "soporte contraste OE3:", cu["curves"][part]["0.05"]["common_contrasts"])
        if part == "test":
            filas.append(r"\midrule")
    (SALIDA / "tab_curvas.tex").write_text("\n".join(filas) + "\n", encoding="utf-8", newline="\n")
    # ---- cGAN al 5 % frente a la entrada al 10 % por geometría (dirección, d45470b) ----
    filas = []
    for part, gs in [("test", ["geo-test-01", "geo-test-02", "geo-test-03"]), ("generalization", ["geo-gen-01"])]:
        for g in gs:
            cg = s[part]["cgan_original"]["by_geometry"][g]
            e10 = cu["curves"][part]["0.1"]["by_geometry"][g]
            e50 = cu["curves"][part]["0.5"]["by_geometry"][g]
            assert cg["ssim"] > e10["ssim"] and cg["psnr"] > e10["psnr"], g
            assert cg["ssim"] < e50["ssim"] and cg["psnr"] < e50["psnr"], g
            filas.append(f"{g} & {c(cg['ssim'], 4)} & {c(e10['ssim'], 4)} & {c(cg['psnr'], 3)} & {c(e10['psnr'], 3)} \\\\")
    (SALIDA / "tab_cgan_10.tex").write_text("\n".join(filas) + "\n", encoding="utf-8", newline="\n")
    print("tabla cGAN 5 % frente a entrada 10 %: 4 geometrías verificadas")
    # ---- Cruces ----------------------------------------------------------------------------
    for part in ["test", "generalization"]:
        for m in ["unet_original", "cgan_original"]:
            print(part, m, json.dumps(cu["grid_crossings"][part][m]["psnr_macro"])[:300])
    print("listo")


if __name__ == "__main__":
    main()

"""Checks C1, C2, C4 and C5 evaluated on the SC3 control runs (jobs 30621, 30622).

Inputs: datos/sc3/controles-*/resultados/<run>/ with histograms, nominal-direction
histogram (_gen), energy-cut and nested-square histograms, metadata, command,
log and exit code, produced by controles/ejecutar_controles*.sbatch.

Criteria are the ones fixed in PUNTOS_NO_DEMOSTRADOS.md before the runs.

Outputs: resultados/controles-sc3.json, figuras/fig7-controles-plano-energia.png,
figuras/fig8-controles-inyeccion-margen.png

Usage (from the repository root):
    python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/controles_sc3.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

import comun as c

GEO = "geo-train-01"
BANDAS = [(1e4, 3e4), (3e4, 6e4), (6e4, 1e5), (1e5, 2e5), (2e5, 1e7)]
CORTES = ["0", "0.5", "1", "2", "3", "5"]
SUB = ["0.6", "50", "150", "300"]


def cargar(d: Path) -> dict:
    meta = json.loads((d / f"{GEO}_view0.meta.json").read_text(encoding="utf-8"))
    h = {"full": {"0": c.leer_histograma(d / f"{GEO}_view0_hist.csv").astype(float)}}
    for k in CORTES[1:]:
        p = d / f"{GEO}_view0_hist_ecut{k}.csv"
        if p.exists():
            h["full"][k] = c.leer_histograma(p).astype(float)
    for s in SUB:
        for k in CORTES:
            p = d / f"{GEO}_view0_hist_sub{s}_ecut{k}.csv"
            if p.exists():
                h.setdefault(s, {})[k] = c.leer_histograma(p).astype(float)
    g = d / f"{GEO}_view0_gen.csv"
    return {"dir": d, "meta": meta, "exit": int((d / "exit_code.txt").read_text().strip()), "h": h,
            "gen": c.leer_histograma(g).astype(float) if g.exists() else None}


def geometria():
    geo = c.leer_geometria(GEO)
    el = c.centros_elevacion_deg()
    b = c.bordes_azimut_v1_deg()
    az = 0.5 * (b[1:] + b[:-1])
    x = c.opacidad_vista(geo, 0, el, az)
    sil = np.array([el[x[:, j] > 0].max() if (x[:, j] > 0).any() else -99.0 for j in range(c.N_AZ)])
    cielo = (x == 0) & (el[:, None] > sil[None, :] + 1.0)
    return geo, el, az, x, cielo


def camino_edificio_m(geo, el_deg, margen=50.0):
    """Air path of the edifice-injection variant for the central azimuth (C++ formula)."""
    rc = geo["edifice"]["base_radius_m"] + margen
    hc = geo["edifice"]["height_m"] + margen
    e = math.radians(el_deg)
    fx, fz = -math.cos(e), math.sin(e)          # detector at (+D, 0) looking to -x
    ix, iz = c.DET_DISTANCE_M, c.DET_HEIGHT_M
    a, b, cc = fx * fx, 2 * ix * fx, ix * ix - rc * rc
    disc = b * b - 4 * a * cc
    t = 0.0
    if disc > 0:
        t1, t2 = (-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a)
        hi = min(t2, (hc - iz) / fz)
        if hi > max(t1, 0.0):
            t = hi
    return t + 1.0


def modelo_cielo(el_deg, camino_m, lados_half, corte, edges, cdf, tabla):
    banda = int(np.clip(np.searchsorted(edges, el_deg, side="right") - 1, 0, cdf.shape[0] - 1))
    p = c.muestras_momento(cdf[banda], sub=4)
    r = c.transporte_aire(p, camino_m * 100 * c.RHO_G4_AIR, c.RHO_G4_AIR, tabla, n_pasos=200)
    sy = r["sigma_y_m"]
    sz = sy / math.cos(math.radians(el_deg))
    vivo = r["p_decay"] * (r["t_final"] > corte)
    return [float(np.mean(vivo * c.contencion_cuadrado(sy, sz, h))) for h in lados_half]


def fraccion_anidada(num, den):
    if den <= 0:
        return float("nan"), float("nan")
    p = num / den
    return p, math.sqrt(max(p * (1 - p), 0.0) / den)


def main() -> None:
    runs = {}
    for raiz in sorted(c.DATOS_SC3.glob("controles-*/resultados")):
        for d in sorted(p for p in raiz.iterdir() if p.is_dir()):
            if (d / "exit_code.txt").exists():
                runs[d.name] = cargar(d)
    geo, el, az, x, cielo = geometria()
    roca = x >= 1e4
    filas_ok = cielo.sum(axis=1) > 0
    interior = filas_ok & (el > 20) & (el < 42)
    edges, cdf = c.leer_p_cdf()
    tabla = c.TablaRangoAire()
    r_inicio = c.DET_DISTANCE_M + geo["edifice"]["base_radius_m"] + 300.0
    salida = {"corridas": {}}
    for n, r in runs.items():
        m = r["meta"]
        salida["corridas"][n] = {
            "carpeta": c.ruta_relativa(r["dir"]), "exit": r["exit"], "eventos": m["events_transported"],
            "registrados": m["detected_in_bins"], "eficiencia": m["detected_in_bins"] / m["events_transported"],
            "sigma": c.binomial_sigma(m["detected_in_bins"], m["events_transported"]),
            "ekin_media_gev": m["mean_ekin_detected_gev"], "semilla": m["seed"], "pared_s": m["wall_seconds"],
            "controles": m.get("oe1_controles"), "sha256_hist": c.sha256(r["dir"] / f"{GEO}_view0_hist.csv"),
            "comando": (r["dir"] / "comando.txt").read_text(encoding="utf-8").strip()}

    # --- Regression: patched executables without options == production executable
    ref = runs.get("r00-produccion")
    salida["regresion_parche_inerte"] = {
        n: bool(np.array_equal(ref["h"]["full"]["0"], runs[n]["h"]["full"]["0"]))
        for n in ("r01-parche-por-defecto", "a00-parche-v2-por-defecto", "c00-parche-v3-por-defecto")
        if ref and n in runs}

    # --- C1 / C2 / C5 on nested squares
    def anidado(n, num_key, den_key):
        r = runs[n]
        filas = []
        for k in CORTES:
            hn = r["h"][num_key][k]
            hd = r["h"][den_key][k]
            bandas = []
            for lo, hi in BANDAS:
                msk = (x >= lo) & (x < hi)
                p, s = fraccion_anidada(hn[msk].sum(), hd[msk].sum())
                bandas.append({"banda": [lo, hi], "num": int(hn[msk].sum()), "den": int(hd[msk].sum()),
                               "razon": p, "sigma": s})
            pc, sc_ = fraccion_anidada(hn[cielo].sum(), hd[cielo].sum())
            pr, sr = fraccion_anidada(hn[roca].sum(), hd[roca].sum())
            filas.append({"corte_gev": float(k), "bandas": bandas, "cielo": {"razon": pc, "sigma": sc_},
                          "roca_total": {"razon": pr, "sigma": sr, "den": int(hd[roca].sum())},
                          "conteo_roca_den_sobre_sin_corte": hd[roca].sum() / r["h"][den_key]["0"][roca].sum()})
        return filas

    def criterio_c1(filas, modelo_cielo_por_corte):
        for f in filas:
            ok_roca = all(b["razon"] >= 0.98 and b["sigma"] <= 0.01 for b in f["bandas"])
            mod = modelo_cielo_por_corte[f'{f["corte_gev"]:g}']
            f["modelo_cielo_razon"] = mod
            f["cielo_vs_modelo_pp"] = 100 * (f["cielo"]["razon"] - mod)
            f["cumple_roca"] = ok_roca
            f["cumple"] = ok_roca and abs(f["cielo_vs_modelo_pp"]) <= 1.0
        cumplen = [f["corte_gev"] for f in filas if f["cumple"]]
        return min(cumplen) if cumplen else None

    def modelo_razon_cielo(camino_fn):
        filas_i = np.where(interior)[0]
        out = {}
        for k in CORTES:
            num = den = 0.0
            for i in filas_i[::4]:
                w = (runs["a01-anidado-actual"]["gen"][i] * cielo[i]).sum()
                e50, e300 = modelo_cielo(el[i], camino_fn(el[i]), [50.0, 300.0], float(k), edges, cdf, tabla)
                num += w * e50
                den += w * e300
            out[k] = num / den
        return out

    if "a01-anidado-actual" in runs:
        mod_leg = modelo_razon_cielo(lambda e: r_inicio / math.cos(math.radians(e)))
        salida["C1"] = anidado("a01-anidado-actual", "50", "300")
        salida["C1_corte_minimo_que_cumple"] = criterio_c1(salida["C1"], mod_leg)
        salida["C5"] = anidado("a01-anidado-actual", "300", "full")
        for f in salida["C5"]:
            # criterion fixed for independent runs: |r - 1| <= 2 sigma_indep
            for b in f["bandas"]:
                b["sigma_independiente"] = b["razon"] * math.sqrt(1 / max(b["num"], 1) + 1 / max(b["den"], 1))
            f["cumple_bandas_2sigma"] = all(abs(b["razon"] - 1) <= 2 * b["sigma_independiente"] for b in f["bandas"])
        full = runs["a01-anidado-actual"]["h"]
        n_ev = runs["a01-anidado-actual"]["meta"]["events_transported"]
        salida["C5_total_pp"] = {k: 100 * (full["full"][k].sum() - full["300"][k].sum()) / n_ev for k in CORTES}
        salida["serie_anidada_eficiencia"] = {s: full[s]["0"].sum() / n_ev for s in SUB} | {"600": full["full"]["0"].sum() / n_ev}
    def evaluar_c2(n, camino_fn):
        r = runs[n]
        den = (r["gen"] * cielo).sum(axis=1)
        ef = np.where(den > 0, (r["h"]["300"]["0"] * cielo).sum(axis=1) / np.maximum(den, 1), np.nan)
        mod = np.array([modelo_cielo(e, camino_fn(e), [300.0], 0.0, edges, cdf, tabla)[0]
                        if interior[i] else np.nan for i, e in enumerate(el)])
        out = {"eficiencia_cielo_filas_20_42": {"media": float(np.nanmean(ef[interior])),
                                                "min_fila": float(np.nanmin(ef[interior]))},
               "residuo_vs_modelo_pp": {"medio": float(100 * np.nanmean((ef - mod)[interior])),
                                        "max_abs": float(100 * np.nanmax(np.abs(ef - mod)[interior]))},
               "eficiencia_total": salida["corridas"][n]["eficiencia"]}
        out["cumple"] = bool(np.nanmin(ef[interior]) >= 0.97 and out["residuo_vs_modelo_pp"]["max_abs"] <= 1.0)
        return out, ef

    curvas_c2 = {}
    if "a01-anidado-actual" in runs:
        salida["C2_actual"], curvas_c2["actual"] = evaluar_c2(
            "a01-anidado-actual", lambda e: r_inicio / math.cos(math.radians(e)))
    if "a02-anidado-edificio" in runs:
        mod_edi = modelo_razon_cielo(lambda e: camino_edificio_m(geo, e))
        salida["C1_edificio"] = anidado("a02-anidado-edificio", "50", "300")
        salida["C1_edificio_corte_minimo_que_cumple"] = criterio_c1(salida["C1_edificio"], mod_edi)
        salida["C2_edificio"], curvas_c2["edificio"] = evaluar_c2("a02-anidado-edificio",
                                                                  lambda e: camino_edificio_m(geo, e))
        salida["C2_edificio"]["camino_aire_m"] = {f"{e:.1f}": camino_edificio_m(geo, e) for e in el[::51]}
    if "c01-anidado-cono" in runs:
        mod_cono = modelo_razon_cielo(lambda e: 1.0)
        salida["C1_cono"] = anidado("c01-anidado-cono", "50", "300")
        salida["C1_cono_corte_minimo_que_cumple"] = criterio_c1(salida["C1_cono"], mod_cono)
        salida["C2_cono"], curvas_c2["cono"] = evaluar_c2("c01-anidado-cono", lambda e: 1.0)
        salida["C5_cono"] = anidado("c01-anidado-cono", "300", "full")
        nc = runs["c01-anidado-cono"]
        # rock counts vs the surrogate CSDA expectation (az-edges-v1 solid angle)
        lam_hist = c.mapa_lambda_surrogado(x, el)
        lam = lam_hist / (c.fraccion_columna_historica()[None, :] * (c.N_AZ - 1)) * (c.N_AZ - 1) / c.N_AZ
        escala = nc["meta"]["events_transported"] / c.S0_V1
        salida["roca_vs_csda_cono_600m"] = [
            {"banda": [lo, hi], **{f"corte_{k}": float(nc["h"]["300"][k][(x >= lo) & (x < hi)].sum()
                                                       / (escala * lam[(x >= lo) & (x < hi)].sum())) for k in ("0", "3")}}
            for lo, hi in BANDAS]
        salida["roca_vs_csda_actual_600m"] = [
            {"banda": [lo, hi], **{f"corte_{k}": float(runs["a01-anidado-actual"]["h"]["300"][k][(x >= lo) & (x < hi)].sum()
                                                       / (escala * lam[(x >= lo) & (x < hi)].sum())) for k in ("0", "3")}}
            for lo, hi in BANDAS] if "a01-anidado-actual" in runs else None
        salida["C5_cono_total_pp"] = {k: 100 * (nc["h"]["full"][k].sum() - nc["h"]["300"][k].sum())
                                      / nc["meta"]["events_transported"] for k in CORTES}

    # --- C4: generation margin (job 30621, 600 m plane, 2e6 events)
    c4 = {}
    for n, marg in (("r05-plano-600m", 0), ("r09-margen-2deg", 2), ("r10-margen-5deg", 5),
                    ("r08-edificio-600m", 0), ("m01-edificio-margen-2deg", 2), ("m02-edificio-margen-5deg", 5),
                    ("c01-anidado-cono", 0), ("c02-cono-margen-5deg", 5)):
        if n not in runs or runs[n]["gen"] is None:
            continue
        h, g = runs[n]["h"]["full"]["0"], runs[n]["gen"]
        e_fila = (h * cielo).sum(1) / np.maximum((g * cielo).sum(1), 1)
        sel = filas_ok & (el >= 30) & (el <= 42)
        tend = np.polyfit(el[sel], e_fila[sel], 1)
        top = np.arange(c.N_EL - 5, c.N_EL)
        dev_f = e_fila[top] - np.polyval(tend, el[top])
        filas_c = (el >= 30) & (el <= 42)
        e_col = (h[filas_c] * cielo[filas_c]).sum(0) / np.maximum((g[filas_c] * cielo[filas_c]).sum(0), 1)
        ref_col = np.mean(e_col[20:-20])
        dev_c = np.concatenate([e_col[:5], e_col[-5:]]) - ref_col
        sig_f = np.sqrt(np.clip(e_fila[top] * (1 - e_fila[top]), 0, None) / np.maximum((g * cielo).sum(1)[top], 1))
        den_col = (g[filas_c] * cielo[filas_c]).sum(0)
        c4[n] = {"margen_deg": marg,
                 "inyeccion": "edificio" if "edificio" in n else ("cono" if "cono" in n else "actual"), "filas_superiores_desviacion_pp": [float(100 * v) for v in dev_f],
                 "columnas_borde_desviacion_pp": [float(100 * v) for v in dev_c],
                 "max_abs_pp": float(100 * max(np.max(np.abs(dev_f)), np.max(np.abs(dev_c)))),
                 "sigma_fila_pp": float(100 * np.median(sig_f)),
                 "sigma_columna_pp": float(100 * np.median(np.sqrt(np.clip(e_col * (1 - e_col), 0, None)
                                                                   / np.maximum(den_col, 1)))),
                 "dispersion_empirica_columnas_interiores_pp": float(100 * np.std(e_col[20:-20], ddof=1)),
                 "dispersion_empirica_filas_30_42_pp": float(100 * np.std(e_fila[sel] - np.polyval(tend, el[sel]), ddof=2)),
                 "media_desviacion_bordes_pp": float(100 * np.mean(np.concatenate([dev_f, dev_c]))),
                 "_e": e_fila, "_col": e_col}
        c4[n]["cumple"] = c4[n]["max_abs_pp"] <= 1.0
    salida["C4"] = {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")} for k, v in c4.items()}
    for iny in ("actual", "edificio", "cono"):
        ok = [v["margen_deg"] for v in c4.values() if v["cumple"] and v["inyeccion"] == iny]
        salida[f"C4_margen_minimo_que_cumple_{iny}"] = min(ok) if ok else None

    # --- production impact of the validated recipe (cone injection, E > 3 GeV, 5 deg margin)
    if {"a01-anidado-actual", "c01-anidado-cono", "c02-cono-margen-5deg"} <= runs.keys():
        b4 = c.bordes_azimut_v1_deg()
        xc = c.opacidad_vista(geo, 0, el.reshape(-1, 4).mean(1), (0.5 * (b4[1:] + b4[:-1])).reshape(-1, 4).mean(1),
                              paso_m=4.0)
        sel = (xc >= 3e4) & (xc < 1e5)
        roi = lambda h: h.reshape(64, 4, 64, 4).sum(axis=(1, 3))[sel]  # noqa: E731
        ra = roi(runs["a01-anidado-actual"]["h"]["300"]["0"])
        rb = roi(runs["c01-anidado-cono"]["h"]["300"]["3"])
        c02 = runs["c02-cono-margen-5deg"]
        salida["impacto_produccion"] = {
            "rois_geo_train_01": int(sel.sum()),
            "factor_conteo_roi_mediana": float(np.median(rb / np.maximum(ra, 1))),
            "factor_conteo_roi_suma": float(rb.sum() / ra.sum()),
            "p10_roi_actual_por_2e7": float(np.percentile(ra, 10)),
            "p10_roi_receta_por_2e7": float(np.percentile(rb, 10)),
            "fraccion_generada_en_ventana_margen_5": float(c02["gen"].sum() / c02["meta"]["events_transported"]),
            "nucleo_s_por_evento": {n: runs[n]["meta"]["wall_seconds"] * 24 / runs[n]["meta"]["events_transported"]
                                    for n in ("a01-anidado-actual", "c01-anidado-cono", "c02-cono-margen-5deg")},
        }
        imp = salida["impacto_produccion"]
        imp["nucleo_s_por_evento_en_ventana_receta"] = (imp["nucleo_s_por_evento"]["c02-cono-margen-5deg"]
                                                        / imp["fraccion_generada_en_ventana_margen_5"])

    # --- separate-plane series (job 30621)
    serie = [("r02-plano-1.2m", 1.2), ("r03-plano-100m", 100), ("r04-plano-300m", 300),
             ("r05-plano-600m", 600), ("r06-plano-1200m", 1200)]
    salida["serie_planos_separados"] = [{"lado_m": l, **{k: salida["corridas"][n][k] for k in ("eficiencia", "sigma", "registrados", "eventos", "ekin_media_gev")}}
                                        for n, l in serie if n in salida["corridas"]]

    # --------------------------------------------------------------- figures
    plt, coma = c.configurar_matplotlib()
    fig, axs = plt.subplots(1, 4, figsize=(18, 3.9), gridspec_kw={"wspace": 0.3})
    ax = axs[0]
    s = salida["serie_planos_separados"]
    ax.errorbar([p["lado_m"] for p in s], [100 * p["eficiencia"] for p in s], yerr=[100 * p["sigma"] for p in s],
                fmt="o-", label="Planos separados, 2·10⁶")
    if "serie_anidada_eficiencia" in salida:
        sa = salida["serie_anidada_eficiencia"]
        lados = [1.2, 100, 300, 600, 1200]
        vals = [sa["0.6"], sa["50"], sa["150"], sa["300"], sa["600"]]
        ax.plot(lados, [100 * v for v in vals], "s--", label="Cuadrados anidados, 2·10⁷")
    for p in s:
        if p["lado_m"] in (1.2, 100, 1200):
            ax.annotate(f'{100 * p["eficiencia"]:.2f}'.replace(".", ","), (p["lado_m"], 100 * p["eficiencia"]),
                        textcoords="offset points", xytext=(-14, -14), fontsize=7)
    ax.set_xscale("log")
    ax.set_xlabel("Lado del plano (m)")
    ax.set_ylabel("Registrados / transportados (%)")
    ax.set_title("Serie de planos repetida (semilla 777)")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ax.yaxis.set_major_formatter(coma)
    for ax, clave, titulo in [(axs[1], "C1", "C1, inyección actual"),
                              (axs[2], "C1_edificio", "C1, cilindro del edificio + 50 m"),
                              (axs[3], "C1_cono", "C1, 1 m antes de la roca")]:
        if clave not in salida:
            ax.set_visible(False)
            continue
        for f in salida[clave]:
            xs = np.arange(len(BANDAS)) + 0.07 * CORTES.index(f'{f["corte_gev"]:g}')
            ax.errorbar(xs, [b["razon"] for b in f["bandas"]], yerr=[b["sigma"] for b in f["bandas"]],
                        fmt="o-", ms=3, label=f'E > {f["corte_gev"]:g} GeV'.replace(".", ","))
        ax.axhline(1.0, color="k", lw=0.6)
        ax.axhline(0.98, color="k", lw=0.8, ls=":")
        ax.set_xticks(range(len(BANDAS)), ["10–30", "30–60", "60–100", "100–200", ">200"])
        ax.set_xlabel("Columna de roca (10³ g/cm²)")
        ax.set_ylabel("Conteo 100 m / 600 m (anidado)")
        ax.set_title(titulo)
        ax.legend(fontsize=6.5)
        ax.yaxis.set_major_formatter(coma)
    rutas = [c.guardar_figura(fig, "fig7-controles-plano-energia.png")]
    plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.9), gridspec_kw={"wspace": 0.3})
    ax = axs[0]
    for clave, et in (("actual", "Inyección actual (D + R + 300 m)"), ("edificio", "Cilindro del edificio + 50 m"),
                      ("cono", "1 m antes de la roca")):
        if clave in curvas_c2:
            ax.plot(el[filas_ok], 100 * curvas_c2[clave][filas_ok], ".", ms=3, label=et)
    ax.axhline(97, color="k", lw=0.6, ls=":")
    ax.set_xlabel("Elevación (°)")
    ax.set_ylabel("Eficiencia en cielo abierto (%)")
    ax.set_title("C2: aire previo a la inyección (cuadrado de 600 m)")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ax.yaxis.set_major_formatter(coma)
    ax = axs[1]
    for n, et, col in (("r05-plano-600m", "Actual, sin margen", "C0"), ("r10-margen-5deg", "Actual, margen 5°", "C1"),
                       ("r08-edificio-600m", "Edificio, sin margen", "C2"), ("m01-edificio-margen-2deg", "Edificio, margen 2°", "C4"),
                       ("m02-edificio-margen-5deg", "Edificio, margen 5°", "C3"),
                       ("c01-anidado-cono", "Antes de la roca, sin margen", "C5"),
                       ("c02-cono-margen-5deg", "Antes de la roca, margen 5°", "C6")):
        if n in c4:
            ax.plot(el[filas_ok], 100 * c4[n]["_e"][filas_ok], ".", ms=3, color=col, label=et)
    ax.set_xlim(30, 47.5)
    ax.set_ylim(35, 105)
    ax.set_xlabel("Elevación (°)")
    ax.set_ylabel("Eficiencia en cielo abierto (%)")
    ax.set_title("C4: margen angular de generación (plano 600 m)")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ax.yaxis.set_major_formatter(coma)
    rutas.append(c.guardar_figura(fig, "fig8-controles-inyeccion-margen.png"))
    plt.close(fig)

    salida["figuras"] = rutas
    salida["entorno"] = c.entorno()
    c.escribir_json(c.RESULTADOS / "controles-sc3.json", salida)
    resumen = {k: salida.get(k) for k in ("regresion_parche_inerte", "C1_corte_minimo_que_cumple",
                                          "C1_edificio_corte_minimo_que_cumple", "C4_margen_minimo_que_cumple_actual",
                                          "C4_margen_minimo_que_cumple_edificio",
                                          "C5_total_pp", "serie_anidada_eficiencia")}
    resumen["impacto_produccion"] = salida.get("impacto_produccion")
    for k in ("C2_actual", "C2_edificio", "C2_cono", "C1_cono_corte_minimo_que_cumple", "C4_margen_minimo_que_cumple_cono"):
        resumen[k] = salida.get(k)
    print(json.dumps(resumen, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()

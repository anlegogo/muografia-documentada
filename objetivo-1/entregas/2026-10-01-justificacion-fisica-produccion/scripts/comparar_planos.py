"""Point 1: counting-plane size comparison from the evidence preserved on SC3.

Inputs (all versioned under datos/sc3): run metadata, histograms, logs and
SLURM accounting of jobs 29467-29484 (2026-08-30). Plane sizes are assigned
from the source history (commits 81a5935, 477f193, 653f0fd), because the
metadata written by the simulator do not record the plane size.

Outputs: resultados/comparacion-planos.json, figuras/fig1-eficiencia-plano.png,
figuras/fig2-planos-por-pixel.png

Usage (from the repository root):
    python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/comparar_planos.py
"""

from __future__ import annotations

import json
import math

import numpy as np

import comun as c

GEO = "geo-train-01"

# Plane size per job, from the source history (see README, section 1).
CORRIDAS = [
    {"job": 29475, "lado_plano_m": 1.2, "commit_codigo": "81a5935",
     "muestreo": "EcoMug directo (sin tablas)", "dir": "smoke-29475"},
    {"job": 29477, "lado_plano_m": 100.0, "commit_codigo": "477f193",
     "muestreo": "EcoMug directo (sin tablas)", "dir": "smoke-29477"},
    {"job": 29480, "lado_plano_m": 100.0, "commit_codigo": "30fd245 (tablas) + 477f193 (plano)",
     "muestreo": "tablas S0 (30 d)", "dir": "smoke-29480"},
    {"job": 29484, "lado_plano_m": 600.0, "commit_codigo": "653f0fd",
     "muestreo": "tablas S0 (30 d)", "dir": "smoke-29484"},
]

# Values only reported in the source comment of 653f0fd (2M events, seed 777).
SERIE_COMENTARIO = [
    {"lado_plano_m": 100.0, "eficiencia_pct": 64.2, "job": None,
     "estado": "faltante: no hay trabajo SLURM de 2M eventos con plano de 100 m; "
               "el valor coincide con 29480 (64,16 %) al redondear"},
    {"lado_plano_m": 300.0, "eficiencia_pct": 73.07, "job": 29481,
     "estado": "faltante: srun interactivo con salida en /tmp del nodo (borrada); "
               "SLURM registra FAILED 2:0 tras 12 min; asignacion al plano de 300 m inferida"},
    {"lado_plano_m": 600.0, "eficiencia_pct": 73.81, "job": 29482,
     "estado": "faltante: srun interactivo con --out /tmp/ab600 (borrado); COMPLETED 0:0"},
]
N_SERIE = 2_000_000


def cargar_corridas() -> list[dict]:
    sacct = {int(r["JobID"]): r for r in c.leer_sacct(c.DATOS_SC3 / "sacct-serie-planos.txt")}
    filas = []
    for r in CORRIDAS:
        d = c.DATOS_SC3 / r["dir"]
        meta = json.loads((d / f"{GEO}_view0.meta.json").read_text(encoding="utf-8"))
        hist = d / f"{GEO}_view0_hist.csv"
        n, k = meta["events_transported"], meta["detected_in_bins"]
        s = sacct[r["job"]]
        filas.append({
            **{kk: vv for kk, vv in r.items() if kk != "dir"},
            "semilla": meta["seed"], "hilos": meta["threads"],
            "eventos_generados_ecomug": meta["ecomug_draws_total"],
            "eventos_transportados": n, "registrados_en_pixeles": k,
            "eficiencia": k / n, "sigma_binomial": c.binomial_sigma(k, n),
            "ekin_media_registrada_gev": meta["mean_ekin_detected_gev"],
            "pared_s": meta["wall_seconds"], "nodo_slurm": s["NodeList"],
            "estado_slurm": f'{s["State"]} {s["ExitCode"]}', "comando": s["SubmitLine"],
            "inicio": s["Start"],
            "sha256_meta": c.sha256(d / f"{GEO}_view0.meta.json"),
            "sha256_hist": c.sha256(hist), "hist": c.ruta_relativa(hist),
        })
    return filas


def energia_ganada(f100: dict, f600: dict) -> dict:
    """Mean kinetic energy of the muons gained when going from 100 m to 600 m.

    Both runs share N, seed and tables, so E_gain = (K6*E6 - K1*E1)/(K6 - K1).
    Only exact if the 100 m set is a subset of the 600 m set (same events
    scored); MT event streams are not guaranteed identical, so this is an
    estimate whose statistical uncertainty is not quantified here.
    """
    k1, e1 = f100["registrados_en_pixeles"], f100["ekin_media_registrada_gev"]
    k6, e6 = f600["registrados_en_pixeles"], f600["ekin_media_registrada_gev"]
    return {"muones_ganados": k6 - k1, "ekin_media_ganados_gev": (k6 * e6 - k1 * e1) / (k6 - k1)}


def analisis_por_pixel() -> dict:
    geo = c.leer_geometria(GEO)
    el = c.centros_elevacion_deg()
    az = c.centros_azimut_historicos_deg()
    x = c.opacidad_vista(geo, 0, el, az)
    h1 = c.leer_histograma(c.DATOS_SC3 / "smoke-29480" / f"{GEO}_view0_hist.csv").astype(float)
    h6 = c.leer_histograma(c.DATOS_SC3 / "smoke-29484" / f"{GEO}_view0_hist.csv").astype(float)
    lam = c.mapa_lambda_surrogado(x, el)
    interior = np.ones_like(x, dtype=bool)
    interior[:, [0, -1]] = False
    sil = np.array([el[x[:, j] > 0].max() if (x[:, j] > 0).any() else np.nan for j in range(c.N_AZ)])
    bajo_sil = sil[None, :] - el[:, None]
    bandas_x = [(0, 1), (1, 1e4), (1e4, 3e4), (3e4, 6e4), (6e4, 1e5), (1e5, 2e5), (2e5, 1e7)]
    por_x = []
    for lo, hi in bandas_x:
        m = (x >= lo) & (x < hi) & interior
        c1, c6, lm = h1[m].sum(), h6[m].sum(), lam[m].sum()
        por_x.append({"columna_roca_g_cm2": [lo, hi], "pixeles": int(m.sum()),
                      "conteo_100m": int(c1), "conteo_600m": int(c6),
                      "razon_100_600": c1 / c6,
                      "sigma_razon": (c1 / c6) * math.sqrt(1 / max(c1, 1) + 1 / max(c6, 1)),
                      "esperado_csda_surrogado": lm,
                      "razon_600m_vs_csda": c6 / lm, "razon_100m_vs_csda": c1 / lm})
    bandas_s = [(-99, -1), (-1, 0), (0, 0.5), (0.5, 1), (1, 2), (2, 4), (4, 99)]
    por_sil = []
    for lo, hi in bandas_s:
        m = (bajo_sil > lo) & (bajo_sil <= hi) & np.isfinite(bajo_sil) & interior
        c1, c6 = h1[m].sum(), h6[m].sum()
        por_sil.append({"grados_bajo_silueta": [lo, hi], "pixeles": int(m.sum()),
                        "conteo_100m": int(c1), "conteo_600m": int(c6), "razon_100_600": c1 / c6})
    roca = (x > 0) & interior
    return {"bandas_columna": por_x, "bandas_silueta": por_sil,
            "fraccion_conteos_en_roca_600m": h6[roca].sum() / h6[interior].sum(),
            "razon_global_roca": h1[roca].sum() / h6[roca].sum(),
            "razon_global_cielo": h1[(x == 0) & interior].sum() / h6[(x == 0) & interior].sum(),
            "_mapas": (x, h1, h6, lam, el, az)}


def figuras(filas, serie, pix) -> list[str]:
    plt, coma = c.configurar_matplotlib()
    rutas = []
    # Figure 1: efficiency vs plane side
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for f in filas:
        tabla = f["muestreo"].startswith("tablas")
        ax.errorbar(f["lado_plano_m"], 100 * f["eficiencia"], yerr=100 * f["sigma_binomial"],
                    fmt="o" if tabla else "s", color="C0" if tabla else "C1", ms=6, capsize=3)
        desplazamiento = {29477: (8, -14), 29480: (8, 4)}.get(f["job"], (6, -10))
        ax.annotate(f'{f["job"]}', (f["lado_plano_m"], 100 * f["eficiencia"]),
                    textcoords="offset points", xytext=desplazamiento, fontsize=7)
    for s in serie:
        ax.plot(s["lado_plano_m"], s["eficiencia_pct"], marker="x", color="C3", ms=8, ls="none")
    ax.plot([], [], "o", color="C0", label="Tablas S0, N = 36.174.573 (datos conservados)")
    ax.plot([], [], "s", color="C1", label="EcoMug directo, N = 100.000 (datos conservados)")
    ax.plot([], [], "x", color="C3", label="Comentario de código, N = 2·10⁶ (datos faltantes)")
    ax.set_xscale("log")
    ax.set_xlabel("Lado del plano de conteo (m)")
    ax.set_ylabel("Registrados / transportados (%)")
    ax.yaxis.set_major_formatter(coma)
    ax.xaxis.set_major_formatter(coma)
    ax.set_title(f"{GEO}, vista 0: eficiencia de registro según el plano")
    ax.legend(fontsize=7, loc="center right")
    rutas.append(c.guardar_figura(fig, "fig1-eficiencia-plano.png"))
    plt.close(fig)

    # Figure 2: per-pixel comparison 100 m vs 600 m
    x, h1, h6, lam, el, az = pix["_mapas"]
    k = 8
    a1 = h1.reshape(c.N_EL // k, k, c.N_AZ // k, k).sum(axis=(1, 3))
    a6 = h6.reshape(c.N_EL // k, k, c.N_AZ // k, k).sum(axis=(1, 3))
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(a6 > 0, a1 / a6, np.nan)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.9))
    im = axs[0].imshow(r, origin="lower", aspect="auto", cmap="viridis", vmin=0.2, vmax=1.0,
                       extent=[az[0], az[-1], el[0], el[-1]])
    axs[0].contour(az, el, x, levels=[1.0], colors="w", linewidths=0.8)
    fig.colorbar(im, ax=axs[0], label="Conteo plano 100 m / plano 600 m")
    axs[0].set_xlabel("Azimut relativo (°)")
    axs[0].set_ylabel("Elevación (°)")
    axs[0].set_title("Razón por macropíxel 8×8 (blanco: silueta)")
    axs[0].grid(False)
    b = pix["bandas_columna"]
    etiquetas = ["cielo", "<10"] + [f'{lo/1e3:g}–{hi/1e3:g}' if hi < 1e7 else f'>{lo/1e3:g}'
                                    for lo, hi in (bb["columna_roca_g_cm2"] for bb in b[2:])]
    xs = np.arange(len(b))
    axs[1].errorbar(xs, [bb["razon_100_600"] for bb in b], yerr=[bb["sigma_razon"] for bb in b],
                    fmt="o-", label="Plano 100 m / plano 600 m")
    axs[1].plot(xs, [bb["razon_600m_vs_csda"] for bb in b], "s--", label="Plano 600 m / esperado CSDA")
    axs[1].plot(xs, [bb["razon_100m_vs_csda"] for bb in b], "^--", label="Plano 100 m / esperado CSDA")
    axs[1].axhline(1.0, color="k", lw=0.6)
    axs[1].set_yscale("log")
    axs[1].set_xticks(xs, etiquetas, rotation=30, fontsize=7)
    axs[1].set_xlabel("Columna de roca (10³ g/cm²)")
    axs[1].set_ylabel("Razón")
    axs[1].yaxis.set_major_formatter(coma)
    axs[1].set_title("Por columna de roca (columnas interiores)")
    axs[1].legend(fontsize=7)
    rutas.append(c.guardar_figura(fig, "fig2-planos-por-pixel.png"))
    plt.close(fig)
    return rutas


def main() -> None:
    filas = cargar_corridas()
    serie = [dict(s) for s in SERIE_COMENTARIO]
    for s in serie:
        p = s["eficiencia_pct"] / 100
        s["sigma_binomial_pct_si_N_2e6"] = 100 * math.sqrt(p * (1 - p) / N_SERIE)
    f100 = next(f for f in filas if f["job"] == 29480)
    f600 = next(f for f in filas if f["job"] == 29484)
    pix = analisis_por_pixel()
    rutas = figuras(filas, serie, pix)
    pix.pop("_mapas")
    d300 = serie[2]["eficiencia_pct"] - serie[1]["eficiencia_pct"]
    sig = math.hypot(serie[1]["sigma_binomial_pct_si_N_2e6"], serie[2]["sigma_binomial_pct_si_N_2e6"])
    salida = {
        "geometria": GEO, "vista": 0,
        "corridas_conservadas": filas,
        "serie_2M_semilla_777_comentario_653f0fd": serie,
        "diferencia_300_600_pp": d300, "sigma_diferencia_pp_si_independientes": sig,
        "deficit_100_vs_600_relativo": 1 - f100["registrados_en_pixeles"] / f600["registrados_en_pixeles"],
        "energia_ganada_100_a_600": energia_ganada(f100, f600),
        "por_pixel_29480_vs_29484": pix,
        "figuras": rutas, "entorno": c.entorno(),
    }
    c.escribir_json(c.RESULTADOS / "comparacion-planos.json", salida)
    print(json.dumps({k: salida[k] for k in ("diferencia_300_600_pp", "sigma_diferencia_pp_si_independientes",
                                            "deficit_100_vs_600_relativo", "energia_ganada_100_a_600")},
                     indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()

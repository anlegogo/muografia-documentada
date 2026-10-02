"""Point 2b: equivalent exposure time of a production run.

Reproduces the historical normalization S0 (open-sky counts per view in 30 d)
from the Guan flux, applies the az-edges-v1 solid angle (256 equal azimuth
intervals) and quantifies how S0 changes under each convention choice that the
current chain fixes implicitly. Also maps the effective exposure per elevation
row implied by the measured open-sky efficiency of job 29484.

Outputs: resultados/exposicion-equivalente.json, figuras/fig4-exposicion.png

Usage (from the repository root):
    python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/exposicion_equivalente.py
"""

from __future__ import annotations

import json
import math

import numpy as np

import comun as c

DIAS = 30.0
T_S = DIAS * 86400.0


def s0(e_min_por_fila, el, d_az_rad, factor_area=None, flujo=c.guan_diff, n=6000):
    """Sum over rows of Phi_int(E_min) * A * dOmega * T (azimuth-uniform rows)."""
    cz = np.sin(np.radians(el))
    phi = np.empty(el.size)
    for i, (em, z) in enumerate(zip(np.broadcast_to(e_min_por_fila, el.shape), cz)):
        e = np.logspace(math.log10(em), math.log10(2e5), n)
        phi[i] = np.trapezoid(flujo(e, z), e)
    d_el = math.radians((c.EL_MAX_DEG - c.EL_MIN_DEG) / (c.N_EL - 1))
    d_omega = d_az_rad * d_el * np.cos(np.radians(el))
    if factor_area is None:
        filas = phi * c.DET_AREA_CM2 * d_omega * T_S * c.N_AZ
    else:
        filas = phi * c.DET_AREA_CM2 * d_omega * T_S * factor_area
    return filas


def main() -> None:
    el = c.centros_elevacion_deg()
    _, w_hist = c.leer_pesos_fila()
    d_az_hist = math.radians(2 * c.AZ_HALF_DEG / (c.N_AZ - 1))
    d_az_v1 = math.radians(2 * c.AZ_HALF_DEG / c.N_AZ)
    e_min = float(c.e_min_csda(c.X_AIRE_SURROGATE))

    filas_hist = s0(e_min, el, d_az_hist)
    filas_v1 = s0(e_min, el, d_az_v1)
    filas_v1_n4 = s0(e_min, el, d_az_v1, n=24000)

    # physical vertical panel: projected area A cos(el) cos(az) per bin (v1 centers)
    az_v1 = 0.5 * (c.bordes_azimut_v1_deg()[1:] + c.bordes_azimut_v1_deg()[:-1])
    proy = np.cos(np.radians(el))[:, None] * np.cos(np.radians(az_v1))[None, :]
    filas_panel = s0(e_min, el, d_az_v1, factor_area=proy.sum(axis=1))

    tabla = c.TablaRangoAire()
    e_aire_bethe_t = float(tabla.energia(c.X_AIRE_SURROGATE))  # kinetic energy with range = 367.5 g/cm2
    variantes = {
        "adoptada (umbral CSDA roca sobre 3 km de aire, E total)": filas_v1.sum(),
        "umbral interpretado como energía cinética (E_total = E_min + m)": s0(e_min + c.M_MU, el, d_az_v1).sum(),
        "densidad del aire G4_AIR en el umbral": s0(float(c.e_min_csda(3000 * 100 * c.RHO_G4_AIR)), el, d_az_v1).sum(),
        "umbral por rango Bethe en aire (cinética)": s0(e_aire_bethe_t + c.M_MU, el, d_az_v1).sum(),
        "sin umbral de aire (E_total desde p = 0,5 GeV/c de EcoMug)": s0(math.hypot(0.5, c.M_MU), el, d_az_v1).sum(),
        "panel vertical físico (área proyectada A·cos(el)·cos(az))": filas_panel.sum(),
    }
    ref = variantes["adoptada (umbral CSDA roca sobre 3 km de aire, E total)"]

    # angular coverage (v1): rows keep the historical centers, half-step margin on both ends
    medio_paso = 0.5 * (c.EL_MAX_DEG - c.EL_MIN_DEG) / (c.N_EL - 1)
    el_lo, el_hi = c.EL_MIN_DEG - medio_paso, c.EL_MAX_DEG + medio_paso
    omega_exacto = math.radians(2 * c.AZ_HALF_DEG) * (math.sin(math.radians(el_hi)) - math.sin(math.radians(el_lo)))
    d_el = math.radians(2 * medio_paso)
    omega_discreto = float((d_az_v1 * d_el * np.cos(np.radians(el))).sum() * c.N_AZ)

    # effective exposure per row if the counts are read as detector counts (job 29484, open sky)
    rel = json.loads((c.RESULTADOS / "relacion-plano-detector.json").read_text(encoding="utf-8")) \
        if (c.RESULTADOS / "relacion-plano-detector.json").exists() else None
    geo = c.leer_geometria("geo-train-01")
    x = c.opacidad_vista(geo, 0, el, c.centros_azimut_historicos_deg())
    h6 = c.leer_histograma(c.DATOS_SC3 / "smoke-29484" / "geo-train-01_view0_hist.csv").astype(float)
    inyect = 36174573 * (w_hist / w_hist.sum())[:, None] * c.fraccion_columna_historica()[None, :]
    cielo = (x == 0)
    cielo[:, [0, -1]] = False
    ef = np.where(cielo.sum(1) > 0, (h6 * cielo).sum(1) / np.maximum((inyect * cielo).sum(1), 1e-9), np.nan)

    n_casos = {"etapa 2 (24.000.000 pares)": 24_000_000, "S0 v1 (30 d)": round(c.S0_V1),
               "2 × S0 v1": 2 * round(c.S0_V1), "10 × S0 v1": 10 * round(c.S0_V1)}
    t_eq = {k: DIAS * v / c.S0_V1 for k, v in n_casos.items()}

    plt, coma = c.configurar_matplotlib()
    fig, axs = plt.subplots(1, 3, figsize=(14, 3.9), gridspec_kw={"wspace": 0.45})
    ax = axs[0]
    ax.plot(el, w_hist, "k-", lw=2.2, alpha=0.35, label="Tabla histórica row_weights_30d")
    ax.plot(el, filas_hist, "C0--", lw=1, label="Recalculado (Guan), malla histórica")
    ax.plot(el, filas_v1, "C1-", lw=1, label="Recalculado (Guan), az-edges-v1")
    ax.set_xlabel("Elevación (°)")
    ax.set_ylabel("Muones de cielo abierto por fila en 30 d")
    ax.set_title("Normalización por fila de elevación")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ax = axs[1]
    nombres = list(variantes)
    vals = [100 * (variantes[k] / ref - 1) for k in nombres]
    ax.barh(range(len(nombres)), vals, color=["k"] + ["C0"] * (len(nombres) - 1))
    cortos = ["Adoptada", "Umbral como E cinética", "ρ de G4_AIR en el umbral", "Umbral por rango Bethe",
              "Sin umbral de aire", "Panel vertical físico"]
    ax.set_yticks(range(len(nombres)), cortos, fontsize=7)
    ax.invert_yaxis()
    ax.axvline(0, color="k", lw=0.6)
    ax.set_xlabel("Cambio de S0 respecto de la convención adoptada (%)")
    ax.set_title("Sensibilidad de S0 a las convenciones")
    ax.xaxis.set_major_formatter(coma)
    ax = axs[2]
    ax.plot(el, DIAS * ef, "C1.", ms=3, label="Exposición efectiva (29484, cielo abierto)")
    ax.axhline(DIAS, color="k", lw=0.8, ls="--", label="Exposición nominal declarada")
    ax.set_xlabel("Elevación (°)")
    ax.set_ylabel("Días equivalentes")
    ax.set_title("Exposición si el conteo se lee como detector")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ax.yaxis.set_major_formatter(coma)
    ruta = c.guardar_figura(fig, "fig4-exposicion.png")
    plt.close(fig)

    salida = {
        "formula": "N_v1(T) = sum_b Phi_int(E_min, theta_b) * A * dOmega_b * T ; T_eq = 30 d * N / S0_v1",
        "e_min_umbral_gev": e_min,
        "s0_tabla_historica": float(w_hist.sum()),
        "s0_recalculado_malla_historica": float(filas_hist.sum()),
        "diferencia_relativa_historica": float(filas_hist.sum() / w_hist.sum() - 1),
        "max_dif_relativa_por_fila": float(np.max(abs(filas_hist / w_hist - 1))),
        "s0_v1_declarado": c.S0_V1,
        "s0_v1_recalculado": float(filas_v1.sum()),
        "diferencia_relativa_v1": float(filas_v1.sum() / c.S0_V1 - 1),
        "error_integracion_relativo": float(filas_v1_n4.sum() / filas_v1.sum() - 1),
        "angulo_solido_sr": {"exacto": omega_exacto, "suma_discreta_v1": omega_discreto,
                             "diferencia_relativa": omega_discreto / omega_exacto - 1,
                             "elevacion_cubierta_deg": [el_lo, el_hi], "azimut_cubierto_deg": [-30, 30]},
        "tasa_v1_por_segundo": float(filas_v1.sum() / T_S),
        "variantes_s0": {k: {"s0": float(v), "cambio_relativo": float(v / ref - 1)} for k, v in variantes.items()},
        "energia_cinetica_rango_aire_bethe_gev": e_aire_bethe_t,
        "factor_proyeccion_panel_vertical_medio": float(filas_panel.sum() / filas_v1.sum()),
        "exposicion_equivalente_dias": t_eq,
        "exposicion_efectiva_cielo_29484_dias": {"min": float(np.nanmin(DIAS * ef)), "max": float(np.nanmax(DIAS * ef)),
                                                 "media_ponderada": float(DIAS * np.nansum((h6 * cielo).sum(1)) /
                                                                         np.nansum((inyect * cielo).sum(1)))},
        "figura": ruta, "entorno": c.entorno(),
    }
    if rel:
        salida["referencia_modelo"] = c.ruta_relativa(c.RESULTADOS / "relacion-plano-detector.json")
    c.escribir_json(c.RESULTADOS / "exposicion-equivalente.json", salida)
    print(json.dumps({k: salida[k] for k in ("s0_recalculado_malla_historica", "diferencia_relativa_historica",
                                            "s0_v1_recalculado", "diferencia_relativa_v1", "angulo_solido_sr",
                                            "variantes_s0", "factor_proyeccion_panel_vertical_medio",
                                            "exposicion_equivalente_dias", "exposicion_efectiva_cielo_29484_dias",
                                            "energia_cinetica_rango_aire_bethe_gev")}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()

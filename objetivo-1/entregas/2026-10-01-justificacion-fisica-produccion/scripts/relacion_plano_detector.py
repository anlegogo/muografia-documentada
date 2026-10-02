"""Point 2a: how records on the large plane relate to the 1.2 m physical detector.

A semi-analytic transport model of open-sky muons through the air path that
the generator imposes (range-out, decay in flight, Gaussian multiple-scattering
displacement) is compared row by row with the measured open-sky efficiency of
jobs 29480 (100 m plane) and 29484 (600 m plane). The model is then used to
predict the efficiency for any plane size, including the 1.2 m panel and the
300 m plane whose data are missing.

Outputs: resultados/relacion-plano-detector.json, figuras/fig3-modelo-contencion.png

Usage (from the repository root):
    python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/relacion_plano_detector.py
"""

from __future__ import annotations

import json
import math

import numpy as np

import comun as c

GEO = "geo-train-01"
LADOS_M = [1.2, 10.0, 50.0, 100.0, 300.0, 600.0, 1200.0, 6000.0]
MARGEN_SILUETA_DEG = 1.0


def modelo_por_fila(el_deg, edges, cdf, r_inicio_m, tabla, lados):
    """Efficiency eps(row, side) for open-sky lines of sight."""
    out = np.zeros((el_deg.size, len(lados)))
    asintota = np.zeros(el_deg.size)
    sigma_mediana = np.zeros(el_deg.size)
    for i, e in enumerate(el_deg):
        banda = int(np.clip(np.searchsorted(edges, e, side="right") - 1, 0, cdf.shape[0] - 1))
        p = c.muestras_momento(cdf[banda], sub=4)
        longitud = r_inicio_m / math.cos(math.radians(e))
        r = c.transporte_aire(p, longitud * 100.0 * c.RHO_G4_AIR, c.RHO_G4_AIR, tabla, n_pasos=200)
        sy = r["sigma_y_m"]
        sz = sy / math.cos(math.radians(e))     # vertical plane, oblique incidence
        vivo = r["p_decay"]
        asintota[i] = vivo.mean()
        sigma_mediana[i] = float(np.median(sy[r["sobrevive_rango"]]))
        for j, lado in enumerate(lados):
            out[i, j] = np.mean(vivo * c.contencion_cuadrado(sy, sz, lado / 2.0))
    return out, asintota, sigma_mediana


def main() -> None:
    geo = c.leer_geometria(GEO)
    r_inicio = c.DET_DISTANCE_M + geo["edifice"]["base_radius_m"] + 300.0  # PrimaryGeneratorAction
    el = c.centros_elevacion_deg()
    az = c.centros_azimut_historicos_deg()
    x = c.opacidad_vista(geo, 0, el, az)
    sil = np.array([el[x[:, j] > 0].max() if (x[:, j] > 0).any() else -99.0 for j in range(c.N_AZ)])
    cielo = (x == 0) & (el[:, None] > sil[None, :] + MARGEN_SILUETA_DEG)
    cielo[:, [0, -1]] = False

    _, w = c.leer_pesos_fila()
    p_fila = w / w.sum()
    n = 36174573
    inyectados = n * p_fila[:, None] * c.fraccion_columna_historica()[None, :]
    h1 = c.leer_histograma(c.DATOS_SC3 / "smoke-29480" / f"{GEO}_view0_hist.csv").astype(float)
    h6 = c.leer_histograma(c.DATOS_SC3 / "smoke-29484" / f"{GEO}_view0_hist.csv").astype(float)

    edges, cdf = c.leer_p_cdf()
    tabla = c.TablaRangoAire()
    modelo, asintota, sigma_med = modelo_por_fila(el, edges, cdf, r_inicio, tabla, LADOS_M)
    j100, j600 = LADOS_M.index(100.0), LADOS_M.index(600.0)

    filas_validas = cielo.sum(axis=1) > 0
    med100 = np.full(el.size, np.nan)
    med600 = np.full(el.size, np.nan)
    sig600 = np.full(el.size, np.nan)
    for i in np.where(filas_validas)[0]:
        m = cielo[i]
        k1, k6, nn = h1[i, m].sum(), h6[i, m].sum(), inyectados[i, m].sum()
        med100[i], med600[i] = k1 / nn, k6 / nn
        sig600[i] = math.sqrt(k6) / nn
    res100 = med100 - modelo[:, j100]
    res600 = med600 - modelo[:, j600]
    interior = filas_validas & (el > 20.0) & (el < 42.0)
    bajas = filas_validas & (el < 13.0)

    # whole-image prediction (open-sky lines of sight only) for every plane size
    todo_cielo = (x == 0)
    iny_cielo = (inyectados * todo_cielo).sum(axis=1)
    pred_total = {f"{lado:g}": float((iny_cielo[:, None] * modelo).sum(axis=0)[j] / n)
                  for j, lado in enumerate(LADOS_M)}
    roca = x > 0
    contrib_roca = {"100": float(h1[roca].sum() / n), "600": float(h6[roca].sum() / n)}
    pred_total_asintota = float((iny_cielo * asintota).sum() / n)

    plt, coma = c.configurar_matplotlib()
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 3.9))
    ax = axs[0]
    ax.plot(el[filas_validas], 100 * med100[filas_validas], ".", ms=3, color="C0", label="Medido, plano 100 m")
    ax.plot(el[filas_validas], 100 * med600[filas_validas], ".", ms=3, color="C1", label="Medido, plano 600 m")
    ax.plot(el, 100 * modelo[:, j100], "-", color="C0", lw=1, label="Modelo, 100 m")
    ax.plot(el, 100 * modelo[:, j600], "-", color="C1", lw=1, label="Modelo, 600 m")
    ax.plot(el, 100 * asintota, "k--", lw=0.8, label="Modelo, plano infinito")
    ax.set_xlabel("Elevación (°)")
    ax.set_ylabel("Eficiencia en cielo abierto (%)")
    ax.set_title("Cielo abierto: medido vs. modelo por fila")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ax.yaxis.set_major_formatter(coma)

    ax = axs[1]
    ax.plot(el[filas_validas], 100 * res100[filas_validas], ".", ms=3, color="C0", label="100 m")
    ax.plot(el[filas_validas], 100 * res600[filas_validas], ".", ms=3, color="C1", label="600 m")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel("Elevación (°)")
    ax.set_ylabel("Medido − modelo (puntos porcentuales)")
    ax.set_title("Residuo del modelo gaussiano")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ax.yaxis.set_major_formatter(coma)

    ax = axs[2]
    pgrid = np.logspace(math.log10(0.6), 3, 120)
    for lon, col in [(2000.0, "C2"), (2800.0, "C3")]:
        r = c.transporte_aire(pgrid, lon * 100 * c.RHO_G4_AIR, c.RHO_G4_AIR, tabla, n_pasos=300)
        s = np.where(r["sobrevive_rango"], r["sigma_y_m"], np.nan)
        ax.loglog(pgrid, s, color=col, label=f"{lon/1e3:g} km de aire".replace(".", ","))
    for lado in (100, 300, 600):
        ax.axhline(lado / 2, color="gray", lw=0.6, ls=":")
        ax.text(0.65, lado / 2 * 1.08, f"semilado {lado/2:g} m", fontsize=6.5, color="gray")
    ax.axhline(0.6, color="gray", lw=0.6, ls=":")
    ax.text(0.65, 0.66, "semilado panel 0,6 m", fontsize=6.5, color="gray")
    ax.set_xlabel("Momento inicial (GeV/c)")
    ax.set_ylabel("Desplazamiento lateral rms (m)")
    ax.set_title("Escala del desplazamiento (Highland)")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ax.yaxis.set_major_formatter(coma)
    ruta = c.guardar_figura(fig, "fig3-modelo-contencion.png")
    plt.close(fig)

    salida = {
        "geometria": GEO, "vista": 0,
        "supuestos": {
            "lineas": "solo cielo abierto (columna de roca nula y > 1° sobre la silueta; sin columnas extremas)",
            "camino_aire_m": f"R_inicio / cos(elev), R_inicio = {r_inicio:g} m (PrimaryGeneratorAction)",
            "aire": f"G4_AIR, densidad {c.RHO_G4_AIR} g/cm3, X0 = {c.AIR_X0_G_CM2} g/cm2",
            "perdida": "Bethe con efecto densidad (Sternheimer), sin pérdidas radiativas ni fluctuaciones",
            "dispersion": "Highland diferencial, núcleo gaussiano; sin colas de dispersión simple",
            "decaimiento": f"c·tau = {c.C_TAU_MU_M} m",
            "espectro": "cuantiles p_cdf.txt por banda (el mismo muestreo del generador)",
            "plano": "cuadrado vertical; componente vertical escalada por 1/cos(elev)",
        },
        "validacion_filas_20_a_42_grados": {
            "residuo_100m_medio_pp": float(100 * np.nanmean(res100[interior])),
            "residuo_100m_max_abs_pp": float(100 * np.nanmax(abs(res100[interior]))),
            "residuo_600m_medio_pp": float(100 * np.nanmean(res600[interior])),
            "residuo_600m_max_abs_pp": float(100 * np.nanmax(abs(res600[interior]))),
            "sigma_poisson_fila_600m_pp_mediana": float(100 * np.nanmedian(sig600[interior])),
        },
        "residuo_600m_filas_sobre_44_grados_pp": float(100 * np.nanmean(res600[filas_validas & (el > 44)])),
        "residuo_100m_filas_bajo_13_grados_pp": float(100 * np.nanmean(res100[bajas])),
        "residuo_600m_filas_bajo_13_grados_pp": float(100 * np.nanmean(res600[bajas])),
        "eficiencia_total_predicha_solo_cielo": pred_total,
        "eficiencia_total_predicha_plano_infinito": pred_total_asintota,
        "contribucion_medida_pixeles_roca": contrib_roca,
        "eficiencia_total_medida": {"100": float(h1.sum() / n), "600": float(h6.sum() / n)},
        "desplazamiento_mediano_m_por_elevacion": {f"{e:.1f}": float(s) for e, s in
                                                   zip(el[::32], sigma_med[::32])},
        "figura": ruta, "entorno": c.entorno(),
    }
    c.escribir_json(c.RESULTADOS / "relacion-plano-detector.json", salida)
    print(json.dumps({k: salida[k] for k in ("validacion_filas_20_a_42_grados",
                                            "residuo_600m_filas_sobre_44_grados_pp",
                                            "eficiencia_total_predicha_solo_cielo",
                                            "eficiencia_total_predicha_plano_infinito",
                                            "contribucion_medida_pixeles_roca",
                                            "eficiencia_total_medida")}, indent=1))


if __name__ == "__main__":
    main()

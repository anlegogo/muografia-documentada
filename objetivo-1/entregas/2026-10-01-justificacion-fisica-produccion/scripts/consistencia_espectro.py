"""Point 2c: consistency between the generated momentum spectrum and the rate S0.

S0 integrates the Guan flux above E_min = 0.798 GeV (air threshold of the
surrogate), while the generator draws momenta from the EcoMug conditional
quantiles (p >= 0.5 GeV/c) and then transports every muon through 2-3 km of
air in Geant4. This script compares, per elevation band, (i) the shape of the
EcoMug sample against the Guan spectrum over the same range, (ii) the
fraction of generated muons below the S0 threshold, (iii) the rate that
corresponds to the generated range, and (iv) the open-sky losses that the
transport adds on top of the threshold already applied in S0.

Outputs: resultados/consistencia-espectro.json, figuras/fig5-espectro.png

Usage (from the repository root):
    python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/consistencia_espectro.py
"""

from __future__ import annotations

import json
import math

import numpy as np

import comun as c


def cdf_guan(e_grid, e0, cz):
    """CDF of the Guan spectrum restricted to E >= e0 (total energy)."""
    e = np.logspace(math.log10(e0), math.log10(2e5), 8000)
    f = c.guan_diff(e, cz)
    acum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(e))])
    return np.interp(e_grid, e, acum / acum[-1], left=0.0, right=1.0)


def main() -> None:
    edges, cdf = c.leer_p_cdf()
    e_umbral = float(c.e_min_csda(c.X_AIRE_SURROGATE))
    geo = c.leer_geometria("geo-train-01")
    r_inicio = c.DET_DISTANCE_M + geo["edifice"]["base_radius_m"] + 300.0
    tabla = c.TablaRangoAire()
    _, w = c.leer_pesos_fila()
    el_filas = c.centros_elevacion_deg()

    bandas = []
    for b in range(cdf.shape[0]):
        el_c = 0.5 * (edges[b] + edges[b + 1])
        cz = math.sin(math.radians(el_c))
        p = c.muestras_momento(cdf[b], sub=16)
        e_tot = np.sqrt(p**2 + c.M_MU**2)
        e0 = float(e_tot.min())
        grid = np.sort(e_tot)
        f_eco = (np.arange(grid.size) + 0.5) / grid.size
        f_guan = cdf_guan(grid, e0, cz)
        ks = float(np.max(np.abs(f_eco - f_guan)))
        i_e0 = float(c.guan_integral(e0, np.array([cz]))[0])
        i_um = float(c.guan_integral(e_umbral, np.array([cz]))[0])
        i_pmax = float(c.guan_integral(float(e_tot.max()), np.array([cz]))[0])
        longitud = r_inicio / math.cos(math.radians(el_c))
        tr = c.transporte_aire(p, longitud * 100 * c.RHO_G4_AIR, c.RHO_G4_AIR, tabla, n_pasos=200)
        filas_banda = (el_filas >= edges[b]) & (el_filas < edges[b + 1] if b < cdf.shape[0] - 1 else el_filas <= edges[b + 1])
        bandas.append({
            "banda_deg": [float(edges[b]), float(edges[b + 1])],
            "peso_s0": float(w[filas_banda].sum() / w.sum()),
            "e_total_min_generado_gev": e0, "e_total_max_generado_gev": float(e_tot.max()),
            "mediana_ecomug_gev": float(np.median(e_tot)),
            "mediana_guan_mismo_rango_gev": float(np.interp(0.5, f_guan, grid)),
            "ks_ecomug_vs_guan": ks,
            "fraccion_generada_bajo_umbral_s0_ecomug": float(np.mean(e_tot < e_umbral)),
            "fraccion_bajo_umbral_s0_guan": 1 - i_um / i_e0,
            "razon_tasa_rango_generado_vs_s0": i_e0 / i_um,
            "fraccion_flujo_sobre_maximo_generado": i_pmax / i_um,
            "camino_aire_m": longitud,
            "supervivencia_rango_aire": float(tr["sobrevive_rango"].mean()),
            "supervivencia_rango_y_decaimiento": float(tr["p_decay"].mean()),
        })

    pesos = np.array([b["peso_s0"] for b in bandas])
    resumen = {
        "umbral_s0_gev": e_umbral,
        "fraccion_generada_bajo_umbral_ponderada": float(np.sum(pesos * [b["fraccion_generada_bajo_umbral_s0_ecomug"] for b in bandas])),
        "perdida_transporte_aire_ponderada": float(1 - np.sum(pesos * [b["supervivencia_rango_y_decaimiento"] for b in bandas])),
        "ks_max": float(max(b["ks_ecomug_vs_guan"] for b in bandas)),
        "ks_min": float(min(b["ks_ecomug_vs_guan"] for b in bandas)),
    }

    plt, coma = c.configurar_matplotlib()
    fig, axs = plt.subplots(1, 3, figsize=(14, 3.9), gridspec_kw={"wspace": 0.35})
    ax = axs[0]
    for b, col in [(0, "C0"), (7, "C1"), (15, "C2")]:
        p = c.muestras_momento(cdf[b], sub=16)
        e_tot = np.sort(np.sqrt(p**2 + c.M_MU**2))
        el_c = 0.5 * (edges[b] + edges[b + 1])
        ax.semilogx(e_tot, (np.arange(e_tot.size) + 0.5) / e_tot.size, color=col,
                    label=f"EcoMug, {edges[b]:.1f}–{edges[b+1]:.1f}°".replace(".", ","))
        ax.semilogx(e_tot, cdf_guan(e_tot, e_tot[0], math.sin(math.radians(el_c))), "--", color=col, lw=0.9)
    ax.axvline(e_umbral, color="k", lw=0.7, ls=":")
    ax.text(e_umbral * 1.05, 0.05, "umbral S0", fontsize=7)
    ax.set_xlabel("Energía total (GeV)")
    ax.set_ylabel("Distribución acumulada")
    ax.set_title("EcoMug (continua) vs. Guan (discontinua)")
    ax.legend(fontsize=6.5, loc="lower right")
    ax.yaxis.set_major_formatter(coma)
    ax = axs[1]
    xc = np.array([0.5 * (bb["banda_deg"][0] + bb["banda_deg"][1]) for bb in bandas])
    ax.plot(xc, [100 * bb["fraccion_generada_bajo_umbral_s0_ecomug"] for bb in bandas], "o-",
            label="Generados bajo el umbral de S0 (EcoMug)")
    ax.plot(xc, [100 * bb["fraccion_bajo_umbral_s0_guan"] for bb in bandas], "s--",
            label="Misma fracción según Guan")
    ax.plot(xc, [100 * (bb["razon_tasa_rango_generado_vs_s0"] - 1) for bb in bandas], "^:",
            label="Exceso de tasa si S0 cubriera el rango generado")
    ax.plot(xc, [100 * (1 - bb["supervivencia_rango_y_decaimiento"]) for bb in bandas], "d-",
            label="Pérdida adicional por transporte en aire (modelo)")
    ax.set_xlabel("Elevación (°)")
    ax.set_ylabel("%")
    ax.set_title("Umbral de S0 frente al espectro generado")
    ax.legend(fontsize=6.5)
    ax.xaxis.set_major_formatter(coma)
    ax.yaxis.set_major_formatter(coma)
    ax = axs[2]
    ax.plot(xc, [bb["ks_ecomug_vs_guan"] for bb in bandas], "o-")
    ax.set_xlabel("Elevación (°)")
    ax.set_ylabel("Distancia de Kolmogorov–Smirnov")
    ax.set_title("Forma espectral EcoMug vs. Guan (mismo rango)")
    ax.xaxis.set_major_formatter(coma)
    ax.yaxis.set_major_formatter(coma)
    ruta = c.guardar_figura(fig, "fig5-espectro.png")
    plt.close(fig)

    salida = {"resumen": resumen, "bandas": bandas, "figura": ruta,
              "supuestos": {"energia_guan": "E en la parametrización de Guan tratada como energía total",
                            "transporte": "mismo modelo que relacion_plano_detector.py (G4_AIR, camino R_inicio/cos)",
                            "geometria_camino": "geo-train-01 (R_inicio = 1956,2 m)"},
              "entorno": c.entorno()}
    c.escribir_json(c.RESULTADOS / "consistencia-espectro.json", salida)
    print(json.dumps(resumen, indent=1))
    for bb in bandas[::5]:
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in bb.items()})


if __name__ == "__main__":
    main()

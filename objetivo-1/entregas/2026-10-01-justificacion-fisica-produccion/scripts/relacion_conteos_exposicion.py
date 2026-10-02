"""Counts-exposure relation of the directional-estimator image (az-edges-v1).

    E[C_ij] = T * A_perp * dOmega_ij * Phi_ij * eps_ij

Phi_ij   Guan integral flux above E_min(367.5 g/cm2 of air) at zenith 90 - el_i
         (S0 convention; azimuth independent)               [cm^-2 s^-1 sr^-1]
A_perp   1.44e4 cm2, normal to each direction (no projection)
dOmega   (60/256 deg)(45/255 deg) cos(el_i), 256 equal azimuth intervals [sr]
T        30 d * N_nom / S0_v1, N_nom = primaries whose nominal direction falls
         in the image window (counted exactly by the _gen histogram)
eps_ij   E[C_ij] / E[N_nom,ij]: registered with E_kin > 3 GeV in pixel ij per
         nominal injection in ij (transmission x cut efficiency x migration)

EcoMug enters only through the conditional momentum shape (p_cdf.txt); the
absolute rate comes from the Guan integral through S0.

Also computes, for the physical-detector option, the projected area and the
geometric acceptance of an illustrative two-plane telescope, and the dilution
of a spatially wide source from the nested squares of run c01.

Inputs: tables, datos/sc3/controles-30626 (c01, c02), datos/sc3/prueba-integracion.
Outputs: resultados/relacion-conteos-exposicion.json, figuras/fig9-relacion-conteos-exposicion.png

Usage (from the repository root):
    python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/relacion_conteos_exposicion.py
"""

from __future__ import annotations

import json
import math

import numpy as np

import comun as c
import controles_sc3 as cs

T_30D_S = 30 * 86400.0
BANDAS = [(1e4, 3e4), (3e4, 6e4), (6e4, 1e5), (1e5, 2e5), (2e5, 1e7)]
MEDIO_LADO_PANEL = 0.6
OBJ_C3 = 1600   # panel counts per band: Poisson 2.5 %, 95 % interval about +-5 %


def flujo_y_angulo_solido():
    el = c.centros_elevacion_deg()
    cz = np.sin(np.radians(el))
    e_min = float(c.e_min_csda(c.X_AIRE_SURROGATE))
    phi = np.array([c.guan_integral(e_min, np.array([z]), n=6000)[0] for z in cz])
    d_az = math.radians(2 * c.AZ_HALF_DEG / c.N_AZ)
    d_el = math.radians((c.EL_MAX_DEG - c.EL_MIN_DEG) / (c.N_EL - 1))
    d_omega = d_az * d_el * np.cos(np.radians(el))
    return el, e_min, phi, d_omega


def p_chi2(x: float, k: int) -> float:
    """Upper-tail chi-square probability, Wilson-Hilferty approximation (k large)."""
    z = ((x / k) ** (1 / 3) - (1 - 2 / (9 * k))) / math.sqrt(2 / (9 * k))
    return 0.5 * math.erfc(z / math.sqrt(2))


def cargar(job: str, nombre: str) -> dict:
    return cs.cargar(c.DATOS_SC3 / f"controles-{job}" / "resultados" / nombre)


def gen_integracion() -> tuple[np.ndarray, int]:
    base = c.DATOS_SC3 / "prueba-integracion" / "oe1-v1-prueba" / "geo-train-06" / "view0"
    g = sum(c.leer_histograma(b / "geo-train-06_view0_gen.csv").astype(float) for b in sorted(base.glob("block*")))
    ev = sum(json.loads((b / "geo-train-06_view0.meta.json").read_text(encoding="utf-8"))["events_transported"]
             for b in sorted(base.glob("block*")))
    return g, ev


def aceptacion_telescopio(el, az, lado_m, separacion_m):
    """Two square planes of side L separated by d along the horizontal normal.

    Overlap area on the plane for direction (el, az): (L - d|tan ax|)(L - d|tan ay|),
    with tan ax = tan(az) and tan ay = tan(el)/cos(az); area normal to the
    direction = overlap * cos(angle to the normal) = overlap * cos(el) cos(az).
    Returned as a fraction of A_perp = L^2.
    """
    e = np.radians(el)[:, None]
    a = np.radians(az)[None, :]
    tx = np.abs(np.tan(a))
    ty = np.abs(np.tan(e) / np.cos(a))
    sobre = np.clip(lado_m - separacion_m * tx, 0, None) * np.clip(lado_m - separacion_m * ty, 0, None)
    return sobre * np.cos(e) * np.cos(a) / lado_m**2


def main() -> None:
    el, e_min, phi, d_omega = flujo_y_angulo_solido()
    filas_s0 = phi * c.DET_AREA_CM2 * d_omega * T_30D_S * c.N_AZ
    s0_calc = float(filas_s0.sum())
    _, w = c.leer_pesos_fila()
    w_v1 = w * (c.N_AZ - 1) / c.N_AZ

    # --- images with exact nominal counts
    c01 = cargar("30626", "c01-anidado-cono")
    c02 = cargar("30626", "c02-cono-margen-5deg")
    g_int, ev_int = gen_integracion()
    imagenes = {}
    for nombre, gen, n_gen in (("c01 (2e7, sin margen)", c01["gen"], c01["meta"]["events_transported"]),
                               ("c02 (2e6, margen 5°)", c02["gen"], c02["meta"]["events_transported"]),
                               ("integración 108+109 (2e5, margen 5°)", g_int, ev_int)):
        n_nom = float(gen.sum())
        esperado_fila = n_nom * w_v1 / w_v1.sum()
        obs_fila = gen.sum(axis=1)
        chi2 = float(np.sum((obs_fila - esperado_fila) ** 2 / esperado_fila))
        imagenes[nombre] = {"primarios_generados": int(n_gen), "nominales_en_ventana": int(n_nom),
                            "fraccion_en_ventana": n_nom / n_gen, "T_dias": 30 * n_nom / c.S0_V1,
                            "chi2_filas_gen_vs_tabla": chi2, "grados_libertad": int(c.N_EL - 1),
                            "p_valor_aprox": p_chi2(chi2, c.N_EL - 1)}
    imagenes["producción k = 10 (planificada)"] = {"nominales_en_ventana": round(10 * c.S0_V1), "T_dias": 300.0}

    # --- eps_ij and transmission from c01 (E > 3 GeV, 600 m square)
    geo, el_g, az, x, cielo = cs.geometria()
    cuentas = c01["h"]["300"]["3"]
    gen = c01["gen"]
    with np.errstate(divide="ignore", invalid="ignore"):
        eps = np.where(gen > 0, cuentas / gen, np.nan)
    eps_cielo_fila = np.array([np.nansum(cuentas[i][cielo[i]]) / max(gen[i][cielo[i]].sum(), 1)
                               if cielo[i].any() else np.nan for i in range(c.N_EL)])
    eps_cielo_ref = np.interp(el, el[np.isfinite(eps_cielo_fila)], eps_cielo_fila[np.isfinite(eps_cielo_fila)])
    transmision = eps / eps_cielo_ref[:, None]
    # identity check: E[C] = T * A * dOmega * Phi * eps summed over the image equals the counts
    t_c01 = imagenes["c01 (2e7, sin margen)"]["T_dias"] * 86400
    pred = t_c01 * c.DET_AREA_CM2 * (d_omega * phi * (c.S0_V1 / s0_calc))[:, None] * np.nan_to_num(eps)
    identidad = float(pred.sum() / cuentas.sum())

    # --- physical-detector option
    proy = (np.cos(np.radians(el))[:, None] * np.cos(np.radians(az))[None, :])
    peso = (phi * d_omega)[:, None] * np.ones((1, c.N_AZ))
    factor_proy = float((peso * proy).sum() / peso.sum())
    telescopios = {}
    for d_sep in (0.3, 0.6, 1.2):
        acc = aceptacion_telescopio(el, az, c.DET_SIDE_M, d_sep)
        telescopios[f"{d_sep:g}"] = {"factor_medio_ponderado": float((peso * acc).sum() / peso.sum()),
                                     "fraccion_pixeles_sin_aceptacion": float(np.mean(acc <= 0)),
                                     "elevacion_maxima_con_aceptacion_deg": float(np.degrees(np.arctan(c.DET_SIDE_M / d_sep)))}
    resolucion = {f"{p_cm:g} cm / {d:g} m": math.degrees(p_cm / 100 / (d * math.sqrt(6)))
                  for p_cm in (1.0, 4.0) for d in (0.3, 0.6, 1.2)}

    # containment of the 600 m square counts in the panel and in the 100 m square (c01, E > 3 GeV)
    conten = []
    for lo, hi in BANDAS:
        m = (x >= lo) & (x < hi)
        n6 = c01["h"]["300"]["3"][m].sum()
        conten.append({"banda": [lo, hi], "cuadrado_600m": int(n6),
                       "panel_1_2m": int(c01["h"]["0.6"]["3"][m].sum()),
                       "fraccion_panel": float(c01["h"]["0.6"]["3"][m].sum() / n6),
                       "fraccion_100m": float(c01["h"]["50"]["3"][m].sum() / n6)})
    dilucion_50 = (2 * 50.0) ** 2 / (2 * MEDIO_LADO_PANEL) ** 2

    # --- sizing of control C3 (wide source, central 1.2 m panel), geo-train-01 view 0
    banda_c3 = (x >= 3e4) & (x < 2e5)
    f_dir = float(gen[banda_c3].sum() / gen.sum())          # nominal directions in the target band
    n_banda = float(c01["h"]["300"]["3"][(x >= 3e4) & (x < 6e4)].sum())  # per 2e7, 30-60e3 band
    coste_ev = json.loads((c.RESULTADOS / "controles-sc3.json").read_text(encoding="utf-8"))[
        "impacto_produccion"]["nucleo_s_por_evento"]["c01-anidado-cono"]
    control_c3 = {"fraccion_direcciones_banda_3e4_2e5": f_dir, "conteo_banda_30_60_por_2e7": n_banda,
                  "objetivo_conteo_panel_banda_30_60": OBJ_C3, "nucleo_s_por_evento_c01": coste_ev, "por_semilado": []}
    for g in (5.0, 10.0, 20.0, 50.0):
        dil = (2 * g) ** 2 / (2 * MEDIO_LADO_PANEL) ** 2
        n_total = OBJ_C3 / n_banda * 2e7 * dil            # all directions, if equivalence holds
        n_dir = n_total * f_dir                          # directions restricted to the band
        control_c3["por_semilado"].append({"semilado_m": g, "dilucion": dil, "primarios_todas_direcciones": n_total,
                                           "primarios_direcciones_banda": n_dir,
                                           "horas_nucleo_direcciones_banda": n_dir * coste_ev / 3600})
    control_c3["etapa_a_cuadrados_pequenos_horas_nucleo"] = 2e7 * coste_ev / 3600
    plan = json.loads((c.RESULTADOS / "plan-produccion.json").read_text(encoding="utf-8"))
    k10 = next(o for o in plan["receta_validada"]["opciones"] if o["k"] == 10)

    # --- figure
    plt, coma = c.configurar_matplotlib()
    fig, axs = plt.subplots(1, 4, figsize=(18, 3.9), gridspec_kw={"wspace": 0.32})
    ax = axs[0]
    ax.plot(el, filas_s0 * c.S0_V1 / s0_calc, "C0-", label="Φ·A·ΔΩ·T (30 d), por fila")
    ax.plot(el, w_v1, "k:", label="Tabla v1 (row_weights × 255/256)")
    ax.set_xlabel("Elevación (°)")
    ax.set_ylabel("Inyecciones nominales por fila (30 d)")
    ax.set_title("Tasa por fila, malla v1")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ext = [az[0], az[-1], el[0], el[-1]]
    from matplotlib.colors import LogNorm
    for ax, mapa, titulo, norma in ((axs[1], eps, "ε_ij (c01, E > 3 GeV, 600 m)", None),
                                    (axs[2], np.clip(transmision, 1e-4, None), "Transmisión ε_ij / ε_cielo(el)",
                                     LogNorm(vmin=1e-4, vmax=1.2))):
        im = ax.imshow(mapa, origin="lower", aspect="auto", extent=ext, cmap="viridis",
                       **({"norm": norma} if norma else {"vmin": 0, "vmax": 1}))
        ax.contour(az, el, x, levels=[1.0], colors="w", linewidths=0.6)
        fig.colorbar(im, ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel("Azimut relativo (°)")
        ax.set_ylabel("Elevación (°)")
        ax.grid(False)
    ax = axs[3]
    acc = aceptacion_telescopio(el, az, c.DET_SIDE_M, 0.6)
    im = ax.imshow(acc, origin="lower", aspect="auto", extent=ext, vmin=0, vmax=1, cmap="magma")
    fig.colorbar(im, ax=ax)
    ax.set_title("Detector: A_eff/A⊥, telescopio ilustrativo d = 0,6 m")
    ax.set_xlabel("Azimut relativo (°)")
    ax.set_ylabel("Elevación (°)")
    ax.grid(False)
    ruta = c.guardar_figura(fig, "fig9-relacion-conteos-exposicion.png")
    plt.close(fig)

    salida = {
        "definiciones": {
            "E_min_gev": e_min, "A_perp_cm2": c.DET_AREA_CM2,
            "dOmega_sr": "(60/256 deg)(45/255 deg) cos(el)", "suma_dOmega_sr": float(d_omega.sum() * c.N_AZ),
            "S0_v1_declarado": c.S0_V1, "S0_v1_recalculado": s0_calc,
            "diferencia_relativa": s0_calc / c.S0_V1 - 1, "tasa_s-1": c.S0_V1 / T_30D_S,
            "phi_cm2_s_sr": {"el_2": float(phi[0]), "el_24.5": float(phi[c.N_EL // 2]), "el_47": float(phi[-1])},
        },
        "imagenes": imagenes,
        "identidad_c01_prediccion_sobre_conteo": identidad,
        "eps_c01": {"cielo_media_filas_20_42": float(np.nanmean(eps_cielo_fila[(el > 20) & (el < 42)])),
                    "transmision_mediana_roca_3e4_1e5": float(np.nanmedian(transmision[(x >= 3e4) & (x < 1e5)]))},
        "detector": {"factor_area_proyectada": factor_proy, "telescopio_dos_planos": telescopios,
                     "resolucion_angular_rms_deg": resolucion, "pixel_deg": {"az": 60 / 256, "el": 45 / 255},
                     "contencion_c01_E3": conten,
                     "dilucion_fuente_amplia_semilado_50m": dilucion_50,
                     "coste_k10_estimador_h_nucleo": k10["horas_nucleo"],
                     "coste_k10_detector_fuente_amplia_h_nucleo": k10["horas_nucleo"] * dilucion_50,
                     "mediana_roi_k10_estimador": k10["conteo_roi_mediano_referencia"]},
        "control_C3": control_c3,
        "figura": ruta, "entorno": c.entorno(),
    }
    c.escribir_json(c.RESULTADOS / "relacion-conteos-exposicion.json", salida)
    print(json.dumps({k: salida[k] for k in ("definiciones", "imagenes", "identidad_c01_prediccion_sobre_conteo", "eps_c01")},
                     indent=1, ensure_ascii=False))
    print(json.dumps(salida["detector"], indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()

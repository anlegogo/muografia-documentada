"""Point 4: production plan figures from measured timings, sizes and counts.

Inputs:
- datos/sc3/campaign-merged-meta/*.meta.json   (114 views, wall time per view)
- datos/sc3/sacct-campana-bloques.txt           (121 SLURM jobs of the campaign)
- datos/sc3/campaign-manifest.csv               (SHA-256 of the 114 histograms)
- --campana DIR: the merged campaign histograms (SC3: ~/muography-scratch/campaign-merged).
  They are not versioned (26 MB); their SHA-256 are checked against the manifest.

Outputs: resultados/plan-produccion.json, figuras/fig6-estadistica-roi.png,
produccion/manifiesto-v1-k{K}.csv

Usage (from the repository root):
    python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/plan_produccion.py --campana RUTA/campaign-merged
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import statistics as st
from datetime import datetime
from pathlib import Path

import numpy as np

import comun as c

FRACCIONES = [0.5, 0.1, 0.05, 0.01]
REALIZACIONES = 20
K_OPCIONES = [1, 2, 4, 8]
K_RECETA = [4, 8, 10, 16, 32]
C_OBJETIVO_10 = 100           # counts -> 10 % Poisson precision
ROI = 4                       # ROI = 4 x 4 pixels (0.94 deg x 0.70 deg)
BANDA_ROI = (3.0e4, 1.0e5)    # rock column of the ROI centre, g/cm^2
C_OBJETIVO = 400              # counts -> 5 % Poisson precision
PERCENTIL = 10                # 90 % of the ROIs must reach C_OBJETIVO
SEMILLA_MAESTRA_V1 = 20261001
CPUS = 24
MAX_SIMULTANEOS = 4           # QoS MaxSubmitPU observed in the 2026-08-30 campaign
EVENTOS_MAX_BLOQUE = 40_000_000   # keeps a block below ~25 min on 24 legacy cores


def tiempos() -> dict:
    metas = c.leer_metas_campana()
    cs_ev = [m["wall_seconds_total"] * CPUS / m["events_transported"] for m in metas]
    filas = c.leer_sacct(c.DATOS_SC3 / "sacct-campana-bloques.txt")
    vistas = [(re.search(r"GEO=([\w-]+)", f["SubmitLine"]).group(1),
               re.search(r"VIEW=(\d)", f["SubmitLine"]).group(1)) for f in filas]
    inicio = min(datetime.fromisoformat(f["Start"]) for f in filas)
    fin = max(datetime.fromisoformat(f["End"]) for f in filas)
    elapsed = [int(f["ElapsedRaw"]) for f in filas]
    return {
        "vistas": len(metas), "trabajos_slurm": len(filas), "vistas_distintas_en_slurm": len(set(vistas)),
        "trabajos_duplicados": len(filas) - len(set(vistas)),
        "particion": sorted({f["Partition"] for f in filas}), "cpus_por_trabajo": sorted({int(f["NCPUS"]) for f in filas}),
        "nucleo_s_por_evento": {"media": st.mean(cs_ev), "desv": st.stdev(cs_ev), "min": min(cs_ev), "max": max(cs_ev)},
        "pared_s_por_vista": {"media": st.mean(m["wall_seconds_total"] for m in metas),
                              "desv": st.stdev(m["wall_seconds_total"] for m in metas)},
        "slurm_elapsed_s": {"media": st.mean(elapsed), "desv": st.stdev(elapsed), "max": max(elapsed)},
        "horas_nucleo_consumidas": sum(e * CPUS for e in elapsed) / 3600,
        "duracion_campana_h": (fin - inicio).total_seconds() / 3600,
        "inicio": inicio.isoformat(), "fin": fin.isoformat(),
    }


def verificar_y_leer(campana: Path) -> dict[tuple[str, int], np.ndarray]:
    with open(c.DATOS_SC3 / "campaign-manifest.csv", encoding="utf-8") as fh:
        manifiesto = list(csv.DictReader(fh))
    hists = {}
    for r in manifiesto:
        ruta = campana / r["geometry"] / f'{r["geometry"]}_view{r["view"]}_hist.csv'
        if c.sha256(ruta) != r["hist_sha256"]:
            raise SystemExit(f"huella discrepante: {ruta}")
        hists[(r["geometry"], int(r["view"]))] = c.leer_histograma(ruta)
    return hists


def estadistica_roi(hists) -> dict:
    el = c.centros_elevacion_deg()
    az = c.centros_azimut_historicos_deg()
    el_c = el.reshape(-1, ROI).mean(axis=1)
    az_c = az.reshape(-1, ROI).mean(axis=1)
    geos = {}
    por_vista = []
    todos = []
    for (g, v), h in sorted(hists.items()):
        if g not in geos:
            geos[g] = c.leer_geometria(g)
        x = c.opacidad_vista(geos[g], v, el_c, az_c, paso_m=4.0)
        cr = h.reshape(c.N_EL // ROI, ROI, c.N_AZ // ROI, ROI).sum(axis=(1, 3))
        sel = (x >= BANDA_ROI[0]) & (x < BANDA_ROI[1])
        vals = cr[sel].astype(float)
        if vals.size == 0:
            continue
        todos.append(vals)
        q = float(np.percentile(vals, PERCENTIL))
        por_vista.append({"geometria": g, "vista": v, "rois_en_banda": int(vals.size),
                          "mediana": float(np.median(vals)), f"p{PERCENTIL}": q,
                          "k_necesario": C_OBJETIVO / max(q, 1e-9)})
    todos = np.concatenate(todos)
    ks = np.array([p["k_necesario"] for p in por_vista])
    return {"roi_pixeles": ROI, "banda_columna_g_cm2": list(BANDA_ROI), "conteo_objetivo": C_OBJETIVO,
            "percentil": PERCENTIL, "vistas_con_rois": len(por_vista), "rois_totales": int(todos.size),
            "mediana_global": float(np.median(todos)),
            f"p{PERCENTIL}_global": float(np.percentile(todos, PERCENTIL)),
            "k_necesario": {"mediana": float(np.median(ks)), "p90": float(np.percentile(ks, 90)),
                            "max": float(ks.max())},
            "por_vista": por_vista, "_todos": todos}


def almacenamiento(hists, muestras: int = 6) -> dict:
    claves = sorted(hists)[:: max(1, len(hists) // muestras)][:muestras]
    rng = np.random.default_rng(SEMILLA_MAESTRA_V1)
    tam_npz = []
    for k in claves:
        ref = hists[k].astype(np.uint32)
        low = np.stack([np.stack([rng.binomial(ref, f).astype(np.uint32) for _ in range(REALIZACIONES)])
                        for f in FRACCIONES])
        buf = io.BytesIO()
        np.savez_compressed(buf, counts_ref=ref, low_counts=low, fractions=np.array(FRACCIONES))
        tam_npz.append(buf.getbuffer().nbytes)
    tam_csv = [len(np.array2string(hists[k], separator=",", threshold=10**9)) for k in claves]
    return {"npz_pares_bytes_por_vista": {"media": st.mean(tam_npz), "min": min(tam_npz), "max": max(tam_npz),
                                         "vistas_medidas": [f"{g}_view{v}" for g, v in claves]},
            "npz_sin_comprimir_bytes": len(FRACCIONES) * REALIZACIONES * c.N_EL * c.N_AZ * 4,
            "hist_csv_bytes_aprox": st.mean(tam_csv)}


def manifiesto(k: int, ruta: Path, fraccion_ventana: float) -> int:
    """Rows per block; events = k * S0_v1 / window fraction (5 deg generation margin)."""
    geos = sorted(p.stem for p in c.GEOMETRIAS.glob("geo-*.json"))
    n_vista = round(k * c.S0_V1 / fraccion_ventana)
    bloques = math.ceil(n_vista / EVENTOS_MAX_BLOQUE)
    base, resto = divmod(n_vista, bloques)
    filas = []
    for gi, g in enumerate(geos):
        for v in range(6):
            for b in range(bloques):
                semilla = SEMILLA_MAESTRA_V1 * 1_000_000 + gi * 10_000 + v * 1_000 + b
                filas.append((len(filas), g, v, b, semilla, base + (1 if b < resto else 0)))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["fila", "geometria", "vista", "bloque", "semilla", "eventos"])
        wr.writerows(filas)
    return len(filas)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--campana", type=Path, required=True)
    args = ap.parse_args()

    t = tiempos()
    hists = verificar_y_leer(args.campana)
    roi = estadistica_roi(hists)
    alm = almacenamiento(hists)
    cs = t["nucleo_s_por_evento"]

    opciones = []
    for k in K_OPCIONES:
        n_vista = k * c.S0_V1
        n_total = 114 * n_vista
        bloques = 114 * math.ceil(n_vista / EVENTOS_MAX_BLOQUE)
        h_nucleo = n_total * cs["media"] / 3600
        h_nucleo_sigma = n_total * cs["desv"] / 3600 / math.sqrt(114)
        pared = n_total * cs["media"] / CPUS / MAX_SIMULTANEOS / 3600
        opciones.append({
            "k": k, "eventos_por_vista": round(n_vista), "eventos_totales": round(n_total),
            "exposicion_equivalente_dias": 30 * k, "bloques": bloques,
            "horas_nucleo": h_nucleo, "horas_nucleo_sigma_media": h_nucleo_sigma,
            "horas_nucleo_rango_por_dispersion_vistas": [n_total * cs["min"] / 3600, n_total * cs["max"] / 3600],
            "pared_h_con_4_trabajos_simultaneos": pared,
            "fraccion_rois_banda_con_objetivo": float(np.mean(k * roi["_todos"] >= C_OBJETIVO)),
            "conteo_roi_mediano_por_fraccion": {f"{f:g}": k * roi["mediana_global"] * f for f in FRACCIONES},
            "almacenamiento_gb": {
                "histogramas_csv": 114 * alm["hist_csv_bytes_aprox"] * math.ceil(n_vista / EVENTOS_MAX_BLOQUE) / 1e9,
                "pares_npz_comprimidos_medido_k1": (114 * alm["npz_pares_bytes_por_vista"]["media"] / 1e9
                                                     if k == 1 else None),
                "pares_npz_sin_comprimir": 114 * alm["npz_sin_comprimir_bytes"] / 1e9},
        })
    # Validated recipe (controles-sc3.json): cone injection, E > 3 GeV, 5 deg margin.
    imp = json.loads((c.RESULTADOS / "controles-sc3.json").read_text(encoding="utf-8"))["impacto_produccion"]
    factor = imp["factor_conteo_roi_mediana"]
    f_ventana = imp["fraccion_generada_en_ventana_margen_5"]
    cs_ventana = imp["nucleo_s_por_evento_en_ventana_receta"]
    roi_receta = roi["_todos"] * factor
    opciones_receta = []
    for k in K_RECETA:
        en_ventana = 114 * k * c.S0_V1
        opciones_receta.append({
            "k": k, "exposicion_equivalente_dias": 30 * k,
            "eventos_generados_por_vista": round(k * c.S0_V1 / f_ventana),
            "bloques_por_vista": math.ceil(k * c.S0_V1 / f_ventana / EVENTOS_MAX_BLOQUE),
            "horas_nucleo": en_ventana * cs_ventana / 3600,
            "pared_h_con_4_trabajos_simultaneos": en_ventana * cs_ventana / CPUS / MAX_SIMULTANEOS / 3600,
            "fraccion_rois_400": float(np.mean(k * roi_receta >= C_OBJETIVO)),
            "fraccion_rois_100": float(np.mean(k * roi_receta >= C_OBJETIVO_10)),
            "conteo_roi_mediano_referencia": float(k * np.median(roi_receta)),
            "conteo_roi_mediano_fraccion_0_01": float(0.01 * k * np.median(roi_receta)),
            "histogramas_gb": 114 * alm["hist_csv_bytes_aprox"] * 3 * math.ceil(k * c.S0_V1 / f_ventana / EVENTOS_MAX_BLOQUE) / 1e9,
        })
    k_10 = float(C_OBJETIVO_10 / np.percentile(roi_receta, PERCENTIL))
    k_5 = float(C_OBJETIVO / np.percentile(roi_receta, PERCENTIL))
    filas_manifiesto = {k: manifiesto(k, c.ENTREGA / "produccion" / f"manifiesto-receta-k{k}.csv", f_ventana)
                        for k in (1, 10)}

    plt, coma = c.configurar_matplotlib()
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.9), gridspec_kw={"wspace": 0.3})
    ax = axs[0]
    bins = np.logspace(-1, 4, 51)
    ax.hist(roi["_todos"], bins=bins, color="C0", alpha=0.8, label="Referencia (S0, 30 d)")
    for f, col in [(0.1, "C1"), (0.01, "C3")]:
        ax.hist(roi["_todos"] * f, bins=bins, histtype="step", color=col, label=f"Fracción {f:g} (valor medio)".replace(".", ","))
    ax.axvline(C_OBJETIVO, color="k", ls="--", lw=0.8)
    ax.text(C_OBJETIVO * 1.1, ax.get_ylim()[1] * 0.9, "400 (5 %)", fontsize=7)
    ax.set_xscale("log")
    ax.set_xlabel("Conteo por ROI de 4×4 píxeles")
    ax.set_ylabel("ROI (114 vistas)")
    ax.set_title("ROI con columna de roca 3·10⁴–10⁵ g/cm²")
    ax.legend(fontsize=7)
    ax.xaxis.set_major_formatter(coma)
    ax = axs[1]
    kk = [o["k"] for o in opciones]
    ax.plot(kk, [100 * o["fraccion_rois_banda_con_objetivo"] for o in opciones], "o-", color="C0")
    ax.set_xlabel("Multiplicador k de N (N = k·S0 v1)")
    ax.set_ylabel("ROI que alcanzan 400 cuentas (%)", color="C0")
    ax2 = ax.twinx()
    ax2.plot(kk, [o["horas_nucleo"] for o in opciones], "s--", color="C3")
    ax2.set_ylabel("Horas-núcleo (legacy)", color="C3")
    ax2.grid(False)
    ax.set_xscale("log", base=2)
    ax.set_xticks(kk, [str(k) for k in kk])
    ax.set_title("Estadística frente a cómputo")
    ax.yaxis.set_major_formatter(coma)
    ax2.yaxis.set_major_formatter(coma)
    ruta = c.guardar_figura(fig, "fig6-estadistica-roi.png")
    plt.close(fig)

    roi.pop("_todos")
    salida = {"tiempos_medidos": t, "estadistica_roi": roi, "almacenamiento_medido": alm,
              "opciones_receta_historica": opciones,
              "receta_validada": {"factor_conteo_roi": factor, "fraccion_en_ventana": f_ventana,
                                  "nucleo_s_por_evento_en_ventana": cs_ventana,
                                  "k_para_100_cuentas_p10": k_10, "k_para_400_cuentas_p10": k_5,
                                  "opciones": opciones_receta,
                                  "supuesto": "factor medido en geo-train-01 vista 0; se verifica en P0"},
              "parametros": {
                  "fracciones": FRACCIONES, "realizaciones": REALIZACIONES, "cpus": CPUS,
                  "max_simultaneos": MAX_SIMULTANEOS, "eventos_max_bloque": EVENTOS_MAX_BLOQUE,
                  "semilla_maestra_v1": SEMILLA_MAESTRA_V1,
                  "regla_semilla": "maestra*1e6 + indice_geometria*1e4 + vista*1e3 + bloque (orden alfabético del catálogo)"},
              "manifiestos": {f"k{k}": {"ruta": c.ruta_relativa(c.ENTREGA / "produccion" / f"manifiesto-receta-k{k}.csv"),
                                        "filas": n} for k, n in filas_manifiesto.items()},
              "figura": ruta, "entorno": c.entorno()}
    c.escribir_json(c.RESULTADOS / "plan-produccion.json", salida)
    print(json.dumps({"receta": salida["receta_validada"]}, indent=1, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()

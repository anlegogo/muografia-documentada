"""Lectura verificada de los cortes de imagen del OE2 y utilidades comunes.

Entrada: ../../fuentes/datos_figuras/cortes_oe2.npz, extraído con
extraer_cortes_wsl.py de las matrices auditadas de la evaluación final, tras
comprobar las 36 huellas SHA-256 registradas por la dirección (revisión 166be6f).
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

DATOS = Path(__file__).resolve().parent / "datos" / "oe2"
S = 8.239329427901795          # escala de normalización ajustada con entrenamiento
GEOS = ["geo-test-01", "geo-test-02", "geo-test-03", "geo-gen-01"]
MODELOS = ["unet_original", "cgan_original", "B1_C0", "B1_C1", "B2_C0", "B2_C1", "B3_C0", "B3_C1"]
ROTULO = {"referencia": "Referencia", "entrada": r"Entrada, $f=0{,}05$", "unet_original": "U-Net",
          "cgan_original": "cGAN", "B1_C0": "B1 -- C0", "B1_C1": "B1 -- C1", "B2_C0": "B2 -- C0",
          "B2_C1": "B2 -- C1", "B3_C0": "B3 -- C0", "B3_C1": "B3 -- C1"}


def T(c: np.ndarray) -> np.ndarray:
    l = np.log1p(np.asarray(c, dtype=np.float64))
    return l / (S + l)


def cortes() -> dict:
    huellas = {}
    for linea in (DATOS / "huellas.sha256").read_text(encoding="utf-8").splitlines():
        if linea.strip():
            h, n = linea.split(maxsplit=1)
            huellas[n.strip().lstrip("*")] = h
    ruta = DATOS / "cortes_oe2.npz"
    if hashlib.sha256(ruta.read_bytes()).hexdigest() != huellas["cortes_oe2.npz"]:
        raise SystemExit("Huella distinta en cortes_oe2.npz")
    with np.load(ruta) as d:
        z = {k: d[k] for k in d.files}
    out = {}
    for g in GEOS:
        el, az = z[f"{g}/meta/el_edges_deg"], z[f"{g}/meta/az_edges_deg"]
        assert el[0] < el[-1] and az[0] < az[-1], "orientación inesperada"
        assert z[f"{g}/ref"][-20:].mean() > z[f"{g}/ref"][:20].mean(), "filas no ordenadas por elevación"
        img = {"referencia": T(z[f"{g}/ref"]), "entrada": T(z[f"{g}/low"])}
        img.update({m: z[f"{g}/{m}"] for m in MODELOS})
        out[g] = {"img": img, "extent": (float(az[0]), float(az[-1]), float(el[0]), float(el[-1]))}
    return out


def escala_comun(d: dict) -> float:
    """Máximo de T entre todos los paneles de las cuatro geometrías, redondeado hacia
    arriba a la centésima. Es una sola escala para todas las imágenes de las figuras
    (no se ajusta por imagen); T(C) = 0,5 corresponde a la cuenta máxima de
    entrenamiento, de modo que el intervalo [0, 1] dejaría sin uso la mitad del mapa."""
    return float(np.ceil(100 * max(float(v.max()) for g in d.values() for v in g["img"].values())) / 100)

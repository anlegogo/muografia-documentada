"""Lectura verificada de las evidencias del OE2 y de las curvas del OE3.

Entradas (copias obtenidas con git show desde anlegogo/muografia-documentada,
origin/main 08cdc0c; véase ../../fuentes/datos_ef01/ORIGEN.txt):
  - oe2_evidencias_ef01-c2_resultados.json: evaluación final EF-01 con la
    corrección C2 (macropromedios y valores por geometría);
  - oe3_evidencias_curvas-v1_curvas.json: curvas descriptivas de la entrada
    sin red al 1, 5, 10 y 50 %.
Cada archivo se contrasta con huellas.sha256 antes de leerlo.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

DATOS = Path(__file__).resolve().parent / "datos" / "oe2"

MODELOS = ["entrada", "unet_original", "cgan_original",
           "B1_C0", "B1_C1", "B2_C0", "B2_C1", "B3_C0", "B3_C1"]
GEOMETRIAS = {"test": ["geo-test-01", "geo-test-02", "geo-test-03"],
              "generalization": ["geo-gen-01"]}


def _leer(nombre: str) -> dict:
    huellas = {}
    for linea in (DATOS / "huellas.sha256").read_text(encoding="utf-8").splitlines():
        if linea.strip():
            h, n = linea.split(maxsplit=1)
            huellas[n.strip().lstrip("*")] = h
    ruta = DATOS / nombre
    if hashlib.sha256(ruta.read_bytes()).hexdigest() != huellas[nombre]:
        raise SystemExit(f"Huella distinta en {nombre}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def resultados_c2() -> dict:
    return _leer("oe2_evidencias_ef01-c2_resultados.json")


def curvas() -> dict:
    return _leer("oe3_evidencias_curvas-v1_curvas.json")

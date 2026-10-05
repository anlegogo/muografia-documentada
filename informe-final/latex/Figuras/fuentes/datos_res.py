"""Lectura verificada de las evidencias del director para las figuras res_* del capítulo 4.

Copias obtenidas con git show desde anlegogo/muografia-documentada, origin/main
9558099 (ver ../datos/ORIGEN.txt). Cada archivo se contrasta con ../datos/huellas.sha256.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

DATOS = Path(__file__).resolve().parent / "datos" / "director"


def _verificar(nombre: str) -> Path:
    huellas = {}
    for linea in (DATOS / "huellas.sha256").read_text(encoding="utf-8").splitlines():
        if linea.strip():
            h, n = linea.split(maxsplit=1)
            huellas[n.strip().lstrip("*")] = h
    ruta = DATOS / nombre
    if hashlib.sha256(ruta.read_bytes()).hexdigest() != huellas[nombre]:
        raise SystemExit(f"Huella distinta en {nombre}")
    return ruta


def sintesis() -> list[dict]:
    with _verificar("sintesis_metricas.csv").open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def opacidad() -> list[dict]:
    with _verificar("opacidad_nominal.csv").open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def datos_figuras_oe1() -> dict:
    return json.loads(_verificar("datos-figuras.json").read_text(encoding="utf-8"))

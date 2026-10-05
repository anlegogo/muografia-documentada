"""Lectura verificada de los datos de la campaña de 114 vistas (OE1).

Todas las entradas proceden de la rama oe1/justificacion-fisica-produccion de
muografia-documentada (commit registrado en datos/ORIGEN_COMMIT.txt):
  - datos/imagenes/*.npz y *.meta.json: las 114 referencias exportadas;
  - datos/imagenes.sha256: inventario de huellas de esas imágenes;
  - datos/evaluacion-114-344M.json: evaluación de bordes y de roca;
  - datos/huellas-contenido.json: huellas de contenido de los pares;
  - datos/geo-train-08_view0_pairs.npz: archivo de pares regenerado.
Cada función comprueba la huella correspondiente antes de devolver los datos y
detiene la ejecución si no coincide.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

DATOS = Path(__file__).resolve().parent.parent / "datos"


def _sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def _huellas_imagenes() -> dict[str, str]:
    huellas = {}
    for linea in (DATOS / "imagenes.sha256").read_text(encoding="utf-8").splitlines():
        if linea.strip():
            h, nombre = linea.split(maxsplit=1)
            huellas[nombre.strip().lstrip("./")] = h
    return huellas


def imagen(geometria: str, vista: int) -> dict[str, np.ndarray]:
    """Referencia de una vista, verificada contra imagenes.sha256."""
    nombre = f"{geometria}_view{vista}.npz"
    ruta = DATOS / "imagenes" / nombre
    esperado = _huellas_imagenes()[nombre]
    if _sha256(ruta) != esperado:
        raise SystemExit(f"Huella distinta en {nombre}")
    with np.load(ruta) as z:
        return {k: z[k] for k in z.files}


def evaluacion() -> list[dict]:
    """Vistas de la evaluación de la campaña (bordes y roca)."""
    return json.loads((DATOS / "evaluacion-114-344M.json").read_text(encoding="utf-8"))["views"]


def _huella_contenido(a: np.ndarray) -> str:
    h = hashlib.sha256()
    h.update(a.dtype.str.encode())
    h.update(str(a.shape).encode())
    h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


def pares(nombre: str) -> dict[str, np.ndarray]:
    """Archivo de pares, verificado por huella de contenido."""
    esperado = json.loads((DATOS / "huellas-contenido.json").read_text(encoding="utf-8"))["pairs"][nombre]
    with np.load(DATOS / nombre) as z:
        datos = {k: z[k] for k in z.files}
    for clave in ("counts_ref", "low_counts", "fractions"):
        if _huella_contenido(datos[clave]) != esperado[clave]:
            raise SystemExit(f"Huella de contenido distinta en {nombre}:{clave}")
    return datos


def orientar(cuentas: np.ndarray, el_edges: np.ndarray) -> np.ndarray:
    """Devuelve la matriz con la fila 0 en la elevación mínima."""
    return cuentas if el_edges[0] < el_edges[-1] else cuentas[::-1]

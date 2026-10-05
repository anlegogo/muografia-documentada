"""Regenera las figuras del capítulo 2 (Marco teórico) desde sus fuentes TikZ/PGFPlots.

Compila cada fuente con pdfLaTeX en un directorio temporal, copia el PDF a la carpeta
Figuras/ (un nivel arriba de este script) y comprueba que el resultado sea vectorial:
sin imágenes raster incrustadas y con todas las fuentes tipográficas incrustadas.

Uso (desde cualquier carpeta):
    python generar_figuras.py            # todas las figuras del capítulo 2
    python generar_figuras.py fig2-3     # solo las que empiezan por ese prefijo
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FUENTES = Path(__file__).resolve().parent
SALIDA = FUENTES.parent
FIGURAS = ["fig2-1_opacidad_proyeccion", "fig2-2_ruido_conteo", "fig2-3_gan_condicional"]


def compilar(nombre: str) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        orden = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 f"-output-directory={tmp}", str(FUENTES / f"{nombre}.tex")]
        r = subprocess.run(orden, cwd=FUENTES, capture_output=True, text=True, errors="replace")
        pdf = Path(tmp) / f"{nombre}.pdf"
        if r.returncode != 0 or not pdf.exists():
            errores = [l for l in r.stdout.splitlines() if l.startswith("!")]
            raise SystemExit(f"Fallo al compilar {nombre}: {errores[:3]}")
        destino = SALIDA / f"{nombre}.pdf"
        shutil.copyfile(pdf, destino)
    return destino


def comprobar_vectorial(pdf: Path) -> str:
    if not (shutil.which("pdfimages") and shutil.which("pdffonts")):
        return "sin comprobación (faltan pdfimages/pdffonts de Poppler)"
    imagenes = subprocess.run(["pdfimages", "-list", str(pdf)], capture_output=True, text=True).stdout
    raster = len(imagenes.splitlines()[2:])
    fuentes = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout
    no_incrustadas = sum(1 for l in fuentes.splitlines()[2:] if l.split()[-5] != "yes")
    if raster or no_incrustadas:
        raise SystemExit(f"{pdf.name}: {raster} imágenes raster, {no_incrustadas} fuentes sin incrustar")
    return "vectorial, fuentes incrustadas"


def main() -> None:
    if not shutil.which("pdflatex"):
        raise SystemExit("Se requiere pdflatex (TeX Live o MiKTeX); ver requirements.txt")
    prefijos = sys.argv[1:]
    for nombre in FIGURAS:
        if prefijos and not any(nombre.startswith(p) for p in prefijos):
            continue
        pdf = compilar(nombre)
        print(f"{pdf.name}: {comprobar_vectorial(pdf)}")


if __name__ == "__main__":
    main()

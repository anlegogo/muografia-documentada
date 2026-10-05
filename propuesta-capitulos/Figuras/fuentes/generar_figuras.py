"""Regenera las figuras de los capítulos 2, 3 y 4 desde sus fuentes.

Cada figura tiene en esta carpeta una fuente con el mismo nombre que su PDF:
  - .tex (TikZ/PGFPlots): se compila con pdfLaTeX en un directorio temporal;
  - .py (Matplotlib): se ejecuta con el mismo intérprete de Python que este script.
Los PDF se escriben en Figuras/ (un nivel arriba). Después se comprueba que cada
resultado sea vectorial: sin imágenes raster incrustadas y con las fuentes tipográficas
incrustadas. Los scripts de datos verifican las huellas SHA-256 de sus entradas
(carpeta datos/) antes de dibujar y se detienen si no coinciden.

Uso (desde cualquier carpeta):
    python generar_figuras.py                 # todas las figuras
    python generar_figuras.py met_04 res_0    # solo las que empiezan por esos prefijos
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FUENTES = Path(__file__).resolve().parent
SALIDA = FUENTES.parent

FIGURAS = [
    # Capítulo 2 (Marco teórico)
    "fig2-1_opacidad_proyeccion.tex", "fig2-2_ruido_conteo.tex", "fig2-3_gan_condicional.tex",
    # Capítulo 3 (Metodología)
    "met_01_flujo_cerrado.tex", "met_02_escenario_y_vistas.py", "met_03_malla_angular.py",
    "met_04_pares_conteo.py", "met_05_normalizacion.py", "met_06_generador_critico.py",
    "met_07_secuencia_ensayos.py", "met_08_regiones_evaluacion.py", "met_09_evaluacion_multifraccion.tex",
    # Capítulo 4 (Resultados y discusión)
    "res_01_referencias_vector.py", "res_02_bordes.py", "res_03_roca_vector.py", "res_04_compromiso.py",
    "res_05_borde.py", "res_06_comparacion_vector.py", "res_07_multifraccion_vector.py",
    "res_08_opacidad_nominal.py",
]


def compilar_tex(fuente: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        orden = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={tmp}", str(fuente)]
        r = subprocess.run(orden, cwd=FUENTES, capture_output=True, text=True, errors="replace")
        pdf = Path(tmp) / f"{fuente.stem}.pdf"
        if r.returncode != 0 or not pdf.exists():
            errores = [l for l in r.stdout.splitlines() if l.startswith("!")]
            raise SystemExit(f"Fallo al compilar {fuente.name}: {errores[:3]}")
        shutil.copyfile(pdf, SALIDA / f"{fuente.stem}.pdf")


def ejecutar_py(fuente: Path) -> None:
    entorno = {**os.environ, "FIGURAS_DIR": str(SALIDA), "MPLBACKEND": "Agg"}
    r = subprocess.run([sys.executable, fuente.name], cwd=FUENTES, env=entorno,
                       capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"Fallo al ejecutar {fuente.name}:\n{r.stderr[-1500:]}")


def comprobar_vectorial(pdf: Path) -> str:
    if not (shutil.which("pdfimages") and shutil.which("pdffonts")):
        return "generada (sin comprobación: faltan pdfimages/pdffonts de Poppler)"
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
        fuente = FUENTES / nombre
        compilar_tex(fuente) if fuente.suffix == ".tex" else ejecutar_py(fuente)
        pdf = SALIDA / f"{fuente.stem}.pdf"
        print(f"{pdf.name}: {comprobar_vectorial(pdf)}", flush=True)


if __name__ == "__main__":
    main()

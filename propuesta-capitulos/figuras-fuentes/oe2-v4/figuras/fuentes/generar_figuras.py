"""Regenera todas las figuras y tablas del OE2 y del OE3 (capítulos 3 y 4, versión 4).

Uso (desde esta carpeta, con el entorno C:\\Users\\USER\\.venvs\\tesis-figuras y
pdflatex de MiKTeX en el PATH):
    python generar_figuras.py
Salidas: ../pdf/*.pdf (vectoriales, fuentes incrustadas) y ../tablas/*.tex.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PDF = AQUI.parent / "pdf"

TIKZ = ["fig3-5_arquitecturas.tex", "fig3-6_flujo_oe2.tex"]
PYTHON = ["fig4-4_compromiso.py", "fig4-5_borde.py", "fig4-6_curvas_exposicion.py",
          "fig4-7_comparacion_fija.py", "fig4-8_caso_desfavorable.py", "tablas_cap4.py"]


def main() -> None:
    PDF.mkdir(exist_ok=True)
    for f in TIKZ:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                        f"-output-directory={PDF}", f], cwd=AQUI, check=True,
                       stdout=subprocess.DEVNULL)
        for ext in (".aux", ".log"):
            (PDF / f.replace(".tex", ext)).unlink(missing_ok=True)
        print("TikZ:", f)
    for f in PYTHON:
        subprocess.run([sys.executable, f], cwd=AQUI, check=True)


if __name__ == "__main__":
    main()

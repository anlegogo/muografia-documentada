"""Regenera las siete figuras del OE1 (capítulos 3 y 4) con un solo comando.

Uso (desde esta carpeta, con el entorno de figuras activo):
    python generar_figuras.py

Las figuras de datos se generan con Matplotlib (backend PGF + pdfLaTeX) y verifican
las huellas de sus entradas antes de graficar; los diagramas se compilan desde su
fuente TikZ con pdflatex. Todas las salidas quedan en ../pdf/.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PDF = AQUI.parent / "pdf"
SCRIPTS = ["fig3-2_catalogo_cortes.py", "fig3-4_ejemplo_pares.py", "fig4-1_referencias.py",
           "fig4-2_bordes.py", "fig4-3_roca.py"]
TIKZ = ["fig3-1_flujo_oe1.tex", "fig3-3_geometria_observacion.tex"]


def main() -> None:
    PDF.mkdir(exist_ok=True)
    for s in SCRIPTS:
        subprocess.run([sys.executable, s], cwd=AQUI, check=True)
    for t in TIKZ:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                        f"-output-directory={PDF}", t], cwd=AQUI, check=True,
                       stdout=subprocess.DEVNULL)
    for extra in PDF.glob("*.aux"):
        extra.unlink()
    for extra in PDF.glob("*.log"):
        extra.unlink()
    print("figuras regeneradas en", PDF)


if __name__ == "__main__":
    main()

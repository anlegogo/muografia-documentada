# Figuras y tablas del OE2 y del OE3 — versión 4

Figuras vectoriales generadas desde su fuente para los capítulos 3 y 4. Los datos son copias obtenidas con `git show` desde `anlegogo/muografia-documentada`, `origin/main` = `08cdc0c`. Están en `../fuentes/datos_ef01/`, junto con `ORIGEN.txt` y `huellas.sha256`. Cada script verifica la huella SHA-256 de sus datos antes de leerlos.

| Figura en el libro | Archivo | Fuente | Tipo | Datos |
|---|---|---|---|---|
| 3.2 Flujo del OE2 y del OE3 | `pdf/fig3-6_flujo_oe2.pdf` | `fuentes/fig3-6_flujo_oe2.tex` | TikZ | — |
| 3.6 Arquitecturas U-Net y PatchGAN | `pdf/fig3-5_arquitecturas.pdf` | `fuentes/fig3-5_arquitecturas.tex` | TikZ | Implementación v1 (capas y parámetros comprobados a mano: 20.543.809 y 2.762.817) |
| 4.4 Compromiso SSIM/PSNR frente a Q | `pdf/fig4-4_compromiso.pdf` | `fuentes/fig4-4_compromiso.py` | Matplotlib (PGF) | `oe2_evidencias_ef01-c2_resultados.json` |
| 4.5 Comparación fija de imágenes | `pdf/fig4-7_comparacion_fija.pdf` | `fuentes/fig4-7_comparacion_fija.py` | Matplotlib (PGF); matrices a 256 × 256 sin interpolar | `cortes_oe2.npz` |
| 4.6 Caso desfavorable y residuos | `pdf/fig4-8_caso_desfavorable.pdf` | `fuentes/fig4-8_caso_desfavorable.py` | ídem | `cortes_oe2.npz` y resultados C2 |
| 4.7 Error de borde por geometría | `pdf/fig4-5_borde.pdf` | `fuentes/fig4-5_borde.py` | Matplotlib (PGF) | resultados C2 |
| 4.8 Curvas de exposición | `pdf/fig4-6_curvas_exposicion.pdf` | `fuentes/fig4-6_curvas_exposicion.py` | Matplotlib (PGF) | `oe3_evidencias_curvas-v1_curvas.json` y resultados C2 |
| Tablas 4.4 a 4.7 (filas) | `tablas/*.tex` | `fuentes/tablas_cap4.py` | — | Resultados C2, entrega original EF-01 y curvas |

Los nombres de archivo de las figuras TikZ no coinciden con su número final, porque la numeración es automática. El estilo es el mismo de las figuras del OE1 (`estilo_tesis.py`): Latin Modern, coma decimal y paleta Paul Tol *bright*.

## Regenerar todo

```bash
cd fuentes && python generar_figuras.py
```

Requiere el entorno `C:\Users\USER\.venvs\tesis-figuras` y pdflatex de MiKTeX. Después, los capítulos se reconstruyen con `python ../fragmentos/integrar_cap3.py`, `integrar_cap4.py` e `integrar_cap5.py`, que parten de `base-v3/`. Al regenerarlos se obtienen archivos idénticos byte a byte a los del libro de prueba.

## Figuras de imágenes (4.5 y 4.6, informe de la dirección `166be6f`)

Reproducen, con el estilo del libro, la regla de selección del informe académico del OE2 de la dirección: vista 0 y realización 0 de las cuatro geometrías reservadas, y como caso desfavorable la geometría con mayor Q de la cGAN original (geo-test-03, Q = 27,835 %).

Los cortes se extrajeron en WSL con `fuentes/extraer_cortes_wsl.py`, desde las matrices auditadas (`~/evalfinal`), y se guardaron en `../fuentes/datos_figuras/cortes_oe2.npz` (7,7 MB). Antes de leerlas, el script comprobó las **36 huellas SHA-256** del registro de procedencia de la dirección (`procedencia-figuras-direccion.json`).

- El límite de los residuos, 0,350312, coincide con el del director.
- La escala de T es común a todos los paneles, [0; 0,52]. No es [0, 1] porque T(C) = 0,5 corresponde a la cuenta máxima de entrenamiento.
- Las matrices se incrustan a 256 × 256 sin interpolación.

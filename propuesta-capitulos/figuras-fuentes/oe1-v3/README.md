# Figuras del OE1 — versión 3 (capítulos 3 y 4)

Figuras vectoriales generadas desde su fuente para el libro de tesis. Datos de la campaña de 114 vistas de `muografia-documentada`, rama `oe1/justificacion-fisica-produccion` (commit en `datos/ORIGEN_COMMIT.txt`; entrega de datos `f395570`).

| Figura | Fuente | Tipo | Entradas verificadas |
|---|---|---|---|
| 3.1 Cadena de generación y verificación | `fuentes/fig3-1_flujo_oe1.tex` | TikZ | — |
| 3.2 Cortes de densidad del catálogo | `fuentes/fig3-2_catalogo_cortes.py` | Matplotlib (PGF) | JSON del catálogo; malla de 1,5 m incrustada a resolución nativa |
| 3.3 Geometría de observación | `fuentes/fig3-3_geometria_observacion.tex` | TikZ | — |
| 3.4 Referencia y realizaciones | `fuentes/fig3-4_ejemplo_pares.py` | Matplotlib (PGF) | `geo-train-08_view0_pairs.npz` contra `huellas-contenido.json` |
| 4.1 Seis referencias | `fuentes/fig4-1_referencias.py` | Matplotlib (PGF) | imágenes contra `imagenes.sha256` |
| 4.2 Regiones de borde | `fuentes/fig4-2_bordes.py` | Matplotlib (PGF) | `evaluacion-114-344M.json` |
| 4.3 Suficiencia en roca | `fuentes/fig4-3_roca.py` | Matplotlib (PGF) | `evaluacion-114-344M.json` |

**Regenerar todo:** `cd fuentes && python generar_figuras.py` (entorno con matplotlib, numpy y cmcrameri; pdflatex con TikZ y Latin Modern).

Estilo común en `fuentes/estilo_tesis.py`: Latin Modern (T1), coma decimal, 7,5–8,5 pt, mapas de Crameri (batlow), paleta Paul Tol *bright* en diagramas. Las matrices de conteo y densidad se incrustan a su resolución nativa sin interpolación (`interpolation="none"`); ejes, rótulos y barras de color son vectoriales. Ancho máximo 15 cm; insertar a tamaño natural con `\includegraphics{...}`.

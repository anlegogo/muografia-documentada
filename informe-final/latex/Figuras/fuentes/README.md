# Fuentes de las figuras de los capítulos 2, 3 y 4

Cada PDF de `Figuras/` tiene aquí una fuente con el mismo nombre:
- `.tex` (TikZ/PGFPlots) para esquemas y curvas analíticas;
- `.py` (Matplotlib) para las figuras que leen datos.

Todas producen PDF vectorial, sin imágenes raster incrustadas y con las fuentes tipográficas incrustadas.

## Regenerar

```bash
pip install -r requirements.txt
python generar_figuras.py                # las 20 figuras
python generar_figuras.py met_04 res_0   # solo las que empiezan por esos prefijos
```

El script hace tres cosas:
1. compila cada `.tex` con pdfLaTeX o ejecuta cada `.py`;
2. escribe el PDF en `Figuras/`;
3. comprueba con `pdfimages` y `pdffonts` que sea vectorial.

Los scripts de datos verifican las huellas SHA-256 de sus entradas antes de dibujar y se detienen si alguna no coincide. Los requisitos están en `requirements.txt`: Python con NumPy, Matplotlib y cmcrameri, más pdfLaTeX.

**Registro de la entrega de los estudiantes (2026-10-04):** se informó regeneración de las 20 figuras y coincidencia píxel a píxel con los PDF de esa entrega.

**Revisión editorial posterior:** se modificaron y regeneraron `met_09`, `res_06`, `res_07` y `res_08` para corregir el esquema de agregación y mejorar la legibilidad. Sus PDF actuales ya no son idénticos a los de la entrega anterior. Se comprobó que los cuatro no contienen imágenes raster y tienen las fuentes incrustadas. Los datos de entrada se conservaron; la revisión posterior no volvió a ejecutar las otras 16 fuentes.

## Figuras

| Figura | Fuente | Herramienta | Datos de entrada |
|---|---|---|---|
| 2.1 Imagen por transmisión como proyección | `fig2-1_opacidad_proyeccion.tex` | TikZ | — (esquema) |
| 2.2 Estadística de conteo de Poisson | `fig2-2_ruido_conteo.tex` | PGFPlots | — (curvas analíticas) |
| 2.3 GAN condicional de Wasserstein | `fig2-3_gan_condicional.tex` | TikZ | — (esquema) |
| 3.1 Secuencia experimental y particiones | `met_01_flujo_cerrado.tex` | TikZ | — (esquema) |
| 3.2 Geometría y posiciones de observación | `met_02_escenario_y_vistas.py` | Matplotlib | valores del catálogo transcritos en el script |
| 3.3 Coordenadas y malla angular | `met_03_malla_angular.py` | Matplotlib | `datos/oe1/imagenes/geo-train-06_view0.npz`, `datos/oe1/pares/` |
| 3.4 Referencia y pares de conteo | `met_04_pares_conteo.py` | Matplotlib | `datos/oe1/pares/geo-train-06_view3_pairs.npz` |
| 3.5 Normalización y recuperación de cuentas | `met_05_normalizacion.py` | Matplotlib | escala `s` transcrita en el script |
| 3.6 Generador U-Net y crítico | `met_06_generador_critico.py` | Matplotlib | formas de capa transcritas en el script |
| 3.7 Secuencia de ensayos | `met_07_secuencia_ensayos.py` | Matplotlib | — (esquema) |
| 3.8 Regiones y controles de evaluación | `met_08_regiones_evaluacion.py` | Matplotlib | `datos/oe1/imagenes/geo-train-08_view0.npz`, `_codigo_director/` |
| 3.9 Evaluación multifracción | `met_09_evaluacion_multifraccion.tex` | TikZ | — (esquema) |
| 4.1 Referencias del conjunto | `res_01_referencias_vector.py` | Matplotlib | `datos/oe1/imagenes/`, `datos/director/datos-figuras.json` |
| 4.2 Control de bordes | `res_02_bordes.py` | Matplotlib | `datos/oe1/evaluacion-114-344M.json` |
| 4.3 Suficiencia de conteo en roca | `res_03_roca_vector.py` | Matplotlib | `datos/director/datos-figuras.json` |
| 4.4 Comparación en casos fijados | `res_06_comparacion_vector.py` | Matplotlib | `datos/oe2/cortes_oe2.npz` |
| 4.5 Similitud frente a sesgo regional | `res_04_compromiso.py` | Matplotlib | `datos/oe2/oe2_evidencias_ef01-c2_resultados.json` |
| 4.6 Error de borde por geometría | `res_05_borde.py` | Matplotlib | `datos/oe2/oe2_evidencias_ef01-c2_resultados.json` |
| 4.7 Multifracción | `res_07_multifraccion_vector.py` | Matplotlib | `datos/director/sintesis_metricas.csv` |
| 4.8 Opacidad nominal | `res_08_opacidad_nominal.py` | Matplotlib | `datos/director/opacidad_nominal.csv` |

La numeración corresponde al documento compilado. En el capítulo 4, la figura `res_06` aparece antes que `res_04` y `res_05`.

## Módulos comunes

- `estilo_tesis.py`: estilo de las figuras `met_*`, que es el estilo común del documento. Incluye `FIGURAS_DIR` para cambiar la carpeta de salida.
- `guardar_vector.py`: guardado con el backend PDF y usetex para las mallas de 256 × 256 celdas (`met_04`, `met_08`).
- `estilo_res.py`: estilo de las figuras `res_*` (backend PGF, Latin Modern, coma decimal).
- `celdas_vectoriales.py`: dibuja matrices de conteo como polígonos vectoriales sin interpolación y construye barras de color vectoriales (`res_01`, `res_06`).
- Lectores con verificación de huellas:
  - `datos_res.py` lee `datos/director/`;
  - `datos_campana.py` lee `datos/oe1/`;
  - `datos_oe2.py` e `imagenes_oe2.py` leen `datos/oe2/`.

## Datos (`datos/`)

Solo se incluyen los archivos que usan las figuras. Cada subcarpeta tiene un `ORIGEN.txt` y huellas SHA-256.

- `director/`: `sintesis_metricas.csv`, `opacidad_nominal.csv` y `datos-figuras.json`, copiados de `anlegogo/muografia-documentada` (`main` `9558099`).
- `oe1/`: subconjunto de la campaña de 114 vistas (entrega `f395570`):
  - ocho referencias de `imagenes/`;
  - la evaluación de bordes y roca;
  - el archivo de pares de `geo-train-06`, vista 3.
- `oe2/`: cortes de imagen de EF-01, extraídos de las matrices auditadas tras verificar las 36 huellas de la dirección (`166be6f`), y los resultados EF-01-C2 (`08cdc0c`).

`_codigo_director/` conserva el evaluador de regiones geométricas, el protocolo de regiones y las geometrías de entrenamiento que usa `met_08` (`origin/main` `f1094d7`), con huellas comprobadas por el script.

## Procedencia

- `met_02` a `met_08`: Daniel Pinto, rama `docs/caps-1-2` de `muography-thesis`. Solo se cambiaron las rutas de datos y de salida, que ahora son relativas a esta carpeta.
- `res_02`, `res_04` y `res_05` proceden de `fig4-2_bordes`, `fig4-4_compromiso` y `fig4-5_borde`, con el nombre que usa el capítulo 4.

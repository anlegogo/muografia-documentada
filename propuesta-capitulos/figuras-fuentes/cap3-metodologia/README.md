# Figuras del capítulo 3 (Metodología)

Fuentes editables de las nueve figuras solicitadas en el capítulo 3 de la plantilla de Overleaf del director (macro `\FiguraPendienteMet`). Cada PDF está en `manuscrito/Figuras/` con el nombre exacto que espera el capítulo, de modo que reemplaza automáticamente el recuadro «Figura por elaborar».

| Figura | Archivo | Script | Origen de los datos |
|---|---|---|---|
| Secuencia experimental y separación de las particiones | `met_01_flujo_experimental.pdf` | `fuentes/met_01_flujo_experimental.py` | Protocolo e instrucciones de evaluación final OE2 (`muografia-documentada`) |
| Geometría idealizada, anomalías y seis vistas | `met_02_escenario_y_vistas.pdf` | `fuentes/met_02_escenario_y_vistas.py` | Catálogo `geo-train-08.json`, `GeometryConfig.hh`, ficha OE1 y receta operativa |
| Correspondencia dirección–coordenadas | `met_03_malla_angular.pdf` | `fuentes/met_03_malla_angular.py` | `imagenes/geo-train-06_view0.npz` (campaña 114) |
| Entradas reducidas desde una referencia finita | `met_04_pares_conteo.pdf` | `fuentes/met_04_pares_conteo.py` | `pares/geo-train-06_view3_pairs.npz`, realización 0 (campaña 114) |
| Transformación y recuperación de cuentas | `met_05_normalizacion.pdf` | `fuentes/met_05_normalizacion.py` | `muography_dataset.py`, `datos_ajuste.py`, `contrato-datos-v1.json` |
| Arquitectura U-Net y crítico | `met_06_generador_critico.pdf` | `fuentes/met_06_generador_critico.py` | `unet_generator.py`, `patch_critic.py`, `losses.py` |
| Desarrollo experimental y modelos finales | `met_07_secuencia_ensayos.pdf` | `fuentes/met_07_secuencia_ensayos.py` | Configuraciones y diseños de los ensayos OE2 |
| Regiones geométricas y controles | `met_08_regiones_evaluacion.pdf` | `fuentes/met_08_regiones_evaluacion.py` | `geo-train-08.json`, `geo-train-08_view0.npz`, evaluador de regiones del director |
| Comparación descriptiva de fracciones | `met_09_diseno_curvas.pdf` | `fuentes/met_09_diseno_curvas.py` | Esquema sin datos |

El encabezado de cada script registra las rutas de los archivos de entrada, sus huellas SHA-256 y el commit de origen en `anlegogo/muografia-documentada`. Los scripts de datos verifican esas huellas antes de dibujar. Ninguna figura usa las particiones de prueba (`geo-test-01..03`) ni de generalización (`geo-gen-01`).

## Estilo común

`fuentes/estilo_tesis.py` define una sola paleta para todo el documento, con un significado fijo por color: OE1, OE2 y OE3; cielo, roca, borde, anomalía y controles; entrada sin red, U-Net y cGAN. Las particiones reservadas se dibujan en negro rayado. Los conteos usan el mapa `cividis` con barra de color. La tipografía es Latin Modern con coma decimal y las figuras miden 15 cm de ancho. Todas son PDF vectoriales, sin imágenes incrustadas.

`fuentes/guardar_vector.py` guarda las figuras con mallas de 256 × 256 celdas (`met_04`, `met_08`) mediante el backend PDF nativo con LaTeX, porque el backend PGF excede la memoria de pdfTeX.

`fuentes/_codigo_director/` conserva copias del código y los datos del director que usa `met_08`: el evaluador de regiones geométricas, el protocolo de regiones, las geometrías de entrenamiento y las huellas de contenido. Se extrajeron de `origin/main` en `f1094d7`, y el script comprueba sus huellas.

## Regenerar

Requiere Python con NumPy y Matplotlib 3.11, además de pdfLaTeX con `lmodern`. Desde `fuentes/`:

```bash
export DATOS_OE1=/ruta/datos-oe1-campana-114   # imagenes/ y pares/ de la campaña 114
python met_04_pares_conteo.py                   # escribe ../../../Figuras/met_04_pares_conteo.pdf
```

`FIGURAS_DIR` permite cambiar la carpeta de salida. Los scripts `met_01`, `met_02`, `met_05`, `met_06`, `met_07` y `met_09` no leen archivos: llevan transcritos los valores tomados del repositorio `muografia-documentada` (dimensiones del catálogo, escala `s`, formas de capa y número de parámetros), con la fuente y el commit indicados en su encabezado.

## Huellas SHA-256 de los PDF

```
f746af11414a6454…  met_01_flujo_experimental.pdf
434c0ec1ded978c9…  met_02_escenario_y_vistas.pdf
8bbf6796be499bf7…  met_03_malla_angular.pdf
d71c787453d6f4a1…  met_04_pares_conteo.pdf
4d232ade241a478b…  met_05_normalizacion.pdf
8218fa87cf2da7a2…  met_06_generador_critico.pdf
ef18833865ced700…  met_07_secuencia_ensayos.pdf
6b398cf8e3f1ffb5…  met_08_regiones_evaluacion.pdf
def36a0494173047…  met_09_diseno_curvas.pdf
```

Las huellas completas están en `huellas-figuras.sha256`.

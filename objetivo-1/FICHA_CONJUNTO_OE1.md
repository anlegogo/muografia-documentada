# Ficha del conjunto sintético del OE1

Versión documental: 2026-10-03. Datos revisados: entrega estudiantil `f395570`. Esta ficha describe el conjunto corregido recibido y reproducido; no certifica equivalencia instrumental ni sustituye la valoración académica del objetivo.

## Identidad y finalidad

El producto es un conjunto de imágenes de conteos direccionales de muones primarios transmitidos por escenarios volcánicos idealizados, con realizaciones de menor conteo obtenidas mediante adelgazamiento binomial. Permite estudiar imágenes con distintas estadísticas bajo una misma definición de fuente y transporte. No contiene reconstrucciones de densidad ni mediciones de un volcán real.

| Propiedad | Valor |
|---|---|
| Escenarios | 19 geometrías cónicas; 18 con anomalías internas y una homogénea |
| Vistas | Seis por geometría, índices 0–5; separación nominal de 60° |
| Referencias | 114 matrices de 256 × 256, conteos enteros uint32 |
| Primarios | 344.000.000 por vista; 39.216.000.000 en la campaña |
| Organización | 1.026 bloques, nueve por vista; manifiesto fijo con semillas nuevas |
| Corte | Energía cinética al cruzar el plano de registro >3 GeV |
| Azimut relativo | 256 intervalos entre −30° y +30°, convención `az-edges-v1` |
| Elevación | 256 centros entre 2° y 47°, convención `legacy-centers-2-47` |
| Realizaciones reducidas | Fracciones 0,50; 0,10; 0,05; 0,01; veinte realizaciones de cada fracción |
| Pares | 80 por referencia; 9.120 en total |
| Semilla de adelgazamiento | Maestra 20260805; derivación por geometría, vista, fracción y realización |

Un par vincula una realización de menor conteo con su referencia. La referencia también contiene ruido de conteo. Los 80 pares de una vista no son 80 simulaciones independientes de referencia.

## Particiones y prevención de mezcla

| Partición | Geometrías | Referencias | Pares |
|---|---:|---:|---:|
| Entrenamiento | 12 | 72 | 5.760 |
| Validación | 3 | 18 | 1.440 |
| Prueba | 3 | 18 | 1.440 |
| Generalización | 1 | 6 | 480 |
| Total | 19 | 114 | 9.120 |

Las particiones se asignan por geometría. Todas sus vistas y realizaciones permanecen juntas; no dividir aleatoriamente los pares entre particiones. La independencia entre simulaciones o particiones no elimina que compartan las hipótesis del generador.

## Receta efectiva y procedencia

Los estudiantes ejecutaron la campaña en SC3 entre el 2 y el 3 de octubre de 2026, en la partición AMD, con 64 hilos y 8 GB solicitados por trabajo. Se registran Geant4 11.4.2, física FTFP_BERT y transporte solo de primarios; GCC 14.2.0. La fuente combina pesos angulares derivados de Guan y cuantiles de momento de EcoMug, incluida la extensión angular documentada. Se inyecta junto al cono con margen angular de 5°. Los impactos nominales se muestrean sobre un panel de 1,2 m; el plano computacional de registro tiene 600 m de lado y no representa un instrumento de ese tamaño.

Las definiciones y huellas de binario, geometrías y tablas están en la [receta](contratos/receta-operativa-siete-actividades.json). El [manifiesto de campaña](evidencias/preparacion-campana-114/manifiesto-114-344M.csv) identifica cada bloque y semilla. Los indicadores históricos de autorización de la ficha corresponden a su preparación; no se reescriben para alterar la identidad congelada de la ejecución. El acuerdo y la receta efectiva constan en la entrega estudiantil y las revisiones de campaña.

El posproceso reportado en SC3 utilizó Python 3.13.13, NumPy 2.5.2 y SciPy 1.18.1. La regeneración local verificada de los pares utilizó Python 3.12.14 y **NumPy 2.4.4**; debe fijarse esa versión para repetir el contenido comprobado. Los cambios en compresión pueden modificar el hash del NPZ sin modificar sus arreglos: se verifica entonces también el hash de contenido, sin presuponer igualdad.

## Archivos y significado

- `fusion/GEOMETRIA/GEOMETRIA_viewV_hist.csv`: matriz de conteos con corte. Su `.meta.json` describe presupuesto, receta, semillas, sumas y huellas; `entradas.sha256` registra procedencia.
- `imagenes/GEOMETRIA_viewV.npz`: `counts_ref` uint32 y coordenadas angulares explícitas (`az_edges_deg`, `az_centers_deg`, `el_edges_deg`, `el_centers_deg`). El archivo lateral conserva metadatos y hash.
- `GEOMETRIA_viewV_pairs.npz`: `counts_ref`, `low_counts` de forma `(4,20,256,256)`, `fractions` y coordenadas. No se aplica recorte uint16, suavizado ni normalización por imagen.
- `events_transported`: N fijo de primarios; `nominal_in_window`: generación dentro de la ventana nominal. No equivalen al número detectado.
- `exposure_days = -1`: ejecución con N fijo. `conventional_exposure_days = 30 × nominal_in_window / 36.034.069,911914065` es una etiqueta convencional; no son días calibrados de un detector real.

El derivado `dataset-v2` y su conversión para entrenamiento quedan fuera de esta ficha: sus bytes no se han auditado en esta revisión del OE1.

## Calidad y excepciones

Se verificaron 477 huellas de archivos; las 114 exportaciones coinciden con sus histogramas. Se reprodujeron 1.710 intervalos de borde con cobertura familiar del 95 % bajo el modelo binomial y el contraste definidos: todos dentro de ±1 punto porcentual. Se regeneraron los 9.120 pares y coincidieron las 342 huellas de contenido publicadas.

La meta descriptiva de roca se evalúa sobre ROI de 4 × 4 píxeles seleccionadas por columna nominal de cono homogéneo entre 30.000 y 100.000 g/cm²; no caracteriza toda la roca ni cada píxel. La alcanzan 107/114 vistas. Globalmente, 20.713/21.816 ROI tienen al menos 100 cuentas (94,944 %). Las siete excepciones se conservan: `geo-test-03` vistas 1 y 5; `geo-train-06` vista 3; `geo-train-09` vistas 1, 4 y 5; `geo-train-12` vista 2. Sus proporciones están entre 89,19 % y 89,81 %.

La fuente híbrida, el transporte sin secundarios, las geometrías idealizadas y la referencia de cielo sin transporte limitan la interpretación física. No se afirma flujo calibrado, respuesta de detector real ni referencia libre de ruido. Véanse la [definición adoptada](DEFINICION_PRODUCTO_OE1.md) y la [síntesis académica](SINTESIS_RESULTADOS_OE1.md).

## Recuperación y reproducción

Las matrices están en la [entrega congelada f395570](https://github.com/anlegogo/muografia-documentada/tree/f395570/objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/datos/sc3/campana-114). El [Drive comunicado](https://drive.google.com/drive/folders/10gRmkWqmCqN3qOf2gfOWCDG4bcC7zhaT) no se verificó en estos cuatro trabajos. No se presume una licencia abierta por estar en un repositorio; conservar la atribución a los autores y el control de acceso vigente.

Desde la raíz de esta réplica, con `DATOS` apuntando a la carpeta `campana-114` extraída del commit y destinos nuevos:

```bash
python herramientas/evaluar_campana_114.py --fusion "$DATOS/fusion" \
  --plan objetivo-1/evidencias/preparacion-campana-114/plan.json \
  --receta objetivo-1/contratos/receta-operativa-siete-actividades.json \
  --referencia objetivo-1/evidencias/preparacion-siete-actividades/cielo-ideal-margen-5.json \
  --salida NUEVA_EVALUACION.json
python herramientas/empaquetar_angular_v1.py "$DATOS/imagenes" \
  --informe NUEVO_INVENTARIO.json --salida NUEVOS_PARES --semilla 20260805
python herramientas/figuras_cierre_oe1.py --campana "$DATOS" --salida NUEVAS_FIGURAS
```

Comprobar los hashes contra los inventarios de la entrega. El [procedimiento de revisión completa](REVISION_DATOS_F395570.md) especifica la comparación de contenido. Responsabilidad de ejecución original: estudiantes; preparación y verificación local: revisión de la dirección. La ficha consolida evidencia técnica, sin declarar concluida la valoración académica.

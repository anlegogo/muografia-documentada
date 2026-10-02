# Adaptación local de lectura y exportación angular

2026-10-01, Colombia. **Estado: parcial.** Continúa la [revisión de la corrida angular](REVISION_MALLA_ANGULAR_2026-10-01.md). No se solicita otra corrida ni se altera material histórico.

## Implementado y comprobado

Nueva herramienta [preparar_imagen_angular_v1.py](../herramientas/preparar_imagen_angular_v1.py): lee CSV y metadatos de `az-edges-v1`, verifica dimensiones, parámetros angulares y conteos, y exporta un NPZ con:

- `counts_ref`: los mismos píxeles y conteos, sin interpolación ni reducción estadística.
- `az_centers_deg` y `az_edges_deg`: 256 centros y 257 bordes de −30° a +30°.
- `el_centers_deg` y `el_edges_deg`: centros históricos de elevación y sus bordes de media celda. Los extremos 2° y 47° son centros, no límites de imagen.

Conserva los metadatos del simulador y añade contrato de exportación y huellas de las entradas y del NPZ. Relee el archivo generado y compara todas las matrices. Rechaza versiones desconocidas, datos históricos, incoherencias, desbordamiento de enteros, nombres duplicados, mezclas de mallas y sobrescritura de directorios. Valida todo el lote antes de escribir; un fallo de disco durante escritura aún podría dejar una carpeta parcial.

La exportación real de la entrega `90abb96` conserva **750 conteos** exactamente. [Evidencia](evidencias/exportacion-angular-90abb96.json). El NPZ de esta prueba es un derivado local, no un nuevo conjunto de producción. Siete pruebas específicas verifican conservación de píxeles/coordenadas, errores de malla, mezcla de versiones, desbordamiento, duplicados y sobrescritura; [registro](evidencias/pruebas-exportacion-angular.txt).

Desde la raíz de la réplica:

```console
python herramientas/preparar_imagen_angular_v1.py RUTA/geo-train-01_view0_hist.csv --salida NUEVA_CARPETA
python -m unittest discover -s herramientas -p test_preparar_imagen_angular_v1.py -v
```

Requiere NumPy. Para dibujar estos archivos, usar `pcolormesh(az_edges_deg, el_edges_deg, counts_ref, shading="flat")`, con azimut horizontal y elevación vertical. Las máscaras futuras deben calcularse sobre los centros explícitos y declarar su versión. No interpolar una máscara antigua y tratarla como geométricamente revalidada.

## Auditoría de consumidores: qué falta

Inspección de los scripts de estudiantes recibidos en `d8ca749`, con el cambio angular posterior limitado a los archivos de `0dea8e1`:

| Herramienta | Hallazgo y tratamiento |
|---|---|
| `csv_to_npz.py` | Conserva metadatos, pero exporta solo conteos; no exige una versión angular. La nueva herramienta ofrece una alternativa explícita y comprobada. |
| `render_pilot_muogram.py` | Usa `imshow` con extremos de elevación que son centros. Adoptar bordes explícitos para representar las nuevas imágenes. |
| `oe1_stage1_common.py`, `oe1_stage1_roi.py` | Conservan centros azimutales históricos y redondeo antiguo. Mantenerlos para reproducir los ensayos congelados; preparar una ruta nueva antes de generar ROI para la nueva malla. |
| `oe1_stage1_analysis.py`, `oe1_stage2_analysis.py` | Sus gráficos y contornos pertenecen al protocolo histórico. No reutilizarlos para certificar ROI nueva sin adaptación. |
| `compare_engines.py` | Antes de comparar matrices nuevas e históricas, exigir igualdad de coordenadas y observable; igualdad de dimensiones no basta. |
| `build_dataset.py` | Lee matrices y metadatos sin bloquear mezcla de mallas. Añadir control de versión/coordenadas antes del empaquetado definitivo. La validación de lote de nuestra exportación no se propaga automáticamente a ese script. |

No se afirma que toda la cadena esté adaptada. Ahora disponemos de un contrato de lectura/exportación probado y de una lista concreta de consumidores pendientes. Los ensayos A/B anteriores siguen usando su malla histórica y no deben reinterpretarse con estos centros.

## Próximo trabajo antes de producción

Integrar este contrato en representación, ROI y empaquetado de la versión nueva, con pruebas geométricas de las máscaras. Separadamente, justificar aceptación del plano de 600 m y normalización temporal usando evidencia existente. La exportación no valida ese modelo físico, no cambia el tamaño de la futura campaña y no cierra P-04. No es necesario pedir a los estudiantes otra simulación para esta adaptación local.

# Complemento técnico R2-01: entrada al solape desde ambos lados

**Diseño de la revisión, 30 de septiembre de 2026. Estado: preparado y validado geométricamente en local; transporte pendiente en SC3.** No es la etapa 2 ni una estimación del efecto sobre la campaña. Responde al hallazgo [R2-01](REVISION_ETAPA_1_2026-09-30.md).

## Comprobación prevista

Si la geometría corregida asigna al cuerpo denso toda la intersección Z, también cuando el muón llega primero por el conducto. La prueba anterior solo cubrió cruces que entraban desde el cuerpo denso. A mantiene el defecto histórico como diagnóstico, sin constituir una referencia física correcta.

## Diseño fijo

| Parámetro | Valor |
|---|---|
| Caso | geo-train-06, vista 0; mismo catálogo de etapa 1 |
| Primarios | 12 muones negativos de energía cinética 10.000 GeV, dirigidos al centro del panel físico (1000, 0, 1,5) m |
| IDs 0–5 | En sus rectas ideales, llegan a Z desde el conducto |
| IDs 6–11 | En sus rectas ideales, llegan a Z desde el cuerpo denso, como control |
| Variantes | A2 y B2 de la etapa 1, sin cambios de física ni instrumentación |
| Repeticiones técnicas | Tres semillas de transporte: 1026093011, 1026093012 y 1026093013 |
| Emparejamiento | Misma lista e IDs A/B y misma semilla de transporte por par; un hilo por proceso |
| Total | 6 corridas × 12 primarios = **72 transportes** |

Las tres semillas repiten las mismas trayectorias iniciales bajo distintos estados aleatorios de transporte. No son tres muestras representativas nuevas de la fuente y no se agrupan con las 13 corridas anteriores. La energía de 10 TeV conserva el enfoque del control sintético T-S; no representa el espectro natural ni permite extrapolar su frecuencia al conjunto de imágenes.

## Archivos preparados

- [Lista de 12 primarios](ensayos/complemento-r2-01-v1/geo-train-06_v0_r10_r201.primarios.csv), [metadatos](ensayos/complemento-r2-01-v1/geo-train-06_v0_r10_r201.primarios.csv.meta.json) y [huellas SHA-256](ensayos/complemento-r2-01-v1/SHA256SUMS.txt).
- [Trayectorias y resultados geométricos esperados](ensayos/complemento-r2-01-v1/trayectorias-esperadas.json): lado de entrada, coordenadas de entrada/salida y longitud ideal por ID.
- [Generador reproducible](../herramientas/preparar_complemento_r2_01.py), solo biblioteca estándar de Python.
- [Ejecutor de seis corridas](../herramientas/ejecutar_complemento_r2_01.sh), para usar dentro de una asignación SLURM.
- [Validación local](evidencias/validacion-lista-r201-v1.json), con el validador de estudiantes de `3315f82` en modo `--no-stats`: estructura, unidades, identificadores, huellas y retroproyección al panel correctos. No corresponde aplicar una prueba de distribución de fuente a esta lista dirigida.

El [contraste entre implementaciones geométricas](evidencias/diseno-complemento-r201.json) confirma 12 cruces profundos; las longitudes difieren como máximo 9,8 × 10⁻¹² m del cálculo de referencia de los estudiantes.

La lista tiene SHA-256 `ae8318a704d004989f65faaa5b8fe5624281fefef7c65f370a281d2378402ea1`. No cambiarla después de observar resultados: cualquier ajuste exige una nueva versión y conservar el intento previo.

El cálculo local exige más de 20 m de recorrido ideal dentro de Z y más de 5 m entre las entradas en ambas primitivas. Se verificó que 108 rectas paralelas de sensibilidad (9 por trayectoria, desplazamientos de hasta 5 cm por eje transversal) mantienen su lado de entrada. Es un control geométrico, no una cota rigurosa sobre la dispersión múltiple. La trayectoria real debe comprobarse con los registros.

## Ejecución para Daniel y Reinaldo

1. Actualizar el repositorio y copiar la carpeta de insumos conservando sus bytes. Guardar el complemento en una carpeta nueva de SC3, separado de `etapa1/corridas/intento-01`.
2. Usar Geant4 11.4.2 y los módulos de etapa 1; conservar los binarios A2/B2 y tablas. El ejecutor verifica sus binarios contra las huellas recibidas. Si no coinciden, informar qué cambió antes de ejecutarlo; no desactivar el chequeo.
3. En una asignación SC3 pequeña (propuesta: partición `legacy`, 1 CPU, 1 GB, 10 minutos), definir las siguientes variables como rutas absolutas y ejecutar `bash herramientas/ejecutar_complemento_r2_01.sh`. No ejecutarlo en el nodo de acceso.

```bash
export BINARY_A=/ruta/etapa1/build/A2/muography_sim
export BINARY_B=/ruta/etapa1/build/B2/muography_sim
export GEOMETRY=/ruta/catalogo/geo-train-06.json
export TABLES=/ruta/tablas
export ROI_MASK=/ruta/etapa1/analisis/roi/R_int.mask.txt
export INPUT_DIR=/ruta/muografia-documentada/objetivo-1/ensayos/complemento-r2-01-v1
export OUTPUT_DIR=/ruta/complemento-r2-01/intento-01
bash /ruta/muografia-documentada/herramientas/ejecutar_complemento_r2_01.sh
```

Los `/ruta/...` son marcadores que deben sustituirse por las ubicaciones reales. El ejecutor exige salida nueva, realiza `--check-primaries` con ambos binarios y lanza seis procesos secuenciales. Conserva comandos, registros, metadatos, histogramas, huellas y estado. Un proceso terminado correctamente no significa por sí mismo que la prueba física haya pasado. La sintaxis del ejecutor se comprueba localmente; su ejecución con Geant4/SLURM solo se verificará en SC3.

## Qué entregar y cómo interpretarlo

Crear una carpeta de entrega nueva y `RESULTADOS_COMPLEMENTO_R2_01.md` con enlace a este diseño, commits, SHA-256 de insumos/binarios, módulos, trabajo SLURM y cualquier desviación. Adjuntar los seis registros completos `*_muones.csv`, histogramas, metadatos y logs; son 72 filas en total.

Para cada ID y semilla, comparar A/B: `prim_fnv`, `rng0`, `crossed`, `mat_in`, `mat_out`, `lz_m`, `lz_a0_m`, `lz_a1_m`, `lz_rock_m`, `lz_other_m`, energía de entrada/salida, `max_lat_z_mm`, `sum_lat_z_mm`, estado final, detección y bin.

- **Contrato técnico:** 12 IDs completos por corrida, mismos primarios y estado aleatorio inicial por par, sin abortos; histogramas reconstruidos desde las filas. B sin advertencias nuevas de geometría/navegación.
- **Cobertura:** informar por separado IDs 0–5 y 6–11. Comprobar si la trayectoria transportada conserva la entrada planeada. La etiqueta calculada para la recta inicial no prueba por sí sola el lado de entrada real.
- **Material en B:** contrastar que `lz_m` corresponde a `lz_a1_m`, y mostrar cualquier longitud asignada a otros materiales. Usar 1 µm como tolerancia numérica inicial, heredada de T-S; si la dispersión o la cuerda explican una discrepancia, documentarla sin convertir esa explicación en una cota garantizada.
- **Diagnóstico de A:** medir qué material asigna y cómo cambia frente a B. No exigir una diferencia de imagen ni forzar que todos los muones de A recorran A0: A contiene un solapamiento inválido y su navegación es lo que se está investigando.
- **Longitud y energía:** comparar con la longitud de la recta y su sensibilidad como diagnóstico. No exigir igualdad exacta de trayectorias A/B ni presentar la energía interpolada como una medición exacta dentro del paso.

Si el registro agregado no permite establecer la entrada real, o todos los casos siguen sin cubrir el conducto, conservar el resultado e informar los IDs. El paso siguiente será trazar los pasos próximos a Z para esos casos, con coordenadas pre/post y material; cualquier instrumentación adicional se separará y comprobará como inerte antes de repetir. No ampliar automáticamente el número de muones ni cambiar la lista buscando un resultado favorable.

**Cierre de este complemento:** correspondencia técnica correcta y evidencia interpretable de la cobertura de ambos lados y de la asignación de material de B. Tras revisarlo se dimensionará la etapa 2 con fuente representativa; este complemento no resuelve el margen físico, la incertidumbre ni la decisión de regenerar la campaña.

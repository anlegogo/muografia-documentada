# Decisiones de implementación de la etapa 1 del segundo ensayo OE1

Este documento, escrito antes de cualquier transporte en SC3, recoge las decisiones de implementación de la etapa 1 del segundo ensayo OE1. La tabla de la sección 1 resume cada decisión con su motivo y con el control que la verifica; las demás secciones dan el detalle que no cabe en una celda. La sección 3 describe las pruebas técnicas, dónde se conservan sus resultados y cómo responden dos preguntas: si el registro por muón altera la simulación y si la detección de cruces funciona como se espera.

## 1. Resumen de decisiones

DV1 a DV9 son desviaciones o definiciones operativas. D-Q1 a D-Q7 fijan siete puntos que el protocolo deja abiertos.

Siglas y términos de la tabla:

- Z: región 3D de cruce, intersección del conducto (cilindro, anomalía 0) y el elipsoide (anomalía 1) de geo-train-06 (sección 5.2).
- R_int: máscara angular de 195 píxeles de la entrega `712c786` (sección 6).
- A2 y B2: A y B con la instrumentación (sección 2). `s_src` y `s_tr`: semillas de fuente y de transporte (sección 4).
- Paso y cuerda: Geant4 transporta cada muón en pasos; la cuerda es el segmento recto entre el punto inicial y el final de un paso.
- `hist.csv`, `meta.json` y `_muones.csv`: histograma, metadatos y registro por muón de una corrida (en disco, `<geometría>_view0_hist.csv`, `<geometría>_view0.meta.json` y `<geometría>_view0_muones.csv`).
- K0 a K9 y K-ROI: controles (sección 7). T-L, T-R, T-M, T-P, T-S y T-F: pruebas técnicas (sección 3). C1 a C9, R1 y V: pruebas del detector de cruces (sección 3.2).

| ID | Decisión | Motivo | Cómo se verifica |
|---|---|---|---|
| DV1 | Pruebas técnicas fuera de las 13 corridas: 24.120 transportes (1,86 % de la etapa), un hilo por proceso, en un trabajo aparte (sección 3). | PROT:17 exige comprobar que registrar no cambia las condiciones iniciales ni consume números aleatorios. PROT:53 pide controles de trayectorias antes de interpretar cruces. PROT:42 fija las 13 corridas, así que las pruebas van aparte. | `estado-pruebas-tecnicas.txt` con `resultado=OK` y `resumen-pruebas-tecnicas.json`, en `pruebas/` (sección 3.3). |
| DV2 | Números aleatorios comunes en A y B: al empezar cada evento, el generador se resiembra con la clave `{id, s_tr, case_code, TAG_TR}`, propia de cada muón (valores en la sección 4). | PROT:24 admite compartir números aleatorios si se documenta el reinicio por evento. Sin resiembra, el emparejamiento A/B depende de cuántos números consume el motor maestro (el generador que entrega la semilla de cada evento) al construir la geometría (sección 4). | K0 (`s_tr` en el manifiesto), K9 (a), T-M y T-P. |
| DV3 | `in_rint` lo escribe el binario con la máscara R_int exportada y verificada por SHA-256; el análisis lo recalcula fuera de línea. | PROT:49 pide la pertenencia a la ROI por primario. El recálculo detecta una máscara mal cargada. | K0 (huellas de la máscara) y K6 (acuerdo del 100 %). |
| DV4 | En geo-train-01 los campos de cruce valen «no aplica» (`crossed = −1`) y la corrida lleva `--region-pair none`. | geo-train-01 no tiene anomalías. Criterio análogo al de PROT:59. | K6: `region.applicable = false` y `crossed = −1` en todas las filas. |
| DV5 | Listas y registros por muón (≈ 150 MB comprimidos) en almacenamiento compartido, con URL y SHA-256 en el manifiesto. Las tablas derivadas pequeñas van al repositorio. | Tamaño del repositorio. PROT:91 admite un enlace a almacenamiento compartido con manifiesto SHA-256. | `sha256sum -c` de `MANIFIESTO.sha256`. |
| DV6 | `.gitattributes` solo en esta carpeta y solo para datos: `*.csv *.tsv *.txt *.log *.out *.sha256 -text`. | Una exportación local en Windows cambió los finales de línea de 71 textos de la entrega anterior, aunque sus blobs de Git estaban intactos (`REVISION_ENTREGA_2026-09-29.md:13`). | `sha256sum -c` del manifiesto en un clon limpio. |
| DV7 | Tabla por corrida ampliada: caso, réplica, variante, `s_src`, `s_tr`, N, detectados, estados finales, cruces, avisos por código, tiempo de pared, CPU, memoria máxima (RSS), nodo y trabajo. CPU y RSS salen de `getrusage` del propio proceso, escrito en `meta.json`; `recursos.json` solo es respaldo. Las transiciones van en filas por par. | PROT:91 pide por corrida N, transiciones, cruces, detectados, avisos y tiempo. | Columnas de `tabla-corridas.csv` y `transiciones.csv`. |
| DV8 | Cruce: un paso cuya cuerda entra más de 1 µm en Z y mide más de 2 µm dentro de Z. Los roces se cuentan aparte. Longitud, material y energía: sección 5.2. | PROT:50 no fija estas definiciones, y PROT:53 pide especificar cómo se detectan los cruces dentro de un paso y su error geométrico. | C1 a C9, R1, V y T-S (sección 3.2). |
| DV9 | Cada discordancia A/B se clasifica (`cruza_Z`, `roce`, `conducto`, `solo_elipsoide` u `otra`). Las de muones que no cruzan Z no bloquean el reporte de Δ; si alguna queda sin explicar, bloquea la atribución al solape. | PROT:24 no exige trayectorias iguales. En B cambia la distancia a la frontera (safety) del conducto sustraído junto al elipsoide, y eso puede afectar a muones que se detienen en el conducto. | K9 (b) en `contratos.json`: `solo_elipsoide` y `otra` cuentan como sin explicar. La bandera `atribucion_al_solape_bloqueada` retiene la atribución (sección 7). |
| D-Q1 | Gestor de ejecución (el objeto de Geant4 que reparte los eventos entre hilos): `G4TaskRunManager`, el que Geant4 crea por defecto (`G4RunManagerType::Default`), como en el piloto y en la campaña. Usa un hilo trabajador (`--threads 1`); el hilo maestro no transporta. Otro gestor es un error. | PROT:26 pide un hilo por proceso. Con la resiembra, el estado inicial de cada muón no depende del gestor ni del número de hilos. | Con otro gestor, el binario termina con código 4 antes del transporte (`BeamOn`). K6 comprueba un hilo, el generador de números aleatorios MixMaxRng y `G4TaskRunManager`. |
| D-Q2 | Semillas de fuente 2026092901, 2026092902 y 2026092903 en ambos casos. Las listas difieren por caso a través de `case_code` y del radio de partida (1.809,7 m en geo-train-06; 1.956,2 m en geo-train-01). | Son los valores de PROT:37. | K0 (manifiesto) y K1 (las seis listas tienen huellas FNV distintas). |
| D-Q3 | Repetición A/A: `_muones.csv` y `hist.csv` idénticos byte a byte; `meta.json` igual salvo cinco claves de tiempo y recursos. Corre en el mismo trabajo y en el mismo nodo que las demás corridas. | Concreta el «estado completo idéntico» de PROT:55. Compartir nodo evita diferencias de CPU y de libm (la biblioteca matemática del sistema). | K7, bloqueante, incluido el mismo nodo. |
| D-Q4 | Estadística de la etapa 1: conteos exactos. El intervalo score de Tango (para la diferencia de dos proporciones pareadas) y la prueba exacta de McNemar se informan como diagnósticos que no acotan el efecto. | PROT:44: la etapa no está dimensionada para un efecto pequeño. Se esperan ≈ 0,27 detecciones en R_int por corrida: 98 cuentas en 36.174.382 primarios de la campaña de geo-train-06, vista 0. Lo más probable es que n01 y n10 (muones detectados en R_int solo con B y solo con A) valgan 0. | `resultados-etapa1.json` (`intervalo_no_acota_el_efecto = true`) y la nota de `transiciones.csv`. |
| D-Q5 | Control geométrico de B con resolución 100.000 (puntos de muestreo sobre la superficie de cada volumen), tolerancia 0 y `maxErr` 100 (máximo de solapes que Geant4 informa por volumen), con semilla 20260929. Además, el chequeo de solapes de 1.000 puntos que Geant4 ejecuta al colocar cada volumen. | PROT:18 pide resolución y tolerancia registradas; un aviso nuevo en B bloquea. | K2, y K6: ninguna corrida de B muestra avisos de solape o de navegación de Geant4 (GeomVol1002, GeomNav, G4Exception). |
| D-Q6 | La orientación de R_int se demuestra geométricamente: el centroide de Z cae en el píxel (34, 135), dentro de R_int, y su espejo en acimut, columna 120, queda fuera. Si un resultado la contradice, se detiene el trabajo y se informa; la máscara no se redefine. | PROT:59 prohíbe redefinir R_int viendo resultados nuevos. | K-ROI (sección 6). |
| D-Q7 | El margen de la etapa 2 solo se propone después, en `RESULTADOS_ETAPA_1.md`. M1 es el ruido de Poisson de R_int en una imagen de 30 días, ≈ 2,7 × 10⁻⁷ por primario con k = 1. M2 solo entra con una fracción justificada de la señal de la anomalía. | PROT:75 pide un margen justificado que no se deduzca del resultado más favorable del piloto. | Sección 6 de `RESULTADOS_ETAPA_1.md`, con cada insumo rotulado como dato o supuesto (sección 9). |

## 2. Identificación

| Dato | Valor |
|---|---|
| Fecha | 30 de septiembre de 2026 (Colombia, UTC−5). |
| Protocolo | `objetivo-1/PROTOCOLO_SEGUNDO_ENSAYO_OE1.md` v1.0, commit `1054fb867e1315128f2a3f4bd59d4747c9c525b2`. En este documento, PROT:n es la línea n del protocolo. |
| Esta entrega | Rama `oe1/segundo-ensayo-etapa-1`, carpeta `objetivo-1/entregas/2026-09-30-segundo-ensayo-etapa-1/`. |
| Casos | geo-train-06, vista 0 (afectado), y geo-train-01, vista 0 (control). |
| Corridas | Tres réplicas de 100.000 primarios por caso y variante, más la repetición A/A de geo-train-01, réplica 1: 13 corridas y 1.300.000 transportes (PROT:42). |
| Entorno | SC3, Geant4 11.4.2 con la lista de física FTFP_BERT, gcc 14.2.0 (módulos `gnu14/14.2.0` y `geant4/11.4.2`). |
| Estado al 30 de septiembre de 2026 | Ningún transporte en SC3 con estos binarios. Allí solo han corrido, con `srun` y en carpetas de desarrollo, compilaciones y comprobaciones sin transporte. |

Código: repositorio `muography-dl-reconstruction`, rama `oe1/stage1-instrumentation`. P0, P1 y P2 son los parches de diagnóstico geométrico, de corrección geométrica y de instrumentación.

| Versión | Contenido | Commit |
|---|---|---|
| A | Código de la campaña con los modos de diagnóstico geométrico (P0) | `9520170` |
| B | A más la corrección geométrica (P1) | `f1edc80` |
| A2 | A más la instrumentación (P2) | `fdaef4b8aad259f17043ef0fc6fdccc295e3b8e2` |
| B2 | A2 más P1 (cherry-pick de `f1edc80`) | `9bb43f3b620b5e6d62e4b5ea79647dff44c6f3cd` |
| Herramientas | Análisis y scripts de SC3 | `3315f82ffa1a3be604897e34e2319b379f500655` |

- A y B solo difieren en `src/DetectorConstruction.cc`. Por construcción, diff(A2, B2) = diff(A, B). SHA-256 de `P2-instrumentacion.diff`: `caf69f4fb108d5038152bc5f8df082cdea5a3547f183a464e19f01281d1c07dd`.
- En SC3, A2 y B2 son copias de los árboles A y B del piloto con `P2-instrumentacion.diff` aplicado (`patch --fuzz=0`). Solo los archivos que toca P2 se verifican contra los SHA-256 del commit A2. El árbol completo no coincidiría: el `CMakeLists.txt` del piloto difiere del repositorio y el `DetectorConstruction.cc` de A tiene finales de línea CRLF (P2 no toca ninguno de los dos). Las huellas de todos los archivos quedan en `A2-fuentes.sha256` y `B2-fuentes.sha256` (PROT:15).
- Sin cambios respecto al piloto (PROT:16): FTFP_BERT con corte de producción por defecto de 1 m, secundarios descartados al crearse, generador de muones con sus tablas, detector (plano de puntuación de 600 × 600 m) y catálogo. `prepare_sources.sh` rechaza un P2 que toque `DetectorConstruction.*`, `GeometryConfig.*`, `FluxTables.*`, `StackingAction.*`, `GeometryDiagnostics.*`, `CMakeLists.txt` o `tables/`.
- Huellas fijas en `make_manifest.py`: catálogo geo-train-06 `c8f6c135…` y geo-train-01 `ff3c69ab…`; tablas del generador `row_weights_30d.txt` `93ce67ab…`, `p_cdf.txt` `7161c8ad…` y su `meta.json` `7ac4b6a9…`. Compilador, flags y SHA-256 de los ejecutables quedan en `build/compilacion.txt` y `build/binarios.sha256`.
- B aplica la regla «la última anomalía del JSON prevalece», coherente con el motor analítico: cada anomalía ocupa su intersección con el edificio menos las anomalías posteriores. No cambia densidades ni posiciones, y el catálogo es el mismo en A y B (PROT:11). Los casos que combinan recorte y varias sustracciones no se han ensayado.
- Se conservan dos referencias (PROT:11). El margen de recorte de 1 mm no interviene en geo-train-06 (K2 exige `clipped=no`). La densidad del aire es 0,00120479 g/cm³ en Geant4 (G4_AIR) y 0,001225 g/cm³ en el motor analítico (−1,65 %).

## 3. Pruebas técnicas (DV1)

Las pruebas técnicas corren en un trabajo aparte, `pruebas_tecnicas.sbatch` (6 CPU, 20 min, un hilo por proceso, seis procesos a la vez), antes de las 13 corridas. Suman 24.120 transportes, el 1,86 % de los 1.300.000 de la etapa. Las listas técnicas (geo-train-06, geo-train-01 y la auxiliar de T-P) tienen 2.000 muones cada una; la lista sintética de T-S tiene 60. Si en `herramientas/` falta el archivo de compuerta de DV1, o está vacío o sin su texto fijo, el trabajo termina con código 4 sin crear nada. Ese archivo operativo queda en SC3 y no se copia a la entrega.

Términos de la tabla:

- Modo legado: la línea de comandos del piloto, sin los flags nuevos. Modo lista: transporte de una lista congelada de primarios (`--primaries`).
- `--muon-log full` y `--muon-log min`: registro completo, con cruces, y registro mínimo, sin cálculo de cruces.
- `rng0` y `rng1`: huellas del estado del generador de números aleatorios tras la resiembra y al terminar cada muón.
- `run_one`: la función de `principal.sbatch` que lanza cada corrida de producción.

| Prueba | Transportes | Qué compara | Criterio de aceptación |
|---|---|---|---|
| T-L | 8.000 (4 × 2.000) | Modo legado: binarios del piloto (`build-A`, `build-B`) frente a A2 y B2, geo-train-06 vista 0, `--events 2000 --seed 2026092900 --threads 1`. | `hist.csv` idéntico byte a byte; `meta.json` igual salvo tiempos; el modo legado no escribe la clave `oe1_etapa1` ni `_muones.csv`; `run.log` igual con `wall_s` enmascarado. |
| T-R | 2.000 | B2 en modo lista con la lista técnica de geo-train-06, `--muon-log full` frente a `min`. El lado `full` es la corrida g06-B de T-F. | `hist.csv` idéntico; mismos `id`; `rng1` igual para todo `id`; columnas de identidad, detección, estado y número de pasos iguales; `min` deja vacíos los campos de cruce. |
| T-M | 2.000 | Como el lado `full` de T-R, con otra semilla maestra (1026092995) y la misma semilla de transporte (1026092990). | `rng0`, `rng1`, `hist.csv` y `_muones.csv` idénticos; `meta.json` igual salvo tiempos y semilla maestra. |
| T-P | 2.000 | B2 con la lista técnica de geo-train-06 cuyas primeras 100 filas se sustituyen por filas de una lista auxiliar. | Los `id` ≥ 100 conservan `rng0`, `rng1` y todo su resultado; más del 90 % de las 100 primeras filas cambian de primario. |
| T-S | 120 (60 × 2) | 60 μ⁻ sintéticos de 10 TeV en A2 y B2: 20 atraviesan Z con al menos 3 m de profundidad, 20 pasan cerca, a entre 0,5 y 1,0 m de Z, y 20 pasan a más de 50 m. | Clasificación correcta en los 60 (`lz` = 0 en los que no atraviesan).<br>Longitud en Z de los 20 que atraviesan: ± 1 % de la recta en las líneas centrales; en las someras, ese margen se amplía al intervalo de las rectas paralelas desplazadas hasta 0,05 m. Una recta es central si ese intervalo cabe en ± 1 %.<br>Materiales, con tolerancia de 1 µm: en B2, `lz` = `lz_a1`, con `lz_a0`, `lz_rock` y `lz_other` nulos; en A2, `lz` = `lz_a0 + lz_a1`, con `lz_rock` y `lz_other` nulos. |
| T-F | 10.000 (5 × 2.000) | Recorrido completo con el mismo `run_one` de producción: listas técnicas de ambos casos en A2 y B2, más una repetición A/A, y después el mismo script de análisis. Su tabla de corridas registra tiempo de pared, CPU y memoria máxima (RSS) con la instrumentación completa (PROT:44). | Análisis sin contratos fallidos, bloqueantes o no; tabla de 5 corridas; ninguna fila STOPPED, OTHER ni ABORTED. |
| Total | 24.120 | | |

### 3.1 ¿El registro altera la simulación?

Responden T-R y T-L; T-M, T-P y la auditoría estática de K0 completan la respuesta. La conclusión «el registro no altera la simulación» exige que pasen T-R, T-L, T-M y T-P. T-R, T-M y T-P usan B2 en geo-train-06 con 2.000 muones; la conclusión se extiende a A2 porque P2 es el mismo parche en A2 y en B2 (sección 2), y T-S y T-F ejecutan A2 en modo lista con el registro completo.

- T-R transporta los mismos muones con el registro completo y con el mínimo. Si calcular los cruces extrajera números aleatorios o cambiara los pasos, cambiarían `rng1`, `n_steps` o el bin final.
- T-L muestra que A2 y B2, usados sin los flags nuevos, escriben el mismo `hist.csv`, byte a byte, y el mismo `meta.json`, salvo tiempos, que los binarios del piloto.
- T-M y T-P muestran que el flujo aleatorio de cada muón depende solo de (`s_tr`, caso, id). La semilla maestra y los muones anteriores no lo cambian.
- En modo lista no hay una corrida sin registro: el nivel mínimo conserva la resiembra, las huellas `prim_fnv`, `rng0` y `rng1` y los contadores de estado. `rng0` y `rng1` se leen con `put()`, que no extrae números.
- La auditoría estática revisa, por nombre, las líneas que añade P2: no deben extraer números del generador de transporte ni llamar al navegador de Geant4 (el componente que localiza puntos en la geometría). La única extracción permitida está en el modo de generación de listas: la prueba de que el muestreador consumió 7 números por muón, hecha con un motor privado que se descarta.
- Como compara nombres, la auditoría no detecta un alias del motor seguido de una extracción implícita ni generadores ajenos a CLHEP (la biblioteca de números aleatorios de Geant4). Por eso T-R, T-M y T-P cubren PROT:17 con el binario real.

### 3.2 ¿La detección de cruces funciona como se espera?

La detección funciona como se espera si pasan C1 a C9, R1, V, T-S y K-ROI. Las longitudes que mide son de cuerda, con la escala de error de la sección 5.2. Las pruebas del detector corren en SC3 con los flags de producción y, aparte, con detectores de errores de memoria y de comportamiento indefinido (ASan y UBSan).

| Nivel | Prueba | Qué comprueba |
|---|---|---|
| Detector sin Geant4 | C1 | Recta vertical por el centroide de Z con ambos extremos fuera: ℓ = 89,67389128531408 m, igual a la fórmula vertical exacta de `herramientas/validar_volumen_oe1.py`, con tolerancia de 10⁻⁹ m. |
| Detector sin Geant4 | C2 a C9 | Casos analíticos, con tolerancia de 10⁻⁹ m salvo C9:<br>recta horizontal;<br>tangencias a ± 10⁻³ y ± 10⁻⁷ m (cruce profundo, roce o sin contacto, según el caso);<br>cuerdas que atraviesan ambas primitivas sin tocar Z;<br>segmentos dentro de una sola primitiva;<br>segmentos totalmente dentro de Z o con la mitad dentro;<br>segmentos degenerados o paralelos a los ejes;<br>aditividad por trozos;<br>inversión de 100.000 segmentos (C9: 10⁻¹² relativo más un término por el redondeo de las coordenadas). |
| Detector sin Geant4 | R1 | 100.000 segmentos aleatorios por semilla, con seis semillas, frente a una implementación independiente en numpy y un oráculo de muestreo denso. |
| Detector sin Geant4 | V | Volumen de Z por rejillas de rectas paralelas: 83.663,70318 m³ ± 1 m³ (2 m³ en la compilación con ASan y UBSan), el valor de `objetivo-1/evidencias/volumen-independiente-geo-train-06.json`. Comprueba el detector; el transporte queda para T-S (PROT:95). |
| Transporte real | T-S | Clasificación, longitudes y materiales en A2 y B2 (tabla de la sección 3). |
| Geometría angular | K-ROI | El mapa de longitud en Z por píxel cae sobre R_int y no sobre su espejo (sección 6). |

`pruebas-cruces.json` guarda compilador, flags, SHA-256 de las fuentes, semillas de R1 y resultados. También anota los cambios respecto a los valores fijados al diseñar las pruebas: la tolerancia de R1, que escala con las coordenadas; la de C9; y, con ASan y UBSan, rejillas más gruesas para V, con tolerancia de 2 m³.

### 3.3 Conservación de los resultados, rótulo y semillas

Los resultados de las pruebas técnicas se conservan en `pruebas/` de esta carpeta de entrega e indican si el registro altera la simulación y si la detección de cruces funciona como se espera:

| Archivos en `pruebas/` | Qué indican |
|---|---|
| `T-R.json`, `T-L-A.json`, `T-L-B.json`, `T-M.json`, `T-P.json` | Si el registro altera la simulación (sección 3.1). |
| `T-S-A.json`, `T-S-B.json`, `k0/pruebas-cruces.json` y la salida de K-ROI (`kroi.txt` y `kroi/`, copiadas de `verificacion/prep-NN/`) | Si la detección de cruces funciona como se espera (sección 3.2). |
| `T-F.json`, `analisis-TF/` y `analisis-TF.txt` | Resultado del recorrido completo, con el mismo `run_one` de producción y el mismo script de análisis. |
| `validacion-listas-tecnicas.json` y `validacion-listas-tecnicas.txt` | Validación de las listas técnicas. |
| `resumen-pruebas-tecnicas.json` | Veredicto conjunto y fallos de cada prueba T-*; no incluye C1 a C9, R1, V ni K-ROI. |
| `estado-pruebas-tecnicas.txt` | `resultado=OK` o `resultado=FALLO`. |
| `entorno.txt` | Entorno del nodo. |
| `k0/` | Salidas del resto de K0: banco sintético con Geant4 (sin transporte), salida anticipada, inercia del modo legado, pruebas de Python y auditoría estática. La auditoría solo imprime en pantalla, así que su salida se guarda redirigida en `k0/auditoria-aleatorios.txt`. |

`RESULTADOS_ETAPA_1.md` responde las dos preguntas en su sección de pruebas técnicas, con los criterios de las secciones 3.1 y 3.2 de este documento y con enlaces a estos archivos. Las listas técnicas y los registros por muón siguen DV5.

- Rótulo: cada `T-*.json` lleva en el campo `etiqueta` el texto `prueba técnica (DV1), fuera de las 13 corridas`; en SC3, `ETIQUETA.txt` repite ese rótulo con el número de trabajo y queda allí junto al archivo de compuerta. `resumen-pruebas-tecnicas.json` y `analisis-TF/` se identifican por su carpeta.
- Semillas: las listas técnicas usan la semilla de fuente 2026092990 (réplica 0, semilla de transporte 1026092990); la lista auxiliar de T-P usa 2026092991. T-L usa la semilla maestra 2026092900, y T-S una lista sintética determinista (semilla 20260930, réplica 9). Ninguna coincide con las de producción.
- Exclusión: las pruebas corren en otro trabajo y en otra carpeta. Sin `--technical`, `make_manifest.py` rechaza listas con N distinto de 100.000, y el análisis de la etapa 1 solo lee las 13 corridas del manifiesto de producción. Ningún transporte técnico entra en Δ ni en otra estadística de la etapa 1.
- En SC3, el trabajo técnico escribe sus salidas en `~/oe1-trabajo/etapa1/pruebas/tecnicas-NN/`, listas y corridas incluidas, en una carpeta nueva por intento que nunca se reutiliza. Si una prueba falla, producción no se lanza; se corrige y se repite con otro `TEC_NN`.
- Copia a la entrega: los archivos de la tabla pasan de SC3 a `pruebas/` con `rsync` y se comprueban con `sha256sum -c` contra una lista de SHA-256 generada en SC3 antes de copiarlos.

## 4. Números aleatorios comunes y listas de primarios

Semillas de cada réplica, iguales en los dos casos:

| Réplica | `s_src` (semilla de fuente) | `s_tr = s_src − 10⁹` (semilla de transporte) |
|---|---|---|
| 1 | 2026092901 | 1026092901 |
| 2 | 2026092902 | 1026092902 |
| 3 | 2026092903 | 1026092903 |

- `s_tr` queda por debajo de 2³¹ − 1, el módulo que el binario aplica a la semilla maestra, y K0 comprueba su relación con `s_src` en el manifiesto. La semilla maestra `--seed` también vale `s_tr`. `case_code` vale 6 en geo-train-06 y 1 en geo-train-01.
- Seis listas congeladas (2 casos × 3 réplicas × 100.000 muones) se generan antes del transporte con el muestreador compilado del piloto, sin cambios. El modo de generación no crea gestor de ejecución ni transporta. Usa un motor MixMax privado con la clave {`s_src`, `case_code`, 0, `TAG_SRC`} y comprueba que el muestreador consumió exactamente 7 números uniformes por muón.
- Formato `<caso>_v0_r<k>_s<s_src>.primarios.csv`, columnas `id,x_m,y_m,z_m,dx,dy,dz,ekin_gev,pdg,charge_e`: posición en m en el marco del mundo, dirección unitaria de viaje, energía cinética en GeV y código PDG ±13. La fila `id` es el evento `id` en A y en B.
- La huella oficial de cada lista es el SHA-256 del archivo. Otra plataforma puede producir diferencias en las últimas cifras por su libm, así que prevalece el archivo congelado. El binario rechaza (código 1) una lista cuyo SHA-256 no coincide con `--primaries-sha256` o cuya geometría, vista, `case_code` o réplica no corresponden a la corrida.
- Al empezar cada evento, el binario resiembra el generador con `setTheSeeds({id, s_tr, case_code, TAG_TR}, 4)`. El estado inicial de cada muón depende así solo de (`s_tr`, caso, id).
- Geant4 también resiembra cada evento con una clave propia, en la que vale 0 la posición que en la clave OE1 ocupa la etiqueta `TAG_TR` = 0x4F455431, distinta de cero. Por eso los flujos de OE1 no coinciden con los de Geant4. La generación de listas usa otra etiqueta, `TAG_SRC` = 0x4F455331, así que los flujos de fuente y de transporte tampoco coinciden (PROT:38).
- Motivo de la resiembra: sin ella, la semilla de cada evento sale del motor maestro, y el chequeo de solapes del cono al construir la geometría consume ese motor. En el piloto, A y B quedaron emparejados por coincidencia de ese consumo; una anomalía recortada en B lo habría roto sin aviso.
- Cada fila del registro lleva `prim_fnv` (huella FNV-1a de 64 bits del primario tal como lo ve Geant4), `rng0` y `rng1`.
- Antes del transporte (K1), A2 y B2 escriben las seis listas en carpetas distintas y deben coincidir byte a byte. Las semillas 2026092801 a 2026092803 del piloto no se reutilizan.

## 5. Registro por muón

Cada corrida escribe `_muones.csv` con 49 columnas y una fila por primario, ordenadas por `id` y sin tiempos ni rutas.

### 5.1 Estado final y valores ausentes

| Estado | Significado |
|---|---|
| DET | Entra al plano de puntuación dentro de la rejilla de 256 × 256 y cuenta en `hist.csv`. |
| PLANE_OUT | Entra al plano de puntuación fuera de la rejilla. |
| WORLD_EXIT | Su último paso llega al borde del mundo simulado. |
| DECAY | Termina por desintegración. |
| MU_CAPTURE | Termina por captura de μ⁻ en reposo, que incluye la desintegración en órbita. |
| STOPPED | Termina con energía cinética nula, sin ninguna de las causas anteriores. |
| OTHER | Cualquier otro final. |
| ABORTED | Geant4 abortó el evento. |

- Un muón no detectado lleva `detected = 0`, `iel = iaz = −1` e `in_rint = −1`. Las columnas del plano quedan vacías si no llegó a él (PROT:49).
- K6 exige cero filas ABORTED e `id` de 0 a N−1 sin huecos ni repetidos. Así, una corrida incompleta no se confunde con una no detección (PROT:51).

### 5.2 Región de cruce Z y escala de su error

Z es la intersección del cilindro de la anomalía 0 con el elipsoide de la anomalía 1, con las primitivas originales del JSON en coordenadas del mundo, comunes a A y B. Z no es un volumen de Geant4, así que no añade fronteras de paso ni consume números aleatorios.

| Primitiva | Centro (m) | Dimensiones |
|---|---|---|
| Cilindro (anomalía 0) | (20,3; −24,5) | Radio 21 m; z entre 0 y 340 m. |
| Elipsoide (anomalía 1) | (32,2; −74,1; 137,8) | Semiejes 72,9; 61,6 y 64,6 m. |

- En cada paso del muón primario se interseca de forma exacta la cuerda con Z. Como Z es convexa, la cuerda la corta en un solo intervalo, también cuando ambos extremos quedan fuera.
- Cruce (`crossed = 1`): algún paso cuya cuerda entra más de ε = 1 µm en Z y mide más de 2ε = 2 µm dentro de Z; por eso `crossed = 1` implica `n_steps_z ≥ 1`. Entrar más de ε significa tener longitud positiva dentro de Z reducida en ε. Un tramo de 2ε o menos suma a las longitudes pero no fija ningún campo categórico (cruce, pasos, entradas, material, energía). Es lo que queda, por ejemplo, cuando un paso termina sobre una superficie de Z que también es frontera de un volumen de Geant4.
- Roce: la cuerda toca Z agrandada en ε sin penetrarla más de ε, y el contacto queda a más de 2ε de ambos extremos del paso. Un paso que solo empieza o termina sobre la superficie de Z no es un roce. Los roces se cuentan aparte (`n_graze_z`).
- Longitudes: `lz_m` es la longitud de la cuerda dentro de Z y se reparte por material (`lz_rock_m`, `lz_a0_m`, `lz_a1_m`, `lz_other_m`). `lz_true_m` = cuerda en Z × `StepLength`/|cuerda|, donde `StepLength` es la longitud de trayectoria que Geant4 asigna al paso; no se reparte. El material asignado es el del volumen donde empieza el paso; en A depende del lado por el que entra el muón.
- La energía de entrada y de salida se interpola sobre la cuerda y se informa con el intervalo [E_post; E_pre] del paso, que va de la energía al final a la energía al inicio del paso.
- La cuerda no es la trayectoria que sigue el muón en Geant4. WentzelVI, el modelo de dispersión múltiple de muones en FTFP_BERT, desplaza de lado el punto final de cada paso hasta 0,99 veces la distancia a la frontera más cercana. Lo hace aunque la opción `MuHadLateralDisplacement` (desplazamiento lateral para muones y hadrones) esté desactivada. En transporte local de desarrollo, el desplazamiento máximo de cada muón superó 10⁻⁶ mm en ≈ 89 % de los muones y llegó a ≈ 10 mm cerca de Z.
- Cada muón registra `max_lat_z_mm` y `sum_lat_z_mm`: el máximo y la suma del desplazamiento lateral en los pasos cercanos a Z (aquellos cuya cuerda toca ambas primitivas agrandadas 1 m). `sum_lat_z_mm` da la escala del error de longitud, sin acotarlo. Con incidencia θ, el error es ≈ lat/sen θ, donde lat es ese desplazamiento acumulado. En una cuerda rasante crece como √(2·R·lat), así que se informa como ≲ 2√(2·R_max·lat), con R_max = 72,9²/61,6 = 86,27 m (radio de curvatura máximo del elipsoide) y lat en metros (la columna `sum_lat_z_mm` está en mm).
- Una cuerda que penetra Z menos que `max_lat_z_mm` puede quedar clasificada de forma distinta a la trayectoria real. `max_lat_mm`, sobre todos los pasos, es solo diagnóstico: K6 exige que esté informado y coincida con `meta.json`, sin umbral.
- En geo-train-01 no hay primitivas y los campos de cruce valen «no aplica» (DV4). Una geometría con dos o más anomalías lanzada sin `--region-pair` termina con código 2.

## 6. R_int

- Se usa la máscara R_int de la entrega `712c786` sin cambios (PROT:59): 256 × 256 booleanos, 195 píxeles, filas 17 a 50 y columnas 131 a 138. Su orientación, [iEl, iAz] (índice de elevación, índice de acimut), es la de las filas y columnas de `hist.csv`. Huellas: `roi-mascaras.npz` `7546773b…`, contenido `3029f266…`, texto exportado `e76dcbe5…`.
- El binario carga el texto exportado, verificado por SHA-256, y escribe `in_rint` por muón. El análisis lo recalcula y exige un 100 % de acuerdo (K6).
- Orientación (K-ROI): `oe1_stage1_roi.py` usa como centroide de Z el punto (21,36; −30,71; 137,81) m, estimado por Monte Carlo en la entrega `712c786`. Desde el detector se ve a 7,93° de elevación y +1,80° de acimut relativo. Cae en el píxel (34, 135), dentro de R_int; su espejo en acimut (iAz → 255 − iAz) cae en la columna 120, fuera. Por simetría, la z exacta del centroide es 137,8 m; con ella, el píxel y los ángulos redondeados no cambian.
- Segunda comprobación: L_Z es la longitud en Z de la recta central de cada píxel. Al menos el 50 % de la suma de L_Z debe caer dentro de R_int, y la fracción que cae en la máscara espejada debe ser a lo sumo 0,1 veces la que cae en R_int. Si la geometría contradice la máscara, `oe1_stage1_roi.py kroi` termina con código 3.
- Ante esa contradicción, o ante un resultado posterior que la contradiga, se detiene el trabajo y se informa. La máscara no se redefine (PROT:59).
- En geo-train-01 la misma máscara actúa como control angular (PROT:59).

## 7. Controles K0 a K9

No hay K3 a K5: en su lugar van K-ROI y las pruebas técnicas de la sección 3.

| ID | Momento | Qué exige | ¿Bloquea? |
|---|---|---|---|
| K0 | antes y en el análisis | Antes:<br>diff(A2, B2) solo toca `src/DetectorConstruction.cc` y coincide con el diff A/B del piloto;<br>pruebas del detector de cruces;<br>banco sintético con Geant4, sin transporte (13 escenarios);<br>salida anticipada antes de `BeamOn`;<br>inercia del modo legado, comprobada sin transporte (T-L la repite con transporte);<br>pruebas de Python;<br>auditoría estática de aleatorios.<br>En el análisis: manifiesto de 13 corridas, `s_tr = s_src − 10⁹`, listas y máscara con sus SHA-256. | sí |
| K1 | antes | Seis listas de A2 y de B2 idénticas byte a byte.<br>`--check-primaries` igual en ambos binarios; comprueba N, `id` de 0 a N−1 sin duplicados de `id` ni de estado inicial, \|d\| = 1 ± 10⁻¹², dz < 0, Ekin > 0, PDG coherente con la carga y huella FNV igual a la del `.meta.json` de la lista.<br>Seis huellas FNV canónicas distintas, una por lista.<br>Validador de estructura, geometría y modelo de fuente: un valor p < 10⁻⁴ en sus pruebas estadísticas hace fallar K1 y se investiga antes de transportar. | sí |
| K2 | antes | `--check-geometry` de A2 y B2 en ambos casos (D-Q5).<br>Las cuatro salidas llevan la cabecera `resolution=100000 tolerance=0 maxErr=100 seed=20260929`.<br>B2: `status=OK`, `overlapping=0` y sin G4Exception; en geo-train-06, dos líneas `ANOMALY-CSG … clipped=no` (el margen de recorte de 1 mm no interviene), y en geo-train-01, ninguna.<br>A2 en geo-train-01: `status=OK`.<br>A2 en geo-train-06 reproduce el solape histórico. | sí, salvo el solape de A2 en geo-train-06, que solo se anota |
| K-ROI | antes | Sección 6. | sí |
| K6 | cada corrida | Filas = N = `events_transported`, con `id` de 0 a N−1 sin repetir.<br>Sin filas ABORTED ni archivos parciales `.part`.<br>`prim_fnv` recalculado desde la lista para todo id.<br>Histograma reconstruido desde las filas DET, igual en las 65.536 celdas.<br>`in_rint` igual al valor recalculado fuera de línea.<br>Desplazamiento lateral informado.<br>B sin avisos; los de A se comparan con los esperados.<br>Procedencia (variante, semillas, un hilo, gestor) igual al manifiesto.<br>Eficiencia comparada con la de la campaña (27.209.253/36.174.382 = 0,752169 en geo-train-06; 0,73795 en geo-train-01): si su z supera 5 en valor absoluto, se marca para lectura. | sí, salvo la eficiencia y los avisos de A, que solo se anotan |
| K7 | producción | Repetición A/A de geo-train-01 r1: `hist.csv` y `_muones.csv` idénticos byte a byte; `meta.json` igual salvo `wall_seconds`, `seconds_per_event` y las tres claves `rusage_*`; mismo nodo. | sí |
| K8 | producción | Control geo-train-01, A frente a B: registros e histogramas idénticos salvo la columna `variant`. | no; una diferencia se explica antes de atribuir nada (PROT:55) |
| K9 | producción | (a) `prim_fnv` y `rng0` iguales para todo id, en ambos casos.<br>(b) Clasificación de discordancias (DV9).<br>(c) En B, `lz_a0` y `lz_rock` ≤ 1 µm, salvo lo que explica el desplazamiento lateral: `lz_a0 + lz_rock ≤ 2√(2·R_max·Σlat)`, donde Σlat es `sum_lat_z_mm` pasado a metros. | (a) y (c) sí; (b) y las violaciones de (c) explicadas por el desplazamiento lateral, no |

`atribucion_al_solape_bloqueada`, en `contratos.json`, vale `true` si falla cualquier contrato no bloqueante de K8 o K9: una diferencia en el control, una clase sin explicar de K9 (b) o una violación de K9 (c) explicada por el desplazamiento lateral. En ese caso, no se atribuye nada al solape antes de leer esos casos por su `id`.

## 8. Ejecución en SC3

- Orden de ejecución. Cada paso empieza solo si el anterior terminó sin fallos, y hay a lo sumo un trabajo en cola:
  1. Fuentes A2 y B2 (`prepare_sources.sh`, en el nodo de acceso).
  2. Compilación Release sin avisos (`srun`).
  3. Pruebas de K0.
  4. `preparacion.sbatch` (K2, K1 y K-ROI; 2 CPU, 15 min).
  5. Manifiesto de producción de 13 filas (`make_manifest.py`).
  6. `pruebas_tecnicas.sbatch` (DV1).
  7. Commit de congelamiento: script de análisis, especificación de R_int, manifiesto y huellas esperadas.
  8. Ensayo en seco (`DRYRUN=1`), que imprime los 13 comandos.
  9. Trabajo principal (`principal.sbatch`).
- Las 13 corridas van en un solo `sbatch`, `principal.sbatch` (partición `legacy`, un nodo, 13 CPU, 8 GB, 30 min). `xargs -P 13` lanza a la vez los 13 procesos de un hilo en ese nodo. Motivo: la QoS admite cuatro trabajos enviados (MaxSubmitPU=4), y la repetición A/A y cada par A/B deben compartir nodo, CPU y libm.
- Cada intento escribe en una carpeta nueva, `corridas/intento-NN`, creada con `mkdir` sin `-p`; si ya existe, el script termina con código 3. Nada se sobrescribe ni se borra.
- Un fallo de infraestructura (tiempo agotado, nodo, cuota) obliga a relanzar las 13 corridas en `intento-NN+1`, con `MOTIVO.md` (causa, evidencia, cambio). `principal.sbatch` solo acepta el manifiesto completo, y la repetición A/A y cada par A/B deben compartir trabajo y nodo. Un fallo de código o de entradas obliga a corregir, recompilar, repetir de K0 a T-F y relanzar las 13 corridas. Cada reintento suma transportes y se informa.
- El script anula las cinco variables que fuerzan el gestor o los hilos (`G4FORCENUMBEROFTHREADS`, `G4FORCE_EVENTS_PER_TASK`, `G4FORCE_GRAINSIZE`, `G4RUN_MANAGER_TYPE`, `G4FORCE_RUN_MANAGER_TYPE`) y registra sus valores previos en `entorno.txt`, junto con el nodo, `lscpu` y los módulos.
- Cada corrida verifica sus entradas contra las huellas congeladas y guarda `entradas.sha256`, `comando.txt`, `run.log`, `recursos.json`, `avisos.txt`, `meta.json`, `hist.csv`, `_muones.csv` (49 columnas) y `SHA256SUMS`. En B, cualquier aviso de Geant4 hace fallar la corrida. En A, el aviso de solape `GeomVol1002=1` es lo esperado en geo-train-06 y se conserva como diagnóstico histórico; si la cuenta es distinta, la corrida no falla y el resultado queda como evidencia.
- `principal.sbatch` exige al menos 800 MB libres en `/home` (código de salida 2), y `pruebas_tecnicas.sbatch`, al menos 400 MB (código de salida 5). Con ≈ 1,46 GB libres el 30 de septiembre de 2026 solo cabe un intento de producción. El trabajo técnico o un segundo intento pueden exigir liberar antes `~/oe1-trabajo/etapa1-dev`, que no contiene evidencia.
- Después, `post_run.sh` archiva la salida de `sacct`, comprime con `gzip -n -9 -k`, registra el SHA-256 del archivo sin comprimir y del comprimido, y genera un tar por intento. Los archivos sin comprimir se conservan en SC3.

## 9. Salidas del análisis

- `oe1_stage1_analysis.py` evalúa primero los contratos. Si falla uno bloqueante, termina con código 3 y escribe solo `contratos.json`, `BLOQUEADO.txt` y `comando-analisis.txt`; con `--diagnostic-only` escribe además las tablas, todas con el sello `BLOQUEADO`. Los veredictos deben coincidir al reproducir el análisis en SC3 y localmente.
- Archivos: `contratos.json`, `resultados-etapa1.json`, `tabla-corridas.csv`, `transiciones.csv`, `matriz-clases.csv`, `cambios-bin.csv`, `muones-discordantes.csv`, `cruces-union.csv`, `mapas-etapa1.npz`, figuras opcionales y `comando-analisis.txt`.
- Por par (caso, réplica): n00, n01, n10 y n11, que suman N. n_ab cuenta los muones con (Y_A, Y_B) = (a, b), donde Y vale 1 si el muón se detecta dentro de R_int. Δ = (n01 − n10)/N, y 10⁶·Δ en cuentas por millón de primarios generados, con su denominador (N = 100.000).
- Por caso: Δ agrupado (N = 300.000) y media, DE (desviación estándar) y rango por réplica, con la frase «DE = 0 entre réplicas no implica incertidumbre cero» (PROT:76).
- La repetición A/A no entra en Δ, en las transiciones, en el agrupado ni en la DE.
- Diagnósticos (D-Q4): intervalo score de Tango, definido también sin discordancias, y McNemar exacto, que solo informa si hay discordancias. También se informan los límites exactos de Clopper-Pearson (95 %, bilaterales) de p_A y p_B, las probabilidades de detección en R_int con A y con B. Se rotulan como dato (ΣY, las detecciones en R_int, y N) y supuesto (ensayos independientes con una sola probabilidad). `intervalo_no_acota_el_efecto` vale siempre `true`.
- Secundarios:
  - eficiencia;
  - matriz 7 × 7 de clases (R_int, R_cond, R_body, R_rock, R_sky, sin clase, no detectado);
  - cambios de bin;
  - cruces en A, en B, en ambas y en la unión U, con Δ condicional y |U| (PROT:69);
  - mapas A/N, B/N y (B − A)/N, con el pie «diferencia neta; no identifica muones individuales»;
  - comparación de `crossed` con la recta inicial de cada primario de al menos 1.000 GeV.
- Margen de la etapa 2 (D-Q7): se propone después de la etapa 1, en `RESULTADOS_ETAPA_1.md`. Método previsto: M1 = k·√λ₃₀/N₃₀. Dato: λ₃₀ = 98 cuentas de R_int en N₃₀ = 36.174.382 primarios de la imagen de campaña de 30 días de geo-train-06, vista 0. Supuestos: conteo de Poisson y k = 1, donde k es el múltiplo de la desviación de Poisson. Con esos valores, M1 ≈ 2,7 × 10⁻⁷ por primario.

## 10. Fuera de alcance

- La ejecución de la etapa 2; sus valores se fijarán en una versión 1.1 del protocolo (PROT:80).
- La repetición de las 114 vistas y el reprocesamiento de la campaña (PROT:3, PROT:82).
- Cambios en la entrega anterior (`712c786`, rama `oe1/geo-train-06-piloto`) y en el piloto. En SC3, `A0`, `A`, `B`, `build-*` y `salidas/` solo se leen o se copian, y T-L ejecuta los binarios del piloto sin escribir en sus carpetas.
- El muestreo dirigido hacia R_int o hacia Z; la lista sintética de T-S es un control técnico.
- Las corridas de desarrollo con transporte local (WSL, Geant4 11.4.2 compilado allí), que no son evidencia del ensayo.

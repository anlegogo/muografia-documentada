# Revisión independiente de la etapa 1 del segundo ensayo OE1

**Fecha:** 30 de septiembre de 2026, Colombia (UTC−5). **Alcance:** OE1, geo-train-06 y geo-train-01, vista 0. Implementación y transporte: Daniel y Reinaldo en SC3. Revisión: descarga, comprobación independiente y reproducción local del análisis; no se ejecutó Geant4 en esta revisión.

**Dictamen:** la entrega respalda el funcionamiento técnico y la reproducibilidad del análisis de esta etapa. Se confirman los resultados nulos de las 13 corridas. La validación física sigue abierta: falta cubrir la entrada al solape desde el conducto y dimensionar el ensayo representativo. No se aprueba con este documento la etapa 2 ni repetir las 114 vistas.

## 1. Fuentes y trazabilidad

- [Entrega de los estudiantes, commit 3a49770](https://github.com/anlegogo/muografia-documentada/tree/3a4977030a4193098ee66057fbd3c63603d7fa76/objetivo-1/entregas/2026-09-30-segundo-ensayo-etapa-1), rama `oe1/segundo-ensayo-etapa-1`.
- [Código y herramientas, commit 3315f82](https://github.com/Dp100131/muography-dl-reconstruction/tree/3315f82ffa1a3be604897e34e2319b379f500655), rama `oe1/stage1-instrumentation`. A2: `fdaef4b`; B2: `9bb43f3`.
- [Paquete compartido en Drive](https://drive.google.com/drive/folders/1a9VcFXk8JAe8ClxWo81sXA7Jhr4kkk89): `intento-01.tar`, seis listas de primarios y sus metadatos. Se descargaron los archivos; no se evaluaron solo las tablas del informe.
- [Protocolo aplicado, v1.0](PROTOCOLO_SEGUNDO_ENSAYO_OE1.md), congelado en `1054fb8`.
- Evidencia propia: [156 controles independientes](evidencias/revision-etapa1-3a49770.json) y [resumen de reproducción](evidencias/reproduccion-etapa1-3a49770.json). El [auditor](../herramientas/revisar_etapa1_oe1.py) no importa módulos de análisis de los estudiantes.

El conector de Drive agotó el tiempo al descargar el TAR; la descarga directa del archivo compartido terminó correctamente. El TAR tiene 132.864.000 bytes y SHA-256 `53b05115b94bd8d60be674606cb265d16b375536111fd464143da866d4a0c5de`. Los datos se conservan fuera del historial Git. Las ramas de entrega no se fusionan como parte de esta revisión.

## 2. Qué se verificó

| Control | Resultado y alcance |
|---|---|
| Integridad de la entrega | 523/523 entradas del manifiesto de archivos versionados coinciden. |
| Datos grandes | Coinciden las 7 huellas del manifiesto de Drive: TAR y seis listas; también 26/26 archivos crudos y 26/26 comprimidos del manifiesto de producción. Se comprobó además el TAR de pruebas técnicas. |
| Código de análisis | Las seis huellas de scripts coinciden con las registradas en SC3. El diff A2→B2 es idéntico al diff A→B y solo modifica `DetectorConstruction.cc`. Esto no sustituye recompilar los ejecutables en SC3. |
| Reproducción con herramientas de autores | Termina con código 0; 405 comprobaciones OK, sin fallos bloqueantes ni no bloqueantes. |
| Comparación de salidas | Las seis tablas CSV reproducidas son idénticas byte a byte a SC3 y los seis mapas son iguales. Los JSON solo difieren en fecha, rutas y entorno; ningún resultado científico cambia. |
| Verificación independiente | 156 controles propios sin fallos: listas, huellas de primarios, identificación, registros, histogramas, ROI, emparejamiento y pruebas técnicas. |
| Listas y registros | 100.000 filas por corrida, identificadores 0…99.999; huella de lista correcta y huella del primario recalculada desde sus coordenadas, dirección, energía y PDG para todas las filas. |
| Histogramas | Se reconstruyen las 65.536 celdas de las 13 imágenes desde sus registros por muón; coincidencia exacta. Se recalcula la pertenencia a R_int. |
| A/A | El registro completo de la repetición de geo-train-01, réplica 1, es idéntico byte a byte al de su referencia. No se cuenta como réplica independiente. |
| A/B | En los seis pares, todos los campos por muón son iguales salvo la etiqueta de variante: estado, detección, píxel, energías, longitudes y huellas aleatorias incluidas. Se compararon 600.000 pares, no solo imágenes agregadas. |

El recálculo de las huellas FNV verifica el contrato de primarios de esta implementación. La revisión no constituye una prueba formal de independencia del generador aleatorio ni una validación integral de la física de Geant4.

## 3. Resultados de producción confirmados

| Caso, tres réplicas agrupadas | Pares A/B | Detectados por variante | Detectados en R_int por variante | Cambios 0→1 / 1→0 en R_int | Cruces registrados de Z por variante |
|---|---:|---:|---:|---:|---:|
| geo-train-06 | 300.000 | 225.667 | 1 | 0 / 0 | 1 |
| geo-train-01, control angular | 300.000 | 221.245 | 1 | 0 / 0 | No aplica |

Con la repetición A/A se totalizan 1.300.000 transportes de producción. La diferencia estimada en R_int es cero en ambos casos; eso no demuestra equivalencia física. El intervalo diagnóstico reportado y reproducido es aproximadamente [−12,805; 12,805] cuentas por millón para cada caso agrupado. La desviación cero entre las tres réplicas no significa incertidumbre cero.

El único cruce registrado corresponde a geo-train-06, réplica 2, id 3910, en ambas variantes. Tiene 25,6238698 m de cuerda dentro de Z, todos asignados a A1 (cuerpo denso), y termina por captura sin llegar al detector. **Este muón no es la detección de R_int de esa réplica.** Una región angular de la imagen y la intersección 3D son observables distintos.

Un cálculo independiente de las rectas iniciales encuentra 39, 48 y 51 intersecciones ideales con Z por réplica; no equivale a 138 cruces transportados, porque el muón puede perder energía, desviarse o finalizar antes. Ninguna de las rectas de muones de al menos 1.000 GeV cruza Z: por ello, el acuerdo de alta energía de producción comprueba únicamente casos negativos.

## 4. Pruebas técnicas y cobertura que falta

Desde los crudos se comprobaron:

- T-L: histogramas iguales entre binarios anteriores e instrumentados, en A y B, en modo legado.
- T-R: identidad, estado, número de pasos, bin y huellas aleatorias iguales con registro completo y mínimo, para los 2.000 muones de B2.
- T-M: esos resultados se mantienen al cambiar la semilla maestra, conservando la semilla de transporte por muón.
- T-P: las 100 primeras filas corresponden a primarios distintos; desde el id 100 se conservan identidad y resultados.
- T-S: 60/60 clasificaciones correctas en A2 y B2 al compararlas con una intersección analítica independiente de las rectas. Los 20 cruces tienen longitudes dentro del 1 % de la referencia; discrepancia máxima 0,185 %. En B, la longitud en Z corresponde al cuerpo denso.

**Hallazgo R2-01 — cobertura de materiales incompleta.** Los 20 cruces sintéticos de T-S entran, según sus rectas iniciales, desde el elipsoide hacia el cilindro. En A2 todos registran `mat_in=A1` y `lz_a0_m=0`; los 60 registros de A2/B2 son iguales salvo `variant`. No hay un caso sintético que entre a Z desde el conducto. La producción tampoco registra longitud en Z asignada al conducto. El criterio de T-S para A (`lz_a0 + lz_a1 = lz`) puede pasar con `lz_a0=0` en todos los casos, como ocurrió aquí.

Este hallazgo no invalida la detección de cruces comprobada ni exige repetir las 13 corridas. Delimita su cobertura: no se ha contrastado experimentalmente la situación en que la geometría original puede asignar material del conducto a la intersección.

Las 453.607 comprobaciones C++ y las compilaciones con sanitizadores se conservan como evidencia **reportada de SC3**; no se recompilaron en esta revisión. El contraste independiente de T-S no reproduce todos esos ensayos. Las longitudes y energías interpoladas se apoyan en cuerdas de pasos; no deben presentarse como una reconstrucción exacta de la trayectoria física entre sus extremos.

## 5. Observaciones y condiciones para avanzar

| ID | Observación | Acción / criterio de cierre |
|---|---|---|
| R2-01 | Falta cubrir entrada desde el conducto en los controles de transporte. | Preparar un complemento pequeño y separado de la muestra representativa. Congelar trayectorias de ambos lados, explicar geométricamente su lado de entrada y registrar los pasos próximos a Z, materiales, longitudes y energía. B debe respetar la prioridad A1; A se conserva como diagnóstico de navegación defectuosa, no como verdad física. |
| R2-02 | Solo un cruce en producción, sin discordancias. | Mantener la conclusión física como inconclusa. No convertir cero cambios en tasa real cero, ni concluir que la campaña histórica queda validada. |
| R2-03 | El margen M1 y el tamaño de etapa 2 siguen siendo una propuesta. | Justificar el criterio físico de relevancia: k=1 veces el ruido de Poisson de R_int a 30 días es una elección que debe motivarse y relacionarse con los niveles de conteo del OE1. Fijar método, nivel de confianza y tamaño antes de datos nuevos. |
| R2-04 | Los ≈14 millones de primarios por caso suponen que vuelven a observarse cero discordancias. | Tratarlo como escenario de cálculo, no garantía de potencia o precisión. Prever el caso con discordancias y un resultado inconcluso. Resolver almacenamiento y bloqueo de tamaño antes de ejecutar. |

No se solicita aumentar la muestra dirigida hasta obtener un resultado favorable. Su finalidad es comprobar un mecanismo con casos definidos de antemano; no estimar la frecuencia natural del efecto. La posterior comparación de imágenes debe conservar la fuente representativa, o documentar un muestreo con ponderaciones y una incertidumbre justificadas.

**Siguiente paso recomendado:** elaborar el complemento de R2-01 con listas y criterios previos. Revisarlo antes de ampliar la producción. Después se podrá cerrar la versión 1.1 del protocolo: margen, incertidumbre, réplicas nuevas, almacenamiento y recursos. Las cifras de la propuesta de estudiantes aún no son un plan autorizado por esta revisión.

## 6. Reproducción local

Entorno utilizado: Python 3.12.14, NumPy 2.4.4 y pandas 3.0.6, Windows. Los archivos de entrada se conservaron sin cambios científicos. En una exportación de Git en Windows se deben verificar los bytes contra el manifiesto; si los finales de línea fueron convertidos, recuperar el blob Git correspondiente, no modificar el manifiesto para hacerlo coincidir.

La revisión usa estas carpetas relativas al directorio de trabajo que contiene ambos repositorios:

```text
tmp/revision-entrega-3a49770/objetivo-1/entregas/2026-09-30-segundo-ensayo-etapa-1/
tmp/codigo-etapa1-3315f82/                  # código de 3315f82
tmp/datos-etapa1-drive/listas/              # seis CSV y sus metadatos
tmp/datos-etapa1-drive/produccion/intento-01/
tmp/datos-etapa1-drive/tecnicas/tecnicas-01/
tmp/revision-etapa1-reproduccion-director/  # salida del análisis de autores
```

Descargar y verificar el TAR y las listas contra `datos-compartidos/SHA256SUMS.txt`. Extraer el TAR de producción y `pruebas/crudos-tecnicos-01.tar.gz` a las carpetas indicadas; rechazar rutas que salgan del destino y enlaces del TAR. Descomprimir los `*.csv.gz` preservando los comprimidos.

Ejecutar `scripts/analysis/oe1_stage1_analysis.py` del código descargado con `--attempt` apuntando a producción, `--lists-dir` a las seis listas, `--roi-mask`, `--roi-frozen` y `--roi-npz` a `analisis/roi/` de la entrega, `--no-figures` y una carpeta nueva en `--out`. La referencia geométrica es `scripts/simulation/geant4_app/tests/crossing_reference.py` del mismo código; la herramienta puede localizarla automáticamente. No usar `--skip-muon-fnv` ni `--diagnostic-only` para esta reproducción.

Después, ejecutar el auditor (los marcadores representan las carpetas anteriores):

```text
python muografia-documentada/herramientas/revisar_etapa1_oe1.py --entrega ENTREGA --datos DATOS --codigo CODIGO --reproduccion SALIDA_AUTORES --out SALIDA_REVISION.json
```

Se esperan código 0, 156 controles propios sin fallos y 405 comprobaciones del análisis de autores sin fallos. El auditor preserva entradas y escribe solo su JSON de salida. Sus controles de igualdad describen **esta entrega**; una futura diferencia A/B puede ser un resultado físico a investigar y no un error del simulador.

## 7. Efecto sobre el cumplimiento del OE1

P-01 avanza: ya hay comparación individual trazable y reproducible, además de controles geométricos. Sigue pendiente cuantificar el impacto y decidir qué parte del conjunto requiere regeneración. P-02 avanza en documentación y reproducción del análisis de este entorno SC3; no se acredita equivalencia entre versiones de Geant4. P-03/P-04 siguen abiertos.

No se modifica el catálogo, la corrección implementada por los estudiantes, los datos históricos ni el protocolo v1.0 congelado. Esta revisión se incorpora como evidencia propia separada de la entrega y de la decisión académica final.

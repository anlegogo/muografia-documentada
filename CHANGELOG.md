# Registro de cambios

## Auditoría íntegra de etapa 2 — 2026-10-01, Colombia

- Se descargan y verifican 85 archivos (6.685.463.186 bytes), 27 listas y 55 registros completos contra sus huellas congeladas. Los enlaces caducados se recuperaron sin alterar contenido.
- Auditor independiente: 6.966 controles satisfactorios; 605 controles de configuración y 737 archivos auxiliares concordantes. Se verifican 24,3 millones de primarios distintos y los registros correspondientes a 48,7 millones de transportes, incluida A/A por identidad byte a byte.
- Se reproduce Delta=+0,125 por millón e IC95 % [−0,229; +0,469], inconcluso. La comparación de todas las columnas muestra 56 pares distintos: 51 cruces desde conducto y cinco sin cruce registrado, sin efecto de estos últimos en detección/píxel. Se detallan IDs y valores; se precisa el significado de energía final del tramo en Z.
- [Informe completo](objetivo-1/AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md). La auditoría de crudos deja de estar pendiente; producción B requiere resolver entorno/normalización/alcance. OE1 y P-01…P-04 siguen abiertos. No se ejecuta Geant4 ni se contacta a estudiantes.

## Revisión del agregado de etapa 2 — 2026-10-01, Colombia

- Entrega `f88de14`, código `d8ca749`: [revisión](objetivo-1/REVISION_ETAPA_2_2026-10-01.md) de informe, manifiesto, 55 histogramas/metadatos y agregado. 1.247 controles propios satisfactorios y 12 pruebas de autores reproducidas. No se ejecutó transporte.
- Se confirma la categoría inconcluso. Los cuatro CSV agregados se reproducen byte a byte; los cambios seleccionados explican el mapa diferencial.
- Observaciones: identidad limitada a columnas seleccionadas, pérdida de energía distinta de energía de salida y desviación de almacenamiento. Se verificó acceso a Drive, sin descargar/auditar íntegramente los registros grandes en esta revisión.
- Próximo paso: corregir interpretación, completar auditoría de crudos y preparar producción B con entorno/normalización/alcance resueltos. No ampliar automáticamente N; OE1 y P-01…P-04 siguen abiertos.

## Diseño de etapa 2 — 2026-10-01, Colombia

- Por solicitud del director se fija [protocolo v1.1](objetivo-1/PROTOCOLO_ETAPA_2_OE1_V1_1.md), separado del v1.0 histórico. Tamaño fijo: 24 millones de pares principales; 55 corridas y 48,7 millones de transportes con controles. No se ejecutó Geant4 ni se enviaron trabajos a SC3.
- Margen operativo ligado al ruido de conteo de la ROI histórica; intervalo conservador al menos 95 % construido con límites binomiales exactos. Escenarios con cero, una y varias discordancias; resultado inconcluso permitido sin ampliación automática.
- Se incorporan manifiesto, calculador, seis pruebas satisfactorias e instrucciones. Almacenamiento mínimo propuesto: 30 GiB con cuota/retención por verificar; preparación y adaptación de scripts a cargo de estudiantes.
- OE1 y P-01…P-04 siguen abiertos. Se separan alcance de una ROI, regeneración de datos y validación física del conjunto.

## Revisión del complemento R2-01 — 2026-10-01, Colombia

- Revisión local de entrega `a4d7b79`, ejecutada por los estudiantes en SC3 el 30 de septiembre. Comparador `0d97beb` reproducido y auditoría propia: 103/103 controles satisfactorios.
- B asigna el solape al cuerpo denso en 36/36 pares; A lo asigna al conducto en los 18 casos dirigidos desde ese lado. Tres pares cambian de píxel; ninguno cambia su detección.
- Se conserva la limitación del lado inferido en B y de la fuente dirigida; no se estima la frecuencia en la campaña. P-01…P-04 siguen abiertos. Siguiente paso: dimensionar etapa 2 y resolver almacenamiento, sin aprobar ni lanzar todavía una campaña.
- [Revisión, evidencia y comandos](objetivo-1/REVISION_COMPLEMENTO_R2_01_2026-10-01.md).

## Preparación local del complemento R2-01 — 2026-09-30, Colombia

- Se prepara un complemento técnico con 12 muones dirigidos: seis entradas desde el conducto y seis desde el cuerpo denso; 72 transportes propuestos en SC3.
- Se añaden generador, CSV, metadatos, huellas, longitudes esperadas, ejecutor y guía. Validación local de estructura/panel OK y acuerdo entre dos cálculos geométricos.
- La ejecución Geant4 sigue pendiente; no se modifica ni aprueba la etapa 2. [Diseño](objetivo-1/COMPLEMENTO_R2_01.md).

## Revisión de etapa 1 — 2026-09-30, Colombia

- Descarga y verificación del paquete completo de etapa 1, incluidas seis listas y 13 registros por muón.
- Análisis de autores reproducido (405 comprobaciones) y auditor independiente (156 controles), sin fallos.
- Se documenta R2-01: los cruces sintéticos cubren entrada desde el elipsoide, no desde el conducto. No se declara equivalencia física ni se aprueba etapa 2.
- Informe: [revisión de etapa 1](objetivo-1/REVISION_ETAPA_1_2026-09-30.md). Se mantienen las entregas en sus ramas.

## Protocolo del segundo ensayo v1.0 — 2026-09-29

- Diseño documentado desde la revisión: etapa técnica acotada, primarios comunes, observable principal y entregables.
- Se sustituye el encargo de diseño desde cero; la etapa física de mayor estadística permanece condicionada a revisión.
- Se aclara que los recursos de cómputo no constituyen presupuesto económico.

## Extensión del control geométrico — 2026-09-29

- Se contrastan independientemente los volúmenes de las cuatro intersecciones conocidas del catálogo y sus fracciones del volumen del conducto.
- Se registran límites de interpretación: volumen no equivale a sensibilidad muográfica ni a efecto en conteos; el siguiente ensayo permanece pendiente de diseño.

## Control independiente adicional — 2026-09-29

- Se incorpora cálculo de volumen por cuadratura y contraste con la entrega, sin modificar fuentes originales.
- Se documentan coincidencias y límites de la asignación de materiales, incluida la densidad del aire.

## Revisión de entrega y encargo de diseño — 2026-09-29, Colombia

- Se documenta la revisión independiente de la entrega `712c786`, con observaciones y evidencia de recálculo.
- Se actualizan seguimiento, matriz e índice; el primer encargo queda identificado como histórico.
- Se solicita el diseño del segundo ensayo antes de ampliar simulaciones; sin fusión de resultados ni cierre del OE1.

## Revisión técnica del OE1 y preparación de instrucciones — 2026-09-28, Colombia

- Diagnóstico analítico del catálogo: intersecciones entre anomalías en cuatro geometrías y salidas del edificio en otras dos.
- Reproducción en memoria de 9.120 pares: coincidencia exacta, semillas consistentes y sin saturación uint16.
- Se incorporan diagnóstico, revisión de datos, instrucciones para SC3 y plantilla de entrega.
- Se añaden auditor local, ejecutor de piloto y comparador; su ejecución Geant4/SLURM queda pendiente en SC3.
- No se modifica ningún archivo original ni se declara cerrada la validación física.

## Publicación privada en GitHub

- Destino autorizado: `anlegogo/muografia-documentada`; rama `main`.
- Se registra la organización inicial con la identidad GitHub verificada del director, preservando la atribución del material recibido.
- Los datos NPZ y logs se mantienen fuera del historial; su restauración e integridad se documentan en `docs/PROCEDENCIA.md`.

## Incorporación inicial — 2026-09-29T03:08:48.514624+00:00

- Se incorpora una selección local del OE1 desde `b88fa576494cb8a664c46b8c94c5918c5097d616`.
- Se preservan 567 archivos originales con inventario de procedencia y SHA-256.
- Se documentan alcance, datos, cumplimiento, reproducción, pendientes y decisiones.
- Se incluyen datos y logs en disco, excluidos del historial Git.
- Se incorpora un verificador de integridad de solo lectura sobre originales.
- No se modifica código científico ni se ejecuta una nueva campaña. No se incorporan OE2/OE3.

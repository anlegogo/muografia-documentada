# Registro de cambios

## Correcciones locales de fusión y configuración — 2026-10-02

- Nueva fusión estricta, con rechazo de bloques/semillas repetidos o contradictorios, agregados corregidos y verificación SHA exacta o conversión CRLF->LF explícita y trazable. Preserva entradas.
- Empaquetador actualizado para distinguir inyección, margen, plano, selección energética y definiciones de fuente/normalización. Se protege la conservación de bytes de futuras entregas SC3.
- 56 pruebas locales satisfactorias. Dos bloques reales: 200.000 primarios, 69.995 registros seleccionados y 130.190 sin corte; matriz conservada, exportación y lectura satisfactorias.
- [Instrucciones de adopción y límites](objetivo-1/CORRECCIONES_LOCALES_FUSION_CONFIGURACION.md). Rama estudiantil intacta; no se actualizan SC3 ni su lanzador y no se autoriza campaña física.

## Revisión de justificación física y producción — 2026-10-02

- Revisada la entrega f9a77ef sin fusionar su rama. Se ejecutan seis análisis y coinciden 3.045 valores numéricos; 114 histogramas históricos reconstruidos coinciden con el manifiesto.
- Se verifican 19 corridas (92 millones de primarios) y la fusión de integración de 200.000 primarios/69.995 registros, tras normalización de líneas en copia temporal. 181/200 huellas de controles requieren esa normalización.
- Se documentan límites de C1/C2/C3/C5, C4 aún no cumplido, metadatos agregados incorrectos y aceptación de semillas contradictorias/bloques repetidos. Nuestra firma de empaquetado también requiere reconocer las opciones nuevas.
- [Dictamen y siguiente entrega acotada](objetivo-1/REVISION_FISICA_PRODUCCION_2026-10-02.md). No se autoriza campaña final, no se ejecuta Geant4 localmente y no se envían mensajes a estudiantes.

## Consolidación de la cadena local — 2026-10-01, Colombia

- Por autorización del director se completa una alternativa de representación, auditoría multivista y empaquetado binomial versionado: seis vistas por geometría, 80 pares por vista, semillas estables por identidad y uint32 sin recorte. No se generan referencias físicas inexistentes.
- 41 pruebas satisfactorias. Se reexporta la vista real de 750 conteos con huellas de ejecutable/tablas y se representa con bordes correctos; figura inspeccionada y corregida. Auditoría real: una vista de prueba, no campaña final.
- Se amplía la búsqueda de respaldo en historia Git y se documenta la superficie/umbral de aire de la normalización heredada. No se afirma un sesgo físico cuantificado.
- README, matriz y pendientes consolidados para eliminar estados contradictorios. [Guía única, comandos y siguiente entrega](objetivo-1/CADENA_LOCAL_OE1.md). Requiere evidencia de convergencia/normalización y receta SC3 antes de fijar producción. No se envían mensajes ni trabajos al supercomputador.

## Aceptación del plano: revisión conceptual — 2026-10-01, Colombia

- Se revisa la evidencia local de planos 100/300/600 m y se distingue convergencia numérica de aceptación del panel físico. La cota histórica respecto a la asíntota no se reproduce con los materiales identificados.
- [Derivación y control reproducible](objetivo-1/REVISION_ACEPTACION_PLANO.md): contraejemplo 1D exacto y cuadratura, nueve combinaciones. No es Geant4 ni estima el sesgo del volcán.
- P-04 acotado a observable, compensación, generación espacial y normalización. Revisar primero respaldo existente; no se prescribe ni ejecuta otra campaña.

## Integración de regiones y lectura — 2026-10-01, Colombia

- Analizador de conteos dentro/fuera de ROI candidata con validación de geometría, vista, coordenadas, huellas y contenido. Exportador ampliado para preservar procedencia de geometría desde entradas.sha256.
- Ocho pruebas del analizador y nueve del exportador satisfactorias. Rechazo real correcto de imagen geo-train-01 contra ROI geo-train-06; no se generan resultados físicos inexistentes de geo-train-06.
- [Uso y límites](objetivo-1/ADAPTACION_LECTURA_ANGULAR.md#análisis-integrado-de-regiones-candidatas). Integración local disponible; empaquetado definitivo y aceptación física pendientes.

## Regiones geométricas con malla v1 — 2026-10-01, Colombia

- Cálculo propio de seis ROI candidatas de geo-train-06, umbral fijo de 20 m y rayos centrales. Ocho pruebas pasan; 393.216 rayos contrastados con referencia externa, máscaras coincidentes y error máximo 1,33e-10 m.
- Vista 0: 193 píxeles nuevos, 194 con centros antiguos recalculados y 195 en la máscara histórica. Se separa el efecto del recálculo del cambio angular; no se reescribe el ensayo previo.
- [Método y evidencia](objetivo-1/REGIONES_ANGULARES_V1.md). Sin transporte nuevo; integración de consumidores y aceptación física pendientes.

## Lectura y exportación angular — 2026-10-01, Colombia

- Nueva herramienta con coordenadas explícitas y rechazo de mallas incompatibles. Exportación de la entrega 90abb96: 750 conteos conservados píxel a píxel. Siete pruebas específicas satisfactorias.
- [Adaptación y auditoría de consumidores](objetivo-1/ADAPTACION_LECTURA_ANGULAR.md): no se modifica la cadena histórica; ROI y empaquetado definitivo continúan pendientes. No se ejecuta Geant4 ni se solicita otra corrida.

## Revisión de entrega angular — 2026-10-01, Colombia

- Entrega 90abb96 y código 0dea8e1: 1.000 primarios, 750 registros; 24 controles locales y 31 contrastes de huellas/código satisfactorios. Se recibe evidencia de prueba C++ y corrida Geant4 en SC3.
- [Revisión independiente](objetivo-1/REVISION_MALLA_ANGULAR_2026-10-01.md). Sin recompilar localmente ni fusionar la rama de entrega. No hace falta repetir esta corrida.
- Mejora operativa para futuras ejecuciones: propagar el código del simulador al trabajo SLURM. Próximo paso: consumidores de malla y justificación física del conteo/exposición; OE1 sigue abierto.

## Revisor de integración angular — 2026-10-01, Colombia

- Se prepara revisar_smoke_angular.py para revisar metadatos, histograma, log y código de salida de la corrida de 1.000 primarios. Registra huellas; rechaza sobrescribir informes.
- Ocho pruebas sintéticas satisfactorias, incluidos archivos truncados, malla antigua y fallos de ejecución. No representan una corrida Geant4.
- [Instrucciones y evidencia](objetivo-1/correcciones/malla-angular-v1/README.md#revisión-automática-de-la-entrega). Se añade captura del log y del estado real del proceso. Compilación y corrida SC3 pendientes; P-04 permanece abierto.

## Corrección azimutal propuesta — 2026-10-01, Colombia

- A solicitud del director se prepara un parche separado sobre d8ca749: 256 celdas iguales en [-30,30], centros actualizados, conteo Geant4, metadatos versionados y conversión de tablas por 255/256. Originales y entregas congeladas intactos.
- Seis pruebas Python satisfactorias; 1.048.576 direcciones repartidas por igual. Aplicabilidad y diez huellas del parche comprobadas. La conversión CRLF de Git se resolvió repitiendo la verificación con core.autocrlf=false.
- [Paquete y comandos](objetivo-1/correcciones/malla-angular-v1/README.md). Prueba C++ preparada pero no ejecutada; compilación Geant4 e integración de 1.000 primarios quedan para SC3. No habilita producción ni cierra P-04; faltan consumidores de malla y validación de aceptación física.

## Control de muestreo angular — 2026-10-01, Colombia

- Revisión local del director: integración exacta de celdas y cuadratura de 1.044.480 direcciones; diferencia máxima 1,39e-17. Las dos columnas de borde tienen 0,50196 veces la probabilidad nominal; las interiores 1,00392. Probabilidad total conservada.
- Se documenta el soporte real en elevación y el efecto diminuto de redondeo de tablas. [Evidencia y límites](objetivo-1/CONTROL_MUESTREO_ANGULAR.md).
- Próximo paso: fijar centros/bordes/dominio angular y normalización antes de decidir reutilización. No se cambian originales, no se ejecuta Geant4 y no se modifica el resultado A/B. P-04 abierto.

## Preparación de producción — 2026-10-01, Colombia

- Revisión local del director: 114 referencias verificadas contra sus huellas; inventario reproducible de 36 vistas candidatas a regeneración y 78 de reutilización condicionada.
- Se comprueba la suma de pesos y se documenta la diferencia entre impacto nominal en panel de 1,2 m y registro en plano de 600 m. La consistencia de las tablas no certifica exposición física.
- [Plan y siguiente entrega](objetivo-1/PREPARACION_PRODUCCION_OE1.md): definir observable y normalización, justificar aceptación, congelar entorno y receta B. No se ejecutó transporte. P-01…P-04 abiertos.

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

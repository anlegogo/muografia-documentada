# Bitácora de nuestra revisión del OE1

## Lectura y exportación angular — 2026-10-01, Colombia

- Nueva herramienta con coordenadas explícitas y rechazo de mallas incompatibles. Exportación de la entrega 90abb96: 750 conteos conservados píxel a píxel. Siete pruebas específicas satisfactorias.
- [Adaptación y auditoría de consumidores](ADAPTACION_LECTURA_ANGULAR.md): no se modifica la cadena histórica; ROI y empaquetado definitivo continúan pendientes. No se ejecuta Geant4 ni se solicita otra corrida.

## Revisión de entrega angular — 2026-10-01, Colombia

- Entrega 90abb96 y código 0dea8e1: 1.000 primarios, 750 registros; 24 controles locales y 31 contrastes de huellas/código satisfactorios. Se recibe evidencia de prueba C++ y corrida Geant4 en SC3.
- [Revisión independiente](REVISION_MALLA_ANGULAR_2026-10-01.md). Sin recompilar localmente ni fusionar la rama de entrega. No hace falta repetir esta corrida.
- Mejora operativa para futuras ejecuciones: propagar el código del simulador al trabajo SLURM. Próximo paso: consumidores de malla y justificación física del conteo/exposición; OE1 sigue abierto.

## Revisor de integración angular — 2026-10-01, Colombia

- Se prepara revisar_smoke_angular.py para revisar metadatos, histograma, log y código de salida de la corrida de 1.000 primarios. Registra huellas; rechaza sobrescribir informes.
- Ocho pruebas sintéticas satisfactorias, incluidos archivos truncados, malla antigua y fallos de ejecución. No representan una corrida Geant4.
- [Instrucciones y evidencia](correcciones/malla-angular-v1/README.md#revisión-automática-de-la-entrega). Se añade captura del log y del estado real del proceso. Compilación y corrida SC3 pendientes; P-04 permanece abierto.

## Corrección azimutal propuesta — 2026-10-01, Colombia

- A solicitud del director se prepara un parche separado sobre d8ca749: 256 celdas iguales en [-30,30], centros actualizados, conteo Geant4, metadatos versionados y conversión de tablas por 255/256. Originales y entregas congeladas intactos.
- Seis pruebas Python satisfactorias; 1.048.576 direcciones repartidas por igual. Aplicabilidad y diez huellas del parche comprobadas. La conversión CRLF de Git se resolvió repitiendo la verificación con core.autocrlf=false.
- [Paquete y comandos](correcciones/malla-angular-v1/README.md). Prueba C++ preparada pero no ejecutada; compilación Geant4 e integración de 1.000 primarios quedan para SC3. No habilita producción ni cierra P-04; faltan consumidores de malla y validación de aceptación física.

## Control de muestreo angular — 2026-10-01, Colombia

- Revisión local del director: integración exacta de celdas y cuadratura de 1.044.480 direcciones; diferencia máxima 1,39e-17. Las dos columnas de borde tienen 0,50196 veces la probabilidad nominal; las interiores 1,00392. Probabilidad total conservada.
- Se documenta el soporte real en elevación y el efecto diminuto de redondeo de tablas. [Evidencia y límites](CONTROL_MUESTREO_ANGULAR.md).
- Próximo paso: fijar centros/bordes/dominio angular y normalización antes de decidir reutilización. No se cambian originales, no se ejecuta Geant4 y no se modifica el resultado A/B. P-04 abierto.

## Preparación de producción — 2026-10-01, Colombia

- Revisión local del director: 114 referencias verificadas contra sus huellas; inventario reproducible de 36 vistas candidatas a regeneración y 78 de reutilización condicionada.
- Se comprueba la suma de pesos y se documenta la diferencia entre impacto nominal en panel de 1,2 m y registro en plano de 600 m. La consistencia de las tablas no certifica exposición física.
- [Plan y siguiente entrega](PREPARACION_PRODUCCION_OE1.md): definir observable y normalización, justificar aceptación, congelar entorno y receta B. No se ejecutó transporte. P-01…P-04 abiertos.

## Auditoría íntegra de etapa 2 — 2026-10-01, Colombia

- Se descargan y verifican 85 archivos (6.685.463.186 bytes), 27 listas y 55 registros completos contra sus huellas congeladas. Los enlaces caducados se recuperaron sin alterar contenido.
- Auditor independiente: 6.966 controles satisfactorios; 605 controles de configuración y 737 archivos auxiliares concordantes. Se verifican 24,3 millones de primarios distintos y los registros correspondientes a 48,7 millones de transportes, incluida A/A por identidad byte a byte.
- Se reproduce Delta=+0,125 por millón e IC95 % [−0,229; +0,469], inconcluso. La comparación de todas las columnas muestra 56 pares distintos: 51 cruces desde conducto y cinco sin cruce registrado, sin efecto de estos últimos en detección/píxel. Se detallan IDs y valores; se precisa el significado de energía final del tramo en Z.
- [Informe completo](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md). La auditoría de crudos deja de estar pendiente; producción B requiere resolver entorno/normalización/alcance. OE1 y P-01…P-04 siguen abiertos. No se ejecuta Geant4 ni se contacta a estudiantes.

## Revisión del agregado de etapa 2 — 2026-10-01, Colombia

- Entrega `f88de14`, código `d8ca749`: [revisión](REVISION_ETAPA_2_2026-10-01.md) de informe, manifiesto, 55 histogramas/metadatos y agregado. 1.247 controles propios satisfactorios y 12 pruebas de autores reproducidas. No se ejecutó transporte.
- Se confirma la categoría inconcluso. Los cuatro CSV agregados se reproducen byte a byte; los cambios seleccionados explican el mapa diferencial.
- Observaciones: identidad limitada a columnas seleccionadas, pérdida de energía distinta de energía de salida y desviación de almacenamiento. Se verificó acceso a Drive, sin descargar/auditar íntegramente los registros grandes en esta revisión.
- Próximo paso: corregir interpretación, completar auditoría de crudos y preparar producción B con entorno/normalización/alcance resueltos. No ampliar automáticamente N; OE1 y P-01…P-04 siguen abiertos.

## Diseño de etapa 2 — 2026-10-01, Colombia

- Por solicitud del director se fija [protocolo v1.1](PROTOCOLO_ETAPA_2_OE1_V1_1.md), separado del v1.0 histórico. Tamaño fijo: 24 millones de pares principales; 55 corridas y 48,7 millones de transportes con controles. No se ejecutó Geant4 ni se enviaron trabajos a SC3.
- Margen operativo ligado al ruido de conteo de la ROI histórica; intervalo conservador al menos 95 % construido con límites binomiales exactos. Escenarios con cero, una y varias discordancias; resultado inconcluso permitido sin ampliación automática.
- Se incorporan manifiesto, calculador, seis pruebas satisfactorias e instrucciones. Almacenamiento mínimo propuesto: 30 GiB con cuota/retención por verificar; preparación y adaptación de scripts a cargo de estudiantes.
- OE1 y P-01…P-04 siguen abiertos. Se separan alcance de una ROI, regeneración de datos y validación física del conjunto.

## Revisión del complemento R2-01 — 2026-10-01, Colombia

- Revisión local de entrega `a4d7b79`, ejecutada por los estudiantes en SC3 el 30 de septiembre. Comparador `0d97beb` reproducido y auditoría propia: 103/103 controles satisfactorios.
- B asigna el solape al cuerpo denso en 36/36 pares; A lo asigna al conducto en los 18 casos dirigidos desde ese lado. Tres pares cambian de píxel; ninguno cambia su detección.
- Se conserva la limitación del lado inferido en B y de la fuente dirigida; no se estima la frecuencia en la campaña. P-01…P-04 siguen abiertos. Siguiente paso: dimensionar etapa 2 y resolver almacenamiento, sin aprobar ni lanzar todavía una campaña.
- [Revisión, evidencia y comandos](REVISION_COMPLEMENTO_R2_01_2026-10-01.md).

## Preparación local del complemento R2-01 — 2026-09-30, Colombia

- Por solicitud del director se prepara localmente el [complemento R2-01](COMPLEMENTO_R2_01.md), sin transporte Geant4.
- Se definen 12 trayectorias y tres semillas por variante: 72 transportes técnicos, separados de la fuente representativa.
- En desarrollo, una primera propuesta no retroproyectaba al panel físico de 1,2 m; el validador la rechazó. Se corrigieron las direcciones antes de congelar la lista. El intento descartado permanece en tmp, fuera de la entrega.
- Lista final: validador de estudiantes OK, 108 rectas de sensibilidad mantienen la entrada, 12 cruces profundos contrastados con su referencia; discrepancia máxima de longitud 9,8 × 10⁻¹² m.
- Se comprueba sintaxis Bash del ejecutor; su funcionamiento Geant4/SLURM está pendiente en SC3. Se conserva el alcance de R2-01 y P-01…P-04.

## Revisión independiente de etapa 1 — 2026-09-30, Colombia

- Responsable de transporte: Daniel y Reinaldo en SC3. Revisión: análisis local independiente, sin nueva ejecución Geant4.
- Entradas: entrega `3a49770`, código `3315f82`, paquete Drive con TAR y seis listas de primarios.
- Procedimiento y comandos: [revisión de etapa 1](REVISION_ETAPA_1_2026-09-30.md), sección 6. Entorno: Python 3.12.14, NumPy 2.4.4, pandas 3.0.6.
- Resultado: 405 comprobaciones del análisis reproducidas y 156 controles propios sin fallos; 600.000 pares verificados, repetición A/A idéntica y 13 histogramas reconstruidos.
- Limitación: un cruce en producción; los 20 cruces sintéticos también entran desde el elipsoide. R2-01 requiere complemento antes de ampliar. P-01…P-04 permanecen abiertos.
- Evidencia: `evidencias/revision-etapa1-3a49770.json` y `evidencias/reproduccion-etapa1-3a49770.json`. Se conserva el fallo de descarga inicial del conector: tiempo agotado; descarga directa y huellas posteriores correctas.

## Diseño aportado por la revisión — 2026-09-29, Colombia

- Por solicitud del director se define el protocolo del segundo ensayo v1.0; sustituye pedir a los estudiantes un diseño desde cero.
- Etapa 1: dos geometrías, una vista, tres réplicas A/B y repetición técnica A/A; 13 corridas de 100.000 primarios, con trazabilidad individual.
- Se fijan observable, archivos y controles; el margen físico, la incertidumbre y el tamaño de etapa 2 se decidirán tras revisar etapa 1. No se ejecutó ni se autoriza por este registro una campaña completa.

## Ampliación de controles independientes — 2026-09-29, Colombia

- Cuadratura de las cuatro intersecciones conocidas: geo-test-01, geo-train-06, geo-train-08 y geo-train-11.
- Las cuatro estimaciones son compatibles con los valores y errores estándar entregados (discrepancia máxima 1,13 EE). Dos tolerancias del integrador difieren menos de 0,023 m³ en cada caso.
- Evidencia: `evidencias/intersecciones-independientes.json`; interpretación en `CONTROL_FISICO_LOCAL.md`. No se modifica el encargo de los estudiantes ni se ejecuta transporte Geant4.

## Control geométrico independiente — 2026-09-29, Colombia

- Se integró el volumen común conducto/elipsoide de geo-train-06 mediante cuadratura, con dos tolerancias. Resultado: 83.663,703 m³, compatible con la estimación entregada.
- Se contrastaron volumen restante y cuerpo denso; se documentó la diferencia de densidad del aire entre modelos, conservando la coincidencia de clase de material.
- Evidencia y límites en `CONTROL_FISICO_LOCAL.md`; no se ejecutó Geant4 ni se cambió el encargo vigente.

## Primera entrega revisada y solicitud de diseño — 2026-09-29, Colombia

- Fuente: rama `oe1/geo-train-06-piloto`, revisión `712c78664074732a612b47a8fa4a7fe45f8c4746`.
- Evidencia de recálculo incorporada: `evidencias/revision-entrega-712c786.json`. Coinciden 120 huellas, histogramas/metadatos de piloto y reproducción de una vista histórica. No se ejecutó Geant4 localmente.
- Se publica revisión con observaciones O-01…O-05; no se declara cerrado el OE1 ni se fusiona la rama de resultados.
- Encargo: propuesta del siguiente ensayo, con observable, correspondencia de primarios, incertidumbre, control y presupuesto, antes de nuevas corridas de producción.

## Revisión técnica y encargo SC3 — 2026-09-28, Colombia

- Entrada: mismo catálogo y datos incorporados; no se consultó una nueva entrega de estudiantes.
- Se examinó la construcción de sólidos, la asignación del campo analítico y el submuestreo binomial.
- Procedimiento: `python herramientas/auditar_oe1.py`; evidencia en `evidencias/auditoria-oe1.json`, con fecha UTC y versiones.
- Se probaron puntos interiores a anomalías superpuestas y cotas geométricas. Se reprodujeron los 9.120 pares en memoria sin cambiar las fuentes.
- Durante el desarrollo del auditor se corrigió una expectativa inicial de dimensiones 64×64: la cabecera y los datos especifican 256×256. El resultado final utiliza ese contrato y no atribuye ese error del auditor a los estudiantes.
- Se preparó un piloto original/corregido para geo-train-06 vista 0 y tres semillas, más plantilla de resultados. Geant4 no se ejecutó localmente.
- Pendientes: ejecución y justificación física por estudiantes; P-01/P-02/P-03/P-04 siguen abiertos.
- Verificación final: 567/567 archivos recibidos conservan sus huellas; auditor de pares sin errores; tres pruebas de herramientas aprobadas (intersección/separación, salida del cono y comparador con rechazo de presupuesto inconsistente); sintaxis Bash del ejecutor y enlaces Markdown comprobados. No se probó envío real de trabajos SLURM ni compilación del esquema C++.

## Incorporación inicial — registro UTC 2026-09-29T03:08:48.514624+00:00

- Solicitud: organizar una réplica local documentada usando únicamente material relacionado con OE1.
- Entrada: revisión `b88fa576494cb8a664c46b8c94c5918c5097d616` y paquete compartido ya descargado y auditado.
- Actividad: selección de fuentes, datos, figuras y logs; conservación de bytes y rutas; inventario SHA-256; creación de documentación y verificador.
- Evidencia previa incorporada: comprobación de 114 vistas y registro de advertencias de simulación. Estos análisis preceden a esta organización y no representan una nueva ejecución Geant4.
- Evidencia de esta incorporación: [verificación local](evidencias/verificacion-local.json), generada por la herramienta de integridad.
- Resultado científico: generación respaldada; validación física pendiente según [matriz](MATRIZ_CUMPLIMIENTO.md).
- Siguiente paso de investigación: cerrar P-01/P-02 con un procedimiento controlado antes de atribuir validez física completa a la campaña.

La [bitácora de autores](originales/bitacora-simulacion.md) se mantiene independiente y sin cambios.

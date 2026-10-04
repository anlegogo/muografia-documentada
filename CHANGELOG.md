# Registro de cambios

## 2026-10-03 — Implementación y verificación CPU de C0/C1

- Por autorización de la dirección se implementó el diseño de continuación cGAN, conservando generador/crítico iniciales, cinco actualizaciones D por G, dos optimizadores nuevos y pérdida regional solo en G. No se modificó el motor histórico ni el ajuste U-Net.
- Diecinueve controles satisfactorios; cuatro ejecuciones completas verifican recuperación exacta de G, D, ambos Adam, todos los RNG utilizados, registros y predicciones. Batería definitiva: 16 actualizaciones G/80 D; comprobación preliminar adicional: 2 G/10 D. [Guía](objetivo-2/INSTRUCCIONES_CONTINUACION_CGAN_F05.md) y [evidencia](objetivo-2/evidencias/integracion-cgan-ajuste-v1.json).
- Se verificaron evaluación y figuras técnicas, tabla por anomalía frente a C0 y al modelo inicial, y ruta completa con fixtures del piloto anterior. El resultado técnico no acredita calidad: no se ejecutó el ensayo de cinco épocas.
- Se conservaron el entorno temporal aislado y las fuentes originales verificadas desde objetos Git, corrigiendo diferencias de extracción antes de la batería definitiva. No se reparó el índice Git original ni se abrieron imágenes reservadas.
- CG-01 verificado; CG-02 CPU verificado/GPU pendiente; CG-03 preparado bajo aceptación GPU y resultados pendientes. Próximo paso: estudiantes comprueban CUDA y, si se acepta y hay recursos disponibles, completan C0/C1 y entregan todos los resultados. OE2 continúa abierto.


## 2026-10-03 — Revisión independiente del ajuste a6aa6b8

- Por autorización de la dirección se descargaron doce binarios de Drive y se verificaron tamaños/huellas; 137 textos coinciden con el inventario. Se auditaron seis checkpoints y se confirmó recuperación exacta en las cuatro ejecuciones técnicas. [Informe](objetivo-2/REVISION_AJUSTE_A6AA6B8.md).
- Se reprodujeron 720 inferencias CPU, con diferencias máximas de píxel inferiores a 3,83×10^-6. El recálculo de 7.974 valores de evaluación discrepa como máximo 4,45×10^-16. Se verificaron 5.400 errores de cuentas, 168 estadísticas y 21 valores del bootstrap. [Evidencia](objetivo-2/evidencias/revision-ajuste-a6aa6b8.json).
- Resultado: compromiso confirmado. B mejora Q en 15/18 vistas y empeora el error de borde en 18/18; el sesgo medio del cuerpo denso es −70,23 %, frente a −59,96 % inicial. Se generó e inspeccionó una figura de las 18 vistas.
- Incidencias resueltas en la revisión: dispositivo D: con errores, descarga temporal HTTP 403 y diferencias de representación textual; se trabajó en carpeta temporal C:, descarga pública por IDs y comparación de huellas. Las máscaras coinciden en contenido aunque sus NPZ comprimidos difieren. Una copia cGAN incompleta se descartó; se verificó la copia confirmada con generador y crítico.
- Ajuste-02 y la ejecución/evaluación de Ajuste-03 verificados; aceptación física y OE2 pendientes. Se documenta la [propuesta C0/C1 para cGAN](objetivo-2/PROPUESTA_CONTINUACION_CGAN_F05.md), sin presentarla como lista para GPU. Próximo paso: integrar y verificar ese ejecutor antes de delegar entrenamiento.
- No se entrenó, no se fusionó la rama estudiantil ni se abrieron imágenes reservadas. Se mantiene el cierre del OE1.


## 2026-10-03 — Integración y recuperación del ajuste A/B

- Por autorización de la dirección se completaron lector, máscaras train/val, ejecutor, recuperación, auditor GPU, evaluación regional y figuras. Se conservan el diseño científico, el código histórico y las entregas estudiantiles. [Guía vigente](objetivo-2/INSTRUCCIONES_AJUSTE_CUENTAS_F05.md).
- Se verificaron 90 mapas, 30 archivos de datos/metadatos y conservación de las 78 máscaras regionales val previas. Trece controles funcionales, nueve de pérdida y ocho geométricos satisfactorios. Las cuatro ejecuciones técnicas de red completa reproducen exactamente estados y predicciones al recuperar; 16 actualizaciones de la batería y cuatro preliminares. [Evidencia consolidada](objetivo-2/evidencias/integracion-ajuste-v1.json).
- La regresión del evaluador usa 720 predicciones anteriores: diferencia cero en 468 valores regionales y reproducción de 24 contrastes. No son resultados de un nuevo piloto. Se generaron figuras técnicas y se inspeccionó su presentación.
- Incidencias: índice Git original ilegible, dependencias de Adam ausentes y betas con tipos mixtos. Se utilizó copia aislada, dependencias locales y conversión explícita a flotantes; la batería definitiva pasó. No se reparó el índice original.
- Ajuste-01 verificado; Ajuste-02 CPU verificado/GPU pendiente; Ajuste-03 pendiente. No se ejecutó piloto de cinco épocas ni se abrieron imágenes test/generalization. Próximo paso: comprobar CUDA y ejecutar A/B con aceptación técnica; no se declara mejora física ni cierre del OE2.


## Diseño del ajuste de cuentas OE2 — 2026-10-03

- Comparación acotada A/B: mismo checkpoint U-Net inicial, cinco épocas adicionales por rama y selección fija de la época final. [Diseño](objetivo-2/DISENO_AJUSTE_CUENTAS_F05.md).
- Componente regional estable mediante logsumexp, ponderación por familias y nueve comprobaciones matemáticas. Retropropagación finita en la U-Net completa con dos pares train; pesos sin modificaciones.
- Especificaciones marcadas como diseño no ejecutable en GPU: integración y prueba de recuperación pendientes. No se entrena, no se cambia el motor v1 y no se abre test/generalization.

## Evaluación geométrica del piloto OE2 — 2026-10-03

- Regiones derivadas del cono y anomalías para las 18 vistas de validación; 234 registros región/método y 24 contrastes con controles geométricos. [Informe](objetivo-2/EVALUACION_GEOMETRICA_PILOTO_F05.md).
- Ocho pruebas analíticas y contraste de 2.304 rayos por integración independiente. Identidades de datos, geometrías y máscaras registradas.
- U-Net presenta menor error absoluto, con subestimación regional de cuentas; cGAN reduce algunos sesgos de roca y anomalías, pero sobreestima más cielo. No se declara aceptación física ni se amplía entrenamiento.

## Pesos e inferencia del piloto OE2 — 2026-10-03

- Dos mejores checkpoints descargados y verificados; 720 predicciones reproducidas sobre 360 pares val por modelo, dentro de tolerancia CPU/GPU. [Informe](objetivo-2/REVISION_PESOS_PILOTO_F05.md).
- Exploración de 18 vistas y cuatro bandas de elevación: U-Net supera a cGAN en SSIM/PSNR; quedan sesgos de cuentas y evaluación física pendiente. La zona candidata mantiene contraste positivo en U-Net de época 5, matizando la alerta visual anterior.
- Se publican procedimientos y evidencia JSON, sin pesos ni predicciones voluminosas. No se abre test/generalization, no se entrena ni se fusiona la rama estudiantil.

## Revisión de entrega OE2 c054225 — 2026-10-03

- 110 huellas Git verificadas, cuatro configuraciones y registros contrastados, baseline de 360 pares recalculado y estadísticas CSV reproducidas. [Revisión](objetivo-2/REVISION_PILOTO_C054225.md).
- Ejecución GPU documentada en RunPod; no constituye prueba de SC3. Ambos modelos mejoran la entrada; U-Net supera a cGAN en SSIM/PSNR para esta semilla.
- Se registran pesos aún sin enlace, posibles artefactos, alcance limitado del bootstrap por referencia y próximos controles antes de ampliar. No se fusiona la rama estudiantil.

## Diseño del piloto OE2 al 5 % — 2026-10-03

- Protocolo con prueba técnica de dos épocas y piloto U-Net/cGAN de hasta 30 épocas; mismos pares, semilla y lote, con baseline de entrada y conjuntos reservados protegidos.
- Cuatro configuraciones, ejecutor con verificación CUDA, interrupción/reanudación, registros de memoria/tiempo y resumen automático. [Instrucciones SC3](objetivo-2/INSTRUCCIONES_PILOTO_SC3.md).
- Verificación local de ambos métodos y sus reanudaciones en CPU. GPU, valoración de calidad y campaña principal permanecen pendientes; no se lanzan los 24 entrenamientos.

## Correcciones de implementación OE2 v1 — 2026-10-03

- P01–P03 corregidos: GP del promedio por muestra, normalización disponible sin referencia y manifiesto fijado con rechazo de reanudación incompatible. Se conserva código original y procedencia.
- 17 controles satisfactorios, doce casos analíticos de GP y entrenamiento de la arquitectura completa con reanudación idéntica a ejecución continua en CPU. [Detalle y reproducción](objetivo-2/CORRECCIONES_V1.md).
- P04 permanece pendiente; no se evalúa calidad final ni se ejecuta campaña en SC3. El convertidor histórico no fue recuperado; se comprueba directamente igualdad de sus salidas train/val con los paquetes fuente.

## Revisión inicial del OE2 — 2026-10-03

- Ampliación expresamente autorizada a revisión del OE2; se mantiene el cierre del OE1.
- [Diagnóstico de implementación](objetivo-2/README.md): arquitectura reutilizable, compatibilidad de 7.200 pares y prueba de paso por generador/crítico; sin entrenamiento ni acceso a imágenes reservadas.
- Se reproducen la discrepancia entre suma/promedio en GP y la dependencia de normalización respecto de la referencia. Se documentan cuatro pendientes con criterios de cierre, script reproducible, entorno y evidencia numérica.

## Cierre del OE1 por decisión de la dirección — 2026-10-03

- Objetivo aprobado contrastado con el plan, 19 huellas de geometría verificadas y justificación de representatividad completada. Se corrige la identificación del caso homogéneo: geo-train-01; geo-gen-01 contiene anomalías.
- Informe de cierre con ecuaciones, tres figuras integradas y conclusión de cumplimiento. PDF de 15 páginas, fuente editable y evidencia del plan/catálogo. [Informe](objetivo-1/manuscrito/README.md).
- P-01 a P-05 resueltos dentro del alcance idealizado; A-01 a A-08 consolidados y decisión expresa de cierre registrada. Se conservan siete excepciones de conteo y límites físicos. No se solicita nueva campaña ni se declara aprobada la tesis completa. [Registro de cierre](objetivo-1/CIERRE_OE1.md).
- 18 controles numéricos/editoriales repetidos, compilación local sin referencias indefinidas ni desbordes y revisión visual del documento. Datos y rama estudiantil sin cambios.

## Borrador académico del OE1 — 2026-10-03

- Texto descriptivo e impersonal de 11 páginas en PDF y LaTeX: nomenclatura, metodología, adelgazamiento y dependencia, contraste de bordes, resultados, discusión y conclusión acotada. [Documento](objetivo-1/manuscrito/README.md).
- 18 controles numéricos/editoriales satisfactorios; cifras, siete excepciones y coordenadas contrastadas con la evidencia. Compilación local y revisión visual de todas las páginas; el compilador integrado presentó un fallo de entorno.
- P-04 continúa pendiente de valoración e incorporación al manuscrito estudiantil. Se corrigió en la ficha una frase desactualizada sobre la integridad de dataset-v2, ya comprobada en Drive; no se amplía el alcance a entrenamiento.

## Recuperación independiente de Drive — 2026-10-03

- Descarga completa de 753 archivos (1.126.769.406 bytes); 2.291 controles satisfactorios. Coinciden las 477 huellas de fusión/imágenes, los 342 arreglos de pares y los inventarios de distribución.
- P-05 resuelto. En dataset-v2 se comprobó integridad y contenido, sin auditar la conversión ni evaluar redes. [Revisión y evidencia](objetivo-1/REVISION_DISTRIBUCION_DRIVE.md).
- Contrastada la entrega estudiantil cb57145/8fa667c. Se preparó una lista de incorporación al manuscrito; P-04 permanece abierto porque no se recibió una versión redactada y actualizada.

## Cuatro entregables de cierre documental — 2026-10-03

- Ficha final del conjunto y síntesis académica con límites explícitos. Tres figuras científicas en PNG/PDF, generadas desde histogramas y pares verificados.
- README, índice, matriz, pendientes y criterios A-01 a A-08 consolidados; retirados avisos ya superados. Conservada la cronología en Git y bitácora.
- 114 métricas de vista coinciden con la evaluación, 96 enlaces locales comprobados y figuras inspeccionadas. Drive permanece fuera de estos cuatro puntos. [Ficha](objetivo-1/FICHA_CONJUNTO_OE1.md) · [Síntesis y figuras](objetivo-1/SINTESIS_RESULTADOS_OE1.md).

## Revisión directa f395570 — 2026-10-03

- 477 huellas y 114 matrices verificadas; evaluación completa reproducida desde píxeles.
- 9.120 pares regenerados en memoria y 342 huellas de contenido coincidentes. [Informe](objetivo-1/REVISION_DATOS_F395570.md). Drive localizado, sin descarga ni auditoría de dataset-v2.

## Revisión de campaña e037d09 — 2026-10-03

- Registros de 1.026 filas completadas verificados; 25 archivos íntegros, 1.710 intervalos recalculados y 107 pruebas de la rama satisfactorias.
- Siete vistas bajo la meta descriptiva conservadas según acuerdo. Se solicitan matrices ya generadas para revisión directa; no se propone otra campaña. [Informe](objetivo-1/REVISION_CAMPANA_E037D09.md).

## Preparación completa de campaña — 2026-10-02

- Siete actividades completadas: criterios explícitos, análisis de incertidumbre, comparación geométrica, evaluador de 114 vistas, manifiesto candidato, 480 pares y guía SC3.
- 106 pruebas satisfactorias. Se mantiene 344 M como candidato, sin garantía de suficiencia ni orden de transporte. [Entrega](objetivo-1/PREPARACION_CAMPANA_114.md).

## Histogramas del piloto revisados — 2026-10-02

- Se verificaron 27 huellas, seis imágenes y la evaluación completa desde los CSV de `ccbdce0`. Se confirma el resultado del piloto y se precisa la proyección a 344 M; no se habilita producción.
- [Revisión](objetivo-1/REVISION_HISTOGRAMAS_PILOTO_CCBDCE0.md) y evidencia local registradas sin modificar la entrega estudiantil.

## Adopción del alcance idealizado — 2026-10-02

- Alcance idealizado del OE1 adoptado expresamente por la dirección; equivalencia instrumental y C3 quedan como extensión opcional.
- Definición, criterios de cierre, ficha, pendientes y guía actualizados. La decisión no aprueba la receta física, el presupuesto del piloto ni la campaña.

## Unificación del estilo documental — 2026-10-02

- Redacción propia ajustada a estilo académico impersonal y tercera persona, conforme al criterio indicado por la dirección.
- Regla editorial registrada en `AGENTS.md` y `docs/DOCUMENTACION.md`. Se conservan resultados, comandos, atribuciones y documentos originales recibidos.

## Siete actividades locales completadas — 2026-10-02

- Referencia ideal de cielo, análisis de bordes y diseño C3 con incertidumbre simultánea; piloto condicional con máscaras, semillas y presupuesto.
- Worker y lanzador preparados con integridad, publicación verificada e intenciones persistentes; normalización convencional validada y agregada en nuevos bloques.
- 103 pruebas satisfactorias; fusión de datos SC3 reales reproduce las huellas previas. Definición del producto y guía única de estudiantes documentadas. Sin nuevas corridas ni autorización de campaña.

## Revisión de entrega 01a9871 — 2026-10-02

- Prueba técnica de dos bloques en SC3 respaldada; fusión reproducida con hashes idénticos y 113 valores del nuevo análisis contrastados.
- Corrección de T-01: 204 huellas coinciden con los objetos Git originales; la discrepancia era de la copia extraída.
- Se documentan ajustes de referencia de cielo y dimensionamiento/alcance de C3 antes de nuevas corridas. Rama estudiantil sin fusionar; sin cambios al simulador.

## Publicación verificada de bloques — 2026-10-02

- Nueva herramienta de publicación: valida, copia a temporal, verifica todos los bytes y promueve con bloqueo; no sobrescribe resultados distintos y reconoce repeticiones idénticas.
- Fallos controlados de copia, corrupción, escritura de recibo y promoción no publican un bloque. Suite: 78 pruebas satisfactorias. Dos bloques reales publicados localmente y verificados sin alterar entradas ni ejecutar transporte.
- [Uso, adopción y límites](objetivo-1/PUBLICACION_VERIFICADA_BLOQUES.md). Falta integrar y comprobar el flujo en SC3; la validación física permanece abierta.

## Preparación local integral — 2026-10-02

- Probabilidades del algoritmo de fuente calculadas desde las tablas v1: ventana nominal 0,6841465610; 20,18 % de masa en filas extrapoladas. Concordancia con la fracción observada de c02; no valida físicamente la extrapolación.
- Preflight offline de manifiestos k=1/k=10: 114 vistas, 228/1.596 bloques, sin duplicados ni huecos. Integra validación estricta de bloques; no consulta colas ni envía trabajos.
- Ficha de definición candidata y [balance único de resultados y dependencias](objetivo-1/BALANCE_PREPARACION_LOCAL.md). 69 pruebas locales satisfactorias; conserva sin cambios la definición física, los originales, las ramas de estudiantes y la operación de SC3.

## Diagnóstico del observable con datos conservados — 2026-10-02

- Comparados panel de 1,2 m y planos de 100/600 m para los mismos primarios con E > 3 GeV. En bandas de roca, la contención 100/600 cercana a uno no implica contención en el panel. No se interpreta como eficiencia física ni factor correctivo.
- Reanalizados bordes con corte: máximos descriptivos 1,64 pp (sin margen, 20M) y 2,84 pp (5°, 2M). No son comparación pareada ni decisión estadística; no se atribuye empeoramiento al margen.
- [Definiciones pendientes, criterios y reproducción](objetivo-1/DIAGNOSTICO_OBSERVABLE_Y_DECISION.md). 60 pruebas locales satisfactorias; no se ejecutan transportes nuevos ni se cambian normalización o alcance físico.

## Correcciones locales de fusión y configuración — 2026-10-02

- Nueva fusión estricta, con rechazo de bloques/semillas repetidos o contradictorios, agregados corregidos y verificación SHA exacta o conversión CRLF->LF explícita y trazable. Preserva entradas.
- Empaquetador actualizado para distinguir inyección, margen, plano, selección energética y definiciones de fuente/normalización. Se protege la conservación de bytes de futuras entregas SC3.
- 56 pruebas locales satisfactorias. Dos bloques reales: 200.000 primarios, 69.995 registros seleccionados y 130.190 sin corte; matriz conservada, exportación y lectura satisfactorias.
- [Instrucciones de adopción y límites](objetivo-1/CORRECCIONES_LOCALES_FUSION_CONFIGURACION.md). Rama estudiantil intacta; no se actualizan SC3 ni su lanzador y no se autoriza campaña física.

## Revisión de justificación física y producción — 2026-10-02

- Revisada la entrega f9a77ef sin fusionar su rama. Se ejecutan seis análisis y coinciden 3.045 valores numéricos; 114 histogramas históricos reconstruidos coinciden con el manifiesto.
- Se verifican 19 corridas (92 millones de primarios) y la fusión de integración de 200.000 primarios/69.995 registros, tras normalización de líneas en copia temporal. 181/200 huellas de controles requieren esa normalización.
- Se documentan límites de C1/C2/C3/C5, C4 aún no cumplido, metadatos agregados incorrectos y aceptación de semillas contradictorias/bloques repetidos. La firma de empaquetado también requiere reconocer las opciones nuevas.
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

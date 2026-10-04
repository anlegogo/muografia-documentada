# Bitácora del OE2

## Calidad comparable y continuidad OE2–OE3 — 2026-10-04, Colombia

- Actividad de revisión de la dirección: contraste de la síntesis C2 y curvas existentes, leídas desde 166be6ff09b60341fde084d433266b94b6e832cc; no se entrenó, infirió ni simuló.
- Se verificaron las ocho desigualdades SSIM/PSNR de cGAN al 5 % frente a entrada al 10 % en cuatro geometrías y se añadió la tabla correspondiente al balance OE2.
- Resultado: mejora descriptiva frente al doble de conteos; no equivalencia con la referencia completa ni factor físico aceptado. La calidad comparable conserva alcance parcial.
- Se documentó la ruta OE3-P02 a P04: criterio de calidad, desglose por vista/región, comparación de fracciones y redacción. Las tareas adicionales siguen pendientes; no se requiere otra GPU para la síntesis.

[Precisión del balance](CIERRE_OE2.md#precisión-sobre-calidad-comparable-y-continuidad-al-oe3).

## Síntesis académica y cierre documental OE2 — 2026-10-04, Colombia

- Se redactan método, resultados, discusión y conclusión delimitada con la evidencia C2 existente; no hay nuevo entrenamiento ni simulación.
- Se generan e inspeccionan dos figuras desde matrices auditadas, con selección explícita y todas las continuaciones. Se añaden 18 resúmenes y 36 filas por geometría, su CSV y procedencia.
- EF-04 queda preparado como producto documental. La calidad comparable permanece parcial; integración editorial OE2-D01 pendiente. No se adopta el umbral SSIM histórico retirado ni se declara equivalencia física.

[Informe](manuscrito/INFORME_OE2.md) · [matriz](MATRIZ_CUMPLIMIENTO.md).

## Evaluación final y corrección C2 — 2026-10-04, Colombia

- Actividad de la dirección: auditoría de la entrega estudiantil 4e5945e, conservada sin modificar; no hubo nuevo entrenamiento.
- Se verificaron 32 matrices (1.006.637.056 bytes), 50 recibos/manifiestos frente a Git y ocho archivos de referencias. Se reprodujeron 4.320 filas de imagen y 1.134 regionales; muestra CPU/GPU de 32 inferencias consistente.
- Se identificó inestabilidad numérica en controles de contraste. C2 conserva el protocolo original, introduce desempate geométrico explícito y publica índices completos: cuatro pruebas, 162 comprobaciones de sensibilidad y reproducción exacta desde registro.
- Se conserva comparación antes/después: ocho contrastes de referencia cambian y un control puntual B1/generalización pasa a favorable; las doce clasificaciones globales mantienen el compromiso. No se afirma equivalencia física ni 20× demostrado.
- EF-02 y EF-03 verificados en el alcance indicado; EF-C2 verificado; EF-04 y OE2-P04 parciales por alcance académico/científico. Sigue incorporación al manuscrito y confirmación del OE3; no se pide otra corrida GPU.

- [Revisión C2](REVISION_EVALUACION_FINAL_C2.md).

## Preparación de evaluación final OE2 — 2026-10-04, Colombia

- Por solicitud de la dirección, se sustituye la consolidación E1 como requisito bloqueante por inferencia final al 5 % con ocho redes existentes. No hay nuevo entrenamiento.
- Se fijan ocho pesos, cuatro geometrías reservadas y sus ocho archivos de distribución; 480 imágenes por red, 3.840 predicciones. Protocolo y fuentes se registran antes de desempeño reservado.
- Verificación local: cinco pruebas de contratos, siete controles de flujo sintético, ocho pesos/32 inferencias de validación y 441 campos de métricas contrastados. No se calcularon resultados reservados localmente.
- Se corrigió una aserción de igualdad decimal en la prueba sintética (0,1 frente a su representación binaria); el ejecutor no se modificó para cambiar ese resultado. Se representa PSNR infinito explícitamente en casos perfectos.
- EF-01 preparado; EF-02/03 pendientes de ejecución y auditoría. OE2-P04 sigue parcial; no se afirma equivalencia física ni desempeño en otras fracciones.
- [Protocolo](PROTOCOLO_EVALUACION_FINAL_OE2.md) y [tarea delegada](INSTRUCCIONES_EVALUACION_FINAL_OE2.md).

## Revisión y diagnóstico interior de E1 — 2026-10-04, Colombia

- Actividad: auditoría independiente de la entrega estudiantil 804ce85 y diagnóstico local de predicciones, sin nuevo entrenamiento.
- Evidencia: 55 binarios, 18 checkpoints, recuperación exacta B1–B3, 2.520 inferencias; 252 sesgos regionales y mapas de las seis vistas de geometría 1 por pareja.
- Resultado: borde mejor en las 54 comparaciones; exceso interior persistente. E1-04/E1-05 verificados; criterio de nueve controles no satisfecho. Sin aceptación física ni apertura de reservas; OE2-P04 permanece parcial.
- Se registra fe de erratas de tamaño/rutas sin alterar originales y se deja borrador de discusión.
- Siguiente paso delegado: reproducción CPU y consolidación documental, sin otro entrenamiento GPU. [Revisión](REVISION_E1_804CE85.md) e [instrucciones](INSTRUCCIONES_CIERRE_E1.md).

## 2026-10-04 — Integración y comprobación local del ensayo E1

- Actividad autorizada: completar la preparación local y dejar instrucciones autónomas para los estudiantes. Base: bc6ce8f; checkpoint original cGAN de época 5, datos y máscaras verificados.
- Coeficiente: regla de presupuesto de gradiente registrada antes de perfilar doce lotes train; resultado 0,629. Ningún peso se modificó durante el perfil y no se usó val para elegirlo.
- Procedimiento: integración separada, controles de contratos, orquestación y equivalencia; doce ejecuciones CPU completas con interrupción y recuperación; comparación de estados, evaluación técnica, síntesis e inventario. Soporte del borde verificado en las 90 vistas train/val.
- Evidencia y comandos: [diseño](DISENO_BORDE_CGAN.md), [guía](INSTRUCCIONES_BORDE_CGAN.md) y JSON enlazados. Se preservan las entregas históricas.
- Resultado: E1-03 y E1-04 verificados en alcance local; ejecución técnica no equivale a aceptación de calidad. Cero pilotos de cinco épocas y cero ejecuciones CUDA en esta preparación.
- Incidencias resueltas: lectura UTF-8 del generador local de archivos; creación explícita de la carpeta del orquestador en el control con procesos simulados. La evidencia registra los controles finales.
- Siguiente paso: E1-05, prueba técnica en GPU y, solo después de aceptación de las tres parejas, seis continuaciones, evaluación común y entrega íntegra. OE2 y aceptación física pendientes.

## 2026-10-04 — Diagnóstico espacial y preparación E1

- Fecha y zona horaria: 2026-10-04, America/Bogota.
- Actividad autorizada por la dirección: avance local sobre los pendientes de la revisión; diagnóstico, componente experimental y comprobación de gradientes, sin entrenamiento.
- Entradas: main 866e286, entrega f6518ff auditada, seis predicciones finales, referencias/máscaras verificadas y checkpoint original de época 5.
- Procedimiento: descomposición de errores regionales, reproducción del error de borde, contraejemplo con la función original, nueve pruebas analíticas y cuatro cálculos de gradientes sobre train en modo evaluación.
- Evidencia: [diagnóstico y comandos](DIAGNOSTICO_ESPACIAL_CGAN.md), tabla completa, JSON de diagnóstico, comprobaciones y sondeo.
- Resultado: el error del total mejora, pero el espacial empeora en las tres parejas. El candidato detecta redistribuciones invisibles al total y sus gradientes son finitos; una muestra presenta oposición local al gradiente base. Cero pasos de optimizador, estados G/D idénticos y reservas sin abrir.
- Limitaciones: diagnóstico posterior al ensayo, sin identificación causal completa ni validación de calidad del nuevo componente. Cuatro muestras individuales no sustituyen el entrenamiento ni permiten fijar un coeficiente óptimo. No se observaron fallos de ejecución.
- Pendientes: E1-03, fijación prospectiva del coeficiente/diseño mediante train; E1-04, integración y recuperación CPU; E1-05, nueva aceptación GPU antes del ensayo. OE2 y aceptación física pendientes.

## 2026-10-04 — Revisión binaria y numérica de la repetición R1–R3

- Actividad: auditoría independiente de la entrega f6518ff y de los archivos compartidos en Drive, sin entrenamiento nuevo.
- Entradas: 55 binarios (5.910.526.686 bytes), 193 textos fijados por objeto Git, checkpoint inicial y caché de máscaras previamente verificados. Se recuperaron 30 archivos train/val por errores de lectura de la copia antigua; sus huellas coinciden con el contrato.
- Verificación: igualdad exacta de las tres recuperaciones técnicas; seis continuaciones completas; evaluación regional, diagnóstico por anomalía, síntesis e inferencia CPU de 2.520 imágenes. El modelo inicial se infiere una vez y se contrasta con sus tres exportaciones.
- Resultado: ninguna pareja cumple los ocho controles. C1 reduce Q en R1 y R2, lo aumenta en R3 y empeora el borde en las tres. La clasificación es dependencia de la semilla o compromiso.
- Evidencia y reproducción: [informe independiente](REVISION_REPETICION_F6518FF.md), [evidencia JSON](evidencias/revision-repeticion-f6518ff.json) y herramientas enlazadas en el informe.
- Límites: revisión local CPU de artefactos producidos en L40S; sin nueva ejecución CUDA, sin entrenamiento desde cero y sin apertura de test/generalization. La aceptación física y el OE2 permanecen pendientes.
- Siguiente paso: revisar la hipótesis de ajuste y justificar criterios físicos prospectivos antes de solicitar entrenamiento adicional; no repetir selectivamente semillas ni ampliar automáticamente la campaña.

## 2026-10-04 — Repetición cGAN integrada y comprobada localmente

- Fecha y zona: 2026-10-04, America/Bogota. Actividad autorizada por la dirección: adaptar y verificar el diseño de tres parejas; sin lanzamiento GPU.
- Entradas: main 2468ae8, checkpoint original cGAN de época 5, distribución y caché de máscaras ya verificadas. Se conservan las tres semillas fijadas antes de ejecutar.
- Procedimiento: selección versionada de pareja en ejecutor/revisor/evaluador; controles de contratos y gradientes; doce ejecuciones de las redes completas en CPU, continuas y recuperadas; evaluaciones de las tres parejas y síntesis.
- Evidencia: [integración-repetición-v1](evidencias/integracion-repeticion-cgan-v1.json), 50 controles satisfactorios, recuperación exacta en las tres parejas, 48 G/240 D. Se rechazan mezcla de parejas, corrupción de estados y aceptación CPU para piloto GPU. La exportación se recupera sin reentrenar.
- Entorno: copia temporal aislada y dependencias locales de PyTorch, sin reparación del índice Git original. Una lectura del comprobador de publicación requirió explicitar UTF-8 en Windows; se corrigió y la comprobación posterior pasó, sin modificar las fuentes de entrenamiento. Los comandos Python se comprobaron localmente; Bash/CUDA quedan para el equipo GPU. Los resultados técnicos de ocho muestras no acreditan calidad.
- Siguiente paso: [guía completa para los estudiantes](INSTRUCCIONES_REPETICION_CGAN_F05.md), con tres aceptaciones GPU obligatorias, seis continuaciones, tablas por vista/anomalía y síntesis. La aceptación física y el OE2 siguen pendientes; no se abrieron test/generalization ni se contactó a estudiantes.

## 2026-10-04 — Valoración por vista y diseño prospectivo

- Actividad autorizada por la dirección: examinar mejoras/deterioros con los datos disponibles, documentar valoración y diseñar repetición. Fecha: 2026-10-04 America/Bogota.
- Entradas: evaluación CG-04c y predicciones iniciales verificadas. Se recalculó su detalle mediante analyze_predictions y se agregaron las 18 vistas, 24 anomalías y 23 contrastes comunes.
- Evidencia: [valoración](VALORACION_COMPROMISO_CGAN_F05.md), JSON, CSV, figura PNG/PDF inspeccionada y analizador reproducible. Los promedios reconstruyen Q, SSIM, PSNR y cielo/borde con diferencias menores de 1e-12.
- Resultado: mejora agregada C1/C0 con heterogeneidad, deterioro de borde en geo-val-02 y nueve inversiones de signo del contraste medio, varias con referencia cercana a cero. El cuerpo denso de geo-val-03/V1 merece seguimiento explícito. No se modifica la clasificación descriptiva anterior ni se concede aceptación física.
- Decisión: C1 permanece como candidata para estudiar estabilidad de la continuación. Se fijaron tres semillas nuevas y seis continuaciones de cinco épocas, todas desde el mismo checkpoint inicial. Es un diseño condicionado, no una réplica desde cero ni confirmación independiente.
- Límites y siguiente paso: una semilla previa, tres geometrías val observadas; sin nuevas inferencias, entrenamiento ni apertura de particiones reservadas. Adaptar y verificar localmente el ejecutor y sus identidades antes de enviar comandos de ejecución a estudiantes. La especificación permanece ready_for_gpu=false.

## 2026-10-04 — Auditoría de la entrega y binarios CG-04c

- Fecha de revisión: 2026-10-04 America/Bogota; ejecución y publicación estudiantil del 2026-10-04 UTC. Actividad autorizada: verificar los archivos de Drive y la evaluación recibida.
- Entradas: entrega 1ec1c24, 13 binarios, referencias train/val y máscaras verificadas. Fuentes científicas fijadas en 4fc3bd5.
- Procedimiento: tamaños/SHA-256, auditoría restringida de seis checkpoints, igualdad exacta de recuperación, recálculo de 5.334 campos y 1.080 inferencias CPU. [Informe](REVISION_BINARIOS_CG04C.md) y [evidencia](evidencias/revision-binarios-cg04c.json).
- Incidencia: el script local pasó inicialmente índices como tuplas; se corrigió a listas según contrato del evaluador, sin cambiar contenido ni orden. La comparación de máscaras separó huellas de contenedores comprimidos de contenido y metadatos.
- Resultado: CG-02 GPU y CG-03 ejecución/evaluación verificados; CG-04 cerrado en el entorno recibido. Se reproduce mejora descriptiva de C1 frente a C0 con compromisos frente al inicial. La aceptación física permanece pendiente.
- Límites: una semilla, tres geometrías val; no se repitió CUDA localmente ni se abrieron test/generalization. El controlador GPU cambió respecto de CG-04b, por lo que no se atribuye causalidad aislada a la corrección.
- Siguiente decisión: valorar el compromiso físico y fijar repetición/comparación antes de ampliar. No se requieren nuevas corridas para suplir archivos de esta entrega.

## 2026-10-04 — Preparación y validación CPU de CG-04c

- Fecha y zona: 2026-10-04 America/Bogota. Actividad autorizada por la dirección: implementar la corrección propuesta tras revisar CG-04b.
- Entradas: fuentes de 3410c65, checkpoint cGAN verificado, distribución y máscaras train/val conservadas. No se abrieron particiones reservadas.
- Procedimiento: derivación separada W/GP, suma por parámetro y único paso Adam. Siete controles nuevos y ocho del diagnóstico; once de integración y ocho de artefactos. Cuatro ejecuciones técnicas completas en seis procesos CPU, con interrupción tras época 1 y recuperación en proceso nuevo.
- Evidencia: [guía](CORRECCION_GRADIENTES_CG04C.md) y [JSON](evidencias/cg04c-validacion-cpu.json). Los 34 controles pasan; G, D, ambos optimizadores, RNG, historial y predicciones se recuperan exactamente en C0/C1. Total: 16 actualizaciones G y 80 D.
- Incidencias de preparación: intento de construir la guía con un literal JavaScript falló por delimitadores; se guardó mediante parche sin afectar fuentes ni pruebas. La búsqueda amplia de fixtures encontró carpetas de dependencias sin acceso en sandbox; las rutas de los dos fixtures se localizaron y se verificaron en el entorno de pruebas autorizado. No hubo fallos numéricos en la batería definitiva.
- Límites: CPU no acepta GPU; no se ejecutaron las cinco épocas. La suma ordenada es una corrección candidata y no demuestra la causa interna CUDA.
- Próximo paso CG-04: estudiantes ejecutan la prueba técnica L40S con esta versión y salidas nuevas. Tras aceptación exacta y con recursos pueden continuar C0/C1 y evaluar; ante fallo se detienen y conservan evidencia. OE2 continúa abierto.

## 2026-10-04 — Revisión de la entrega CG-04b

- Fecha de revisión: 2026-10-04 America/Bogota; ejecución estudiantil declarada del 2026-10-04 UTC.
- Actividad autorizada: revisar la actualización estudiantil 0f6ec2f y sus archivos Drive.
- Procedimiento: descarga de 22 binarios, verificación SHA-256/tamaños, carga restringida CPU, recálculo con compare_all y contraste de estados e identidades. No se ejecutó CUDA localmente ni entrenamiento.
- Evidencia: [informe](REVISION_BINARIOS_CG04B.md) y [JSON independiente](evidencias/revision-binarios-cg04b.json). Los 580 valores recalculados coinciden; componentes aislados exactos, gradiente conjunto discrepante.
- Incidencia documental: confirmados finales mixtos en la evidencia CG-04; normalizados a LF con igualdad semántica del JSON. Sin cambios en fuentes del entrenamiento.
- Pendiente CG-04: preparar una corrección controlada y validar la recuperación completa en GPU antes de las continuaciones. No se identifica todavía un kernel causal ni se acepta tolerancia numérica.

## 2026-10-03 — Separación de gradientes CG-04b

- Fecha y zona: 2026-10-03 America/Bogota; UTC del 2026-10-04.
- Actividad autorizada por la dirección: preparar la comprobación de las contribuciones al gradiente del crítico tras la auditoría de binarios CG-04.
- Entradas: checkpoint cGAN original y subconjunto técnico train/val. Se conserva semilla, cinco D por G durante la época 1 y penalización 10; test permanece reservado.
- Procedimiento: cinco mediciones independientes por cada condición continua/nueva en C0/C1. El lote de época 2 se deriva sin aplicar pasos de optimización. Se comparan identidad, estado, RNG, forwards, pérdida y gradientes; la suma se calcula offline.
- Evidencia: [guía](DIAGNOSTICO_GRADIENTES_CG04B.md), [validación CPU](evidencias/cg04b-validacion-cpu.json) y pruebas de la herramienta. Veinte procesos CPU y ocho controles funcionales/matemáticos completados.
- Límites: la suma offline no reproduce el orden interno de acumulación CUDA. No se concedió aceptación ni se modificó la tolerancia.
- Pendiente CG-04: ejecutar CG-04b en L40S y revisar los componentes y controles antes de proponer una corrección.

## 2026-10-03 — Auditoría de los binarios CG-04

- Fecha: 2026-10-03 America/Bogota; descarga y revisión en UTC del 2026-10-04.
- Actividad autorizada por la dirección: contraste independiente de binarios, huellas de estados y métricas del diagnóstico estudiantil.
- Entradas: trazas `c45a1a1`, inventario Drive `65ab85c`, 22 binarios y tres shards val verificados; test sin abrir.
- Procedimiento: SHA-256 y tamaños; carga restringida PyTorch en CPU; comparación de redes, Adam y RNG; reconstrucción de referencias y recálculo SSIM/PSNR.
- Evidencia y resultado: [revisión](REVISION_BINARIOS_CG04.md) y [JSON](evidencias/revision-binarios-cg04.json). Los 22 archivos son íntegros y las métricas concuerdan; la discrepancia posterior a reanudar está confirmada.
- Limitaciones y siguiente paso: no se reprodujo CUDA localmente; CG-04 permanece parcial. Aislar las contribuciones al gradiente del crítico antes de proponer corrección o tolerancia.

## 2026-10-03 — Preparación del diagnóstico CG-04

- Fecha y zona horaria: 2026-10-03, America/Bogota. La incidencia estudiantil declara la misma fecha; parte de los registros utiliza UTC del 2026-10-04.
- Actividad autorizada por la dirección: revisión de la entrega `b0ad0b1` y preparación de diagnóstico sin modificar herramientas originales.
- Entradas: código `04b2e46`, checkpoint cGAN original y subconjunto técnico train/val; no se abrió test.
- Procedimiento: procesos independientes continua/repetida/recarga/reanudada; comprobación inmediata de restauración; huellas de forwards, gradientes, pasos Adam y RNG en época 2.
- Evidencia: [guía y criterios](DIAGNOSTICO_RECUPERACION_CGAN.md), [validación CPU](evidencias/diagnostico-recuperacion-cgan-cpu.json), siete pruebas de detección, batería C0/C1 comparada con la ejecución original sin instrumentación.
- Resultado y limitaciones: preparación funcional verificada en CPU; incidencia L40S sin resolver. Las copias y sincronizaciones del diagnóstico pueden cambiar el comportamiento observado. No se acepta la tolerancia propuesta ni se habilita el piloto.
- Pendiente CG-04: ejecutar el diagnóstico GPU, compartir estados binarios y auditar el primer evento diferente.

## 2026-10-03 — Revisión inicial autorizada por la dirección

- Actividad: revisión del código publicado por los estudiantes y diagnóstico local de compatibilidad con dataset-v2. Se conserva la autoría estudiantil de la implementación y simulación; la revisión se incorpora como seguimiento de la dirección.
- Entradas: repositorio original b88fa576494cb8a664c46b8c94c5918c5097d616, contraste de entrenamiento con 3315f82 y distribución Drive de 2026-10-03. Consulta de actualización documental 800ab86 en la rama estudiantil de la réplica, sin fusión.
- Procedimiento: inspección de arquitectura, pérdidas, lector, checkpoints, configuración y registros; ejecución de `herramientas/revisar_base.py` según el comando del [informe](README.md).
- Evidencia: [JSON](evidencias/revision-2026-10-03.json), con huellas y entorno. Comparados 7.200 pares de 90 vistas; forward de generador/crítico satisfactorio; reproducidas dependencia de referencia y discrepancia de GP.
- Incidencias de revisión: primeras consultas de archivos de entrenamiento se hicieron desde la réplica documental y no encontraron esos archivos; se corrigió la ruta al repositorio original. Primera ejecución del diagnóstico falló por exigir igualdad exacta a cero en aritmética float32; se adoptó tolerancia de 1e-8 para GP teóricamente nulo y 1e-5 relativo para su valor analítico. La repetición terminó con código cero. No se modificó la implementación estudiantil para obtener ese resultado.
- Límites: sin entrenamiento, sin inferencia sobre test/generalization, sin validación de GPU ni nueva evaluación de pesos históricos. El cierre del OE1 no cambia.
- Resultado: OE2-P01 a OE2-P04 pendientes, con criterios de cierre y orden propuesto. La siguiente actividad es una corrección versionada y una prueba breve antes de consumir recursos de SC3.

## 2026-10-03 — Corrección autorizada de los tres puntos

- Se creó una implementación derivada de b88fa57, conservando originales y atribución estudiantil. Se corrigieron pérdidas, lector, contrato de normalización y recuperación de checkpoints.
- P01–P03 resueltos para el entrenamiento sobre la distribución fijada; [documentación v1](CORRECCIONES_V1.md) y [evidencia](evidencias/correcciones-v1.json). Preparación: 90 vistas/7.200 pares comparados; escala calculada únicamente con train.
- Primera ejecución: 16 controles satisfactorios. Tras comprobar portabilidad, se fijaron finales LF en manifiesto y fuentes, se normalizaron saltos de línea al identificar código y se añadió una prueba de independencia de la referencia a través del lector. Repetición final: 17 controles satisfactorios, incluida reanudación exacta.
- Incidencias: la consulta adicional al repositorio citado como muography-thesis no pudo ejecutarse mediante gh porque ese ejecutable no está disponible. El convertidor histórico permanece no recuperado; la verificación independiente contra paquetes fuente evita depender de su ejecución para integrar los datos. La ayuda CLI emitió un aviso de caché de fuentes de Matplotlib sin permisos en el perfil de Windows; terminó correctamente y no afectó los controles numéricos.
- Se separó selección del mejor SSIM sin redondear del umbral de paciencia. Los resultados son pruebas técnicas CPU de dos pasos, sin apertura de imágenes reservadas y sin conclusión de calidad.
- Siguiente paso: protocolo OE2-P04 y prueba GPU, antes del entrenamiento prolongado.

## 2026-10-03 — Diseño del piloto OE2-P04

- Autorización de la dirección para preparar protocolo, configuraciones y comandos SC3. Se fijó comparación al 5 % entre U-Net L1 y cWGAN-GP, semilla 2026100301, lote 4 y normalización v1.
- Dos etapas: comprobación técnica de dos épocas con parada/reanudación deliberada, y piloto de hasta 30 épocas con 1.440 pares train/360 val, paciencia 8 y validación por época.
- Se añadieron ejecutor externo y resumen de registros; no se modifica la implementación corregida ni su identidad. Se registra baseline sin red, entorno, memoria CUDA y tiempos.
- Evidencia: [resumen técnico local](evidencias/protocolo-piloto-local.json), [protocolo](PROTOCOLO_PILOTO_F05.md) e [instrucciones](INSTRUCCIONES_PILOTO_SC3.md). Ambos métodos se ejecutan y reanudan en CPU para verificar comandos; esta comprobación no aprueba GPU ni calidad.
- Próximo paso: estudiantes ejecutan A en SC3 y, si pasa, B con autonomía dentro de los límites definidos. Se requiere revisión de resultados antes de ampliar a otras fracciones y repeticiones.
- Resultado local: veinte controles no GPU satisfactorios entre ambos métodos; se comprobó el rechazo de la entrega CPU como aceptación GPU y la coherencia de las cuatro configuraciones. Las dos redes aún empeoran el SSIM de entrada después de cuatro actualizaciones; se registra expresamente sin convertir la prueba técnica en evidencia de calidad. [Verificación del protocolo](evidencias/verificacion-protocolo-v1.json).

## 2026-10-03 — Revisión de entrega c054225

- Se consultó origin y se identificó la nueva rama oe2/piloto-f05. Se extrajo únicamente su entrega para revisión, sin fusión ni modificación de originales.
- Se comprobaron 110 huellas contra objetos Git, configuraciones y registros de cuatro ejecuciones; se reprodujo el baseline de 360 pares y la estadística del CSV. Evidencia: [revisión-c054225.json](evidencias/revision-c054225.json).
- Incidencias del procedimiento: la primera verificación de identidad usó codificación predeterminada de Windows y falló; UTF-8 explícito coincide con la identidad del ejecutor Linux. La extracción local convirtió a CRLF 67 archivos y produjo discrepancias aparentes de huella; los 110 objetos originales Git coinciden. Se mantuvieron los archivos recibidos y se añadió verificación directa del commit.
- Resultado: evidencia técnica GPU RunPod coherente; se inspeccionaron tres figuras. Pendientes P04a–d documentados en la [revisión](REVISION_PILOTO_C054225.md). No se descargaron pesos inexistentes en la entrega ni se repitió inferencia; no se abrieron imágenes reservadas.

## 2026-10-03 — Pesos publicados y revisión independiente

- Se revisó el enlace de la entrega fddd072 y se descargaron los dos mejores checkpoints. Coinciden tamaños, SHA-256, configuraciones, contrato y época seleccionada (5).
- Se reprodujeron 360 predicciones por modelo en CPU, dentro de tolerancias frente al CSV. Se inspeccionaron las 18 vistas y se calculó una exploración regional; no se abrieron imágenes reservadas. [Informe y límites](REVISION_PESOS_PILOTO_F05.md).
- Incidencia local: fallos de lectura e índice Git ilegible; se completó el cálculo en un entorno aislado y la publicación mediante GitHub. No se reparó ni se reconstruyó el índice local.
- P04b resuelto para inferencia de validación y P04a cubierto para los dos mejores pesos. P04c avanza como exploración; P04d continúa pendiente. No se autorizó ni se lanzó la campaña principal.

## 2026-10-03 — Evaluación con regiones geométricas

- Por autorización de la dirección se avanzó en el diagnóstico regional usando datos y pesos ya recibidos. Se fijaron máscaras y medidas sin seleccionar píxeles desde predicciones; la validación ya observada se declara exploratoria.
- Se verificaron geometrías y shards, ocho pruebas analíticas y 2.304 rayos por integración numérica. Se produjeron 18 mapas de regiones, 234 registros región/método y 24 contrastes; figura inspeccionada. [Informe, evidencia y comandos](EVALUACION_GEOMETRICA_PILOTO_F05.md).
- Resultado: reducción de error y conservación de cuentas no son equivalentes. Se documentan sesgos por región y cocientes indefinidos por cero cuentas, sin pseudoconteos ni exclusión silenciosa.
- Incidencias: lectura local fallida, control de contraste cero y contador NumPy no serializable. Procedimientos corregidos y ejecutados completos en entorno aislado; Git local no reparado.
- P04c: diagnóstico geométrico verificado, aceptación física parcial. P04d: diseñar ajuste acotado antes de ampliar. Sin nuevas simulaciones, entrenamiento ni acceso a test/generalization.

## 2026-10-03 — Diseño del ajuste acotado de cuentas

- Se atendió la autorización de la dirección para preparar el siguiente ensayo. Se fijaron control y variante regional, datos, pesos iniciales, semilla, cinco épocas y evaluación pareada. [Diseño y estados](DISENO_AJUSTE_CUENTAS_F05.md).
- Se implementó el componente de pérdida regional y se verificaron nueve casos matemáticos. Se comprobó gradiente regional y total finito sobre los 20.543.809 parámetros con dos pares de entrenamiento; cero pasos de optimizador y pesos idénticos al checkpoint.
- Incidencias: utilidad de gradientes dependiente de SymPy ausente, sustituida por diferencias finitas explícitas; lectura de geometría corregida a UTF-8. Verificaciones finales satisfactorias.
- Estado: diseño/componentes verificados. Ajuste-01 integración, Ajuste-02 CPU/GPU con recuperación y Ajuste-03 piloto pareado pendientes. No se presenta el componente como ejecutor de entrenamiento ni se requiere nueva simulación Geant4.

## 2026-10-03 — Integración y recuperación del ajuste A/B

- Por autorización de la dirección se completaron lector, máscaras train/val, ejecutor, recuperación, auditor GPU, evaluación regional y figuras. Se conservan el diseño científico, el código histórico y las entregas estudiantiles. [Guía vigente](INSTRUCCIONES_AJUSTE_CUENTAS_F05.md).
- Se verificaron 90 mapas, 30 archivos de datos/metadatos y conservación de las 78 máscaras regionales val previas. Trece controles funcionales, nueve de pérdida y ocho geométricos satisfactorios. Las cuatro ejecuciones técnicas de red completa reproducen exactamente estados y predicciones al recuperar; 16 actualizaciones de la batería y cuatro preliminares. [Evidencia consolidada](evidencias/integracion-ajuste-v1.json).
- La regresión del evaluador usa 720 predicciones anteriores: diferencia cero en 468 valores regionales y reproducción de 24 contrastes. No son resultados de un nuevo piloto. Se generaron figuras técnicas y se inspeccionó su presentación.
- Incidencias: índice Git original ilegible, dependencias de Adam ausentes y betas con tipos mixtos. Se utilizó copia aislada, dependencias locales y conversión explícita a flotantes; la batería definitiva pasó. No se reparó el índice original.
- Ajuste-01 verificado; Ajuste-02 CPU verificado/GPU pendiente; Ajuste-03 pendiente. No se ejecutó piloto de cinco épocas ni se abrieron imágenes test/generalization. Próximo paso: comprobar CUDA y ejecutar A/B con aceptación técnica; no se declara mejora física ni cierre del OE2.

## 2026-10-03 — Revisión independiente del ajuste a6aa6b8

- Por autorización de la dirección se descargaron doce binarios de Drive y se verificaron tamaños/huellas; 137 textos coinciden con el inventario. Se auditaron seis checkpoints y se confirmó recuperación exacta en las cuatro ejecuciones técnicas. [Informe](REVISION_AJUSTE_A6AA6B8.md).
- Se reprodujeron 720 inferencias CPU, con diferencias máximas de píxel inferiores a 3,83×10^-6. El recálculo de 7.974 valores de evaluación discrepa como máximo 4,45×10^-16. Se verificaron 5.400 errores de cuentas, 168 estadísticas y 21 valores del bootstrap. [Evidencia](evidencias/revision-ajuste-a6aa6b8.json).
- Resultado: compromiso confirmado. B mejora Q en 15/18 vistas y empeora el error de borde en 18/18; el sesgo medio del cuerpo denso es −70,23 %, frente a −59,96 % inicial. Se generó e inspeccionó una figura de las 18 vistas.
- Incidencias resueltas en la revisión: dispositivo D: con errores, descarga temporal HTTP 403 y diferencias de representación textual; se trabajó en carpeta temporal C:, descarga pública por IDs y comparación de huellas. Las máscaras coinciden en contenido aunque sus NPZ comprimidos difieren. Una copia cGAN incompleta se descartó; se verificó la copia confirmada con generador y crítico.
- Ajuste-02 y la ejecución/evaluación de Ajuste-03 verificados; aceptación física y OE2 pendientes. Se documenta la [propuesta C0/C1 para cGAN](PROPUESTA_CONTINUACION_CGAN_F05.md), sin presentarla como lista para GPU. Próximo paso: integrar y verificar ese ejecutor antes de delegar entrenamiento.
- No se entrenó, no se fusionó la rama estudiantil ni se abrieron imágenes reservadas. Se mantiene el cierre del OE1.

## 2026-10-03 — Implementación y verificación CPU de C0/C1

- Por autorización de la dirección se implementó el diseño de continuación cGAN, conservando generador/crítico iniciales, cinco actualizaciones D por G, dos optimizadores nuevos y pérdida regional solo en G. No se modificó el motor histórico ni el ajuste U-Net.
- Diecinueve controles satisfactorios; cuatro ejecuciones completas verifican recuperación exacta de G, D, ambos Adam, todos los RNG utilizados, registros y predicciones. Batería definitiva: 16 actualizaciones G/80 D; comprobación preliminar adicional: 2 G/10 D. [Guía](INSTRUCCIONES_CONTINUACION_CGAN_F05.md) y [evidencia](evidencias/integracion-cgan-ajuste-v1.json).
- Se verificaron evaluación y figuras técnicas, tabla por anomalía frente a C0 y al modelo inicial, y ruta completa con fixtures del piloto anterior. El resultado técnico no acredita calidad: no se ejecutó el ensayo de cinco épocas.
- Se conservaron el entorno temporal aislado y las fuentes originales verificadas desde objetos Git, corrigiendo diferencias de extracción antes de la batería definitiva. No se reparó el índice Git original ni se abrieron imágenes reservadas.
- CG-01 verificado; CG-02 CPU verificado/GPU pendiente; CG-03 preparado bajo aceptación GPU y resultados pendientes. Próximo paso: estudiantes comprueban CUDA y, si se acepta y hay recursos disponibles, completan C0/C1 y entregan todos los resultados. OE2 continúa abierto.

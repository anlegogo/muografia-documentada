# Registro de cambios

## Cierre experimental del OE3 — 2026-10-04, Colombia

- Se consolida el registro de cierre, con evidencia, definición del factor y disposición de OE3-P01 a P06.
- Se diferencia ejecución terminada de cumplimiento científico parcial: benchmark negativo y opacidad no reconstruida.
- Se retiran como encargos vigentes las rutas anteriores de nuevas corridas; la integración editorial continúa pendiente.
- No se modifican datos, pesos, criterios ni resultados; se actualizan README, índice y revisión de propuesta.

## Diagnóstico nominal de opacidad — 2026-10-04, Colombia

- Se calculan 54 registros geométricos del soporte C2, 48 elegibles, con densidades del JSON y rayos rectos centrales. No se entrena ni se ejecuta transporte.
- Se verifica el registro, la exclusión de solapamientos y cuatro casos analíticos de unidades/composición. La diferencia de opacidad entre objetivo y control se separa en densidad y longitud.
- Se marcan seis filas de geo-gen-01/anomalía 2: el catálogo declara 0,048 g/cm³ y el constructor versionado sustituye rho<0,05 por G4_AIR. No se inventa densidad efectiva ni se altera la campaña.
- Se documenta la diferencia entre referencia nominal conocida y opacidad reconstruida a partir de cuentas. OE3-P06 avanza pero permanece parcial; primero se revisan trazabilidad de materiales y respuesta/calibración antes de solicitar cómputo nuevo.
- [Método, evidencia, incidencias y límites](objetivo-3/OPACIDAD_NOMINAL_Y_ALCANCE.md).


## Auditoría de la entrega OE3-C1 — 2026-10-04, Colombia

- Se conserva e incorpora la entrega de estudiantes `5c3b0ee`, ejecutada con código `39d8fd3` en una L40S. Se descargan 298 archivos de Drive y se verifican los 294 del manifiesto y 96 matrices (3.019.911.168 bytes; 11.520 predicciones nuevas).
- La dirección reproduce la evaluación en CPU usando los datos originales y las predicciones recibidas, sin otra inferencia ni entrenamiento. Se comparan todas las tablas y JSON numéricos, conservando diferencias de entorno y exclusiones.
- El benchmark se revisa también por vista: no se satisface conjuntamente SSIM/PSNR en las 768 combinaciones modelo/fracción/vista. El mínimo y el factor permanecen nulos; no se cambian umbrales para obtener éxito.
- Se publica síntesis de anomalías sobre soporte común, figura, scripts y evidencia de reproducción. El contraste de cuentas no acredita reconstrucción de opacidad.
- OE3-P05 verificado; P06 parcial por interpretación de opacidad, P03 con resultado negativo bajo el benchmark y sin factor físico positivo. P04 continúa aplazado. No se recomienda otra GPU por el solo hecho del resultado desfavorable.
- [Revisión y siguiente decisión metodológica](objetivo-3/REVISION_COMPLEMENTO_OE3_C1.md).


## Preparación del complemento OE3-C1 — 2026-10-04, Colombia

- Se fijan cuatro fracciones y ocho modelos congelados; se reutilizan 3.840 predicciones f05 y quedan 11.520 nuevas. No se entrena ni se simulan muones.
- Se incorpora un benchmark operativo frente a la entrada al 50 %, declarado posterior a resultados conocidos; no se presenta como umbral original ni aceptación física. Se calcula el mínimo muestreado sin asumir monotonía.
- Se implementan SNR/CNR locales con soporte y denominadores explícitos. El contraste de cuentas no se renombra como opacidad reconstruida.
- Pasan ocho pruebas analíticas y dos de flujo. La comprobación real cGAN/CPU reproduce cuatro salidas f05 con diferencia máxima 2,3544e-6; se comprueban formas de otras fracciones sin métricas científicas.
- El bloque f05 reproduce exactamente los resúmenes C2 y añade 9.774 filas locales. Se publican tablas, recibo e inventario; CUDA y las nuevas inferencias científicas siguen pendientes.
- [Instrucciones para estudiantes](objetivo-3/INSTRUCCIONES_COMPLEMENTO_OE3.md), incluyendo ejecución por modelo, integridad, reanudación y entrega. No se declara cierre del OE3 ni se inicia el informe final.


## Revisión directa de propuesta aprobada — 2026-10-04, Colombia

- Se reabrió el PDF de 35 páginas, se extrajo su texto y se inspeccionaron visualmente las páginas PDF 26 y 29. Se registra SHA-256; queda superada la limitación de lectura anterior.
- Se verifican requisitos de SNR local, contraste de opacidad y evaluación de modelos a diferentes submuestreos. La fase 4 exige umbrales predefinidos, pero el PDF no fija sus valores operativos.
- Se corrige la interpretación de cierre: 2:1 descriptivo al 5 % no completa la fase 4. Tampoco se exige medir tiempos en un detector real como condición original.
- OE3-P02 parcial, fuente oficial ya verificada; P05/P06 pendientes. No hubo nuevas simulaciones, entrenamiento, inferencias ni redacción del informe final.

[Revisión completa](docs/REVISION_PROPUESTA_APROBADA.md).

## Desglose experimental OE3 por vista y región — 2026-10-04, Colombia

- Actividad de revisión de la dirección: análisis de métricas conservadas, sin nueva simulación, entrenamiento ni inferencia. Se conserva la autoría estudiantil de las ejecuciones originales.
- Siete fuentes contrastadas con Git; 78 agregados reproducidos, control f05 y cuatro pruebas satisfactorios. Mismo resumen desde CSV originales y recalculados C2. Se publican 768 filas de vista, 4.032 regionales y 1.024 de contraste, código, huellas y figura inspeccionada.
- cGAN frente a entrada al 10 %: mejora SSIM/PSNR en 24/24 vistas y 480/480 correspondencias; Q empeora en 24/24. Contraste favorable en 21/22 vistas de soporte común. No se trata a las realizaciones como réplicas geométricas independientes.
- Se respalda una razón descriptiva 2:1 de conteos bajo SSIM/PSNR; no equivalencia física, máximo alcanzable ni tiempo medido. No se escoge una semilla por tres vistas favorables de B3_C1.
- OE3-P02 y P03 parciales; desglose completado. OE3-P04 se aplaza por indicación de la dirección: primero concluir revisión experimental. Siguiente decisión: alcance de calidad aceptado, sin otra corrida automática.

[Resultado experimental](objetivo-3/RESULTADO_EXPERIMENTAL_OE3.md).

## Calidad comparable y continuidad OE2–OE3 — 2026-10-04, Colombia

- Actividad de revisión de la dirección: contraste de la síntesis C2 y curvas existentes, leídas desde 166be6ff09b60341fde084d433266b94b6e832cc; no se entrenó, infirió ni simuló.
- Se verificaron las ocho desigualdades SSIM/PSNR de cGAN al 5 % frente a entrada al 10 % en cuatro geometrías y se añadió la tabla correspondiente al balance OE2.
- Resultado: mejora descriptiva frente al doble de conteos; no equivalencia con la referencia completa ni factor físico aceptado. La calidad comparable conserva alcance parcial.
- Se documentó la ruta OE3-P02 a P04: criterio de calidad, desglose por vista/región, comparación de fracciones y redacción. Las tareas adicionales siguen pendientes; no se requiere otra GPU para la síntesis.

[Balance OE2](objetivo-2/CIERRE_OE2.md) · [Ruta OE3](objetivo-3/README.md#ruta-de-continuidad-desde-el-oe2).

## Síntesis académica y cierre documental OE2 — 2026-10-04, Colombia

- Se redactan método, resultados, discusión y conclusión delimitada con la evidencia C2 existente; no hay nuevo entrenamiento ni simulación.
- Se generan e inspeccionan dos figuras desde matrices auditadas, con selección explícita y todas las continuaciones. Se añaden 18 resúmenes y 36 filas por geometría, su CSV y procedencia.
- EF-04 queda preparado como producto documental. La calidad comparable permanece parcial; integración editorial OE2-D01 pendiente. No se adopta el umbral SSIM histórico retirado ni se declara equivalencia física.

[Informe](objetivo-2/manuscrito/INFORME_OE2.md).

## Curvas descriptivas de exposición — 2026-10-04, Colombia

- Se calculan localmente cuatro fracciones de entrada sin red con los datos existentes y controles C2: 1.920 imágenes, 504 regiones y 216 contrastes. No hay nueva simulación, entrenamiento ni inferencia de redes.
- El caso 5 % concuerda con C2; cuatro pruebas verifican tratamiento de cruces y ausencia de extrapolación. Se publica figura inspeccionada, tablas completas, huellas y reproducción.
- Las redes al 5 % superan los promedios SSIM/PSNR de la entrada al 10 %, con peor conservación de cuentas. No se declara equivalencia física ni factor alcanzable. El contraste usa soporte común de 21 y 11 combinaciones, explícitamente distinto de C2.
- OE3-P01 verificado; OE3-P02 y P04 pendientes, P03 parcial. Se espera confirmar objetivo oficial y requisitos de calidad. Continúa redacción del manuscrito sin otra GPU.

[Curvas y límites](objetivo-3/README.md).

## Evaluación final y corrección C2 — 2026-10-04, Colombia

- Actividad de la dirección: auditoría de la entrega estudiantil 4e5945e, conservada sin modificar; no hubo nuevo entrenamiento.
- Se verificaron 32 matrices (1.006.637.056 bytes), 50 recibos/manifiestos frente a Git y ocho archivos de referencias. Se reprodujeron 4.320 filas de imagen y 1.134 regionales; muestra CPU/GPU de 32 inferencias consistente.
- Se identificó inestabilidad numérica en controles de contraste. C2 conserva el protocolo original, introduce desempate geométrico explícito y publica índices completos: cuatro pruebas, 162 comprobaciones de sensibilidad y reproducción exacta desde registro.
- Se conserva comparación antes/después: ocho contrastes de referencia cambian y un control puntual B1/generalización pasa a favorable; las doce clasificaciones globales mantienen el compromiso. No se afirma equivalencia física ni 20× demostrado.
- EF-02 y EF-03 verificados en el alcance indicado; EF-C2 verificado; EF-04 y OE2-P04 parciales por alcance académico/científico. Sigue incorporación al manuscrito y confirmación del OE3; no se pide otra corrida GPU.

- [Revisión C2](objetivo-2/REVISION_EVALUACION_FINAL_C2.md).

## Preparación de evaluación final OE2 — 2026-10-04, Colombia

- Por solicitud de la dirección, se sustituye la consolidación E1 como requisito bloqueante por inferencia final al 5 % con ocho redes existentes. No hay nuevo entrenamiento.
- Se fijan ocho pesos, cuatro geometrías reservadas y sus ocho archivos de distribución; 480 imágenes por red, 3.840 predicciones. Protocolo y fuentes se registran antes de desempeño reservado.
- Verificación local: cinco pruebas de contratos, siete controles de flujo sintético, ocho pesos/32 inferencias de validación y 441 campos de métricas contrastados. No se calcularon resultados reservados localmente.
- Se corrigió una aserción de igualdad decimal en la prueba sintética (0,1 frente a su representación binaria); el ejecutor no se modificó para cambiar ese resultado. Se representa PSNR infinito explícitamente en casos perfectos.
- EF-01 preparado; EF-02/03 pendientes de ejecución y auditoría. OE2-P04 sigue parcial; no se afirma equivalencia física ni desempeño en otras fracciones.
- [Protocolo](objetivo-2/PROTOCOLO_EVALUACION_FINAL_OE2.md) y [tarea delegada](objetivo-2/INSTRUCCIONES_EVALUACION_FINAL_OE2.md).

## Revisión y diagnóstico interior de E1 — 2026-10-04, Colombia

- Actividad: auditoría independiente de la entrega estudiantil 804ce85 y diagnóstico local de predicciones, sin nuevo entrenamiento.
- Evidencia: 55 binarios, 18 checkpoints, recuperación exacta B1–B3, 2.520 inferencias; 252 sesgos regionales y mapas de las seis vistas de geometría 1 por pareja.
- Resultado: borde mejor en las 54 comparaciones; exceso interior persistente. E1-04/E1-05 verificados; criterio de nueve controles no satisfecho. Sin aceptación física ni apertura de reservas; OE2-P04 permanece parcial.
- Se registra fe de erratas de tamaño/rutas sin alterar originales y se deja borrador de discusión.
- Siguiente paso delegado: reproducción CPU y consolidación documental, sin otro entrenamiento GPU. [Revisión](objetivo-2/REVISION_E1_804CE85.md) e [instrucciones](objetivo-2/INSTRUCCIONES_CIERRE_E1.md).

## 2026-10-04 — Preparación ejecutable del ensayo espacial E1

- Se fijó lambda_borde=0,629 mediante una regla anterior al perfil de doce lotes train (48 imágenes), sin ajustar con val. Se conservan los pesos iniciales.
- Se integraron configuraciones B1–B3 y herramientas separadas, equivalencia exacta del control, recuperación y rechazo de identidades incompatibles. Se verificaron doce ejecuciones técnicas CPU, evaluaciones, síntesis y controles de artefactos.
- Se preparó el orquestador que exige las tres aceptaciones GPU nuevas antes del piloto, evaluación común e inventario de entrega. El ensayo conserva ocho controles y añade reducción estricta del borde.
- Se delegan prueba GPU y seis continuaciones de cinco épocas, condicionadas a la aceptación técnica; no se ejecutaron aquí ni se concede aceptación física. [Diseño y evidencia](objetivo-2/DISENO_BORDE_CGAN.md).

## 2026-10-04 — Diagnóstico espacial y componente experimental E1

- Se separó el error del total de cuentas y el error píxel a píxel en 468 combinaciones de la entrega R1–R3. En las tres parejas mejora el total del borde mientras empeora su distribución espacial.
- Se comprobó la limitación de la pérdida regional mediante un contraejemplo y se implementó un componente espacial aislado con nueve controles satisfactorios.
- Cuatro sondeos train con la red real verifican gradientes finitos y estados idénticos, sin pasos de optimizador. Se conserva la oposición local observada en una muestra.
- Se documentan E1-01 a E1-05, evidencia y reproducción. Coeficiente, integración, recuperación y prueba GPU pendientes; sin autorización de campaña ni aceptación física. [Diagnóstico](objetivo-2/DIAGNOSTICO_ESPACIAL_CGAN.md).

## 2026-10-04 — Verificación independiente de la repetición cGAN R1–R3

- Se verificaron los 55 binarios de Drive y los estados de los 18 checkpoints de la entrega f6518ff. Las tres recuperaciones técnicas conservan igualdad exacta.
- Se reprodujeron las evaluaciones, los diagnósticos por vista/anomalía, la síntesis y 2.520 inferencias CPU. Se publican el verificador, la evidencia y una figura reproducible en PNG/PDF.
- Ninguna pareja satisface los ocho controles: Q mejora en dos de tres y el error de borde empeora en las tres. La entrega técnica queda verificada; no se concede aceptación física ni cierre del OE2. [Revisión completa](objetivo-2/REVISION_REPETICION_F6518FF.md).

## 2026-10-04 — Integración y verificación de la repetición cGAN

- Se implementaron las seis configuraciones R1–R3, identidad de pareja/semilla, aceptación por pareja y síntesis sin selección retrospectiva. Se conserva la formulación y el diseño prospectivo.
- Cincuenta controles satisfactorios y doce ejecuciones CPU completas verifican recuperación exacta en las tres parejas (48 G/240 D); evaluaciones técnicas y síntesis comprobadas. [Guía y evidencia](objetivo-2/INSTRUCCIONES_REPETICION_CGAN_F05.md).
- Preparados los comandos GPU, las seis continuaciones de cinco épocas y su entrega. Las aceptaciones históricas no habilitan esta versión. No se ejecutaron nuevas continuaciones de cinco épocas, CUDA ni imágenes reservadas; aceptación física y OE2 pendientes.

## 2026-10-04 — Valoración del compromiso y diseño de repetición cGAN

- Se analizaron las 18 vistas y 24 combinaciones de anomalía; se verificó la reproducción de resúmenes y se publicaron tabla CSV, evidencia JSON y figura PNG/PDF.
- C1 mejora q en 15/18 vistas frente a C0, pero empeora borde en las seis vistas de geo-val-02 y SSIM/PSNR en las 18 frente al inicial. La valoración no concede aceptación física.
- Se fijó un diseño de tres parejas nuevas, condicionado al mismo checkpoint inicial; integración de semillas y validación operativa pendientes. No se ejecutó entrenamiento. [Valoración y diseño](objetivo-2/VALORACION_COMPROMISO_CGAN_F05.md).

## 2026-10-04 — Verificación independiente de CG-04c y cinco épocas

- Se descargaron y verificaron 13 binarios, 1.970.094.884 bytes. Se confirmó recuperación exacta desde cuatro checkpoints técnicos y consistencia de las dos continuaciones finales.
- Se reprodujeron 5.334 valores de evaluación y 1.080 inferencias CPU de C0, C1 y cGAN inicial. [Informe y evidencia](objetivo-2/REVISION_BINARIOS_CG04C.md).
- CG-04 queda cerrado para el entorno entregado; las cinco épocas están verificadas. Se conserva la clasificación descriptiva, sin aceptación física ni cierre del OE2. No se inicia la campaña principal.

## 2026-10-04 — Corrección candidata CG-04c

- Se separó la derivación de Wasserstein y GP y se fijó su suma antes de un único paso Adam; se mantienen la pérdida, configuraciones y cinco pasos D por G.
- La identidad registra la política y nuevas huellas; checkpoints y aceptaciones anteriores se rechazan. No se cambia el criterio exacto de recuperación.
- Se verificaron 34 controles y cuatro ejecuciones completas CPU con recuperación exacta (16 G/80 D). [Guía y evidencia](objetivo-2/CORRECCION_GRADIENTES_CG04C.md).
- Se prepararon comandos L40S y continuidad condicionada hacia cinco épocas/evaluación. La aceptación GPU, los resultados del piloto y el cierre del OE2 siguen pendientes.

## 2026-10-04 — Revisión independiente de CG-04b

- Se verificaron 22 binarios, 780 598 748 bytes, estados e identidades; se reprodujeron 580 campos numéricos sin discrepancias respecto de la entrega.
- Los componentes aislados coinciden exactamente, mientras el gradiente conjunto difiere entre proceso continuo y nuevo. [Informe y límites](objetivo-2/REVISION_BINARIOS_CG04B.md).
- Se normalizó a LF la evidencia previa CG-04, sin cambiar su contenido JSON. CG-04 sigue parcial y las cinco épocas pendientes; no se modificó el entrenamiento.

## 2026-10-03 — Preparación de CG-04b

- Se implementó una prueba independiente para separar gradientes Wasserstein y penalización, con controles original/repetida/total y procesos continuos/nuevos. No se alteraron el entrenamiento ni la aceptación GPU.
- Se verificaron ocho controles matemáticos y funcionales y veinte procesos CPU con C0/C1; la evidencia cuantifica también el residuo de reconstrucción de la suma.
- La [guía CG-04b](objetivo-2/DIAGNOSTICO_GRADIENTES_CG04B.md) fija propósito, ecuaciones, comandos, entregables y límites. CG-04 continúa parcial y la prueba L40S queda pendiente.

## 2026-10-03 — Auditoría independiente de binarios CG-04

- Se descargaron y verificaron los 22 binarios (3 933 371 732 bytes), sus estados frente a las trazas y SSIM/PSNR contra referencias verificadas.
- Se confirmó recuperación de los valores registrados y divergencia posterior de gradientes del crítico en proceso CUDA nuevo; C1 presenta diferencia máxima de pesos G de 4,1216612e-5.
- Se documentaron evidencia, límites y siguiente comprobación en la [revisión CG-04](objetivo-2/REVISION_BINARIOS_CG04.md). La aceptación GPU y las continuaciones permanecen pendientes.

## 2026-10-03 — Diagnóstico dirigido de recuperación cGAN

- Se revisó la entrega estudiantil `b0ad0b1`: 97 huellas verificadas y código registrado coincidente con `04b2e46`. La causa CUDA permanece sin demostrar; faltan enlaces a los estados binarios nuevos.
- Se incorporó una herramienta independiente para controles continuos, recarga y reanudación en procesos separados, con huellas de estados y trazas de operaciones; no se modificaron entrenamiento, pérdidas ni aceptación.
- Se verificaron siete pruebas de detección y la batería CPU C0/C1, con comparación frente al ejecutor original sin instrumentación. La evidencia enlazada en la [guía](objetivo-2/DIAGNOSTICO_RECUPERACION_CGAN.md) delimita este control local.
- CG-04 permanece pendiente de ejecución y auditoría GPU; las continuaciones de cinco épocas siguen suspendidas.

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




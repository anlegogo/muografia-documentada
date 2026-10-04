# Bitácora de preparación del OE3

## Revisión directa de propuesta aprobada — 2026-10-04, Colombia

- Se reabrió el PDF de 35 páginas, se extrajo su texto y se inspeccionaron visualmente las páginas PDF 26 y 29. Se registra SHA-256; queda superada la limitación de lectura anterior.
- Se verifican requisitos de SNR local, contraste de opacidad y evaluación de modelos a diferentes submuestreos. La fase 4 exige umbrales predefinidos, pero el PDF no fija sus valores operativos.
- Se corrige la interpretación de cierre: 2:1 descriptivo al 5 % no completa la fase 4. Tampoco se exige medir tiempos en un detector real como condición original.
- OE3-P02 parcial, fuente oficial ya verificada; P05/P06 pendientes. No hubo nuevas simulaciones, entrenamiento, inferencias ni redacción del informe final.

[Revisión completa](../docs/REVISION_PROPUESTA_APROBADA.md).

## Desglose experimental OE3 por vista y región — 2026-10-04, Colombia

- Actividad de revisión de la dirección: análisis de métricas conservadas, sin nueva simulación, entrenamiento ni inferencia. Se conserva la autoría estudiantil de las ejecuciones originales.
- Siete fuentes contrastadas con Git; 78 agregados reproducidos, control f05 y cuatro pruebas satisfactorios. Mismo resumen desde CSV originales y recalculados C2. Se publican 768 filas de vista, 4.032 regionales y 1.024 de contraste, código, huellas y figura inspeccionada.
- cGAN frente a entrada al 10 %: mejora SSIM/PSNR en 24/24 vistas y 480/480 correspondencias; Q empeora en 24/24. Contraste favorable en 21/22 vistas de soporte común. No se trata a las realizaciones como réplicas geométricas independientes.
- Se respalda una razón descriptiva 2:1 de conteos bajo SSIM/PSNR; no equivalencia física, máximo alcanzable ni tiempo medido. No se escoge una semilla por tres vistas favorables de B3_C1.
- OE3-P02 y P03 parciales; desglose completado. OE3-P04 se aplaza por indicación de la dirección: primero concluir revisión experimental. Siguiente decisión: alcance de calidad aceptado, sin otra corrida automática.

[Resultado experimental](RESULTADO_EXPERIMENTAL_OE3.md).

## Calidad comparable y continuidad OE2–OE3 — 2026-10-04, Colombia

- Actividad de revisión de la dirección: contraste de la síntesis C2 y curvas existentes, leídas desde 166be6ff09b60341fde084d433266b94b6e832cc; no se entrenó, infirió ni simuló.
- Se verificaron las ocho desigualdades SSIM/PSNR de cGAN al 5 % frente a entrada al 10 % en cuatro geometrías y se añadió la tabla correspondiente al balance OE2.
- Resultado: mejora descriptiva frente al doble de conteos; no equivalencia con la referencia completa ni factor físico aceptado. La calidad comparable conserva alcance parcial.
- Se documentó la ruta OE3-P02 a P04: criterio de calidad, desglose por vista/región, comparación de fracciones y redacción. Las tareas adicionales siguen pendientes; no se requiere otra GPU para la síntesis.

[Ruta de continuidad](README.md#ruta-de-continuidad-desde-el-oe2).

## Curvas descriptivas de exposición — 2026-10-04, Colombia

- Se calculan localmente cuatro fracciones de entrada sin red con los datos existentes y controles C2: 1.920 imágenes, 504 regiones y 216 contrastes. No hay nueva simulación, entrenamiento ni inferencia de redes.
- El caso 5 % concuerda con C2; cuatro pruebas verifican tratamiento de cruces y ausencia de extrapolación. Se publica figura inspeccionada, tablas completas, huellas y reproducción.
- Las redes al 5 % superan los promedios SSIM/PSNR de la entrada al 10 %, con peor conservación de cuentas. No se declara equivalencia física ni factor alcanzable. El contraste usa soporte común de 21 y 11 combinaciones, explícitamente distinto de C2.
- OE3-P01 verificado; OE3-P02 y P04 pendientes, P03 parcial. Se espera confirmar objetivo oficial y requisitos de calidad. Continúa redacción del manuscrito sin otra GPU.

[Análisis y evidencia](README.md).

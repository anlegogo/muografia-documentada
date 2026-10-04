# Bitácora de preparación del OE3

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

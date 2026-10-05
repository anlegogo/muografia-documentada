# Bitácora de preparación del OE3

## Diagnóstico nominal de opacidad — 2026-10-04, Colombia

- Se calculan 54 registros geométricos del soporte C2, 48 elegibles, con densidades del JSON y rayos rectos centrales. No se entrena ni se ejecuta transporte.
- Se verifica el registro, la exclusión de solapamientos y cuatro casos analíticos de unidades/composición. La diferencia de opacidad entre objetivo y control se separa en densidad y longitud.
- Se marcan seis filas de geo-gen-01/anomalía 2: el catálogo declara 0,048 g/cm³ y el constructor versionado sustituye rho<0,05 por G4_AIR. No se inventa densidad efectiva ni se altera la campaña.
- Se documenta la diferencia entre referencia nominal conocida y opacidad reconstruida a partir de cuentas. OE3-P06 avanza pero permanece parcial; primero se revisan trazabilidad de materiales y respuesta/calibración antes de solicitar cómputo nuevo.
- [Método, evidencia, incidencias y límites](OPACIDAD_NOMINAL_Y_ALCANCE.md).


## Auditoría de la entrega OE3-C1 — 2026-10-04, Colombia

- Se conserva e incorpora la entrega de estudiantes `5c3b0ee`, ejecutada con código `39d8fd3` en una L40S. Se descargan 298 archivos de Drive y se verifican los 294 del manifiesto y 96 matrices (3.019.911.168 bytes; 11.520 predicciones nuevas).
- La dirección reproduce la evaluación en CPU usando los datos originales y las predicciones recibidas, sin otra inferencia ni entrenamiento. Se comparan todas las tablas y JSON numéricos, conservando diferencias de entorno y exclusiones.
- El benchmark se revisa también por vista: no se satisface conjuntamente SSIM/PSNR en las 768 combinaciones modelo/fracción/vista. El mínimo y el factor permanecen nulos; no se cambian umbrales para obtener éxito.
- Se publica síntesis de anomalías sobre soporte común, figura, scripts y evidencia de reproducción. El contraste de cuentas no acredita reconstrucción de opacidad.
- OE3-P05 verificado; P06 parcial por interpretación de opacidad, P03 con resultado negativo bajo el benchmark y sin factor físico positivo. P04 continúa aplazado. No se recomienda otra GPU por el solo hecho del resultado desfavorable.
- [Revisión y siguiente decisión metodológica](REVISION_COMPLEMENTO_OE3_C1.md).


## Preparación del complemento OE3-C1 — 2026-10-04, Colombia

- Se fijan cuatro fracciones y ocho modelos congelados; se reutilizan 3.840 predicciones f05 y quedan 11.520 nuevas. No se entrena ni se simulan muones.
- Se incorpora un benchmark operativo frente a la entrada al 50 %, declarado posterior a resultados conocidos; no se presenta como umbral original ni aceptación física. Se calcula el mínimo muestreado sin asumir monotonía.
- Se implementan SNR/CNR locales con soporte y denominadores explícitos. El contraste de cuentas no se renombra como opacidad reconstruida.
- Pasan ocho pruebas analíticas y dos de flujo. La comprobación real cGAN/CPU reproduce cuatro salidas f05 con diferencia máxima 2,3544e-6; se comprueban formas de otras fracciones sin métricas científicas.
- El bloque f05 reproduce exactamente los resúmenes C2 y añade 9.774 filas locales. Se publican tablas, recibo e inventario; CUDA y las nuevas inferencias científicas siguen pendientes.
- [Instrucciones para estudiantes](INSTRUCCIONES_COMPLEMENTO_OE3.md), incluyendo ejecución por modelo, integridad, reanudación y entrega. No se declara cierre del OE3 ni se inicia el informe final.


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




# Bitácora de preparación del OE3

## README para consulta y reproducción — 2026-10-26, Colombia

Por solicitud de la dirección se reorganiza la entrada del repositorio para su preparación pública: autores, alcance, resultados C2, benchmark negativo, limitaciones y rutas de ejecución. Se separan métricas archivadas, reevaluación, inferencia, entrenamiento y transporte; los avisos operativos antiguos quedan referidos a sus documentos históricos. La dirección informó la sustentación; no se registra fecha del acto, calificación ni aprobación no aportadas.

Se revisó la base `e6f139e406d47c07a210dc87e08314271bc5dcf4`. En una extracción de fuentes versionadas se regeneró la figura de curvas y pasaron 21 pruebas (4 de controles C2, 4 de comparaciones, 8 de métricas locales y 5 de EF-01). La prueba EF-01 falló inicialmente por permisos temporales y ausencia de `metrics` en la ruta de importación; pasó con acceso temporal y `PYTHONPATH` configurado, sin alterar las fuentes. Entorno existente: Python 3.12.14, NumPy 2.4.4, PyTorch 2.6.0+cpu, scikit-image 0.26.0, Matplotlib 3.11.1, SciPy 1.18.1 y filelock 3.32.3.

No se repitieron simulaciones, entrenamiento ni inferencia completa; no se verificó una instalación nueva ni acceso actual a Drive. No se modificaron datos, pesos, protocolos o entregas. Siguiente paso: revisar la actualización documental y resolver acceso externo/licencia antes de una distribución reutilizable. No se cambia la visibilidad del repositorio.


## Publicación editorial — 2026-10-04, Colombia

Actividad: incorporación de la versión corregida por solicitud de la dirección.

Se incorpora la versión LaTeX corregida del informe completo en `informe-final/latex/`, con figuras vectoriales, fuentes editables, datos de las figuras, PDF compilado y ZIP para Overleaf. Se conservan sin cambios los datos experimentales y los capítulos 2 y 5. La compilación local produjo 90 páginas, sin referencias indefinidas ni desbordamientos; las cuatro figuras corregidas se regeneraron y verificaron como vectoriales. No se realizaron nuevas corridas. La inversión de opacidad se delimita como extensión futura, no como requisito adicional de los objetivos aprobados. La publicación no sustituye la aprobación académica.

Evidencia: [registro de correcciones y verificaciones](../informe-final/latex/LEEME_CORRECCIONES_FINALES.txt). Procedimiento: importación del ZIP corregido y comparación byte por byte de sus 121 archivos. Siguiente paso: revisión de los autores y aprobación académica; no se reabren experimentos.

## Integración editorial — 2026-10-04, Colombia

Por autorización de la dirección se integran metodología, resultados, discusión y conclusiones de los tres objetivos en [informe-final](../informe-final/README.md). Se generan tres tablas desde la síntesis auditada, se enlazan seis figuras conservadas y se documentan nomenclatura y contraste con la propuesta. OE3-P04 queda con núcleo experimental integrado; la maquetación institucional y revisión de autores continúan separadas. No se ejecuta cómputo científico nuevo ni se cambia el balance parcial. Evidencia: FUENTES.json y VERIFICACION.json del informe.

## Cierre experimental y documental — 2026-10-04, Colombia

Por solicitud de la dirección se consolida el [cierre](CIERRE_OE3.md) sobre main `d7c865a`. Se revisan la auditoría OE3-C1, la opacidad nominal y el alcance/receta adoptados del OE1. No se ejecutan nuevas inferencias ni simulaciones. Se registra evaluación terminada, benchmark negativo y cumplimiento científico parcial; se conservan nulos f_min y R. P02/P03/P06 se disponen con sus limitaciones, sin declararlos verificados por cierre administrativo. P04 sigue como integración editorial. Se actualizan entradas e índice; originales y datos permanecen intactos.

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





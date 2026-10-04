# Cierre de la ejecución y de la síntesis documental del OE2

Fecha de registro: 2026-10-04, Colombia. Se consolida el trabajo solicitado por la dirección a partir de evidencia existente. No se declara una nueva ejecución experimental, ni aprobación formal de tesis, ni equivalencia física.

**Producto terminado:** [informe académico del OE2](manuscrito/INFORME_OE2.md), con formulación del objetivo, método, matemática, entrenamiento, comparación de ocho redes, dos figuras científicas, resultados por geometría y discusión. La [matriz](MATRIZ_CUMPLIMIENTO.md) vincula cada componente con evidencia.

## Decisión que sustenta el registro

Se consideran terminadas la ejecución final EF-02, su auditoría EF-03 y la preparación de la conclusión delimitada EF-04. No es necesario repetir entrenamientos ni inferencias para obtener estas conclusiones. La entrega original y los antecedentes se conservan sin reescritura.

El objetivo científico tiene cumplimiento parcial en la cláusula de calidad comparable: la cGAN mejora similitud de imagen, pero persisten alteraciones de cuentas. La documentación no transforma esa evidencia en aceptación física. No se certifica cumplimiento científico pleno del OE2; sí se deja concluida su evaluación y redactado el resultado alcanzado. La ausencia de un resultado plenamente favorable se informa como resultado de investigación, sin mantener indefinidamente pendiente la ejecución ya realizada.

## Qué queda a los autores y a la dirección

La integración editorial OE2-D01 consiste en incorporar el texto y las figuras al manuscrito oficial, revisar su numeración, referencias y correspondencia con la propuesta aprobada, y dejar registro de la versión revisada. Se entrega contenido redactado para esa integración, no una solicitud de escribir nuevamente el análisis ni de conseguir otra GPU.

Las evidencias pueden utilizarse desde ahora para la discusión del OE3. Las curvas existentes son descriptivas; no se declarará un factor efectivo de adquisición por el solo hecho de que f = 0,05 corresponda nominalmente a 20 veces menos conteos. Las decisiones de aceptación académica corresponden a la revisión del trabajo y no se atribuyen a este registro técnico.

## Procedencia y control de cambios

- Entrega estudiantil final: `4e5945eefea1f799a4e2adee8858d98d604cf4ba`.
- Revisión e integración C2: `1214307c525ace12c978ede5336fcf893abad7c7`.
- Base de esta consolidación: `08cdc0cb42ce0aa546aebfbf60fbfb89fb6081e3`.
- [Revisión vigente](REVISION_EVALUACION_FINAL_C2.md), [tablas derivadas](manuscrito/TABLAS_OE2.md) y [procedencia de figuras](manuscrito/figuras/procedencia-figuras.json).

La redacción de objetivo se recuperó de la revisión documental previa y se contrastó con el alcance del repositorio; el PDF aprobado local no pudo reabrirse en esta sesión. Se conserva esta limitación de trazabilidad documental sin inventar un criterio de aceptación ni bloquear la síntesis de resultados verificados.

## Precisión sobre calidad comparable y continuidad al OE3

Anotación de revisión: 2026-10-04, Colombia; fuentes leídas en `166be6ff09b60341fde084d433266b94b6e832cc`. Se precisa la interpretación, sin cambiar modelos, métricas ni aceptación. El objetivo plantea calidad comparable de imágenes: no establece literalmente equivalencia física completa como condición independiente. No se añade retrospectivamente esa condición al objetivo. A la vez, la calidad para uso muográfico requiere discutir las alteraciones de cuentas y no permite omitirlas al presentar la mejora de similitud.

Se verificó en las [curvas disponibles](../objetivo-3/evidencias/curvas-v1/curvas.json) y los [resultados C2](evidencias/ef01-c2/resultados.json) que la cGAN original alimentada con el 5 % de conteos supera en SSIM y PSNR a la entrada sin red al 10 %, en el promedio de cada una de las cuatro geometrías. Ambas métricas comparan cada imagen con la misma referencia de alta estadística; no comparan directamente entre sí la salida de la red y la entrada al 10 %.

| Geometría | SSIM cGAN 5 % | SSIM entrada 10 % | PSNR cGAN 5 % [dB] | PSNR entrada 10 % [dB] |
|---|---:|---:|---:|---:|
| geo-test-01 | 0.809504 | 0.766729 | 30.899515 | 25.240011 |
| geo-test-02 | 0.823321 | 0.782241 | 31.106504 | 25.468370 |
| geo-test-03 | 0.869662 | 0.840262 | 31.503588 | 26.458123 |
| geo-gen-01 | 0.825228 | 0.783422 | 31.047417 | 25.349330 |

**Conclusión respaldada:** el modelo mejora la similitud de imágenes de baja estadística y, según SSIM y PSNR, supera imágenes sin procesar con el doble de conteos en los escenarios evaluados. Esta mejora no garantiza conservación equivalente de los conteos regionales. La cGAN permanece por debajo de la entrada al 50 % en SSIM y PSNR agregados, tanto en prueba como en generalización.

Es una comparación descriptiva posterior a la evaluación, no una prueba estadística de equivalencia, un resultado por cada imagen individual ni una demostración de calidad equivalente a la referencia completa. La comparación de promedios no modifica por sí sola el estado parcial de calidad comparable de la matriz. Determinar su alcance académico exige contrastar la definición de calidad con la propuesta aprobada, sin elegir después un umbral que garantice éxito.

Se propone continuar con el OE3 utilizando las predicciones y curvas existentes. No es necesario esperar una afirmación de éxito pleno del OE2 para evaluar el desempeño y los límites del factor de adquisición. La [ruta de trabajo del OE3](../objetivo-3/README.md#ruta-de-continuidad-desde-el-oe2) separa mejora de similitud, conservación regional y reducción nominal. No se solicita otra GPU para este análisis.

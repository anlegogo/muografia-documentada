# Revisión directa de la propuesta aprobada: alcance de OE2 y OE3

**Disposición final — 2026-10-04:** el [cierre experimental del OE3](../objetivo-3/CIERRE_OE3.md) consolida la evaluación concluida y las desviaciones respecto de la propuesta. El cumplimiento científico permanece parcial; el benchmark da resultado negativo y la opacidad no se reconstruyó. Los pendientes históricos inferiores se interpretan con esa disposición, sin encargo de nuevas corridas.

**Actualización posterior al complemento OE3-C1:** la evaluación multifracción y las métricas SNR/CNR ya fueron ejecutadas y auditadas. El benchmark no se satisface; no se demuestra un factor bajo esa regla. La distinción entre contraste de cuentas y opacidad permanece. [Estado vigente y evidencia](../objetivo-3/REVISION_COMPLEMENTO_OE3_C1.md). Las tablas inferiores conservan los pendientes identificados en la lectura inicial de la propuesta.

Fecha de revisión: 2026-10-04, Colombia. Se volvió a abrir y leer directamente `Plan_trabajo_grado.pdf`, fuente aprobada identificada por la dirección. Se extrajo el texto de sus 35 páginas y se inspeccionaron visualmente las páginas PDF 26 y 29. No se editó ni reexportó el PDF.

**Identidad del archivo:** 2.784.610 bytes; SHA-256 `7404530659aab451897ac1eb0be05c8fe7ce9b5c96b0131b18fc638684d51084`. La paginación impresa difiere en dos unidades del índice físico del PDF. Esta lectura supera la limitación de acceso registrada en las revisiones anteriores; sus notas se conservan como antecedentes. Base de evidencia experimental consultada: `4a74e55ec9e9ea53442b57252718e1866eac7b04`.

## 1. Objetivos: texto directo

En la página impresa 9 (PDF 11), el objetivo 2 establece:

> Diseñar e implementar un modelo de aprendizaje profundo basado en redes generativas adversarias condicionales para transformar imágenes muográficas de baja estadística en imágenes de calidad comparable a las de alta estadística.

El objetivo 3 establece:

> Evaluar el desempeño del modelo entrenado y determinar el factor de reducción del tiempo de adquisición alcanzable con el esquema propuesto, comparando la calidad de las imágenes mejoradas por el modelo frente a imágenes obtenidas con tiempos de exposición prolongados.

La sigla cGAN utilizada en documentos de síntesis identifica correctamente el modelo, pero no aparece entre paréntesis en la formulación literal de este objetivo en el PDF. El objetivo general también incluye evaluar calidad y detectabilidad de estructuras internas; no limita la validación a similitud global.

## 2. Qué exige la metodología aprobada

| Fuente de la propuesta | Compromiso o precisión | Consecuencia para la revisión |
|---|---|---|
| 5.6.1, impresa 23 / PDF 25 | SSIM y PSNR comparan imagen generada y referencia de alta estadística. Se menciona SSIM superior a 0,9 como observación general de similitud perceptual. | El comentario 0,9 no está identificado como umbral de aceptación fijado para esta campaña; no se convierte retrospectivamente en tal. |
| 5.6.2, impresa 24 / PDF 26 | Se advierte que mejorar SSIM/PSNR puede difuminar anomalías. Se piden contraste de opacidad y SNR local en regiones de interés. | Detectabilidad forma parte del alcance original; no es una exigencia añadida por la auditoría. Sesgo Q y error espacial son útiles, pero no sustituyen por sí solos SNR local. |
| Fase 1, impresa 26 / PDF 28 | Pares sintéticos con múltiples niveles de submuestreo, equivalentes a exposiciones cortas, frente a todos los eventos disponibles. | No se exige una campaña con detector físico para ejecutar la metodología propuesta. La conversión temporal sigue sujeta a los supuestos de simulación y flujo. |
| Fase 3, impresa 27 / PDF 29 | Evaluación global, contraste de opacidad, SNR local e inspección visual; comparación de entradas, imágenes mejoradas y referencia. | Debe quedar documentada la evaluación de las dos familias de métricas. |
| Fase 4, impresa 27 / PDF 29 | Evaluar modelos a diferentes niveles de submuestreo e identificar el mínimo de estadística de entrada según umbrales predefinidos de SSIM y PSNR. | Variar solo las imágenes sin red mientras todas las redes reciben 5 % no completa este compromiso. |
| Resultados esperados, impresa 28 / PDF 30 | Evaluación que incluya preservación de detectabilidad y límites de aplicabilidad según estadística de entrada. | La ganancia 2:1 obtenida no equivale por sí sola a demostrar el mínimo de entrada ni la preservación requerida. |

El pasaje operativo de la fase 4 dice:

> Para ello, se evaluarán modelos a diferentes niveles de submuestreo y se identificará el nivel mínimo de estadística de entrada que permite al modelo producir imágenes con calidad comparable a la referencia de alta estadística, según umbrales predefinidos de SSIM y PSNR.

En el archivo revisado no se encontraron valores numéricos operativos para esos dos umbrales. La mención de SSIM > 0,9 está en el marco descriptivo, y no se encuentra una meta SSIM > 0,80. Los factores del artículo citado como antecedente tampoco son una meta mínima explícita del trabajo. La propuesta compromete definir umbrales, pero no permite reconstruir ahora una predefinición inexistente.

## 3. Contraste con lo ejecutado

La [evaluación final OE2](../objetivo-2/REVISION_EVALUACION_FINAL_C2.md) y el [desglose OE3](../objetivo-3/RESULTADO_EXPERIMENTAL_OE3.md) verifican SSIM/PSNR, sesgos, errores espaciales y contrastes sobre modelos congelados. Se dispone de inspección visual y de cuatro fracciones de entrada **sin red**. Las redes de esa evaluación recibieron exclusivamente 5 %.

La comparación cGAN 5 % frente a entrada 10 % sigue siendo válida y favorable en las 24 vistas para SSIM/PSNR. No se retiran esos resultados. Sin embargo, no demuestra que una red recibiendo 1 %, 10 % o 50 % satisfaga una calidad determinada, ni identifica el mínimo de entrada requerido por la fase 4.

En la evaluación vigente consultada no se acredita una tabla de SNR local de las anomalías. No se concluye que nunca haya existido una medida histórica: se exige vincular cualquier evidencia histórica a los datos corregidos, pesos y evaluación vigentes antes de reutilizarla. El contraste C2 es un cociente de cuentas de anomalía y controles geométricos menos uno; no debe denominarse automáticamente contraste de opacidad. Hace falta explicitar su correspondencia, justificarlo como indicador sustituto o implementar una medida apropiada. La propuesta no da una fórmula operativa de SNR local ni de ese contraste, de modo que su definición debe documentarse y conservarse entre métodos.

También existe una adaptación de particiones que debe explicarse: la propuesta menciona 70/15/15, mientras la campaña corregida utiliza 12 geometrías train, 3 val, 3 test y 1 de generalización. Se registra como diferencia metodológica; no se recomienda repartir de nuevo los datos tras conocer resultados ni invalidar retrospectivamente el conjunto del OE1.

## 4. Corrección de la conclusión anterior

La posibilidad expresada anteriormente de fundamentar el cierre únicamente con la comparación SSIM/PSNR frente al doble de conteos era incompleta. La lectura de las fases 3 y 4 añade compromisos explícitos que faltaba contrastar. Tampoco corresponde exigir ahora una medición real de campo como condición original: la propuesta plantea simulación y submuestreo.

**Balance:** implementación y evaluación al 5 % verificadas; OE2 y OE3 no deben declararse plenamente cumplidos por el solo hecho de completar ese análisis. El OE3 requiere completar evaluación multifracción, detectabilidad local y justificación de criterios de calidad. No se cambia la evidencia para garantizar un resultado favorable.

## 5. Pendientes experimentales concretos

| ID | Estado | Trabajo y criterio de cierre |
|---|---|---|
| OE3-P02 | parcial | Fuente y formulación oficial ahora verificadas. Falta localizar una predefinición posterior a la propuesta o justificar criterios operativos; si se definen ahora, declarar su carácter posterior y prever una validación adicional adecuada a la afirmación. No escogerlos para asegurar éxito con los números existentes. |
| OE3-P05 | pendiente | Preparar y ejecutar evaluación de redes con distintas fracciones de entrada disponibles. Conservar normalización de entrenamiento, identidades, modelos y particiones. Puede estudiarse primero el uso de pesos existentes, declarando qué fracciones no formaron parte de su entrenamiento; no se asume que se necesite reentrenar todas las variantes. |
| OE3-P06 | pendiente | Definir y verificar SNR local y correspondencia del contraste con opacidad; aplicar a entradas, predicciones y referencias con regiones y exclusiones consistentes. No confundir SNR local, CNR, variación entre realizaciones o error espacial sin una definición explícita. |
| OE3-P03 | parcial | Incorporar P02, P05 y P06 para determinar el mínimo de entrada estudiado y el factor correspondiente, o informar que no se demuestra bajo el criterio. El 2:1 descriptivo actual se conserva con sus límites. |
| OE3-P04 | pendiente | Informe final aplazado por indicación de la dirección hasta culminar la parte experimental. |

**Secuencia recomendada:** preparar primero un protocolo acotado de estos pendientes y sus controles; completar lo calculable con datos/predicciones existentes; delegar únicamente la inferencia adicional que resulte necesaria. No se solicita otra simulación Geant4 ni se inicia entrenamiento por esta revisión. Una nueva evaluación no borra la exposición histórica del catálogo ni convierte automáticamente una decisión posterior en criterio prospectivo.

La revisión presente no ejecuta SNR ni inferencias multifracción. Deja identificado el trabajo faltante contra la propuesta real, conservando el resultado útil ya obtenido.


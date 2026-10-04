# Síntesis del OE2 y transición al OE3

**Actualización:** la comparación descriptiva de las cuatro fracciones ya se realizó y se conserva en [curvas del OE3](../objetivo-3/README.md). No implica un factor de reducción aceptado ni cambia las conclusiones C2.

2026-10-04, Colombia. Documento de la dirección derivado de la [revisión EF-01-C2](REVISION_EVALUACION_FINAL_C2.md). No sustituye la redacción oficial de los objetivos ni declara resultados experimentales nuevos.

## Texto propuesto para resultados y discusión

Se implementó y entrenó un modelo generativo condicionado para recuperar imágenes muográficas a partir de una fracción de conteos de 0,05. Se comparó con una red U-Net entrenada con pérdida L1 y con la entrada de baja estadística, escalada a cuentas equivalentes. La evaluación final incluyó tres geometrías de prueba y una geometría de generalización, con seis vistas y veinte realizaciones por vista. Se evaluaron ocho redes previamente congeladas, incluidas seis continuaciones destinadas a estudiar conservación regional y error de borde. Estas continuaciones comparten inicialización y no constituyen entrenamientos independientes desde cero.

En prueba, la cGAN original aumentó SSIM de 0,7643 a 0,8342 y PSNR de 24,258 a 31,170 dB respecto de la entrada. U-Net alcanzó 0,8545 y 33,074 dB. Sin embargo, el indicador regional Q aumentó de 1,832 % en la entrada a 14,566 % en la cGAN y 22,388 % en U-Net. Q resume sesgo de cuentas en las regiones definidas; no representa error de densidad ni un porcentaje de error de toda la imagen. Las continuaciones redujeron Q respecto de las redes originales, con valores entre 3,996 % y 5,825 % en prueba, a costa de métricas de imagen inferiores a U-Net. El término espacial de borde redujo el error de borde en las cuatro geometrías, pero no produjo una mejora simultánea de todos los indicadores.

La corrección numérica EF-01-C2 estabilizó la selección de controles de contraste y conservó sus índices exactos. SSIM, PSNR y los indicadores regionales permanecieron iguales. El efecto sobre contraste se informa con las tablas corregidas y su comparación con la entrega original. Las doce comparaciones conservaron la clasificación de compromiso o deterioro en al menos un indicador. No se seleccionó una semilla favorable después de abrir los datos de prueba.

Se verificaron la implementación, el entrenamiento y la evaluación descriptiva al 5 % de conteos. La mejora de similitud y reducción de ruido no demuestra por sí sola equivalencia con alta estadística, porque persisten alteraciones de cuentas y no se había fijado un margen físico de equivalencia. El alcance se limita a referencias idealizadas y a un catálogo conocido, con exposición histórica de las escenas reservadas. Por ello no se afirma generalización a volcanes reales, equivalencia física, desempeño en otras fracciones ni validación experimental de un factor de reducción de adquisición.

## Síntesis preparada e integración editorial

Se ha preparado el [informe académico completo](manuscrito/INFORME_OE2.md), con matemática, tablas C2, figuras, discusión, [matriz de cumplimiento](MATRIZ_CUMPLIMIENTO.md) y [registro de cierre documental](CIERRE_OE2.md). EF-04 ya cuenta con una conclusión delimitada redactada. La integración en el manuscrito oficial y su revisión editorial quedan registradas como OE2-D01. No se requiere que los estudiantes repitan el análisis ni ejecuten otra GPU para esta entrega.

El cumplimiento científico de calidad comparable sigue siendo parcial; la elaboración del capítulo no cambia ese resultado. Las referencias posteriores a confirmación del texto oficial se conservan como antecedente de esta síntesis: el nuevo informe recupera la formulación de la revisión de propuesta, dejando explícito que no se pudo reabrir el PDF local en esta sesión.

## Preparación del objetivo 3

La formulación comunicada provisionalmente es evaluar el desempeño y determinar el factor de reducción de adquisición comparando imágenes mejoradas con exposiciones prolongadas. Se espera confirmar la redacción oficial antes de declarar su cumplimiento. La evaluación realizada ya aporta desempeño y referencias; se reutilizará, sin tratarla como un experimento nuevo independiente.

Para flujo estable y condiciones de detección iguales, la esperanza de conteos satisface E[N(t)] = λt. Si f = t_bajo/t_ref = 0,05, el factor nominal es t_ref/t_bajo = 1/f = 20. En este conjunto las imágenes de baja estadística se construyen mediante submuestreo de conteos: el factor es una equivalencia idealizada de exposición, no una medición de tiempo de campo. La duración de entrenamiento o inferencia no es el tiempo de adquisición.

Determinar un factor alcanzable requiere especificar calidad aceptable. No se escogerá después de observar los resultados un umbral que garantice 20×. Deben separarse: reducción nominal de conteos, equivalencia descriptiva según SSIM/PSNR y aceptación física según cuentas/contraste. Si ninguna condición satisface el criterio acordado, se reportará que no se ha demostrado el factor bajo ese criterio.

Se completó localmente el análisis de curvas descriptivas de la entrada para las fracciones ya disponibles (0,01; 0,05; 0,10; 0,50), comparadas con los modelos f05. Esas curvas no demuestran que el modelo funcione cuando recibe otra fracción, ni permiten extrapolar un máximo más allá de los puntos estudiados. La referencia de alta estadística también tiene ruido. Las veinte realizaciones no reemplazan geometrías independientes. Antes de nuevas corridas, se definirá el alcance de esa comparación y cualquier margen científico con justificación externa o de aplicación, dejando explícito qué decisiones son posteriores a esta evaluación.

La incorporación del capítulo y la confirmación del objetivo 3 son los siguientes pasos de coordinación. No se programa una campaña adicional ni se solicita GPU en esta revisión.

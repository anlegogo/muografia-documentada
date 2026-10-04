# Diseño, implementación y evaluación de una cGAN para imágenes muográficas de baja estadística

Documento de síntesis académica del objetivo específico 2. Revisión: 2026-10-04, Colombia. La redacción consolida experimentos ya ejecutados y auditados; las figuras se elaboran posteriormente con las matrices conservadas. El cierre documental no constituye una declaración de equivalencia física ni una aprobación de la tesis.

## 1. Objetivo y alcance de la conclusión

La formulación del objetivo específico 2 es: «Diseñar e implementar un modelo de aprendizaje profundo basado en redes generativas adversarias condicionales (cGAN) para transformar imágenes muográficas de baja estadística en imágenes de calidad comparable a las de alta estadística».

La fuente académica es `Plan_trabajo_grado.pdf`, apartado de objetivos específicos. La transcripción se recupera de la revisión documental previa de la propuesta; coincide con el alcance consignado en el [README del OE2](../README.md). El PDF no pudo reabrirse desde la ubicación local durante esta preparación, por lo que no se presenta esta transcripción como una nueva verificación del archivo. La revisión previa distingue la propuesta aprobada de una versión antigua que exigía SSIM > 0,80; ese umbral retirado no se adopta como criterio de cierre.

Se estudia una transformación de imágenes angulares de conteos. La salida no es un mapa de densidad ni una reconstrucción tridimensional del volcán. La pregunta experimental consiste en determinar qué concordancia con la referencia se obtiene al introducir una fracción de conteos de 0,05, y qué diferencias aparecen entre similitud de imagen y conservación de cuentas. La evaluación final permite concluir sobre los modelos y escenarios conservados, sin exigir un resultado favorable para dar por terminada la ejecución del experimento.

La [matriz de cumplimiento](../MATRIZ_CUMPLIMIENTO.md) distingue los componentes verificados del objetivo y el alcance parcial de la calidad comparable. El desarrollo y su evaluación están terminados; la afirmación amplia de comparabilidad con alta estadística no queda demostrada por todas las medidas estudiadas.

## 2. Datos, particiones y representación

Se utiliza el conjunto corregido del OE1, cuya [ficha](../../objetivo-1/FICHA_CONJUNTO_OE1.md) registra 19 escenarios idealizados y seis vistas por escenario. Cada imagen tiene 256 × 256 píxeles angulares. Las cuatro fracciones disponibles y las veinte realizaciones por fracción producen 9.120 pares. El presente experimento utiliza exclusivamente f = 0,05; no debe confundirse el tamaño del conjunto completo con el número empleado para entrenar cada modelo.

| Partición | Geometrías | Vistas | Pares al 5 % | Uso |
|---|---:|---:|---:|---|
| Entrenamiento | 12 | 72 | 1.440 | Ajuste de parámetros y escala |
| Validación | 3 | 18 | 360 | Selección del checkpoint original y diagnóstico de ajustes |
| Prueba | 3 | 18 | 360 | Comparación final descriptiva |
| Generalización | 1 | 6 | 120 | Comparación final descriptiva, separada |

Sea c_p el conteo de referencia en el píxel p y n_{f,k,p} su realización de baja estadística. El procedimiento de submuestreo se expresa como

$$n_{f,k,p}\mid c_p\sim\operatorname{Binomial}(c_p,f),\qquad x_{f,k,p}=n_{f,k,p}/f.$$

Así, la esperanza condicional de x es c. Sin embargo, las imágenes de baja estadística y la referencia comparten los eventos de origen: no constituyen dos mediciones de campo independientes. La referencia también tiene estadística finita. Las veinte realizaciones describen variabilidad de submuestreo dentro de una escena y no equivalen a veinte geometrías nuevas.

La representación de entrada y objetivo utiliza una transformación acotada, con escala estimada únicamente en entrenamiento:

$$T(c)=\frac{\log(1+c)}{s+\log(1+c)},\qquad s=8{,}239329427901795.$$

El generador recibe u = T(x) y aproxima y = T(c). Para evaluar cuentas se invierte su salida z:

$$\widehat c=T^{-1}(z)=\exp\left(\frac{sz}{1-z}\right)-1,\qquad 0\le z<1.$$

Esta inversión es necesaria: un error pequeño en la escala acotada no representa un error constante en cuentas. Las sumas regionales se realizan después de invertir, sin recortar predicciones ni añadir pseudocuentas. La normalización y sus huellas quedan asociadas a los pesos; no se recalcula una escala con prueba o generalización.

Las reservas se conservaron separadas en el entrenamiento corregido, pero las escenas del catálogo tuvieron exposición histórica durante el desarrollo previo. La [declaración de procedencia](../entregas/2026-10-04-evaluacion-final-f05/PROCEDENCIA_RESERVAS.md) impide presentar esta evaluación como una validación confirmatoria sobre escenarios totalmente desconocidos.

## 3. Modelo y entrenamiento

El generador `unet_dc_5` implementa una U-Net de cinco niveles, con canales 64, 128, 256, 512 y 512. Cada bloque contiene dos convoluciones de 3 × 3, normalización por instancia y activación LeakyReLU. Cuatro operaciones de reducción espacial llevan de 256 × 256 a 16 × 16; el decodificador recupera la resolución mediante convoluciones transpuestas y conexiones de concatenación con el codificador. Una convolución final de 1 × 1 y una sigmoide producen una imagen de un canal. El generador tiene 20.543.809 parámetros. La [implementación](../implementacion/models/unet_generator.py) constituye la especificación exacta.

La cGAN incorpora el crítico condicional `patch_critic_70`, que recibe la entrada junto con la imagen real o generada. Para cada muestra, el promedio espacial de sus puntuaciones define D(u,y). La [corrección v1](../CORRECCIONES_V1.md) fija el cálculo coherente de la penalización de gradiente; no se usa la suma de parches como si fuera la puntuación media de una imagen.

Con $\widetilde y=\epsilon y+(1-\epsilon)G(u)$, la pérdida del crítico y la del generador original se escriben como

$$L_D=\mathbb E[D(u,G(u))]-\mathbb E[D(u,y)]+10\mathbb E[(\|\nabla_{\widetilde y}D(u,\widetilde y)\|_2-1)^2],$$

$$L_G=-\mathbb E[D(u,G(u))]+100L_1,\qquad L_1=\mathbb E[\|G(u)-y\|_1/P],$$

donde P es el número de píxeles y la esperanza representa el promedio sobre las muestras del lote. El control U-Net conserva el mismo generador y se entrena con 100 L1, sin componente adversario. La comparación permite examinar la contribución observada del entrenamiento adversario bajo estas configuraciones; no establece superioridad universal entre familias de redes.

El [piloto](../PROTOCOLO_PILOTO_F05.md) fija lote cuatro, Adam con tasa 10⁻⁴ y parámetros (0; 0,9), cinco actualizaciones del crítico por actualización del generador y semilla 2026100301. Se conserva el conjunto de realizaciones, sin nuevas versiones de submuestreo durante el entrenamiento. La [entrega revisada](../REVISION_PILOTO_C054225.md) registra parada temprana tras 12 épocas para U-Net y 13 para cGAN. En ambos casos se seleccionó el checkpoint de la época 5 por validación. Por tanto, «checkpoint de época 5» no significa que las ejecuciones originales duraran solo cinco épocas. La [verificación de pesos](../REVISION_PESOS_PILOTO_F05.md) documenta la reproducción posterior de sus predicciones.

## 4. Continuaciones para conservar cuentas y reducir errores de borde

La evaluación geométrica de validación identificó que la mejora de SSIM y PSNR coexistía con sesgos regionales. Los ensayos posteriores abordaron ese problema conservando el generador y la normalización. La síntesis final incluye los modelos originales y las seis continuaciones del [ensayo E1](../DISENO_BORDE_CGAN.md), sin seleccionar retrospectivamente una semilla ganadora.

En E1, C0 ya incluye la pérdida regional y C1 añade el término espacial de borde. Estas etiquetas no deben trasladarse a ensayos históricos donde C0 significaba otra configuración:

$$L_G^{C0}=L_{\mathrm{adv}}+100L_1+L_{\mathrm{reg}},\qquad L_G^{C1}=L_G^{C0}+0{,}629L_{\mathrm{borde}}.$$

Lreg promedia diferencias $|\log(1+\overline{\widehat c}_R)-\log(1+\overline c_R)|$, con igual peso entre familias de regiones no vacías, entre anomalías de una familia y entre imágenes del lote. La barra representa la media espacial dentro de la región; no se promedian logaritmos de cuentas por píxel. Su definición y exclusiones están en el [diseño regional](../DISENO_AJUSTE_CUENTAS_F05.md) y la [función implementada](../herramientas/perdida_cuentas_regionales.py). El término espacial se define como

$$L_{\mathrm{borde}}=\frac{1}{B}\sum_{b=1}^{B}\frac{\sum_{p\in R_b}|\widehat c_{bp}-c_{bp}|}{\sum_{p\in R_b}c_{bp}}.$$

Aquí B es el tamaño del lote y Rb la máscara geométrica de borde correspondiente a cada muestra. Se rechazan soportes menores de veinte píxeles, referencias vacías y valores no finitos. Las máscaras orientan la pérdida durante entrenamiento, pero no se convierten en entradas adicionales necesarias para generar una imagen.

El coeficiente 0,629 se fijó mediante un perfil de gradientes en doce lotes de entrenamiento, antes de comparar los nuevos resultados de validación. Es una decisión de escala de optimización, no una tolerancia física. B1, B2 y B3 emplean semillas 2026100411, 2026100412 y 2026100413. Cada pareja parte de los mismos pesos originales de generador y crítico, con optimizadores nuevos, tasa 10⁻⁵ y cinco épocas adicionales. Se conserva la quinta época de cada continuación según el diseño fijo. Las seis redes no son seis entrenamientos independientes desde cero.

Las comprobaciones de recuperación técnica y la [revisión de E1](../REVISION_E1_804CE85.md) respaldan la ejecución. Recuperar exactamente un entrenamiento evita introducir una diferencia técnica entre variantes; por sí mismo no demuestra calidad física.

## 5. Evaluación final y trazabilidad

El [protocolo EF-01](../PROTOCOLO_EVALUACION_FINAL_OE2.md) congela ocho modelos, cuatro geometrías y 480 entradas, generando 3.840 predicciones. La entrega estudiantil corresponde a `4e5945eefea1f799a4e2adee8858d98d604cf4ba`. Su integración y revisión C2 se publicaron en `1214307c525ace12c978ede5336fcf893abad7c7`; la síntesis presente parte de `08cdc0cb42ce0aa546aebfbf60fbfb89fb6081e3`.

SSIM y PSNR se calculan en la escala T con rango uno. SSIM utiliza ventana uniforme de 7 × 7, K1 = 0,01 y K2 = 0,03; PSNR = −10 log10(MSE) para ese rango. Los valores se promedian por geometría y luego con igual peso entre geometrías de una partición. No se mezclan prueba y generalización en una única cifra de desempeño.

Para una región R y realización k, el sesgo firmado y el error espacial relativo son

$$b_{Rk}=\frac{\sum_{p\in R}(\widehat c_{kp}-c_p)}{\sum_{p\in R}c_p},\qquad a_{Rk}=\frac{\sum_{p\in R}|\widehat c_{kp}-c_p|}{\sum_{p\in R}c_p}.$$

El indicador Q de una geometría promedia con igual peso dos componentes: el valor absoluto del sesgo medio entre realizaciones de roca y el correspondiente a las anomalías. Las anomalías se promedian dentro de cada vista, y después se promedian las vistas. En particular, el valor absoluto se aplica después de promediar sesgos entre realizaciones; Q no es la media de todos los errores absolutos por píxel. Un Q bajo puede coexistir con ruido alto. Q tampoco es un error de densidad ni un porcentaje de error de toda la imagen.

El contraste de anomalía compara su media de cuentas con controles de roca sin anomalía, a igual elevación y con longitudes de trayecto próximas. Se expresa como el cociente de medias menos uno y se evalúa su error absoluto frente a la referencia. La [corrección C2](../REVISION_EVALUACION_FINAL_C2.md) resuelve empates numéricos en la selección de donantes mediante tolerancia geométrica de 10⁻⁸ m y guarda los índices exactos. Es una corrección posterior a la evaluación, no un protocolo prospectivo nuevo. No modifica pesos, imágenes, regiones, SSIM ni PSNR.

Se conservan 54 registros de contraste, de los cuales 48 son estimables geométricamente. El resumen C2 usa soporte común completo de todos los métodos: 30 combinaciones en prueba y 16 en generalización. Los casos restantes no se convierten en ceros ni se ocultan. Deben citarse las tablas corregidas; los contrastes de la entrega original permanecen como antecedente.

La auditoría verificó 83 archivos distribuidos, incluidas 32 matrices con 1.006.637.056 bytes. El recálculo reprodujo exactamente 4.320 filas de métricas de imagen; las 1.134 filas regionales coincidieron hasta 4,44 × 10⁻¹⁶. La inferencia independiente se comprobó sobre una muestra de 32 imágenes, con diferencia máxima CPU/GPU de 4,85 × 10⁻⁶. Esa muestra no debe describirse como una nueva inferencia de las 3.840 salidas: la reevaluación completa correspondió a las métricas sobre matrices conservadas. Los [resultados C2](../evidencias/ef01-c2/resultados.json) enlazan la evidencia numérica vigente.

## 6. Resultados

La Tabla 1 compara todos los métodos en las dos particiones. Q se expresa en porcentaje; el error de contraste es adimensional. SSIM y PSNR aumentan con la similitud, mientras Q y el error de contraste disminuyen con la discrepancia correspondiente. Los resultados completos por geometría, incluidos cielo y borde, se conservan en [tablas completas](TABLAS_OE2.md).

| Partición | Modelo | SSIM | PSNR [dB] | Q [%] | Error de contraste |
|---|---|---:|---:|---:|---:|
| test | entrada | 0.764308 | 24.257520 | 1.8321 | 0.337054 |
| test | unet_original | 0.854477 | 33.073913 | 22.3881 | 0.092463 |
| test | cgan_original | 0.834162 | 31.169869 | 14.5661 | 0.135104 |
| test | B1_C0 | 0.827666 | 30.839092 | 5.8245 | 0.133285 |
| test | B1_C1 | 0.827813 | 30.848882 | 4.8209 | 0.102743 |
| test | B2_C0 | 0.827375 | 30.771852 | 3.9957 | 0.112458 |
| test | B2_C1 | 0.827304 | 30.770108 | 4.7270 | 0.109112 |
| test | B3_C0 | 0.826329 | 30.728786 | 4.8276 | 0.116575 |
| test | B3_C1 | 0.827260 | 30.767968 | 5.4800 | 0.127915 |
| generalization | entrada | 0.750185 | 23.903636 | 1.0927 | 0.289711 |
| generalization | unet_original | 0.845414 | 32.883414 | 26.5053 | 0.071503 |
| generalization | cgan_original | 0.825228 | 31.047417 | 16.9586 | 0.086302 |
| generalization | B1_C0 | 0.816116 | 30.484632 | 3.8080 | 0.105524 |
| generalization | B1_C1 | 0.815143 | 30.508758 | 4.3228 | 0.090703 |
| generalization | B2_C0 | 0.814546 | 30.331068 | 4.1305 | 0.114919 |
| generalization | B2_C1 | 0.815367 | 30.403166 | 4.7548 | 0.096729 |
| generalization | B3_C0 | 0.814863 | 30.404222 | 4.0539 | 0.073659 |
| generalization | B3_C1 | 0.814591 | 30.371460 | 2.2712 | 0.077246 |


**Tabla 1.** Resultados finales calculados de la síntesis C2, sin elegir modelos después de observar prueba.

En prueba, la cGAN original mejora SSIM de 0,7643 a 0,8342 y PSNR de 24,258 a 31,170 dB respecto de la entrada. U-Net alcanza 0,8545 y 33,074 dB. Sin embargo, Q pasa de 1,832 % en la entrada a 14,566 % con cGAN y 22,388 % con U-Net. La mejor concordancia en la representación acotada no se traduce en mejor conservación del promedio regional de cuentas.

Las seis continuaciones presentan Q entre 3,996 % y 5,825 % en prueba, inferior al de los modelos originales, pero superior al de la entrada. Sus métricas de imagen también son inferiores a las de U-Net. Generalización muestra el mismo tipo de compromiso: la entrada alcanza Q = 1,093 %, frente a 16,959 % de cGAN y 26,505 % de U-Net. No se obtiene una variante que resuelva simultáneamente todas las discrepancias evaluadas.

La Figura 1 muestra la primera vista y realización de cada geometría, fijadas por índice. La escala es idéntica en los dieciséis paneles y no se ajusta por imagen. La suavidad de U-Net y la textura de cGAN deben interpretarse junto con las medidas regionales; ninguna apariencia constituye por sí sola evidencia de recuperación física.

![Figura 1. Referencia, entrada al 5 %, U-Net y cGAN en cuatro casos fijados por índice.](figuras/comparacion-fija.png)

**Figura 1.** Comparación descriptiva en T(c), vista 0 y realización 0. Los ejes indican índices de píxel angular, no coordenadas cartesianas ni distancias.

Para mostrar una limitación explícita, la Figura 2 toma la geometría con mayor Q de la cGAN original entre las cuatro evaluadas: geo-test-03, con Q = 27,835 %. Dentro de ella se mantiene vista 0 y realización 0; no se busca la imagen visualmente más desfavorable. Se incluyen las seis continuaciones y sus residuos normalizados.

![Figura 2. Caso desfavorable y residuos de todos los modelos congelados.](figuras/caso-desfavorable.png)

**Figura 2.** Comparación posterior a la evaluación, seleccionada por una regla descriptiva explícita. La fila inferior representa diferencias en T(c), con escala común simétrica; no representa sesgo en cuentas ni error de densidad. El Q citado corresponde a la geometría completa, no al panel individual.

Las doce comparaciones predeclaradas —seis por partición— conservan la clasificación de compromiso o deterioro en al menos un indicador. El error espacial de borde se reduce en las comparaciones C1/C0, pero esa mejora no elimina los compromisos restantes. C2 cambia la lectura puntual de contraste en B1/generalización: C1 presenta menor error que C0. No cambia la clasificación global de ninguna comparación. Por ello, ni la frase histórica de nueve comparaciones ni la interpretación anterior de ese contraste deben trasladarse al informe final.

## 7. Discusión y conclusión del objetivo

El desarrollo demuestra que una cGAN condicional puede transformar las entradas al 5 % en imágenes con mayor similitud respecto de la referencia bajo SSIM y PSNR. El control U-Net supera a la cGAN original en ambas métricas en las particiones evaluadas. La componente adversaria no muestra una ventaja global en esta comparación; atribuirle una recuperación física superior requeriría evidencia adicional que los resultados presentes no proporcionan.

La entrada escalada conserva mejor los promedios regionales pese a su ruido visible. Esto es coherente con la esperanza condicional del submuestreo, sin implicar que cada píxel o realización sea preciso. Las redes reducen variación y modifican estructura, pero pueden introducir sesgos sistemáticos. Las continuaciones regionales y espaciales atenúan parte de esos sesgos a costa de otros indicadores. Los resultados ilustran por qué una imagen más suave o un SSIM mayor no basta para certificar equivalencia muográfica.

El estudio queda limitado a un catálogo idealizado y previamente conocido, una sola fracción de entrada para las redes finales y una única geometría en generalización. Los pares comparten referencia finita; las semillas de continuación comparten pesos de partida. No se presentan las veinte realizaciones como réplicas geométricas independientes, ni se extrapolan estos promedios a volcanes reales. Tampoco se fija después de observar las tablas una tolerancia que convierta el resultado en aceptación.

**Conclusión:** se completaron y verificaron el diseño, la implementación, el entrenamiento y la evaluación descriptiva de la cGAN, junto con el control U-Net y los ajustes estudiados. Se logró mejora de similitud de imagen respecto de la entrada de baja estadística. La calidad comparable a alta estadística queda respaldada de forma parcial: persisten discrepancias regionales y no se demostró equivalencia física. El experimento y su documentación pueden darse por terminados con esta conclusión delimitada; no corresponde registrar cumplimiento científico pleno de la formulación amplia.

## 8. Continuidad hacia el OE3

Las [curvas descriptivas ya calculadas](../../objetivo-3/README.md) comparan fracciones de conteos existentes con las redes evaluadas al 5 %. Permiten reutilizar esta evidencia, pero no demuestran desempeño del modelo en otras fracciones de entrada. La relación nominal 1/f = 20 no es un factor de reducción alcanzable validado: representa submuestreo idealizado, sujeto a flujo y condiciones constantes. El tiempo de entrenamiento o de ejecución en GPU tampoco es tiempo de adquisición.

La siguiente actividad consiste en integrar y revisar editorialmente esta síntesis en el manuscrito de los autores, conservando las limitaciones, y desarrollar la conclusión del OE3 con las curvas disponibles y un criterio de calidad explícito. La integración editorial no requiere entrenamiento, inferencia ni simulación nuevos. Cualquier búsqueda de equivalencia física más amplia constituiría un estudio adicional, con criterios justificados y declarados antes de sus nuevas evaluaciones.

## 9. Reproducción y atribución

Las simulaciones, entrenamientos y entrega de predicciones corresponden a los estudiantes, según los registros enlazados. La auditoría independiente, la corrección numérica C2 y la presente consolidación documental se registran como actividades de revisión de la dirección. Se mantienen los originales y su procedencia.

La [guía de reproducción](README.md) identifica entradas, comandos y dependencias de las figuras; la [procedencia de figuras](figuras/procedencia-figuras.json) conserva índices y SHA-256 de las matrices utilizadas. Las tablas se transcriben programáticamente de C2, sin recalcular métricas ni ejecutar redes. La conclusión documental queda registrada en [CIERRE_OE2.md](../CIERRE_OE2.md).

# 3. Metodología

Este capítulo integra los procedimientos efectivamente ejecutados del conjunto sintético, el entrenamiento y la evaluación. Las simulaciones y los entrenamientos se atribuyen a los estudiantes; las revisiones locales contrastan integridad, predicciones o métricas según la evidencia indicada. No se presenta el recálculo de métricas como repetición del transporte o del entrenamiento.

## 3.1. Diseño del conjunto y observable

El estudio se desarrolló mediante simulación de transmisión de muones en diecinueve edificios cónicos idealizados, dieciocho con anomalías internas y uno homogéneo. Se emplearon seis vistas por geometría, separadas nominalmente 60°, y se registraron imágenes angulares de 256 × 256 píxeles. La representatividad es de configuraciones y mecanismos de contraste; no constituye muestreo estadístico de volcanes ni reproducción de un sitio real.

La [ficha de datos](../objetivo-1/FICHA_CONJUNTO_OE1.md) documenta Geant4 11.4.2, FTFP_BERT, GCC 14.2.0 y transporte solo de primarios. La fuente combina pesos angulares derivados de Guan con cuantiles de momento de EcoMug. Se inyecta junto al cono con margen angular de 5°. Los impactos nominales se muestrean en un panel de 1,2 m, mientras el plano computacional de registro tiene 600 m de lado. Estas dimensiones desempeñan funciones distintas y no describen un detector real de 600 m.

Se cuentan primarios que cruzan el plano con energía cinética superior a 3 GeV; el píxel se asigna por dirección final. El azimut relativo abarca −30° a +30° en 256 intervalos; la elevación emplea 256 centros entre 2° y 47° con su convención registrada. Cada vista utiliza 344.000.000 primarios en nueve bloques. La campaña contiene 1.026 bloques y 39.216.000.000 primarios; estos últimos no equivalen al número detectado.

La evaluación de borde utiliza quince regiones por vista y el criterio congelado de ±1 punto porcentual frente a la referencia ideal. La estadística de roca se describe mediante ROI de 4 × 4 píxeles, seleccionadas por columna nominal del cono homogéneo entre 30.000 y 100.000 g/cm². La meta es que al menos el 90 % de esas ROI alcance cien cuentas. Ambos controles tienen objetos diferentes: ninguno acredita por sí solo respuesta instrumental calibrada.

La variable de exposición convencional obedece a la Ec. (3.1):

$$
T_{\mathrm{conv}}=30\,\frac{N_{\mathrm{ventana}}}{36\,034\,069.911914065}.
\tag{3.1}
$$

Su etiqueta en días no representa una calibración temporal de un detector. La ejecución utiliza un número fijo de primarios y registra \`exposure_days=-1\`. La [receta](../objetivo-1/contratos/receta-operativa-siete-actividades.json) conserva las convenciones y huellas; no se reescriben sus indicadores históricos para cambiar el registro de producción.

## 3.2. Datos, particiones y representación

Se utiliza el conjunto corregido del OE1, cuya [ficha](../objetivo-1/FICHA_CONJUNTO_OE1.md) registra 19 escenarios idealizados y seis vistas por escenario. Cada imagen tiene 256 × 256 píxeles angulares. Las cuatro fracciones disponibles y las veinte realizaciones por fracción producen 9.120 pares. El entrenamiento y EF-01 utilizan exclusivamente f = 0,05; el complemento OE3-C1 evalúa después las cuatro fracciones con esos mismos pesos. Por tanto, no debe confundirse el tamaño del conjunto completo con el número empleado para entrenar cada modelo.

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

Las reservas se conservaron separadas en el entrenamiento corregido, pero las escenas del catálogo tuvieron exposición histórica durante el desarrollo previo. La [declaración de procedencia](../objetivo-2/entregas/2026-10-04-evaluacion-final-f05/PROCEDENCIA_RESERVAS.md) impide presentar esta evaluación como una validación confirmatoria sobre escenarios totalmente desconocidos.

La distribución 12/3/3 más una geometría de generalización es una adaptación respecto del reparto 70/15/15 mencionado en la propuesta. Se conserva para evitar redistribuir las reservas después de conocer resultados; no se presenta como reproducción exacta de aquel porcentaje.

## 3.3. Modelo y entrenamiento

El generador `unet_dc_5` implementa una U-Net de cinco niveles, con canales 64, 128, 256, 512 y 512. Cada bloque contiene dos convoluciones de 3 × 3, normalización por instancia y activación LeakyReLU. Cuatro operaciones de reducción espacial llevan de 256 × 256 a 16 × 16; el decodificador recupera la resolución mediante convoluciones transpuestas y conexiones de concatenación con el codificador. Una convolución final de 1 × 1 y una sigmoide producen una imagen de un canal. El generador tiene 20.543.809 parámetros. La [implementación](../objetivo-2/implementacion/models/unet_generator.py) constituye la especificación exacta.

La cGAN incorpora el crítico condicional `patch_critic_70`, que recibe la entrada junto con la imagen real o generada. Para cada muestra, el promedio espacial de sus puntuaciones define D(u,y). La [corrección v1](../objetivo-2/CORRECCIONES_V1.md) fija el cálculo coherente de la penalización de gradiente; no se usa la suma de parches como si fuera la puntuación media de una imagen.

Con $\widetilde y=\epsilon y+(1-\epsilon)G(u)$, la pérdida del crítico y la del generador original se escriben como

$$L_D=\mathbb E[D(u,G(u))]-\mathbb E[D(u,y)]+10\mathbb E[(\|\nabla_{\widetilde y}D(u,\widetilde y)\|_2-1)^2],$$

$$L_G=-\mathbb E[D(u,G(u))]+100L_1,\qquad L_1=\mathbb E[\|G(u)-y\|_1/P],$$

donde P es el número de píxeles y la esperanza representa el promedio sobre las muestras del lote. El control U-Net conserva el mismo generador y se entrena con 100 L1, sin componente adversario. La comparación permite examinar la contribución observada del entrenamiento adversario bajo estas configuraciones; no establece superioridad universal entre familias de redes.

El [piloto](../objetivo-2/PROTOCOLO_PILOTO_F05.md) fija lote cuatro, Adam con tasa 10⁻⁴ y parámetros (0; 0,9), cinco actualizaciones del crítico por actualización del generador y semilla 2026100301. Se conserva el conjunto de realizaciones, sin nuevas versiones de submuestreo durante el entrenamiento. La [entrega revisada](../objetivo-2/REVISION_PILOTO_C054225.md) registra parada temprana tras 12 épocas para U-Net y 13 para cGAN. En ambos casos se seleccionó el checkpoint de la época 5 por validación. Por tanto, «checkpoint de época 5» no significa que las ejecuciones originales duraran solo cinco épocas. La [verificación de pesos](../objetivo-2/REVISION_PESOS_PILOTO_F05.md) documenta la reproducción posterior de sus predicciones.

## 3.4. Continuaciones para conservar cuentas y reducir errores de borde

La evaluación geométrica de validación identificó que la mejora de SSIM y PSNR coexistía con sesgos regionales. Los ensayos posteriores abordaron ese problema conservando el generador y la normalización. La síntesis final incluye los modelos originales y las seis continuaciones del [ensayo E1](../objetivo-2/DISENO_BORDE_CGAN.md), sin seleccionar retrospectivamente una semilla ganadora.

En E1, C0 ya incluye la pérdida regional y C1 añade el término espacial de borde. Estas etiquetas no deben trasladarse a ensayos históricos donde C0 significaba otra configuración:

$$L_G^{C0}=L_{\mathrm{adv}}+100L_1+L_{\mathrm{reg}},\qquad L_G^{C1}=L_G^{C0}+0{,}629L_{\mathrm{borde}}.$$

Lreg promedia diferencias $|\log(1+\overline{\widehat c}_R)-\log(1+\overline c_R)|$, con igual peso entre familias de regiones no vacías, entre anomalías de una familia y entre imágenes del lote. La barra representa la media espacial dentro de la región; no se promedian logaritmos de cuentas por píxel. Su definición y exclusiones están en el [diseño regional](../objetivo-2/DISENO_AJUSTE_CUENTAS_F05.md) y la [función implementada](../objetivo-2/herramientas/perdida_cuentas_regionales.py). El término espacial se define como

$$L_{\mathrm{borde}}=\frac{1}{B}\sum_{b=1}^{B}\frac{\sum_{p\in R_b}|\widehat c_{bp}-c_{bp}|}{\sum_{p\in R_b}c_{bp}}.$$

Aquí B es el tamaño del lote y Rb la máscara geométrica de borde correspondiente a cada muestra. Se rechazan soportes menores de veinte píxeles, referencias vacías y valores no finitos. Las máscaras orientan la pérdida durante entrenamiento, pero no se convierten en entradas adicionales necesarias para generar una imagen.

El coeficiente 0,629 se fijó mediante un perfil de gradientes en doce lotes de entrenamiento, antes de comparar los nuevos resultados de validación. Es una decisión de escala de optimización, no una tolerancia física. B1, B2 y B3 emplean semillas 2026100411, 2026100412 y 2026100413. Cada pareja parte de los mismos pesos originales de generador y crítico, con optimizadores nuevos, tasa 10⁻⁵ y cinco épocas adicionales. Se conserva la quinta época de cada continuación según el diseño fijo. Las seis redes no son seis entrenamientos independientes desde cero.

Las comprobaciones de recuperación técnica y la [revisión de E1](../objetivo-2/REVISION_E1_804CE85.md) respaldan la ejecución. Recuperar exactamente un entrenamiento evita introducir una diferencia técnica entre variantes; por sí mismo no demuestra calidad física.

## 3.5. Evaluación final y trazabilidad

El [protocolo EF-01](../objetivo-2/PROTOCOLO_EVALUACION_FINAL_OE2.md) congela ocho modelos, cuatro geometrías y 480 entradas, generando 3.840 predicciones. La entrega estudiantil corresponde a `4e5945eefea1f799a4e2adee8858d98d604cf4ba`. Su integración y revisión C2 se publicaron en `1214307c525ace12c978ede5336fcf893abad7c7`; la síntesis presente parte de `08cdc0cb42ce0aa546aebfbf60fbfb89fb6081e3`.

SSIM y PSNR se calculan en la escala T con rango uno. SSIM utiliza ventana uniforme de 7 × 7, K1 = 0,01 y K2 = 0,03; PSNR = −10 log10(MSE) para ese rango. Los valores se promedian por geometría y luego con igual peso entre geometrías de una partición. No se mezclan prueba y generalización en una única cifra de desempeño.

Para una región R y realización k, el sesgo firmado y el error espacial relativo son

$$b_{Rk}=\frac{\sum_{p\in R}(\widehat c_{kp}-c_p)}{\sum_{p\in R}c_p},\qquad a_{Rk}=\frac{\sum_{p\in R}|\widehat c_{kp}-c_p|}{\sum_{p\in R}c_p}.$$

El indicador Q de una geometría promedia con igual peso dos componentes: el valor absoluto del sesgo medio entre realizaciones de roca y el correspondiente a las anomalías. Las anomalías se promedian dentro de cada vista, y después se promedian las vistas. En particular, el valor absoluto se aplica después de promediar sesgos entre realizaciones; Q no es la media de todos los errores absolutos por píxel. Un Q bajo puede coexistir con ruido alto. Q tampoco es un error de densidad ni un porcentaje de error de toda la imagen.

El contraste de anomalía compara su media de cuentas con controles de roca sin anomalía, a igual elevación y con longitudes de trayecto próximas. Se expresa como el cociente de medias menos uno y se evalúa su error absoluto frente a la referencia. La [corrección C2](../objetivo-2/REVISION_EVALUACION_FINAL_C2.md) resuelve empates numéricos en la selección de donantes mediante tolerancia geométrica de 10⁻⁸ m y guarda los índices exactos. Es una corrección posterior a la evaluación, no un protocolo prospectivo nuevo. No modifica pesos, imágenes, regiones, SSIM ni PSNR.

Se conservan 54 registros de contraste, de los cuales 48 son estimables geométricamente. El resumen C2 usa soporte común completo de todos los métodos: 30 combinaciones en prueba y 16 en generalización. Los casos restantes no se convierten en ceros ni se ocultan. Deben citarse las tablas corregidas; los contrastes de la entrega original permanecen como antecedente.

La auditoría verificó 83 archivos distribuidos, incluidas 32 matrices con 1.006.637.056 bytes. El recálculo reprodujo exactamente 4.320 filas de métricas de imagen; las 1.134 filas regionales coincidieron hasta 4,44 × 10⁻¹⁶. La inferencia independiente se comprobó sobre una muestra de 32 imágenes, con diferencia máxima CPU/GPU de 4,85 × 10⁻⁶. Esa muestra no debe describirse como una nueva inferencia de las 3.840 salidas: la reevaluación completa correspondió a las métricas sobre matrices conservadas. Los [resultados C2](../objetivo-2/evidencias/ef01-c2/resultados.json) enlazan la evidencia numérica vigente.


## 3.6. Evaluación multifracción y métricas locales

El complemento OE3-C1 utiliza los ocho pesos congelados en las cuatro fracciones F = {0,01; 0,05; 0,10; 0,50}. Reutiliza 3.840 predicciones al 5 % y añade 11.520: ocho modelos, tres fracciones y 480 imágenes. No se entrenan redes especializadas en cada fracción. Se estudia transferencia de los pesos entrenados al 5 % a otras estadísticas.

La entrada siempre es T(n/f), con la escala original. La inferencia conserva lote cuatro, modo evaluación, determinismo y TF32 desactivado según el [protocolo](../objetivo-3/PROTOCOLO_COMPLEMENTO_OE3.md). Las verificaciones técnicas de archivos y recuperación no constituyen umbrales científicos.

Para una anomalía A se conservan los cinco donantes por píxel y las ponderaciones C2. La media de fondo incluye esas ponderaciones; su desviación espacial se calcula sobre donantes únicos. Las desviaciones usan un grado de libertad de corrección. Los indicadores de la Ec. (3.2) distinguen intensidad local, contraste respecto de dispersión y cociente de cuentas:

$$
\mathrm{SNR}_A=\frac{\mu_A}{s_A},\qquad
\mathrm{CNR}_{A,B}=\frac{\mu_A-\mu_B}{s_B},\qquad
C_N=\frac{\mu_A}{\mu_B}-1.
\tag{3.2}
$$

SNR describe variación espacial, que puede contener estructura y ruido. CNR es firmado. Ninguno es una probabilidad de detección. Se exige el soporte geométrico fijado —al menos veinte píxeles emparejados y cobertura del 80 %— y se conservan motivos de no estimabilidad cuando un denominador se anula; no se agregan pseudocuentas.

Se registra además la media de D_k = μ_A,k − μ_B,k dividida por su desviación entre realizaciones, sin dividir por raíz de veinte. No se interpreta como estadístico de significación. La referencia única no aporta veinte réplicas para estimar esa dispersión.

La síntesis multifracción usa soportes comunes diferentes por métrica: treinta combinaciones anomalía/vista para SNR y treinta y dos para CNR/contraste. Los errores absolutos se calculan por realización antes de promediar; después se promedian casos dentro de geometría y geometrías con igual peso por partición. Estos valores no se mezclan con el contraste C2 anterior, que empleaba otros soportes y agregación. La inversión de signo exige producto estrictamente negativo con el contraste de referencia; una referencia próxima a cero hace sensible esta clasificación.

## 3.7. Criterio de reducción de conteos

La propuesta compromete umbrales de SSIM/PSNR, pero no fija cifras operativas. El complemento toma la entrada sin red al 50 % como referente, con umbrales por vista definidos antes de las inferencias nuevas. La decisión es posterior a los resultados históricos; no se presenta como predefinición original ni como tolerancia geofísica.

Para cada modelo m y partición S, la Ec. (3.3) define las fracciones aceptadas:

$$
\mathcal A_{m,S}=\{f\in F:\ \forall v\in S,\
\overline{\mathrm{SSIM}}_{m,f,v}\ge\tau_{\mathrm{SSIM},v}
\ \land\
\overline{\mathrm{PSNR}}_{m,f,v}\ge\tau_{\mathrm{PSNR},v}\}.
\tag{3.3}
$$

Las barras representan medias de veinte realizaciones; los umbrales se calculan frente a la referencia completa. La tolerancia aritmética de 10⁻¹² no es un margen de calidad. Cuando el conjunto no es vacío, se aplica la Ec. (3.4):

$$
f_{\min,m,S}=\min\mathcal A_{m,S},\qquad
R_{m,S}=\frac{0.50}{f_{\min,m,S}}.
\tag{3.4}
$$

R sería una razón de exposiciones bajo proporcionalidad de conteos y tiempo. Si el conjunto es vacío, ambas cantidades quedan no determinadas, no cero ni uno. Se examinan todas las fracciones sin suponer monotonía ni interpolar. La razón 1/f es nominal respecto de todos los eventos y no implica equivalencia de calidad.

## 3.8. Opacidad nominal y límites de interpretación

La Ec. (3.5) define opacidad y su versión nominal para un trayecto recto de longitud L con una anomalía de longitud ℓ:

$$
X=\int\rho(l)\,dl,\qquad
X_{\mathrm{nom}}=100[\rho_r(L-\ell)+\rho_a\ell].
\tag{3.5}
$$

El factor cien convierte metros en centímetros cuando las densidades están en g/cm³. X se expresa en g/cm², mientras C_N es adimensional. El diagnóstico usa rayos centrales y el catálogo; no invierte las predicciones ni sigue trayectorias dispersadas de partículas.

La diferencia frente al control separa contribución de densidad y de longitud. Se conservan cuarenta y ocho filas elegibles de cincuenta y cuatro, con seis filas advertidas para la anomalía 2 de geo-gen-01: el catálogo indica 0,048 g/cm³ y el constructor conservado sustituye densidades inferiores a 0,05 por G4_AIR. No se afirma que la densidad nominal sea la efectiva de producción. El [diagnóstico](../objetivo-3/OPACIDAD_NOMINAL_Y_ALCANCE.md) documenta esta limitación, sin atribuirle causalmente los errores de las redes.

## 3.9. Control documental

Las huellas vinculan datos, pesos, predicciones y configuraciones. El conjunto de referencia, sus exclusiones y las variantes desfavorables se conservan. La nomenclatura común se recoge en [NOMENCLATURA.md](NOMENCLATURA.md); los resultados se presentan en el [capítulo 4](04_RESULTADOS.md). La reproducibilidad técnica se distingue de la validez física y de la aprobación académica.

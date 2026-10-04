# Complemento experimental OE3-C1: fracciones de entrada y métricas locales

2026-10-04, Colombia. Diseño posterior a EF-01-C2 y a las curvas descriptivas, preparado por la dirección. Se conservan los resultados conocidos y se declara esa exposición; el complemento no es una validación confirmatoria independiente. No se redacta el informe final ni se inicia entrenamiento.

## 1. Pregunta y alcance

Se completa la evaluación de los ocho modelos congelados cuando reciben 1 %, 5 %, 10 % y 50 % de los conteos existentes. Se pregunta cómo cambia su desempeño, si alguna fracción alcanza un referente de calidad definido para este complemento y qué ocurre con las anomalías. La evaluación al 5 % se reutiliza; las otras fracciones requieren nuevas inferencias. Se mantienen U-Net y cGAN originales y las seis continuaciones B1–B3, sin elegir la semilla con mejor resultado previo.

Las redes fueron entrenadas/ajustadas al 5 %. Evaluarlas al 1 %, 10 % y 50 % estudia transferencia a otras estadísticas de entrada; no equivale a entrenar una red para cada fracción. Un resultado desfavorable también debe entregarse. No hay búsqueda adicional de pesos, épocas, pérdidas ni normalización. La [revisión de propuesta](../docs/REVISION_PROPUESTA_APROBADA.md) delimita los compromisos P02, P05 y P06 que motivan este trabajo.

## 2. Contrato y tamaño

| Elemento | Decisión fijada |
|---|---|
| Datos | Los cuatro escenarios de prueba/generalización del contrato EF-01, seis vistas y veinte realizaciones por vista |
| Pesos | Los ocho SHA-256 de `objetivo-2/configuraciones/evaluacion-final-v1.json` |
| Entrada | T(n/f), con la escala de entrenamiento s = 8,239329427901795; sin volver a estimarla |
| Normalización | T(c) = log(1+c)/(s+log(1+c)); la salida se invierte antes de evaluar cuentas |
| Fracciones | 0,01; 0,05; 0,10; 0,50, en sus índices originales 3, 2, 1, 0 |
| Inferencia | Modo evaluación, lote 4, determinismo activado, TF32 desactivado |
| Reutilización | 3.840 predicciones al 5 %, verificadas mediante recibos e identidades originales |
| Trabajo nuevo | 11.520 predicciones: 8 modelos × 3 fracciones × 480 imágenes |
| Volumen | 96 NPY nuevos de 120 × 256 × 256 float32; aproximadamente 3,02 GB decimales de matrices. Además se conservan unos 1,01 GB del bloque 5 % |
| Separación | Prueba: tres geometrías; generalización: una. No se agrupan realizaciones como geometrías independientes |

La [configuración ejecutable](configuraciones/complemento-v1.json) fija fuentes, fracciones, modelos, umbrales por vista, registro C2 y tolerancia técnica. Las modificaciones de código o configuración invalidan los recibos del complemento; no se mezclan salidas de versiones diferentes. No se alteran el ejecutor EF-01 ni los datos originales.

## 3. Calidad de imagen: criterio operativo y límites

La propuesta exige umbrales predefinidos, pero no aporta valores numéricos de aceptación. No se importan 0,80, 0,90 ni un PSNR arbitrario como condición supuestamente aprobada. Tampoco se toma de otro problema un factor de reducción publicado.

**Referente operativo principal:** entrada sin red al 50 %, el mayor nivel disponible distinto de la referencia completa. Para cada geometría g y vista v, se fijan tau_SSIM(g,v) y tau_PSNR(g,v) como los promedios de sus veinte realizaciones frente a la referencia completa. Los 48 valores quedan guardados en la configuración antes de ejecutar las nuevas inferencias. Proceden de `objetivo-3/evidencias/curvas-v1/imagenes.csv`; su huella se conserva. Esta regla compara con un nivel alto existente y evita comparar la referencia consigo misma, cuyo PSNR sería infinito.

Una fracción de entrada satisface **este benchmark de imagen** si el modelo alcanza simultáneamente ambos umbrales en todas las vistas de la partición. Se usa 10⁻¹² solo como tolerancia aritmética. Se evalúan todas las fracciones: no se detiene el análisis tras un fallo ni se supone monotonía. Se informa el mínimo de la rejilla que satisface la regla por modelo y partición; si no existe, se devuelve nulo. Se conservan todas las comparaciones, sin seleccionar automáticamente un modelo ganador.

El factor asociado a ese benchmark es R = 0,50/f_min, sujeto a proporcionalidad entre conteos y exposición. Si f_min = 0,50, R = 1 y no hay reducción. El valor 1/f_min es únicamente una razón nominal frente al total de eventos, y no una equivalencia demostrada con su calidad. Los resultados de prueba y generalización se mantienen separados; una afirmación sobre todo el catálogo requiere una fracción que satisfaga la regla en ambas particiones, sin asumir que sus mínimos implican monotonía.

**Origen de la decisión:** este benchmark se define después de conocer f05 y las curvas sin red. Está fijado antes de las nuevas inferencias, pero no fue el umbral original de la propuesta ni acredita por sí mismo calidad equivalente a la referencia completa. La elección del 50 % es una convención operacional de esta campaña, no una tolerancia geofísica validada. OE3-P02 mantiene alcance parcial para aceptación científica amplia. La comparación secundaria frente al 10 % ya publicada se conserva; no sustituye al referente principal cuando este sea desfavorable.

## 4. SNR local, CNR y contraste

Se conservan las regiones geométricas y los índices de donantes de C2. Cada píxel de anomalía tiene cinco controles a la misma elevación y con longitud geométrica próxima; los casos requieren al menos veinte píxeles emparejados y cobertura mínima del 80 %. Se conservan seis registros geométricamente insuficientes y cualquier exclusión adicional por denominador nulo. No se añaden pseudocuentas ni se transforman datos no estimables en ceros.

Para cada realización, A contiene los píxeles de anomalía emparejados. La media de fondo mu_B se calcula con los cinco donantes de cada objetivo, manteniendo las ponderaciones de C2. Para estimar la dispersión del fondo se usan los donantes **únicos**, evitando contar repetidamente un mismo píxel como si fueran observaciones distintas. Las desviaciones espaciales s_A y s_B usan ddof = 1.

Se fijan tres indicadores diferentes:

$$\mathrm{SNR}_{A}=\frac{\mu_A}{s_A},\qquad \mathrm{CNR}_{A,B}=\frac{\mu_A-\mu_B}{s_B},\qquad C_N=\frac{\mu_A}{\mu_B}-1.$$

SNR_A describe intensidad relativa a dispersión **espacial dentro de la anomalía**. CNR es firmado y describe contraste relativo a dispersión del fondo. C_N reproduce el contraste de cuentas de C2. SNR no se denomina CNR ni se interpreta como probabilidad de detección. La dispersión espacial puede contener estructura real además de ruido; estas convenciones se declaran expresamente y no se atribuyen como fórmulas prescritas por la propuesta o por O'Donnell.

Además, para D_k = mu_A,k − mu_B,k se registra media(D_k)/sd(D_k) entre las veinte realizaciones, sin dividir por raíz de veinte. Este indicador repetido no es el SNR espacial ni un estadístico de significación. Para la referencia única es no estimable; no se fabrican veinte copias para estimar ruido. Si la desviación es cero, se guarda nulo y el motivo, no infinito ni éxito automático.

Las tres métricas se calculan para entradas, las ocho redes y referencia de alta estadística. Se publican tablas completas por realización y soportes comunes por métrica. No se seleccionan regiones a partir del error o signo favorable. Las curvas de SNR/CNR deben leerse con errores de contraste, inversiones de signo, Q y error espacial: una salida constante o suavizada no se declara mejor por un cociente aislado.

La [implementación de métricas](herramientas/metricas_locales_oe3.py) conserva la definición exacta. El complemento registra resultados descriptivos; no incorpora un umbral universal de detectabilidad ni certifica conservación física por superar un SNR arbitrario.

## 5. Qué significa opacidad en este complemento

La opacidad física es X = integral rho(l) dl, habitualmente expresada en g/cm². El contraste C_N de las imágenes es un cociente de cuentas; no tiene esas unidades ni equivale automáticamente a X. A geometría y aceptación comparables, la transmisión responde a la cantidad de materia atravesada, pero una inversión cuantitativa requiere un modelo calibrado de flujo/transmisión, energía y material.

Por tanto, se denomina **contraste de transmisión en cuentas, indicador sustituto para estudiar visibilidad de anomalías**. Se conserva su referencia sintética y se evalúan sus errores, sin presentar una imagen de opacidad reconstruida. La correspondencia cualitativa no demuestra proporcionalidad ni exactitud de densidad. Si el cierre académico exige contraste cuantitativo de opacidad, hará falta una calibración explícita adicional: OE3-P06 no se da por resuelto en esa parte mediante un cambio de nombre.

## 6. Verificación, ejecución y entrega

La preparación local incluye pruebas analíticas de cocientes y soporte, pruebas de exportación/reanudación/corrupción con una red identidad sintética, y una prueba de inferencia real con cGAN original en CPU. Esta prueba real repite cuatro imágenes al 5 %, comprueba igualdad bit a bit de dos inferencias continuas y compara con la entrega conservada; verifica además forma, finitud e inversión de cuatro imágenes por cada fracción nueva. No calcula métricas científicas de esas doce salidas técnicas.

El límite 10⁻⁴ de diferencia máxima de píxel es una tolerancia técnica CPU/GPU de esta comprobación, no el criterio de calidad de imagen. Cada modelo requiere su propio `smoke` en el mismo entorno antes de las inferencias GPU completas. Un fallo técnico detiene ese modelo; un resultado científico desfavorable no se utiliza para interrumpir la evaluación.

La [guía de ejecución](INSTRUCCIONES_COMPLEMENTO_OE3.md) contiene comandos y entrega. Las fracciones nuevas se guardan en carpetas separadas. Se verifican huellas de pesos, datos, registro C2 y salidas; se rechazan identidades incompatibles, recibos incompletos y corrupción. Repetir un comando reutiliza archivos completos idénticos. La evaluación conjunta exige todos los modelos y fracciones.

## 7. Estado y atribución

Este protocolo y sus verificaciones locales corresponden a preparación de la dirección. Las simulaciones y entrenamientos originales siguen atribuidos a los estudiantes. Se registra qué parte se ejecutó localmente en [verificación](VERIFICACION_COMPLEMENTO_OE3.md). No se afirma que la inferencia multifracción completa ni CUDA estén verificadas antes de recibirlas.

OE3-P05 queda preparado, pendiente de las nuevas inferencias y su revisión. OE3-P06 incorpora definición operativa y evaluación local al 5 %; las demás fracciones y la interpretación cuantitativa de opacidad permanecen delimitadas. OE3-P03 depende de la evaluación completa. OE3-P04, informe final, continúa aplazado por indicación de la dirección.

## Referencias comprobadas y relación con las decisiones

- [O'Donnell et al., 2025, artículo](https://arxiv.org/html/2502.02624v2): compara calidad a distintos tiempos de muestreo y estudia estructuras mediante un modelo de segmentación. Es un antecedente en tomografía por dispersión de infraestructura; sus resultados no fijan umbrales universales para estas imágenes de transmisión. No se le atribuyen las convenciones SNR/CNR de este protocolo.
- [Jourde et al., 2016, experimento de calibración](https://www.nature.com/articles/srep23054): distingue opacidad, flujo medido y condiciones que afectan la interpretación temporal. Fundamenta mantener separadas cuentas y opacidad, sin trasladar sus cifras de calibración a este catálogo.
- Propuesta aprobada: `Plan_trabajo_grado.pdf`, SHA-256 `7404530659aab451897ac1eb0be05c8fe7ce9b5c96b0131b18fc638684d51084`, páginas impresas 24 y 27. [Revisión directa](../docs/REVISION_PROPUESTA_APROBADA.md).

# Síntesis de resultados del objetivo específico 1

2026-10-03. Texto preparado para su incorporación y revisión en el informe académico. Se limita al conjunto idealizado del OE1 y a la evidencia verificada; no incluye entrenamiento ni evaluación de redes.

## Producto obtenido y relación con el objetivo

Se generó un conjunto de imágenes sintéticas de muografía por transmisión mediante simulación Monte Carlo en escenarios volcánicos idealizados. El catálogo contiene 19 geometrías cónicas, 18 con anomalías internas y una homogénea. Cada geometría se observó desde seis direcciones, con lo que se obtuvieron 114 referencias de 256 × 256 píxeles. Cada píxel registra el número de muones primarios que alcanza el plano computacional con energía cinética superior a 3 GeV dentro de un intervalo de dirección final.

La campaña utilizó 344 millones de primarios por vista, distribuidos en 1.026 bloques, para un total de 39.216 millones. Las referencias se acompañan de realizaciones de menor conteo obtenidas mediante adelgazamiento binomial con fracciones 0,50; 0,10; 0,05 y 0,01. Las veinte realizaciones por fracción producen 80 pares por referencia y 9.120 pares en total. Las particiones se conservan por geometría, evitando que las variantes de una misma referencia aparezcan en entrenamiento y evaluación.

Estos componentes respaldan la obtención del producto solicitado: escenarios sintéticos, transporte Monte Carlo, imágenes por transmisión y diferentes estadísticas de conteo. La representatividad se entiende dentro de una familia de edificios cónicos con heterogeneidades idealizadas; no se afirma que las geometrías reproduzcan un volcán concreto o todos los escenarios de exploración.

## Trazabilidad y reproducibilidad

Los registros de SC3 respaldan la finalización de las 1.026 filas de simulación. Se registraron tres trabajos fallidos que posteriormente se completaron; no se duplicaron filas completadas. La campaña transcurrió entre el 2 de octubre a las 18:10:27 y el 3 de octubre de 2026 a las 09:48:49. La suma de recursos asignados, incluyendo fallos, fue de 2.356,73 hilo-horas; esta magnitud no debe confundirse con horas de reloj ni con núcleos físicos.

Se verificaron 477 huellas de archivos de fusión y exportación. Las 114 imágenes conservan exactamente los conteos y coordenadas de los histogramas originales. La evaluación se reprodujo localmente desde los píxeles. Asimismo, se regeneraron en memoria los 9.120 pares con NumPy 2.4.4 y se comprobó coincidencia de las 342 huellas de contenido publicadas. La verificación reproduce el posproceso y la reducción de conteos; no constituye una segunda ejecución independiente de Geant4.

## Evaluación de calidad

Se evaluaron quince regiones de borde por vista frente a la referencia ideal de fuente, mediante intervalos binomiales y corrección simultánea para las 114 vistas. Las 1.710 regiones cumplieron el criterio de ±1 punto porcentual con el intervalo completo dentro de la tolerancia. El mayor extremo absoluto fue de aproximadamente 0,933 puntos porcentuales. El contraste examina la respuesta relativa al modelo ideal y no separa por sí mismo efectos de aire, dispersión o muestreo.

Para describir la estadística en roca se seleccionaron regiones de 4 × 4 píxeles usando la columna nominal del cono homogéneo entre 30.000 y 100.000 g/cm². Las anomalías forman parte del transporte, aunque no de la selección de estas regiones. Globalmente, 20.713 de 21.816 regiones (94,944 %) alcanzaron 100 cuentas. La meta descriptiva de al menos 90 % de regiones con ese conteo se alcanzó en 107 de las 114 vistas.

Las siete vistas restantes presentaron valores entre 89,19 % y 89,81 %. Conforme al acuerdo previo, se conservaron sin aumentar el presupuesto, descartar imágenes ni modificar el criterio. El porcentaje global no sustituye la evaluación por vista. Tampoco permite afirmar una precisión del 10 % por píxel: la referencia de 100 cuentas se aplica a regiones agregadas y solo caracteriza aproximadamente el ruido de conteo, no la incertidumbre de modelo.

## Figuras para el informe

![Ejemplos de referencias](figuras/cierre-2026-10-03/01-referencias.png)

**Figura 1.** Ejemplos de seis referencias de la campaña, elegidos para mostrar diferentes geometrías y casos bajo la meta de roca; no constituyen una muestra estadística representativa. Se muestran conteos por píxel sin suavizado, sobre coordenadas angulares y con una escala de color común logarítmica, lineal entre cero y una cuenta. Las siluetas no son mapas de densidad ni fotografías de volcanes. [PDF](figuras/cierre-2026-10-03/01-referencias.pdf).

![Referencia y realizaciones de menor conteo](figuras/cierre-2026-10-03/02-pares.png)

**Figura 2.** Referencia de `geo-train-06`, vista 3, y primera realización de cada fracción de adelgazamiento, con semilla maestra 20260805. Los paneles comparten escala de color y muestran conteos sin renormalizar por la fracción. Las realizaciones se condicionan a la misma referencia finita; no son nuevas corridas independientes de transporte. [PDF](figuras/cierre-2026-10-03/02-pares.pdf).

![Calidad de roca por vista y distribución global](figuras/cierre-2026-10-03/03-calidad-roca.png)

**Figura 3.** Izquierda: porcentaje de ROI que alcanza 100 cuentas, por geometría y vista; los asteriscos identifican las siete vistas bajo la meta del 90 %. Derecha: proporción global de ROI que alcanza cada umbral; el eje horizontal se limita al percentil 99,5 de los conteos para facilitar la lectura. El valor 94,94 % utiliza todas las 21.816 ROI, ponderadas por su número, sin sustituir los indicadores individuales. [PDF](figuras/cierre-2026-10-03/03-calidad-roca.pdf).

Las figuras se generan desde los datos mediante [figuras_cierre_oe1.py](../herramientas/figuras_cierre_oe1.py), con huellas de origen y métricas en [datos-figuras.json](figuras/cierre-2026-10-03/datos-figuras.json).

## Limitaciones y conclusión acotada

La fuente híbrida y su extensión angular son hipótesis del conjunto. La simulación conserva únicamente primarios; no incluye una respuesta instrumental completa, secundarios ni fondo experimental. El plano de registro es computacional y no equivale a un detector físico de 1,2 m. La exposición etiquetada es convencional; no representa duración calibrada. La referencia ideal de cielo no incluye transporte en aire y no convierte automáticamente una normalización en transmisión física calibrada.

Las referencias de conteo alto mantienen ruido, y las realizaciones reducidas comparten esa referencia. La representatividad geométrica y física debe justificarse dentro del alcance idealizado, sin extrapolar los controles a equivalencia experimental. La conversión `dataset-v2` y el reentrenamiento de modelos no se evalúan aquí.

La evidencia disponible respalda la obtención y reproducción técnica de las 114 referencias y los 9.120 pares bajo el alcance adoptado. No se identifica una necesidad de repetir la campaña para completar estas verificaciones. La [copia de distribución](REVISION_DISTRIBUCION_DRIVE.md) ya se verificó de forma independiente. Quedan la incorporación de esta síntesis al informe y la revisión académica de la representatividad. El cierre formal del objetivo corresponde a esa valoración y no a una declaración automática del software.

Fuentes internas: [ficha del conjunto](FICHA_CONJUNTO_OE1.md), [revisión de datos f395570](REVISION_DATOS_F395570.md), [revisión de ejecución e037d09](REVISION_CAMPANA_E037D09.md), [definición adoptada y criterios de cierre](DEFINICION_PRODUCTO_OE1.md).

## Incorporación al manuscrito y revisión pendiente

En la revisión local del 2026-10-03 se encontró una plantilla `Informe_Final_Muografia`: metodología contiene guías de redacción y los capítulos de resultados y conclusiones están reservados, sin contenido. No se identificó un manuscrito actualizado en la entrega `cb57145`. Por tanto, este texto es material preparado para incorporación; no acredita que el informe de estudiantes ya esté actualizado ni permite dictaminar su coherencia integral.

| Sección del informe | Incorporación requerida | Comprobación de la revisión académica |
|---|---|---|
| Metodología del OE1 | Geometrías, fuente, observable, receta final, 344 M por vista, formación angular y adelgazamiento binomial según la ficha. | Distinguir 19 geometrías, 114 vistas y 9.120 pares; especificar energía cinética >3 GeV y plano computacional. |
| Resultados del OE1 | Cifras y tres figuras de esta síntesis, con referencias a los inventarios. | Identificar la campaña de octubre; no atribuirle conteos, configuraciones o métricas de la campaña histórica. |
| Discusión | Justificación de la familia de escenarios, ruido de las referencias, dependencia entre realizaciones y siete vistas bajo la meta descriptiva. | Explicar qué representa el conjunto y qué no permite inferir; no presentar el 94,944 % global como cumplimiento de todas las vistas. |
| Conclusión del OE1 | Obtención del conjunto sintético con distintos niveles de conteo bajo el alcance adoptado. | No afirmar equivalencia instrumental, tiempos físicos calibrados, generalización experimental ni reconstrucción de densidad demostrada por estas pruebas. |
| Reproducibilidad | Commit de la entrega, enlace de distribución, versiones, semillas, comandos y procedimiento de integridad. | Citar la versión efectivamente utilizada; distinguir transporte realizado en SC3 de posproceso reproducido localmente. |

La próxima entrega académica debe identificar una versión concreta del manuscrito y sus secciones modificadas. La revisión posterior contrastará esas secciones con esta síntesis, la ficha y los criterios A-01 a A-08. Esta tarea no requiere por sí misma más transporte en SC3 ni autoriza iniciar OE2/OE3.

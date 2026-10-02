# Referencias y diseño estadístico preparados localmente

2026-10-02. Cálculos y herramientas terminados con los datos disponibles; no hubo nuevas corridas Geant4. [Resultados reproducibles](evidencias/preparacion-siete-actividades/resumen.json), [herramienta de reproducción](../herramientas/analizar_preparacion_angular.py).

## Cielo: resultado del análisis existente

Se analizaron c01 (20 millones, margen 0°) y c02 (2 millones, margen 5°), ambas con corte de 3 GeV. La nueva referencia ideal de fuente tiene probabilidad de superar ese corte entre 0,4584 y 0,9588 según elevación. Esto es probabilidad inicial, no eficiencia de transmisión por roca.

Las 28 filas sin cielo observado incluyen 7.122 píxeles de roca. Manteniendo fija la eficiencia observada y cambiando solamente el denominador extrapolado por el tabulado, la razón nueva/anterior en esos píxeles es:

| Corrida | Mínimo | Mediana | Máximo |
|---|---:|---:|---:|
| c01 | 0,9538 | 0,9538 | 1,0117 |
| c02 | 0,9203 | 0,9203 | 0,9761 |

Es una **sensibilidad al denominador**, no una corrección física demostrada. La diferencia entre corridas también incluye ruido de la referencia observada. El producto diagnóstico nuevo C/(N·p_ideal) utiliza además la probabilidad nominal esperada, no el histograma inicial fluctuante de cada píxel. Sus matrices están guardadas como derivados separados; las imágenes recibidas no se modificaron.

## Bordes: definición que puede evaluarse sin extrapolar filas

Se fijan diez columnas extremas (cinco a cada lado, usando cielo de 30–42°), cinco filas superiores y un interior de columnas 20–235 en cielo de 30–42°. El cielo excluye roca y deja un grado por encima de la silueta. Las máscaras usan geometría y direcciones centrales; no son una simulación de aceptación.

En cada región r se calcula e_r = [C_r/N − p_ideal,r] / p_nominal,r. El contraste es e_borde − e_interior, con tolerancia ±0,01, es decir, **±1 punto porcentual de probabilidad seleccionada por inyección nominal**. La resta de p_ideal ajusta el cambio de espectro con elevación. El contraste mide no uniformidad respecto a esa referencia ideal; no aísla por sí solo la causa entre aire, migración o muestreo.

Cada C_r/N se trata como proporción binomial de N historias independientes con máximo una llegada registrada por primario. Se construyen intervalos Clopper–Pearson para las 16 probabilidades, con Bonferroni, y se restan sus extremos para acotar cada contraste. No se supone independencia entre regiones: se usa una cota simultánea conservadora. Si el registro permitiera múltiples cruces o pesos por primario habría que cambiar el modelo.

La evaluación de los archivos existentes da:

| Corrida | Dentro de tolerancia con intervalo completo | Inconclusas | Intervalo completamente fuera |
|---|---:|---:|---:|
| c01 | 3 | 12 | 0 |
| c02 | 0 | 15 | 0 |

**Ninguna corrida permite cerrar todos los bordes.** «Inconcluso» no significa que el borde sea correcto ni que esté mal. Son diagnósticos retrospectivos; el criterio se definió después de recibirlos y es distinto del anterior ajuste lineal. No comparar sus máximos como si fueran la misma magnitud ni seleccionar la regla que dé el resultado más favorable.

Herramientas: [evaluador por vista](../herramientas/evaluar_bordes_angular.py), [evaluador del piloto completo](../herramientas/evaluar_piloto_angular.py). El segundo verifica máscaras, geometría, tablas, receta, N y semillas contra el diseño antes de emitir resultados.

## Piloto de seis vistas: propuesta calculada, no orden de ejecución

[Diseño y máscaras congelados](evidencias/piloto-propuesto-siete-actividades/diseno-piloto.json), [manifiesto](evidencias/piloto-propuesto-siete-actividades/manifiesto-piloto-propuesto.csv). Se propone geo-train-06, con anomalías, seis vistas, margen 5° y E_cin >3 GeV. El error familiar es 5 % para las seis vistas: cada evaluación usa α=0,05/6, y luego reparte entre sus 16 probabilidades.

El diseño conservador, alrededor de una diferencia verdadera cero y con potencia conjunta aproximada objetivo 80 %, da **211 millones de primarios por vista**, divididos en seis bloques de unos 35,17 millones. Total: **1.266 millones, 36 bloques**. A la tasa de c01 serían unas **187,3 horas-núcleo**, no horas de reloj. No es una medición del coste de geo-train-06; se conserva esa limitación en el presupuesto.

El tamaño proviene de una aproximación normal con cota de Cauchy para la desviación del contraste. No es el mínimo posible ni una garantía de potencia bajo otro modelo. Se eligió una regla conservadora y auditable; si se desea reducir su coste, se debe revisar y congelar otro diseño antes de ejecutar, no reducirlo después de ver resultados. El manifiesto previo k=1 de 52,7 millones/vista no demuestra automáticamente la potencia de este nuevo criterio.

Se evalúa una sola vez al completar el N fijado. No ampliar hasta que «pase». Una diferencia verdadera cercana al umbral puede seguir dando inconclusión con muchos eventos. El piloto también entrega mediana, percentil 10 y fracción de ROI de roca de 4×4 con al menos 100 cuentas. La selección de ROI usa columna **nominal del cono homogéneo**, con marcha de rayos de 2 m, sin anomalías en la máscara; las anomalías sí están en el transporte. No confundir esa etiqueta con opacidad real de la geometría heterogénea. Hay 244 ROI seleccionadas por vista. Sus conteos servirán para dimensionar producción con la receta real; no se sustituye esa comprobación por el factor histórico 0,124 ni se declara P1 aprobada si los bordes pasan.

## C3: comparación espacial opcional, correctamente dimensionada

Si se exige equivalencia con el panel, comparar dos brazos independientes bajo la misma ley angular y definición de inyección: C para fuente nominal sobre el panel/plano grande; D para fuente amplia/panel central. La razón es R=(D/N_G)/(C/N_P)/(A_P/A_G). Deben justificarse área proyectada/normal y superficie de fuente; el área por sí sola no prueba equivalencia.

Se fijan **cuatro bandas** de columna: 10–30, 30–60, 60–100 y 100–200 mil g/cm². El diseño de referencia conserva la ventana angular completa; no descuenta el coste usando el recorte angular de tres bandas y margen no validado. El tamaño espacial g es un parámetro a justificar, no queda demostrado por contener el 99 % de las salidas de otra fuente. C3-a no se ordena automáticamente: primero se debe argumentar qué dominio haría válida la comparación.

El [evaluador C3](../herramientas/estadistica_control_angular.py) usa intervalos binomiales para cada brazo, con Bonferroni sobre las ocho probabilidades, y forma límites de la razón. Esto corresponde al N fijo de la simulación y evita presentar como exacta una aproximación Poisson. Cero cuentas produce límites abiertos/inconclusión; no se añade una pseudocuenta para forzar equivalencia.

Decisión fijada: los cuatro intervalos deben quedar enteros en [0,95;1,05]. Si alguno queda enteramente fuera, hay evidencia contra esa tolerancia en la comparación definida; si la cruza, es inconclusa. N se fija antes de correr; llegar a una cantidad de cuentas detectadas no es una regla de parada autorizada.

Para igual cantidad esperada de cuentas en ambos brazos, una planificación conservadora con potencia conjunta aproximada 80 % cerca de R=1 da **28.527 cuentas esperadas por brazo y por banda**. Es mayor que un cálculo de anchura aislada de 2.496 o 4.991 cuentas: ahora se incluyen la potencia y el método simultáneo conservador elegido. No es un mínimo universal; un método más eficiente requeriría su propio diseño y verificación.

Se comprobó la aproximación mediante 20.000 experimentos binomiales sintéticos de la banda limitante: potencia de una banda 0,9652; cota conjunta por unión usando el límite inferior de la incertidumbre Monte Carlo, aproximadamente 0,850. **No son simulaciones de muones ni evidencia de equivalencia física.** Se asumen la tasa de c01, R=1 y el mismo modelo de conteo.

| Semilado de fuente g | Horas-núcleo ilustrativas, ambos brazos, ventana completa |
|---|---:|
| 5 m | 3.670 |
| 10 m | 14.523 |
| 20 m | 57.934 |
| 50 m | 361.814 |

Estas cifras usan tasas de c01 **sin margen** y una tasa de transporte media; no son un presupuesto de la receta final. Muestran por qué no se debe lanzar C3 con las 1.600 cuentas ni prometer el coste anterior. Si C3 se elige, actualizar tasas y dominio, fijar presupuesto y código de fuente amplia antes de correr. El conjunto idealizado no necesita asumir ese gasto para respaldar una equivalencia instrumental que no afirma.

## Fuentes del método y reproducción

Se usan [límites binomiales exactos de NIST](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm), la [desigualdad de Bonferroni](https://www.itl.nist.gov/div898/handbook/prc/section4/prc463.htm) y [cuantiles beta de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html). Las pruebas comparan límites con la inversión independiente de `binomtest` y verifican cobertura para ejemplos de N pequeño. No se requiere un modelo de detector para esos cálculos estadísticos.

Para reproducir, usar `analizar_preparacion_angular.py` con la entrega congelada, las tablas v1 y los originales de la réplica; después `preparar_piloto_angular.py` con geo-train-06 y el mismo `comun.py`. Todos los destinos deben ser nuevos. Los JSON conservan hashes y entorno. Los comandos completos están en la guía operativa.

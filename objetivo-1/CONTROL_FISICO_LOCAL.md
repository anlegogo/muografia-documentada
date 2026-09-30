# Control independiente de geometría y materiales — 29 de septiembre de 2026

## Alcance

Se realizó una integración numérica independiente del volumen de intersección conducto/elipsoide de `geo-train-06`. Usa el catálogo recibido, sin ejecutar el programa de los estudiantes ni Geant4. Es un control de la parte geométrica de la validación física; no mide el efecto de la corrección sobre los conteos.

## Método y resultados

Se integra en XY la longitud vertical común a ambos sólidos, con cuadratura adaptativa, en lugar de estimar el volumen por muestreo Monte Carlo. Ambas anomalías de este caso están contenidas en el edificio. Se repitió con dos tolerancias; los resultados difieren en 0,001835 m³. Esa estabilidad no es una cota rigurosa de error total.

| Magnitud | Cálculo independiente | Valor entregado | Interpretación |
|---|---|---|---|
| Intersección | 83.663,703 m³ | 83.641,9 ± 44,7 m³ (error estándar reportado) | Diferencia de 21,803 m³, aproximadamente 0,49 errores estándar reportados. Compatible. |
| Conducto completo | 471.050,402 m³ | — | Fórmula exacta del cilindro. |
| Conducto tras sustraer intersección | 387.386,699 m³ | Geant4 B: 387.492,0; error estándar reportado 90,7 m³ | Diferencia de 105,301 m³, aproximadamente 1,16 errores estándar reportados. Compatible. |
| Cuerpo denso | 1.215.148,535 m³ | 1.215.148,5 m³ esperado; 1.215.150 m³ impreso en Geant4 | Consistente con redondeo. |

La comparación toma las incertidumbres de los estudiantes como reportadas, sin recalcular aquí sus estimadores Monte Carlo. Evidencia, versiones y huellas en [volumen independiente](evidencias/volumen-independiente-geo-train-06.json). Herramienta: [validar_volumen_oe1.py](../herramientas/validar_volumen_oe1.py), requiere SciPy.

## Materiales y alcance de la equivalencia

El examen del catálogo y de los siete sondeos entregados es coherente con la regla «la última anomalía prevalece» en la región común. Los seis puntos en roca/anomalías tienen densidades coincidentes. El punto exterior tiene clase aire en ambos motores, pero densidad analítica 0,001225 g/cm³ frente a 0,00120479 g/cm³ reportada en Geant4: aproximadamente 1,65 % menos. Esto es una diferencia de modelo declarada en los propios archivos, no una prueba de error del transporte. No debe afirmarse identidad exacta de densidades para todos los materiales.

La revisión del parche confirma la intención de sustraer anomalías posteriores y recortar las que salen del edificio. Los desplazamientos se expresan en el sistema local de cada sólido. El recorte usa un margen de 1 mm: es necesario conservar esa precisión en la descripción de la corrección; no representa identidad matemática con el campo analítico en todas las fronteras. No se ha compilado ni comprobado aquí la navegación de sólidos booleanos.

## Consecuencia para el OE1

### Ampliación a las cuatro geometrías con intersecciones

Se repitió la integración independiente para las cuatro parejas identificadas. Para las cavidades se usa la misma integral con los tres semiejes iguales al radio. El contraste utiliza el diagnóstico de los estudiantes de la revisión `712c786`; su huella y las de cada entrada constan en [intersecciones independientes](evidencias/intersecciones-independientes.json).

| Geometría | Intersección independiente (m³) | Estimación de estudiantes ± error estándar (m³) | Porcentaje del conducto ocupado por la intersección |
|---|---:|---:|---:|
| geo-test-01 | 6.879,757 | 6.888,792 ± 8,003 | 0,662 % |
| geo-train-06 | 83.663,703 | 83.641,919 ± 44,671 | 17,761 % |
| geo-train-08 | 111.734,423 | 111.691,384 ± 71,160 | 8,864 % |
| geo-train-11 | 28.902,724 | 28.900,706 ± 21,906 | 4,557 % |

Las discrepancias son menores de 1,13 errores estándar reportados en los cuatro casos. Esto es una comprobación numérica favorable de sus estimaciones, no una prueba formal de equivalencia ni una medida de impacto en conteos. Las diferencias entre las dos tolerancias de cuadratura están por debajo de 0,023 m³; el error indicado por la integral exterior no incorpora rigurosamente todo el error anidado.

**Utilidad para el siguiente ensayo:** disponer de referencias independientes para validar implementaciones y no extrapolar el caso geo-train-06 a todo el catálogo. En geo-train-06/08 la regla de prioridad asigna un cuerpo más denso al volumen común; en geo-test-01/geo-train-11 asigna una cavidad de menor densidad. Esa comparación entre materiales posibles no establece qué material recorrió cada muón en la construcción original inválida. El porcentaje de volumen tampoco ordena la sensibilidad de las vistas.

Esta ampliación no examina volúmenes que sobresalen del edificio (`geo-gen-01`, `geo-test-03`) ni justifica abrir nuevas simulaciones en la partición test. El cálculo de geo-test-01 es un control de geometría, no una evaluación de modelos o un ajuste de parámetros con sus resultados.

Para repetir: `python herramientas/validar_intersecciones_oe1.py`. Para comparar además con los estudiantes, añadir `--referencia` seguido de la ruta a `diagnostico/auditoria-geometrica-oe1.json` de su entrega. Sin esa opción solo se calculan los volúmenes; el script actualiza el JSON de evidencia derivada. Requiere SciPy. No modifica datos originales.

Hay un control independiente adicional favorable a la geometría corregida de este caso. Se mantiene el [encargo de diseño del segundo ensayo](DISENO_SIGUIENTE_ENSAYO_OE1.md): estos cálculos no justifican cerrar el impacto físico ni repetir toda la campaña. Registrar explícitamente densidades y márgenes en la propuesta; si se pretende comparar motores con gran precisión, justificar su efecto según las trayectorias relevantes, sin atribuir automáticamente a esa diferencia de aire los resultados observados.

# Cierre del objetivo específico 1

**Estado: cumplido y cerrado por decisión de la dirección, el 2026-10-03, dentro del alcance idealizado adoptado.** La solicitud expresa de consolidar y cerrar el objetivo se registra en esta revisión. No se presenta como una aprobación institucional de la tesis, una aceptación emitida por los estudiantes ni una validación experimental.

## Objetivo y criterio de cumplimiento

El plan `Plan_Final_Muografía.pdf`, sección 4.2, página impresa 9, establece:

> Generar un conjunto de datos sintéticos de imágenes muográficas por transmisión, con diferentes niveles de estadística de conteo, mediante simulación Monte Carlo que reproduzca escenarios representativos de exploración volcánica.

El [registro de evidencia](manuscrito/EVIDENCIA_CIERRE.json) conserva el enunciado, la huella del plan consultado y las 19 geometrías contrastadas contra la receta. No se cambia el objetivo; se explicita la interpretación de representatividad aceptada en el alcance del proyecto.

| Componente del objetivo | Producto y justificación | Balance |
|---|---|---|
| Conjunto sintético de imágenes por transmisión | 114 referencias de 256 × 256, con cuentas direccionales de primarios tras el transporte y coordenadas explícitas. | Verificado. No son mapas reconstruidos de densidad. |
| Diferentes estadísticas de conteo | 9.120 pares, cuatro fracciones y veinte realizaciones por fracción; reproducción de 342 huellas de contenido. | Verificado. Referencias finitas y dependencia entre realizaciones declaradas. |
| Simulación Monte Carlo | Receta Geant4, versiones, geometrías, semillas, registro de 1.026 bloques y productos de 39.216.000.000 primarios. | Verificado en los registros y productos. No se atribuye una segunda ejecución local de transporte. |
| Escenarios representativos | 19 edificios cónicos con variación dimensional, control homogéneo, déficits y excesos de densidad, combinaciones de anomalías y seis vistas. | Justificación incorporada y aceptada para el estudio sintético idealizado; no se afirma representatividad estadística de volcanes reales. |
| Entrega y documentación | Datos de Git y Drive íntegros; ficha, procedimiento reproducible e informe con ecuaciones, resultados, figuras y conclusión. | Verificado documentalmente. |

## Justificación y producto documental

El [informe de cierre](manuscrito/INFORME_OE1.pdf) integra metodología, nomenclatura, justificación de representatividad, controles, resultados, figuras, discusión y conclusión. Su [fuente editable](manuscrito/INFORME_OE1.tex) conserva las ecuaciones y referencias.

La representatividad es de mecanismos y configuraciones: caminos de distinta columna de masa, contrastes positivos y negativos, cambios de proyección y fluctuación de conteo. El catálogo no pretende muestrear una población de volcanes ni caracterizar un sitio real. Los radios basales abarcan 509,7–698,7 m y las alturas 356,2–449,6 m. La roca de fondo es de 2,65 g/cm³. Estos intervalos describen el catálogo, no una validación geológica externa.

El control homogéneo es `geo-train-01`. El caso `geo-gen-01` contiene un conducto y dos cavidades. Se corrigió la frase del borrador que atribuía homogeneidad a la geometría reservada; las 19 huellas del catálogo coinciden con la receta y no se modificaron los datos.

## Condiciones que se conservan en el cierre

- Los 1.710 contrastes de bordes cumplen el criterio establecido. La meta de roca se alcanza en 107/114 vistas; las siete excepciones permanecen identificadas, sin descartarlas ni reinterpretarlas como conformes.
- El plano de 600 m es computacional. La fuente híbrida y el transporte solo de primarios no acreditan equivalencia con un instrumento real.
- La exposición es convencional, sin conversión calibrada a días físicos. El cierre no demuestra un factor de reducción de adquisición.
- Las referencias tienen ruido y los pares comparten referencias. La comprobación de integridad de dataset-v2 no certifica conversión, entrenamiento ni desempeño de redes.
- La atribución de ejecución a estudiantes y de revisión documental a la dirección se conserva. No se alteran originales, recetas congeladas ni la rama de estudiantes.

Estas condiciones delimitan el resultado aceptado; no se convierten en nuevas obligaciones de simulación dentro del OE1. Una equivalencia instrumental exigiría un alcance adicional explícito.

## Estado operativo

P-01 a P-05 quedan resueltos dentro del alcance descrito; los criterios A-01 a A-08 cuentan con evidencia y decisión de cierre. No quedan tareas de generación, verificación o redacción del informe específico del OE1 pendientes. No se solicita otra corrida de SC3.

La incorporación de este informe a la tesis completa, su revisión por los estudiantes y su presentación son actividades del documento global y de su responsabilidad académica. No se afirma que la tesis completa haya sido entregada o aprobada. OE2 y OE3 permanecen fuera de este cierre y requieren su propio trabajo y autorización de alcance.

La cronología anterior se conserva en Git, el [registro de cambios](../CHANGELOG.md) y la [bitácora](BITACORA.md). Los avisos de pendiente de revisiones anteriores describen su fecha de emisión; el estado vigente es el presente registro.

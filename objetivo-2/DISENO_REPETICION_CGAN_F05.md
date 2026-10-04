# Diseño de repetición de la continuación cGAN al 5 %

Fecha: 2026-10-04, America/Bogota. **Estado: diseño científico fijado; integración operativa de semillas y verificación del ejecutor pendientes. No constituye todavía una orden de ejecución.** Se deriva de la [valoración por vista y anomalía](VALORACION_COMPROMISO_CGAN_F05.md). No se lanza entrenamiento en esta preparación.

## Pregunta y alcance

¿La ventaja regional de C1 frente a C0 se mantiene al variar la semilla de continuación, y qué deterioros de imagen, borde y anomalías reaparecen?

El ensayo estudia **estabilidad condicionada al mismo checkpoint inicial**. No estima variabilidad de entrenamientos desde cero, incertidumbre de la simulación, ni generalización a geometrías reservadas. Las tres parejas nuevas son repeticiones estocásticas de la continuación; todas heredan los mismos pesos y su selección previa sobre validación.

## Matriz fijada antes de ejecutar

| Pareja | Semilla nueva | C0 | C1 |
|---|---:|---|---|
| R1 | 2026100401 | λregional = 0 | λregional = 1 |
| R2 | 2026100402 | λregional = 0 | λregional = 1 |
| R3 | 2026100403 | λregional = 0 | λregional = 1 |

Son seis continuaciones nuevas. El ensayo previo con semilla 2026100303 se conserva como antecedente exploratorio y se presenta por separado: no se cuenta retrospectivamente como una repetición prospectiva. Tres parejas constituyen un presupuesto acotado para detectar inestabilidad evidente, no un tamaño muestral justificado para significación estadística.

Cada ejecución comienza desde el checkpoint cGAN original de época 5, SHA-256 `e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0`, con G y D originales y optimizadores nuevos. No parte de los C0/C1 finales recibidos ni encadena quince épocas.

Se conservan: generador unet_dc_5, crítico patch_critic_70, fracción 0,05, 1.440 train/360 val, normalización y máscaras verificadas, lote 4, cinco épocas adicionales, selección fija de la quinta, Adam lr=1e-5/betas=(0;0,9), cinco pasos D por G, GP=10, L1=100, derivación separada CG-04c, sin AMP, aumentos ni parada temprana.

Dentro de cada pareja se usa la misma semilla, inicialización, orden de muestras y configuración. C0/C1 solo difieren en el término regional y su identificación. Entre parejas cambia la semilla; no cambian los datos ni sus realizaciones de conteo. Las trayectorias C0/C1 pueden diferir porque sus pérdidas son distintas.

## Evaluación pareada y regla prospectiva

Para cada semilla s y medida M, registrar ΔM_s = M(C1,s) − M(C0,s). Se conservan los ocho controles originales, por pareja y sin redondeo: Q menor, ningún Q por geometría mayor, cielo/borde no peores, los 23 contrastes comunes, error de contraste no mayor, SSIM y PSNR no menores. No se cambian coeficientes, épocas ni tolerancias después de examinar una pareja.

Se informarán las tres diferencias individuales, su mediana y rango. Como regla de lectura fijada para esta repetición:

- **Concordancia repetida del criterio agregado:** las tres parejas satisfacen los ocho controles originales. Es respaldo exploratorio a la estabilidad de la comparación C1/C0, no aceptación física.
- **Resultado dependiente de la semilla o compromiso:** alguna pareja no satisface todos los controles, aunque otras sí. Se conservan todas las parejas y se identifica qué medida cambia de dirección.
- **Ausencia de reducción consistente de Q:** informar cuántas parejas reducen Q y cuáles no. No se sustituye una semilla por otra favorable.

No se emplean las 360 imágenes, 18 vistas o veinte realizaciones como si fueran repeticiones independientes de entrenamiento. Con tres parejas y tres geometrías observadas, no se proclama significación ni se calculan intervalos que aparenten una base confirmatoria. La media y el rango por semilla son descripciones del ensayo condicionado.

## Salvaguardas físicas predefinidas

En cada pareja se entregan las 18 vistas y las 24 combinaciones de vista/anomalía frente a C0, cGAN inicial y entrada. Mostrar magnitud y signo del sesgo, error absoluto de cuentas, soporte en píxeles/cuentas, contraste de referencia/predicción, cambios de signo y cocientes indefinidos.

Registrar especialmente los hallazgos exploratorios, sin excluir los demás: las seis vistas de geo-val-02 para borde; geo-val-02/V2, geo-val-03/V1 y V5 para q; el cuerpo denso de geo-val-03, incluido su contraste en V1; las seis vistas de geo-val-01 frente al modelo inicial. Identificarlos como casos señalados por el ensayo previo, no como prueba independiente.

Si los ocho controles agregados se repiten pero persisten deterioros locales relevantes, la conclusión será «ventaja agregada repetida con limitaciones físicas persistentes». No se certifica físicamente el modelo por una votación de semillas. Antes de una campaña confirmatoria deberán definirse tolerancias físicas justificadas por el uso previsto y el alcance de la tesis; estas no se deducen de los resultados presentes.

## Preparación operativa pendiente

El ejecutor vigente comprueba configuraciones con huellas fijas e incluye una sola semilla. **No editar a mano C0.json/C1.json ni pasar un parámetro de semilla que no existe.** El [JSON de diseño](configuraciones/repeticion-cgan-f05/diseno.spec.json) es una especificación no ejecutable (`ready_for_gpu: false`).

Se debe implementar un mecanismo versionado para las seis configuraciones, identificadores de pareja y semilla en checkpoints, selección de configuración en ejecutor/revisor/evaluador, y aceptación compatible por pareja. La auditoría actual asume los nombres C0/C1 y sus configuraciones originales; no se reutiliza sin adaptar esos contratos.

Antes de delegar: controles de rechazo de mezcla de semillas/configuraciones, igualdad de fuentes e inicialización, emparejamiento de índices, contadores y selección de época; después batería CPU continua/recuperada para las tres parejas. En GPU se requiere la misma batería de dos épocas por pareja (12 ejecuciones técnicas en total, con 18 lanzamientos por las recuperaciones). No se utiliza la aceptación de la versión anterior para saltar esa comprobación. No se modifica el criterio exacto de recuperación.

Tras esa preparación, el encargo podrá dar autonomía para completar las tres parejas y su evaluación si pasan las comprobaciones y hay recursos. Ante fallo técnico se conserva la evidencia y se detiene la pareja; no se compensa con más épocas ni se cambia el diseño. La inspección intermedia no debe detener parejas posteriores por un resultado científico desfavorable.

## Presupuesto y entrega

Seis continuaciones × cinco épocas × 360 lotes = **10.800 actualizaciones G y 54.000 D**. Las tres baterías técnicas añaden 48 G y 240 D. Una GPU puede ejecutarlas secuencialmente; no se requiere entrenamiento distribuido.

Como referencia de planificación, las dos continuaciones recibidas registraron 640,2 y 654,7 segundos de cómputo. Tres parejas equivalentes darían aproximadamente 3×(640,2+654,7)=3.884,7 s, unos 65 minutos de cómputo en condiciones semejantes. No incluye instalación, prueba técnica, transferencia, evaluación y esperas, ni constituye un compromiso de duración o costo. Medir recursos con la primera batería del nuevo ejecutor.

Entregar seis checkpoints finales y predicciones, sus registros completos, aceptaciones técnicas por pareja, manifiestos de huellas/tamaños y enlaces de Drive, evaluación por semilla y síntesis pareada sin selección de la mejor semilla. Conservar fallos, tiempos y memoria. Los binarios grandes no se versionan en Git.

El trabajo posterior a este diseño corresponde primero a integración y verificación local. La campaña principal, otras fracciones, entrenamiento desde cero y apertura de test/generalization permanecen fuera de este ensayo.

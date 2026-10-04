# Objetivo específico 2: revisión de la implementación recibida

**Síntesis documental del OE2 preparada:** [informe académico](manuscrito/INFORME_OE2.md), [matriz de cumplimiento](MATRIZ_CUMPLIMIENTO.md) y [registro de cierre de ejecución](CIERRE_OE2.md). EF-02, EF-03 y la conclusión documental EF-04 completos. La calidad comparable mantiene alcance parcial; no se declara equivalencia física. Resta integración editorial en el manuscrito, sin nuevas corridas.

**Evaluación final al 5 % revisada; corrección C2 verificada.** Se recibieron y auditaron los ocho modelos y sus 3.840 predicciones. Las métricas de imagen/regiones se reproducen; el contraste queda corregido con índices registrados y comparación antes/después. [Revisión vigente](REVISION_EVALUACION_FINAL_C2.md) · [Síntesis y siguiente paso](SINTESIS_OE2_TRANSICION_OE3.md). No se requiere otra GPU. La implementación/evaluación está verificada; equivalencia física y alcance académico siguen delimitados, no se declara cumplimiento científico pleno.

## Antecedentes conservados


**E1 ejecutado y revisado:** 55 binarios íntegros, recuperación exacta en B1–B3 y 2.520 inferencias reproducidas. El borde mejora en todas las vistas, pero persiste sobreestimación interior en geometría 1; ninguna pareja cumple los nueve controles. [Revisión y diagnóstico](REVISION_E1_804CE85.md) · [Consolidación E1 histórica, no bloqueante](INSTRUCCIONES_CIERRE_E1.md). OE2 continúa abierto.

**OE2 — repetición cGAN revisada:** se verificaron los 55 binarios, la recuperación exacta de las tres parejas, las seis continuaciones y su inferencia. C1 reduce el sesgo regional en dos parejas y lo aumenta en la tercera; el error de borde empeora en las tres y ninguna satisface los ocho controles. La [revisión independiente](REVISION_REPETICION_F6518FF.md) confirma dependencia de la semilla o compromiso. No se concede aceptación física ni se amplía la campaña; el siguiente paso es revisar el diseño científico y los criterios de aceptación. El OE2 permanece abierto.

**Estado al 2026-10-03: correcciones OE2-P01 a P03 implementadas y verificadas localmente.** Véase [correcciones v1, evidencia y reproducción](CORRECCIONES_V1.md). OE2-P04 tiene un [protocolo de piloto al 5 %](PROTOCOLO_PILOTO_F05.md) y [comandos para SC3](INSTRUCCIONES_PILOTO_SC3.md); se recibió y [revisó el piloto ejecutado en GPU RunPod](REVISION_PILOTO_C054225.md). Los [dos pesos seleccionados y su inferencia fueron verificados](REVISION_PESOS_PILOTO_F05.md) en los 360 pares de validación. La [evaluación geométrica](EVALUACION_GEOMETRICA_PILOTO_F05.md) cuantifica sesgos de cuentas y conservación de contrastes: el diagnóstico está verificado; la aceptación física y la campaña principal siguen pendientes. El texto de revisión siguiente conserva los hallazgos del código histórico. La dirección autorizó expresamente esta revisión del OE2. El cierre del OE1 se mantiene; no se declara cumplido el OE2 ni se inicia una campaña de entrenamiento.

El objetivo consiste en diseñar e implementar una cGAN que transforme imágenes muográficas de baja estadística en imágenes de calidad comparable a las de alta estadística. La salida considerada es una imagen muográfica; esta revisión no acredita reconstrucción de densidad.

## Material y procedencia

Se revisó el código publicado por los estudiantes en [muography-dl-reconstruction, b88fa57](https://github.com/Dp100131/muography-dl-reconstruction/tree/b88fa576494cb8a664c46b8c94c5918c5097d616): `scripts/training/`, `models/`, configuración `e17_final.json`, manifiestos de pesos y registros históricos. Tras consultar los remotos, no se encontraron diferencias en `scripts/training` respecto de la rama `oe1/stage1-instrumentation` (3315f82). Esto identifica la versión examinada, sin afirmar que no exista código adicional sin publicar o en otro repositorio.

En la réplica, la rama estudiantil `oe1/justificacion-fisica-produccion` llegó a 800ab86 con documentación de representatividad y campaña. No se fusionó esa rama. Para la comprobación de entrada se utilizó la distribución local `drive-2026-10-03/dataset-v2`, previamente verificada durante el [cierre del OE1](../objetivo-1/CIERRE_OE1.md).

## Qué se puede reutilizar

| Componente | Resultado de la revisión |
|---|---|
| Arquitectura condicional | Existe una cWGAN-GP: generador U-Net y crítico que recibe entrada y candidata concatenadas. |
| Configuración histórica seleccionada | `unet_dc_5`, 20.543.809 parámetros; crítico `patch_critic_70`; pérdida adversaria más L1. No confundir con el generador predeterminado `unet_p2p_6`. |
| Entrenamiento | Existen optimizadores, semillas, registros, parada temprana y recuperación de estados. Son una base útil, sujeta a los pendientes siguientes. |
| Datos corregidos | Las 15 geometrías de train/val conservan exactamente referencias y 7.200 pares al convertir al formato de entrenamiento; no se detectó pérdida por el cambio a uint16. |
| Compatibilidad de red | Un par corregido de geo-train-01, fracción 0,05, atraviesa el generador y el crítico con valores finitos y dimensiones esperadas. Se usaron pesos aleatorios: no es una evaluación de calidad. |
| Resultados anteriores | Hay pesos y métricas históricas. Corresponden al conjunto anterior y no acreditan desempeño sobre la campaña corregida. No se repitió aquí su evaluación. |

Las particiones contienen 5.760 pares de entrenamiento, 1.440 de validación, 1.440 de prueba y 480 de generalización. Los pares de una misma geometría comparten referencia y no constituyen miles de escenarios independientes. En esta revisión no se abrieron imágenes de prueba ni generalización, ni se entrenó una red.

## Hallazgos y pendientes

### OE2-P01 — Agregación del crítico y penalización del gradiente

**Estado vigente: resuelto en la implementación derivada v1; hallazgo histórico conservado a continuación.** En `scripts/training/losses.py`, las pérdidas adversarias usan el promedio del mapa del crítico, mientras que `gradient_penalty` diferencia su suma mediante `grad_outputs=ones_like(scores)`.

Para un mapa con P parches, la puntuación por muestra utilizada por la pérdida es

\[
C(x,y)=\frac{1}{P}\sum_{p=1}^{P}D_p(x,y).
\]

La implementación penaliza \(\|\nabla_y\sum_pD_p\|_2\), que equivale a \(P\|\nabla_y C\|_2\), en lugar de penalizar el gradiente de esa misma puntuación promedio. El mapa 30×30 tiene P=900. No es simplemente una constante multiplicativa de toda la pérdida: cambia el gradiente objetivo de la regularización.

La prueba construye un crítico cuyo promedio tiene gradiente de norma uno. La penalización coherente es cero, pero la función publicada devuelve 808.201 para 30×30 y 38.025 para 14×14; con un único parche sí devuelve cero. Son valores de una prueba analítica, no pérdidas observadas en los entrenamientos históricos. La prueba histórica con crítico escalar no detecta esta diferencia.

**Cierre requerido:** definir una puntuación escalar por muestra y emplearla consistentemente en pérdida y penalización; añadir una prueba con varios parches y registrar una nueva versión. Los pesos históricos no se convierten en pesos corregidos mediante un cambio de etiqueta.

### OE2-P02 — Normalización dependiente de la referencia

**Estado vigente: resuelto mediante normalización v1 ajustada solo con train; hallazgo histórico conservado a continuación.** El modo seleccionado `ref_equivalent` calcula

\[
x=\frac{\log(1+n_{\mathrm{low}}/f)}{\log(1+\max n_{\mathrm{ref}})},\qquad
y=\frac{\log(1+n_{\mathrm{ref}})}{\log(1+\max n_{\mathrm{ref}})}.
\]

La fracción f es conocida, pero el máximo de la referencia no está disponible cuando únicamente se recibe una imagen de baja estadística. El propio código describe esta escala como un oráculo. La prueba confirma que, manteniendo idéntica la imagen de entrada, cambiar la referencia cambia la entrada normalizada.

Esto permite un experimento con información privilegiada si se declara expresamente, pero no demuestra una inferencia operativa. **Cierre requerido:** fijar una transformación disponible en inferencia, ajustada solo con entrenamiento o calculada desde la entrada, declarar su inversión y tratamiento del rango y aplicarla coherentemente en validación. La salida sigmoide exige revisar cualquier objetivo que pueda superar uno. El caso de referencia vacía produce valores no finitos; debe existir una política explícita, aunque no se observó ese caso en los shards examinados.

### OE2-P03 — Identidad y selección del conjunto

**Estado vigente: integración resuelta sobre distribución fijada en v1; recuperación del convertidor histórico continúa como antecedente documental.** El lector apunta a `dataset/shards` y `results/dataset/splits.json` del repositorio histórico. Para el diagnóstico se redirigieron estas rutas únicamente en memoria. Esto prueba compatibilidad de arreglos, no una integración de producción terminada.

El checkpoint guarda configuración y commit, pero no vincula obligatoriamente el estado a las huellas de los datos. La protección contra una configuración diferente es útil, aunque no basta cuando cambian los archivos bajo las mismas rutas.

**Cierre requerido:** parámetros explícitos para datos y particiones, verificación del manifiesto de la distribución, registro de huellas en configuración/checkpoint y rechazo de reanudación cuando cambia el conjunto. Debe recuperarse y fijarse también la versión del convertidor referido por `conversion-report.json`; ese informe identifica `analysis/convert_oe1_package.py` y su huella, pero no sustituye el código reproducible. La igualdad numérica de train/val ya está comprobada aquí.

### OE2-P04 — Protocolo y evidencia sobre los datos corregidos

**Estado vigente: piloto, continuaciones y E1 verificados; diagnóstico regional realizado. Aceptación física y evaluación final pendientes.** La existencia de modelos históricos reduce el trabajo de implementación, pero todavía se requiere un protocolo específico: fracciones, modelo por fracción o condicionamiento explícito por f, semillas, presupuesto, comparación con U-Net L1 y criterio de selección.

La configuración histórica usa modelos separados por fracción; la imagen de baja estadística es la condición del crítico. No corresponde describirla como una única red condicionada explícitamente por f. El criterio `min_delta=0.001` afecta qué checkpoint se considera mejor: se debe distinguir mejora suficiente para paciencia de máximo absoluto de SSIM, o declarar expresamente el criterio adoptado.

**Cierre requerido:** tras P01–P03, una prueba corta de entrenamiento, guardado y reanudación; después entrenamiento reproducible con train/val y valoración documentada. No se exige una nueva simulación Geant4 para iniciar estos trabajos. Test/generalization deben mantenerse fuera de la selección; la exposición histórica a geometrías del catálogo debe declararse y no presentarse como una reserva completamente nueva. La evaluación final comparativa no se certifica en esta auditoría.

## Evidencia y reproducción

El [diagnóstico JSON](evidencias/revision-2026-10-03.json) registra versiones, huellas del código, 15 shards, comparación de 90 vistas, paso por la red y pruebas matemáticas. El [script](herramientas/revisar_base.py) recibe rutas explícitas y abre únicamente train/val. Entorno de revisión: Python 3.12.14, PyTorch 2.6.0+cpu, NumPy 2.4.4; dos hilos, semilla 20261003. Esto no verifica CUDA ni el rendimiento en SC3.

Desde la raíz de esta réplica, sustituyendo las rutas por las ubicaciones locales:

```powershell
python objetivo-2/herramientas/revisar_base.py --codigo ../tmp/revision-muography-dl-reconstruction --datos trabajo/drive-2026-10-03 --salida objetivo-2/evidencias/revision-2026-10-03.json
```

El script termina correctamente cuando reproduce los diagnósticos, incluidos los defectos actuales; no equivale a una aprobación del código para entrenar. Al corregir el código deberán cambiarse las expectativas y conservar esta evidencia del antes. Véase la [bitácora](BITACORA.md).

**Secuencia vigente:** P01–P03 corregidos, piloto GPU recibido y pesos seleccionados verificados sobre val. Las regiones geométricas y el diagnóstico de calibración están verificados. El ajuste acotado está diseñado e implementado, con recuperación exacta verificada en CPU; la entrega GPU y la comparación U-Net ya fueron verificadas. La clasificación de compromiso y el deterioro del cuerpo denso respecto del modelo inicial impiden declarar aceptación física o ampliar automáticamente. El resultado de la revisión es una base aprovechable con correcciones concretas, no la necesidad de comenzar desde cero.

## Diseño del ajuste de cuentas

Se preparó el [ensayo A/B de continuación de U-Net](DISENO_AJUSTE_CUENTAS_F05.md), con cinco épocas por rama y selección fija de la época final. La integración y el entrenamiento técnico en CPU están verificados mediante 30 controles y recuperación exacta en ambas variantes. El evaluador reproduce 468 cifras regionales del diagnóstico previo. La [revisión independiente de la entrega a6aa6b8](REVISION_AJUSTE_A6AA6B8.md) verifica recuperación GPU mediante sus artefactos, cinco épocas por rama y reproducción de 720 inferencias. Ajuste-01/02 están verificados; Ajuste-03 está completado y verificado como comparación, con resultado de compromiso y sin aceptación física. Se incorpora la [propuesta cGAN](PROPUESTA_CONTINUACION_CGAN_F05.md); su integración y recuperación exacta ya están verificadas en CPU mediante 19 controles y cuatro ejecuciones de las redes completas. La [entrega CG-04c y sus cinco épocas ya se verificaron](REVISION_BINARIOS_CG04C.md); la valoración y la repetición vigente se enlazan al inicio. La campaña principal permanece pendiente.

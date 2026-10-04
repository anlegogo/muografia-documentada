# Evaluación final OE2 · protocolo EF-01

Fecha: 2026-10-04. **Protocolo fijado antes de calcular desempeño en las particiones reservadas.** Se sustituye como prioridad la repetición del diagnóstico E1 por una evaluación conjunta de pesos existentes. No se solicita nuevo entrenamiento. La dirección autorizó avanzar hacia la evaluación final; no se declara anticipadamente cumplido el objetivo.

## Alcance y pregunta

Se evalúa la implementación de recuperación de imágenes muográficas con **5 % de los conteos**, usando la referencia idealizada de alta estadística del OE1. La salida es una imagen de cuentas equivalentes, no densidad. Se pregunta cuánto recupera la cGAN, cómo se compara con la entrada y con U-Net, y qué efecto conservan los ajustes regionales/de borde fuera de validación.

Este cierre experimental abarca los modelos entrenados al 5 %. No demuestra desempeño en las otras tres fracciones ni sustituye una campaña de 24 entrenamientos. Tampoco certifica detector o volcán real. La conclusión de alcance debe mantenerse al redactar el cumplimiento académico del objetivo.

## Modelos congelados y comparación

El [contrato ejecutable](configuraciones/evaluacion-final-v1.json) fija ocho SHA-256:

1. U-Net L1 original, mejor checkpoint de validación de época 5.
2. cGAN original, mejor checkpoint de validación de época 5: modelo principal de la comparación original.
3. B1-C0, B1-C1, B2-C0, B2-C1, B3-C0 y B3-C1: las seis continuaciones completas de E1, siempre quinta época adicional.

La entrada sin red, corregida por la fracción, se calcula sobre exactamente los mismos pares. Son nueve métodos, ocho redes. Los seis ajustes se conservan como análisis secundario completo, no como una búsqueda de la semilla ganadora sobre prueba. No se cambia de checkpoint según resultados reservados ni se promueve automáticamente el mejor número de una tabla. Las tres continuaciones comparten inicialización y no estiman variabilidad desde cero.

Comparaciones prospectivas: cGAN original frente a entrada; U-Net frente a entrada; cGAN original frente a U-Net; y C1 frente a C0 dentro de B1, B2 y B3. No se mezclan las definiciones históricas de C0.

## Datos y exposición anterior

| Partición | Geometrías | Vistas | Realizaciones/vista | Imágenes al 5 % |
|---|---:|---:|---:|---:|
| test | geo-test-01 a geo-test-03 | 18 | 20 | 360 |
| generalization | geo-gen-01 | 6 | 20 | 120 |

Se conservarán las dos particiones separadas. Ocho redes producen **3.840 predicciones**, más 480 entradas comparadoras; no son nuevas simulaciones. El contrato fija los ocho archivos NPZ/metadatos de estos cuatro escenarios con las huellas ya verificadas en la distribución del OE1. No necesita regenerar los pares. Los archivos originales contienen cuatro fracciones; el ejecutor usa exclusivamente índice 2, f=0,05.

Las geometrías, referencias y propiedades del catálogo se conocían y se inspeccionaron durante el OE1. Las tres geometrías test y la única geometría de generalización no constituyen una muestra amplia de volcanes. La integridad previa no equivale a evaluar redes, pero tampoco permite presentar el catálogo como completamente desconocido. Antes de ejecutar, los autores dejarán constancia de cualquier uso adicional de test/generalization en entrenamiento, elección de épocas, arquitectura o parámetros; si existió o no puede descartarse, los resultados se rotularán como evaluación descriptiva sobre datos potencialmente expuestos, sin afirmar independencia confirmatoria. No se oculta esa limitación ni se modifica la partición para eliminar casos difíciles.

## Métricas y regla de lectura

Se conserva \(T(c)=\log(1+c)/(s+\log(1+c))\), con \(s=8{,}239329427901795\), ajustado solo con train. La entrada es \(T(n/f)\); la referencia, \(T(c)\). Se invierte cada predicción antes de sumar cuentas, sin recortes ni pseudocuentas.

Se registran SSIM y PSNR por imagen, con la parametrización existente y rango uno. Por geometría y vista se evalúan sesgo firmado, sesgo absoluto medio y error espacial normalizado por cuentas de referencia, en cielo, roca sin anomalía, borde y cada anomalía. Las máscaras y los controles de contraste conservan los parámetros geométricos del protocolo anterior; no se seleccionan regiones según el error observado.

Para una región R y realización k:

\[
b_{Rk}=\frac{\sum_{p\in R}(\widehat c_{kp}-c_p)}{\sum_{p\in R}c_p},\qquad
a_{Rk}=\frac{\sum_{p\in R}|\widehat c_{kp}-c_p|}{\sum_{p\in R}c_p}.
\]

Q conserva la media, con igual peso, de sesgo absoluto del promedio en roca y anomalías; las anomalías se promedian dentro de cada vista antes de promediar vistas. Se requiere soporte completo. En una geometría sin anomalías o con regiones no estimables se reporta Q como no aplicable/incompleto y se conserva el indicador de roca: no se inventa un cero ni se suprimen escenarios.

Las regiones con menos de 20 píxeles o referencia nula quedan registradas como no estimables según referencia/geometría, igual para todos los métodos. En contraste se informa soporte y realizaciones con control nulo; el resumen comparable usa únicamente soporte común completo de todos los métodos y muestra su número. No se fija de antemano el número 23 observado en validación. Las tablas completas conservan los demás casos.

SSIM y PSNR se resumen por geometría y después con igual peso entre geometrías de la misma partición. El contraste agregado conserva explícitamente el soporte común; también se informa por geometría. Un caso idéntico a la referencia tiene PSNR infinito, representado por `null` con `perfect_match: true`; no se confunde con PSNR cero ni se elimina silenciosamente.

La salida genera diferencias candidato menos comparador y controles descriptivos por geometría para SSIM, PSNR, Q, cielo, borde y contraste. La clasificación es `incomplete`, `no_deterioration_in_listed_metrics` o `tradeoff_or_deterioration`. La ausencia de deterioro no implica equivalencia ni superioridad estadística. No se hacen pruebas que traten las veinte realizaciones como veinte geometrías independientes.

**Calidad comparable a alta estadística:** no existe en el protocolo previo un margen absoluto de equivalencia física justificado. No se inventa ahora un umbral de SSIM o de error para garantizar el cierre. La evaluación cuantifica concordancia y limitaciones; una mejora frente a la entrada o un resultado favorable frente a U-Net no prueban automáticamente equivalencia con la referencia. Si la evidencia no respalda la afirmación amplia, el informe debe limitarla. Esto permite terminar el experimento con una conclusión válida, aunque sea de compromiso, sin encadenar entrenamientos hasta obtener un resultado favorable.

## Ejecutor y conservación

[evaluacion_final_oe2.py](herramientas/evaluacion_final_oe2.py) dispone de `preflight`, `infer` y `evaluate`. Comprueba datos, fuentes, pesos, normalización e identidad. La inferencia usa modo evaluación y no carga optimizadores para entrenar. Exporta 120 imágenes por geometría con recibo SHA-256. Una ejecución repetida reutiliza exportaciones completas idénticas; rechaza identidad o archivos alterados. Los modelos pueden repartirse entre GPU distintas; cada carpeta de modelo tiene bloqueo exclusivo. Se mantiene lote cuatro, determinismo y TF32 desactivado.

La evaluación exige los ocho modelos y las cuatro geometrías antes de concluir. No se detiene por resultados científicos desfavorables, solo por errores técnicos. Se escribe el entorno y un inventario completo. Pesos y NPY permanecen fuera de Git; los informes JSON/CSV y los recibos permiten la revisión posterior.

## Verificación previa y estado

Cinco pruebas de contratos y siete comprobaciones del flujo sintético pasaron, incluyendo exportación de 480 imágenes de prueba, reutilización, rechazo de identidad distinta y corrupción, evaluación conjunta y geometría sin anomalías. Se verificaron los ocho pesos reales con 32 inferencias sobre validación: máximo de diferencias inferior a 1e-4. El nuevo cálculo regional, SSIM, PSNR y contraste coincide en 441 campos con las tablas E1 de una vista de validación de cada pareja, hasta 5,56e-17. No se repitió el entrenamiento ni se abrió desempeño reservado localmente. La prueba GPU de inferencia queda a cargo de la ejecución final, no de otro entrenamiento técnico.

[Evidencia con pesos reales](evidencias/evaluacion-final-local.json) · [flujo sintético](evidencias/evaluacion-final-flujo.json) · [pruebas de contratos](herramientas/test_evaluacion_final_oe2.py) · [integración](herramientas/test_flujo_final_oe2.py).

OE2-P04 permanece parcial hasta recibir, revisar e interpretar la evaluación. EF-01 queda preparado y verificado localmente; EF-02 (inferencia reservada), EF-03 (evaluación y auditoría) y EF-04 (conclusión académica delimitada) siguen pendientes. Las [instrucciones de ejecución final](INSTRUCCIONES_EVALUACION_FINAL_OE2.md) sustituyen la consolidación E1 como paso bloqueante. El resultado alimentará el siguiente objetivo sin afirmar que OE3 esté realizado.

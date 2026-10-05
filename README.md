# Muografía: documentación y seguimiento académico

**Informe LaTeX corregido — 2026-10-04:** [proyecto editable](informe-final/latex/README.md) · [PDF compilado](informe-final/latex/main.pdf) · [ZIP para Overleaf](informe-final/latex/Trabajo_de_Grado_Muografia_corregido.zip). Se publica el documento completo revisado; el informe en Markdown se conserva como antecedente de integración.

**Informe integrado — 2026-10-04:** [metodología, resultados, discusión y conclusiones](informe-final/README.md) redactados y revisados, con seis figuras y tablas trazables. La integración del núcleo experimental está completa en Markdown; resta adaptación institucional y revisión de autores. El cumplimiento científico parcial de OE2/OE3 se conserva.

**Estado vigente del OE3 — 2026-10-04:** [cierre experimental y documental](objetivo-3/CIERRE_OE3.md). Evaluación finalizada; cumplimiento científico parcial. No se demuestra un factor de reducción bajo el benchmark y no se reconstruyó opacidad cuantitativa. No quedan nuevas corridas asignadas; resta la integración del informe final. Las notas inferiores conservan la cronología y no reabren encargos superados.

**Revisión vigente del complemento OE3-C1:** se verificaron las 96 matrices nuevas y se reprodujo la evaluación multifracción. Ningún modelo satisface conjuntamente SSIM/PSNR del referente sin red al 50 % en las fracciones estudiadas; no se demuestra un factor de reducción bajo ese benchmark. SNR/CNR y contraste de cuentas evaluados; la opacidad cuantitativa continúa delimitada. [Auditoría y balance](objetivo-3/REVISION_COMPLEMENTO_OE3_C1.md). No se encarga otro entrenamiento por este resultado negativo.

**Desglose experimental ejecutado:** [comparación por vista y región](objetivo-3/RESULTADO_EXPERIMENTAL_OE3.md). La cGAN al 5 % supera SSIM/PSNR de la entrada al 10 % en 24/24 vistas y 480/480 correspondencias, con deterioro de Q en 24/24 vistas. Se cuantifica una reducción descriptiva 2:1 de conteos bajo esas métricas; no un factor físico aceptado ni el máximo alcanzable. No se requiere otra GPU para reproducir este balance. La redacción del informe final se aplaza hasta concluir la revisión experimental, por indicación de la dirección.

**Síntesis documental del OE2 preparada:** [informe académico](objetivo-2/manuscrito/INFORME_OE2.md), [matriz de cumplimiento](objetivo-2/MATRIZ_CUMPLIMIENTO.md) y [registro de cierre de ejecución](objetivo-2/CIERRE_OE2.md). EF-02, EF-03 y la conclusión documental EF-04 completos. La calidad comparable mantiene alcance parcial; no se declara equivalencia física. Resta integración editorial en el manuscrito, sin nuevas corridas.

**Preparación OE3:** [curvas descriptivas de exposición](objetivo-3/README.md) calculadas con 1 %, 5 %, 10 % y 50 % de conteos existentes. Comparaciones visuales y físicas separadas; sin factor efectivo de adquisición demostrado ni nuevas corridas.

**Evaluación final al 5 % revisada; corrección C2 verificada.** Se recibieron y auditaron los ocho modelos y sus 3.840 predicciones. Las métricas de imagen/regiones se reproducen; el contraste queda corregido con índices registrados y comparación antes/después. [Revisión vigente](objetivo-2/REVISION_EVALUACION_FINAL_C2.md) · [Síntesis y siguiente paso](objetivo-2/SINTESIS_OE2_TRANSICION_OE3.md). No se requiere otra GPU. La implementación/evaluación está verificada; equivalencia física y alcance académico siguen delimitados, no se declara cumplimiento científico pleno.

## Antecedentes conservados


**E1 ejecutado y revisado:** 55 binarios íntegros, recuperación exacta en B1–B3 y 2.520 inferencias reproducidas. El borde mejora en todas las vistas, pero persiste sobreestimación interior en geometría 1; ninguna pareja cumple los nueve controles. [Revisión y diagnóstico](objetivo-2/REVISION_E1_804CE85.md) · [Consolidación E1 histórica, no bloqueante](objetivo-2/INSTRUCCIONES_CIERRE_E1.md). OE2 continúa abierto.

**OE2 — repetición cGAN revisada:** se verificaron los 55 binarios, la recuperación exacta de las tres parejas, las seis continuaciones y su inferencia. C1 reduce el sesgo regional en dos parejas y lo aumenta en la tercera; el error de borde empeora en las tres y ninguna satisface los ocho controles. La [revisión independiente](objetivo-2/REVISION_REPETICION_F6518FF.md) confirma dependencia de la semilla o compromiso. No se concede aceptación física ni se amplía la campaña; el siguiente paso es revisar el diseño científico y los criterios de aceptación. El OE2 permanece abierto.

**Estado del OE1 — 2026-10-03: cumplido y cerrado por decisión de la dirección bajo el alcance idealizado adoptado.** Datos, distribución, justificación e informe específico completos. [Registro de cierre](objetivo-1/CIERRE_OE1.md). No se requieren nuevas corridas para este alcance; no se declara aprobada la tesis completa.

| Documento | Contenido |
|---|---|
| [Informe de cierre del OE1](objetivo-1/manuscrito/README.md) | Informe con figuras integradas, nomenclatura, formulación matemática y justificación. |
| [Ficha del conjunto](objetivo-1/FICHA_CONJUNTO_OE1.md) | Datos, campos, receta, particiones, versiones, límites y reproducción. |
| [Síntesis de resultados y figuras](objetivo-1/SINTESIS_RESULTADOS_OE1.md) | Texto para el informe y tres figuras exportables en PNG/PDF. |
| [Definición y criterios de cierre](objetivo-1/DEFINICION_PRODUCTO_OE1.md) | Alcance adoptado y evidencia de A-01 a A-08. |
| [Matriz de cumplimiento](objetivo-1/MATRIZ_CUMPLIMIENTO.md) | Aspectos verificados y límites de la conclusión. |
| [Pendientes](objetivo-1/PENDIENTES.md) | P-01 a P-05 resueltos dentro del alcance aceptado. |
| [Revisión directa f395570](objetivo-1/REVISION_DATOS_F395570.md) | 477 huellas, evaluación desde píxeles y reproducción de 9.120 pares. |
| [Distribución verificada](objetivo-1/REVISION_DISTRIBUCION_DRIVE.md) | Descarga independiente, integridad y procedimiento reproducible. |
| [Índice documental](docs/INDICE.md) | Herramientas, protocolos y revisiones anteriores. |

La campaña contiene 19 escenarios idealizados con seis vistas, 344 millones de primarios por vista y 39.216 millones en total. Cumplen el criterio 1.710 regiones de borde; 107/114 vistas alcanzan la meta descriptiva de roca. Se conservan las siete excepciones y el 94,944 % global de ROI con al menos 100 cuentas no sustituye los indicadores individuales.

## Datos y versiones

El conjunto corregido de `f395570` se distingue del catálogo histórico conservado en `objetivo-1/originales/`. Los históricos no se convierten en referencias finales por renombrarlos. Las entregas estudiantiles permanecen en su rama; esta documentación las revisa sin fusionarlas automáticamente.

`objetivo-1/evidencias/` contiene las verificaciones; `objetivo-1/figuras/` los gráficos; `herramientas/` los procedimientos reproducibles. Los archivos grandes de trabajo local se guardan en `trabajo/`, fuera del historial Git. Consultar [procedencia](docs/PROCEDENCIA.md), [ficha actual](objetivo-1/FICHA_CONJUNTO_OE1.md) y [versiones locales](requirements-oe1-local.txt).

La cronología permanece en el [registro de cambios](CHANGELOG.md), la [bitácora](objetivo-1/BITACORA.md) y los informes fechados. Se retiraron de esta entrada los avisos de preparación y recepción ya superados. No se certifica un detector real.

## Apertura del OE2 — revisión inicial

Por autorización expresa de la dirección se incorpora la [revisión de la implementación estudiantil](objetivo-2/README.md). Existe una cWGAN-GP reutilizable y se comprobó la compatibilidad de 7.200 pares de entrenamiento/validación. La penalización del crítico, la normalización y la identidad de los datos se corrigieron en una [implementación derivada v1](objetivo-2/CORRECCIONES_V1.md), con 17 controles y reanudación exacta en una prueba técnica de entrenamiento. El OE2 permanece pendiente de protocolo y entrenamiento prolongado; no se declara desempeño final.

El [piloto al 5 %](objetivo-2/PROTOCOLO_PILOTO_F05.md) está diseñado: comparación U-Net/cGAN, prueba técnica con reanudación y hasta 30 épocas antes de presupuestar la campaña principal. Se incluyen [instrucciones para SC3](objetivo-2/INSTRUCCIONES_PILOTO_SC3.md); la [entrega GPU RunPod fue revisada](objetivo-2/REVISION_PILOTO_C054225.md): ambas redes mejoran la entrada y U-Net supera a cGAN en las métricas de este piloto. La [verificación independiente de los pesos](objetivo-2/REVISION_PESOS_PILOTO_F05.md) reproduce las métricas de ambos modelos en 360 pares de validación. La [evaluación con regiones geométricas](objetivo-2/EVALUACION_GEOMETRICA_PILOTO_F05.md) detecta sesgos de cuentas distintos entre cielo, roca y anomalías. La aceptación física permanece pendiente; se diseñó el ajuste acotado antes de ampliar.

El [ajuste acotado de conservación de cuentas](objetivo-2/DISENO_AJUSTE_CUENTAS_F05.md) está diseñado: dos continuaciones pareadas de U-Net y un término regional verificado en CPU. La integración y la recuperación exacta ya se verificaron mediante entrenamiento técnico en CPU. La [entrega de las dos continuaciones fue revisada independientemente](objetivo-2/REVISION_AJUSTE_A6AA6B8.md): doce binarios íntegros, recuperación exacta y 720 inferencias reproducidas. El resultado es un compromiso: menor sesgo regional, con deterioro de borde/PSNR frente al control y sesgo persistente en el cuerpo denso. Se documenta una [propuesta de continuación cGAN](objetivo-2/PROPUESTA_CONTINUACION_CGAN_F05.md), ya implementada y verificada en CPU. La [entrega CG-04c y sus cinco épocas ya se verificaron](objetivo-2/REVISION_BINARIOS_CG04C.md). Su valoración motivó la repetición de tres parejas indicada al inicio; no se presenta el ensayo anterior como pendiente.


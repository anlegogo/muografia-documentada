# Revisión independiente de los binarios CG-04

Fecha de revisión: 2026-10-03, America/Bogota (2026-10-04 UTC).

**Resultado: recepción e integridad verificadas; incidencia de recuperación CUDA pendiente.** No se concede aceptación GPU ni se habilitan las continuaciones de cinco épocas.

## Procedencia y controles

Se revisó la entrega estudiantil de `oe2/continuacion-cgan-f05`: trazas congeladas en `c45a1a1cea72bdc3966bdd916408a591b45738dd` y publicación de la verificación Drive en `65ab85c2b880e7cc71d80780e918140b696e2ac8`. El diagnóstico utilizado corresponde a `main` `0c789d7`; su SHA-256 coincide con la identidad registrada.

Se descargaron desde la [carpeta compartida](https://drive.google.com/drive/folders/1Jjg7MofdRF4QpdcARYW1RvgUgrO8Y6I6) los 22 binarios: 14 checkpoints y ocho arreglos de predicciones, 3 933 371 732 bytes. Los 22 tamaños y SHA-256 coinciden con el inventario. La descarga se realizó por los enlaces públicos porque el conector rechazó los checkpoints de 279 756 678 bytes por superar su límite de 268 435 456 bytes.

La auditoría local cargó los checkpoints con `torch.load(..., map_location='cpu', weights_only=True)`; no ejecutó entrenamiento CUDA. Se verificaron valores de redes, estados y pasos de Adam y RNG contra las huellas de frontera y los últimos eventos de las trazas. Los checkpoints idénticos por SHA-256 de repetida y recarga se identificaron como copias exactas de los continuos.

Se verificaron también las huellas de los tres shards de validación y se recalcularon SSIM y PSNR con las ocho predicciones de cada ejecución y las referencias normalizadas según el contrato. Las métricas coinciden con lo declarado dentro de 1e-12. No se abrió test ni se estimó generalización. La [evidencia de auditoría](evidencias/revision-binarios-cg04.json) conserva las huellas, diferencias por tensor, momentos Adam, entorno y métricas independientes.

## Hallazgos

1. El checkpoint de época 1 coincide en valores con las fronteras de las cuatro modalidades de cada variante. Las diferencias de ubicación entre el archivo CPU y la ejecución CUDA no implican cambios numéricos.
2. Continua, repetida y recarga tienen checkpoints finales y predicciones idénticos en C0 y C1.
3. En reanudada, los estados aleatorios finales coinciden con continua; los pasos Adam son correctos: cuatro pasos G y veinte D al final. Las redes y los momentos de Adam presentan diferencias numéricas.
4. Los estados finales leídos de los binarios coinciden con las huellas de los últimos eventos de las trazas.
5. La comparación independiente de las 76 entradas por traza confirma que el primer evento diferente en ambas variantes es el índice 6, `epoch2/batch0/D/gradients`: `net.0.bias`, `net.0.weight`, `net.2.weight` y `net.5.weight`. Las seis entradas previas coinciden. En total difieren 68 eventos en C0 y 66 en C1.

| Continua frente a reanudada | C0 | C1 |
|---|---:|---:|
| Máxima diferencia absoluta en G | 2,9351562e-5 | 4,1216612e-5 |
| Máxima diferencia absoluta en D | 4,9155205e-6 | 6,3781663e-6 |
| Máxima diferencia absoluta en predicciones normalizadas | 1,5698373e-5 | 2,3946166e-5 |
| Diferencia absoluta media en predicciones | 2,7116567e-7 | 3,9219451e-7 |
| SSIM continua | 0,8222093776973222 | 0,8220471350685156 |
| SSIM reanudada | 0,8222097180625256 | 0,8220474095815962 |

La diferencia no se limita a las métricas: se encuentra directamente en los estados de las redes. Su magnitud en esta prueba corta no permite garantizar su efecto tras cinco épocas ni justificar automáticamente una tolerancia.

## Interpretación y siguiente comprobación

La evidencia respalda que la serialización y la restauración de los estados registrados conservan sus valores. La primera divergencia observada se encuentra en los gradientes del crítico antes de actualizarlo, al usar un proceso nuevo. No se ha identificado un kernel ni una causa definitiva; la igualdad de los valores de la pérdida y de los forwards no demuestra igualdad de todas las operaciones internas de derivación.

CG-04 conserva estado **parcial**: recepción, integridad y correspondencia de los resultados verificadas; resolución de la discrepancia pendiente. Ya no se necesita solicitar de nuevo estos archivos a los estudiantes. Los binarios originales de los intentos anteriores no se conservaron, según la entrega; esta auditoría corresponde al diagnóstico CG-04.

La siguiente comprobación debe aislar, con el mismo lote y estado de época 1, las contribuciones al gradiente del crítico de la pérdida Wasserstein y de la penalización de gradiente. Debe comparar proceso continuo y proceso nuevo sin pasos de optimización que mezclen los efectos, conservar el estado aleatorio y controlar que la suma reconstruya el gradiente total. Esto delimitará si la discrepancia aparece en una contribución o en su acumulación; es un diseño de comprobación pendiente, no una corrección validada.

Se mantienen los criterios exactos y la suspensión de las continuaciones. Cualquier cambio de criterio requerirá justificación metodológica documentada. El diagnóstico de reanudación no constituye una evaluación del cumplimiento científico del OE2.

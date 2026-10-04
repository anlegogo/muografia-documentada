# Verificación independiente de la entrega CG-04c

## Resultado y alcance

Fecha de revisión: 2026-10-04, America/Bogota. La ejecución estudiantil y la publicación de archivos declaran 2026-10-04 UTC. Se fija la entrega en [1ec1c24](https://github.com/anlegogo/muografia-documentada/tree/1ec1c242f7899c76b34e0f0f2bd02f1063775568/objetivo-2/entregas/2026-10-03-continuacion-cgan-f05), con ejecución del código `02ce48a6f2986c931149f26a9a7e66e0a8495156`, que incorpora `4fc3bd5`.

**CG-04: verificado y cerrado para el entorno y la batería entregados.** La recuperación exacta se confirma desde los binarios. CG-02 queda verificado para esa ejecución GPU; CG-03 tiene las dos continuaciones y su evaluación verificadas. Esto no equivale a aceptación física ni al cierre del OE2.

## Archivos, estados y datos

Se descargaron los 13 binarios de la [carpeta Drive](https://drive.google.com/drive/folders/1sCnyxugko3_H3fpkUwZVGX4syaarqTOp): seis checkpoints y siete arreglos de predicciones. Coinciden sus tamaños y SHA-256: 1.970.094.884 bytes. La [evidencia independiente](evidencias/revision-binarios-cg04c.json) conserva el inventario y las comprobaciones.

Se cargaron los checkpoints mediante `torch.load(weights_only=True, map_location='cpu')`. La auditoría técnica volvió a comparar G, D, ambos Adam, RNG, registros numéricos y predicciones entre entrenamiento continuo y recuperado: igualdad exacta en C0 y C1. Se verificaron las cuatro identidades y huellas contra la aceptación publicada; no se aceptó únicamente su bandera JSON.

Los dos checkpoints finales corresponden a la quinta época adicional, con 1.800 actualizaciones G y 9.000 D por variante. Se verificaron estados finitos, contadores, fuentes, configuración, índices, exportaciones y resúmenes. Las fuentes coinciden con la corrección validada y publicada.

Los datos train/val se verificaron contra el contrato. El manifiesto de máscaras entregado coincide con la identidad de las ejecuciones. Las máscaras locales coinciden en contenido, geometrías, protocolo, soporte y metadatos; para esa comparación solo se excluyeron las huellas de los contenedores NPZ comprimidos. No se abrieron test ni generalización.

## Reproducción de evaluación e inferencia

Se recalcularon las tablas mediante `evaluar_ajuste_cgan.tables`, usando los 360 índices de validación, las predicciones descargadas y las referencias verificadas. Los 5.334 campos flotantes comparados difieren como máximo 1,7763568394002505e-15. Se comprobaron también campos no numéricos y los 24 registros por anomalía.

Se ejecutaron 1.080 inferencias CPU: 360 de C0, 360 de C1 y 360 de la cGAN inicial, cargando los pesos verificados.

| Modelo | Diferencia máxima de píxel CPU–CUDA | Diferencia SSIM | Diferencia PSNR (dB) |
|---|---:|---:|---:|
| C0 | 8.61287e-6 | 1.75827e-9 | 2.69118e-7 |
| C1 | 7.89762e-6 | 4.37392e-9 | 9.65123e-8 |
| inicial_cgan | 3.93391e-6 | 2.62286e-9 | 1.26913e-7 |


Las tolerancias de contraste de inferencia entre CPU y CUDA son 1e-4 por píxel, 1e-5 en SSIM y 1e-3 dB en PSNR. Son distintas de la aceptación técnica de recuperación, que continúa exigiendo igualdad exacta. No se repitió entrenamiento GPU localmente.

## Resultado científico

| Indicador | Entrada | cGAN inicial | C0 | C1 |
|---|---:|---:|---:|---:|
| Q regional (%) | 1,814 | 12,340 | 7,204 | 4,765 |
| SSIM | 0,75181 | 0,82279 | 0,81487 | 0,81570 |
| PSNR (dB) | 24,168 | 31,104 | 30,572 | 30,646 |

Se reproduce la clasificación `mejora_concordante_descriptiva`: C1 satisface los ocho controles frente a C0 y reduce Q un 33,85 %. Sin embargo, ambas continuaciones tienen menor SSIM/PSNR que el modelo inicial. C1 empeora Q en geo-val-01 respecto del inicial; entre las 24 combinaciones de vista/anomalía, empeora la magnitud del sesgo medio en ocho frente a C0 y en cinco frente al inicial. La magnitud del sesgo medio no debe confundirse con la media de los sesgos absolutos por realización.

La entrada sin red conserva un Q menor que C1, aunque tiene SSIM y PSNR inferiores. Mejor calidad de imagen y mejor conservación de cuentas no son intercambiables.

Es una sola semilla de entrenamiento y tres geometrías de validación, con veinte realizaciones por vista. Las realizaciones no equivalen a entrenamientos independientes. Se conserva `physical_acceptance: false`; no se atribuye al ensayo significación estadística ni generalización.

## Límites y siguiente decisión

El entorno estudiantil declara L40S, PyTorch 2.6.0+cu118 y controlador 570.124.06. El diagnóstico previo CG-04b utilizó controlador 595.91.07: esta aceptación demuestra funcionamiento del conjunto de código y entorno actual, pero no aísla causalmente el efecto de la corrección frente al cambio de controlador.

La comprobación pendiente de archivos queda resuelta. No se requiere repetir estas cinco épocas por una deficiencia de entrega. La siguiente decisión consiste en valorar el compromiso entre conservación regional y fidelidad de imagen y fijar el protocolo de repetición/comparación antes de ampliar el entrenamiento. No se lanza automáticamente la campaña principal ni se modifica la regla de decisión a posteriori.

## Procedimiento e incidencias

Se utilizaron las herramientas de auditoría y evaluación fijadas en `4fc3bd5`, con PyTorch CPU y dos hilos. La revisión primero valida integridad y estados, después recalcula las tablas y finalmente ejecuta inferencia con los pesos. El script local de revisión y su huella se identifican en la evidencia.

El primer recálculo se detuvo porque el script de revisión pasó índices como tuplas y el evaluador exige listas serializadas. Se corrigió la representación, manteniendo orden y contenido; no se modificaron datos, fuentes científicas ni criterios. La auditoría definitiva se completó después de esa corrección.

# Revisión independiente de CG-04b

## Resultado y alcance

**CG-04 permanece parcial.** Se verificó la entrega estudiantil de separación de gradientes: los componentes Wasserstein y penalización coinciden exactamente entre proceso continuo y proceso nuevo; el gradiente de la pérdida conjunta sigue discrepando. No se habilitan las continuaciones de cinco épocas ni se modifica la aceptación exacta.

Revisión: 2026-10-04, America/Bogota. El informe estudiantil declara ejecución del 2026-10-04 UTC. Entrega fijada en [0f6ec2f](https://github.com/anlegogo/muografia-documentada/blob/0f6ec2fa8675dd866772d2ce6d783f681f297eca/objetivo-2/entregas/2026-10-03-continuacion-cgan-f05/DIAGNOSTICO_CG04B.md), rama `oe2/continuacion-cgan-f05`; código ejecutado `dd90bd744a42778f7cb2f82fe813f41fecb6b444`, que incorpora `a259615`. Se conserva la entrega en su rama.

## Evidencia verificada

Se descargaron 22 binarios desde el [directorio publicado](https://drive.google.com/drive/folders/1TgQNOXAHLg3JNfu4u3oV3feCqGdEwpNk): veinte archivos de gradientes y dos checkpoints de época 1, 780598748 bytes en total. Todos coinciden en tamaño y SHA-256 con el inventario. La [evidencia independiente](evidencias/revision-binarios-cg04b.json) conserva las huellas y los resultados recalculados.

Se cargaron los archivos mediante `torch.load(weights_only=True, map_location="cpu")`. Se reprodujeron las comparaciones con `compare_all` de [la herramienta CG-04b](herramientas/aislar_gradientes_cgan.py), sin ejecutar entrenamiento ni CUDA localmente. Los 580 campos numéricos flotantes de ambas comparaciones coinciden con los declarados, con diferencia máxima cero; también se comprobaron claves, tipos, indicadores y campos no flotantes. Los checkpoints coinciden con las diez fronteras registradas por brazo; los contadores Adam corresponden a dos pasos G y diez D. Las identidades de fuentes y de la herramienta coinciden.

Entorno de ejecución estudiantil: NVIDIA L40S, PyTorch 2.6.0+cu118, CUDA 11.8, cuDNN 9.1.0, Python 3.12.3 y NumPy 2.3.5. El recálculo independiente usa PyTorch CPU; verifica artefactos de aquella ejecución, sin certificar otra GPU.

## Comparación entre proceso continuo y nuevo

| Gradiente | Máxima diferencia absoluta C0 | Máxima diferencia absoluta C1 |
|---|---:|---:|
| Original | 4.172325134277344e-7 | 4.246830940246582e-7 |
| Repetición del original | 4.172325134277344e-7 | 4.246830940246582e-7 |
| Total explícito | 4.172325134277344e-7 | 4.246830940246582e-7 |
| Wasserstein aislado | 0 | 0 |
| Penalización ponderada aislada | 0 | 0 |

Dentro de cada condición, original, repetición y total explícito coinciden exactamente. Las comprobaciones pareadas de estados, entradas, RNG, forwards y pérdida total escalar son satisfactorias. La diferencia del gradiente conjunto se encuentra en `net.0.weight`, `net.0.bias`, `net.2.weight` y `net.5.weight`.

Si se escribe la pérdida como $L_D=L_W+\lambda_{GP}L_{GP}$, su gradiente matemático es la suma de las dos contribuciones. En aritmética finita, una sola derivación del grafo conjunto y la suma posterior de gradientes aislados pueden seguir órdenes de operación distintos. La suma offline incluida en la evidencia no reproduce el orden interno de CUDA y no constituye una tolerancia de aceptación.

## Interpretación y siguiente paso

La evidencia acota la discrepancia a la ruta de derivación conjunta en estas condiciones; no identifica por sí sola un kernel específico ni demuestra una causa definitiva. Tampoco mide la calidad de reconstrucción de las continuaciones.

Se propone preparar una variante controlada que calcule por separado ambas contribuciones y las combine en orden fijo antes de un único paso del optimizador del crítico. Esta variante todavía no está implementada ni validada. Deberá preservar la pérdida, los cinco pasos D por G y los estados del entrenamiento; después deberá superar la comprobación técnica completa de recuperación exacta en GPU, incluidos modelos, optimizadores, RNG, registros y predicciones. Solo entonces corresponde proceder conforme a las [instrucciones C0/C1](INSTRUCCIONES_CONTINUACION_CGAN_F05.md). No se recomienda sustituir el criterio por una tolerancia elegida a partir de esta discrepancia.

## Incidencia documental

Se confirmó el aviso estudiantil: `evidencias/revision-binarios-cg04.json` contenía 2168 saltos CRLF y un salto LF aislado, frente a la regla LF del repositorio. Se normalizó ese archivo a LF y se comprobó igualdad del JSON antes y después. Las huellas de ambas representaciones quedan en la evidencia de esta revisión. La corrección es de formato y no modifica herramientas, configuraciones ni resultados científicos.

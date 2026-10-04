# Incidencia: recuperación inexacta de la cGAN en GPU

2026-10-03 (Colombia). Continuación cGAN C0/C1 según las [instrucciones](../../INSTRUCCIONES_CONTINUACION_CGAN_F05.md), con el código de `main` en `04b2e46` sin modificaciones. La etapa técnica superó todos sus pasos, pero la aceptación GPU falla. Por eso no se ejecutaron las continuaciones de cinco épocas. Esta entrega reúne registros, comandos, entorno y diagnóstico, y una [propuesta](PROPUESTA_TOLERANCIA_RECUPERACION.md) para la decisión de la dirección.

## 1. Intentos

| | Intento 1 | Intento 2 |
|---|---|---|
| Equipo | Pod RunPod con 1 × NVIDIA L40S, driver 570.124.06 | Pod RunPod distinto con 1 × NVIDIA L40S, driver 595.91.07 |
| Entorno | Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.3.5, SciPy 1.18.1, scikit-image 0.26.0, Matplotlib 3.11.1, filelock 3.16.1 | El mismo, instalado con el mismo script |
| Datos | 30 shards de train/val y `best.pt` cGAN `e54d51f7…`: 31 de 31 huellas | 31 de 31 huellas |
| Máscaras y 6 ejecuciones técnicas | Código 0 | Código 0 |
| `revisar_ajuste_cgan.py --exigir-gpu` | `ValueError: Recuperación distinta: generator` | El mismo error |
| Evidencia | Completa en [datos/intento-1/](datos/intento-1/): comandos, stdout, stderr, códigos, entorno, historiales, identidades y resúmenes | [Transcripción de consola](datos/intento-2/salidas-consola.json); el pod se apagó antes de copiar sus archivos |

Los comandos son los literales de las instrucciones, ejecutados con [lanzar.sh](verificacion/lanzar.sh) después de [instalar_entorno.sh](verificacion/instalar_entorno.sh) y [sincronizar_datos.py](verificacion/sincronizar_datos.py). Cada comando efectivo está en `datos/intento-1/logs/*.comando.txt`.

## 2. Diagnóstico

1. **La diferencia aparece después de reanudar.** En C0 y C1, la ejecución continua y la recuperada coinciden bit a bit en la época 1 y difieren en la época 2. Las métricas cambian del orden de 1e-7 relativo; el SSIM técnico de C0 es 0,8222094 frente a 0,8222097 ([historiales del intento 1](datos/intento-1/tecnica/tecnica/)).
2. **La GPU es determinista entre procesos con la misma historia.** Una segunda ejecución continua de C0 reprodujo bit a bit los pesos de la primera en las dos épocas ([diagnóstico](datos/intento-1/diagnostico/), [registro](datos/intento-1/diagnostico-C0-continua-2.log)).
3. **El estado guardado está completo.** [diagnosticar_reanudacion_cgan.py](verificacion/diagnosticar_reanudacion_cgan.py) usa las funciones del ejecutor sin cambios.
   - Ejecuta la época 1 y luego la época 2 de cinco maneras dentro de un mismo proceso: continua, recarga completa, solo RNG, solo optimizadores y solo redes.
   - La continua reproduce la ejecución continua registrada.
   - Las cuatro variantes posteriores dan el mismo resultado entre sí, incluida la que solo restaura el RNG recién guardado, que no altera el estado. Ese resultado es distinto de la continua y de la recuperada.
   - La época 2 depende, por tanto, de lo que el proceso ejecutó antes, no del estado serializado.
4. **No lo resuelven variables de entorno** ([probar_entornos.sh](verificacion/probar_entornos.sh)):
   - `PYTORCH_NO_CUDA_MEMORY_CACHING=1` reproduce las mismas huellas, lo que descarta el asignador de memoria.
   - `TORCH_CUDNN_V8_API_DISABLED=1` cambia los valores, pero mantiene la discrepancia.
   - `CUDA_MODULE_LOADING=EAGER` no cambia nada.
5. **La magnitud es pequeña.** C0, época 2, continua frente a recuperada:

   | Elemento | Tensores distintos | Diferencia absoluta máxima |
   |---|---|---|
   | Generador | 45 de 46 | 2,9e-5 (`enc1.0.bias`, escala 0,33) |
   | Crítico | 6 de 7 | 4,9e-6 |
   | Predicciones en la escala normalizada [0, 1) | — | 1,6e-5; diferencia media 2,7e-7 |

**Interpretación.** El redondeo de punto flotante de los kernels CUDA depende del historial del proceso, en una cGAN con penalización de gradiente de segundo orden. El mecanismo concreto no se identificó.

La dirección verificó la recuperación exacta de este ejecutor en CPU, y el ejecutor del ajuste U-Net, sin crítico, superó la misma prueba en esta GPU. Igualar bit a bit la ejecución continua y la recuperada en CUDA no fue posible con el código y el entorno actuales.

## 3. Estado

- No se modificaron herramientas, configuraciones ni criterios. Las continuaciones de cinco épocas no se ejecutaron, porque el ejecutor exige la aceptación GPU.
- La decisión sobre cómo continuar corresponde a la dirección. La [propuesta](PROPUESTA_TOLERANCIA_RECUPERACION.md) describe una alternativa sin aplicarla.

# Diagnóstico CG-04 de la recuperación cGAN en GPU

2026-10-03 (Colombia). Ejecución del [diagnóstico de la dirección](../../DIAGNOSTICO_RECUPERACION_CGAN.md) con `diagnosticar_recuperacion_cgan.py` sin modificaciones. Solo se ejecutó el diagnóstico: no se lanzaron continuaciones de cinco épocas. El diagnóstico declara `gpu_accepted: false`.

## Condiciones

| Elemento | Valor |
|---|---|
| Código | Rama `oe2/continuacion-cgan-f05` en `558ad1d791ffbd34552d515e8e6651a25d81db11`, merge de `main` `0c789d7`. Clon Git en el pod desde un bundle de la rama; `git status --short` vacío ([commit.txt](datos/diagnostico-cg04/diagnostico-cgan/commit.txt), [git-status.txt](datos/diagnostico-cg04/diagnostico-cgan/git-status.txt)) |
| Equipo | Pod RunPod con 1 × NVIDIA L40S, driver 570.124.06 ([nvidia-smi.txt](datos/diagnostico-cg04/diagnostico-cgan/nvidia-smi.txt)) |
| Entorno | El mismo del intento 1: Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.3.5, SciPy 1.18.1, scikit-image 0.26.0, Matplotlib 3.11.1, filelock 3.16.1 ([pip-freeze.txt](datos/diagnostico-cg04/diagnostico-cgan/pip-freeze.txt), [python-torch.txt](datos/diagnostico-cg04/python-torch.txt)) |
| Datos | 30 shards de train/val y `best.pt` cGAN `e54d51f7…`: 31 de 31 huellas ([datos.log](datos/diagnostico-cg04/datos.log)). Máscaras generadas con `datos_ajuste.py` ([manifiesto](datos/diagnostico-cg04/manifiesto-mascaras.json)) |
| Comandos | Los literales de la guía, con `CUDA_VISIBLE_DEVICES=0` y `CUBLAS_WORKSPACE_CONFIG=:4096:8` ([diagnostico_pod.sh](verificacion/diagnostico_pod.sh)) |

Los ocho procesos, cuatro por rama, terminaron como `completada` y el script terminó con código 0 ([diagnostico.log](datos/diagnostico-cg04/diagnostico.log)).

## Resultados

| Rama | Comparación | Estado en la frontera | Primera diferencia | Eventos distintos | Predicción: dif. máx. / media | SSIM técnico |
|---|---|---|---|---:|---|---|
| C0 | repetida | igual | ninguna | 0 | 0 / 0 | 0,8222094 = 0,8222094 |
| C0 | recarga | igual | ninguna | 0 | 0 / 0 | 0,8222094 = 0,8222094 |
| C0 | reanudada | igual | `epoch2/batch0/D/gradients` | 68 | 1,57e-5 / 2,71e-7 | 0,8222094 frente a 0,8222097 |
| C1 | repetida | igual | ninguna | 0 | 0 / 0 | 0,8220471 = 0,8220471 |
| C1 | recarga | igual | ninguna | 0 | 0 / 0 | 0,8220471 = 0,8220471 |
| C1 | reanudada | igual | `epoch2/batch0/D/gradients` | 66 | 2,39e-5 / 3,92e-7 | 0,8220471 frente a 0,8220474 |

Fuentes: [C0/diagnostico.json](datos/diagnostico-cg04/diagnostico-cgan/C0/diagnostico.json) y [C1/diagnostico.json](datos/diagnostico-cg04/diagnostico-cgan/C1/diagnostico.json).

**Lectura según los criterios de la guía.**

- **El control es estable con la instrumentación.** «continua» y «repetida» coinciden en ambas ramas.
- **El estado no cambia al cargar.** En «reanudada», `restore-check.json` declara `values_equal: true`. Las diferencias de metadatos corresponden a la ubicación CPU/CUDA de los tensores cargados, que la guía pide informar por separado. La comparación en la frontera de la época 2 tampoco muestra diferencias de valores ni de metadatos.
- **La recarga en el mismo proceso es exacta.** Cargar redes, Adam y RNG en los mismos objetos reproduce la continua sin diferencias.
- **La primera diferencia está en los gradientes del crítico, solo en un proceso nuevo.** En la traza de «reanudada», el inicio del lote, el forward de G, los tres forward de D y la pérdida de D del primer lote de la época 2 son idénticos a la continua. La primera diferencia aparece en los gradientes de D (capas `net.0`, `net.2` y `net.5`), antes de la primera actualización. Desde ahí se propaga a los eventos siguientes.

El evento señalado delimita la siguiente comprobación: el backward de la pérdida del crítico, que incluye la penalización de gradiente de segundo orden, en el primer cálculo de un proceso nuevo con estado idéntico. Las huellas localizan una operación observada; no identifican un kernel ni una causa definitiva.

## Archivos binarios

Los 22 binarios (`epoch1.pt`, `epoch2.pt` y `predicciones-val.npy` de las ocho ejecuciones) suman 3,94 GB y no se versionan. Sus rutas, tamaños y huellas están en [binarios-drive.txt](datos/diagnostico-cg04/binarios-drive.txt). Se descargaron del pod y se verificaron contra los inventarios `archivos.json`: 57 de 57 archivos en C0 y 57 de 57 en C1. El enlace de Drive se agregará cuando se suban.

Los checkpoints y predicciones de la prueba técnica original no se conservaron: los pods de esos intentos se apagaron y solo se copiaron registros, historiales y JSON.

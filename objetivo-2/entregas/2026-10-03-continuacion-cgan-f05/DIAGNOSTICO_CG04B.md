# Diagnóstico CG-04b: separación de los gradientes del crítico

2026-10-04 (UTC). Ejecución del [diagnóstico de la dirección](../../DIAGNOSTICO_GRADIENTES_CG04B.md) con `aislar_gradientes_cgan.py` sin modificaciones. Solo se ejecutó el diagnóstico, que declara `gpu_accepted: false`. No se lanzaron continuaciones.

## Condiciones

| Elemento | Valor |
|---|---|
| Código | Rama `oe2/continuacion-cgan-f05` en `dd90bd744a42778f7cb2f82fe813f41fecb6b444`, merge de `main` `a259615`. Clon Git en el pod desde un bundle de la rama ([commit.txt](datos/cg04b/cg04b/commit.txt)) |
| `git status --short` | ` M objetivo-2/evidencias/revision-binarios-cg04.json` ([git-status.txt](datos/cg04b/cg04b/git-status.txt)). Ese archivo de `main` fue commiteado con finales de línea mixtos (CRLF y LF), mientras `.gitattributes` exige `eol=lf`; Git lo marca como modificado en cualquier checkout limpio. No se editó, y no es una herramienta ni una configuración |
| Equipo | Pod RunPod con 1 × NVIDIA L40S, driver 595.91.07 ([nvidia-smi.txt](datos/cg04b/cg04b/nvidia-smi.txt)) |
| Entorno | El mismo del diagnóstico CG-04: Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.3.5 ([pip-freeze.txt](datos/cg04b/cg04b/pip-freeze.txt), [python-torch.txt](datos/cg04b/python-torch.txt)) |
| Datos | 31 de 31 huellas, incluido el `best.pt` cGAN `e54d51f7…` ([datos.log](datos/cg04b/datos.log)). Máscaras con `datos_ajuste.py` ([manifiesto](datos/cg04b/manifiesto-mascaras.json)) |
| Comandos | Los literales de la guía, con `CUDA_VISIBLE_DEVICES=0` y `CUBLAS_WORKSPACE_CONFIG=:4096:8` ([cg04b_pod.sh](verificacion/cg04b_pod.sh)) |

Los 20 procesos, diez por rama, terminaron como `completada` y el script terminó con código 0 ([cg04b.log](datos/cg04b/cg04b.log)).

## Resultados

Fuentes: [C0/comparacion.json](datos/cg04b/cg04b/C0/comparacion.json) y [C1/comparacion.json](datos/cg04b/cg04b/C1/comparacion.json).

**Emparejamiento.** En ambas ramas, `paired_states_inputs_rng_forwards` es verdadero: identidad, frontera, lote, entrada y salida generada, estados aleatorios y los tres forward del crítico coinciden entre las mediciones.

**Controles.**

| Rama | Condición | original frente a repetida | original frente a total |
|---|---|---|---|
| C0 | continua / nueva | exacto, 0 / exacto, 0 | exacto, 0 / exacto, 0 |
| C1 | continua / nueva | exacto, 0 / exacto, 0 | exacto, 0 / exacto, 0 |

**Proceso continuo frente a proceso nuevo** (diferencia absoluta máxima del gradiente):

| Medición | C0 | C1 |
|---|---|---|
| original | 4,17e-7 | 4,25e-7 |
| repetida | 4,17e-7 | 4,25e-7 |
| total | 4,17e-7 | 4,25e-7 |
| solo Wasserstein, \(g_W\) | 0 (exacto) | 0 (exacto) |
| solo penalización, \(g_P\) | 0 (exacto) | 0 (exacto) |

En `original`, los parámetros que difieren son `net.0.weight`, `net.0.bias`, `net.2.weight` y `net.5.weight`, los mismos señalados por CG-04.

**Reconstrucción offline** (total explícito frente a la suma \(g_W+g_P\) calculada en CPU, diferencia absoluta máxima):

| Rama | Condición | float32 | float64 |
|---|---|---|---|
| C0 | continua | 1,19e-7 | 9,13e-8 |
| C0 | nueva | 4,17e-7 | 4,15e-7 |
| C1 | continua | 1,19e-7 | 1,06e-7 |
| C1 | nueva | 4,25e-7 | 4,25e-7 |

## Lectura según la guía

1. **Los controles son exactos.** La medición es estable entre procesos con la misma historia, y la separación explícita conserva el gradiente total.
2. **La discrepancia no aparece en ninguna contribución por separado.** Los gradientes de \(L_W\) y de \(L_P\), cada uno derivado en su propio proceso, son idénticos bit a bit en el proceso continuo y en el nuevo. Solo difieren las mediciones que derivan la suma \(L_W+L_P\) en un mismo backward.
3. **La suma explícita se separa más en el proceso nuevo.** En el continuo, el total se aparta de la suma offline en 1,2e-7. En el nuevo se aparta en 4,2e-7, lo mismo que la diferencia continua frente a nueva. Según la guía, estas diferencias offline son descriptivas: la suma en CPU no reproduce el orden interno de acumulación de CUDA.

La ruta queda delimitada a la **combinación de las dos contribuciones dentro de un mismo backward** sobre los parámetros `net.0`, `net.2` y `net.5`, y no al cálculo de cada una por separado. No se identifica un kernel ni una causa definitiva.

## Archivos binarios

Los 22 binarios (20 `gradientes.pt` y 2 `epoch1.pt`) suman 0,78 GB y no se versionan. Sus rutas, tamaños y huellas están en [binarios-drive.txt](datos/cg04b/binarios-drive.txt). Se descargaron del pod y se verificaron contra los inventarios `archivos.json`: 58 de 58 archivos en C0 y 58 de 58 en C1. Son archivos nuevos y no reemplazan los del diagnóstico CG-04. **Copia en Drive:** [carpeta cg04b](https://drive.google.com/drive/folders/1TgQNOXAHLg3JNfu4u3oV3feCqGdEwpNk), con las carpetas completas C0 y C1, registros y entorno (133 archivos, incluidos los 22 binarios listados).

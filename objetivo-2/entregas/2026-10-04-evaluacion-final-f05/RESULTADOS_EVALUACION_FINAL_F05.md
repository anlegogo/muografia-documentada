# Resultados de la evaluación final OE2 al 5 %

2026-10-04 (Colombia). Ejecución de las [instrucciones de evaluación final](../../INSTRUCCIONES_EVALUACION_FINAL_OE2.md) según el [protocolo EF-01](../../PROTOCOLO_EVALUACION_FINAL_OE2.md), con el código de `main` en `d42b763` sin modificaciones. Antes de inferir se registró la [procedencia de las particiones reservadas](PROCEDENCIA_RESERVAS.md) en el commit `a2b5318`. Ese commit no cambia código y es el que se ejecutó. No se entrenó, no se seleccionaron modelos y no se modificaron criterios.

**Alcance:** evaluación **descriptiva sobre datos potencialmente expuestos** (ver la procedencia), con fracción f = 0,05 y ocho modelos congelados. No es una evaluación confirmatoria independiente ni declara aceptación física o equivalencia (`physical_acceptance: false`, `equivalence_claim: false`).

## 1. Ejecución

| Elemento | Valor |
|---|---|
| Código | Rama `oe2/evaluacion-final-f05`, commit `a2b53186634862bc724be3d332eeb2817c84cfe1` (base `d42b763` y procedencia). Clon en el pod desde un bundle de esa rama ([commit.txt](datos/evaluacion-final-f05/registro/commit.txt)) |
| Inicio de la inferencia | 2026-10-04T17:23:15Z ([fecha-inicio.txt](datos/evaluacion-final-f05/registro/fecha-inicio.txt)); la procedencia se confirmó a las 17:20:44Z |
| Equipo | Pod RunPod con 1 × NVIDIA L40S, driver 570.195.03 ([gpu.txt](datos/evaluacion-final-f05/registro/gpu.txt)) |
| Entorno | Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.3.5, SciPy 1.18.1, scikit-image 0.26.0 y filelock 3.16.1 ([entorno.txt](datos/evaluacion-final-f05/registro/entorno.txt)); es el mismo de E1 |
| Datos | Los ocho archivos de `geo-test-01..03` y `geo-gen-01` (NPZ y metadatos) de la distribución OE1 en Drive; las huellas coinciden con el contrato |
| Pesos | Los ocho checkpoints descargados de sus enlaces de Drive y verificados por SHA-256 ([pesos.log](datos/registros/pesos.log), [fuentes-pesos.tsv](verificacion/fuentes-pesos.tsv)) |
| Preflight | `{"data_files": 8, "models": 8, "arrays_opened": false, "passed": true}` ([preflight.json](datos/evaluacion-final-f05/preflight.json)) |
| Intervalo (UTC) | Preparación 17:22:26–17:23:17; inferencia 17:23:27–17:25:33; evaluación 17:25:40–17:26:24 ([estado.log](datos/registros/estado.log)) |

Los comandos son los de la guía para una GPU, en tres etapas:

- [etapa0_preparar.sh](verificacion/etapa0_preparar.sh): preflight.
- [etapa1_inferencia.sh](verificacion/etapa1_inferencia.sh): bucle `infer` de los ocho modelos con `--device cuda`.
- [etapa2_evaluacion.sh](verificacion/etapa2_evaluacion.sh): `evaluate` una sola vez, con el informe en `informe-v1`.

Todos terminaron sin error.

**Tiempo de inferencia por modelo** (480 predicciones, `completed.json`):

| Modelo | Tiempo |
|---|---:|
| `unet_original` | 12,6 s |
| `cgan_original` | 15,3 s |
| `B1_C0` | 17,8 s |
| `B1_C1` | 14,0 s |
| `B2_C0` | 3,5 s |
| `B2_C1` | 3,5 s |
| `B3_C0` | 13,8 s |
| `B3_C1` | 14,3 s |

La evaluación en CPU tardó 44 s.

**Lecturas literales e incidencias.**

1. **Se usó RunPod en lugar de SC3**, con 1 GPU.
2. **Estado de Git.** `main` `d42b763` mantiene nueve archivos confirmados con CRLF: las configuraciones `borde-cgan-v1/B*-C*.json` y tres evidencias. Git los marca como modificados en cualquier copia limpia. Se verificó que son idénticos byte a byte a `HEAD` ([estado-git.txt](datos/evaluacion-final-f05/registro/estado-git.txt)). Ninguno forma parte de las fuentes fijadas por el contrato, cuyo control superó el preflight.
3. **Inventario del entorno.** Se generó con `uv pip freeze`, porque el entorno virtual creado con `uv` no incluye `pip`.

## 2. Resumen por partición

Las cifras son macropromedios por geometría de [evaluacion-final.json](datos/evaluacion-final-f05/informe-v1/evaluacion-final.json). Se informan 4.320 registros de imagen (480 por método, nueve métodos), 1.134 registros regionales y 54 combinaciones de contraste: 48 estimables y 6 con geometría insuficiente. Q, cielo y borde están en porcentaje respecto de las cuentas de referencia. El borde es el error espacial normalizado. Ninguna región quedó como no estimable y Q está completo en las cuatro geometrías.

**Test** (360 imágenes por método; contraste sobre 30 combinaciones comunes):

| Método | SSIM | PSNR (dB) | Q (%) | Error de contraste | Borde test-01 / 02 / 03 (%) |
|---|---:|---:|---:|---:|---|
| Entrada sin red | 0,7643 | 24,258 | 1,832 | 0,3366 | 11,57 / 12,04 / 13,53 |
| `unet_original` | 0,8545 | 33,074 | 22,388 | 0,0932 | 6,89 / 6,76 / 7,24 |
| `cgan_original` | 0,8342 | 31,170 | 14,566 | 0,1351 | 14,49 / 13,45 / 14,44 |
| `B1_C0` | 0,8277 | 30,839 | 5,825 | 0,1329 | 11,10 / 10,44 / 11,79 |
| `B1_C1` | 0,8278 | 30,849 | 4,821 | 0,1006 | 6,74 / 6,57 / 8,11 |
| `B2_C0` | 0,8274 | 30,772 | 3,996 | 0,1127 | 11,29 / 10,88 / 11,87 |
| `B2_C1` | 0,8273 | 30,770 | 4,727 | 0,1089 | 6,83 / 6,73 / 7,75 |
| `B3_C0` | 0,8263 | 30,729 | 4,828 | 0,1169 | 11,03 / 10,61 / 13,08 |
| `B3_C1` | 0,8273 | 30,768 | 5,480 | 0,1277 | 6,82 / 6,87 / 8,34 |

**Generalización** (`geo-gen-01`, 120 imágenes por método; contraste sobre 16 combinaciones comunes):

| Método | SSIM | PSNR (dB) | Q (%) | Cielo (%) | Borde (%) | Error de contraste |
|---|---:|---:|---:|---:|---:|---:|
| Entrada sin red | 0,7502 | 23,904 | 1,093 | 6,81 | 12,00 | 0,2713 |
| `unet_original` | 0,8454 | 32,883 | 26,505 | 4,68 | 6,66 | 0,0730 |
| `cgan_original` | 0,8252 | 31,047 | 16,959 | 14,56 | 13,40 | 0,0885 |
| `B1_C0` | 0,8161 | 30,485 | 3,808 | 3,10 | 10,29 | 0,1013 |
| `B1_C1` | 0,8151 | 30,509 | 4,323 | 2,26 | 6,60 | 0,1376 |
| `B2_C0` | 0,8145 | 30,331 | 4,131 | 2,16 | 10,65 | 0,1135 |
| `B2_C1` | 0,8154 | 30,403 | 4,755 | 2,14 | 6,65 | 0,0996 |
| `B3_C0` | 0,8149 | 30,404 | 4,054 | 2,53 | 10,55 | 0,0760 |
| `B3_C1` | 0,8146 | 30,371 | 2,271 | 2,14 | 6,88 | 0,0779 |

Las cifras por geometría, vista, realización y región están en [imagenes.csv](datos/evaluacion-final-f05/informe-v1/imagenes.csv), [regiones.csv](datos/evaluacion-final-f05/informe-v1/regiones.csv) y en el JSON completo. Pueden reproducirse con [resumen_evaluacion_final.py](verificacion/resumen_evaluacion_final.py).

## 3. Comparaciones prospectivas

Las nueve comparaciones fijadas por el protocolo se clasificaron como `tradeoff_or_deterioration`: cuatro pares en test y en generalización, más C1 frente a C0 en B1–B3. Ninguna fue `no_deterioration_in_listed_metrics` ni `incomplete`. La clasificación no implica significación ni superioridad estadística (`statistical_superiority: false`).

En test, las diferencias candidato menos comparador, para las tres geometrías:

- **cGAN original frente a la entrada.**
  - Mejora: SSIM +0,058 a +0,077 y PSNR +6,6 a +7,1 dB; reduce el error de contraste entre 0,18 y 0,22.
  - Empeora: Q aumenta entre 2,2 y 25,9 puntos, y los errores de cielo y borde también aumentan.
- **U-Net original frente a la entrada.**
  - Mejora: SSIM +0,075 a +0,100 y PSNR +8,6 a +9,0 dB; reduce cielo, borde y contraste.
  - Empeora: Q aumenta entre 9,3 y 33,8 puntos.
- **cGAN original frente a U-Net original.**
  - Mejora: Q es entre 7,1 y 8,5 puntos menor.
  - Empeora: SSIM baja entre 0,017 y 0,024, PSNR entre 1,8 y 2,0 dB, y los errores de cielo, borde y contraste son mayores.
- **C1 frente a C0 (B1–B3).**
  - El error espacial de borde baja en las tres geometrías de cada pareja, entre 3,7 y 4,7 puntos.
  - El error de cielo también baja en todas, como mucho 0,9 puntos.
  - Q, contraste, SSIM y PSNR cambian de signo según la pareja y la geometría, con diferencias de SSIM no mayores de 0,002 y de PSNR no mayores de 0,12 dB.

En generalización se repite el mismo patrón de signos en las seis comparaciones.

## 4. Lectura

1. **Calidad de imagen.** Todas las redes aumentan SSIM y PSNR respecto de la entrada al 5 % en las cuatro geometrías reservadas: SSIM de 0,75–0,76 a 0,81–0,86 y PSNR en 6–9 dB. La U-Net original obtiene los valores más altos.
2. **Conservación de cuentas.** La entrada sin red tiene el menor sesgo regional (Q de 1,8 % en test y 1,1 % en generalización). Las redes originales lo aumentan: U-Net 22,4 % y 26,5 %; cGAN 14,6 % y 17,0 %. Las continuaciones de E1 lo mantienen entre 2,3 y 5,8 %, con SSIM y PSNR menores que la U-Net.
3. **Término de borde.** La reducción del error espacial de borde observada en validación se repite en las cuatro geometrías reservadas para las tres parejas.
4. **Ningún modelo mejora todos los indicadores a la vez.** La evidencia muestra una mejora de calidad de imagen con un compromiso en la conservación de cuentas. No respalda por sí sola la afirmación amplia de calidad comparable a alta estadística.

Son tres geometrías de test y una de generalización, de un catálogo sintético conocido. Las veinte realizaciones por vista no son geometrías independientes. Los porcentajes se refieren a cuentas sobre referencias idealizadas, no a densidad.

## 5. Archivos binarios

No se versionan. Las 32 matrices de predicciones (8 modelos × 4 geometrías, 120 × 256 × 256 en float32) suman **1.006.637.056 bytes**. Sus huellas y tamaños están en [binarios.sha256](datos/binarios.sha256) y [binarios.tamanos.txt](datos/binarios.tamanos.txt), y coinciden con [inventario-predicciones.json](datos/evaluacion-final-f05/informe-v1/inventario-predicciones.json).

- **Verificación local:** todos los archivos del pod se copiaron a almacenamiento local y se verificaron contra un manifiesto generado en el pod: 113 de 113.
- **Verificación en Drive:** la copia se verificó contra `binarios.sha256`: 32 de 32. El enlace público lista los 32 archivos sin sesión iniciada, y una descarga pública de `binarios.sha256` y de dos matrices coincide con sus huellas ([verificacion-drive-binarios.json](datos/verificacion-drive-binarios.json)).
- **Identidades y recibos:** los recibos por geometría, las identidades y los `completed.json` de los ocho modelos están en [datos/evaluacion-final-f05/](datos/evaluacion-final-f05/).

**Copia de distribución:** [carpeta de Drive oe2-evaluacion-final-f05](https://drive.google.com/drive/folders/1UfRJTnuwYfgql5SJdklM2Cp-P0ychaAA), con la estructura `<modelo>/<geometría>.npy`, junto con las identidades, los recibos y `completed.json` de cada modelo (48 JSON idénticos a los de la rama), `binarios.sha256`, `binarios.tamanos.txt` y `LEEME.txt`.

## 6. Reproducción

1. Clonar la rama en `/workspace/repo`. Copiar `verificacion/` a `/workspace` y los ocho archivos reservados a `/workspace/insumos/dataset-v2/shards/`.
2. `bash etapa0_preparar.sh`: entorno, pesos desde Drive, registro y preflight.
3. `bash etapa1_inferencia.sh`: inferencia de los ocho modelos.
4. `bash etapa2_evaluacion.sh`: evaluación conjunta.

Las huellas de esta entrega están en [huellas.sha256](huellas.sha256).

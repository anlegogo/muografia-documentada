# Resultados del complemento OE3-C1: fracciones de entrada y métricas locales

2026-10-04 (Colombia). Ejecución de las [instrucciones del complemento](../../INSTRUCCIONES_COMPLEMENTO_OE3.md), según el [protocolo OE3-C1](../../PROTOCOLO_COMPLEMENTO_OE3.md), con el código de `main` en `39d8fd3` sin modificaciones. No se entrenó, no se simularon muones, no se modificaron pesos ni criterios y no se seleccionó ningún modelo.

**Alcance:** evaluación descriptiva de los ocho modelos congelados del OE2 cuando reciben el 1, 5, 10 y 50 % de los conteos, sobre datos potencialmente expuestos. El bloque del 5 % se reutilizó de EF-01. No declara equivalencia física ni reconstrucción de opacidad (`physical_equivalence: false`, `opacity_reconstructed: false`).

## 1. Ejecución

| Elemento | Valor |
|---|---|
| Código | `main` `39d8fd3e398a540ea42e025fce8c42fa25986dfa`, clonado en el pod desde un bundle y comprobado contra `commit-esperado.txt` ([commit.txt](datos/complemento-oe3-v1/registro/commit.txt)) |
| Equipo | Pod RunPod con 1 × NVIDIA L40S, driver 595.91.07 ([gpu.txt](datos/complemento-oe3-v1/registro/gpu.txt)) |
| Entorno | Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.3.5, SciPy 1.18.1, scikit-image 0.26.0 y filelock 3.16.1 ([python-torch.txt](datos/complemento-oe3-v1/registro/python-torch.txt), [entorno.txt](datos/complemento-oe3-v1/registro/entorno.txt)); es el mismo entorno de EF-01 |
| Datos | Los ocho archivos de `geo-test-01..03` y `geo-gen-01` de la distribución del OE1, con las huellas del contrato |
| Pesos | Los ocho checkpoints de EF-01, descargados de sus enlaces de Drive y verificados por SHA-256: 8 de 8 ([pesos.log](datos/complemento-oe3-v1/registro/pesos.log)) |
| Bloque 5 % | Carpeta original de EF-01: 32 NPY con identidades, recibos y `completed.json`. Las 32 huellas coincidieron con sus recibos antes y después de la transferencia |
| Pruebas del director | `test_complemento_oe3.py` y `test_flujo_complemento_oe3.py`: OK ([registro](datos/complemento-oe3-v1/registro/)) |
| Preflight | `{"data_files": 8, "models": 8, "arrays_opened": false, "passed": true, "existing_f05_images": 3840, "reused_f05": true, "registry_verified": true, "new_images_planned": 11520}` ([preflight.json](datos/complemento-oe3-v1/preflight.json)) |
| Intervalo (UTC) | Preparación 23:24:59–23:26:13; `smoke` e inferencia 23:26:13–23:30:12; evaluación 23:30:12–23:31:52 ([estado.log](datos/registros-pod/estado.log)) |

Se siguió la secuencia de la guía con una GPU: pruebas, `preflight`, y para cada modelo `smoke` y después `infer` con `--device cuda:0`; `evaluate` se ejecutó una sola vez al terminar los ocho modelos, con el informe en `informe/`. Los scripts están en [verificacion/](verificacion/).

**Comprobación técnica (`smoke`).** Los ocho modelos dieron `passed: true`. La diferencia máxima frente al bloque del 5 % fue **0** en los ocho: la L40S reprodujo bit a bit las predicciones conservadas de EF-01. Las salidas de las tres fracciones nuevas tuvieron forma, finitud e inversión válidas. Los recibos están en `datos/complemento-oe3-v1/smoke-<modelo>.json`.

**Inferencia.** 11.520 predicciones nuevas: 8 modelos × 3 fracciones × 480 imágenes, en 96 NPY de 120 × 256 × 256 float32 (3.019.911.168 bytes). Cada modelo y fracción tardó entre 4,8 y 5,0 s (`completed.json`).

**Lecturas literales e incidencias.**

1. **Se usó RunPod en lugar de SC3**, con 1 GPU.
2. **Clonado del código.** El bundle guardaba la referencia como `refs/remotes/origin/main`, de modo que los dos primeros intentos de clonar fallaron antes de instalar nada (`CLONE_FALLO`; [intento 1](datos/registros-pod/estado-intento1.log), [intento 2](datos/registros-pod/estado-intento2.log)). Se corrigió solo el paso de clonado: inicializar el repositorio, traer esa referencia y hacer `checkout --detach` del commit esperado. No se ejecutó ninguna herramienta del complemento en esos intentos.
3. **Estado de Git.** `main` `39d8fd3` mantiene 20 archivos confirmados con CRLF que Git marca como modificados en cualquier copia limpia. La preparación verificó que son idénticos byte a byte a `HEAD` ([estado-git.txt](datos/complemento-oe3-v1/registro/estado-git.txt)).
4. **Driver.** El driver del pod (595.91.07) difiere del de EF-01 (570.195.03). La comprobación técnica igualmente reprodujo el bloque del 5 % con diferencia cero.

## 2. Resultados

La evaluación conjunta produjo exactamente los registros que prevé la guía: **17.280** filas de imagen, **4.536** regionales, **216** de contraste y **39.096** de métricas locales, además de 2.160 registros de señal entre realizaciones ([resultado.json](datos/complemento-oe3-v1/informe/resultado.json), [inventario](datos/complemento-oe3-v1/informe/inventario.json)). Los soportes locales comunes a las cuatro fracciones y a todos los métodos son 30 combinaciones anomalía/vista para SNR, 32 para CNR y 32 para el contraste de cuentas.

**Referente de imagen del protocolo** (entrada sin red al 50 %, umbrales SSIM y PSNR por geometría y vista): **ningún modelo satisface la regla en todas las vistas con ninguna de las cuatro fracciones**, ni en prueba ni en generalización. `minimum_sampled_fraction` es nulo para los 8 modelos en ambas particiones. El protocolo prevé este caso como resultado permitido.

Macropromedios (SSIM / PSNR en dB / Q en %). Los valores de las redes son el intervalo entre las ocho:

| Partición | Fracción | Entrada sin red | Redes: SSIM | Redes: PSNR | Redes: Q |
|---|---:|---|---|---|---|
| Prueba | 1 % | 0,6959 / 22,537 / 2,897 | 0,8091–0,8414 | 29,264–31,143 | 33,529–47,334 |
| Prueba | 5 % | 0,7643 / 24,258 / 1,832 | 0,8263–0,8545 | 30,729–33,074 | 3,996–22,388 |
| Prueba | 10 % | 0,7964 / 25,722 / 1,334 | 0,8219–0,8567 | 30,131–33,023 | 15,732–32,064 |
| Prueba | 50 % | 0,9250 / 33,101 / 0,437 | 0,7256–0,8442 | 26,103–30,186 | 25,453–56,413 |
| Generalización | 1 % | 0,6851 / 22,299 / 3,067 | 0,7980–0,8356 | 29,069–31,365 | 40,220–52,203 |
| Generalización | 5 % | 0,7502 / 23,904 / 1,093 | 0,8145–0,8454 | 30,331–32,883 | 2,271–26,505 |
| Generalización | 10 % | 0,7834 / 25,349 / 0,895 | 0,8115–0,8466 | 29,493–32,882 | 4,445–41,570 |
| Generalización | 50 % | 0,9197 / 32,752 / 0,449 | 0,7079–0,8353 | 25,656–30,427 | 21,124–45,593 |

El caso del 5 % reproduce los valores de EF-01-C2. Las tablas completas por modelo, geometría, vista, región, contraste y métricas locales están en `datos/complemento-oe3-v1/informe/`.

## 3. Lectura literal

1. Con el 50 % de los conteos, cada una de las ocho redes obtiene SSIM y PSNR **menores** que con el 5 % y que la entrada sin red al 50 %, en las dos particiones.
2. Con el 1 %, cada red mantiene SSIM y PSNR por encima de la entrada sin red al 1 % y al 10 %, pero su Q queda entre 33,5 y 52,2 %.
3. Entre el 5 % y el 10 %, el SSIM de cada red cambia como máximo 0,0056 en prueba y 0,0052 en generalización, y el PSNR como máximo 0,641 y 0,838 dB; Q cambia de forma distinta según el modelo.
4. Las redes se entrenaron o ajustaron al 5 %. Estos resultados describen su transferencia a otras estadísticas de entrada; no equivalen a entrenar una red por fracción.

La interpretación científica, la conclusión de OE3-P03, P05 y P06 y cualquier decisión sobre el factor de reducción corresponden a la revisión de la dirección. Las filas repetidas por modelo y fracción no son experimentos independientes.

## 4. Archivos binarios

No se versionan. Las 96 matrices nuevas suman **3.019.911.168 bytes**; sus huellas y tamaños están en [binarios.sha256](datos/binarios.sha256) y [binarios.tamanos.txt](datos/binarios.tamanos.txt). La salida completa se copió a almacenamiento local y se verificó contra el manifiesto generado en el pod, 294 de 294 archivos ([manifiesto.sha256](datos/complemento-oe3-v1/manifiesto.sha256)), y la copia en Drive se verificó con el mismo manifiesto y con `binarios.sha256`.

**Copia de distribución:** [carpeta de Drive oe3-complemento-oe3-f05](https://drive.google.com/drive/folders/12RB9qJ32WjUWGFBQRxuvIiZ7szTM9IbO). El enlace público lista los 298 archivos sin sesión iniciada, y una descarga pública de `binarios.sha256`, de dos matrices (1 % y 50 %) y de `informe/resultado.json` coincide con sus huellas ([verificacion-drive-binarios.json](datos/verificacion-drive-binarios.json)). Contiene la carpeta completa de salida (`preflight.json`, ocho `smoke-<modelo>.json`, `f001`, `f010` y `f050` con NPY, recibos, identidad y `completed.json`, `informe/` y `registro/`), junto con `binarios.sha256`, `binarios.tamanos.txt` y `LEEME.txt`.

## 5. Reproducción

1. Clonar `main` en `39d8fd3` en `/workspace/repo`; copiar `verificacion/` a `/workspace`, los ocho archivos reservados a `/workspace/insumos/dataset-v2/shards/` y la carpeta original de EF-01 al 5 % a `/workspace/existente/evaluacion-final-f05/`.
2. `bash etapa0_preparar.sh`: entorno, pesos desde Drive, pruebas y preflight.
3. `bash etapa1_smoke_infer.sh`: `smoke` e `infer` de los ocho modelos.
4. `bash etapa2_evaluacion.sh`: evaluación conjunta y manifiesto.

Las huellas de esta entrega están en [huellas.sha256](huellas.sha256).

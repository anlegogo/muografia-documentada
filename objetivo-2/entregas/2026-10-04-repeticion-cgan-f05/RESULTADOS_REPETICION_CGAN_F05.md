# Resultados de la repetición cGAN al 5 %

2026-10-04 (Colombia). Ejecución de las [instrucciones de repetición](../../INSTRUCCIONES_REPETICION_CGAN_F05.md) según el [diseño fijado](../../DISENO_REPETICION_CGAN_F05.md), con el código de `main` en `fd20c674758327acbdfc5015b117e3353ff96a0f` sin modificaciones. Se comprobaron en GPU las tres parejas R1, R2 y R3. Como las tres aceptaron la recuperación exacta, se completaron las seis continuaciones de cinco épocas y su evaluación.

**Resultado de la síntesis: `dependencia_de_semilla_o_compromiso`** ([sintesis-repeticion.json](datos/cgan-repeticion-f05/sintesis-repeticion.json)).

- Ninguna pareja satisface los ocho controles.
- C1 reduce Q en R1 y R2, y lo aumenta en R3.
- El error de borde de C1 es mayor que el de C0 en las tres parejas.
- La mejora concordante observada con la semilla 2026100303 no se repite con estas tres semillas.

La clasificación es descriptiva (`physical_acceptance: false`). Son tres continuaciones condicionadas al mismo checkpoint, no entrenamientos independientes desde cero.

## 1. Ejecución

| Elemento | Valor |
|---|---|
| Código | Rama `oe2/repeticion-cgan-f05` creada desde `main` `fd20c67`, sin cambios. Clon en el pod desde un bundle de esa rama; `git status --porcelain` vacío ([commit.txt](datos/cgan-repeticion-f05/commit.txt), [estado-git.txt](datos/cgan-repeticion-f05/estado-git.txt)) |
| Equipo | Pod RunPod con 3 × NVIDIA L40S de 46 GB, driver 580.126.09 ([gpu.txt](datos/cgan-repeticion-f05/gpu.txt)) |
| Entorno | Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.3.5, SciPy 1.18.1, scikit-image 0.26.0, Matplotlib 3.11.1 y filelock 3.16.1 ([entorno.txt](datos/cgan-repeticion-f05/entorno.txt), [python-torch.txt](datos/entorno/python-torch.txt)). Es el mismo entorno de las entregas CG-04c |
| Datos | 30 shards de train/val y el `best.pt` cGAN `e54d51f7…`, descargados de las copias de Drive y verificados: 31 de 31 huellas ([datos.log](datos/registros/datos.log)) |
| Máscaras | Generadas una sola vez en el pod con `datos_ajuste.py` y usadas sin cambios en todo el ensayo ([manifiesto](datos/manifiesto-mascaras.json)) |
| Ejecutor | Reinaldo Cárdenas Tirado, mediante los scripts de [verificacion/](verificacion/) |
| Intervalo (UTC, 2026-10-04) | Preparación 07:24:35–07:26:04; comprobación GPU 07:26:18–07:27:13; continuaciones 07:27:26–07:47:45; evaluación y síntesis 07:47:56–07:49:37 ([estado.log](datos/registros/estado.log)) |

Todos los comandos terminaron sin error. Son los bloques literales de la guía, organizados en cuatro etapas:

- [etapa0_preparar.sh](verificacion/etapa0_preparar.sh): preparación.
- [etapa1_tecnica.sh](verificacion/etapa1_tecnica.sh): bloque 1.
- [etapa2_piloto.sh](verificacion/etapa2_piloto.sh): bloque 2.
- [etapa3_evaluacion.sh](verificacion/etapa3_evaluacion.sh): bloque 3.

Las rutas comunes están en [comun.sh](verificacion/comun.sh). El entorno y los datos se prepararon con los scripts de las entregas anteriores ([instalar_entorno.sh](verificacion/instalar_entorno.sh), [sincronizar_datos.py](verificacion/sincronizar_datos.py)).

**Desviaciones y lecturas literales.**

1. **Una pareja por GPU, en paralelo, con visto bueno de la dirección** (grupo del proyecto, 2026-10-04 hacia las 02:15, hora de Colombia). R1 se ejecutó en la GPU 0, R2 en la 1 y R3 en la 2. Cada pareja usó la misma GPU física para su comprobación técnica, su aceptación y sus dos continuaciones. Los comandos son los de la guía y solo cambia `CUDA_VISIBLE_DEVICES`. El ejecutor registra el dispositivo como `cuda:0` con nombre `NVIDIA L40S` en las tres parejas. Las tres evaluaciones y la síntesis se ejecutaron en secuencia en la GPU 0, con el mismo dispositivo para las tres parejas.
2. **Se usó RunPod en lugar de SC3**, como en las entregas anteriores, así que no hay identificadores SLURM.
3. **`python -m pip freeze`.** El entorno virtual creado con `uv` no incluye `pip`, de modo que el inventario `entorno.txt` se generó con `uv pip freeze`, como en las entregas anteriores.
4. **Driver.** El pod usó el driver 580.126.09; la entrega CG-04c usó el 570.124.06. Las tres aceptaciones GPU se obtuvieron con el driver de este pod.

## 2. Comprobación técnica en GPU

Por pareja se ejecutaron cuatro pruebas técnicas: C0 y C1, cada una continua y otra interrumpida tras la época 1 y reanudada. Son 12 pruebas, 18 lanzamientos, 48 actualizaciones de G y 240 de D. Las tres auditorías `revisar_ajuste_cgan.py --pareja … --exigir-gpu` declararon `passed: true`, `gpu_accepted: true` y `exact_recovery: true`.

| Pareja | Semilla | GPU | Aceptación | Política del gradiente del crítico |
|---|---:|---:|---|---|
| R1 | 2026100401 | 0 | [aceptacion-gpu.json](datos/cgan-repeticion-f05/R1/aceptacion-gpu.json) | `wasserstein-then-weighted-gp-v1` |
| R2 | 2026100402 | 1 | [aceptacion-gpu.json](datos/cgan-repeticion-f05/R2/aceptacion-gpu.json) | `wasserstein-then-weighted-gp-v1` |
| R3 | 2026100403 | 2 | [aceptacion-gpu.json](datos/cgan-repeticion-f05/R3/aceptacion-gpu.json) | `wasserstein-then-weighted-gp-v1` |

Cada época técnica de ocho pares tardó entre 2,3 y 2,4 s en la primera época de cada proceso y entre 0,76 y 0,79 s en la segunda época continua.

## 3. Continuaciones de cinco épocas

Las seis ejecuciones completaron sus cinco épocas sin interrupción (`completed: true`, `epoch: 5`, `resume_count: 0`). Cada una partió del checkpoint cGAN original con optimizadores nuevos e hizo 1.800 actualizaciones de G y 9.000 de D.

| Pareja | Rama | Cómputo total | Tiempo por época | Memoria CUDA máx. |
|---|---|---:|---:|---:|
| R1 | C0 | 590,8 s | 116,9–120,5 s | 1,96 GB |
| R1 | C1 | 599,0 s | 118,7–121,9 s | 1,96 GB |
| R2 | C0 | 587,9 s | 116,7–119,6 s | 1,96 GB |
| R2 | C1 | 597,6 s | 118,5–121,9 s | 1,96 GB |
| R3 | C0 | 596,4 s | 118,4–120,3 s | 1,96 GB |
| R3 | C1 | 605,2 s | 120,2–122,2 s | 1,96 GB |

Las tres parejas corrieron a la vez, de modo que el bloque completo tardó 20 minutos de reloj. En secuencia en una sola GPU habría requerido unos 60 minutos de cómputo.

## 4. Evaluación por pareja

Las cifras salen de `evaluar_ajuste_cgan.py` sobre los 360 pares de validación. La entrada y la cGAN inicial son idénticas en las tres evaluaciones. Q y los errores están en porcentaje; el error de contraste corresponde a las 23 combinaciones comunes.

| Pareja | Modelo | Q | Q `geo-val-01` | Q `geo-val-02` | Q `geo-val-03` | Cielo | Borde | Contraste | SSIM | PSNR (dB) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| — | Entrada | 1,814 | 1,198 | 2,551 | 1,692 | 6,802 | 12,092 | 0,2464 | 0,75181 | 24,168 |
| — | cGAN inicial | 12,340 | 3,470 | 15,744 | 17,806 | 12,648 | 14,419 | 0,0907 | 0,82279 | 31,104 |
| R1 | C0 | 13,841 | 18,553 | 5,192 | 17,779 | 2,766 | 10,882 | 0,1407 | 0,81420 | 30,503 |
| R1 | C1 | 5,711 | 7,215 | 4,100 | 5,818 | 2,346 | 11,448 | 0,0870 | 0,81648 | 30,667 |
| R2 | C0 | 10,300 | 13,528 | 8,188 | 9,183 | 2,575 | 10,652 | 0,0954 | 0,81568 | 30,530 |
| R2 | C1 | 9,434 | 10,897 | 3,910 | 13,496 | 2,634 | 11,121 | 0,0782 | 0,81623 | 30,636 |
| R3 | C0 | 5,871 | 6,847 | 3,960 | 6,807 | 2,415 | 10,882 | 0,0994 | 0,81694 | 30,706 |
| R3 | C1 | 7,700 | 8,006 | 4,143 | 10,951 | 2,657 | 10,967 | 0,1032 | 0,81486 | 30,546 |

Fuentes: [R1](datos/cgan-repeticion-f05/R1/evaluacion/comparacion-cgan.json), [R2](datos/cgan-repeticion-f05/R2/evaluacion/comparacion-cgan.json) y [R3](datos/cgan-repeticion-f05/R3/evaluacion/comparacion-cgan.json).

**Controles de la regla, C1 frente a C0.**

| Control | R1 | R2 | R3 |
|---|:---:|:---:|:---:|
| Q menor | Sí | Sí | No |
| Ningún Q por geometría mayor | Sí | No (`geo-val-03`) | No |
| Cielo no peor | Sí | No | No |
| Borde no peor | No | No | No |
| Mismo soporte de contraste | Sí | Sí | Sí |
| Error de contraste no mayor | Sí | Sí | No |
| SSIM no menor | Sí | Sí | No |
| PSNR no menor | Sí | Sí | No |
| Decisión del evaluador | `compromiso` | `compromiso` | `sin_mejora_del_indicador_principal` |

## 5. Síntesis pareada

Diferencias C1 − C0. En Q y en los errores, un valor negativo favorece a C1; en SSIM y PSNR, uno positivo. Q, cielo y borde están en puntos porcentuales.

| Medida | R1 | R2 | R3 | Mediana | Rango |
|---|---:|---:|---:|---:|---|
| Q | −8,130 | −0,866 | +1,829 | −0,866 | [−8,130; +1,829] |
| Cielo | −0,421 | +0,059 | +0,242 | +0,059 | [−0,421; +0,242] |
| Borde | +0,566 | +0,468 | +0,085 | +0,468 | [+0,085; +0,566] |
| Contraste | −0,0537 | −0,0172 | +0,0038 | −0,0172 | [−0,0537; +0,0038] |
| SSIM | +0,00228 | +0,00055 | −0,00209 | +0,00055 | [−0,00209; +0,00228] |
| PSNR (dB) | +0,164 | +0,106 | −0,160 | +0,106 | [−0,160; +0,164] |

`concordant_pairs: 0`, `pairs_reducing_Q: 2` y `decision: dependencia_de_semilla_o_compromiso`. Según la regla del diseño, ninguna pareja repite la concordancia del criterio agregado. La dirección del efecto sobre Q depende de la semilla. El único cambio con la misma dirección en las tres parejas es el aumento del error de borde de C1.

**Variación del control entre semillas.** El Q de C0 vale 13,84 % en R1, 10,30 % en R2 y 5,87 % en R3; en el antecedente con semilla 2026100303 fue 7,20 %. La dispersión de la continuación sin término regional entre semillas es del mismo orden que las diferencias C1 − C0. Es una observación descriptiva sobre tres continuaciones; no es una estimación de variabilidad.

## 6. Diagnóstico por vista y anomalía

Proviene de `analizar_compromiso_cgan.py` por pareja ([R1](datos/cgan-repeticion-f05/R1/compromiso/compromiso-cgan.json), [R2](datos/cgan-repeticion-f05/R2/compromiso/compromiso-cgan.json), [R3](datos/cgan-repeticion-f05/R3/compromiso/compromiso-cgan.json), con tablas `vistas.csv` y figuras `compromiso-vistas.pdf`).

| C1 frente a C0, por vista (de 18) | R1 | R2 | R3 |
|---|---:|---:|---:|
| q mejor / peor | 15 / 3 | 12 / 6 | 6 / 12 |
| Cielo mejor / peor | 12 / 6 | 6 / 12 | 12 / 6 |
| Borde mejor / peor | 1 / 17 | 0 / 18 | 6 / 12 |
| SSIM mejor / peor | 15 / 3 | 12 / 6 | 3 / 15 |
| PSNR mejor / peor | 17 / 1 | 17 / 1 | 0 / 18 |

| C1 frente a la cGAN inicial, por vista (de 18) | R1 | R2 | R3 |
|---|---:|---:|---:|
| q mejor / peor | 12 / 6 | 11 / 7 | 12 / 6 |
| SSIM peor | 17 | 18 | 18 |
| PSNR peor | 18 | 18 | 18 |
| Cielo y borde mejores | 18 y 18 | 18 y 18 | 18 y 18 |

| Anomalías (24 combinaciones de vista y anomalía) | R1 | R2 | R3 |
|---|---:|---:|---:|
| Mayor magnitud del sesgo medio que C0 | 4 | 14 | 14 |
| Mayor magnitud del sesgo medio que la cGAN inicial | 7 | 10 | 10 |
| Contrastes comunes en que C1 mejora a C0 (de 23) | 17 | 13 | 15 |
| Inversiones de signo del contraste medio de C1 | 11 | 8 | 13 |

**El cuerpo denso de `geo-val-03` concentra los mayores sesgos de C1 en las tres parejas.** Ahora predomina la sobreestimación: el sesgo firmado medio más alto es +39,4 % en R1 (V5), +62,4 % en R2 (V5) y +54,7 % en R3 (V4), sobre referencias de 144 a 210 cuentas y de 362 a 524 píxeles. Estos porcentajes se refieren a cuentas respecto de la referencia idealizada y no equivalen a error de densidad.

Las figuras del evaluador (`geo-val-01.png` a `geo-val-03.png` en cada carpeta `evaluacion/`) cubren las 18 vistas de cada pareja.

## 7. Lectura

Con la regla fijada antes de ejecutar, el resultado es **dependiente de la semilla o de compromiso**:

- En R1 se repite una reducción grande de Q, como en el antecedente, pero con mayor error de borde.
- En R2 la reducción de Q es pequeña y empeoran el cielo, el borde y `geo-val-03`.
- En R3, C1 empeora frente a C0 en Q y en casi todas las medidas.

No se sustituyó ninguna semilla ni se modificaron coeficientes, épocas o tolerancias.

Frente a la cGAN inicial, C1 reduce en las tres parejas los errores de cielo y borde en las 18 vistas. También empeora SSIM en 17 o 18 vistas y PSNR en las 18. La entrada sin red conserva un Q (1,81 %) menor que cualquier continuación.

Las tres parejas no estiman la variabilidad de entrenamientos desde cero ni la generalización. Tampoco se abrieron test ni generalización.

## 8. Archivos binarios

No se versionan. Hay 55 archivos, 5,6 GB:

- los 18 `last.pt`: 12 técnicos y 6 finales;
- las 21 predicciones: 12 técnicas, 6 finales y 3 de la cGAN inicial, una por evaluación;
- la caché de máscaras: manifiesto y 15 NPZ.

Sus huellas y tamaños están en [binarios.sha256](datos/binarios.sha256) y [binarios.tamanos.txt](datos/binarios.tamanos.txt). Todos los archivos del pod se copiaron a almacenamiento local y se verificaron contra un manifiesto generado en el pod: 260 de 260. La copia de Drive se verificó también contra `binarios.sha256`: 55 de 55. El enlace público lista los 55 binarios sin sesión iniciada, y una descarga pública de `binarios.sha256`, un `last.pt` y un arreglo de predicciones coincide con sus huellas ([verificacion-drive-binarios.json](datos/verificacion-drive-binarios.json)).

**Copia de distribución:** [carpeta de Drive oe2-repeticion-cgan-f05](https://drive.google.com/drive/folders/19H0ByGPw8zhwLQdzqWcqpMmt4A-OhhDW), con la misma estructura de carpetas, `binarios.sha256`, `binarios.tamanos.txt` y `LEEME.txt`.

## 9. Reproducción

1. Clonar la rama en `/workspace/repo` y copiar `verificacion/` a `/workspace` (`comun.sh` fija las rutas y la asignación de parejas a GPU).
2. `bash etapa0_preparar.sh`: instala el entorno, descarga y verifica los datos, prepara las máscaras y hace el registro inicial de la guía.
3. `bash etapa1_tecnica.sh`: bloque 1. Termina con código distinto de cero si alguna aceptación no es exacta.
4. `bash etapa2_piloto.sh`: bloque 2, solo con las tres aceptaciones.
5. `bash etapa3_evaluacion.sh`: bloque 3 y síntesis.

Las huellas de esta entrega están en [huellas.sha256](huellas.sha256).

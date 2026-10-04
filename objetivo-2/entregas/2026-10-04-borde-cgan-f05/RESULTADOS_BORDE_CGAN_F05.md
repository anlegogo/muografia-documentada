# Resultados del ensayo de borde E1

2026-10-04 (Colombia). Ejecución de las [instrucciones del ensayo E1](../../INSTRUCCIONES_BORDE_CGAN.md) según el [diseño fijado](../../DISENO_BORDE_CGAN.md), con el código de `main` en `156d4f5699f500c692d466f56c48ca25bda79c0c` sin modificaciones. Las tres parejas B1, B2 y B3 superaron la prueba técnica en GPU con recuperación exacta. Por eso se completaron las seis continuaciones de cinco épocas, la evaluación, la síntesis y el inventario de la guía.

**Resultado de la síntesis: `dependencia_de_semilla_o_compromiso`** ([sintesis-borde.json](datos/ensayo-borde-e1/sintesis-borde.json)).

- **La pregunta específica del ensayo da un resultado consistente.** El término espacial reduce el error de borde en las tres parejas: entre 3,97 y 4,25 puntos porcentuales, de 11,05–11,26 % a 6,89–7,08 %.
- **Ninguna pareja satisface los nueve controles.** `geo-val-01` empeora en las tres parejas y Q aumenta en B3. Además hay deterioros puntuales de cielo (B1), contraste (B2) y PSNR (B1 y B3).

La clasificación es descriptiva (`physical_acceptance: false`). Son tres continuaciones condicionadas al mismo checkpoint, no entrenamientos independientes desde cero.

## 1. Ejecución

| Elemento | Valor |
|---|---|
| Código | Rama `oe2/borde-cgan-f05` creada desde `main` `156d4f5`, sin cambios. Clon en el pod desde un bundle de esa rama ([commit.txt](datos/ensayo-borde-e1/registro/commit.txt)) |
| Equipo | Pod RunPod con 3 × NVIDIA L40S de 46 GB, driver 580.126.09 ([gpu.txt](datos/ensayo-borde-e1/registro/gpu.txt)) |
| Entorno | Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.3.5, SciPy 1.18.1, scikit-image 0.26.0, Matplotlib 3.11.1 y filelock 3.16.1 ([entorno.txt](datos/ensayo-borde-e1/registro/entorno.txt), [python-torch.txt](datos/entorno/python-torch.txt)). Es el mismo entorno de la repetición R1–R3 |
| Datos | 30 shards de train/val y el `best.pt` cGAN `e54d51f7…`, descargados de las copias de Drive y verificados: 31 de 31 huellas ([datos.log](datos/registros/datos.log)) |
| Máscaras | Generadas una sola vez en el pod con `datos_ajuste.py` y usadas sin cambios en todas las fases ([manifiesto](datos/manifiesto-mascaras.json)) |
| Ejecutor | Reinaldo Cárdenas Tirado, mediante los scripts de [verificacion/](verificacion/) |
| Intervalo (UTC, 2026-10-04) | Preparación 14:30:05–14:31:25; fase técnica 14:31:32–14:32:49; piloto 14:33:00–14:53:35; evaluación y síntesis 14:53:46–14:55:19; inventario 14:55:40 ([estado.log](datos/registros/estado.log)) |

Todos los comandos terminaron sin error. Son las invocaciones literales de `orquestar_borde_cgan.py` e `inventariar_entrega_borde.py` de la guía, organizadas en cuatro etapas:

- [etapa0_preparar.sh](verificacion/etapa0_preparar.sh): preparación.
- [etapa1_tecnica.sh](verificacion/etapa1_tecnica.sh): fase técnica.
- [etapa2_piloto.sh](verificacion/etapa2_piloto.sh): piloto.
- [etapa3_evaluacion.sh](verificacion/etapa3_evaluacion.sh): evaluación, síntesis e inventario.

Las rutas comunes están en [comun.sh](verificacion/comun.sh). La raíz `OUT` fue compartida por los tres procesos, como exige la guía, y las consolas de cada orquestador quedaron en ella (`B*-tecnica-consola.log`, `B*-piloto-consola.log`).

**Desviaciones y lecturas literales.**

1. **Una pareja por GPU, según la guía y el mensaje del director en el grupo.** B1 se ejecutó en la GPU 0, B2 en la 1 y B3 en la 2. Cada pareja conservó su GPU en la fase técnica y en sus dos variantes del piloto. Las tres evaluaciones y la síntesis se ejecutaron en secuencia en la GPU 0.
2. **Estado de Git.** En un clon limpio de `156d4f5`, `git status --porcelain` marca nueve archivos como modificados: las seis configuraciones `borde-cgan-v1/B*-C*.json`, `diagnostico-espacial-cgan.json`, `perfil-gradientes-borde.json` y `sondeo-gradientes-borde.json`. Esos archivos se confirmaron con finales de línea CRLF, mientras `.gitattributes` exige `eol=lf`, de modo que Git los marca en cualquier copia. No se editaron. Antes de ejecutar se comprobó que los bytes de cada uno coinciden con el objeto de `HEAD` (`git hash-object --no-filters` igual a `git rev-parse HEAD:<archivo>`) ([estado-git.txt](datos/ensayo-borde-e1/registro/estado-git.txt), [estado-git-verificado.txt](datos/ensayo-borde-e1/registro/estado-git-verificado.txt)).
3. **Se usó RunPod en lugar de SC3**, como en las entregas anteriores, así que no hay identificadores SLURM.
4. **Inventario del entorno.** Se generó con `uv pip freeze`, porque el entorno virtual creado con `uv` no incluye `pip`.

## 2. Prueba técnica en GPU

El orquestador ejecutó por pareja C0 y C1, cada una continua y otra interrumpida tras la época 1 y recuperada. Generó `aceptacion-gpu.json` solo con igualdad exacta. Las tres aceptaciones declaran `gpu_accepted: true` y `exact_recovery: true` con la política `wasserstein-then-weighted-gp-v1` del crítico. En total: 12 ejecuciones técnicas, 48 actualizaciones de G y 240 de D.

| Pareja | Semilla | GPU | Aceptación |
|---|---:|---:|---|
| B1 | 2026100411 | 0 | [aceptacion-gpu.json](datos/ensayo-borde-e1/B1/aceptacion-gpu.json) |
| B2 | 2026100412 | 1 | [aceptacion-gpu.json](datos/ensayo-borde-e1/B2/aceptacion-gpu.json) |
| B3 | 2026100413 | 2 | [aceptacion-gpu.json](datos/ensayo-borde-e1/B3/aceptacion-gpu.json) |

La fase técnica completa de las tres parejas tardó 77 s de reloj. El inventario reaudita las tres aceptaciones (`technical_gates`).

## 3. Continuaciones de cinco épocas

Las seis ejecuciones completaron sus cinco épocas sin interrupción (`completed: true`, `epoch: 5`, `resume_count: 0`). Cada una partió del checkpoint cGAN original con optimizadores nuevos e hizo 1.800 actualizaciones de G y 9.000 de D.

| Pareja | Rama | Cómputo total | Tiempo por época | Memoria CUDA máx. |
|---|---|---:|---:|---:|
| B1 | C0 | 602,1 s | 119,2–122,4 s | 1,96 GB |
| B1 | C1 | 606,5 s | 119,7–124,3 s | 1,96 GB |
| B2 | C0 | 602,2 s | 118,7–122,1 s | 1,96 GB |
| B2 | C1 | 602,7 s | 119,5–122,4 s | 1,96 GB |
| B3 | C0 | 602,0 s | 118,9–122,3 s | 1,96 GB |
| B3 | C1 | 600,6 s | 118,7–122,5 s | 1,96 GB |

El piloto completo tardó 20,6 minutos de reloj. El término de borde no produjo diferencias de tiempo apreciables en esta implementación y equipo.

## 4. Evaluación por pareja

Las cifras salen de `evaluar_borde_cgan.py` sobre los 360 pares de validación. La entrada y la cGAN inicial son idénticas en las tres evaluaciones. Q, cielo y borde están en porcentaje. El borde es el error absoluto espacial de la región, es decir, el error píxel a píxel. El contraste corresponde a las 23 combinaciones comunes.

| Pareja | Modelo | Q | Q `geo-val-01` | Q `geo-val-02` | Q `geo-val-03` | Cielo | Borde | Contraste | SSIM | PSNR (dB) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| — | Entrada | 1,814 | 1,198 | 2,551 | 1,692 | 6,802 | 12,092 | 0,2464 | 0,75181 | 24,168 |
| — | cGAN inicial | 12,340 | 3,470 | 15,744 | 17,806 | 12,648 | 14,419 | 0,0907 | 0,82279 | 31,104 |
| B1 | C0 | 6,233 | 7,576 | 5,130 | 5,993 | 2,478 | 11,146 | 0,1157 | 0,81572 | 30,646 |
| B1 | C1 | 4,802 | 8,554 | 3,139 | 2,713 | 2,490 | 6,891 | 0,0866 | 0,81578 | 30,637 |
| B2 | C0 | 7,812 | 8,753 | 4,706 | 9,975 | 2,468 | 11,263 | 0,0782 | 0,81456 | 30,526 |
| B2 | C1 | 7,158 | 10,506 | 5,221 | 5,748 | 2,319 | 7,045 | 0,0960 | 0,81495 | 30,588 |
| B3 | C0 | 5,018 | 5,154 | 4,901 | 4,997 | 2,343 | 11,052 | 0,0868 | 0,81512 | 30,612 |
| B3 | C1 | 5,486 | 8,767 | 3,522 | 4,169 | 2,270 | 7,084 | 0,0783 | 0,81480 | 30,562 |

Fuentes: [B1](datos/ensayo-borde-e1/B1/evaluacion/comparacion-cgan.json), [B2](datos/ensayo-borde-e1/B2/evaluacion/comparacion-cgan.json) y [B3](datos/ensayo-borde-e1/B3/evaluacion/comparacion-cgan.json).

**Controles de la regla, C1 frente a C0.**

| Control | B1 | B2 | B3 |
|---|:---:|:---:|:---:|
| Q menor | Sí | Sí | No |
| Error espacial de borde estrictamente menor | Sí | Sí | Sí |
| Ningún Q por geometría mayor | No (`geo-val-01`) | No (`geo-val-01`, `geo-val-02`) | No (`geo-val-01`) |
| Cielo no peor | No | Sí | Sí |
| Borde no peor | Sí | Sí | Sí |
| Mismo soporte de contraste | Sí | Sí | Sí |
| Error de contraste no mayor | Sí | No | Sí |
| SSIM no menor | Sí | Sí | No |
| PSNR no menor | No | Sí | No |
| Controles satisfechos | 6/9 | 7/9 | 5/9 |
| Decisión del evaluador | `compromiso_o_sin_mejora` | `compromiso_o_sin_mejora` | `compromiso_o_sin_mejora` |

## 5. Síntesis pareada

Diferencias C1 − C0. En Q y en los errores, un valor negativo favorece a C1; en SSIM y PSNR, uno positivo. Q, cielo y borde están en puntos porcentuales.

| Medida | B1 | B2 | B3 | Mediana | Rango |
|---|---:|---:|---:|---:|---|
| Q | −1,431 | −0,653 | +0,468 | −0,653 | [−1,431; +0,468] |
| Cielo | +0,012 | −0,148 | −0,074 | −0,074 | [−0,148; +0,012] |
| Borde (espacial) | −4,255 | −4,218 | −3,968 | −4,218 | [−4,255; −3,968] |
| Contraste | −0,0290 | +0,0177 | −0,0085 | −0,0085 | [−0,0290; +0,0177] |
| SSIM | +0,00006 | +0,00039 | −0,00032 | +0,00006 | [−0,00032; +0,00039] |
| PSNR (dB) | −0,010 | +0,063 | −0,051 | −0,010 | [−0,051; +0,063] |

`concordant_pairs: 0`, `pairs_reducing_Q: 2` y `decision: dependencia_de_semilla_o_compromiso`. El único cambio de dirección constante y de magnitud apreciable es la reducción del error espacial de borde. Las diferencias de SSIM y PSNR son pequeñas y cambian de signo entre parejas. El aumento de Q en `geo-val-01` se repite en las tres: +0,98, +1,75 y +3,61 puntos porcentuales.

## 6. Diagnóstico por anomalía

| Anomalías (24 combinaciones de vista y anomalía) | B1 | B2 | B3 |
|---|---:|---:|---:|
| Mayor magnitud del sesgo medio que C0 | 9 | 12 | 13 |
| Mayor magnitud del sesgo medio que la cGAN inicial | 6 | 7 | 6 |

Fuentes: `anomalias-cgan.json` y `anomaly_diagnostics` de cada evaluación.

El cuerpo denso de `geo-val-03` sigue concentrando los mayores sesgos de C1. El sesgo firmado medio más alto es +17,7 % en B1 (V5; C0: +27,3 %), +32,3 % en B2 (V2; C0: +30,7 %) y +25,7 % en B3 (V5; C0: +22,0 %), sobre referencias de 163 a 210 cuentas y de 379 a 524 píxeles. Estos porcentajes se refieren a cuentas respecto de la referencia idealizada y no equivalen a error de densidad. Las figuras del evaluador (`geo-val-01.png` a `geo-val-03.png` en cada carpeta `evaluacion/`) cubren las 18 vistas de cada pareja.

## 7. Lectura

Con la regla fijada antes de ejecutar, el resultado es **dependiente de la semilla o de compromiso**. Sin embargo, el efecto buscado por E1 aparece en las tres parejas: el término espacial reduce el error píxel a píxel del borde en unos 4 puntos porcentuales, alrededor de un 37 % relativo, frente a un control que ya incluía el término regional. Esa reducción no se acompaña de una mejora general:

- `geo-val-01` empeora siempre.
- Q, cielo, contraste, SSIM y PSNR cambian de dirección según la semilla.

No se sustituyó ninguna semilla ni se modificaron coeficiente, épocas o tolerancias.

Frente a la cGAN inicial, las seis continuaciones tienen menor Q global y menores errores de cielo y borde, y también menor SSIM y PSNR. La entrada sin red conserva un Q (1,81 %) menor que cualquier continuación.

Las tres parejas no estiman la variabilidad de entrenamientos desde cero ni la generalización. Tampoco se abrieron test ni generalización.

## 8. Archivos binarios

No se versionan. El [inventario de la guía](datos/ensayo-borde-e1/inventario-entrega.json) registra 216 archivos, 55 de ellos destinados a Drive:

- los 18 `last.pt`: 12 técnicos y 6 finales;
- las 21 predicciones;
- la caché de máscaras: manifiesto y 15 NPZ.

En total suman 5.952.730.120 bytes, con tamaño y SHA-256 de cada uno. Todos los archivos del pod se copiaron a almacenamiento local y se verificaron contra un manifiesto generado en el pod: 246 de 246. La copia de Drive se verificó contra [binarios.sha256](datos/binarios.sha256), que reproduce las huellas del inventario para los 55 binarios: 55 de 55. El enlace público lista los 55 binarios sin sesión iniciada, y una descarga pública de `binarios.sha256`, un `last.pt` y un arreglo de predicciones coincide con sus huellas ([verificacion-drive-binarios.json](datos/verificacion-drive-binarios.json)).

**Copia de distribución:** [carpeta de Drive oe2-borde-cgan-f05](https://drive.google.com/drive/folders/1cuOFqrq8BbWTDSpdIegLpPK5jmLz3TMF), con las rutas relativas del inventario, `binarios.sha256`, `binarios.tamanos.txt` y `LEEME.txt`.

## 9. Reproducción

1. Clonar la rama en `/workspace/repo` y copiar `verificacion/` a `/workspace` (`comun.sh` fija las rutas y la asignación de parejas a GPU).
2. `bash etapa0_preparar.sh`: instala el entorno, descarga y verifica los datos, prepara las máscaras y registra el commit y el estado de Git.
3. `bash etapa1_tecnica.sh`: fase técnica de las tres parejas. Termina con código distinto de cero si alguna aceptación no es exacta.
4. `bash etapa2_piloto.sh`: piloto; el orquestador exige las tres aceptaciones.
5. `bash etapa3_evaluacion.sh`: evaluación, síntesis e inventario.

Las huellas de esta entrega están en [huellas.sha256](huellas.sha256).

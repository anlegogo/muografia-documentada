# Resultados del piloto OE2 al 5 %

2026-10-03 (Colombia). Ejecución del protocolo [OE2-P04](../../PROTOCOLO_PILOTO_F05.md) según las [instrucciones del piloto](../../INSTRUCCIONES_PILOTO_SC3.md), con el código de `main` en `86cb6eb00411d7af9f8329ac9e445137bc7259cf` sin modificaciones. Se compararon la U-Net `unet_dc_5` entrenada solo con L1 y la misma U-Net con el crítico `patch_critic_70` (cWGAN-GP), sobre los 1.440 pares de entrenamiento y los 360 de validación de la fracción 0,05.

**Resultado.** La etapa técnica y el piloto completo superaron todas las comprobaciones automáticas (`technical_checks_passed: true` en ambos resúmenes). Las dos redes mejoran la entrada sin red en SSIM y PSNR de validación. La U-Net con L1 supera a la cWGAN-GP en ambas métricas, en las 18 referencias de validación. La aceptación técnica no acredita calidad física, y la comparación se basa en una sola semilla.

## 1. Condiciones de ejecución

| Elemento | Valor |
|---|---|
| Código | `main` `86cb6eb`, extraído con `git archive` ([commit-codigo.txt](datos/commit-codigo.txt)); `implementation_sha256` `f2dcc640…b263a`, idéntica en los cuatro registros |
| Datos | Contrato `contrato-datos-v1.json` (SHA-256 `80db70d7…8b03`); [123 de 123 archivos verificados](datos/entorno/verificacion-datos.txt) antes de entrenar |
| Hardware | Pod RunPod con 2 × NVIDIA L40S de 46 GB (capacidad 8.9), driver 580.126.09, 128 hilos de CPU |
| Entorno | Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.4.4, SciPy 1.18.1, scikit-image 0.26.0, Matplotlib 3.11.1 ([pip-freeze.txt](datos/entorno/pip-freeze.txt), [python-torch.txt](datos/entorno/python-torch.txt), [nvidia-smi.txt](datos/entorno/nvidia-smi.txt)) |
| Asignación | Etapa A en la GPU 0; etapa B con la U-Net en la GPU 0 y la cWGAN-GP en la GPU 1, en paralelo y en directorios distintos |
| Intervalo | Etapa A de 21:43:26 a 21:43:53 UTC; etapa B de 21:44:03 a 22:03:05 UTC ([registros](datos/logs/)) |

**Desviaciones respecto de las instrucciones, sin cambios en configuración, semilla, épocas ni datos.**

1. **Se usó RunPod en lugar de SC3.** En SC3 las dos Titan X estaban ocupadas por trabajos de otro usuario y la cuota de `/home` estaba en 19,55 de 20 GB. Por eso no hay identificadores SLURM y los tiempos son de reloj del pod.
2. **El código no es un clon Git.** Se extrajo con `git archive`, de modo que el motor registra `git_commit: "unknown"`. La identidad del código queda fijada por el commit registrado y por `implementation_sha256`.
3. **Los datos se obtuvieron de la copia de Drive.** Las huellas del contrato corresponden a la copia de distribución en Drive, no a la copia local de la rama de entrega del OE1, cuyos archivos difieren por compresión. 70 archivos se descargaron en el pod y 53 desde otro equipo, porque Drive limitó las descargas desde la IP del pod. Todos se verificaron contra el contrato ([fetch_data.py](verificacion/fetch_data.py), [drive-ids.tsv](verificacion/drive-ids.tsv)).

## 2. Comprobación técnica (etapa A)

Los cuatro comandos terminaron con código 0 y sin salida de error. Cada método terminó la primera época con `stop_file`, que es la interrupción prevista, y completó la segunda al reanudar. [resumen-tecnico.json](datos/resultados/resumen-tecnico.json): diez comprobaciones satisfactorias por método, `same_contract: true` y `local_cpu_check_only: false`.

## 3. Piloto completo (etapa B)

Ambos métodos se detuvieron por parada temprana: ocho validaciones sin mejorar en al menos 0,001. En los dos casos el mejor `val_ssim` correspondió a la época 5. [resumen-piloto.json](datos/resultados/resumen-piloto.json).

| Método | Mejor época | Épocas | SSIM modelo | SSIM entrada | Diferencia | Tiempo total | Tiempo por época | Memoria máx. reservada |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| U-Net (L1) | 5 | 12 | 0,8437 | 0,7518 | +0,0919 | 200,6 s | 16,2 s | 2,37 GB |
| cWGAN-GP | 5 | 13 | 0,8228 | 0,7518 | +0,0710 | 1.134,0 s | 86,7 s | 2,50 GB |

El tiempo por época excluye la primera. El tiempo total corresponde a la sesión de entrenamiento según `piloto-sesiones.jsonl`. Las curvas de validación y de pérdidas son finitas y no muestran divergencia ni colapso ([figuras](figuras/)):

- **U-Net:** la pérdida L1 de entrenamiento desciende de forma monótona. El SSIM de validación se estabiliza entre 0,842 y 0,844 a partir de la época 4.
- **cWGAN-GP:** el SSIM de validación oscila entre 0,803 y 0,823 sin tendencia sostenida. La estimación de Wasserstein baja hasta la época 9 y luego sube de nuevo, de 1,10 a 1,49. La penalización de gradiente se mantiene por debajo de 0,07.

## 4. Mejora frente a la entrada y aporte de la componente adversaria

Se calcularon SSIM y PSNR por imagen sobre los 360 pares de validación con `best.pt` de cada método y las funciones de métrica del director ([analizar_piloto_val.py](verificacion/analizar_piloto_val.py), [metricas-por-imagen-val.csv](datos/analisis-val/metricas-por-imagen-val.csv), [analisis-val.json](datos/analisis-val/analisis-val.json)).

Las medias reproducen exactamente el `best_val_ssim` de cada registro. Los intervalos son percentiles del 95 % de un bootstrap por conglomerados: las 18 referencias (geometría, vista) se remuestrean con 10.000 réplicas y semilla 20261003. El análisis es descriptivo y no interviene en la selección.

| Comparación | ΔSSIM [IC 95 %] | ΔPSNR, dB [IC 95 %] | Referencias con diferencia positiva |
|---|---|---|---:|
| U-Net − entrada | +0,0919 [0,0889; 0,0946] | +8,74 [8,65; 8,82] | 18/18 |
| cWGAN-GP − entrada | +0,0710 [0,0692; 0,0726] | +6,94 [6,87; 7,01] | 18/18 |
| cWGAN-GP − U-Net | −0,0209 [−0,0226; −0,0193] | −1,80 [−1,82; −1,78] | 0/18 |

La ordenación se repite en las tres geometrías de validación. En SSIM:

| Geometría | Entrada | U-Net | cWGAN-GP |
|---|---:|---:|---:|
| `geo-val-01` | 0,727 | 0,825 | 0,800 |
| `geo-val-02` | 0,775 | 0,859 | 0,842 |
| `geo-val-03` | 0,753 | 0,847 | 0,827 |

En este piloto, la componente adversaria **reduce** SSIM y PSNR respecto de la misma U-Net entrenada solo con L1.

**Alcance del intervalo.** Recoge la variabilidad entre referencias de validación condicionada a un único entrenamiento por método. No incluye la variabilidad entre semillas ni entre geometrías no vistas. Con tres geometrías de validación y una semilla, la diferencia no puede generalizarse como ventaja establecida de un método.

## 5. Observaciones cualitativas

Las figuras `samples/` (épocas 5 y 10 de cada método) muestran las cuatro primeras realizaciones de `geo-val-01`, vista 0. Esta geometría contiene únicamente un conducto vertical de 2,071 g/cm³.

- **U-Net.** La predicción es suave. Elimina el grano de conteo de la entrada y también el que contiene la referencia, que es finita y ruidosa. Aparecen bandas horizontales de intensidad en la parte baja del edificio.
  - En la época 10 surge un punto oscuro circular en el interior del cono, en la misma posición en las cuatro realizaciones. Por su forma y signo no corresponde al conducto definido y debe considerarse un posible artefacto.
  - En la época 5, la seleccionada, solo se observa una mancha tenue en esa región.
- **cWGAN-GP.** La predicción reproduce una textura granular semejante a la de la referencia. Las métricas píxel a píxel penalizan ese grano porque no coincide con el ruido particular de la referencia, lo que es coherente con su menor SSIM y PSNR. No se observa el punto oscuro.

Estas observaciones se basan en cuatro realizaciones de una sola vista y no certifican fidelidad física. La preservación de anomalías no se evaluó, porque el protocolo del piloto no define métricas regionales y las reserva para el protocolo de evaluación posterior.

## 6. Pesos

Los pesos no se versionan en Git. Huellas y tamaños de los ocho archivos: [pesos.sha256](datos/pesos.sha256) y [pesos.tamanos.txt](datos/pesos.tamanos.txt).

| Archivo | Tamaño (bytes) | SHA-256 |
|---|---:|---|
| `oe2-v1-piloto-f05-unet-s2026100301/checkpoints/best.pt` | 246.595.774 | `734bc5dc1aa4cdc16a3fa0b6de2d58da7575c5bd0b1fe342bc266283f0e8e57a` |
| `oe2-v1-piloto-f05-cgan-s2026100301/checkpoints/best.pt` | 279.758.342 | `e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0` |

Los ocho archivos (`best.pt` y `last.pt` de las cuatro ejecuciones) se copiaron desde el pod a almacenamiento local y se verificaron allí: 8 de 8 huellas coinciden. **Copia de distribución:** [carpeta de Drive oe2-piloto-f05-pesos](https://drive.google.com/drive/folders/18pOGXzN2lEhKfxJlpcC4GuTujkNyA-ix), con los ocho pesos, `pesos.sha256`, `pesos.tamanos.txt` y un `LEEME.txt`. Los ocho archivos se descargaron desde el enlace público, sin sesión iniciada, y sus huellas coinciden con las de esta entrega: 8 de 8 ([verificacion-drive-pesos.json](datos/verificacion-drive-pesos.json)).

## 7. Lectura según el protocolo

Corresponde a la decisión 2 del protocolo: **funcionamiento correcto y calidad inconclusa respecto de la componente adversaria.** Ambos métodos funcionan y mejoran la entrada. La cWGAN-GP no mejora a la U-Net en las métricas definidas, y la U-Net presenta un posible artefacto después de la época seleccionada. No se inició ninguna otra fracción ni la campaña de 24 entrenamientos. No se abrieron las particiones de prueba ni de generalización: el protocolo del piloto las excluye y el contrato de datos no las contiene.

## 8. Reproducción

- [pod_setup.sh](verificacion/pod_setup.sh): entorno.
- [fetch_data.py](verificacion/fetch_data.py): datos verificados.
- [run_stage.sh](verificacion/run_stage.sh): comandos de las instrucciones, con salida estándar, errores y código de salida en `datos/logs/`.
- [analizar_piloto_val.py](verificacion/analizar_piloto_val.py): análisis por imagen.
- [figuras_piloto.py](verificacion/figuras_piloto.py): figuras PDF vectoriales generadas desde `metrics.jsonl` con pdfLaTeX.

Los registros completos de las cuatro ejecuciones (`record/`, `metrics.jsonl`, `summary.json`, `piloto-entorno.json`, `piloto-sesiones.jsonl`, `baseline-entrada.json` y `samples/`) están en [datos/resultados/](datos/resultados/). Las huellas de esta entrega están en [huellas.sha256](huellas.sha256).

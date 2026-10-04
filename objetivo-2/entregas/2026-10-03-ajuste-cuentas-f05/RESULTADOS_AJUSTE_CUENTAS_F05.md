# Resultados del ajuste de cuentas al 5 %

2026-10-03 (Colombia). Ejecución del [diseño](../../DISENO_AJUSTE_CUENTAS_F05.md) y de las [instrucciones](../../INSTRUCCIONES_AJUSTE_CUENTAS_F05.md) del ajuste acotado de conservación de cuentas. Se usó el código de `main` en `66548a69bb21575323a4eaa2a9f805868f798a62`, sin modificaciones.

Se compararon dos continuaciones de cinco épocas del mismo `best.pt` U-Net del piloto (SHA-256 `734bc5dc…e57a`). Ambas usan los mismos datos, semilla (2026100302), orden, optimizador nuevo y presupuesto. La rama **A** conserva la pérdida `100·L1`. La rama **B** añade el término regional `L_reg` con coeficiente 1. La única diferencia entre configuraciones es `lambda_regional`: 0 en A y 1 en B.

**Resultado según la regla del director: compromiso** (`decision: compromiso` en [comparacion-piloto.json](datos/comparacion-piloto.json)):

- B reduce el indicador principal Q de 13,29 % a 11,24 %, y no aumenta Q en ninguna de las tres geometrías de validación.
- B empeora nominalmente el error absoluto de cuentas en el borde y el PSNR.

La clasificación es descriptiva. Una única ejecución por rama no permite afirmar significación ni ventaja establecida.

## 1. Ejecución

| Elemento | Valor |
|---|---|
| Código | `main` `66548a6`, extraído con `git archive` sin conversión de fin de línea ([commit-codigo.txt](datos/commit-codigo.txt)) |
| Hardware | Pod RunPod con 1 × NVIDIA L40S de 46 GB (capacidad 8.9) y driver 570.124.06 ([nvidia-smi.txt](datos/entorno/nvidia-smi.txt)) |
| Entorno | Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.3.5, SciPy 1.18.1, scikit-image 0.26.0, Matplotlib 3.11.1 y filelock 3.16.1 ([pip-freeze.txt](datos/entorno/pip-freeze.txt)). Son las versiones verificadas por la dirección, con PyTorch sustituido por su compilación CUDA |
| Datos | 30 shards de train y val y el `best.pt` inicial, descargados de las copias de Drive y verificados contra el contrato v1: 31 de 31 ([datos.log](datos/datos.log), [fuentes-drive.tsv](verificacion/fuentes-drive.tsv)) |
| Máscaras | 15 geometrías y 90 mapas ([manifiesto-mascaras.json](datos/manifiesto-mascaras.json)) |
| Intervalo (UTC, 2026-10-04) | Máscaras 02:03:17–02:03:20; etapa técnica 02:03:20–02:04:25; A 02:04:25–02:07:29; B 02:07:29–02:10:34; evaluación y figuras hasta 02:11:19 ([registros](datos/logs/)) |

Los trece pasos terminaron con código 0 y sin salida de error. Corresponden a los comandos literales de las instrucciones, ejecutados en secuencia en una GPU con [lanzar.sh](verificacion/lanzar.sh).

**Desviaciones y lecturas literales.**

1. **Se usó RunPod en lugar de SC3**, igual que en el piloto, así que no hay identificadores SLURM.
2. **Entorno.** Se tomó la lista de versiones del entorno verificado por la dirección. Difiere del entorno del piloto (NumPy 2.4.4). El ejecutor fija la identidad dentro de este ensayo y las dos ramas comparten entorno.
3. **No se fija un margen de no deterioro.** La regla del director compara valores sin redondear y exige `B ≤ A` nominalmente. No se introdujo ninguna tolerancia.

## 2. Comprobación técnica en GPU

Se ejecutaron las cuatro ejecuciones técnicas: continua y recuperada por rama, con interrupción tras la primera época. [aceptacion-gpu.json](datos/aceptacion-gpu.json) declara `gpu_accepted: true`, `technical_checks_passed: true` y `exact_recovery: true`. Cada época técnica de ocho pares tardó 0,23 s en ambas ramas, después de 2,4 s de inicialización en la primera.

## 3. Entrenamiento A/B

Las dos ramas completaron las cinco épocas sin interrupción (`completed: true`, `epoch: 5`, `resumed: false`).

| Rama | Tiempo de cómputo | Tiempo por época | Memoria CUDA máx. | L1 época 5 | L_reg época 5 | SSIM val época 5 |
|---|---:|---:|---:|---:|---:|---:|
| A: control | 174,1 s | 33,3–38,3 s | 1,89 GB | 0,008545 | 0,0298 | 0,84297 |
| B: regional | 175,5 s | 33,5–37,8 s | 1,89 GB | 0,008656 | 0,0134 | 0,84306 |

El término regional no añadió costo medible. En B, `L_reg` bajó de 0,0204 a 0,0134 mientras L1 quedaba ligeramente por encima de A. En A, `L_reg` solo se registra, porque su peso es cero. Todas las pérdidas, gradientes y predicciones fueron finitos ([curvas-ajuste.pdf](figuras/curvas-ajuste.pdf), [history A](datos/piloto/A/history.json), [history B](datos/piloto/B/history.json)).

## 4. Evaluación según los criterios del director

Las cifras salen de `evaluar_ajuste.py` sobre los 360 pares de validación, con idénticas regiones para entrada, A y B ([comparacion-metricas.pdf](figuras/comparacion-metricas.pdf)).

| Medida | Entrada | A: control | B: regional | Criterio | ¿Se cumple? |
|---|---:|---:|---:|---|:---:|
| Q (%) | 1,814 | 13,287 | 11,239 | B < A | Sí |
| Q `geo-val-01` (%) | 1,198 | 2,731 | 2,653 | B ≤ A | Sí |
| Q `geo-val-02` (%) | 2,551 | 13,953 | 11,790 | B ≤ A | Sí |
| Q `geo-val-03` (%) | 1,692 | 23,175 | 19,274 | B ≤ A | Sí |
| MAE de cielo (%) | 6,802 | 1,777 | 1,686 | B ≤ A | Sí |
| MAE de borde (%) | 12,092 | 5,139 | 5,699 | B ≤ A | **No** |
| Error de contraste (23 combinaciones comunes) | 0,2464 | 0,0868 | 0,0834 | B ≤ A | Sí |
| SSIM | 0,751812 | 0,842971 | 0,843064 | B ≥ A | Sí |
| PSNR (dB) | 24,1677 | 32,8188 | 32,7686 | B ≥ A | **No** |

El sesgo firmado medio regional, por familia y promediado sobre vistas y regiones, es:

| Familia | A | B |
|---|---:|---:|
| Roca sin anomalía | −1,28 % | +0,45 % |
| Anomalías | −26,93 % | −23,96 % |
| Cielo | −0,90 % | +0,33 % |
| Borde | −0,75 % | −1,10 % |

**Lectura.** Con los criterios fijados de antemano:

- **Conservación.** Mejora: Q baja 2,05 puntos (−15,4 % relativo) y baja en cada geometría. El sesgo de anomalías se reduce, pero sigue siendo grande (−24 %).
- **Calidad.** Se mantiene en SSIM (+0,00009) y en el error de contraste. No se mantiene en PSNR (−0,050 dB) ni en el MAE de borde (+0,56 puntos).

El resultado corresponde a la categoría «compromiso», no a una mejora concordante.

La entrada sin red tiene Q de 1,81 %, muy por debajo de ambas redes. El adelgazamiento binomial reescalado es insesgado en esperanza, de modo que las dos variantes introducen sesgos regionales que la entrada no tiene, aunque reducen mucho su error píxel a píxel.

## 5. Análisis complementario (fuera de la regla de decisión)

[analizar_cuentas.py](verificacion/analizar_cuentas.py) calcula por imagen el error relativo de cuentas totales en la imagen completa y por familia, para la entrada, el modelo inicial de la época 5, A y B ([cuentas-complementario.json](datos/analisis-complementario/cuentas-complementario.json), [cuentas-por-imagen.csv](datos/analisis-complementario/cuentas-por-imagen.csv), [error-cuentas.pdf](figuras/error-cuentas.pdf)).

Los intervalos del 95 % se obtienen por bootstrap en dos niveles, primero sobre geometrías y luego sobre vistas, con 10.000 réplicas y semilla 20261004. Son descriptivos: con tres geometrías y una ejecución por rama no recogen la variabilidad entre entrenamientos.

| Diferencia pareada | Media | IC 95 % |
|---|---:|---|
| \|error total\|, B − A | −0,57 puntos | [−1,40; −0,14] |
| \|error en roca\|, B − A | −1,21 puntos | [−2,42; +0,28] |
| \|error en anomalías\|, B − A | −1,76 puntos | [−3,07; −0,24] |
| \|error en borde\|, B − A | +0,35 puntos | [+0,12; +0,70] |
| SSIM, B − A | +0,00009 | [−0,00158; +0,00098] |
| PSNR, B − A | −0,050 dB | [−0,121; −0,004] |

El análisis por imagen coincide en dirección con la evaluación del director: mejor conservación en anomalías, en cielo y en el total, y peor en el borde. En roca, el intervalo incluye el cero. En SSIM, el intervalo incluye el cero, lo que **no demuestra equivalencia**. Solo indica que este ensayo no detecta una diferencia.

El modelo inicial de la época 5 presenta un error medio en roca de −16,96 %, coherente con el −16,97 % del diagnóstico regional del director, y un error total de +3,90 %. **La continuación sin término regional (A) ya reduce el error medio en roca a −1,28 %.** Gran parte de la corrección del sesgo en roca proviene de continuar el entrenamiento con tasa de aprendizaje menor. El aporte específico del término regional es la diferencia B − A informada arriba.

## 6. Observaciones cualitativas

Las [figuras del director](datos/figuras-piloto/) muestran las 18 vistas, con referencia, entrada media, A, B y sus residuos a escala común. Las predicciones de A y B son visualmente casi indistinguibles. Ambas conservan las bandas horizontales de intensidad en la parte baja del cono que se observaron en el piloto, y sus residuos muestran una estructura en bandas semejante. La inspección no sustituye las métricas y no certifica fidelidad física.

## 7. Archivos binarios

No se versionan. Se calcularon las huellas y tamaños de los seis `last.pt` (cuatro técnicos y dos finales) y de las seis predicciones de validación ([binarios.sha256](datos/binarios.sha256), [binarios.tamanos.txt](datos/binarios.tamanos.txt)). Se copiaron a almacenamiento local y se verificaron allí: 12 de 12 huellas coinciden.

| Archivo | SHA-256 |
|---|---|
| `piloto/A/last.pt` | `f82680767c5c84d573a5d3a44a074a0540cf06502ca51469483890e640d3638d` |
| `piloto/B/last.pt` | `9788ccea4639ddeec317548d314703ec3badffa322983224fac6575db30d811e` |

La copia de distribución en Drive se registrará con su enlace y su verificación.

## 8. Reproducción

1. Copiar la carpeta `verificacion/` al pod, junto con `git archive` de `66548a6` en `/workspace/repo`.
2. `bash instalar_entorno.sh /workspace`
3. `python3 sincronizar_datos.py fuentes-drive.tsv /workspace/insumos`
4. `bash lanzar.sh /workspace`. El lanzador es idempotente y reanuda una rama interrumpida con `--reanudar`.
5. Desde los datos entregados: `python verificacion/figuras_ajuste.py datos figuras`

Las huellas de esta entrega están en [huellas.sha256](huellas.sha256).

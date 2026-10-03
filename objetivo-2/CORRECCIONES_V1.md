# Correcciones de implementación del OE2 — versión 1

**2026-10-03. OE2-P01, P02 y P03 resueltos para la implementación derivada y la distribución fijada.** Se verificó entrenamiento, guardado y reanudación en CPU. Continúan pendientes el protocolo de entrenamiento prolongado, la comprobación en GPU y la evaluación del desempeño (OE2-P04). El cierre del OE1 permanece vigente.

## Procedencia y alcance

La [implementación](implementacion/scripts/training/engine.py) deriva del repositorio estudiantil b88fa57. Se reutilizan los generadores, el crítico y el motor, con modificaciones delimitadas; se sustituye el lector por un contrato explícito. Las [huellas de procedencia](evidencias/procedencia-implementacion-v1.json) distinguen archivos de origen y derivados. No se editan originales ni se fusiona la rama estudiantil. Los comentarios históricos conservados describen la base y no sustituyen este procedimiento vigente.

Los pesos anteriores son antecedentes; no se cargan como reanudación de esta versión. La corrección de GP y el cambio de normalización requieren nuevos entrenamientos. No se afirma que una prueba técnica de dos pasos consiga calidad de reconstrucción.

## P01: puntuación común para el crítico

Se define, para cada muestra i y sus P parches,

\[
C_i(x_i,y_i)=P^{-1}\sum_{p=1}^{P}D_{ip}(x_i,y_i).
\]

Las pérdidas adversarias y la penalización usan esta misma puntuación. Se diferencia cada puntuación respecto de la imagen interpolada, sin dividir el gradiente individual por el tamaño del lote:

\[
L_D=\frac1B\sum_i[C_i(x_i,G(x_i))-C_i(x_i,y_i)]
+\lambda_{\mathrm{GP}}\frac1B\sum_i(\|\nabla_{\hat y_i}C_i(x_i,\hat y_i)\|_2-1)^2.
\]

La [función corregida](implementacion/scripts/training/losses.py) conserva la interpolación aleatoria por muestra y la pérdida L1 del generador. Doce casos analíticos verifican normas 1 y 2, lotes de 1 y 2, y mapas de 1×1, 14×14 y 30×30: GP es respectivamente 0 y 1, independientemente del número de parches y del lote. Se conserva la [evidencia anterior](evidencias/revision-2026-10-03.json).

## P02: normalización disponible en inferencia

Se adopta `train_log_bounded_v1`. El máximo M se obtiene exclusivamente de las referencias de las doce geometrías de entrenamiento; se congela una sola escala para todas las vistas y fracciones:

\[
M=3786,\qquad s=\log(1+\max(1,M))=8.239329427901795.
\]

Para un conteo no negativo c se define

\[
T_s(c)=\frac{\log(1+c)}{s+\log(1+c)},\qquad
x=T_s(n_{\mathrm{low}}/f),\quad y=T_s(n_{\mathrm{ref}}).
\]

La entrada utiliza únicamente la imagen de baja estadística, su fracción conocida f y la escala congelada. Cambiar la referencia de una pareja no cambia x; esta propiedad se comprobó a través del lector real. Validación utiliza la misma s; no se ajusta con sus máximos ni con test/generalization.

La transformación conserva el carácter logarítmico, es monótona y mantiene cualquier conteo finito razonable dentro de [0,1), compatible con la salida sigmoide, sin recortar referencias por superar el máximo de entrenamiento. Una imagen vacía produce ceros. La inversión es

\[
T_s^{-1}(z)=\exp\!\left(\frac{s z}{1-z}\right)-1,\quad 0\le z<1.
\]

Se recuperan conteos equivalentes a la referencia, no conteos adelgazados. Una salida exactamente igual a uno o fuera del rango numérico invertible se rechaza explícitamente; no se oculta mediante recorte. La prueba incluye ida/vuelta para 0, 1, 100, 4.000 y 1.000.000 cuentas, las cuatro fracciones y entradas inválidas.

**Implicación metodológica:** SSIM, PSNR y L1 se calculan ahora en otra representación. No son directamente comparables con las tablas históricas. Esta elección resuelve la disponibilidad de la transformación en inferencia; su conveniencia científica debe evaluarse con el protocolo OE2-P04, incluyendo el baseline bajo la misma transformación. No se declara una normalización óptima.

Las funciones `normalize_input`, `normalize_counts` e `inverse_counts` se encuentran en el [lector](implementacion/scripts/training/muography_dataset.py). La escala se guarda en manifiesto, registro y checkpoint para su reutilización en inferencia.

## P03: datos fijados y reanudación protegida

Se exige raíz de datos, manifiesto y SHA-256 esperado explícitos. El [manifiesto v1](evidencias/contrato-datos-v1.json) vincula particiones, normalización, metadatos, 15 shards train/val, 90 paquetes fuente y los informes de distribución. Su huella es:

```text
80db70d75e5ef2c40955881a87dd46b767137c24cb72dc1aa458a71c1efd8b03
```

La preparación comprueba los 7.200 pares directamente contra los paquetes de origen, formas, tipos, fracciones, ausencia de solapamiento entre particiones y conteos bajos no superiores a su referencia. El entrenamiento verifica los archivos antes de consumirlos; el lector verifica nuevamente los bytes de cada shard que carga. La reanudación revalida los archivos y rechaza identidades distintas de datos, normalización o implementación. También rechaza checkpoints históricos sin este contrato y configuraciones distintas en el mismo directorio.

La identidad del código utiliza SHA-256 sobre las fuentes Python con saltos de línea normalizados. La ubicación física de los datos no forma parte de su identidad: se permite trasladar los mismos archivos. El manifiesto se publica con finales LF para conservar su huella en Windows y Linux. No se admite sustituir una distribución comprimida por otra de contenido equivalente bajo esta identidad: debe emitirse un manifiesto nuevo, con nueva procedencia.

La recuperación del convertidor histórico citado como `analysis/convert_oe1_package.py` sigue siendo un antecedente documental no recuperado en esta sesión. La integración resuelta no depende de ejecutar ese convertidor: comprueba independientemente sus salidas contra cada paquete train/val y fija los archivos resultantes. No se atribuye al código nuevo la creación original de dataset-v2. La reproducción exacta del convertidor de los estudiantes continúa como seguimiento de procedencia, separada de la corrección del vínculo datos–entrenamiento.

El lector de esta versión permite únicamente train/val. Los subconjuntos de prueba técnica están identificados mediante `smoke_train_pairs` y `smoke_val_pairs`; sus límites se incluyen en la configuración y no deben trasladarse inadvertidamente a una campaña. Se deshabilita el adelgazamiento adicional y la reanudación a mitad de época en esta versión; la prueba usa pares congelados y checkpoints al terminar época.

## Verificación realizada

La [evidencia de correcciones](evidencias/correcciones-v1.json) contiene **17 controles satisfactorios**, con una familia de doce casos matemáticos para GP. Se utilizó el generador completo `unet_dc_5` de 20.543.809 parámetros y el crítico de 2.762.817 parámetros, no redes sustitutas pequeñas.

- Dos actualizaciones de entrenamiento sobre un par train y validación sobre un par val, fracción 0,05; una actualización del crítico por paso en esta prueba.
- Repetición con interrupción al terminar la primera época y reanudación de la segunda: los pesos del generador y del crítico coinciden exactamente con la ejecución continua. Esto comprueba funcionalmente la recuperación de optimizadores y estado aleatorio.
- Pérdidas, gradientes y métricas finitos; archivos `last.pt` y `best.pt` generados.
- Rechazo comprobado de datos alterados, manifiesto incorrecto, checkpoint histórico y cambios en identidad de código, datos y normalización.
- Sin imágenes de test/generalization. No se ejecutó una campaña de entrenamiento ni una prueba CUDA.

Como ajuste del mismo ciclo de guardado, `best.pt` ahora sigue el máximo de SSIM sin redondear; la mejora mínima para paciencia se lleva por separado. Con batch=1, el indicador de dispersión entre imágenes vale cero por construcción y no informa sobre colapso.

Entorno: Python 3.12.14, PyTorch 2.6.0+cpu, NumPy 2.4.4, dos hilos. Las [dependencias verificadas](requirements-cpu-verificado.txt) describen CPU; no constituyen una selección automática de CUDA para SC3.

## Reproducción y uso

Los comandos se ejecutan desde la raíz de la réplica, en un entorno con las dependencias verificadas. Los datos pesados permanecen fuera de Git. `trabajo/drive-2026-10-03` debe contener la distribución fijada completa, incluidos `pares/` y `dataset-v2/`.

Para repetir todos los controles, escoger un directorio de trabajo nuevo:

```powershell
python objetivo-2/herramientas/probar_correcciones.py --data-root trabajo/drive-2026-10-03 --manifest objetivo-2/evidencias/contrato-datos-v1.json --work trabajo/oe2-prueba-nueva --output trabajo/oe2-prueba-nueva.json
```

Para ejecutar únicamente el entrenamiento técnico desde la interfaz habitual:

```powershell
python objetivo-2/implementacion/scripts/training/train_cwgan_gp.py --config objetivo-2/implementacion/scripts/training/configs/smoke_v1.json --data-root trabajo/drive-2026-10-03 --data-manifest objetivo-2/evidencias/contrato-datos-v1.json --manifest-sha256 80db70d75e5ef2c40955881a87dd46b767137c24cb72dc1aa458a71c1efd8b03 --out-root trabajo/oe2-runs --resume none
```

Los checkpoints quedan en `trabajo/oe2-runs/oe2-v1-smoke/checkpoints/` y los registros en su subdirectorio `record/`. Para reanudar, utilizar exactamente la misma configuración y `--resume auto`. La recuperación ya fue comprobada con una interrupción real al finalizar época; repetir el comando después de completar ambas épocas no añade entrenamiento.

Para otra distribución se puede emitir un manifiesto mediante el lector con `--data-root` y `--output`; no se debe sobrescribir el manifiesto fijado. Preparar otra distribución constituye un cambio de experimento y no habilita reanudar pesos anteriores.

La siguiente actividad es diseñar OE2-P04 y comprobar el entorno GPU con un ensayo corto. No corresponde lanzar todavía un entrenamiento prolongado con la configuración smoke ni interpretar sus métricas como resultado del objetivo.

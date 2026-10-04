# Ejecución del complemento OE3-C1

## Encargo

Se evaluará qué ocurre cuando los mismos modelos reciben 1 %, 10 % y 50 % de los conteos. El bloque 5 % ya existe y se reutiliza. También se medirá la señal y el contraste local de las anomalías. El propósito es completar la evaluación comprometida en la propuesta y determinar el mínimo de entrada estudiado bajo el benchmark documentado, conservando resultados desfavorables.

No se entrenan modelos, no se modifican pesos ni se simulan nuevos muones. Se conservan los ocho modelos; no se elige una semilla a partir de los resultados conocidos. Revisar primero el [protocolo](PROTOCOLO_COMPLEMENTO_OE3.md).

## Preparación

Actualizar la rama de trabajo con `origin/main`, conservando cambios propios y registrando el commit utilizado. Usar un checkout que preserve los bytes de las fuentes congeladas; no reformatear archivos para resolver una discrepancia de huella. Si existen cambios locales, integrarlos conscientemente antes de ejecutar; no usar un reinicio forzado.

Se necesitan:

- Python con el entorno de inferencia EF-01: NumPy, PyTorch, scikit-image y filelock. Conservar versión de PyTorch/CUDA y equipo en los recibos.
- Los cuatro shards y metadatos bajo `dataset-v2/shards` de la distribución OE1 verificada.
- Un JSON con las rutas locales de los ocho pesos, según el [ejemplo EF-01](../objetivo-2/configuraciones/pesos-evaluacion-final-ejemplo.json).
- La carpeta original de predicciones EF-01 al 5 %, con sus ocho carpetas de modelo, NPY, recibos y `completed.json`. No basta copiar solo los NPY.
- El registro `objetivo-2/evidencias/ef01-c2/controles.json`, en los bytes publicados.

Reservar unos 3,02 GB para las 96 matrices nuevas, además de las predicciones al 5 %, pesos, datos e informes. No se fija una duración de GPU sin medirla; el primer modelo permite estimar tiempo restante. Un máximo de tres trabajadores puede repartir **modelos completos distintos** en dispositivos distintos, conservando lote cuatro y un único escritor por modelo. No se cambian tamaños de lote para utilizar más GPU. Cada trabajador ejecuta su propia prueba técnica por modelo.

## Comandos en Linux/CUDA

Desde la raíz del repositorio, adaptar únicamente rutas. La salida debe ser nueva para este complemento. `set -e` detiene la secuencia ante un error técnico.

```bash
set -e
DATA=/ruta/insumos
WEIGHTS=/ruta/pesos-locales.json
EXISTING=/ruta/evaluacion-final-f05
OUT=/ruta/complemento-oe3-v1
COMMON_ARGS=(--repo . --data "$DATA" --weights "$WEIGHTS" --existing "$EXISTING" --registry objetivo-2/evidencias/ef01-c2/controles.json --output "$OUT")

python objetivo-3/herramientas/test_complemento_oe3.py
python objetivo-3/herramientas/test_flujo_complemento_oe3.py
python objetivo-3/herramientas/complemento_oe3.py preflight "${COMMON_ARGS[@]}"

for MODEL in unet_original cgan_original B1_C0 B1_C1 B2_C0 B2_C1 B3_C0 B3_C1; do
  python objetivo-3/herramientas/complemento_oe3.py smoke "${COMMON_ARGS[@]}" --model "$MODEL" --device cuda:0
  python objetivo-3/herramientas/complemento_oe3.py infer "${COMMON_ARGS[@]}" --model "$MODEL" --device cuda:0
done

python objetivo-3/herramientas/complemento_oe3.py evaluate "${COMMON_ARGS[@]}" --report "$OUT/informe"
```

En tres dispositivos, dividir explícitamente la lista de modelos; no lanzar la lista completa tres veces. Ejecutar `evaluate` una sola vez, después de finalizar los ocho modelos. La evaluación usa las matrices en CPU y no vuelve a inferir ni entrenar. Si la carpeta del informe ya existe, conservarla y elegir una carpeta nueva para una repetición justificada.

## Qué significa pasar la prueba técnica

`smoke` debe finalizar con `passed: true`: dos inferencias continuas idénticas, diferencia máxima frente al bloque 5 % no mayor de 10⁻⁴ y salidas válidas en las otras fracciones. El programa `infer` exige el recibo de esa prueba para el mismo modelo y entorno. Esto comprueba funcionamiento y compatibilidad; no garantiza que mejoren SSIM, PSNR o las anomalías.

Si falla, conservar el mensaje completo, entorno y recibos, y comunicar el fallo antes de cambiar el código. No relajar tolerancias ni entrenar para hacer pasar la prueba. Si la calidad científica es desfavorable, continuar hasta completar todos los modelos y entregar el resultado. No seleccionar únicamente las fracciones favorables.

## Entrega verificable

Subir a Drive la carpeta completa de salida, que incluirá:

1. `preflight.json` y ocho `smoke-<modelo>.json`.
2. `f001`, `f010` y `f050`: ocho modelos por fracción, cada uno con cuatro NPY, recibos, identidad y `completed.json`; 96 NPY nuevos y 11.520 imágenes.
3. `informe/resultado.json`, `imagenes.csv`, `regiones.csv`, `contrastes.json`, `metricas_locales.csv`, `snr_repeticiones.json` e `inventario.json`.
4. Registro del commit, comandos, versiones de entorno, dispositivos y fallos si existieron. No incluir contraseñas, tokens ni credenciales.

En Git, añadir un Markdown de entrega con el enlace de Drive, commit del código, fecha, modelos finalizados y resumen de cualquier incidencia. Subir también los JSON/CSV de evaluación y los recibos que no contienen matrices, o enlazarlos de forma inequívoca en el inventario de entrega. Los NPY y pesos permanecen fuera de Git. No editar protocolos o evidencia previa para ajustar el resultado.

La evaluación completa esperada contiene 17.280 filas de métricas de imagen, 4.536 regionales, 216 registros de contraste y 39.096 filas locales, contando entradas y referencia según cada tabla. Las filas repetidas por modelo/fracción no son experimentos independientes. Los nulos por dispersión o control cero deben conservarse con su causa.

El resultado se revisará antes de declarar cumplimiento. Un mínimo de fracción nulo es un resultado permitido, no un fallo del software. La actividad no implica comenzar todavía el libro/informe final.

# Instrucciones para repetir la continuación cGAN al 5 %

Fecha: 2026-10-04, America/Bogota. **Estado: integración y recuperación exacta verificadas en CPU; preparada la comprobación GPU de esta versión.** Las cinco épocas de las tres parejas nuevas todavía no se han ejecutado. Se mantiene abierto el OE2 y no se concede aceptación física.

## Propósito y alcance

La entrega anterior mostró menor sesgo regional de C1 frente a C0, junto con deterioros locales. Se busca comprobar si esa comparación se mantiene al cambiar la semilla de continuación. El [diseño fijado](DISENO_REPETICION_CGAN_F05.md) define tres parejas nuevas: R1/2026100401, R2/2026100402 y R3/2026100403. Cada pareja compara C0 sin término regional y C1 con dicho término. Se conservan todas las parejas; no se escoge la mejor semilla.

Las seis continuaciones parten del mismo checkpoint original cGAN de época 5, con generador y crítico originales y optimizadores nuevos. No se continúa desde los C0/C1 finales ni se encadenan quince épocas. SHA-256 inicial:

```text
e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0
```

Las configuraciones efectivas están en [repeticion-cgan-f05](configuraciones/repeticion-cgan-f05/). Se seleccionan mediante `--pareja R1`, `R2` o `R3`; no se editan semillas ni parámetros manualmente. El JSON `diseno.spec.json` describe el diseño, no es un archivo de entrada del ejecutor.

## Preparación del entorno

Actualizar la rama de entrega con `origin/main`, resolver cualquier conflicto antes de ejecutar y registrar el commit usado. Mantener ese código y el mismo entorno durante las tres parejas. La nueva identidad incluye pareja/semilla y nuevas huellas: **las aceptaciones y checkpoints de versiones anteriores no autorizan esta repetición**. La entrega CG-04c permanece como antecedente verificado con su versión histórica.

Basta una GPU, por ejemplo la L40S utilizada antes; no se utiliza entrenamiento distribuido. Conservar el entorno CUDA verificado por los estudiantes, registrar sus versiones y comprobarlo de nuevo con las pruebas siguientes. Se requieren PyTorch, NumPy, SciPy, scikit-image, filelock y Matplotlib; no actualizar dependencias entre parejas.

Ejecutar los bloques desde la raíz del repositorio, en Bash, en una sesión que permanezca activa. Sustituir las rutas por ubicaciones absolutas reales. `SALIDAS` debe ser un directorio nuevo y disponer de espacio para las doce ejecuciones técnicas y seis continuaciones.

```bash
set -euo pipefail
export CUDA_VISIBLE_DEVICES=0
DATA="/ruta/distribucion-verificada"
PESOS="/ruta/cgan-best-original.pt"
MASCARAS="/ruta/mascaras-ajuste-v1"
SALIDAS="/ruta/trabajo/cgan-repeticion-f05"
test ! -e "$SALIDAS"
mkdir -p "$SALIDAS"
git rev-parse HEAD > "$SALIDAS/commit.txt"
git status --porcelain > "$SALIDAS/estado-git.txt"
test ! -s "$SALIDAS/estado-git.txt"
python -m pip freeze > "$SALIDAS/entorno.txt"
nvidia-smi > "$SALIDAS/gpu.txt"
COMUN=(--datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS")
```

Reutilizar la misma caché de máscaras íntegra del ajuste anterior. Si no está disponible, prepararla una sola vez con `python objetivo-2/herramientas/datos_ajuste.py --datos "$DATA" --salida "$MASCARAS"`. No regenerarla ni intercambiarla durante el ensayo: también se comprueba la huella del NPZ comprimido. Los datos, normalización y pesos son los ya verificados; no se generan nuevos adelgazamientos ni se abren imágenes test/generalization.

## 1. Comprobación GPU de las tres parejas

Por pareja: ocho muestras train y ocho val, dos épocas, ejecución continua y otra interrumpida/recuperada de cada variante. Las métricas de estas muestras pequeñas no deciden calidad.

```bash
for PAR in R1 R2 R3; do
  T="$SALIDAS/$PAR/tecnica"
  mkdir -p "$T"
  for RAMA in C0 C1; do
    python objetivo-2/herramientas/ejecutar_ajuste_cgan.py \
      "${COMUN[@]}" --pareja "$PAR" --rama "$RAMA" --etapa tecnica \
      --salida "$T/$RAMA-continua" 2>&1 | tee "$T/$RAMA-continua.log"
    python objetivo-2/herramientas/ejecutar_ajuste_cgan.py \
      "${COMUN[@]}" --pareja "$PAR" --rama "$RAMA" --etapa tecnica \
      --salida "$T/$RAMA-recuperada" --parar-tras 1 2>&1 | tee "$T/$RAMA-interrumpida.log"
    python objetivo-2/herramientas/ejecutar_ajuste_cgan.py \
      "${COMUN[@]}" --pareja "$PAR" --rama "$RAMA" --etapa tecnica \
      --salida "$T/$RAMA-recuperada" --reanudar 2>&1 | tee "$T/$RAMA-recuperada.log"
  done
  python objetivo-2/herramientas/revisar_ajuste_cgan.py --pareja "$PAR" \
    --C0-continua "$T/C0-continua" --C0-recuperada "$T/C0-recuperada" \
    --C1-continua "$T/C1-continua" --C1-recuperada "$T/C1-recuperada" \
    --exigir-gpu --salida "$SALIDAS/$PAR/aceptacion-gpu.json" \
    2>&1 | tee "$SALIDAS/$PAR/auditoria-gpu.log"
done
```

Las **tres** auditorías deben terminar sin error y declarar `gpu_accepted: true` y `exact_recovery: true`. Se exige igualdad exacta de generador, crítico, ambos Adam, estados aleatorios, registros numéricos y predicciones. No se relaja el criterio con una tolerancia ni se reutiliza una aceptación de otra pareja.

Son doce ejecuciones técnicas, dieciocho lanzamientos de proceso por las recuperaciones, **48 actualizaciones G y 240 D**. Conservar todas las carpetas: el piloto vuelve a auditar sus checkpoints. Si se cambia su ubicación, repetir el comando del revisor con las rutas correctas.

Ante fallo técnico se conserva el registro y se detiene la secuencia antes del piloto. No cambiar determinismo, lote, coeficientes o entorno para forzar la aprobación.

## 2. Seis continuaciones de cinco épocas

Después de las tres aceptaciones GPU y con recursos disponibles, ejecutar el bloque completo. No hace falta una consulta adicional entre parejas si se mantiene el protocolo y no aparecen fallos técnicos.

```bash
for PAR in R1 R2 R3; do
  test -f "$SALIDAS/$PAR/aceptacion-gpu.json"
done
for PAR in R1 R2 R3; do
  mkdir -p "$SALIDAS/$PAR/piloto"
  for RAMA in C0 C1; do
    python objetivo-2/herramientas/ejecutar_ajuste_cgan.py \
      "${COMUN[@]}" --pareja "$PAR" --rama "$RAMA" --etapa piloto \
      --salida "$SALIDAS/$PAR/piloto/$RAMA" \
      --aceptacion-gpu "$SALIDAS/$PAR/aceptacion-gpu.json" \
      2>&1 | tee "$SALIDAS/$PAR/piloto/$RAMA.log"
  done
done
```

Cada ejecución utiliza 1.440 train y 360 val, lote 4 y cinco épocas adicionales; se selecciona la quinta sin parada temprana ni selección por el mejor SSIM. Total: **10.800 pasos G y 54.000 D**. La estimación previa es aproximadamente 65 minutos de cómputo en condiciones similares, sin pruebas técnicas, evaluación, transferencias y esperas. Registrar tiempo y memoria reales.

Un resultado científico desfavorable no autoriza detener las parejas restantes o sustituir semillas. Una ejecución incompleta se recupera con **su mismo comando** y `--reanudar`; no volver a lanzar todos los bloques sobre salidas existentes. La recuperación exige la misma pareja, variante, datos, código y entorno. Para una parada ordenada puede crearse `STOP` dentro de la carpeta de ejecución; retirarlo antes de continuar.

Una ejecución completada no se reentrena. Si solo falló la exportación final, repetir su comando con `--exportar`, sin `--reanudar`; se reconstruyen las salidas sin modificar los pesos. Conservar registros anteriores y usar otro nombre para el nuevo log. Los fallos de memoria, valores no finitos o identidad requieren detenerse y reportar.

## 3. Evaluación y síntesis completa

Con las seis continuaciones terminadas, ejecutar en el mismo dispositivo de evaluación para las tres parejas. Se recalcula la referencia inicial y se conservan los resultados de entrada, modelo inicial, C0 y C1.

```bash
for PAR in R1 R2 R3; do
  E="$SALIDAS/$PAR/evaluacion"
  python objetivo-2/herramientas/evaluar_ajuste_cgan.py \
    "${COMUN[@]}" --pareja "$PAR" --etapa piloto --dispositivo cuda \
    --control "$SALIDAS/$PAR/piloto/C0" --regional "$SALIDAS/$PAR/piloto/C1" \
    --salida "$E" --figuras 2>&1 | tee "$SALIDAS/$PAR/evaluacion.log"
  python objetivo-2/herramientas/analizar_compromiso_cgan.py \
    --datos "$DATA" --mascaras "$MASCARAS" \
    --comparacion "$E/comparacion-cgan.json" --anomalias "$E/anomalias-cgan.json" \
    --predicciones-iniciales "$E/predicciones-cgan-inicial.npy" \
    --salida "$SALIDAS/$PAR/compromiso" 2>&1 | tee "$SALIDAS/$PAR/compromiso.log"
done
python objetivo-2/herramientas/resumir_repeticion_cgan.py \
  --raiz "$SALIDAS" --etapa piloto --salida "$SALIDAS/sintesis-repeticion.json"
```

Las carpetas de evaluación/compromiso y el archivo de síntesis deben ser nuevos. El informe de evaluación registra las rutas absolutas de las ejecuciones; conservarlas hasta completar la síntesis. Si se trasladan, repetir la evaluación hacia una salida nueva y conservar el informe anterior. Para usar CPU en evaluación, cambiar las tres invocaciones a `--dispositivo cpu`; no mezclar dispositivos entre parejas.

La síntesis verifica las tres identidades, checkpoints, fuentes y referencias; calcula C1−C0 por pareja, mediana y rango para Q, cielo, borde, contraste, SSIM y PSNR. Recalcula los ocho controles y conserva todas las semillas. Revisar también las 18 vistas y 24 combinaciones de vista/anomalía de cada pareja: un promedio favorable no elimina deterioros localizados.

Incluso con tres comparaciones agregadas favorables, `physical_acceptance` permanece falso. Son continuaciones condicionadas al mismo checkpoint, no tres entrenamientos desde cero ni una demostración de generalización.

## Entrega y cierre de esta etapa

Publicar en la rama estudiantil un resumen con commit, entorno, comandos, tiempos, memoria, incidencias, resultado de cada pareja y síntesis. Incluir registros `identity.json`, `history.json`, `summary.json`, `exports.json`, `indices-val.json`, `last-session.json`, las tres aceptaciones, evaluaciones, tablas y figuras.

Guardar en Drive los **18 checkpoints** (12 técnicos y 6 de piloto), sus predicciones, las tres predicciones iniciales de evaluación y la caché recuperable. Registrar enlaces accesibles, tamaños y SHA-256. Los binarios grandes no se versionan en Git. La revisión posterior decidirá el alcance científico; no ampliar automáticamente a otras fracciones ni abrir reservas.

## Evidencia y reproducción local

La [verificación local](evidencias/integracion-repeticion-cgan-v1.json) registra 50 controles: 29 de contratos, síntesis y gradientes; 11 matemáticos y 10 de artefactos reales. Las doce ejecuciones CPU terminaron con recuperación exacta en las tres parejas. Se comprobó también la ruta de las tres evaluaciones técnicas y su síntesis, sin decisión de calidad.

Contratos y gradientes, desde la raíz:

```bash
python -m unittest discover -s objetivo-2/herramientas -p 'test_repeticion_cgan.py'
python -m unittest discover -s objetivo-2/herramientas -p 'test_gradientes_critico.py'
python -m unittest discover -s objetivo-2/herramientas -p 'test_aislar_gradientes_cgan.py'
```

Para reproducir las ejecuciones técnicas en CPU, usar una salida nueva, añadir `--cpu-test` a los comandos del ejecutor del bloque 1 y omitir `--exigir-gpu` al auditar. La aceptación indicará GPU falso. No ejecutar el bloque 2 con esas salidas. Los [controles de artefactos](herramientas/test_artefactos_repeticion_cgan.py) reciben `--raiz`, `--datos`, `--mascaras`, `--pesos` y `--salida`; usan por defecto la subcarpeta `tecnica` de cada pareja. Verifican únicamente artefactos CPU y recuperan una exportación sin reentrenar. Los once controles matemáticos se reproducen con `test_ajuste_cgan.py --fase matematica` y las rutas descritas en la [guía anterior](INSTRUCCIONES_CONTINUACION_CGAN_F05.md#reproducción-de-los-controles-locales).

Se verificaron las interfaces Python y los comandos equivalentes en Windows/CPU. Los bloques Bash/CUDA se entregan para su ejecución en el equipo GPU; no se presentan como ejecutados localmente. La actualización prepara esa comprobación y las seis continuaciones, no las acredita como realizadas.


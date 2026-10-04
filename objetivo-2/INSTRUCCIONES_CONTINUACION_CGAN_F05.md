# Ejecución de la continuación cGAN C0/C1 al 5 %

**Actualización 2026-10-03 — CG-04:** ante el fallo de recuperación GPU reportado en `b0ad0b1`, no ejecutar las continuaciones de cinco épocas. Seguir primero el [diagnóstico dirigido](DIAGNOSTICO_RECUPERACION_CGAN.md). Se conserva el criterio exacto de aceptación; el diagnóstico no emite una autorización GPU.

Fecha: 2026-10-03, Colombia. **Estado: implementación y recuperación exacta verificadas en CPU; comprobación CUDA y ensayo de cinco épocas pendientes.**

La [propuesta de diseño](PROPUESTA_CONTINUACION_CGAN_F05.md) queda implementada sin cambios en sus parámetros científicos. La comparación pregunta si el término regional aporta algo a una cGAN que también continúa entrenándose. No se presupone mejora ni se declara cumplido el OE2.

## Qué quedó verificado

La [evidencia local](evidencias/integracion-cgan-ajuste-v1.json) registra:

- Diecinueve controles satisfactorios: pérdida/gradiente C0 idénticos al original, gradiente regional C1, GP del promedio de parches, separación de actualizaciones, proporción cinco pasos D/uno G, estados aleatorios y rechazo de cambios incompatibles.
- Cuatro ejecuciones de las redes completas: C0 y C1, cada una continua e interrumpida/recuperada. Coinciden exactamente generador, crítico, ambos optimizadores, RNG de Torch CPU/CUDA según dispositivo, NumPy y Python, registros numéricos y predicciones.
- Dieciséis actualizaciones de G y ochenta de D en la batería definitiva. Una comprobación preliminar adicional realizó dos de G y diez de D; no sustituye la batería.
- Protección frente a corrupción de crítico o contador del optimizador, escrituras simultáneas, cambio de rama, reanudación de una ejecución terminada y uso de aceptación U-Net como si fuera cGAN.
- Exportación recuperable sin modificar el checkpoint ni realizar pasos de optimización.
- Evaluación técnica de ocho pares, seis registros de anomalía y tres figuras. Se inspeccionó geo-val-03. La ruta de evaluación completa también se comprobó usando predicciones del piloto anterior como fixtures: no son nuevos resultados cGAN.

La [comparación técnica](evidencias/comparacion-tecnica-cgan-v1.json) conserva todos los valores, incluso los desfavorables. Tras cuatro pasos de G por variante, SSIM es 0,82222 en C0 y 0,82207 en C1, frente a 0,82467 inicial sobre esas ocho muestras. Esta selección pequeña verifica funcionamiento, no calidad ni convergencia. La clasificación automática es exclusivamente comprobación técnica.

Entorno CPU utilizado: Python 3.12.14, PyTorch 2.6.0+cpu, NumPy 2.3.5 y dos hilos. Se reutilizan las dependencias del ajuste U-Net, incluidas SciPy, scikit-image y filelock; Matplotlib se utiliza para figuras. Para GPU se requiere una compilación PyTorch 2.6 compatible con CUDA y el equipo. Registrar pip freeze y nvidia-smi de la ejecución, mantener el entorno durante todo el ensayo y no cambiar parámetros para superar un error.

Se utilizó la copia temporal aislada ante los errores de dispositivo ya observados en D:. Las fuentes originales de crítico y pérdidas se restauraron desde sus bytes Git y se comprobaron antes de la batería definitiva; no se modificaron el motor histórico ni las entregas de estudiantes.

## Preparación

Actualizar la rama de trabajo con main, conservar el commit exacto y ejecutar desde la raíz del repositorio. Los archivos efectivos son [C0.json](configuraciones/ajuste-cgan-v1/C0.json) y [C1.json](configuraciones/ajuste-cgan-v1/C1.json). Solo difieren en identificador, nombre de variante y peso regional.

Los pesos iniciales son los de **cGAN**, incluidos generador y crítico, en época 5. No usar los pesos U-Net. La [revisión de pesos del piloto](REVISION_PESOS_PILOTO_F05.md) identifica la entrega. SHA-256 requerido:

```text
e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0
```

Se conserva la distribución corregida y la normalización v1; no se generan nuevos adelgazamientos ni se abren test/generalization. Preparar rutas absolutas reales:

```bash
set -e
export CUDA_VISIBLE_DEVICES=0
DATA="/ruta/distribucion-verificada"
PESOS="/ruta/cgan-best.pt"
MASCARAS="/ruta/trabajo/mascaras-ajuste-v1"
SALIDAS="/ruta/trabajo/cgan-ajuste-v1"
```

Una GPU basta para ejecutar las variantes secuencialmente. El ejecutor no es distribuido. No se necesita un pod de ocho GPUs; el presupuesto real se estimará con la prueba técnica cGAN, no extrapolando el tiempo de U-Net.

Puede reutilizarse una caché de máscaras íntegra del ajuste anterior, conservando manifiesto y quince NPZ. Si no está disponible, elegir un directorio nuevo y ejecutar una vez:

```bash
python objetivo-2/herramientas/datos_ajuste.py --datos "$DATA" --salida "$MASCARAS"
```

No regenerar ni intercambiar esa caché durante el ensayo: la identidad del archivo comprimido también se comprueba. Las cuatro pruebas y las continuaciones deben utilizar la misma caché.

## Etapa técnica obligatoria en GPU

Ocho pares train y ocho val, lote cuatro, dos épocas. Por variante se requiere una ejecución continua y otra que se interrumpe tras la primera época y recupera la segunda:

```bash
for RAMA in C0 C1; do
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-continua"
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --parar-tras 1
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --reanudar
done

python objetivo-2/herramientas/revisar_ajuste_cgan.py --C0-continua "$SALIDAS/tecnica/C0-continua" --C0-recuperada "$SALIDAS/tecnica/C0-recuperada" --C1-continua "$SALIDAS/tecnica/C1-continua" --C1-recuperada "$SALIDAS/tecnica/C1-recuperada" --exigir-gpu --salida "$SALIDAS/aceptacion-gpu-cgan.json"
```

La aceptación requiere salida sin error, gpu_accepted y exact_recovery verdaderos. No exige que mejoren las métricas de estas ocho muestras. La evidencia CPU y la aceptación del ajuste U-Net se rechazan como autorización de este piloto.

Conservar las cuatro carpetas técnicas: el lanzamiento del piloto vuelve a cargar y auditar sus checkpoints. Si se mueven, regenerar el archivo de aceptación con las rutas vigentes. Registrar tiempo y memoria; si exceden los recursos disponibles, detenerse y reportarlo.

## Dos continuaciones de cinco épocas

Tras aceptación GPU satisfactoria y disponibilidad de recursos, completar ambas variantes desde el checkpoint cGAN original, con optimizadores nuevos. No se utilizan los pesos de las pruebas técnicas.

```bash
for RAMA in C0 C1; do
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa piloto --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/piloto/$RAMA" --aceptacion-gpu "$SALIDAS/aceptacion-gpu-cgan.json"
done
```

El presupuesto es 1.800 actualizaciones de G y 9.000 de D por variante: 3.600 y 18.000 entre ambas. Se usan 1.440 pares train y 360 val. Se selecciona la quinta época adicional sin parada temprana ni elección retrospectiva por SSIM.

last.pt es el checkpoint final únicamente cuando summary.json declara completed y epoch igual a cinco. Incluye G, D, ambos optimizadores y todos los estados aleatorios utilizados. Una ejecución incompleta se recupera repitiendo su comando con --reanudar. No se cambian rama, semillas, datos, código o entorno durante la recuperación.

Para parar ordenadamente, crear STOP en la carpeta de ejecución; se detiene al terminar una época completa. Retirar ese archivo antes de reanudar. Si falla una exportación después de completar la quinta época, repetir el comando con --exportar y sin --reanudar; se reconstruyen los archivos derivados sin entrenar.

No desactivar determinismo, reducir el lote de una sola variante, cambiar GP o corregir un peso regional para conseguir aprobación. Un fallo de memoria, valores no finitos o identidad requiere conservar el registro y detener esa ejecución.

## Evaluación y entrega

Con ambas variantes completas:

```bash
python objetivo-2/herramientas/evaluar_ajuste_cgan.py --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --control "$SALIDAS/piloto/C0" --regional "$SALIDAS/piloto/C1" --etapa piloto --dispositivo cuda --salida "$SALIDAS/evaluacion-piloto" --figuras
```

La carpeta de evaluación debe ser nueva. --dispositivo cpu permite evaluar sin GPU, pero no habilita entrenamiento de cinco épocas en CPU. Se recalcula la referencia cGAN inicial y se conservan sus predicciones. El generador recibe únicamente la imagen de baja estadística normalizada.

La entrega debe incluir:

- Commit, comandos, versiones, hardware, tiempos, memoria, incidencias y manifiesto de máscaras.
- Aceptación GPU y los registros identity.json, history.json, summary.json, last-session.json, exports.json e indices-val.json de las seis ejecuciones.
- comparacion-cgan.json, anomalias-cgan.json y las tres figuras que abarcan las 18 vistas. La tabla por anomalía muestra soporte, referencia, sesgo firmado, magnitud del sesgo, error absoluto espacial y deterioros frente al control y al modelo inicial.
- En Drive: seis last.pt, seis arreglos predicciones-val.npy, las predicciones de la cGAN inicial de la evaluación y la caché de máscaras o su copia recuperable. Publicar enlaces, tamaños y SHA-256; no versionar esos binarios en Git.

La regla de decisión conserva Q, geometrías, cielo/borde, contraste, SSIM y PSNR. Los indicadores por anomalía no cambian retrospectivamente esa regla: impiden interpretar un promedio favorable como aceptación física automática. Se entrega también un resultado desfavorable. No se amplía a otras fracciones, semillas o particiones sin revisar este ensayo.

## Reproducción de los controles locales

El archivo test_ajuste_cgan.py recibe --datos, --mascaras, --pesos, --ejecuciones, --predicciones-previas y --salida. --fase matematica ejecuta once controles; --fase artefactos ejecuta ocho sobre las cuatro carpetas técnicas; --fase todo reúne ambos. Las predicciones previas son fixtures U-Net/cGAN del piloto anterior identificadas por huella, no resultados nuevos.

Para repetir únicamente la etapa técnica en CPU, añadir --cpu-test a sus seis comandos de ejecución y omitir --exigir-gpu al revisor. El resultado declara gpu_accepted falso. Esa prueba no sustituye CUDA ni acredita la calidad científica.

CG-01 queda verificado; CG-02 queda parcial, con CPU verificado y GPU pendiente; CG-03 queda preparado para ejecución condicionada, sin resultados del ensayo completo. El OE2 permanece abierto.

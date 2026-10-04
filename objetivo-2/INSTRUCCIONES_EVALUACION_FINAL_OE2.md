# Ejecutar ahora: evaluación final OE2 al 5 %

**Prioridad vigente:** ejecutar inferencia con pesos existentes y evaluar prueba/generalización según el [protocolo EF-01](PROTOCOLO_EVALUACION_FINAL_OE2.md). No repetir E1 ni su diagnóstico como requisito. La redacción puede avanzar en paralelo. No hay nuevo entrenamiento, nuevas épocas ni nuevas simulaciones.

## Preparar una sola vez

1. Actualizar `main` conservando cambios y ramas anteriores. Crear una rama de entrega, por ejemplo `oe2/evaluacion-final-f05`. Registrar `git rev-parse HEAD` y la fecha antes de inferir. Conservar finales de línea de los archivos de código; las huellas fijan exactamente las fuentes del repositorio.
2. Usar el entorno PyTorch que ya ejecutó E1, con NumPy, SciPy, scikit-image y filelock. No es necesario repetir la aceptación de recuperación del entrenamiento: aquí no se entrena. Registrar GPU, driver y versiones.
3. Tener disponibles los ocho archivos de prueba/generalización de `dataset-v2/shards`, desde la [distribución OE1](https://drive.google.com/drive/folders/10gRmkWqmCqN3qOf2gfOWCDG4bcC7zhaT), y los ocho pesos finales. El ejecutor comprobará las huellas. Reutilizar los archivos conservados.
4. Copiar [pesos-evaluacion-final-ejemplo.json](configuraciones/pesos-evaluacion-final-ejemplo.json) fuera de Git y completar sus ocho rutas locales. No cambiar los nombres de los modelos ni las huellas del protocolo. Los pesos iniciales están en la [carpeta del piloto](https://drive.google.com/drive/folders/18pOGXzN2lEhKfxJlpcC4GuTujkNyA-ix); los seis de E1, en el [índice verificado](INDICE_ARTEFACTOS_E1.md).
5. Registrar en `PROCEDENCIA_RESERVAS.md` si estos datos se usaron antes para entrenamiento o decisiones del modelo, además de las inspecciones del catálogo en OE1. Si hubo uso previo o incertidumbre, declararlo; no presentar esa evaluación como independencia confirmatoria.

Desde la raíz del repositorio, completar estas tres rutas y usar una salida nueva:

```bash
set -euo pipefail
DATA=/ruta/insumos
WEIGHTS=/ruta/pesos-evaluacion.json
OUT=/ruta/nueva/evaluacion-final-f05
SCRIPT=objetivo-2/herramientas/evaluacion_final_oe2.py
python "$SCRIPT" preflight --data "$DATA" --weights "$WEIGHTS" --output "$OUT"
```

`DATA` contiene `dataset-v2/shards/geo-test-01.npz`, su `.meta.json`, y análogos para test-02, test-03 y gen-01. `WEIGHTS` es el JSON de rutas, no una carpeta. Preflight verifica ocho datos/metadatos y ocho checkpoints, sin calcular métricas.

## Con una GPU: ejecutar el bloque completo

```bash
for MODEL in unet_original cgan_original B1_C0 B1_C1 B2_C0 B2_C1 B3_C0 B3_C1; do
  python "$SCRIPT" infer --data "$DATA" --weights "$WEIGHTS" \
    --output "$OUT" --model "$MODEL" --device cuda
done
python "$SCRIPT" evaluate --data "$DATA" --weights "$WEIGHTS" \
  --output "$OUT" --report "$OUT/informe-v1"
```

La evaluación posterior se calcula en CPU; no necesita otra sesión de entrenamiento. Se permite completar todos los modelos y la evaluación sin esperar otra aprobación. Cada modelo genera 480 predicciones: 360 de test y 120 de generalización. Total de redes: 3.840; más la comparación con 480 entradas. Se registran tiempos reales, sin prometer una duración fija.

## Si ya se dispone de tres GPU

Repartir modelos completos, manteniendo las mismas rutas DATA/WEIGHTS/OUT en las tres terminales:

- GPU 0: `unet_original cgan_original B1_C0`.
- GPU 1: `B1_C1 B2_C0 B2_C1`.
- GPU 2: `B3_C0 B3_C1`.

En cada terminal establecer `export CUDA_VISIBLE_DEVICES=N` y usar el mismo bucle con su lista y `--device cuda`. No iniciar dos procesos para el mismo modelo. Una vez terminados los tres grupos, ejecutar **una sola vez** `evaluate`; exige el conjunto completo. No es necesario contratar tres GPU: una permite la misma evaluación.

## Interrupciones y entrega

- Repetir el comando de inferencia conserva y verifica geometrías terminadas; recalcula únicamente una geometría que quedó sin recibo completo. Deben conservarse protocolo, pesos, equipo/entorno y rutas de salida. Un error de identidad, corrupción, memoria o valores inválidos se reporta con el log; no se resuelve cambiando pesos o tolerancias.
- Si falla únicamente la evaluación, conservar predicciones y usar una ruta nueva de informe al repetirla. No volver a entrenar ni generar predicciones para cambiar un resultado desfavorable.
- Guardar en Drive las 32 matrices NPY finales (ocho modelos × cuatro geometrías), aproximadamente 1.006.637.056 bytes en total, y sus recibos/identidades. Confirmar los tamaños con el inventario generado; no reemplazar la carpeta E1. Compartir el enlace accesible.
- En la rama nueva: `PROCEDENCIA_RESERVAS.md`, commit, entorno, GPU, comandos y tiempos; `preflight.json`, identidades, recibos y `completed.json` de los ocho modelos; `evaluacion-final.json`, ambos CSV e `inventario-predicciones.json`; resumen de incidencias y enlace a Drive.
- No elegir una semilla, una geometría o una métrica para ocultar los resultados restantes. Informar el commit de entrega al terminar; la auditoría posterior utilizará estas predicciones y no pedirá repetir el entrenamiento.

La tarea termina con la evaluación completa y accesible, aunque haya deterioros. Después se redactará la conclusión del objetivo con su alcance real. No se abren otras fracciones ni se modifican criterios después de ver estas reservas.

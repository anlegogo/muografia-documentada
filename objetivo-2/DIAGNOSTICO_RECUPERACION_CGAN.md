# Diagnóstico de la recuperación cGAN en CUDA

Fecha de preparación: 2026-10-03, America/Bogota.

## Propósito y estado

**CG-04 — Recuperación CUDA: pendiente de diagnóstico GPU.** Se prepara una prueba corta para localizar la primera diferencia entre continuar una ejecución y cargar su estado en otro proceso. No se modifica el ejecutor, la configuración C0/C1 ni el criterio de aceptación. Este diagnóstico no autoriza las continuaciones de cinco épocas y siempre declara `gpu_accepted: false`.

La entrega estudiantil revisada es `oe2/continuacion-cgan-f05`, commit `b0ad0b1cf6396e55bebe88169ee09ee0ff4401de`. Se verificaron las 97 huellas de su manifiesto y las 13 huellas del código registradas. En los historiales, C0 y C1 coinciden en la época 1 y difieren en la 2; la repetición continua de C0 coincide en pesos declarados y métricas, excluidos tiempos. Los estados binarios no pudieron auditarse: la entrega no enlaza los nuevos checkpoints y predicciones; el listado Drive contiene entradas y pesos iniciales.

La explicación por redondeo dependiente del historial permanece como hipótesis. El diagnóstico estudiantil recorre variantes en un orden fijo dentro del mismo proceso y no proporciona un control continuo adicional en cada posición ni huellas intermedias para todas las variantes. Desactivar una opción de memoria tampoco descarta todas las diferencias de ejecución. La tolerancia propuesta no se adopta: una tolerancia relativa de 1e-4 en SSIM cercano a 0,82 permite aproximadamente 8,2e-5 de diferencia absoluta, comparable con efectos de orden 1e-4; no cuatro órdenes menor. No se extrapola el comportamiento de dos épocas técnicas a una continuación completa.

## Qué se ejecuta

La herramienta [diagnosticar_recuperacion_cgan.py](herramientas/diagnosticar_recuperacion_cgan.py) lanza cuatro procesos independientes, en orden, por variante:

| Proceso | Procedimiento |
|---|---|
| continua | Época 1, guarda una copia, sigue a época 2 sin cargar. |
| repetida | Repite desde el origen exactamente el procedimiento continuo, en otro proceso. |
| recarga | Época 1, guarda y carga redes, Adam y RNG en los mismos objetos, luego época 2. |
| reanudada | Proceso nuevo: construye las redes y optimizadores, carga el checkpoint de época 1 de continua y ejecuta época 2. |

Cada época usa exclusivamente los ocho ejemplos train y ocho val de la prueba técnica existente. Se conservan semilla, orden, cinco pasos D por G, pérdidas y pesos iniciales. Por variante se ejecutan siete épocas técnicas en total (14 actualizaciones G, 70 D); en C0+C1, 28 G y 140 D. No se entrena sobre test ni se evalúa generalización.

Se registran:
- Huellas por tensor de redes, momentos y contadores Adam, RNG CPU/CUDA/NumPy/Python al guardar y antes de la época 2.
- Comparación inmediata del archivo cargado con el estado vivo. Cambios de ubicación CPU/CUDA se informan por separado; los valores deben conservarse.
- En los dos lotes de época 2: entradas, salidas de G y D, pérdidas, gradientes antes del paso, parámetros y Adam después del paso, y RNG al inicio y fin.
- Primer evento y hojas diferentes, métricas y diferencias absolutas de predicciones.

La instrumentación añade copias a CPU y sincronizaciones. Si el fallo desaparece con ella, el resultado será inconcluso sobre la ejecución original; no se declarará resuelto. Las huellas localizan una operación observada, no un kernel ni una causa definitiva.

## Instrucciones para los estudiantes

1. Conservar toda la evidencia anterior y actualizar la rama incorporando `main`. Registrar `git rev-parse HEAD` y `git status --short`; no cambiar las herramientas durante la prueba.
2. Usar una sola GPU visible y el mismo entorno documentado del intento 1 (PyTorch 2.6.0+cu118, resto de dependencias según la guía de continuación). Conservar los datos, máscaras y checkpoint cGAN inicial de SHA-256 `e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0`.
3. Ejecutar lo siguiente desde la raíz del repositorio, reemplazando las cuatro rutas. `SALIDA` debe ser una carpeta nueva; cada variante también exige una salida inexistente.

```bash
set -euo pipefail
export CUDA_VISIBLE_DEVICES=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8
DATOS=/ruta/datos
MASCARAS=/ruta/mascaras
PESOS=/ruta/cgan-best.pt
SALIDA=/ruta/nueva/diagnostico-cgan

mkdir "$SALIDA"
git rev-parse HEAD > "$SALIDA/commit.txt"
git status --short > "$SALIDA/git-status.txt"
nvidia-smi > "$SALIDA/nvidia-smi.txt"
python -m pip freeze > "$SALIDA/pip-freeze.txt"

for RAMA in C0 C1; do
  python objetivo-2/herramientas/diagnosticar_recuperacion_cgan.py \
    --rama "$RAMA" --datos "$DATOS" --mascaras "$MASCARAS" \
    --pesos "$PESOS" --salida "$SALIDA/$RAMA" \
    2>&1 | tee "$SALIDA/$RAMA-consola.log"
done
```

No usar `--cpu-test` en la L40S. No invocar manualmente `--modo`: es la interfaz interna de los procesos hijos. No lanzar las continuaciones de cinco épocas después de este diagnóstico. Si un proceso falla, conservar la carpeta y el log; no borrar ni reutilizar la salida. Las carpetas contendrán varios checkpoints grandes; reservar varios GB libres. No se promete un tiempo GPU: las copias de diagnóstico agregan trabajo respecto a la prueba anterior.

## Entrega

En la rama de los estudiantes: informe breve, commit y entorno, comandos, todos los JSON/JSONL y logs del diagnóstico, incluyendo `restore-check.json`, `boundary-*.json`, `trace.jsonl`, `diagnostico.json` y `archivos.json`.

En Drive: carpetas completas C0 y C1, con todos los `epoch1.pt`, `epoch2.pt` y `predicciones-val.npy`. Incorporar enlaces, tamaños y SHA-256 al repositorio; `archivos.json` ya calcula el inventario de cada variante. Compartir también los checkpoints y predicciones de la prueba original si se conservaron. No sustituir archivos anteriores bajo el mismo nombre.

## Lectura y criterio de cierre

- Si cambia el estado inmediatamente al cargar, investigar esa restauración antes de interpretar el entrenamiento.
- Si continua y repetida difieren, no se ha reproducido la estabilidad del control con la instrumentación.
- Si el estado inicial coincide y la primera diferencia aparece después, el evento señalado delimita la siguiente comprobación.
- Si todas las variantes coinciden, el diagnóstico instrumentado es exacto, pero no prueba que la incidencia original haya desaparecido.
- CG-04 se cerrará únicamente con evidencia GPU auditada y una corrección comprobada o una decisión metodológica explícita, motivada y documentada. No se sustituye la aceptación original por este informe.

La validación CPU y las pruebas de detección de alteraciones se registran en [la evidencia local](evidencias/diagnostico-recuperacion-cgan-cpu.json). Su alcance es funcional: no reproduce la incidencia L40S.

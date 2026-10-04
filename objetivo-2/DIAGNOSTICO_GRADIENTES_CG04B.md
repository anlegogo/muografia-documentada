# CG-04b: separación de los gradientes del crítico

Preparación: 2026-10-03, America/Bogota. Seguimiento del pendiente **CG-04**, sin cambiar su identificador ni el criterio de aceptación.

## Propósito

La [auditoría de CG-04](REVISION_BINARIOS_CG04.md) confirmó que el estado se recupera correctamente y que la primera diferencia observada aparece en los gradientes del crítico al reanudar en un proceso nuevo. Esta prueba busca determinar si la diferencia se encuentra en una contribución concreta al gradiente o si requiere investigar su combinación. No se ha identificado todavía una causa CUDA.

La pérdida del crítico es

$$
L_D=L_W+L_P,\qquad
L_W=\frac1B\sum_{i=1}^{B}\left[D_\theta(x_i,\widehat y_i)-D_\theta(x_i,y_i)\right],
$$
$$
L_P=\lambda_{GP}\frac1B\sum_{i=1}^{B}
\left(\left\|\nabla_{\widetilde y_i}D_\theta(x_i,\widetilde y_i)\right\|_2-1\right)^2,
\quad \widetilde y_i=\alpha_i y_i+(1-\alpha_i)\widehat y_i.
$$

Aquí, $D_\theta$ representa la puntuación media del mapa de parches, $x_i$ es la condición, $y_i$ la referencia normalizada y $\widehat y_i=G(x_i)$ la imagen generada sin gradiente para el paso del crítico. Se mantiene $\lambda_{GP}=10$. Se medirán

$$
g_W=\nabla_\theta L_W,\qquad
g_P=\nabla_\theta L_P,\qquad
g_T=\nabla_\theta(L_W+L_P).
$$

En aritmética real, $g_T=g_W+g_P$. En punto flotante, distintas rutas de acumulación pueden producir diferencias; por eso la suma se mide y se informa, sin imponer una tolerancia de aceptación nueva.

## Diseño y controles

[aislar_gradientes_cgan.py](herramientas/aislar_gradientes_cgan.py) ejecuta diez procesos independientes por variante, C0 y C1. Cada proceso realiza **una única medición de gradientes sobre el primer lote de la época 2**.

| Medición | Qué se deriva |
|---|---|
| original | La pérdida total con la función original del ejecutor. |
| repetida | Repetición independiente de original. |
| total | La suma explícita de las dos contribuciones, con las mismas operaciones de forward. |
| wasserstein | Solo $L_W$, aunque también se construye la penalización para conservar el forward y el consumo aleatorio. |
| penalizacion | Solo $L_P$, ya multiplicada por 10. |

Cada medición se hace en dos condiciones:
- **continua:** desde los pesos iniciales, se ejecuta la época 1 técnica con ocho pares y su validación; se continúa con la medición.
- **nueva:** en otro proceso se restaura el checkpoint de época 1 producido por continua/original; se realiza la medición.

No se encadenan backward de componentes en un mismo proceso. Cada caso tiene sus propias redes, estado y grafo. No se aplica ningún paso Adam al lote medido: se detiene tras obtener sus gradientes. La época 1 sí usa los pasos originales necesarios para recrear el historial continuo.

Por variante hay cinco épocas 1 técnicas: diez actualizaciones G y cincuenta D; para C0+C1, veinte G y cien D de preparación, más veinte mediciones backward sin actualización. Se mantiene exclusivamente el subconjunto train/val técnico; no se abre test ni se lanzan las continuaciones de cinco épocas.

Antes de interpretar las diferencias se exige igualdad de identidad, frontera, lote, entrada/fake, estados aleatorios antes/después del forward, los tres forwards del crítico y el valor de la pérdida total. Se verifica que los parámetros y los estados de Adam no cambien durante la medición. El proceso falla con registros si estos controles no se cumplen.

Se guardan los gradientes completos por parámetro. Un parámetro sin dependencia de una contribución se representa con cero para sumarlo, y su nombre se registra en `unused_parameters`; no se confunde con un gradiente observado distinto de cero.

## Ejecución en la L40S

Actualizar la rama incorporando `main`, conservar el mismo entorno del diagnóstico anterior y ejecutar desde la raíz. Usar una GPU visible. Reemplazar las cuatro rutas; `SALIDA` debe ser una carpeta nueva.

```bash
set -euo pipefail
export CUDA_VISIBLE_DEVICES=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8
DATOS=/ruta/datos
MASCARAS=/ruta/mascaras
PESOS=/ruta/cgan-best.pt
SALIDA=/ruta/nueva/cg04b

mkdir "$SALIDA"
git rev-parse HEAD > "$SALIDA/commit.txt"
git status --short > "$SALIDA/git-status.txt"
nvidia-smi > "$SALIDA/nvidia-smi.txt"
python -m pip freeze > "$SALIDA/pip-freeze.txt"

for RAMA in C0 C1; do
  python objetivo-2/herramientas/aislar_gradientes_cgan.py \
    --rama "$RAMA" --datos "$DATOS" --mascaras "$MASCARAS" \
    --pesos "$PESOS" --salida "$SALIDA/$RAMA" \
    2>&1 | tee "$SALIDA/$RAMA-consola.log"
done
```

El checkpoint inicial sigue siendo el cGAN original de época 5, SHA-256 `e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0`. El programa crea su propio checkpoint de época 1; no se sustituye manualmente por los archivos anteriores.

No usar `--cpu-test` en GPU. `--temperatura`, `--componente` y `--checkpoint` son argumentos internos: no hace falta invocarlos. Si un proceso falla, conservar toda la carpeta y reportar el log; no reutilizar ni sobrescribir la salida. La ejecución original y los criterios del piloto permanecen intactos.

## Entrega y lectura

Subir al repositorio todos los JSON y logs, especialmente `comparacion.json`, `resultado.json`, los comandos, códigos de salida y `archivos.json`. Compartir por Drive los veinte `gradientes.pt` y los dos `epoch1.pt`, con enlaces e inventarios. Son archivos nuevos; no reemplazar los del diagnóstico CG-04.

Revisar en este orden:
1. `controls`: original/repetida debe ser estable. Original/total comprueba si la separación explícita conserva el gradiente total. Si falla, no atribuir automáticamente una causa a un componente.
2. `continuous_vs_new`: muestra qué mediciones difieren al reiniciar el proceso, con diferencias absolutas y normas por parámetro.
3. `reconstruction`: compara el total explícito con la suma de los componentes, calculada offline en CPU en float32 y float64. La suma offline no reproduce el orden interno de acumulación CUDA; sus diferencias son descriptivas, no una prueba automática de fallo ni una aceptación.
4. Si todos los controles son exactos y la discrepancia aparece en una sola contribución, esa ruta queda delimitada para la siguiente investigación. Si la instrumentación hace desaparecer la discrepancia original, el resultado es inconcluso sobre su causa.

La herramienta siempre declara `gpu_accepted: false`. No autoriza entrenamientos largos, no modifica pesos del lote observado y no cambia tolerancias. La [validación CPU](evidencias/cg04b-validacion-cpu.json) verifica el funcionamiento de la herramienta; la incidencia L40S continúa pendiente de esta ejecución.

## Resultado de la validación CPU

Se completaron ocho controles matemáticos/funcionales y veinte procesos reales, diez por variante. Original/repetida y original/total coincidieron exactamente; todas las mediciones continua/nueva también coincidieron. El gradiente original reproduce la primera medición D del diagnóstico CG-04 CPU. El máximo residuo absoluto de la suma offline fue 2,384185791015625e-7 en C0 y C1, tanto en float32 como en float64; no se adopta como tolerancia GPU. La validación final se realizó el 2026-10-04 a las 04:59 UTC (2026-10-03 en Colombia).

## Reproducción de los controles CPU

En el entorno de dependencias del proyecto, ejecutar `python objetivo-2/herramientas/test_aislar_gradientes_cgan.py`. La matriz completa se reproduce con los mismos comandos anteriores, añadiendo `--cpu-test` y usando salidas nuevas. Este indicador solo cambia el dispositivo del diagnóstico; nunca permite continuar el piloto. La evidencia enlazada conserva la versión de Python/PyTorch, las huellas del código y los resultados por variante.

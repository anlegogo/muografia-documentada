# CG-04c: corrección del gradiente y validación GPU

**Actualización posterior a la entrega — 2026-10-04:** la [verificación independiente](REVISION_BINARIOS_CG04C.md) confirma la aceptación técnica GPU y ambas continuaciones de cinco épocas. Los apartados siguientes conservan el procedimiento y el estado de su preparación como antecedente; no constituyen un encargo de repetir el ensayo. CG-04 está cerrado para el entorno recibido y la aceptación física del OE2 sigue pendiente.

Fecha: 2026-10-04, America/Bogota. **Implementación candidata; la aceptación L40S sigue pendiente.** Se busca recuperar exactamente un entrenamiento interrumpido antes de ejecutar las cinco épocas C0/C1.

## Cambio y fundamento

La [revisión CG-04b](REVISION_BINARIOS_CG04B.md) verificó componentes aislados exactos y discrepancia al derivar la pérdida conjunta. Esto motiva modificar su cálculo, sin afirmar que se haya identificado un kernel causal.

Para los parámetros del crítico, se conserva la pérdida

\[
L_D=L_W+\lambda_{GP}L_{GP},\qquad
L_W=\mathbb{E}[C(x,\hat y)]-\mathbb{E}[C(x,y)].
\]

Se calculan separadamente

\[
g_W=\nabla_{\theta_D}L_W,\quad
g_{GP}=\nabla_{\theta_D}(\lambda_{GP}L_{GP}),\quad
g_D=g_W+g_{GP}.
\]

Se usa `torch.autograd.grad` primero para W y después para GP. Luego se asigna la suma a cada `.grad` y se aplica **un solo paso Adam**. Un parámetro sin contribución GP, como el sesgo de salida, aporta cero en ese término. Se exige contribución W para todos los parámetros y se rechazan pérdidas y gradientes no finitos antes de aplicar el paso.

Se preservan forwards, muestra aleatoria de interpolación, promedio del mapa del crítico, penalización 10, semillas, configuraciones, pesos iniciales y cinco pasos D por G. La pérdida regional permanece únicamente en G de C1. No se introduce una tolerancia GPU. La igualdad matemática no implica identidad bit a bit con la trayectoria histórica: es una versión numérica nueva y exige ejecuciones nuevas.

La implementación está en [gradientes_critico.py](herramientas/gradientes_critico.py), integrada en [el ejecutor](herramientas/ejecutar_ajuste_cgan.py). La identidad registra `critic_gradient_policy=wasserstein-then-weighted-gp-v1` y las huellas de las fuentes. Los checkpoints y aceptaciones de versiones anteriores son incompatibles. Para reproducir los diagnósticos históricos CG-04/CG-04b se debe utilizar su código fijado en `a259615c69a12bb0a84859ad3a7a3922a79f6012`, en otra copia; no ejecutarlos con la continuación modificada.

## Verificación local y límites

La [evidencia CPU](evidencias/cg04c-validacion-cpu.json) registra los controles matemáticos, de integración, recuperación y artefactos. Se comprueban gradiente analítico, sesgo sin GP, conservación del RNG, sustitución de gradientes previos, un único paso Adam y rechazo de estados incompatibles/no finitos. La batería técnica utiliza las redes completas y el checkpoint cGAN verificado, con ocho pares train y ocho val.

Resultado local: **34 controles satisfactorios** (7 de la corrección, 8 de regresión del diagnóstico, 11 de integración y 8 de artefactos). Las cuatro ejecuciones de red completa recuperan exactamente; se realizaron 16 pasos G y 80 D. La corrección está verificada en CPU y pendiente en L40S.

La recuperación se compara en G, D, ambos Adam, RNG, registros numéricos y predicciones. Los tiempos de cómputo quedan fuera de esa igualdad. La evidencia local declara `gpu_accepted: false`; no acredita CUDA ni mejora científica. No se abren test/generalization.

Controles unitarios desde `objetivo-2/herramientas`:

```bash
python -m unittest test_gradientes_critico test_aislar_gradientes_cgan
```

Para repetir la batería CPU se usan los comandos técnicos siguientes añadiendo `--cpu-test` a los seis lanzamientos y omitiendo `--exigir-gpu` en el revisor. Los controles existentes de integración y artefactos se ejecutan con `test_ajuste_cgan.py` sobre esas carpetas nuevas; véanse [sus argumentos](INSTRUCCIONES_CONTINUACION_CGAN_F05.md#reproducción-de-los-controles-locales).

## Trabajo de los estudiantes en L40S

Actualizar la rama de entrega incorporando `main` y registrar el commit resultante. Mantener el entorno L40S anterior y una GPU. Elegir una carpeta nueva; conservar las anteriores. No reanudar checkpoints CG-04/CG-04b ni reutilizar sus aceptaciones.

Desde la raíz del repositorio, en Bash, sustituir las cuatro rutas:

```bash
set -euo pipefail
export CUDA_VISIBLE_DEVICES=0
DATA="/ruta/distribucion-verificada"
PESOS="/ruta/cgan-best.pt"
MASCARAS="/ruta/mascaras-ajuste-v1"
SALIDAS="/ruta/nueva/cgan-cg04c"
test ! -e "$SALIDAS"
mkdir -p "$SALIDAS"
git rev-parse HEAD > "$SALIDAS/commit.txt"
git status --short > "$SALIDAS/git-status.txt"
python -m pip freeze > "$SALIDAS/pip-freeze.txt"
nvidia-smi > "$SALIDAS/nvidia-smi.txt"

for RAMA in C0 C1; do
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-continua" 2>&1 | tee "$SALIDAS/$RAMA-continua.log"
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --parar-tras 1 2>&1 | tee "$SALIDAS/$RAMA-parada.log"
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --reanudar 2>&1 | tee "$SALIDAS/$RAMA-reanudada.log"
done

python objetivo-2/herramientas/revisar_ajuste_cgan.py --C0-continua "$SALIDAS/tecnica/C0-continua" --C0-recuperada "$SALIDAS/tecnica/C0-recuperada" --C1-continua "$SALIDAS/tecnica/C1-continua" --C1-recuperada "$SALIDAS/tecnica/C1-recuperada" --exigir-gpu --salida "$SALIDAS/aceptacion-gpu-cgan.json" 2>&1 | tee "$SALIDAS/auditoria.log"
```

Son cuatro ejecuciones técnicas mediante seis procesos: C0/C1 continuas y C0/C1 interrumpidas y recuperadas. En total se realizan 16 actualizaciones G y 80 D. No son las cinco épocas del piloto. Registrar tiempo y memoria para valorar el presupuesto; no se estima la duración GPU a partir de CPU.

**Si falla:** detenerse, conservar logs y carpetas completas y publicar la incidencia. No cambiar semillas, precisión, lote, penalización, determinismo ni tolerancias para obtener aprobación. No lanzar el piloto.

**Si termina sin error y el auditor declara `gpu_accepted: true` y `exact_recovery: true`:** con recursos disponibles pueden continuar directamente con las [dos variantes de cinco épocas](INSTRUCCIONES_CONTINUACION_CGAN_F05.md#dos-continuaciones-de-cinco-épocas), manteniendo las variables anteriores y esta misma versión/entorno. Ambas comienzan desde el checkpoint cGAN original de época 5, con optimizadores nuevos; no desde los pesos técnicos. El ejecutor vuelve a auditar la evidencia antes de entrenar. Si no hay recursos suficientes, conservar la aceptación y reportar tiempos.

Al finalizar ambas, ejecutar la [evaluación y entrega](INSTRUCCIONES_CONTINUACION_CGAN_F05.md#evaluación-y-entrega). La aceptación técnica solo verifica reproducción del entrenamiento; la calidad de imágenes y cuentas regionales se determina después.

## Entrega y estado

Publicar un informe CG-04c con commit, entorno, comandos, resultados, tiempos, memoria e incidencias. Incluir logs y JSON de las cuatro pruebas y su aceptación; guardar checkpoints y predicciones en Drive con enlaces, tamaños y SHA-256. Si se completa el piloto, entregar también ambas continuaciones y la evaluación, incluso si el resultado es desfavorable.

CG-04 permanece parcial hasta revisar la aceptación GPU; CG-03 continúa condicionado y el OE2 sigue abierto. No se amplía automáticamente a otras fracciones, semillas ni particiones.

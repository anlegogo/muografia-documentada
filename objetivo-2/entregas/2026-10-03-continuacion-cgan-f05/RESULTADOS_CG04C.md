# Resultados CG-04c: aceptación GPU y continuación cGAN C0/C1

2026-10-04 (UTC). Ejecución de la [corrección CG-04c](../../CORRECCION_GRADIENTES_CG04C.md) en GPU. Como la auditoría aceptó la recuperación exacta, se continuó con las [dos continuaciones de cinco épocas y la evaluación](../../INSTRUCCIONES_CONTINUACION_CGAN_F05.md), según indica esa guía. Herramientas, configuraciones y criterios se usaron sin modificaciones.

## 1. Condiciones

| Elemento | Valor |
|---|---|
| Código | Rama `oe2/continuacion-cgan-f05` en `02ce48a6f2986c931149f26a9a7e66e0a8495156`, merge de `main` `4fc3bd5`. Clon Git en el pod desde un bundle de la rama; `git status --short` vacío ([commit.txt](datos/cg04c/cgan-cg04c/commit.txt), [git-status.txt](datos/cg04c/cgan-cg04c/git-status.txt)) |
| Equipo | Pod RunPod con 1 × NVIDIA L40S, driver 570.124.06 ([nvidia-smi.txt](datos/cg04c/cgan-cg04c/nvidia-smi.txt)) |
| Entorno | Python 3.12.3, torch 2.6.0+cu118 (CUDA 11.8, cuDNN 9.1.0), NumPy 2.3.5, SciPy 1.18.1, scikit-image 0.26.0, Matplotlib 3.11.1, filelock 3.16.1 ([pip-freeze.txt](datos/cg04c/cgan-cg04c/pip-freeze.txt)) |
| Datos | 31 de 31 huellas, incluido el `best.pt` cGAN `e54d51f7…` ([datos.log](datos/cg04c/datos.log)). Máscaras con `datos_ajuste.py` ([manifiesto](datos/cg04c/manifiesto-mascaras.json)) |
| Comandos | Los literales de ambas guías, con `CUDA_VISIBLE_DEVICES=0` ([cg04c_pod.sh](verificacion/cg04c_pod.sh)). Registros por paso en [datos/cg04c/cgan-cg04c/](datos/cg04c/cgan-cg04c/) |

Todos los pasos terminaron sin error ([cg04c.log](datos/cg04c/cg04c.log)).

## 2. Aceptación técnica en GPU

Las seis ejecuciones técnicas terminaron sin error. Son C0 y C1, cada una con una ejecución continua y otra interrumpida tras la época 1 y reanudada; suman 16 actualizaciones de G y 80 de D. `revisar_ajuste_cgan.py --exigir-gpu` declaró `passed: true`, `gpu_accepted: true` y `exact_recovery: true` ([aceptacion-gpu-cgan.json](datos/cg04c/cgan-cg04c/aceptacion-gpu-cgan.json), [auditoria.log](datos/cg04c/cgan-cg04c/auditoria.log)).

Con la derivación separada del gradiente del crítico, la ejecución recuperada coincide exactamente con la continua en G, D, ambos Adam, RNG, registros y predicciones. Así se cierra en esta GPU la discrepancia documentada en CG-04 y CG-04b.

## 3. Continuaciones de cinco épocas

| Rama | Épocas | Tiempo por época | Cómputo total | Memoria CUDA máx. | SSIM val época 5 |
|---|---:|---:|---:|---:|---:|
| C0 (sin término regional) | 5, `completed` | 126,3–131,3 s | 640,2 s | 1,96 GB | 0,81487 |
| C1 (con término regional) | 5, `completed` | 128,7–135,3 s | 654,7 s | 1,96 GB | 0,81570 |

Cada rama hizo 1.800 actualizaciones de G y 9.000 de D, partiendo del checkpoint cGAN original con optimizadores nuevos. Se seleccionó la quinta época, sin parada temprana ([summary C0](datos/cg04c/cgan-cg04c/piloto/C0/summary.json), [summary C1](datos/cg04c/cgan-cg04c/piloto/C1/summary.json)).

## 4. Evaluación según los criterios del director

Las cifras salen de `evaluar_ajuste_cgan.py` sobre los 360 pares de validación ([comparacion-cgan.json](datos/cg04c/cgan-cg04c/evaluacion-piloto/comparacion-cgan.json)).

| Medida | Entrada | cGAN inicial (época 5) | C0 | C1 | Criterio C1 frente a C0 |
|---|---:|---:|---:|---:|:---:|
| Q (%) | 1,814 | 12,340 | 7,204 | 4,765 | Cumple |
| Q `geo-val-01` (%) | 1,198 | 3,470 | 11,118 | 6,647 | Cumple |
| Q `geo-val-02` (%) | 2,551 | 15,744 | 4,012 | 2,377 | Cumple |
| Q `geo-val-03` (%) | 1,692 | 17,806 | 6,483 | 5,272 | Cumple |
| MAE de cielo (%) | 6,802 | 12,648 | 2,830 | 2,238 | Cumple |
| MAE de borde (%) | 12,092 | 14,419 | 11,278 | 11,265 | Cumple |
| Error de contraste | 0,2464 | 0,0907 | 0,1052 | 0,0913 | Cumple |
| SSIM | 0,75181 | 0,82279 | 0,81487 | 0,81570 | Cumple |
| PSNR (dB) | 24,168 | 31,104 | 30,572 | 30,646 | Cumple |

**Decisión del evaluador: `mejora_concordante_descriptiva`.** Los ocho controles de `decision_checks` son verdaderos. Según el diseño, la clasificación es descriptiva y no acredita significación ni aceptación física (`physical_acceptance: false`).

**Indicadores que la regla no decide, pero que deben leerse junto con ella:**

- **Calidad de imagen frente al modelo inicial.** Tanto C0 como C1 tienen menor SSIM y PSNR que la cGAN inicial: 0,8157 frente a 0,8228 y 30,65 frente a 31,10 dB. La continuación cGAN mejora la conservación regional a costa de calidad de imagen respecto del punto de partida. El término regional no causa esa pérdida, porque C1 queda por encima de C0.
- **Conservación en `geo-val-01`.** C1 (6,65 %) mejora a C0 (11,12 %), pero empeora frente a la cGAN inicial (3,47 %).
- **Diagnóstico por anomalía.** De 24 combinaciones de vista y anomalía, C1 tiene mayor magnitud de sesgo que C0 en 8 y que el modelo inicial en 5 ([anomalias-cgan.json](datos/cg04c/cgan-cg04c/evaluacion-piloto/anomalias-cgan.json)). El promedio favorable no es uniforme.
- **Sesgo firmado medio por familia** (C0 → C1): cielo −2,00 % → +0,01 %; roca +1,95 % → +1,38 %; borde −2,64 % → +0,41 %; anomalías +9,17 % → +5,93 %. La entrada sin red es casi insesgada en todas las familias, entre −0,04 % y +0,84 %.

Es una sola ejecución por rama sobre tres geometrías de validación. No se estima variabilidad entre entrenamientos, ni se abrieron test o generalización. Las [figuras del evaluador](datos/cg04c/cgan-cg04c/evaluacion-piloto/) cubren las 18 vistas.

## 5. Archivos binarios

No se versionan. Huellas y tamaños de los seis `last.pt` (cuatro técnicos y dos finales), las seis predicciones de validación y las predicciones de la cGAN inicial: [binarios.sha256](datos/cg04c/binarios.sha256) y [binarios.tamanos.txt](datos/cg04c/binarios.tamanos.txt). Se descargaron del pod y se verificaron en almacenamiento local: 13 de 13. La caché de máscaras es reproducible con `datos_ajuste.py` y su manifiesto está incluido. El enlace de Drive se agregará cuando se suban.

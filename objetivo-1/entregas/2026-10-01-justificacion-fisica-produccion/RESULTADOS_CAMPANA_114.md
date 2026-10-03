# Resultados de la campaña de 114 vistas

2026-10-03 (Colombia). Campaña ejecutada según [ACUERDO_CAMPANA_114.md](ACUERDO_CAMPANA_114.md) y [PREPARACION_CAMPANA_114.md](../../PREPARACION_CAMPANA_114.md): 344 millones de primarios por vista, fijos, en las 114 vistas (19 geometrías × 6), con el [manifiesto candidato](../../evidencias/preparacion-campana-114/manifiesto-114-344M.csv) sin cambios (1.026 bloques de ~38,22 M, SHA-256 `f5180881a003336fa5515e5ce74d2e056ca93a7f457db97c4931e2fc33f19a4a`).

**Resultado.** Los 1.026 bloques se publicaron y verificaron. La fusión, la evaluación, la exportación y el inventario terminaron con código 0 y sin salida de error. **Integridad: 114 de 114 referencias. Bordes: 1.710 de 1.710 regiones dentro de ±1 pp. Roca: 107 de 114 vistas alcanzan la meta descriptiva**; las 7 restantes quedan entre 0,892 y 0,898 y se conservan y reportan. Ninguna herramienta declara validación física ni habilita producción.

## 1. Ejecución

| Elemento | Valor |
|---|---|
| Partición | `amd` de SC3: exadell (AMD EPYC 9554) y smexa (AMD EPYC 9534), 64 hilos, 8 GB y un límite de 15 min por trabajo |
| Trabajos | 1.029: 1.026 `COMPLETED 0:0` y 3 `FAILED` (filas 120–122, por cuota de `/home` excedida, reintentadas y completadas). 642 en smexa y 387 en exadell ([sacct-campana.txt](datos/sc3/campana-114/posproceso/sacct-campana.txt)) |
| Duración por bloque | 128,9 s de media (mínimo 105, máximo 161) |
| Intervalo | 2026-10-02 18:10:27 a 2026-10-03 09:48:49, ~15,6 h de reloj |
| Cómputo | ~2.352 hilo-horas asignadas |
| Lanzador | Herramientas de la réplica `7c120ce`, con las opciones `--particion`, `--tiempo` y `--memoria` (`bdfd4ba`, `fa79196`) y la verificación paralela de bloques publicados (`c5eac94`, con plan equivalente comprobado) |
| Incidencias | Cuota de `/home` llena a las 20:03 (se liberaron 2,3 GB de cachés de entrenamiento tras respaldarlas y verificarlas en otro equipo); falsos bloqueos por visibilidad de NFS (resueltos sin intervención por el ciclo v4); ~21 min de envío detenido en total |

## 2. Evaluación de las 114 vistas

[evaluacion-114-344M.json](datos/sc3/campana-114/posproceso/evaluacion-114-344M.json), producido por `evaluar_campana_114.py` con el plan congelado, la receta y la referencia ideal de cielo con margen de 5°.

**Bordes.** Las 15 regiones de cada una de las 114 vistas son equivalentes dentro de ±1 pp con el intervalo completo, con α = 0,05/114 por vista (familia completa al 95 %). El mayor extremo de un intervalo fue 0,933 pp (geo-train-02, vista 5, `column_2`).

**Roca** (indicador descriptivo: ≥ 90 % de las ROI de 4 × 4 con ≥ 100 cuentas). Lo cumplen 107 de 114 vistas. Por vista, la fracción va de 0,892 a 1,000 (mediana 0,961), la mediana de cuentas por ROI de 190 a 260,5, y el percentil 10 de 97,2 a 157,5.

| Geometría | Vistas que cumplen | Fracción ≥ 100 (mín.–máx.) | ROI por vista |
|---|---:|---|---:|
| geo-gen-01 | 6/6 | 0,959–0,969 | 196 |
| geo-test-01 | 6/6 | 0,988–1,000 | 170 |
| geo-test-02 | 6/6 | 0,961–0,966 | 178 |
| geo-test-03 | 4/6 | 0,892–0,919 | 222 |
| geo-train-01 | 6/6 | 0,954–0,967 | 152 |
| geo-train-02 | 6/6 | 0,900–0,943 | 230 |
| geo-train-03 | 6/6 | 0,920–0,947 | 188 |
| geo-train-04 | 6/6 | 0,980–1,000 | 150 |
| geo-train-05 | 6/6 | 0,905–0,933 | 210 |
| geo-train-06 | 5/6 | 0,893–0,922 | 244 |
| geo-train-07 | 6/6 | 0,970–0,994 | 168 |
| geo-train-08 | 6/6 | 0,951–0,971 | 204 |
| geo-train-09 | 3/6 | 0,893–0,917 | 206 |
| geo-train-10 | 6/6 | 0,973–0,989 | 186 |
| geo-train-11 | 6/6 | 0,953–0,984 | 192 |
| geo-train-12 | 5/6 | 0,897–0,940 | 234 |
| geo-val-01 | 6/6 | 0,987–0,994 | 156 |
| geo-val-02 | 6/6 | 0,980–0,993 | 152 |
| geo-val-03 | 6/6 | 0,949–0,965 | 198 |

Vistas por debajo de la meta, conservadas sin cambios: geo-test-03 v1 (0,896) y v5 (0,892); geo-train-06 v3 (0,893); geo-train-09 v1 (0,898), v4 (0,898) y v5 (0,893); geo-train-12 v2 (0,897). Corresponden a geometrías con más ROI de roca. No se aumentó N, no se descartaron imágenes ni se modificó la regla después de conocer los resultados. La proyección previa a la campaña estimaba una fracción media de 89,7–91,1 %; la mediana observada por vista es 96,1 %.

## 3. Productos y huellas

| Producto | Ubicación en SC3 | Tamaño | Huella |
|---|---|---|---|
| Bloques publicados (1.026) | `~/muography-scratch/oe1-114-344M-publicados` | 734 MB | [bloques-publicados.sha256](datos/sc3/campana-114/posproceso/bloques-publicados.sha256) |
| Fusión (114 vistas) | `~/muography-scratch/oe1-114-344M-fusion` | 32 MB | [fusion.sha256](datos/sc3/campana-114/posproceso/fusion.sha256) |
| Imágenes exportadas (114 NPZ) | `~/muography-scratch/oe1-114-344M-imagenes` | 11 MB | [imagenes.sha256](datos/sc3/campana-114/posproceso/imagenes.sha256) |
| Inventario | — | — | [inventario-114-344M.json](datos/sc3/campana-114/posproceso/inventario-114-344M.json): 114/114, `technical_complete: true`, 9.120 pares objetivo |

Evidencia completa en [datos/sc3/campana-114/posproceso/](datos/sc3/campana-114/posproceso/): comandos, salidas, códigos de salida, entorno, huellas de herramientas frente a Git (57 de 57) y `salidas.sha256` (25 archivos). Scripts ejecutados: [campana_114_preparar_7c120ce.sh](verificacion/campana_114_preparar_7c120ce.sh), [campana_114_lanzar_v5.sh](verificacion/campana_114_lanzar_v5.sh) (y versiones anteriores) y [campana_114_posproceso.sh](verificacion/campana_114_posproceso.sh).

## 4. Siguiente paso

Formar los 9.120 pares con `empaquetar_angular_v1.py --salida` y NumPy 2.4.4 (la versión con la que se verificaron los 480 pares del piloto), convertirlos al formato de entrenamiento sin pérdida y reentrenar el modelo con estos datos.

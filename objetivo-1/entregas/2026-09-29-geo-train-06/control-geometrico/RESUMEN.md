# Control geométrico — variantes A y B, catálogo de 19 geometrías

## 1. Propósito

Verificar, sobre el catálogo completo de 19 geometrías y sus 6 vistas de detector, que la corrección B1 ("la anomalía posterior en el orden del JSON gana la región de intersección, recortada al edificio") elimina en Geant4 las superposiciones de volúmenes detectadas en la construcción recibida (variante A), y que el campo de materiales resultante coincide con el del motor analítico de referencia. El control se ejecuta en cuatro tareas (T1–T4) sobre dos binarios de la misma base de código: la variante A (geometría recibida, con diagnóstico P0 inerte) y la variante B (A más la corrección P1 "B1").

## 2. Herramientas y parámetros

| Parámetro | Valor |
|---|---|
| Motor | Geant4 11.4.2 (`geant4-config --version`) |
| Compilador | GNU 14.2.0 (módulo `gnu14/14.2.0`) |
| Binario variante A | `build-A/muography_sim`, SHA-256 `935e8ceca0d4010929d6791c4cf3e78cd0a47d43def96cd3fdbb8bb5d3b8d7b1` |
| Binario variante B | `build-B/muography_sim`, SHA-256 `7c5416a90563ec8b17446f1d20ec8986aafb5401d5e833bff36ec512413d41f6` |
| T1 — resolución de `CheckOverlaps` | 100 000 puntos de muestreo por volumen |
| T1 — tolerancia | 0 |
| T1 — semilla | 20 260 929 |
| T2 — semilla | 20 260 929 |
| T2 — muestras Monte Carlo de volumen (`--volume-stat`) | 10 000 000 |
| T4 — semilla | 2 026 092 900 |
| T4 — eventos | 10 000 |
| T4 — hilos | 8 |
| Geometría de detalle (T2–T4) | `geo-train-06`, vista 0 |

Motor de referencia analítico: `scripts/simulation/surrogate/geometry.py` del repositorio muography-dl-reconstruction (método `VolcanoGeometry.density`), sobre el mismo catálogo JSON que alimenta los binarios de Geant4.

### Ejecución en SC3

| Trabajo SLURM | Tarea | Script | Partición / nodo | CPU / memoria | Duración | Estado SLURM |
|---|---|---|---|---|---|---|
| 30465 | T1, primer intento | `control_geometrico.sbatch`, versión previa | legacy / guane02 | 24 / 48G | 00:00:32 | COMPLETED 0:0 (registro de estado fallido) |
| 30466 | T2 y T4 | `control_t2_t4.sbatch` | legacy / guane03 | 8 / 16G | 00:00:16 | COMPLETED 0:0 |
| 30467 | T1 | `control_geometrico.sbatch` | legacy / guane02 | 24 / 48G | 00:00:33 | COMPLETED 0:0 |

Fuente: `sacct-30465-30467.txt` (horas absolutas en hora local del clúster, UTC−5).

- Trabajo 30465: los 228 logs de `--check-geometry` se escribieron, pero el paso de registro de estado falló (`Permission denied` en `oe1-ctrl-t1-30465.out`) porque la variable `STATUSDIR` no se exportaba a los procesos lanzados por `xargs`. SLURM lo registró como COMPLETED porque el script no propagaba ese error. La única diferencia entre el script de 30465 y el entregado es la línea `export OUT TABLAS SEED STATUSDIR` (antes, `export OUT TABLAS SEED`).
- Trabajo 30467: se ejecutó en la misma carpeta de salida y regeneró los 228 logs, `resultados-t1.tsv` y `registro-t1.txt`; cada log se escribe con una redirección que trunca el archivo, y todas las marcas de tiempo del archivo `control-geometrico-logs.tar.gz` para esos archivos caen dentro de la ejecución de 30467. Ningún archivo producido por 30465 se usa en los resultados; su salida SLURM se conserva como registro del fallo.
- Los dos scripts `.sbatch` se entregan exactamente como se ejecutaron en 30466 y 30467 (huellas en `SHA256SUMS.txt`). Contienen rutas del clúster (`#SBATCH --output=/home/<usuario>/oe1-trabajo/salidas/control-geometrico/slurm/%x-%j.out` y `ROOT="$HOME/oe1-trabajo"`); para ejecutarlos en otra cuenta hay que crear antes el directorio de salida de SLURM y ajustar la línea `--output`.

## 3. T1 — control de superposiciones (228 corridas)

228 = 19 geometrías × 6 vistas × 2 variantes (trabajo 30467). Los códigos de salida coinciden con lo esperado: 1 (superposición detectada) en las 36 corridas de la variante A sobre las 6 geometrías defectuosas, y 0 en las 78 corridas restantes de A y en las 114 de B (`oe1-ctrl-t1-30467.out`).

| Geometría | Vistas con superposición — A | Vistas con superposición — B |
|---|---|---|
| geo-gen-01 | 6/6 | 0/6 |
| geo-test-01 | 6/6 | 0/6 |
| geo-test-02 | 0/6 | 0/6 |
| geo-test-03 | 6/6 | 0/6 |
| geo-train-01 a geo-train-05 | 0/6 cada una | 0/6 cada una |
| geo-train-06 | 6/6 | 0/6 |
| geo-train-07 | 0/6 | 0/6 |
| geo-train-08 | 6/6 | 0/6 |
| geo-train-09, geo-train-10 | 0/6 cada una | 0/6 cada una |
| geo-train-11 | 6/6 | 0/6 |
| geo-train-12 | 0/6 | 0/6 |
| geo-val-01, geo-val-02, geo-val-03 | 0/6 cada una | 0/6 cada una |

**Veredicto T1: cumple.** La variante B reporta 0 superposiciones en las 114 corridas. La variante A reporta superposición en las 6 vistas de exactamente las 6 geometrías esperadas (geo-gen-01, geo-test-01, geo-test-03, geo-train-06, geo-train-08, geo-train-11) y 0 superposiciones en las 78 corridas restantes (13 geometrías × 6 vistas). No se registraron corridas parciales (geometría con superposición en solo algunas vistas) ni discrepancias entre el código de salida y el resultado reportado por `OVERLAP-CHECK-SUMMARY`.

## 4. T2 — sondeos, volúmenes y cortes (geo-train-06, vista 0)

### 4.1 Sondeos puntuales

| Punto (x, y, z) [m] | Material analítico | Densidad analítica [g/cm³] | Resultado A | Resultado B |
|---|---|---|---|---|
| (21,354; −30,722; 137,795) | anomalía 1 (cuerpo denso) | 3,285 | anomalía 1 | anomalía 1 |
| (20,3; −24,5; 300,0) | anomalía 0 (conducto) | 1,832 | anomalía 0 | anomalía 0 |
| (20,3; −24,5; 40,0) | anomalía 0 (conducto) | 1,832 | anomalía 0 | anomalía 0 |
| (21,35; −30,7; 90,0) | anomalía 0 (conducto) | 1,832 | anomalía 0 | anomalía 0 |
| (32,2; −130,0; 137,8) | anomalía 1 (cuerpo denso) | 3,285 | anomalía 1 | anomalía 1 |
| (200,0; 0,0; 50,0) | roca | 2,65 | roca | roca |
| (0,0; 0,0; 420,0) | aire | 0,001225 | aire | aire |

**Los 7 sondeos de la variante B coinciden exactamente con la clase de material analítica.** (La variante A también coincidió en los 7 puntos elegidos; esto es un dato de diagnóstico y no un criterio bloqueante para A, cuya navegación no está definida en la región de superposición.)

### 4.2 Volúmenes de las anomalías (variante B)

| Anomalía | Volumen esperado [m³] | Volumen observado [m³] | Error estándar combinado [m³] | Diferencia [m³] | Diferencia en EE combinados |
|---|---|---|---|---|---|
| anomalía 0 (conducto menos la intersección) | 387 408,5 ± 44,7 | 387 492,0 (Monte Carlo, N = 10 000 000, EE = 90,7) | 101,1 | 83,5 | 0,83 |
| anomalía 1 (cuerpo denso completo) | 1 215 148,5 (exacto) | 1 215 150,0 (analítico exacto; impreso a 6 cifras significativas) | 5,0 (piso de precisión de impresión) | 1,5 | 0,30 |

**Ambos volúmenes de la variante B caen dentro de 3 errores estándar combinados del valor esperado.** El error estándar combinado de la anomalía 0 propaga la incertidumbre Monte Carlo del binario (90,7 m³, N = 10⁷) y la del volumen de intersección auditado (44,7 m³, `auditoria-geometrica-oe1.json`). El de la anomalía 1 refleja únicamente el redondeo del formato de impresión del binario (`%g` a 6 cifras significativas: `1.21515e+06`), ya que ese volumen es analítico exacto en ambos motores.

### 4.3 Comparación de cortes contra el motor analítico

| Corte | Puntos | Discrepancias totales | De borde (± medio paso de grilla) | De clase aire | No explicadas |
|---|---|---|---|---|---|
| y = −30,7 m — variante A | 126 721 | 20 | 20 | 0 | 0 |
| y = −30,7 m — variante B | 126 721 | 20 | 20 | 0 | 0 |
| z = 137,8 m — variante A | 105 651 | 0 | 0 | 0 | 0 |
| z = 137,8 m — variante B | 105 651 | 0 | 0 | 0 | 0 |

**Cero discrepancias no explicadas en los cortes de la variante B** (y, como referencia, también en la variante A para estos dos cortes). Las 20 discrepancias del corte y = −30,7 m están a media grilla o menos de la superficie del cono o de una anomalía, donde la densidad analítica no es constante; ninguna corresponde a un emparejamiento con aire ni queda sin explicación.

**Veredicto T2: cumple** (sondeos, volúmenes y cortes).

## 5. T3 — figuras

Cuatro mapas PNG (`viridis`/paleta categórica, etiquetas en español, misma escala de color en los tres paneles de material):

1. `t3_corte_y-30.7_materiales.png` — mapas de material (motor analítico, Geant4 A, Geant4 B) en el corte y = −30,7 m.
2. `t3_corte_y-30.7_discrepancias.png` — discrepancias no explicadas, A vs. analítico y B vs. analítico, mismo corte.
3. `t3_corte_z137.8_materiales.png` — mapas de material en el corte z = 137,8 m.
4. `t3_corte_z137.8_discrepancias.png` — discrepancias no explicadas, mismo corte.

Los cuatro mapas de discrepancias no muestran ningún punto marcado (consistente con el conteo de la sección 4.3).

## 6. T4 — corrida normal (geo-train-06, vista 0, 10 000 eventos, 8 hilos)

| Verificación | Variante A (referencia) | Variante B (criterio bloqueante) |
|---|---|---|
| `RUN DONE` impreso | sí | sí |
| Líneas `GeomVol1002` | 1 (esperado: la geometría recibida sigue defectuosa) | 0 |
| Líneas `GeomNav` | 0 | 0 |
| `events_transported` | 10 000 | 10 000 |
| `detected_in_bins` | 7 601 | 7 601 |
| Suma del histograma | 7 601,0 | 7 601,0 |
| Suma del histograma = `detected_in_bins` | sí | sí |

**Veredicto T4: cumple** para la variante B (impresión limpia, sin `GeomVol1002` ni `GeomNav`, histograma y metadatos no vacíos, conteo de eventos transportados y suma del histograma consistentes). La variante A se ejecutó como referencia y, como se esperaba, imprimió una advertencia `GeomVol1002` en la construcción; esto no es un criterio bloqueante para A.

Nota: además del conteo agregado (7 601 detectados de 10 000 eventos), el histograma de 256 × 256 bins es **idéntico byte a byte** entre A y B (`geo-train-06_view0_hist.csv`, SHA-256 `a31f3e8d…` en ambas variantes, ver `SHA256SUMS.txt`). La corrección B1 sí cambia el material que encuentran las trayectorias que cruzan la intersección conducto–cuerpo denso (83 641,9 m³ según `../diagnostico/auditoria-geometrica-oe1.json`); la igualdad se explica por la estadística de esta corrida corta. Según el pre-registro de ROI (`../analisis/roi-preregistro.json`), los 195 píxeles cuya línea de visión recorre al menos 20 m de la intersección reciben ≈ 1,1 conteos por 10⁶ eventos según el modelo analítico (≈ 2,1 si se aplica el cociente campaña/modelo de 1,91 medido en esa región), es decir ≈ 0,01–0,02 conteos esperados con 10 000 eventos. Con la misma semilla, A y B parten de la misma secuencia de eventos: en modo multihilo, Geant4 genera en el hilo maestro las semillas de cada evento y reinicia el generador aleatorio al comienzo de cada evento (comportamiento por defecto, `SeedOncePerCommunication` = 0; la aplicación solo fija la semilla del hilo maestro, en `muography_sim.cc`), de modo que una diferencia de transporte en un evento no altera los números aleatorios de los demás. Solo las trayectorias que cruzan la intersección pueden diferir entre variantes; histogramas idénticos son coherentes con que ninguna trayectoria detectada la haya cruzado. No se verificó trayectoria por trayectoria. **Límite explícito**: esta corrida (vista 0, 10 000 eventos) no mide el efecto de B1 sobre los conteos; solo muestra que ambos binarios se ejecutan limpiamente y producen histogramas y metadatos consistentes.

## 7. Veredicto global

| Tarea | Veredicto |
|---|---|
| T1 | cumple |
| T2 | cumple |
| T3 | 4 figuras generadas |
| T4 | cumple |
| **Global** | **cumple** |

Todas las cifras de este documento provienen de `criterios-t1-t4.json`, `sondeos-volumenes.json`, `cortes-comparacion.json` y `resumen-solapes.csv`, generados por `scripts/analysis/oe1_geometry_check_report.py` (repositorio muography-dl-reconstruction) a partir de los datos crudos listados en `SHA256SUMS.txt`, salvo los datos de ejecución de la sección 2 (`sacct-30465-30467.txt`, salidas SLURM) y las cifras citadas del diagnóstico y del pre-registro de ROI en la sección 6.

## 8. Límites

- El muestreo aleatorio de superficies que usa `CheckOverlaps` (T1) es evidencia de superposición o de su ausencia con una resolución fija de 100 000 puntos; no es una prueba geométrica universal de ausencia de superposición para cualquier resolución arbitrariamente alta.
- Los sondeos puntuales del navegador (T2, sección 4.1) son estáticos: reportan qué volumen y densidad asigna el navegador de Geant4 en un punto fijo, no el comportamiento del transporte de partículas a través de ese punto.
- La diferencia de densidad del aire entre motores (Geant4 `G4_AIR` = 0,00120479 g/cm³ frente al valor analítico 0,001225 g/cm³) es una diferencia de material de referencia esperada y no defectiva; se comparó por clase de material ("aire"), no por valor numérico exacto.
- El vértice del cono difiere por construcción entre motores (radio de vértice de Geant4 = 0,1 m frente al radio de vértice analítico = 0 m); los puntos en esa vecindad se clasifican como de borde y no como discrepancia.
- Los volúmenes de la sección 4.2 combinan, según el caso, incertidumbre Monte Carlo del binario, incertidumbre del volumen de intersección auditado, y el piso de precisión de impresión del formato `%g` a 6 cifras significativas del binario; ninguno de los tres es una fuente de error física.
- T4 (sección 6) no mide el efecto de B1 sobre los conteos; solo muestra ejecución limpia y consistencia interna de salida (ver nota al final de la sección 6).

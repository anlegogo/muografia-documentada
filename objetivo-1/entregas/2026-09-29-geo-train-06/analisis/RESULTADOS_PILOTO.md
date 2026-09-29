# Resultados del piloto A/B — geo-train-06, vista 0

## 1. Objeto y trazabilidad

Este documento reporta el piloto comparativo A/B de `geo-train-06`, vista 0, entre la geometría recibida (variante A, "original") y la corrección B1 (variante B, "corregida"), diseñado en el paso 4 del plan operativo y pre-registrado en `PREREGISTRO_ROI.md` antes de ejecutarse. La corrección B1 reemplaza, en el solape geométrico entre el conducto y el cuerpo denso, la resolución dependiente de la trayectoria de navegación de Geant4 por una construcción CSG explícita (`G4SubtractionSolid`, ver sección 2), que asigna ese volumen al cuerpo denso.

**Diseño del piloto:** 1 000 000 de eventos transportados por corrida, 3 semillas compartidas entre A y B (números aleatorios comunes) — `2026092801`, `2026092802`, `2026092803` —, 8 hilos, 6 corridas en total (3 semillas × 2 variantes).

**Binarios y envío (SLURM):**

| | Variante A ("original") | Variante B ("corregida") |
|---|---|---|
| Binario | `build-A/muography_sim`, sha-256 `935e8ceca0d4…d3b8d7b1` | `build-B/muography_sim`, sha-256 `7c5416a905…12413d41f6` |
| Job SLURM | 30468 | 30469 |
| Partición / nodo | legacy / guane01 | legacy / guane01 |
| Estado / código de salida | COMPLETED, 0:0 | COMPLETED, 0:0 |
| Tiempo transcurrido | 00:04:10 | 00:04:04 |

Fuente: `../piloto/envio.txt`, `../piloto/sacct-30468-30469.txt`. El script de envío (`ejecutar_piloto_oe1.sbatch`, sha-256 `8178a3b2f377…8f93732de9`) es el que entregó la revisión, sin modificar; las opciones de partición, memoria, tiempo y variables de entorno (variante, binario, geometría, tablas) se pasaron en la línea de `sbatch`, no dentro del script.

**Trazabilidad de código y pre-registro frente al envío del piloto.** El pre-registro de ROI (`PREREGISTRO_ROI.md`, `roi-preregistro.json`, `roi-mascaras.npz`) quedó fijado en el commit `cc7dc76` del repositorio de la entrega documentada (`docs(oe1): añade el pre-registro de ROI y las verificaciones de registro en azimut del piloto`), con fecha de commit `2026-09-29T10:57:07Z` (huso `-05:00` reportado como `05:57:07 -0500`; verificado con `git show -s --format="%ci" cc7dc76`). El envío del piloto (`envio.txt`) quedó registrado con `fecha_utc: 2026-09-29T10:57:45Z`. El commit del pre-registro precede al envío por 38 s: las cinco ROI, sus máscaras y el efecto esperado (`Δ_max`) de la sección 4 de `PREREGISTRO_ROI.md` quedaron fijados antes de que existiera cualquier dato del piloto real, de modo que la interpretación de la sección 5 de este documento no pudo ajustarse a lo que el piloto terminara mostrando.

El subcomando `analyze` de `scripts/analysis/oe1_pilot_roi.py`, que produjo los resultados de la sección 4, quedó versionado en el commit `0c8fd33` del repositorio de código (`feat(analysis): add pre-registered OE1 pilot ROI analysis`; sha-256 del archivo `5b82b05f9975…30a5a42468`, el mismo que registra `metadata.script_sha256` de `roi-resultados.json`). Se escribió mientras corría el piloto, implementando literalmente las secciones 6 y 7 del pre-registro, y se probó solo con datos sintéticos. Antes de terminarlo ya se conocían la validación de las seis corridas y la salida del comparador del revisor (eficiencias globales idénticas entre A y B); a partir del diseño de semillas comunes se le añadió el tratamiento de varianza nula entre réplicas. Ninguna cifra por ROI del piloto se calculó antes de ejecutar `analyze`.

## 2. Validación de las 6 corridas

Todas las corridas: `SHA256SUMS` verificado (hist, meta, `run.log`, `comando.txt` recalculados contra el archivo de cada carpeta), `RUN DONE` en `run.log`, `events=1 000 000`, y suma del histograma (`geo-train-06_view0_hist.csv`, descomprimido en copia temporal fuera del repositorio) igual a `detected_in_bins` del `.meta.json` en las 6 corridas.

| Variante | Semilla | Eventos | Detectados | Detectados/eventos | `GeomVol1002` | `GeomNav` | Tiempo de pared (s) | Carpeta |
|---|---|---|---|---|---|---|---|---|
| original | 2026092801 | 1 000 000 | 752 098 | 0,752098 | 1 | 0 | 81,4951 | `../piloto/original/2026092801/` |
| original | 2026092802 | 1 000 000 | 752 380 | 0,752380 | 1 | 0 | 78,9779 | `../piloto/original/2026092802/` |
| original | 2026092803 | 1 000 000 | 751 804 | 0,751804 | 1 | 0 | 81,6164 | `../piloto/original/2026092803/` |
| corregida | 2026092801 | 1 000 000 | 752 098 | 0,752098 | 0 | 0 | 76,0010 | `../piloto/corregida/2026092801/` |
| corregida | 2026092802 | 1 000 000 | 752 380 | 0,752380 | 0 | 0 | 78,3998 | `../piloto/corregida/2026092802/` |
| corregida | 2026092803 | 1 000 000 | 751 804 | 0,751804 | 0 | 0 | 81,2572 | `../piloto/corregida/2026092803/` |

Fuente: `geo-train-06_view0.meta.json` y `run.log` de cada corrida (conteo de `GeomVol1002`/`GeomNav` por `grep -c` sobre `run.log`). En A, el único aviso `GeomVol1002` por corrida (`G4PVPlacement::CheckOverlaps()`, solape entre `anomaly_1` y `anomaly_0`) es el esperado para la geometría recibida, sin resolución CSG del solape; en B no aparece ningún aviso `GeomVol1002` ni `GeomNav`, y los tres `run.log` de B registran en su lugar `ANOMALY-CSG name=anomaly_0 kind=conduit … solid=G4SubtractionSolid placed=yes` seguido de `anomaly_1 kind=dense_body … placed=yes`, consistente con la resolución explícita del solape por sustracción booleana.

## 3. Comparador del revisor

Salida de `herramientas/comparar_piloto_oe1.py` (sha-256 `16ccee3028bc…9cacfd718f69fd46`), ejecutado en el clúster (`guane.sc3.uis.edu.co`, Python 3.9.25, NumPy 1.23.5, salida de proceso `exit=0`, sin `ValueError`; ver `comando-comparador.txt` y `salida-comparador.txt`), sobre el histograma completo de la vista (65 536 píxeles), no restringido a las ROI:

| Semilla | Eficiencia A | Eficiencia B | Δ eficiencia | Diferencia absoluta media por píxel y evento |
|---|---|---|---|---|
| 2026092801 | 0,752098 | 0,752098 | 0,0 | 0,0 |
| 2026092802 | 0,752380 | 0,752380 | 0,0 | 0,0 |
| 2026092803 | 0,751804 | 0,751804 | 0,0 | 3,0518×10⁻¹¹ |

Media de Δ eficiencia entre las 3 semillas: 0,0. Desviación entre réplicas: 0,0. Error estándar de la media: 0,0 (`resumen-piloto.json`, campos `media_delta_eficiencia`, `desviacion_entre_replicas`, `error_estandar_media_delta`).

**Límites, en el propio texto del comparador** (`resumen-piloto.json`, campo `limites`): "Tres pares son piloto. Semilla compartida no asegura trayectorias idénticas. Sin criterio automático de equivalencia; revisar mapas, geometría e incertidumbre local." El propio comparador anota además, por semilla (campo `nota_espacial`): "Incluye fluctuaciones Monte Carlo; no es por sí sola cambio físico."

El valor no nulo de la semilla `2026092803` (3,0518×10⁻¹¹) es exactamente `2 / (65 536 × 10⁶)`: dos píxeles de los 65 536 difieren en una cuenta cada uno sobre 10⁶ eventos — el mismo evento cambiado que identifica el análisis de ROI en la sección 4.

## 4. Análisis de ROI prerregistrado

Salida de `oe1_pilot_roi.py analyze` (sha-256 del script `5b82b05f9975…30a5a42468`; `roi-resultados.json`, `roi-resultados-mapas.png`; ejecutado con Python 3.13.5 / NumPy 2.4.4, `metadata.generated_utc = 2026-09-29T11:35:10Z`). Validación interna del script: `validation.ok = true`, sin errores ni advertencias.

**Conteos por ROI y semilla** (conteo crudo dentro de la máscara; A y B tienen el mismo `events_transported` por semilla, 1 000 000, por lo que el conteo "por 10⁶ eventos" coincide con el conteo crudo):

| ROI | Píxeles | Semilla 2026092801 (A=B) | Semilla 2026092802 (A=B) | Semilla 2026092803 (A=B) | Media D (B−A) | SD entre réplicas |
|---|---|---|---|---|---|---|
| `R_int` | 195 | 2 | 0 | 2 | 0,0 | 0,0 |
| `R_cond` | 769 | 84 | 82 | 73 | 0,0 | 0,0 |
| `R_body` | 830 | 14 | 17 | 19 | 0,0 | 0,0 |
| `R_rock` (control) | 12 849 | 2 875 | 2 848 | 2 901 | 0,0 | 0,0 |
| `R_sky` (control) | 50 842 | 749 020 | 749 349 | 748 717 | 0,0 | 0,0 |

**Comparación contra el efecto pre-registrado** (`Δ_max` y EE pre-registrado por 10⁶ eventos, sección 4 de `PREREGISTRO_ROI.md`; EE observado = SD/√3, usado solo para el control de espurios, nunca para clasificar):

| ROI | `Δ_max` (pre-registrado) | EE previsto (media 3 semillas) | `|Δ_max|`/EE previsto | EE observado (media 3 semillas) | Categoría (sección 7) |
|---|---|---|---|---|---|
| `R_int` | −0,0933 | 0,8629 | 0,108 | 0,0 | Inconcluso por potencia insuficiente |
| `R_cond` | −0,0028 | 3,2528 | 0,0009 | 0,0 | Inconcluso por potencia insuficiente |
| `R_body` | −0,0007 | 1,8858 | 0,0004 | 0,0 | Inconcluso por potencia insuficiente |
| `R_rock` (control) | 0,0 | 21,9427 | 0,0 | 0,0 | Inconcluso por potencia insuficiente |
| `R_sky` (control) | 0,0 | 707,7373 | 0,0 | 0,0 | Inconcluso por potencia insuficiente |

**Controles** (`control_check`, sección 6 punto 5 de `PREREGISTRO_ROI.md`): en `R_rock` y `R_sky`, la diferencia emparejada media es compatible con 0 dentro de su propio error estándar observado (`compatible_with_zero: true`, `spurious_difference_detected: false` en ambos); el procedimiento no introduce una diferencia espuria.

**Eficiencia global por variante** (`global_efficiency.per_variant`, suma de las 3 semillas): A = 2 256 282 / 3 000 000 = 0,752094; B = 2 256 282 / 3 000 000 = 0,752094 — idéntica cifra a 6 decimales.

**Figura:** `roi-resultados-mapas.png` (3 767 116 bytes) muestra, por semilla y en promedio, los mapas de conteo por evento de A y B y el mapa de diferencia firmada (B−A) con las cinco máscaras superpuestas, conforme al plan de la sección 6, punto 6 de `PREREGISTRO_ROI.md`.

**El único evento cambiado.** De los 3 000 000 de eventos transportados por variante (3 semillas × 1 000 000), el histograma crudo de A y B es idéntico píxel a píxel en las semillas `2026092801` y `2026092802`, y difiere en exactamente 2 de los 65 536 píxeles en la semilla `2026092803`: el píxel (fila de elevación 39, columna de azimut 133) tiene conteo 1 en A y 0 en B, y el píxel (fila 40, columna 133) tiene conteo 0 en A y 1 en B (comprobado por descompresión y comparación directa de `geo-train-06_view0_hist.csv` de ambas variantes, semilla `2026092803`; las demás 65 534 celdas son idénticas). Ambos píxeles están dentro de la máscara `R_int` (verificado contra `roi-mascaras.npz`), de modo que el conteo total de `R_int` en esa semilla es 2 tanto en A como en B (sección 4, tabla de conteos): la corrección B1 desplazó el bin de llegada de una trayectoria detectada, en la frontera dentro de la intersección conducto–cuerpo denso, sin cambiar el total de ninguna ROI. Esto muestra que la corrección tiene un efecto real y localizable a nivel de evento individual dentro de `R_int` — no es únicamente ruido de punto flotante — pero, al tratarse de un solo evento sobre 3 000 000, no muestra nada sobre la dirección ni la magnitud del efecto sistemático que predice la sección 4 (`B1` frente a `conduit-wins`), ni sobre si ese efecto es distinto de 0 en el agregado.

## 5. Interpretación según la sección 7 de `PREREGISTRO_ROI.md`

Las cinco ROI —`R_int`, `R_cond`, `R_body` y los controles `R_rock`, `R_sky`— caen en el caso 1 de la sección 7: el error estándar previsto de la media de 3 semillas excede `|Δ_max|` en las tres ROI de interés (cociente 0,108 en `R_int`, 0,0009 en `R_cond`, 0,0004 en `R_body`) y ambos controles tienen `Δ_max = 0` por construcción. El resultado se reporta como inconcluyente por potencia insuficiente en las tres ROI de interés, sin que el signo de la diferencia observada (que además es exactamente 0 en las tres) sea relevante para esa clasificación.

Esto **no** equivale a evidencia de que A y B sean equivalentes: la sección 7 distingue explícitamente ese caso 1 (inconcluso por potencia insuficiente) del caso 3 (nulo con potencia adecuada), y este piloto cae en el primero. La estadística planeada (3 semillas de 1 000 000 de eventos, con la magnitud de `Δ_max` pre-registrada) no tenía, de partida, capacidad para separar 0 de `Δ_max` en ninguna de las tres ROI de interés.

Lo que este piloto sí establece:

- **Transporte limpio en B**: cero avisos `GeomVol1002`/`GeomNav` en las 3 corridas de B, frente a exactamente un aviso `GeomVol1002` por corrida en A (sección 2) — la construcción CSG (`G4SubtractionSolid`) elimina el solape ambiguo que generaba el aviso en la geometría recibida.
- **Eficiencia global idéntica entre A y B** en las 3 semillas y en el agregado (sección 3 y 4): 0,752098, 0,752380 y 0,751804 por semilla, 0,752094 en el agregado de 3 000 000 de eventos por variante.
- **Comportamiento consistente con números aleatorios comunes**: los histogramas completos de A y B son idénticos píxel a píxel en 2 de las 3 semillas, y difieren en exactamente 2 píxeles (un desplazamiento de bin de un único evento) en la tercera — la varianza entre A y B queda, en la práctica, casi enteramente suprimida por el uso de semillas compartidas, muy por debajo de lo que asumió el cálculo pre-registrado del error estándar (que modeló A y B como Poisson independientes; ver sección 6).
- **Un evento con cambio localizado y verificable** dentro de `R_int`, atribuible a la corrección de la resolución del solape, sin que ese cambio, por sí solo, altere el total de ninguna ROI ni permita pronunciarse sobre la dirección o magnitud del efecto sistemático pre-registrado.

## 6. Propuesta de presupuesto para una corrida siguiente (propuesta, no decisión)

Esta sección propone un método para dimensionar una futura corrida comparativa con mayor potencia estadística en `R_int`; no recomienda una cifra de eventos ni decide si esa corrida debe ejecutarse. Se apoya en un modelo simplificado, explícito en sus supuestos, y en el único dato empírico disponible sobre la tasa de eventos que cambian entre A y B (el evento único de la sección 4), que es una estimación muy débil.

**Modelo con números aleatorios comunes (CRN).** Bajo semillas compartidas, un evento que produce el mismo resultado en A y en B no aporta nada a la diferencia pareada `D_s`; solo los eventos cuyo resultado cambia contribuyen. Sea, para una ROI dada:

- `N` = eventos transportados por corrida y por variante (igual en A y B por usar semillas comunes).
- `r` = probabilidad de que un evento dado sea un "evento cambiado" respecto de esa ROI (su pertenencia a la máscara difiere entre A y B).
- `k` = número de semillas independientes (réplicas emparejadas).
- `Δ_max` = magnitud del efecto sistemático pre-registrado por 10⁶ eventos (sección 4 de `PREREGISTRO_ROI.md`).

Si cada evento cambiado desplaza el conteo pareado en ±1 y los eventos cambiados son aproximadamente independientes entre sí (aproximación de Poisson, válida para `r` pequeño), el conteo de eventos cambiados en una corrida de `N` eventos tiene media y varianza ≈ `N·r`. Expresado en la misma normalización "por 10⁶ eventos" que usa `roi-resultados.json`:

```
Var(D_s, por 1e6 eventos) ≈ r · (1e6)^2 / N
EE(media de k semillas)   = 1e6 · sqrt(r / (N·k))
```

Exigiendo `EE ≤ |Δ_max| / 2` (mismo criterio de separación que usa la sección 7 de `PREREGISTRO_ROI.md` para distinguir los casos 1 y 3, aplicado aquí como objetivo de diseño en vez de como resultado observado):

```
N ≥ (4e12 · r) / (k · Δ_max^2)
```

**Modelo independiente (sin semillas comunes, para comparación).** Si A y B se corrieran con semillas distintas, sus conteos serían aproximadamente Poisson independientes, con varianza combinada `2·λ` (siendo `λ` el conteo esperado por corrida bajo B1). Esta es, de hecho, la suposición que ya usó la sección 4 de `PREREGISTRO_ROI.md` al calcular el error estándar previsto (`EE previsto media 3 semillas = sqrt(2·λ/3)`), aunque el piloto real sí usó semillas comunes. En la misma normalización, con `λ_1e6` el conteo esperado por 10⁶ eventos bajo B1 (`PREREGISTRO_ROI.md`, sección 4):

```
EE(media de k semillas) = sqrt(2 · λ_1e6 · 1e6 / (N·k))
N ≥ (8e6 · λ_1e6) / (k · Δ_max^2)
```

Para `R_int` (`λ_1e6 = 1,1169`, `Δ_max = 0,0933`, `k = 3`, `N = 1e6`), esta fórmula reproduce exactamente el EE previsto ya pre-registrado (0,8629), lo que confirma la fórmula independiente. El EE bajo el modelo CRN de esta sección, con la misma `N` y `k`, y usando la tasa `r̂` estimada abajo, da ≈0,33 — unas 2,6 veces menor que la cifra pre-registrada (0,8629) que asumía independencia — y el SD observado entre las 3 réplicas reales fue, de hecho, exactamente 0,0 (sección 4). Esto es consistente con lo esperado: al compartir semillas, solo los eventos que cruzan la frontera de la ROI aportan varianza, y esos eventos son raros.

**Estimación de `r` a partir del piloto.** El único dato disponible es el evento único de la sección 4: 1 evento cambiado sobre 3 000 000 de eventos examinados (3 semillas × 1 000 000 por variante), `r̂ = 1/3 000 000 ≈ 3,33×10⁻⁷`. Al ser un conteo de Poisson de exactamente 1 observación, su intervalo de confianza exacto (Garwood) al 95 % es [0,0253; 5,572] conteos, es decir `r ∈ [8,44×10⁻⁹; 1,857×10⁻⁶]` — un intervalo de casi tres órdenes de magnitud de ancho: es una estimación muy débil, y así debe leerse. Además, el único evento observado no cruzó la frontera de `R_int` (ambos píxeles, antes y después, quedan dentro de la máscara; sección 4), por lo que `r̂` probablemente sobreestima la tasa de eventos que efectivamente cambian el conteo de `R_int` — los tamaños de corrida de la tabla siguiente deben leerse, por esta razón, como estimaciones conservadoras (más grandes de lo estrictamente necesario) más que como un mínimo ajustado.

**Rango del efecto (`Δ_max`).** La sección 5.2 de `PREREGISTRO_ROI.md` (unidad U8c, exploratoria, no pre-registrada) encontró que la asimetría inducida por una anomalía en mapas de campaña de Geant4 es, aproximadamente, un orden de magnitud más débil que la que predice el motor analítico sin dispersión (`Z` combinado observado ≈1,29 frente a `Z` esperado por el modelo ≈16,44) — el mismo motor analítico sin dispersión que produce el `Δ_max` pre-registrado de la sección 4. Si esa misma razón aplicara a `Δ_max`, el efecto real en `R_int` podría ser cercano a `Δ_max/10 ≈ 0,00933` en vez de `0,0933`. Esta sección usa ambos valores como escenarios, no como una corrección validada de `Δ_max`.

**Tabla de escenarios** (`k = 3` semillas, como en el piloto; eventos totales = `k · N · 2` variantes; conversión a horas de CPU con ~0,73 ms de tiempo de hilo por evento, medido en la reproducción de campaña de esta entrega (`../reproduccion/geo-train-06_view0.meta.json`: `seconds_per_event` = 3,044·10⁻⁵ s de pared con 24 hilos, es decir 0,731 ms por evento); el propio piloto, calculado como tiempo de pared × 8 hilos / eventos, da en promedio ≈0,64 ms/evento en sus 6 corridas, algo menor; se usa 0,73 ms por ser la cifra medida a escala de campaña y la más conservadora):

| Modelo | `r` usado | `Δ_max` usado | `N` por corrida y variante | Eventos totales | Horas-CPU (0,73 ms/evento) |
|---|---|---|---|---|---|
| CRN, `r̂` puntual | 3,33×10⁻⁷ | 0,0933 | 5,1×10⁷ | 3,1×10⁸ | ≈62 |
| CRN, `r̂` puntual | 3,33×10⁻⁷ | 0,00933 (U8c) | 5,1×10⁹ | 3,1×10¹⁰ | ≈6 210 |
| CRN, límite inferior IC 95 % | 8,44×10⁻⁹ | 0,0933 | 1,3×10⁶ | 7,8×10⁶ | ≈1,6 |
| CRN, límite inferior IC 95 % | 8,44×10⁻⁹ | 0,00933 (U8c) | 1,3×10⁸ | 7,8×10⁸ | ≈157 |
| CRN, límite superior IC 95 % | 1,857×10⁻⁶ | 0,0933 | 2,8×10⁸ | 1,7×10⁹ | ≈346 |
| CRN, límite superior IC 95 % | 1,857×10⁻⁶ | 0,00933 (U8c) | 2,8×10¹⁰ | 1,7×10¹¹ | ≈34 610 |
| Independiente (sin CRN) | — | 0,0933 | 3,4×10⁸ | 2,1×10⁹ | ≈417 |
| Independiente (sin CRN) | — | 0,00933 (U8c) | 3,4×10¹⁰ | 2,1×10¹¹ | ≈41 630 |

Como referencia de escala, la exposición de campaña por vista es de ≈3,6×10⁷ eventos en 30 días (`S0 = 36 175 379,9` muones/vista/30 d, `PREREGISTRO_ROI.md`, sección 4; esta cifra proviene de la calibración del motor surrogate frente a la campaña Geant4, no de la Etapa 4 del plan operativo): el escenario CRN con `r̂` puntual y `Δ_max` pre-registrado (5,1×10⁷ eventos por corrida y variante) es del mismo orden que esa exposición; los escenarios con el efecto un orden de magnitud más débil (U8c) o con el límite superior del intervalo de `r`, y en particular el modelo independiente, exceden esa exposición en uno a tres órdenes de magnitud.

**Advertencias explícitas sobre este presupuesto:**

- `r` se estima de un único conteo de Poisson; su intervalo de confianza abarca casi tres órdenes de magnitud y no debe leerse como una tasa medida con precisión.
- El modelo CRN asume que cada evento cambiado desplaza el conteo en exactamente ±1 y que los eventos cambiados son independientes entre sí; no se ha validado contra un conjunto de datos CRN de alta estadística.
- `Δ_max` proviene de un motor analítico sin dispersión (limitación ya documentada en la sección 8 de `PREREGISTRO_ROI.md`); el escenario "U8c" (orden de magnitud menor) es una hipótesis exploratoria, no una corrección validada.
- El criterio `EE ≤ |Δ_max|/2` usa el mismo umbral heurístico de "2·EE" que la sección 7 de `PREREGISTRO_ROI.md` señala explícitamente como no equivalente a un intervalo de Student-t formal con solo 3 semillas (`t(0,975; 2) ≈ 4,303`, no 2); un diseño que exigiera el valor `t` exacto requeriría una corrida mayor que las de esta tabla.
- Las horas-CPU son una conversión aritmética de ~0,73 ms de tiempo de hilo por evento (reproducción de campaña, sección 6), no una medición de `TotalCPU` de estas corridas (`sacct` no reportó `TotalCPU` para los jobs 30468/30469; ver sección 2).
- Esta sección es una propuesta de método de dimensionamiento; no recomienda ejecutar ninguna corrida ni fija un tamaño definitivo.

## 7. Limitaciones y reproducción

**Limitaciones:**

- Las cinco ROI son inconcluyentes por potencia insuficiente (sección 5); ninguna cifra de este documento demuestra ni descarta un efecto de la corrección B1 sobre los conteos detectados.
- El subcomando `analyze` se versionó (commit `0c8fd33`) después de ejecutarse sobre los datos del piloto; el archivo versionado es idéntico (mismo sha-256 `5b82b05f…`) al que produjo `roi-resultados.json`.
- Los conteos de `GeomVol1002`/`GeomNav` se obtuvieron por coincidencia de texto (`grep -c`) sobre `run.log`; no se auditó el resto del registro de Geant4 en busca de otras clases de aviso.
- `Δ_max` (sección 4 de `PREREGISTRO_ROI.md`) proviene de un motor analítico sin dispersión múltiple ni fluctuaciones de pérdida de energía; la sección 5.2 de ese documento indica que puede sobreestimar el efecto real en Geant4 en, aproximadamente, un orden de magnitud.
- El presupuesto de la sección 6 es una propuesta con supuestos explícitos, no una medición ni una recomendación de ejecución.

**Reproducción** (desde la raíz del repositorio `muography-dl-reconstruction`):

Descompresión de copias de los histogramas del piloto (nunca sobre los archivos del repositorio; las seis rutas son `original|corregida` × `2026092801|2026092802|2026092803`):

```
gunzip -k muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/piloto/original/2026092801/geo-train-06_view0_hist.csv.gz
gunzip -k muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/piloto/original/2026092802/geo-train-06_view0_hist.csv.gz
gunzip -k muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/piloto/original/2026092803/geo-train-06_view0_hist.csv.gz
gunzip -k muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/piloto/corregida/2026092801/geo-train-06_view0_hist.csv.gz
gunzip -k muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/piloto/corregida/2026092802/geo-train-06_view0_hist.csv.gz
gunzip -k muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/piloto/corregida/2026092803/geo-train-06_view0_hist.csv.gz
```

Análisis de ROI (borrar los seis `.csv` descomprimidos después de ejecutar):

```
python scripts/analysis/oe1_pilot_roi.py analyze \
  --pilot-root muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/piloto \
  --out-dir muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/analisis
```

Comparador del revisor, ejecutado en el clúster (`guane.sc3.uis.edu.co`, Python 3.9.25, NumPy 1.23.5; ruta de usuario del clúster sustituida por `<usuario>` respecto del comando literal registrado en `comando-comparador.txt`, para no incluir un identificador de autor en este documento):

```
python3 comparar_piloto_oe1.py /home/<usuario>/oe1-trabajo/salidas/piloto-geo-train-06-v0 \
  --out /home/<usuario>/oe1-trabajo/salidas/comparacion-piloto-v0/resumen-piloto.json
```

Pruebas de verificación del script de análisis:

```
python scripts/analysis/test_oe1_pilot_roi.py
```

**Huellas sha-256 citadas en este documento:**

| Archivo | sha-256 |
|---|---|
| `build-A/muography_sim` | `935e8ceca0d4010929d6791c4cf3e78cd0a47d43def96cd3fdbb8bb5d3b8d7b1` |
| `build-B/muography_sim` | `7c5416a90563ec8b17446f1d20ec8986aafb5401d5e833bff36ec512413d41f6` |
| `ejecutar_piloto_oe1.sbatch` | `8178a3b2f377f8f06870eb27088c117a5086d33b524a304b058268bf93732de9` |
| `comparar_piloto_oe1.py` | `16ccee3028bc8233f25ff668b7ebdb9abaa3805a84e6c20e9cacfd718f69fd46` |
| `oe1_pilot_roi.py` (commit `0c8fd33`, con `analyze`) | `5b82b05f997514b20aad61804817c9478ead057fd8f57db070ba2230a5a42468` |
| `oe1_pilot_roi.py` (commit `fa21f57`, pre-registro, sin `analyze`) | `5204191864c83fa09d3107bb9004f2009f83fb9453f779a66dd438cf9bc8435b` |

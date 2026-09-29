# Pre-registro de ROI — geo-train-06, vista 0 (piloto A/B)

## 1. Objetivo

Fijar, antes de ejecutar el piloto comparativo A/B (geometría recibida frente a la corrección B1), las regiones de interés (ROI) y el efecto esperado en cada una, de modo que la interpretación posterior no pueda ajustarse a lo que el piloto termine mostrando. Las ROI se derivan exclusivamente de la geometría (longitudes de recorrido por trazado de rayos), nunca de un umbral sobre las imágenes medidas, para que la máscara no se mueva con el ruido de la corrida. La comparación central es la intersección conducto–cuerpo denso (`R_int`), donde la geometría recibida (variante A) deja el material indefinido y dependiente de la trayectoria de navegación, frente a la corrección B1 (variante B), que asigna el cuerpo denso a esa región.

## 2. Entradas y huellas (sha-256)

| Entrada | Ruta | sha-256 |
|---|---|---|
| Catálogo de geometría | `scripts/simulation/geometry_catalog/geometries/geo-train-06.json` | `c8f6c1352af1f7564356cffbd98e26fd6a5881e5ece15a0ab6f2ed60c8ea26ed` |
| Tabla de normalización de flujo | `scripts/simulation/geant4_app/tables/meta.json` | `7ac4b6a9353af701b56e5a97ee783ed59072d58df52d80ddbdc0f5f70147d35d` |
| Histograma de campaña (geometría recibida, vista 0) | `../muography-thesis/data/campaign-geant4-merged/geo-train-06/geo-train-06_view0_hist.csv` | `78bd394ec73d09a8167d5fd2122386db2778956853c75bdcb54e11d61f33ed14` (idéntica a `hist_sha256` en el `.meta.json` original de esta vista) |
| Script de pre-registro | `scripts/analysis/oe1_pilot_roi.py` | `5204191864c83fa09d3107bb9004f2009f83fb9453f779a66dd438cf9bc8435b` |

Los valores exactos de sha-256, junto con la versión de Python y de NumPy usadas, quedan en el bloque `metadata` de `roi-preregistro.json` (fuente autoritativa; esta tabla es un resumen). Todas las salidas de este documento (`roi-preregistro.json`/`.npz`/`.png`, `registro-orientacion.json`/`.png` y `registro-orientacion-suma.json`/`.png`, esta última nueva, ver sección 5.2) fueron regeneradas con esta versión final del script, que incorpora los subcomandos `registration` y `registration-sum`; frente a su primera generación solo cambian `metadata.generated_utc` y `metadata.script_sha256` en los tres JSON — los arreglos de `roi-mascaras.npz` y los tres PNG son idénticos byte a byte.

Geometría: cono de radio de base 509,7 m, altura 416,3 m, roca 2,65 g/cm³; conducto (anomalía 0, ρ = 1,832 g/cm³, centro (20,3; −24,5) m, radio 21 m, z 0–340 m); cuerpo denso (anomalía 1, ρ = 3,285 g/cm³, centro (32,2; −74,1; 137,8) m, semiejes 72,9/61,6/64,6 m). Vista 0: detector en (1000; 0; 1,5) m, mirando hacia el eje del cono.

## 3. Definición de las cinco ROI

Recorrido único por rayo (misma rejilla angular, mismas direcciones y misma ventana marchada que `imaging.opacity_map`; ver `scripts/simulation/surrogate/imaging.py` y `scripts/evaluation/roi.py`). Para cada píxel se descompone la longitud de recorrido dentro del cono en cuatro categorías disjuntas: dentro de ambos sólidos (`L_int`), dentro del conducto exclusivamente (`L_cond`), dentro del cuerpo denso exclusivamente (`L_body`) y roca sin anomalía (`L_rock_solo`); `L_cono` es la cuerda total dentro del cono. Umbral de longitud mínima: `min-path-m = 20,0 m` (10 pasos de marcha de 2,0 m). Las cinco máscaras se construyen por prioridad estricta, de modo que son disjuntas por construcción:

| ROI | Regla | Píxeles |
|---|---|---|
| `R_int` | `L_int ≥ 20,0 m` | 195 |
| `R_cond` | no `R_int`; `L_cond ≥ 20,0 m` | 769 |
| `R_body` | no `R_int`, no `R_cond`; `L_body ≥ 20,0 m` | 830 |
| `R_rock` (control) | `L_cono ≥ 20,0 m` y (`L_int`+`L_cond`+`L_body`) `< 1,0 m` | 12 849 |
| `R_sky` (control) | `L_cono = 0` | 50 842 |

Sobre 65 536 píxeles de la vista (256×256), 51 quedan sin clasificar (recorrido de anomalía presente pero por debajo del umbral, o recorrido total de roca por debajo de 20 m sin ser cielo); no forman parte de ninguna ROI ni afectan la comparación.

## 4. Campos de material y efecto esperado

Sobre el mismo recorrido se evalúan tres campos de densidad, cambiando solo la asignación en la región de solape y en las dos regiones exclusivas:

- **B1** — el cuerpo denso ocupa el solape (ρ = 3,285 g/cm³). Es la misma regla que ya aplica el motor analítico (índice posterior gana) y coincide con lo que devuelve la sonda estática de Geant4 en el centroide del solape de la geometría recibida, por lo que es el mejor sustituto analítico disponible de lo que mide realmente la variante A.
- **conduit-wins** — el conducto ocupa el solape (ρ = 1,832 g/cm³). No es una corrección propuesta: es la envolvente superior de lo que la variante A podría llegar a resolver en cualquier punto del solape, dado que el material ahí es indeterminado.
- **homogeneous** — sin anomalías, solo roca. Referencia para el control cielo/roca.

Se verificó que el campo B1, reconstruido por la descomposición de longitudes de este script, reproduce `imaging.opacity_map(geo, vista)` con una diferencia máxima de 8,7×10⁻¹¹ g/cm² (consistencia numérica, no una comparación física adicional).

**Conteos esperados por 10⁶ eventos** (mapa lambda del motor surrogate, normalizado por el flujo de cielo abierto S0 = 36 175 379,9 muones/vista/30 d, escalado por el factor `conteo_detectado_campaña / Σλ_B1` = 27 209 253 / 34 480 336,7 = **0,7891** — corrección aproximada de la integral de flujo idealizada del surrogate a la escala detectada por Geant4; ver limitaciones):

| ROI | B1 | conduit-wins | Δ_max = B1 − conduit-wins | EE Poisson por corrida | EE previsto media 3 semillas | \|Δ_max\|/EE |
|---|---|---|---|---|---|---|
| `R_int` | 1,1169 | 1,2103 | **−0,0933** | 1,0569 | 0,8629 | **0,108** |
| `R_cond` | 15,8714 | 15,8741 | −0,0028 | 3,9839 | 3,2528 | 0,0009 |
| `R_body` | 5,3341 | 5,3348 | −0,0007 | 2,3096 | 1,8858 | 0,0004 |
| `R_rock` (control) | 722,2230 | 722,2230 | 0,0000 | 26,8742 | 21,9427 | 0,0000 |
| `R_sky` (control) | 751 338,07 | 751 338,07 | 0,0000 | 866,80 | 707,74 | 0,0000 |

El signo es consistente en toda la tabla: el material más denso (B1) siempre predice menos o igual cantidad de conteos que el conducto ganando el solape, nunca más. Los controles `R_rock` y `R_sky` muestran Δ_max exactamente 0 (ninguno de los dos campos difiere fuera de las regiones de anomalía), lo cual es la verificación de que el procedimiento no introduce diferencias espurias.

`EE previsto media 3 semillas` = `sqrt(2·N/3)` con `N` = conteo esperado bajo B1 por corrida, asumiendo Poisson independiente entre A y B en cada semilla (protocolo fijado antes del piloto real, con 3 semillas: 2026092801/02/03).

**Lectura del cociente `|Δ_max|/EE` en `R_int` (0,108):** el efecto máximo posible entre las dos hipótesis extremas (B1 frente a conduit-wins) es casi diez veces menor que el error estándar previsto de la media de 3 corridas de 1 000 000 de eventos. Esto significa que, con la estadística planeada, el piloto muy probablemente NO podrá distinguir estadísticamente la geometría recibida (A) de la corregida (B) en `R_int` a partir del ruido de conteo solo. Esta conclusión se deja registrada aquí, antes del piloto, precisamente para que no se sobreinterprete un resultado nulo del piloto como si demostrara equivalencia entre A y B.

## 5. Comprobación de registro de píxeles

**Correlación campaña–esperado** (log1p de conteos, píxeles con esperado > 0, sobre los 65 536 píxeles de la vista):

| Campo | orientación real | espejo en azimut | espejo en elevación |
|---|---|---|---|
| B1 | 0,987883 | 0,987884 (z = −0,734) | −0,543427 (z = 455,89) |
| conduit-wins | 0,987880 | 0,987882 (z = −1,134) | −0,543434 (z = 455,87) |
| homogeneous | 0,987835 | 0,987835 (z = 0,000) | −0,543442 (z = 455,60) |

`z` es el estadístico de Steiger (1980) para dos correlaciones **dependientes** que comparten una variable (el vector de campaña): la correlación real y la del espejo no provienen de muestras independientes, sino del mismo vector de campaña correlacionado con dos mapas esperados que a su vez están altamente correlacionados entre sí (`r12(mapa real, mapa espejado en azimut) = 0,999996`; `r12(mapa real, mapa espejado en elevación) = −0,559`, para el campo B1). Por eso `z` se calcula con la covarianza asintótica de las dos transformadas de Fisher (Steiger, 1980, ec. 3; Cohen y Cohen, 1983, cap. 3), no con la fórmula de dos muestras independientes (`SE = sqrt(2/(n−3))`), que subestimaría la varianza real al ignorar que ambas correlaciones comparten la misma muestra. Umbral de decisión: |z| > 3. **Elevación: resuelta** — la orientación real supera al espejo por más de 455 desviaciones estándar; invertir el eje de elevación produce una correlación negativa, claramente peor. **Azimut: inconcluyente** — la correlación real y la del espejo en azimut son indistinguibles (|z| < 1,2) en los tres campos, incluyendo el campo homogéneo, donde ambas son *exactamente* iguales. Esto no es un defecto del registro: el edificio es un cono centrado en el eje de mira, simétrico en azimut salvo por el conducto y el cuerpo denso, que ocupan menos del 3 % de los píxeles de la vista; una correlación global sobre el mapa completo no tiene poder estadístico para distinguir el azimut correcto del espejado cuando la asimetría solo la aporta una región tan pequeña.

El registro de píxeles en azimut y elevación está garantizado, independientemente de esta prueba estadística, por la equivalencia exacta de la fórmula de binning: tanto la rejilla angular del surrogate (`angular_grid` en `scripts/simulation/surrogate/imaging.py`) como el histograma de Geant4 (`binIndex`, `scripts/simulation/geant4_app/src/SteppingAction.cc`, líneas 22–58) usan la convención de centros de `numpy.linspace(mín, máx, N)` sobre los mismos límites (`az_half`, `el_min`, `el_max`) y el mismo azimut relativo a la dirección de mira. La prueba de correlación es una verificación estadística adicional, no la única evidencia de registro; para el azimut es, por construcción geométrica, inconcluyente y se reporta como tal en vez de forzarla a "aprobada". Las secciones 5.1 y 5.2 documentan dos intentos independientes de dar poder estadístico a esta verificación mediante geometrías con anomalías fuera de eje; ambos concluyen igualmente en NO RESUELTO, sin que ninguno altere las ROI ni los números pre-registrados en las secciones 3–5.

**Control cielo/roca** (conteos de campaña por evento, dividido por S0): media en `R_sky` = 1,473×10⁻⁵; media en `R_rock` = 2,249×10⁻⁷ (razón ≈ 65×, cielo claramente mayor, como se espera de un control sin absorción frente a un control con roca homogénea).

**Cociente campaña/esperado por ROI** (conteo de campaña ÷ Σλ_B1, ambos sobre 30 días, sin aplicar el factor de escala global): `R_sky` = 0,787 (coincide con el factor de escala global 0,789, esperado porque el cielo domina el total de la vista); `R_rock` = 3,16; `R_cond` = 3,73; `R_body` = 2,50; `R_int` = 1,91. El surrogate subestima sistemáticamente el conteo de Geant4 en las regiones de roca profunda y de anomalía (razón 1,9–3,7) frente a las regiones de cielo abierto (razón ≈ 0,79); ver limitaciones.

## 5.1 Verificación empírica del azimut entre geometrías (unidad U8b)

La sección 5 dejó el azimut de `geo-train-06` **inconcluyente** (|z| < 1,2 en los tres campos), no porque el registro de píxeles esté en duda, sino porque el cono es axisimétrico en azimut salvo por el conducto y el cuerpo denso, que cubren menos del 3 % de los píxeles de la vista: una correlación global sobre las 65 536 celdas no tiene poder estadístico para separar la orientación correcta de su espejo cuando la asimetría la aporta una región tan pequeña. Antes de dar por buenas las ROI de `geo-train-06` para el piloto, esta sección somete el registro en azimut a una verificación **empírica independiente**, usando geometrías del catálogo con una cavidad fuera de eje (densidad 0,068–0,464 g/cm³, radio 27,9–48,0 m en las 5 geometrías finalmente usadas), cuyo defecto de conteo unilateral es justamente el tipo de asimetría capaz de romper la simetría axial y dar poder estadístico a la prueba.

**Geometrías y vistas usadas.** Únicamente geometrías de entrenamiento/validación (nunca `geo-test-*` ni `geo-gen-*`), excluyendo `geo-train-06` (es el caso bajo prueba) y `geo-train-11`/`geo-train-08` (sus anomalías, aunque también incluyen cavidades fuera de eje, están lo bastante cerca entre sí en 3D como para que cuál "gana" un punto compartido sea ambiguo bajo la regla de prioridad secuencial — la misma clase de ambigüedad que la unidad U8 diagnosticó para `geo-train-06`, que haría que un único campo de opacidad analítico no fuera un sustituto inequívoco de lo transportado por Geant4 ahí). Se comprobó que ninguna de las cinco geometrías elegidas tiene ese problema (distancia 3D entre centros mayor que la suma de radios en todos los pares de anomalías):

| Geometría | Anomalías | Cavidad fuera de eje |
|---|---|---|
| `geo-train-03` | cavidad | ρ = 0,267 g/cm³, radio 35,8 m, centro (−10,3; −95,3) m |
| `geo-train-05` | conducto + cavidad | ρ = 0,335 g/cm³, radio 29,4 m, centro (−69,0; 24,0) m |
| `geo-train-07` | cavidad + cuerpo denso | ρ = 0,169 g/cm³, radio 48,0 m, centro (−27,7; −140,1) m |
| `geo-train-10` | cavidad + cavidad | ρ = 0,464/0,068 g/cm³, radios 27,9/45,7 m |
| `geo-val-02` | cavidad | ρ = 0,208 g/cm³, radio 38,8 m, centro (121,6; 54,6) m |

Se evaluaron las 6 vistas de cada geometría (30 casos geometría×vista), contra el histograma de campaña Geant4 de la misma campaña de entrenamiento (geometría recibida, 30 d, ≈3,6×10⁷ eventos/vista).

**Método.** Por cada (geometría, vista): mapa esperado con el motor analítico para las anomalías propias de la geometría (`imaging.opacity_map`, reutilizado sin cambios) y para el cono homogéneo sin anomalías (nueva función `homogeneous_opacity_map`, que solo reutiliza `roi.rock_path_length`/`roi._march_window`, sin repetir la marcha de rayos). Residuo del modelo `m = log(E_anom / E_homog)`; residuo de campaña `c = log((C + 0,5) / (s·E_homog))` con `s = ΣC / ΣE_anom` sobre los píxeles evaluados. Píxeles evaluados: `E_homog > 0`, dentro de la huella del cono, y `C ≥ 20` conteos de campaña (umbral por defecto). `r_verdadero = corr(c, m)`; `r_espejo = corr(c, m espejado en azimut)`; `z` de Steiger (misma prueba de correlaciones dependientes de la sección 5, con `r12 = corr(m, m_espejo)`); bootstrap por bloques de píxel (16×16, 2 000 remuestreos, semilla por caso derivada de forma determinista de la semilla base 20260929 y del par (geometría, vista) mismo —no de su posición en la lista pedida—, de modo que el IC de cada caso es reproducible por separado) de `Δr = r_verdadero − r_espejo`, con intervalo de confianza (IC) del 95 % por percentiles; `tamaño de señal` = número de píxeles evaluados con `|m| > 0,05`. Se repite el mismo cálculo espejando en **elevación** como control positivo (el eje ya resuelto por la sección 5).

**Criterio fijado antes de calcular** (constante `REGISTRATION_CRITERION`, escrita en `registro-orientacion.json` antes de computar cualquier caso): el azimut se declara **CONFIRMADO** si TODO caso con `tamaño de señal ≥ 50` tiene `Δr > 0` con IC 95 % que excluye 0, y ningún caso evaluado (de cualquier tamaño de señal) tiene `Δr < 0` con IC que excluye 0; **CONTRADICHO** si algún caso tiene `Δr < 0` con IC que excluye 0; **NO RESUELTO** en cualquier otro caso. El script termina con código de salida distinto de cero solo si el veredicto es CONTRADICHO.

**Resultado por caso** (`n` = píxeles evaluados; señal = píxeles con `|m| > 0,05`; `Δr = r_verdadero − r_espejo`; IC 95 % por bootstrap de bloques):

| Geometría | Vista | n | Señal | Δr | IC 95 % | z (Steiger) |
|---|---|---|---|---|---|---|
| geo-train-03 | 0 | 1 176 | 0 | 0,0000 | [0,0000; 0,0000] | 0,000 |
| geo-train-03 | 1 | 1 189 | 0 | 0,0000 | [0,0000; 0,0000] | 0,000 |
| geo-train-03 | 2 | 1 182 | 0 | 0,0000 | [0,0000; 0,0000] | 0,000 |
| geo-train-03 | 3 | 1 182 | 0 | 0,0000 | [0,0000; 0,0000] | 0,000 |
| geo-train-03 | 4 | 1 182 | 0 | 0,0000 | [0,0000; 0,0000] | 0,000 |
| geo-train-03 | 5 | 1 170 | 0 | 0,0000 | [0,0000; 0,0000] | 0,000 |
| geo-train-05 | 0 | 1 366 | 13 | −0,0174 | [−0,1918; 0,1646] | −0,459 |
| geo-train-05 | 1 | 1 346 | 20 | 0,0090 | [−0,0953; 0,0975] | 0,283 |
| geo-train-05 | 2 | 1 360 | 24 | 0,0113 | [−0,0315; 0,0541] | 0,520 |
| geo-train-05 | 3 | 1 362 | 14 | −0,0090 | [−0,1347; 0,1201] | −0,240 |
| geo-train-05 | 4 | 1 359 | 5 | −0,0112 | [−0,0740; 0,0368] | −0,483 |
| geo-train-05 | 5 | 1 363 | 1 | −0,0155 | [−0,0584; 0,0368] | −0,670 |
| geo-train-07 | 0–5 | 2 044–2 094 | 0 | 0,0000 | [0,0000; 0,0000] | 0,000 |
| geo-train-10 | 0–5 | 2 119–2 175 | 0 | 0,0000 | [0,0000; 0,0000] | 0,000 |
| geo-val-02 | 0–5 | 1 458–1 481 | 0 | 0,0000 | [0,0000; 0,0000] | 0,000 |

(Las filas `geo-train-07`, `geo-train-10` y `geo-val-02` están colapsadas por vista porque las seis dan `Δr = 0,0000` y señal = 0 exactamente: la tabla completa, caso por caso, está en `registro-orientacion.json`, campo `per_case`.)

**Por qué la señal es prácticamente nula.** El residuo del modelo `m` sí tiene variación real y sustancial (hasta 0,35 en valor absoluto, ~500 píxeles con `|m| > 0,05` sobre la huella completa del cono en varios casos) allí donde el rayo atraviesa la cavidad — pero esos píxeles quedan casi siempre del lado equivocado del filtro `C ≥ 20`: son precisamente los más opacos (recorrido de roca profundo, cientos de metros), con tan pocos muones detectados en 30 días que el conteo de campaña ahí es 0 o casi 0. El filtro de conteo mínimo, necesario para que el residuo de campaña no sea puro ruido de Poisson de un solo conteo, termina reteniendo sobre todo píxeles cercanos al borde de la silueta (donde el conteo es alto mientras que el efecto de la anomalía, profunda, todavía es pequeño). El caso con más señal, `geo-train-05` vista 2 (conducto **y** cavidad, 24 píxeles de señal), es también el único cuyo IC 95 % se acerca a excluir 0 por el lado positivo (límite inferior −0,0315), sin lograrlo.

**Control positivo de elevación.** Repetido con el mismo umbral `C ≥ 20`, este control da resultados igualmente poco concluyentes para la mayoría de los casos (IC 95 % que siempre incluye 0), y resultados exactamente `Δr = NaN` (sin variación del residuo del modelo dentro del conjunto evaluado) para `geo-train-03` y `geo-val-02`: en esas dos geometrías, los píxeles que pasan el filtro de conteo caen en un rango de elevación bajo (filas ≈ 8–99 de 256) cuyo espejo en elevación cae enteramente en cielo abierto (`L_roca = 0`), donde `m ≡ 0` por construcción tanto en la orientación real como en la espejada. Esto no es un defecto del control ni del código — es la misma clase de límite de potencia estadística que afecta al azimut, aplicado aquí al eje ya resuelto por la sección 5 con una prueba de correlación global sobre las 65 536 celdas (que sí incluye el fuerte gradiente cielo/roca en elevación); confirma que la ausencia de señal significativa en esta subsección es un problema de **potencia de esta verificación concreta**, no evidencia en contra del modelo ni del registro de píxeles.

**Veredicto: NO RESUELTO** (`azimuth_verdict.verdict = "UNRESOLVED"` en `registro-orientacion.json`). De los 30 casos evaluados, ninguno alcanza el umbral de tamaño de señal (`≥ 50` píxeles; el máximo observado es 24, en `geo-train-05` vista 2), de modo que ningún caso califica para la barra de CONFIRMADO; y ningún caso tiene `Δr < 0` con IC que excluya 0, de modo que tampoco hay CONTRADICCIÓN. El script terminó con código de salida 0.

**Qué implica para las ROI pre-registradas.** Ninguna. Este resultado **no confirma ni refuta** el registro en azimut, y por lo tanto **no se altera ninguna definición de ROI** de la sección 3 ni ningún número de las secciones 4–5 de este documento: siguen fijados exactamente como se pre-registraron. El registro de píxeles en azimut sigue apoyándose, como ya establecía la sección 5, en la equivalencia exacta a nivel de código entre `angular_grid`/`ray_directions` (surrogate) y `binIndex` (Geant4) — la única evidencia de registro en azimut disponible hasta ahora sigue siendo esa equivalencia de código, no una confirmación estadística independiente; esta unidad (U8b) intentó honestamente producir esa segunda evidencia y, con las 19 geometrías y la estadística de 30 días disponibles, no lo logró ni en un sentido ni en otro. La sección 5.2 (unidad U8c) documenta un segundo intento, con un diseño estadístico distinto (suma de conteos sobre regiones en vez de correlación píxel a píxel) pensado específicamente para superar la limitación de potencia diagnosticada aquí; su resultado es igualmente NO RESUELTO, de modo que la conclusión de este párrafo se mantiene sin cambios tras dos intentos independientes.

**Reproducción:**

```
python scripts/analysis/oe1_pilot_roi.py registration \
  --campaign-dir ../muography-thesis/data/campaign-geant4-merged \
  --out-dir muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/analisis
```

ejecutado desde la raíz del repositorio `muography-dl-reconstruction`, con los valores por defecto: geometrías `geo-train-03 geo-train-05 geo-train-07 geo-train-10 geo-val-02`, vistas 0–5, `min-counts = 20`, `block = 16`, `bootstrap = 2000`, `seed = 20260929` (semilla base; cada caso usa además su propia sub-semilla determinista, ver método arriba). Sha-256 del script (con los subcomandos `registration` y `registration-sum` ya incorporados): `5204191864c83fa09d3107bb9004f2009f83fb9453f779a66dd438cf9bc8435b`. Salidas: `registro-orientacion.json` (criterio, los 30 casos con precisión completa —incluida la sub-semilla efectiva de cada uno—, veredicto, huellas sha-256 de cada geometría y cada histograma de campaña usados) y `registro-orientacion.png` (residuo de campaña, residuo del modelo en orientación real y residuo del modelo espejado en azimut, misma escala de color, para `geo-train-05` vista 2 — el caso de mayor señal). Pruebas de verificación: `python scripts/analysis/test_oe1_pilot_roi.py` (incluye dos pruebas sintéticas del bootstrap por bloques y del veredicto: una orientación verdadera que debe dar CONFIRMADO y una espejada que debe dar CONTRADICHO).

## 5.2 Verificación del azimut por suma de conteos en regiones (U8c)

**Motivación.** La sección 5.1 (unidad U8b) quedó limitada por potencia estadística: el filtro de conteo mínimo por píxel (`C ≥ 20`), necesario para que el residuo de campaña no fuera puro ruido de Poisson de un solo conteo, retiene sobre todo píxeles cercanos al borde de la silueta, donde el conteo es alto pero el efecto de la anomalía, profunda, todavía es pequeño, y descarta los píxeles de mayor residuo del modelo (`|m|` hasta 0,35), que caen en zonas de recorrido de roca profundo con conteo de campaña bajo o nulo. El caso con más señal de los 30 evaluados, `geo-train-05` vista 2, alcanzó solo 24 píxeles con `|m| > 0,05`, por debajo del umbral de 50 fijado para que un caso califique hacia CONFIRMADO. Esta unidad (U8c) reemplaza la correlación píxel a píxel por una suma de conteos de campaña sobre regiones completas, estadístico que no depende de un filtro de conteo mínimo por píxel y por lo tanto conserva la contribución de los píxeles profundos que la sección 5.1 tuvo que descartar.

**Geometrías y vistas.** A diferencia de la sección 5.1 (que filtró a 5 geometrías con cavidad fuera de eje para maximizar la señal de una correlación píxel a píxel), esta unidad usa las 12 geometrías de entrenamiento/validación disponibles (`geo-train-01, 02, 03, 04, 05, 07, 09, 10, 12, geo-val-01, 02, 03`), excluyendo únicamente `geo-train-06` (el caso bajo prueba) y `geo-train-08`/`geo-train-11` por la misma ambigüedad de solape entre anomalías diagnosticada en la sección 5.1, ya que el estadístico de suma de regiones no depende de que la anomalía esté fuera de eje. Se evalúan las 6 vistas de cada una (72 casos geometría×vista), contra el histograma de campaña Geant4 de la geometría recibida (30 d).

**Método.** Por cada (geometría, vista) se calcula el residuo del modelo `m = log(E_anom/E_homog)` (mismo par de mapas que la sección 5.1). Sobre `m` se definen, por prioridad y exclusión mutua con su espejo en azimut `s` (columna `j → N_az−1−j`): región de exceso `S = {m(p) > 0,05, |m(s(p))| < 0,01, no flip(p)}` y región de déficit `D = {m(p) < −0,05, |m(s(p))| < 0,01, no flip(p)}`, con mirrors `S' = s(S)`, `D' = s(D)`; `flip(p)` es la máscara de píxeles excluidos por la compuerta de simetría (ver "Enmienda" más abajo). Estadístico por sub-prueba: `k` = conteo de campaña sumado sobre la región (`S` o `D`); `N` = conteo de campaña sumado sobre la unión región∪espejo; sub-prueba elegible si `N ≥ 100` (umbral fijado antes de calcular, independiente del sentido del desequilibrio). `z = (k − N/2)/√(N/4)`; `z_s` = `+z` para una sub-prueba de exceso y `−z` para una de déficit, de modo que `z_s > 0` significa que el desequilibrio apunta en el sentido que predice el registro a nivel de código. Combinación: `Z` de Stouffer = `Σz_s/√n` sobre las sub-pruebas elegibles (asumidas independientes por provenir de geometrías/vistas distintas). Control nulo: cada par (región, espejo) de cada sub-prueba elegible se reevalúa sobre el mapa de campaña de la misma vista de cada otra geometría cuyo propio residuo del modelo cumpla `|m| < 0,01` en toda la unión (para no mezclar una anomalía real de esa geometría con el control), dando `z_null` con la misma fórmula no firmada, solo si esa geometría también cumple `N ≥ 100`; se combinan en `Z_null` (Stouffer) y se reporta además `máx|z_null|`, porque las evaluaciones nulas reutilizan los mismos mapas de campaña en varios pares de región y no son independientes entre sí.

**Criterio fijado antes de calcular** (constante `REGISTRATION_SUM_CRITERION` en `registro-orientacion-suma.json`, campo `criterion`): **CONFIRMADO** si al menos una sub-prueba es elegible, el control nulo pasa (`|Z_null| < 3` y `máx|z_null| < 4`), `Z ≥ 3` y ninguna sub-prueba elegible tiene `z_s ≤ −3`; **CONTRADICHO** si el control nulo pasa y `Z ≤ −3`; **NO RESUELTO** si ninguna sub-prueba es elegible, o el control nulo falla (`|Z_null| ≥ 3` o `máx|z_null| ≥ 4`), o no se cumple ni la condición de CONFIRMADO ni la de CONTRADICHO. El script termina con código de salida distinto de cero solo si el veredicto es CONTRADICHO.

**Enmienda a la compuerta de simetría (fijada antes de calcular cualquier suma de regiones).** El primer intento de ejecución (`registro-orientacion-suma-intento-1.log`, iniciado 2026-09-29T09:31:00Z) se detuvo en la compuerta de simetría original —de punto flotante, tolerancia 1,0×10⁻⁹— sin haber calculado ninguna suma de región: el mapa homogéneo (`L`, longitud de recorrido en roca sin anomalías) no era exactamente simétrico en azimut en las vistas oblicuas 1, 2, 4 y 5, con una diferencia relativa máxima de 9,154×10⁻³ (`geo-train-12` vista 1, entre otros casos listados en el log). El diagnóstico, hecho antes de tocar el criterio o de calcular ninguna suma, fue que solo un número muy pequeño de píxeles por caso (p. ej. 2 de 65 536 en `geo-train-12` vista 1) tienen un recorrido de roca que difiere de su espejo en exactamente un paso de marcha de rayos (`RAY_STEP_M = 2,0 m`): un cruce de punto flotante en el muestreo de la superficie del cono (float32) que solo ocurre en vistas oblicuas (las vistas 0 y 3 son exactamente simétricas). Documentado en el campo `criterion.amendment` de `registro-orientacion-suma.json`, la compuerta se enmendó para aceptar únicamente diferencias que sean múltiplos exactos del paso de marcha (dentro de 1,0×10⁻⁶ del entero más cercano) en, como máximo, el 0,1 % de los píxeles de la huella del cono; esos píxeles (`flip(p)`) se excluyen de toda región y de su espejo, y se exige simetría exacta del resto. Con la compuerta enmendada, las 72 combinaciones geometría×vista pasan (`symmetry_check.n_cases_failing_gate = 0`, `max_rel_diff_after_exclusion` = 0 en todos los casos).

**Resultado por geometría** (`n` sub-pruebas elegibles agrupa exceso y déficit de las 6 vistas; `z_s` mín/máx sobre esas sub-pruebas; `Σk`/`ΣN` = suma de conteos de campaña en la región / en región∪espejo, sobre las sub-pruebas elegibles de esa geometría; detalle completo por sub-prueba —incluidos `p_model` y el valor p binomial exacto— en `registro-orientacion-suma.json`, campos `eligible_subtests_summary` y `per_case`):

| Geometría | Sub-pruebas elegibles | `z_s` mín | `z_s` máx | Σk | ΣN |
|---|---|---|---|---|---|
| `geo-train-01` | 0 | — | — | — | — |
| `geo-train-02` | 6 | −2,277 | 1,807 | 3 324 | 6 772 |
| `geo-train-03` | 6 | −1,190 | 2,058 | 636 | 1 297 |
| `geo-train-04` | 6 | −1,034 | 0,344 | 2 446 | 4 828 |
| `geo-train-05` | 6 | −1,290 | 1,609 | 9 804 | 19 536 |
| `geo-train-07` | 9 | −0,633 | 1,448 | 2 300 | 4 494 |
| `geo-train-09` | 6 | −2,219 | 0,875 | 7 864 | 15 911 |
| `geo-train-10` | 6 | −0,282 | 1,177 | 5 592 | 11 081 |
| `geo-train-12` | 6 | −0,796 | 0,164 | 779 | 1 531 |
| `geo-val-01` | 6 | 0,370 | 1,688 | 7 216 | 14 081 |
| `geo-val-02` | 6 | −0,615 | 1,707 | 1 657 | 3 214 |
| `geo-val-03` | 6 | 0,000 | 2,095 | 15 602 | 31 007 |
| **Total** | **69** | | | | |

`geo-train-01` no aporta sub-pruebas elegibles: en sus 6 vistas, ningún píxel satisface la definición de `S` o `D` (residuo del modelo por debajo de los umbrales `t`/`t0` en toda la huella), no porque `N` sea insuficiente. De las 144 sub-pruebas posibles (72 casos × 2 tipos), 68 no tienen región definida (como en `geo-train-01`) y 7 adicionales tienen región pero `N < 100` (no elegibles); las 69 restantes son las de la tabla.

**Combinación y control nulo** (`registro-orientacion-suma.json`, campo `combination`): `Z = 1,292` sobre las 69 sub-pruebas elegibles; control nulo sobre 334 evaluaciones, `Z_null = 1,481`, `máx|z_null| = 3,224` (por debajo de los umbrales 3 y 4 — el control nulo pasa).

**Veredicto: NO RESUELTO** (`verdict.verdict = "UNRESOLVED"`, razón registrada: `"combined Z is between the confirmation and contradiction thresholds"`). El control nulo pasa y ninguna sub-prueba elegible tiene `z_s ≤ −3`, pero `Z = 1,292` no alcanza el umbral `Z ≥ 3` de CONFIRMADO. El script terminó con código de salida 0.

**Observación exploratoria, no prerregistrada.** Cada sub-prueba elegible registra también `p_model = E_anom(S)/(E_anom(S) + E_anom(S'))` (análogamente con `D`/`D'`), la fracción de energía-modelo que el motor analítico asigna a la región frente a su espejo bajo la orientación correcta; este campo es contexto y nunca interviene en el veredicto. La asimetría que el modelo predice, con la misma convención de signo que `z_s` (positivo en `S`, negativo en `D`), es `z_esperado = ±2(p_model − 0,5)√N`, calculado aquí para las 69 sub-pruebas elegibles a partir de `per_case[*].subtests.{excess,deficit}.{p_model,N}`. Su combinación de Stouffer es `Σz_esperado/√69 = 16,44` (mediana 1,50, máximo 6,42), muy por encima del umbral 3 — el modelo analítico, sin ruido, predice una asimetría fuerte y sistemática en la dirección del registro correcto. Definiendo, para cada sub-prueba, la versión "orientada" `k_ef` (= `k` en exceso, `N−k` en déficit) y `p_ef` (= `p_model` en exceso, `1−p_model` en déficit) para que ambas queden siempre en el sentido que predice el registro: la razón observada agrupada es `Σk_ef/Σ(N−k_ef) = 1,010` (cociente de conteo de campaña `C(S)/C(S')`, agrupando también los casos de déficit en la misma convención), frente a `Σ(p_ef·N)/ΣN = 0,5268` de probabilidad-modelo ponderada por `N`, es decir una razón predicha `p̄/(1−p̄) = 1,113`. El control nulo pasa (sección anterior), por lo que los datos rechazan tanto la magnitud de la asimetría predicha por el modelo en la dirección esperada (~15 desviaciones estándar por debajo de `Z_esperado = 16,44`) como una asimetría en el sentido contrario: la asimetría inducida por la anomalía en estos mapas de campaña de Geant4 es, aproximadamente, un orden de magnitud más débil que la que predice el modelo analítico de trazado recto en estas regiones. La causa **no** está establecida. Una hipótesis compatible con los hechos conocidos, sin más evidencia que la aquí presentada: los histogramas de Geant4 clasifican muones por dirección de **llegada** sobre un plano de conteo de 600×600 m (`kScoringHalfM` en `scripts/simulation/geant4_app/src/DetectorConstruction.cc`; los primarios se inyectan hacia el panel real de 1,2 m, `PrimaryGeneratorAction.cc`), de modo que la dispersión múltiple traslada muones de direcciones de baja opacidad hacia bins de alta opacidad; la sección 5 ya midió razones de conteo campaña/modelo de 1,9–3,7 en las ROI de roca profunda y anomalía frente a 0,79 en cielo abierto, y ese exceso de conteo "filtrado" diluiría el contraste relativo de anomalías profundas. El modelo analítico no tiene dispersión (ya listado como limitación en la sección 8). Esto se presenta únicamente como hipótesis, no como hallazgo establecido.

**Consecuencias.** Las definiciones de ROI y todos los números de las secciones 3–5 se mantienen exactamente como se pre-registraron. El registro en azimut sigue apoyado, como evidencia primaria, en la equivalencia exacta de código entre `angular_grid`/`ray_directions` (surrogate) y `binIndex` (Geant4); ni la sección 5.1 ni esta sección aportan una confirmación o refutación estadística independiente. El efecto máximo esperado `Δ_max` de la sección 4 se calculó con el motor analítico sin dispersión, y la discrepancia de contraste modelo-versus-Geant4 documentada arriba sugiere que ese `Δ_max` es, si acaso, una sobreestimación del efecto real esperado en Geant4 — lo cual refuerza, no cambia, la expectativa ya pre-registrada de que el piloto de 10⁶ eventos no tendrá potencia para resolver el efecto de `R_int` (sección 4, cociente `|Δ_max|/EE = 0,108`). La discrepancia de contraste modelo-Geant4 queda como un problema abierto de OE1, fuera del alcance de esta entrega.

**Reproducción:**

```
python scripts/analysis/oe1_pilot_roi.py registration-sum \
  --campaign-dir ../muography-thesis/data/campaign-geant4-merged \
  --out-dir muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/analisis
```

ejecutado desde la raíz del repositorio `muography-dl-reconstruction`, con los valores por defecto: las 12 geometrías listadas arriba (auto-descubiertas, excluyendo `geo-train-06/08/11`), vistas 0–5, `min-n-per-subtest = 100`, umbrales `t = 0,05`, `t0 = 0,01`. Sha-256 del script: `5204191864c83fa09d3107bb9004f2009f83fb9453f779a66dd438cf9bc8435b`. Salidas: `registro-orientacion-suma.json` (criterio con su enmienda, compuerta de simetría por caso, las 69 sub-pruebas elegibles y las 334 evaluaciones nulas con precisión completa, combinación y veredicto, huellas sha-256 de entrada) y `registro-orientacion-suma.png`. Pruebas de verificación: `python scripts/analysis/test_oe1_pilot_roi.py` (incluye pruebas sintéticas específicas de esta unidad: confirmación con orientación verdadera, contradicción con campaña espejada, NO RESUELTO sin anomalía, disyunción y simetría-espejo de las regiones, sub-prueba no elegible por debajo de `N` mínimo, la compuerta de simetría aceptando cruces de un paso exacto y rechazando diferencias que no son múltiplo del paso, y el control nulo de simetría anulando un CONFIRMADO espurio).

## 6. Plan de análisis fijado antes del piloto

1. Por cada ROI (`R_int`, `R_cond`, `R_body`, `R_rock`, `R_sky`) y cada semilla (2026092801/02/03), calcular el conteo total dentro de la máscara para la corrida A (geometría recibida) y para la corrida B (corrección B1), a partir de `geo-train-06_view0_hist.csv` de cada corrida del piloto.
2. Calcular la diferencia emparejada por semilla `D_s = conteo_B,s − conteo_A,s` en cada ROI (signo: negativo si B1/la corrección reduce el conteo frente a lo recibido, consistente con el signo de `Δ_max` de la sección 4).
3. Calcular la media de las 3 diferencias, la desviación estándar entre réplicas y el error estándar de la media (`SD / sqrt(3)`).
4. Comparar la media observada y su error estándar contra `Δ_max` de la sección 4 (el efecto máximo posible bajo las dos hipótesis extremas del material del solape).
5. Verificar los controles `R_rock` y `R_sky`: la diferencia emparejada ahí debe ser compatible con 0 dentro de su propio error estándar; si no lo es, el procedimiento (no la hipótesis del solape) está introduciendo una diferencia espuria y el resultado en `R_int`/`R_cond`/`R_body` no es interpretable hasta resolverlo.
6. Producir, para cada semilla y para el promedio, el mapa de conteos por evento de A y de B y el mapa de diferencia firmada (B − A), con las cinco máscaras superpuestas.

## 7. Criterios de interpretación

No hay umbral automático de aceptación en el sentido de una decisión binaria "el piloto confirma/descarta la corrección"; sí hay, para eliminar el margen de ajuste posterior, una partición explícita y completa de los cuatro resultados posibles por ROI, fijada aquí, antes de correr el piloto. Sea `SE` el error estándar previsto de la media de 3 semillas (sección 4) y `D` la media observada de la diferencia emparejada B−A (sección 6, punto 3):

1. **Inconcluso por potencia insuficiente**: si `SE > |Δ_max|` (en `R_int`, `SE_previsto = 0,8629 > |Δ_max| = 0,0933`, cociente 0,108 — ver sección 4), el resultado se reporta como inconcluyente para esa ROI sin mirar siquiera el signo de `D`: la estadística planeada no tiene, de partida, capacidad para separar 0 de `Δ_max`. Esto **no** se reporta como evidencia de que A y B son equivalentes.
2. **Efecto presente**: si `SE ≤ |Δ_max|` y `|D| > 2·SE` y el signo de `D` coincide con el de `Δ_max`, el resultado es consistente con que el material del solape afecta el conteo detectado en la dirección esperada.
3. **Nulo con potencia adecuada**: si `SE ≤ |Δ_max|` y `|D| ≤ 2·SE`, el resultado es un nulo informativo (distinto del caso 1: aquí la estadística sí tenía, en principio, capacidad para detectar `Δ_max`, y no lo hizo) — se reporta como "sin evidencia de efecto en esta ROI", no como demostración de ausencia de efecto.
4. **Discordante**: si `SE ≤ |Δ_max|` y `|D| > 2·SE` pero el signo o la magnitud de `D` NO son compatibles con `Δ_max` (p. ej. signo opuesto, o `|D|` muy por encima de `|Δ_max|`), el resultado se reporta como discordante con la hipótesis del solape y requiere investigación adicional antes de cualquier conclusión; no se descarta ni se acepta automáticamente.

El umbral `2·SE` en los casos 2–4 es una regla de decisión heurística e informal fijada aquí, **no** un intervalo de confianza formal de Student-t: con solo 3 semillas (`df = 2`), el valor crítico t exacto al 95 % de dos colas es `t(0,975; 2) ≈ 4,303`, no 2, y a conteos esperados de orden 1 por corrida (caso de `R_int`) la distribución de Poisson subyacente es discreta y asimétrica, por lo que un intervalo simétrico tipo Wald-normal es una aproximación débil a la incertidumbre real. Si se necesita un intervalo formal para la redacción de resultados del piloto (unidad U9), debe construirse con `t(0,975; 2) ≈ 4,303`, no con 2, y advertirse explícitamente esa debilidad en `R_int`.

Los controles `R_rock` y `R_sky` sirven exclusivamente para descartar una diferencia espuria del procedimiento (sección 6, punto 5); no se usan para calibrar ni ajustar el resultado de `R_int`/`R_cond`/`R_body`.

## 8. Limitaciones

- El modelo de expectativa es un surrogate analítico de trazado de rayos con integración de flujo (sin dispersión múltiple, sin fluctuaciones de pérdida de energía, sin eficiencia instrumental); los números de la sección 4 son una expectativa de orden de magnitud, no una predicción física completa de Geant4.
- El factor de escala global (0,789) es una aproximación de un solo número para toda la vista. La sección 5 muestra que no es válido a nivel de ROI: el surrogate reproduce bien la escala del cielo abierto (cociente campaña/esperado ≈ 0,79) pero subestima el conteo de Geant4 por un factor de 1,9 a 3,7 en las regiones de roca profunda y de anomalía, que son precisamente las ROI de interés. Los conteos esperados de la sección 4 deben leerse como una cota de orden de magnitud del efecto relativo entre B1 y conduit-wins, no como una predicción absoluta de lo que medirá el piloto real.
- La variante A (geometría recibida) tiene, por construcción, un material indefinido y dependiente de la trayectoria de navegación en el solape; B1 y conduit-wins son las dos hipótesis extremas de lo que A podría resolver ahí, no una simulación de A misma. El piloto (unidad U9) es el que mide A realmente.
- La comprobación de registro en azimut es inconcluyente por la simetría del edificio en el eje de mira (sección 5); los dos intentos empíricos independientes de darle poder estadístico (sección 5.1, correlación por geometría; sección 5.2, suma de conteos por región) también terminan en NO RESUELTO. El registro de píxeles se sostiene, en definitiva, en la equivalencia exacta de código citada en la sección 5, no en una confirmación estadística independiente.
- La sección 5.2 encuentra que la asimetría de conteo inducida por una anomalía, en los mapas de campaña de Geant4 usados en esa verificación, es aproximadamente un orden de magnitud más débil que la que predice el motor analítico sin dispersión; se documenta ahí como observación exploratoria con una hipótesis (dispersión múltiple que traslada muones hacia bins de mayor opacidad) no establecida, y queda como problema abierto de OE1 más allá de esta entrega.

## 9. Reproducción

```
python scripts/analysis/oe1_pilot_roi.py preregister \
  --campaign-hist ../muography-thesis/data/campaign-geant4-merged/geo-train-06/geo-train-06_view0_hist.csv \
  --out-dir muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/analisis
```

ejecutado desde la raíz del repositorio `muography-dl-reconstruction`, con los valores por defecto: geometría `geo-train-06`, vista 0, `min-path-m = 20,0`, `seed = 20260929` (no usado: este subcomando es determinista; se acepta solo por consistencia de interfaz con los subcomandos `registration` y `registration-sum`). Sha-256 del script: `5204191864c83fa09d3107bb9004f2009f83fb9453f779a66dd438cf9bc8435b`. Salidas: `roi-mascaras.npz` (las cinco máscaras y los arreglos de longitud de recorrido), `roi-preregistro.json` (definiciones, parámetros, huellas de entrada y todos los números de este documento con precisión completa) y `roi-preregistro.png` (máscaras sobre el mapa esperado B1 y sobre el histograma de campaña). Pruebas de verificación: `python scripts/analysis/test_oe1_pilot_roi.py`.

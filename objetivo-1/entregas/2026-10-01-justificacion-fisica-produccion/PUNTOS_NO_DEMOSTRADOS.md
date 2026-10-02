# Puntos no demostrados: comprobaciones, criterios y resultados

> **Alcance ajustado tras la revisión de la dirección (2026-10-02):** C1 y C5 demuestran **contención entre planos grandes** para una fuente restringida al panel nominal, no equivalencia con un detector físico de 1,2 m (F-01). C3 vuelve a estar abierto, con un diseño dimensionado en [IMAGEN_FINAL_OBSERVABLE.md](IMAGEN_FINAL_OBSERVABLE.md). El 99,97 % de C2 corresponde a la imagen sin corte energético y no cierra la normalización (F-02). C4 sigue abierto para el observable con corte (F-03). C6 no es el único pendiente. Los resultados numéricos de abajo se mantienen; las conclusiones se leen con este alcance.

Cada punto indica la pregunta, la comparación y el criterio de resultado satisfactorio, fijados antes de ejecutar. C1, C2, C4 y C5 se ejecutaron en SC3 el 2026-10-02 en trabajos cortos (30621, 30622, 30625 y 30626; 16,7 h-núcleo en total). Los datos, comandos, logs y huellas están en `datos/sc3/controles-*`. La evaluación es reproducible con `scripts/controles_sc3.py`, que genera `resultados/controles-sc3.json` y las figuras 7 y 8.

**Ejecutable de control.** Se aplicó un parche de diagnóstico (`controles/controles-oe1-v3.patch`, con versiones v1 y v2 anteriores) sobre una copia del árbol de producción `angular-v1` (commit `0dea8e1`). El parche añade opciones por variables de entorno: tamaño del plano, cuadrados anidados en el plano, cortes de energía cinética, histograma de direcciones nominales, punto de inyección y margen angular. **Sin variables, los tres ejecutables parcheados reproducen bit a bit el histograma del ejecutable de producción** (geo-train-01, vista 0, 2·10⁶ primarios, semilla 777: 1.473.703 registros idénticos en r01, a00 y c00 frente a r00).

**Cuadrados anidados.** Un único plano de 1.200 m registra a la vez los cuadrados de 1,2; 100; 300 y 600 m de lado, con los mismos muones. La razón entre planos es entonces una fracción binomial anidada, con σ = √(p(1−p)/n). Todas las corridas usan geo-train-01 y la vista 0.

## C1. Contaminación de los píxeles de roca por muones blandos dispersados — **independencia del plano entre 100 y 600 m con E > 3 GeV e inyección junto a la roca; la equivalencia con el panel no está demostrada**

**Pregunta.** ¿Existe un observable en el que el plano grande y el panel físico coincidan, de modo que la imagen deje de depender del tamaño del plano?

**Comparación.** Razón de conteos 100 m / 600 m por banda de columna de roca, para cortes E_cin > {0; 0,5; 1; 2; 3; 5} GeV en el plano. 2·10⁷ primarios por variante de inyección, anidados.

**Criterio.** El menor corte con razón ≥ 0,98 y σ ≤ 0,01 en todas las bandas de roca, y razón de cielo abierto dentro de ±1 punto porcentual del modelo semianalítico evaluado con el mismo corte.

**Resultado (figura 7).**

| Inyección | Sin corte: razón por banda (10–30 / 30–60 / 60–100 / 100–200 / >200 ·10³ g/cm²) | Menor corte que cumple | Conteo de roca que conserva ese corte |
|---|---|---|---|
| Actual (D + R + 300 m) | 0,900 / 0,839 / 0,679 / 0,381 / 0,255 | 5 GeV | 24,2 % |
| Cilindro del edificio + 50 m | 0,979 / 0,950 / 0,867 / 0,627 / 0,457 | 3 GeV | 37,6 % |
| 1 m antes de entrar en roca | 0,998 / 0,991 / 0,969 / 0,853 / 0,724 | **3 GeV** | **83,5 %** |

Con E > 3 GeV e inyección junto a la roca, las razones por banda son 1,000 / 0,999 / 0,994 / 0,990 / 0,991 (mínima 0,9895 ± 0,0025), y la razón de cielo abierto coincide con el modelo a menos de 0,01 pp. Con la inyección actual, el conteo de roca a 600 m es de 3,1 a 6,8 veces la expectativa CSDA. Con inyección junto a la roca baja a 0,60–1,09 sin corte y a 0,57–0,85 con E > 3 GeV. El exceso de muones blandos dispersados desaparece. La diferencia restante con la CSDA no se evaluó en esta entrega (ver «Fuera de alcance»).

## C2. Doble descuento del aire en la normalización — **cumple sin corte con inyección 1 m antes de la roca; la normalización con el observable final sigue abierta (F-02)**

**Pregunta.** El espectro inyectado es de nivel del mar. ¿Debe atravesar el aire previo?

**Comparación.** Eficiencia de cielo abierto por fila (conteo en el cuadrado de 600 m dividido por las inyecciones con dirección nominal en esa fila), filas de 20 a 42°, para tres puntos de inyección. 2·10⁷ primarios cada una.

**Criterio, fijado para la variante (b).** Eficiencia ≥ 0,97 en todas las filas de 20 a 42°, con la pérdida restante explicada por el modelo del tramo de aire residual dentro de ±1 punto porcentual.

**Resultado (figura 8, izquierda).**

| Inyección | Eficiencia media | Fila mínima | Residuo frente al modelo (máximo) | Cumple |
|---|---:|---:|---:|---|
| Actual | 81,0 % | 72,9 % | 2,4 pp | no |
| (b) Cilindro del edificio + 50 m (0,56–1,74 km de aire) | 93,6 % | 91,2 % | 2,5 pp | no |
| (c) 1 m antes de la roca | 99,97 % | 99,69 % | 0,36 pp | **sí** |

La variante (b), especificada de antemano, no cumple: deja entre 0,56 y 1,74 km de aire. La variante (c) se añadió tras ese resultado y se evaluó con el mismo criterio. Con (c), el número de muones inyectados en la ventana coincide con los registrados en cielo abierto, y la convención S0 («muones que llegan al detector») queda consistente con el transporte. El tiempo de transporte baja de 0,796 a 0,532 ms de núcleo por evento.

## C3. Equivalencia con un detector físico mediante generación en área amplia — **abierto**

La independencia del plano de C1 no implica equivalencia con el panel: ambos planos grandes registran la misma fuente restringida (F-01). Con los datos anidados de c01, solo entre el 3,6 % y el 70,4 % de los registros con E > 3 GeV del cuadrado de 600 m caen en el panel de 1,2 m, según la banda. El control queda dimensionado en dos etapas (C3-a: escala de desplazamiento, unas 3 h-núcleo; C3-b: fuente amplia restringida en dirección, entre 6,6 y 660 h-núcleo según el semilado), con un criterio de equivalencia por intervalos simultáneos en [IMAGEN_FINAL_OBSERVABLE.md](IMAGEN_FINAL_OBSERVABLE.md#3-propuesta). La estimación anterior de 6.600 h-núcleo correspondía a todas las direcciones.

## C4. Pérdida por migración angular en los bordes de la ventana — **mejora clara; el criterio de 1 pp no se cumple de forma estricta**

**Pregunta.** ¿Qué margen angular de generación elimina el déficit en los bordes?

**Comparación.** Ventana de generación ampliada en Δ ∈ {0; 2; 5}° por lado, conteo en la ventana nominal y cuadrado de 600 m. Se mide la desviación de las cinco filas superiores respecto del ajuste lineal de 30–42°, y la de las cinco columnas de cada borde respecto de la media de las columnas interiores. 2·10⁶ primarios por caso.

**Criterio.** El menor Δ con todas las desviaciones ≤ 1 pp.

**Resultado (figura 8, derecha).**

| Inyección, margen | Desviación máxima | Desviación media en bordes | Dispersión empírica entre columnas interiores |
|---|---:|---:|---:|
| Actual, 0° | 31,5 pp | −19,0 pp | 1,8 pp |
| Actual, 5° | 4,1 pp | −1,2 pp | 2,3 pp |
| Cilindro, 5° | 4,3 pp | −0,5 pp | 2,4 pp |
| Antes de la roca, 0° | 4,2 pp | −0,8 pp | 0,2 pp |
| Antes de la roca, 5° | 1,65 pp | −0,07 pp | 0,75 pp |

Ninguna configuración cumple estrictamente. Además, estos valores corresponden al histograma **sin corte**. Sobre la imagen con E > 3 GeV, el diagnóstico de la dirección da 1,64 pp (c01, sin margen) y 2,84 pp (c02, 5°) ([DIAGNOSTICO_OBSERVABLE_Y_DECISION.md](../../DIAGNOSTICO_OBSERVABLE_Y_DECISION.md)). La dispersión empírica no es un intervalo de confianza válido con migración entre píxeles; el criterio requiere réplicas independientes. **C4 queda abierto.** Con inyección junto a la roca y margen de 5°, el sesgo medio de borde desaparece (−0,07 pp) y la desviación máxima, 1,65 pp, está a 2,2 dispersiones empíricas. Esa dispersión, medida en las columnas interiores, es la fluctuación propia de esta corrida y no un efecto de borde; su origen detallado no se analizó (θ₀ ≈ 0,07° a 0,5 GeV/c en 1 m de aire, frente a bins de 0,18–0,23°). Sin margen, el déficit es real: −3,3 pp en las columnas extremas y −4,2 pp en la fila superior. **Se adopta un margen de 5°.** Confirmar el criterio de 1 pp exige una muestra unas 6 veces mayor; esa verificación se incluye en el piloto P0 del plan.

## C5. Asíntota del plano — **cumple**

**Comparación.** Cuadrado de 600 m frente al plano de 1.200 m, mismos muones, 2·10⁷ primarios.

**Criterio.** |ε₁₂₀₀ − ε₆₀₀| < 0,1 pp en total, y razón por banda de roca compatible con 1 dentro de 2σ (σ de corridas independientes, tal como se fijó).

**Resultado.**

- Sin corte, la diferencia total es de 0,037 pp; con E > 0,5 GeV o más, ≤ 0,005 pp. Todas las bandas cumplen.
- Con inyección junto a la roca, la diferencia es exactamente cero en todos los cortes.
- La serie se repitió con N = 2·10⁶ y semilla 777, en planos separados con la malla v1: 1,53 / 64,08 / 72,94 / 73,69 / 73,72 % para 1,2 / 100 / 300 / 600 / 1.200 m. Reproduce los tres valores del comentario de código (64,2 / 73,07 / 73,81 %) con un desfase uniforme de −0,12 a −0,13 pp, que no se analizó por separado. La afirmación «menos de 0,5 % de la asíntota» queda respaldada por datos conservados: el plano de 600 m está a 0,04 pp del de 1.200 m.

## C6. Convención de área y significado de «30 días» — decisión pendiente

S0 usa A = 1,44 m² normal a cada dirección. Un panel vertical real aporta A·cos(el)·cos(az), lo que reduce S0 un 21,5 %. Interpretar la energía del umbral como cinética cambia S0 un −2,1 %. No requiere corrida. Con la inyección (c), además, el umbral de aire de S0 (0,798 GeV) deja de tener contrapartida física. La ficha de datos debe declarar si S0 se recalcula desde el rango generado (+6,2 %, figura 4) o se mantiene como convención. Es una decisión de definición, **no la única pendiente**: se suman F-01 y F-03 (ver [IMAGEN_FINAL_OBSERVABLE.md](IMAGEN_FINAL_OBSERVABLE.md#5-lo-que-queda-sin-demostrar)).

## Fuera de alcance de esta entrega

- La comparación de transmisión Geant4 frente a CSDA en roca (razones de 0,57 a 1,09 con la inyección (c)): es física del motor de transporte, no del estimador.
- C1 se evaluó en una sola geometría homogénea (geo-train-01). La extrapolación del corte de 3 GeV a geometrías con anomalías se verifica en el piloto P0 del plan con geo-train-06.

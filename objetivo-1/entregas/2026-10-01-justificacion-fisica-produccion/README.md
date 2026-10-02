# Justificación física y plan de producción del conjunto de imágenes del OE1

Entrega del 2026-10-01 (Colombia), con comprobaciones en SC3 del 2026-10-02. Rama `oe1/justificacion-fisica-produccion`, creada desde `main` en `18aa5b1`.

Esta entrega responde a la solicitud de [PENDIENTES.md](../../PENDIENTES.md) y [CADENA_LOCAL_OE1.md](../../CADENA_LOCAL_OE1.md): los archivos, comandos, semillas y conteos de la comparación de planos de conteo; la relación del conteo con el detector de 1,2 m y con la exposición; y un plan de producción. Se revisaron los seis commits del director posteriores a `f35ee7c`: `ac0277c`, `963697b`, `63ecb65`, `c63e296`, `2036cf1` y `18aa5b1`. Contienen la revisión de la corrida angular, el exportador, las regiones, la integración de ROI, la [revisión de la aceptación del plano](../../REVISION_ACEPTACION_PLANO.md) y la cadena local. No traen instrucciones que contradigan la solicitud.

Los puntos 1 y 2 se analizaron sobre datos existentes en SC3 y en los repositorios. Las comprobaciones del punto 3 (C1, C2, C4 y C5) se ejecutaron en SC3 en trabajos cortos: 30621, 30622, 30625 y 30626, unas 16,7 h-núcleo en total. Además, una prueba de integración de la cadena de producción usó dos bloques de 10⁵ primarios. **No se lanzó la producción del conjunto.** No se modificaron `main`, `originales/`, entregas anteriores ni el árbol de producción `angular-v1` de SC3.

## Contenido

| Archivo | Contenido |
|---|---|
| [scripts/comun.py](scripts/comun.py) | Física común: flujo de Guan, pérdida de energía de Bethe en aire con efecto densidad, Highland, decaimiento, mallas y lectores |
| [scripts/comparar_planos.py](scripts/comparar_planos.py) | Punto 1; figuras 1 y 2; [comparacion-planos.json](resultados/comparacion-planos.json) |
| [scripts/relacion_plano_detector.py](scripts/relacion_plano_detector.py) | Punto 2a; figura 3; [relacion-plano-detector.json](resultados/relacion-plano-detector.json) |
| [scripts/exposicion_equivalente.py](scripts/exposicion_equivalente.py) | Punto 2b; figura 4; [exposicion-equivalente.json](resultados/exposicion-equivalente.json) |
| [scripts/consistencia_espectro.py](scripts/consistencia_espectro.py) | Punto 2c; figura 5; [consistencia-espectro.json](resultados/consistencia-espectro.json) |
| [scripts/controles_sc3.py](scripts/controles_sc3.py) | Punto 3: C1, C2, C4 y C5 sobre las corridas de SC3; figuras 7 y 8; [controles-sc3.json](resultados/controles-sc3.json) |
| [scripts/plan_produccion.py](scripts/plan_produccion.py) | Punto 4; figura 6; [plan-produccion.json](resultados/plan-produccion.json); manifiestos |
| [PUNTOS_NO_DEMOSTRADOS.md](PUNTOS_NO_DEMOSTRADOS.md) | Punto 3: seis comprobaciones con pregunta, comparación, criterio y **resultado** |
| [controles/](controles/) | Parches de diagnóstico (v1, v2 y v3) y sbatch de las comprobaciones |
| [PLAN_PRODUCCION.md](PLAN_PRODUCCION.md) | Punto 4: vistas, criterio de N, cómputo, almacenamiento y comandos |
| [produccion/](produccion/) | `preparar_arbol_receta.sh`, `bloque_v1.sbatch`, `lanzar_v1.py`, `fusionar_v1.py`, `prueba_integracion.sh` y manifiestos de la receta con k = 1 y k = 10 |
| [datos/sc3/](datos/sc3/) | Evidencia copiada de SC3: metadatos, histogramas y logs de 29475/29477/29480/29484; 114 metadatos de campaña; extractos de `sacct`; scripts SLURM históricos; `controles-30621/30622/30625/30626` (corridas completas con huellas verificadas); `prueba-integracion/`; receta de entorno (`receta-entorno-geant4.txt`) |

## Uso

Dependencias: Python ≥ 3.12, NumPy y Matplotlib. La ejecución verificada usó Python 3.13.5, NumPy 2.4.4 y Matplotlib 3.10.7 en Windows. No hace falta SciPy ni Geant4. Desde la raíz de la réplica:

```console
python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/comparar_planos.py
python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/relacion_plano_detector.py
python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/exposicion_equivalente.py
python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/consistencia_espectro.py
python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/controles_sc3.py
python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/plan_produccion.py --campana RUTA/campaign-merged
```

Cada script tarda menos de 1 min. Los cinco primeros solo leen archivos versionados; `plan_produccion.py` usa además `controles-sc3.json`, así que se ejecuta después. El último necesita los 114 histogramas fusionados de SC3 (`~/muography-scratch/campaign-merged`, 26 MB, sin versionar), cuyas huellas comprueba contra `datos/sc3/campaign-manifest.csv` antes de usarlos. Los JSON registran el entorno. Los scripts no usan números aleatorios, salvo la medición del tamaño del NPZ, que tiene semilla fija.

---

## 1. Comparación de los planos de 100, 300 y 600 m

Los metadatos del simulador **no registran el tamaño del plano**. Por eso cada corrida se asigna a un plano a partir de la historia del código fuente (`muography-thesis`) y de `sacct`:

- `81a5935`, 18:43: el contador tiene el tamaño del panel, 1,2 m.
- `477f193`, 19:01: plano de 100 m.
- `30fd245`, 19:22: generador por tablas S0.
- `653f0fd`, 20:02: plano de 600 m.

Todas las corridas usan geo-train-01, vista 0, Geant4 11.4.2 MT y el nodo guane01 (figura 1).

| Trabajo | Plano | Muestreo | Semilla | Hilos | Generados (EcoMug) | Transportados | Registrados | Eficiencia ± σ binomial | E_cin. media registrada | Estado |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 29475 | 1,2 m | EcoMug directo | 20260805 | 8 | 2.145.555 | 100.000 | 1.203 | 1,203 ± 0,035 % | 94,4 GeV | conservado |
| 29477 | 100 m | EcoMug directo | 20260805 | 8 | 2.146.114 | 100.000 | 63.890 | 63,89 ± 0,15 % | 10,4 GeV | conservado |
| 29480 | 100 m | tablas S0 (30 d) | 20260805 | 24 | 36.174.573 | 36.174.573 | 23.209.619 | 64,160 ± 0,008 % | 24,6 GeV | conservado |
| 29484 | 600 m | tablas S0 (30 d) | 20260805 | 24 | 36.174.573 | 36.174.573 | 26.693.501 | 73,791 ± 0,007 % | 21,5 GeV | conservado |
| — | 100 m | tablas, N = 2·10⁶ | 777 | — | — | — | — | 64,2 % (comentario) | — | **faltante** |
| 29481 | 300 m (inferido) | tablas, N = 2·10⁶ | 777 | 24 | — | — | — | 73,07 % (comentario) | — | **faltante** |
| 29482 | 600 m | tablas, N = 2·10⁶ | 777 | 24 | — | — | — | 73,81 % (comentario) | — | **faltante** |

Los comandos exactos (`SubmitLine`) están en [sacct-serie-planos.txt](datos/sc3/sacct-serie-planos.txt) y en el JSON. Las huellas de cada histograma y metadato también están en el JSON.

**Datos faltantes.** La serie de 2·10⁶ eventos con semilla 777 solo consta en el comentario de `DetectorConstruction.cc`. 29481 y 29482 fueron `srun` interactivos con salida en `/tmp` del nodo. El 2026-10-01 se revisó `/tmp` de guane01 y ya no contiene esos archivos. 29481 figura como FAILED 2:0 tras 12 min. No hay trabajo SLURM de 2·10⁶ eventos con el plano de 100 m; el valor 64,2 % coincide con 29480 (64,16 %) al redondear. No se encontró ningún otro tamaño de plano. Estos valores no se reconstruyen. Si los tres fueran binomiales con N = 2·10⁶, la diferencia de 300 a 600 m sería de 0,74 ± 0,04 puntos porcentuales: significativa, y por tanto no indica saturación.

**Serie repetida con datos conservados (trabajo 30621; C5).** Con el mismo N = 2·10⁶ y la misma semilla 777, en planos separados y con la malla v1: 1,53 / 64,08 / 72,94 / 73,69 / 73,72 % para 1,2 / 100 / 300 / 600 / 1.200 m. Los tres valores del comentario quedan reproducidos con un desfase uniforme de −0,12 a −0,13 pp. Con cuadrados anidados (2·10⁷ primarios), el plano de 600 m queda a 0,037 pp del de 1.200 m.

**Resultado por píxel, 29480 frente a 29484** (misma N, semilla y tablas; figura 2). La razón de conteos 100 m/600 m vale 0,870 en cielo abierto y baja con la columna de roca:

| Columna de roca (g/cm²) | 0 | <10⁴ | 1–3·10⁴ | 3–6·10⁴ | 6–10·10⁴ | 1–2·10⁵ | >2·10⁵ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Razón 100 m/600 m | 0,870 | 0,93 | 0,90 | 0,83 | 0,68 | 0,38 | 0,25 |
| Plano 600 m / expectativa CSDA | 0,77 | 1,3 | 3,2 | 5,7 | 6,8 | 5,6 | 3,1 |

El 99,6 % de los conteos está en cielo abierto. Por eso la convergencia de la eficiencia total refleja el cielo abierto y no dice nada sobre los píxeles de roca, que son los relevantes para el OE1. Al pasar de 100 a 600 m se ganan 3.483.882 muones con una energía cinética media estimada de 0,86 GeV, calculada como (K₆E₆ − K₁E₁)/(K₆ − K₁).

## 2a. Relación entre los registros del plano grande y el detector de 1,2 m

**Muestreo (verificado en `PrimaryGeneratorAction.cc`).** Para cada primario se toma la fila de elevación con probabilidad w_fila/S0, el azimut uniforme en ±30° y el punto de impacto nominal x uniforme sobre el panel P de 1,2 × 1,2 m. Después se retrocede una longitud R_inicio/cos(el), con R_inicio = D + R_base + 300 m (1.956,2 m en geo-train-01), y el momento se toma de los cuantiles EcoMug de su banda. Sin transporte, cada primario llegaría a P con su dirección nominal. **El área física solo entra en la normalización.** El conteo del estimador es:

C_b = Σ_{x ∈ P} 1[sobrevive, llega al plano S, dirección final ∈ b],

y el de un detector físico es:

D_b = Σ_{x ∈ ℝ²} 1[sobrevive, llega a P, dirección final ∈ b].

Con el cambio de variable Δ = x_final − x, C = D si la probabilidad de transporte no depende de x en la escala de Δ (invariancia lateral) y si S contiene todos los Δ. Es la condición que la dirección ya planteó con un contraejemplo. **No existen pesos.** La normalización es N/S0 y el área del plano no aparece en ningún factor.

**Escala de Δ (figura 3, derecha).** Con Highland en 2–2,8 km de aire, el desplazamiento lateral rms de los muones que sobreviven es de unos 50–100 m a 0,6–1 GeV/c, de unos 4–8 m a 10 GeV/c y de menos de 1 m por encima de unos 100 GeV/c. En cielo abierto el aire es lateralmente homogéneo y la condición se cumple. En los píxeles de roca y cerca de la silueta no se cumple, porque un Δ de 50 m equivale a 2,9° de paralaje a 1 km.

**Validación del modelo (figura 3).** El modelo combina frenado (Bethe en G4_AIR; el mínimo ionizante calculado, 1,8146 MeV cm²/g, coincide con el valor PDG de 1,815), decaimiento y núcleo gaussiano de Highland, con el espectro exacto del generador. Reproduce la eficiencia de cielo abierto medida en las filas de 20 a 42°:

- Plano de 100 m: residuo medio +0,28 puntos porcentuales, máximo 0,96. La σ de Poisson por fila es de unos 0,2 puntos porcentuales.
- Plano de 600 m: residuo medio −0,90 puntos porcentuales, máximo 2,45.

La eficiencia total predicha es del 64,3 % con 100 m y del 76,2 % con 600 m, y el plano infinito daría también un 76,2 %. Para el panel de 1,2 m predice un 1,43 %, del mismo orden que el 1,20 % de 29475, que usa otro muestreo de direcciones. El modelo no incluye las colas de dispersión simple, las fluctuaciones de pérdida ni la migración angular hacia fuera de la ventana. Esta última produce −11 puntos porcentuales en las filas por encima de 44° y −2,5 por debajo de 13°. El déficit de −0,90 a 600 m indica que el modelo gaussiano no acota la asíntota.

**Conclusión.** Para muones de cielo abierto, el plano grande es un estimador válido del flujo direccional que llega al panel: la condición de invariancia se cumple y la eficiencia coincide con el modelo con un error de alrededor de 1 punto porcentual. En los píxeles de roca, el conteo está dominado por muones blandos desplazados entre decenas y cientos de metros. Su número depende del plano, y no se ha demostrado su equivalencia con un detector físico. **Resuelto en C1:** con inyección 1 m antes de la roca y E_cin > 3 GeV en el plano, la razón 100 m / 600 m es ≥ 0,989 en todas las bandas de roca (σ ≤ 0,0052) y se conserva el 83,5 % del conteo en roca. Con ese observable, la imagen deja de depender del tamaño del plano (figura 7). Para muones de más de 3 GeV, el desplazamiento residual es de pocos metros (figura 3), lo que acota la diferencia con un panel físico a un paralaje del orden de un píxel; esa cota no se midió directamente.

## 2b. Exposición equivalente

N(T) = Σ_b Φ_int(E_min, θ_b) · A · ΔΩ_b · T, con:

- Φ_int: integral de Guan por encima de E_min = 0,7981 GeV, el umbral CSDA de 3 km de aire con densidad 1,225·10⁻³ g/cm³.
- A = 1,44 m², normal a cada dirección.
- ΔΩ_b = Δaz · Δel · cos(el).

La exposición equivalente es T_eq = 30 d · N / S0_v1.

| Magnitud | Valor |
|---|---|
| S0 recalculado con la malla histórica | 36.177.630, frente a 36.175.380 de la tabla (+6,2·10⁻⁵; máximo por fila 5·10⁻⁴, por la interpolación del surrogate) |
| S0 v1 (Δaz = 60/256°) recalculado | 36.036.311, frente a 36.034.069,91 declarado (+6,2·10⁻⁵) |
| Error de integración numérica | < 10⁻⁵ (6.000 frente a 24.000 nodos) |
| Cobertura angular v1 | az −30…+30°, el 1,912…47,088°; Ω = 0,73204 sr (suma discreta frente a exacta: 4·10⁻⁷) |
| Tasa v1 | 13,90 muones/s en la ventana |
| T_eq | 24·10⁶ pares (etapa 2): 19,98 d; S0 v1: 30 d; k·S0 v1: 30·k d |

**Sensibilidad a la convención (figura 4).** Si la energía del umbral se toma como cinética, S0 cambia un −2,1 %. Con la densidad de G4_AIR, +0,27 %. Con el umbral por rango de Bethe en aire, −0,59 %. Sin umbral de aire, +6,2 %. Con un panel vertical físico (A·cos(el)·cos(az)), −21,5 %. Estas variaciones son incertidumbres de **definición**, no estadísticas. Si los conteos de 29484 se leen como cuentas de detector, la exposición efectiva en cielo abierto es de 23,1 días, con un rango por fila de 12,1 a 27,7, y no de 30 ([C2](PUNTOS_NO_DEMOSTRADOS.md#c2-doble-descuento-del-aire-en-la-normalización), [C6](PUNTOS_NO_DEMOSTRADOS.md#c6-convención-de-área-y-significado-de-30-días)).

## 2c. Consistencia entre el espectro generado y la tasa

Resultados de `consistencia-espectro.json` (figura 5):

- **Forma.** El espectro EcoMug es más blando que el de Guan en el mismo rango. La distancia de Kolmogorov–Smirnov entre ambos va de 0,063 a 0,119, y en la banda de 30–33° la mediana es de 3,56 GeV frente a 4,69 GeV. Esto concuerda con la diferencia espectral documentada en `build_generator_tables.py`.
- **Rango.** EcoMug empieza en p = 0,5 GeV/c (E total de 0,511 a 0,614 GeV según la banda), pero S0 solo cuenta E > 0,798 GeV. Ponderado por S0, el 6,6 % de los primarios generados está por debajo del umbral de la tasa: un 0,1 % a 2–5° y un 9,1 % a 44–47°. Integrar Guan en el rango generado aumentaría la tasa entre un 0,6 % y un 8,5 % según la banda.
- **Transporte.** El aire entre la inyección y el detector elimina otro 19,5 %, ponderado por S0, por frenado y decaimiento. Esto se suma al umbral de aire ya aplicado en S0.

**Conclusión.** La normalización es internamente consistente con la convención del surrogate, que se reproduce a 6·10⁻⁵. Sin embargo, no es consistente con un espectro de nivel del mar transportado por el aire: el aire se descuenta dos veces. **Resuelto en C2:** inyectando 1 m antes de que la línea de mira entre en roca, la eficiencia de cielo abierto pasa del 81,0 % al 99,97 % (fila mínima 99,69 %; residuo frente al modelo ≤ 0,36 pp). La tasa S0 queda así consistente con lo que se registra (figura 8).

## 3. Comprobaciones ejecutadas en SC3

Detalle, criterios y tablas en [PUNTOS_NO_DEMOSTRADOS.md](PUNTOS_NO_DEMOSTRADOS.md). Todas con geo-train-01 y vista 0.

| Comprobación | Resultado | Estado |
|---|---|---|
| Regresión del parche | Los ejecutables parcheados sin opciones reproducen bit a bit el histograma de producción (3/3) | cumple |
| C1, observable independiente del plano | E_cin > 3 GeV con inyección junto a la roca: razón 100/600 ≥ 0,989 en todas las bandas | cumple |
| C2, doble descuento del aire | Inyección 1 m antes de la roca: cielo abierto 99,97 %. La variante (b), fijada de antemano, no cumple (93,6 %) | cumple con (c) |
| C3, referencia con generación amplia | No necesaria, porque C1 encontró un observable | no se ejecuta |
| C4, margen angular | Margen de 5°: sesgo medio de borde −0,07 pp; máximo 1,65 pp (2,2σ empíricas) frente al criterio de 1 pp | parcial; se confirma en P0 |
| C5, asíntota | 600 m frente a 1.200 m: 0,037 pp sin corte, 0 pp con la receta | cumple |
| C6, convención de área | Decisión de definición | pendiente |

## 4. Plan de producción

Ver [PLAN_PRODUCCION.md](PLAN_PRODUCCION.md). Cifras clave:

- **Receta:** inyección 1 m antes de la roca, margen de 5°, plano de 600 m, imagen de referencia con E_cin > 3 GeV, ejecutable `0dea8e1` + parche v3. El árbol de producción ya está compilado en SC3 (trabajo 30627), y la cadena lanzador → bloque → fusión → exportador del director se probó con éxito (30628 y 30629).
- **Vistas:** se generan las 114. Ninguna referencia histórica se reutiliza, por la malla v1, la geometría B y el cambio de observable.
- **N:** el conteo en ROI de roca con la receta es 0,124 veces el histórico, que estaba inflado por el fondo blando. Para 100 cuentas (10 %) en el 90 % de las ROI hace falta k ≈ 9,5. **Se recomienda k = 10**: 526,7 millones de primarios por vista (300 días convencionales), 8.305 h-núcleo, unas 86,5 h de pared con cuatro trabajos, 1,3 GB de histogramas y hasta 2,4 GB de pares. Para 5 % haría falta k ≈ 38, unas 31.500 h-núcleo.
- **P0** (geo-train-06, seis vistas, k = 1, unas 44 h-núcleo) verifica el factor en una geometría con anomalías y C4 con más estadística antes de P1.

**Receta de entorno (P-02).** Geant4 11.4.2 MT, módulos `gnu14/14.2.0` y `geant4/11.4.2`, GCC 14.2.0 y lista de física `FTFP_BERT`. Las versiones de los paquetes de datos (G4NDL 4.7.1, G4EMLOW 8.8, PhotonEvaporation 6.1.2, RadioactiveDecay 6.1.2, G4PARTICLEXS 4.2, entre otros) están en `datos/sc3/receta-entorno-geant4.txt`, y el `CMakeCache.txt` de producción en `datos/sc3/controles-30621/resultados/`. **Observación:** `build-az-edges-v1` se compiló con `CMAKE_BUILD_TYPE` vacío, sin `-O3`. El árbol de la receta reproduce esa configuración para conservar la equivalencia bit a bit. Compilar en Release podría reducir el coste, pero exigiría una nueva regresión.

---

## Resumen

1. **Planos.** Se identificó qué corrida corresponde a cada plano, con conteos, semillas y comandos. La serie original de 2·10⁶ eventos se había perdido; se **repitió con datos conservados**, reproduce los valores citados con un desfase de ~0,12 pp, y el plano de 600 m queda a 0,04 pp del de 1.200 m.
2. **Cielo abierto.** El plano grande es un estimador correcto del flujo direccional. Un modelo independiente reproduce la eficiencia con un error de 0,3 a 0,9 pp.
3. **Roca.** Con la configuración histórica, el conteo en roca dependía del plano: la razón 100/600 bajaba hasta 0,25 y el conteo era de 3 a 7 veces la expectativa CSDA, por muones blandos de unos 0,9 GeV. **Con la receta validada esa dependencia desaparece** (razón ≥ 0,989) y el conteo en roca queda en 0,6–1,1 veces la CSDA.
4. **Normalización.** S0 se reprodujo desde Guan con un error de 6·10⁻⁵. El doble descuento del aire (19,5 %) **se eliminó** con la inyección junto a la roca (cielo abierto 99,97 %). La pérdida en los bordes de la ventana (hasta 32 pp) **se redujo** a un sesgo medio de −0,07 pp con un margen de 5°.
5. **Producción.** La receta, el ejecutable, los manifiestos, el lanzador y la fusión están probados en SC3. Con k = 10 la producción cuesta 8.305 h-núcleo.

## Pendientes

- **C6:** declarar la convención de área (normal o panel vertical, −21,5 %) y si S0 se recalcula sin el umbral de aire (+6,2 %). Es la única decisión antes de P0.
- **P0:** verificar el factor de conteo de la receta en geo-train-06 (criterio: dentro del 20 % de 0,124) y C4 con 5,3·10⁷ primarios por vista (criterio: ≤ 1 pp).
- La transmisión Geant4 frente a CSDA en roca (0,57–1,09) no se evaluó: corresponde a la física del motor, no al estimador.
- Las respuestas E2-01, E2-02 y E2-04 no forman parte de esta entrega.

## Propuesta para completar el OE1

1. Decidir C6 y registrarlo en la ficha de datos.
2. Ejecutar P0 con los comandos de [PLAN_PRODUCCION.md](PLAN_PRODUCCION.md) (sección 4), aplicar sus dos criterios y fijar k.
3. Ejecutar P1 (114 vistas, k = 10 salvo que P0 indique otro valor) con el lanzador idempotente. Después fusionar, exportar y empaquetar con la cadena local, y publicar una ficha de datos versionada con la trazabilidad historia → receta v1 → referencia → pares.

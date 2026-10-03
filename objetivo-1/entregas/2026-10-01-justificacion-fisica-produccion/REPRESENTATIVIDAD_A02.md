# Representatividad del conjunto (A-02) — borrador

2026-10-03. Borrador para la valoración académica de la dirección y su incorporación al informe del OE1. Cada cifra remite al archivo que la contiene; lo que no está documentado se indica como tal.

## 1. Alcance de la afirmación

El objetivo aprobado pide imágenes muográficas por transmisión, con distintos niveles de estadística, obtenidas por simulación Monte Carlo «que reproduzca escenarios representativos de exploración volcánica» ([ALCANCE.md](../../ALCANCE.md)). Bajo el [alcance idealizado adoptado](../../DEFINICION_PRODUCTO_OE1.md), representatividad significa aquí que el catálogo cubre una familia de edificios cónicos con heterogeneidades internas del tipo que la muografía volcánica asocia a conductos, cavidades y cuerpos densos (Tanaka et al., 2007; Oláh et al., 2018; Tanaka et al., 2023), observados en geometría de transmisión. No se afirma que las geometrías reproduzcan un volcán concreto ni que las imágenes equivalgan a las de un instrumento real.

## 2. Escenarios y geometría

El catálogo de 19 geometrías se generó de forma determinista con semilla 20260805 y con requisitos de cobertura explícitos: cada tipo de anomalía aparece solo y combinado, existe un control homogéneo y una geometría de generalización excluida del resto ([make_catalog.py](../../originales/scripts/simulation/geometry_catalog/make_catalog.py)). Los parámetros, leídos de los [JSON del catálogo](../../originales/scripts/simulation/geometry_catalog/geometries/), cuyas huellas coinciden con las de la [receta](../../contratos/receta-operativa-siete-actividades.json), son:

| Elemento | Valores |
|---|---|
| Edificio | Cono; radio basal 509,7–698,7 m; altura 356,2–449,6 m; 2,65 g/cm³ en las 19 geometrías |
| Conductos | 11, en 11 geometrías; 1,831–2,151 g/cm³; radio 18,4–35,4 m; desde la base hasta 320,2–391,8 m |
| Cavidades | 13, en 10 geometrías; 0,048–0,468 g/cm³; radio 20,2–48,9 m; centro a 94,0–245,1 m de altura |
| Cuerpos densos | 8, en 8 geometrías; 3,014–3,285 g/cm³; semiejes 34,5–78,1 m; centro a 59,8–189,0 m |
| Combinaciones | Solo conducto (3), solo cavidad (2), solo cuerpo denso (3), dos cavidades (1), conducto+cavidad (2), conducto+cuerpo denso (2), cavidad+cuerpo denso (1), tres tipos (2), conducto+dos cavidades (2), control homogéneo `geo-train-01` (1) |

Las anomalías tienen contrastes de ambos signos respecto de la roca: conductos y cavidades menos densos, cuerpos densos más densos. La partición por geometría es 12/3/3/1 ([ficha](../../FICHA_CONJUNTO_OE1.md)). `geo-gen-01` repite la combinación de `geo-train-11` con otros parámetros: evalúa generalización a nuevas posiciones y tamaños, no a un tipo nuevo de anomalía.

Seis geometrías presentaban intersecciones entre anomalías o salidas del edificio ([diagnóstico](../../DIAGNOSTICO_GEOMETRIAS.md)). La construcción corregida recorta las anomalías al edificio con margen de 1 mm y asigna la región común a la anomalía posterior, sin modificar densidades ni posiciones ([protocolo](../../PROTOCOLO_SEGUNDO_ENSAYO_OE1.md), [control](../../CONTROL_FISICO_LOCAL.md)). La integración independiente de las cuatro intersecciones coincide con las estimaciones de los estudiantes dentro de 1,13 errores estándar. No hay control independiente equivalente para los volúmenes que sobresalen del edificio en `geo-gen-01` y `geo-test-03` ([control](../../CONTROL_FISICO_LOCAL.md)), y los casos combinados de recorte y sustracción múltiple quedaron sin ensayar ([revisión](../../REVISION_ENTREGA_2026-09-29.md)).

Cada geometría se observa desde seis vistas separadas 60°, con el punto de observación a 1.000 m del eje y 1,5 m de altura ([GeometryConfig.hh](../../originales/scripts/simulation/geant4_app/include/GeometryConfig.hh)). La imagen tiene 256 × 256 píxeles: azimut relativo entre −30° y +30° y centros de elevación entre 2° y 47°. En el cono homogéneo, sobre la malla de celdas de 4 × 4 píxeles con columna positiva, el percentil 90 de la columna nominal va de 212.689 a 295.740 g/cm², y entre el 70,7 % y el 87,1 % de las celdas alcanza al menos 100.000 g/cm² ([plan.json](../../evidencias/preparacion-campana-114/plan.json)). Las imágenes abarcan, por tanto, desde cielo abierto hasta opacidades altas. El indicador de suficiencia usa ROI de 4 × 4 píxeles en la banda nominal de 30.000–100.000 g/cm²: entre 150 y 244 por geometría (3.636 distintas en las 19 geometrías) y 21.816 en las 114 vistas. Esas máscaras ignoran las anomalías, que sí se transportan.

El plan aprobado preveía perfiles «inspirados en perfiles topográficos reales» como Asama o Sakurajima, adaptados a geometrías simplificadas (`PlanTrabajoGrado_main.tex`, metodología del OE1). El catálogo emplea conos; esa simplificación debe declararse en el informe.

## 3. Fuente

La fuente combina pesos de dirección derivados de la parametrización de Guan et al. (2015) con cuantiles de momento de EcoMug (Pagano et al., 2021): 257 cuantiles en 16 bandas de elevación ([receta](../../contratos/receta-operativa-siete-actividades.json)). El impacto nominal es uniforme sobre un panel de 1,2 m, y la generación se extiende 5° fuera de la ventana. La probabilidad de generar dentro de la ventana es 0,6841465610; el 20,1825 % de la masa procede de filas de elevación extrapoladas linealmente, y el 20,5255 % usa el espectro de la banda extrema ([balance](../../BALANCE_PREPARACION_LOCAL.md)). La normalización S0 se reprodujo desde Guan con error relativo de 6,2·10⁻⁵ frente a la tabla. El espectro de EcoMug es más blando que el de Guan (distancia de Kolmogorov–Smirnov 0,063–0,119) ([README](README.md)).

Se propone, para valoración, que esta fuente resulta aceptable para el producto idealizado porque todas las referencias y realizaciones comparten una misma definición documentada, y la tarea de OE2/OE3 depende de la relación entre conteos de distinta estadística bajo esa definición, no de una escala absoluta de flujo. El espectro más blando de EcoMug y la masa extrapolada citados arriba forman parte de esa hipótesis común. Su límite es explícito: el modelo híbrido y su extensión son hipótesis del conjunto, no un flujo calibrado ([definición](../../DEFINICION_PRODUCTO_OE1.md)).

## 4. Transporte

El transporte usa Geant4 11.4.2 con la lista física FTFP_BERT (Agostinelli et al., 2003). Solo se siguen primarios: los secundarios se eliminan al crearse (`physics_note` en los [metadatos de fusión](datos/sc3/campana-114/fusion/)). El primario se inyecta aproximadamente 1 m antes de entrar en el cono, a partir del último punto interior de un muestreo del rayo cada 0,5 m (1 m antes del panel si no se detecta roca), y se registra en un plano computacional de 600 m si su energía cinética supera 3 GeV, con malla `az-edges-v1` ([receta](../../contratos/receta-operativa-siete-actividades.json), [ficha](../../FICHA_CONJUNTO_OE1.md)). Los controles documentados son estos ([puntos no demostrados](PUNTOS_NO_DEMOSTRADOS.md), [campaña](RESULTADOS_CAMPANA_114.md)):

- **Independencia del plano (C1, C5):** con inyección junto a la roca y corte de 3 GeV, la razón de conteos 100 m/600 m es al menos 0,9895 ± 0,0025 en todas las bandas de roca; se conserva el 83,5 % del conteo en roca. Entre 600 y 1.200 m la diferencia es 0 pp.
- **Aire previo (C2):** sin corte, la eficiencia de cielo abierto es del 99,97 % (fila mínima 99,69 %). Así se evita descontar dos veces el aire de un espectro de nivel del mar.
- **Bordes (C4 y campaña):** con margen de 5°, el sesgo medio de borde es −0,07 pp sin corte. En la campaña, las 1.710 regiones de borde quedan dentro de ±1 pp frente a la referencia ideal de cielo, con un extremo máximo de 0,933 pp.

Estos controles respaldan que, con inyección junto a la roca y corte de 3 GeV, la imagen no depende del tamaño del plano entre 100 y 1.200 m, y que los bordes de la campaña concuerdan con la referencia ideal. Antes de la campaña, C4 quedó abierto con el criterio estricto (desviación máxima de 1,65 pp sin corte; 1,64 pp y 2,84 pp sobre la imagen con E > 3 GeV en los diagnósticos c01 y c02), y C2 se cumple solo sin corte. Ninguno de estos controles establece equivalencia con el panel. No representan secundarios, aire antes de la roca (salvo 1 m), respuesta de detector ni fondo experimental. La referencia de cielo no incluye pérdidas en aire, decaimiento, dispersión ni migración angular. C1 se evaluó en una sola geometría homogénea y una vista. Con el corte, el conteo en roca resultó 0,57–0,85 veces la expectativa CSDA, una diferencia que no se analizó.

## 5. Estadística

Cada vista recibió 344.000.000 primarios en nueve bloques, con 1.026 bloques en total ([ficha](../../FICHA_CONJUNTO_OE1.md)). Los conteos con corte por vista van de 115.272.159 a 121.975.257, y la etiqueta convencional de exposición, de 195,92 a 195,95 días convencionales, sin significado de días reales ([metadatos de fusión](datos/sc3/campana-114/fusion/)).

La meta descriptiva de al menos 90 % de ROI con 100 cuentas se cumple en 107/114 vistas. Globalmente, 20.713/21.816 ROI la alcanzan (94,944 %). Las siete excepciones, entre 89,19 % y 89,81 %, se conservaron conforme al [acuerdo previo](ACUERDO_CAMPANA_114.md).

Las realizaciones reducidas se obtienen por adelgazamiento binomial con fracciones 0,50; 0,10; 0,05 y 0,01, veinte por fracción y semilla maestra 20260805. El resultado son 9.120 pares. Es el submuestreo previsto en el plan, siguiendo a O'Donnell et al. (2025). Por construcción, cada conteo reducido conserva en promedio la fracción f de la referencia; pero las realizaciones comparten la misma referencia finita y no equivalen a corridas independientes de f·N primarios ([definición](../../DEFINICION_PRODUCTO_OE1.md)).

## 6. Limitaciones y extensiones fuera del alcance

- **Equivalencia instrumental:** en `geo-train-01`, vista 0, solo entre el 3,6 % y el 70,4 % de los registros con E > 3 GeV del plano de 600 m caen en el panel de 1,2 m, según la banda de elevación ([README](README.md)). Afirmar que las imágenes son las de ese detector exigiría el control C3, con fuente amplia, aceptación y resolución.
- **Topografía real:** un escenario como el Cerro Machín requeriría incorporar su topografía y densidades. El repositorio no lo contiene, y `referencias.bib` no tiene una entrada citable para él.
- **Física omitida:** secundarios, aire previo, fondo, alteración hidrotermal y variabilidad de la densidad de la roca.
- **Calibración:** el flujo absoluto y la exposición en días reales no están calibrados.

Son extensiones posibles, no obligaciones del alcance adoptado. La conversión `dataset-v2` y el entrenamiento de modelos quedan fuera del OE1.

## 7. Conclusión acotada

La evidencia documentada respalda que el conjunto es representativo dentro de la familia idealizada. Cubre tres tipos de anomalía con contrastes de ambos signos, solos y combinados; opacidades desde cielo abierto hasta columnas altas; seis direcciones de observación; y una fuente y un transporte únicos y trazables, con controles de plano, aire y bordes en el alcance descrito en la sección 4. No respalda la reproducción de un volcán concreto, un flujo calibrado ni la equivalencia con un detector. La valoración académica final corresponde a la dirección.

### Claves BibTeX utilizadas

`tanaka2007asama`, `olah2018sakurajima`, `tanaka2023muography`, `guan2015muonflux`, `pagano2021ecomug`, `agostinelli2003geant4`, `odonnell2025particles`.

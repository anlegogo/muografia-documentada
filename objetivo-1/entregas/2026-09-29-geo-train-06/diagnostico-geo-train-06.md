# Diagnóstico geométrico — geo-train-06

## 1. Resumen

`geo-train-06` combina un conducto vertical (anomalía 0) y un cuerpo denso elipsoidal (anomalía 1) cuyas regiones se intersectan en un volumen de 83 641,9 ± 44,7 m³ (auditoria-geometrica-oe1.json, `geometries[geo-train-06].pairs[0]`). El motor analítico y la construcción Geant4 recibida no representan el mismo campo de materiales en esa región: el primero recorta y asigna la densidad de la anomalía posterior en el orden del JSON; el segundo coloca ambos sólidos como hermanos completos, sin recorte, lo que deja la navegación indefinida donde se superponen. La corrección adoptada (B1) reproduce en Geant4 la regla que el motor analítico ya aplica. El defecto y otros cinco de la misma naturaleza en el catálogo (intersecciones o salidas del edificio) fueron confirmados de forma independiente en `auditoria-oe1.json` y coinciden en las 19 geometrías con el cálculo presentado aquí.

## 2. Geometría

| Elemento | Parámetro | Valor |
|---|---|---|
| Edificio | forma | cono |
| | radio de base (R) | 509,7 m |
| | altura (H) | 416,3 m |
| | densidad de roca | 2,65 g/cm³ |
| Conducto (anomalía 0) | densidad | 1,832 g/cm³ |
| | centro (x, y) | (20,3; −24,5) m |
| | radio | 21,0 m |
| | rango z | 0,0 – 340,0 m |
| | volumen analítico | 471 050,4 m³ |
| Cuerpo denso (anomalía 1) | densidad | 3,285 g/cm³ |
| | centro (x, y, z) | (32,2; −74,1; 137,8) m |
| | semiejes (ax, ay, az) | (72,9; 61,6; 64,6) m |
| | volumen analítico | 1 215 148,5 m³ |

(auditoria-geometrica-oe1.json, `geometries[geo-train-06].edifice` y `.volumes`)

Convención de coordenadas: el mundo tiene z = 0 en la base del edificio y z = H en el vértice. El motor analítico usa un cono de vértice de radio 0 (`scripts/simulation/surrogate/geometry.py`, método `density`, superficie `z = H·(1 − r/R)`). Geant4 construye el edificio como un `G4Cons` con radio de base R en z = 0 y radio de vértice 0,1 m en z = H (`scripts/simulation/geant4_app/src/DetectorConstruction.cc`, líneas 56–61), de modo que su radio de cono es `R_G4(z) = R − (R − 0,1)·z/H`. El sólido `G4Cons` se coloca con su centro en el marco local en z_mundo = H/2; las anomalías, colocadas como hijas de ese volumen, trasladan su coordenada z restando H/2 (mismo archivo, líneas 64–93).

## 3. Defecto

**Intersección conducto–cuerpo denso.** Sobre 4 000 000 de muestras uniformes en la caja envolvente común, 1 868 350 cayeron dentro de ambos sólidos: volumen = 83 641,9 ± 44,7 m³ (error estándar binomial), rango z = 81,27 – 194,23 m, centroide = (21,36; −30,71; 137,81) m. La intersección representa el 17,76 % del volumen del conducto y el 6,88 % del volumen del cuerpo denso. El punto testigo con mayor margen mínimo simultáneo (convención propia: 1 en el centro de cada sólido, 0 en su superficie, negativo fuera) es (22,61; −37,17; 137,51) m, con margen 0,624 respecto al conducto y 0,623 respecto al cuerpo denso — es decir, un punto interior a ambos sólidos con holgura comparable frente a las dos superficies, no un caso límite. (auditoria-geometrica-oe1.json, mismo bloque de pares.)

**Contención en el edificio.** Ambas anomalías están contenidas en el cono Geant4 (apex 0,1 m): el conducto con un margen radial de 40,68 m en su extremo superior (z = 340,0 m; frente al cono analítico, 40,60 m); el cuerpo denso queda entre z = 73,2 m y z = 202,4 m, ambos dentro de [0; 416,3] m, sin exceso radial detectado sobre una parametrización de su superficie con 1 440 × 721 puntos (paso angular de 0,25°). Ninguna de las dos anomalías sale del edificio: el defecto es exclusivamente la intersección entre ellas.

## 4. Evidencia histórica

El registro `b-09-0-29628.out` (vista 0 de `geo-train-06`, campaña recuperada) contiene:

```
Checking overlaps for volume anomaly_1:0 (G4Ellipsoid) ...
-------- WWWW ------- G4Exception-START -------- WWWW -------
*** G4Exception : GeomVol1002
      issued by : G4PVPlacement::CheckOverlaps()
Overlap with volume already placed !
          Overlap is detected for volume anomaly_1:0 (G4Ellipsoid) with anomaly_0:0 (G4Tubs)
          overlap at local point (1087.52,1032.69,-67723.2) by 19.5003 m   (max of 91 cases)
NOTE: Reached maximum fixed number -1- of overlaps reports for this volume !
*** This is just a warning message. ***
-------- WWWW -------- G4Exception-END --------- WWWW -------
```

seguido, sin interrupción de la corrida, por:

```
RUN DONE geo-train-06 view 0: events=36174382 detected=27209253 wall_s=1064.67
```

La misma advertencia (`Overlap is detected for volume anomaly_1:0 (G4Ellipsoid) with anomaly_0:0 (G4Tubs)`) aparece en los seis registros de la campaña para esta geometría (`b-09-0-29628.out` a `b-09-5-29637.out`, vistas 0 a 5), consistente con una intersección propia de la geometría y no de una vista particular. El punto muestreado por el control de superposición de Geant4 (a 19,5003 m de exceso, en el marco local del sólido) es independiente del punto testigo de esta auditoría y no es directamente comparable con él: uno reporta la penetración de un punto de muestreo del control de superposición, el otro un punto interior con margen máximo simultáneo.

## 5. Qué hace cada motor

**Motor analítico.** Para cada punto evalúa primero si está dentro del cono (vértice de radio 0); si lo está, asigna la densidad de roca y luego recorre las anomalías en el orden del JSON, sobrescribiendo la densidad con la de cada anomalía cuya región contiene al punto (`scripts/simulation/surrogate/geometry.py`, método `density`). Como el cuerpo denso es la anomalía de mayor índice (1), su densidad —3,285 g/cm³— prevalece en toda la intersección. Esta es una regla de prioridad determinista y sin ambigüedad.

**Geant4 recibido.** Cada anomalía se construye como un sólido completo (`G4Tubs`, `G4Orb` o `G4Ellipsoid`) y se coloca como hija del volumen del edificio, hermana de las demás anomalías, sin recorte ni sustracción entre ellas (`DetectorConstruction.cc`, líneas 67–93). El control de superposición (`pSurfChk`, invocado vía `G4PVPlacement::CheckOverlaps()`) sólo emite la advertencia `GeomVol1002` señalada en la sección 4; no impide la construcción ni resuelve qué material ve el transporte en la región compartida. Qué densidad se aplica ahí depende del orden en que el navegador de Geant4 visita los volúmenes hermanos superpuestos, que no está definido por la geometría — de ahí que el material en esa región se reporte como indeterminado.

## 6. Decisión B1 e interpretación física

La corrección adoptada (B1) define la región de cada anomalía como `anomalía_i = (A_i ∩ cono) − ⋃_{j>i} A_j`: cada anomalía se recorta al edificio y, además, se sustrae la unión de todas las anomalías de índice posterior. El JSON del catálogo no se modifica; sólo cambia cómo se construyen los sólidos a partir de él. Para `geo-train-06`, esto hace que el cuerpo denso (índice 1, posterior) ocupe íntegramente la intersección, y que el conducto (índice 0) quede interrumpido —reemplazado por el cuerpo denso— entre z ≈ 81,3 m y z ≈ 194,2 m, el rango z de la intersección medido en la sección 3. Físicamente, la columna de material a lo largo del eje del conducto no es homogénea en ese tramo: una intrusión más densa ocupa el volumen que de otro modo sería conducto.

Esta regla es la misma que ya aplica el motor analítico usado para diseñar el catálogo (sección 5), de modo que B1 hace que Geant4 y el motor analítico compartan el mismo campo de materiales. La comparación entre ambos (`consistency_b1_vs_analytic` en el JSON) evaluó 5 868 350 puntos —los usados en el muestreo de la sección 3 más un muestreo uniforme adicional de la caja envolvente conjunta de las anomalías— y encontró 355 discrepancias (0,006 % de los puntos), todas explicadas por la franja donde el cono de Geant4 (vértice 0,1 m) y el cono analítico (vértice 0) difieren; ninguna discrepancia quedó sin explicar. La regla B1 es única y se aplica igual a las seis geometrías defectuosas del catálogo, incluidas las que presentan salida lateral del edificio (sección 9): en esos casos, el recorte al cono elimina la parte de la anomalía que sobresale, sin necesidad de una regla adicional.

Construcción CSG: cada anomalía se instancia como intersección booleana (`G4IntersectionSolid`) entre su sólido y el cono del edificio, y luego como sustracción booleana (`G4SubtractionSolid`) de cada anomalía de índice posterior, en el marco local del cono (la misma traslación z_local = z_mundo − H/2 ya usada para las posiciones). Cuando la sustracción o la intersección resultan en un sólido vacío para una anomalía dada —no ocurre en `geo-train-06`, donde ambas anomalías conservan volumen positivo tras el recorte—, esa anomalía no se coloca como volumen físico.

## 7. Alternativas B2 y B3

**B2 — prioridad al conducto.** En vez de que la anomalía posterior prevalezca, el conducto ganaría la intersección frente a cualquier anomalía superpuesta. Para `geo-train-06` esto asignaría 1,832 g/cm³ (la densidad del conducto) en la región de 83 641,9 m³ que hoy se resuelve como 3,285 g/cm³ bajo B1. Cambia el campo de materiales sin cambiar el catálogo, pero deja de coincidir con la regla que el motor analítico ya aplica al mismo JSON (sección 5), por lo que introduciría una divergencia nueva entre motores en vez de resolver la existente.

**B3 — reubicar el cuerpo denso.** Se calculó el desplazamiento horizontal mínimo del centro del cuerpo denso, a lo largo de la dirección desde el eje del conducto hacia su centro actual, que elimina el solape. En la sección transversal más ancha del elipsoide (z = 137,8 m, semiejes ecuatoriales 72,9 × 61,6 m) frente al disco del conducto (radio 21,0 m), el desplazamiento mínimo es s* = 32,114 m, obtenido con la distancia exacta punto–elipse (búsqueda de raíz por bisección, sin asumir que el punto más cercano de la elipse esté sobre la línea de centros). El valor de holgura cerrado en s* es del orden de 10⁻¹⁴ m (prácticamente tangente, dentro del error de redondeo de punto flotante). Como verificación independiente por muestreo, un muestreo Monte Carlo de 200 000 puntos halla 0 puntos superpuestos en s* y 19 de 200 000 puntos superpuestos 0,5 m antes de s* (auditoria-geometrica-oe1.json, `detail.b3_mc_verification`). El nuevo centro quedaría en (39,69; −105,33) m. Adoptar B3 cambia un parámetro publicado del catálogo (el centro del cuerpo denso), por lo que exigiría una nueva versión del archivo JSON y, con ella, una nueva identidad de la geometría; no es una corrección de construcción sino un cambio del escenario físico representado.

## 8. Efecto esperado de orden de magnitud

Para la vista 0 (detector en (1 000,0; 0,0; 1,5) m, mirando hacia el centroide de la intersección), la línea de visión recta desde el detector hasta ese punto atraviesa: 698,95 m de cuerda total dentro del cono, de los cuales 596,52 m son roca exclusiva, 40,49 m corresponden al conducto (íntegramente compartidos con el cuerpo denso en este tramo de la línea) y 61,94 m son cuerpo denso exclusivo. Bajo B1, la columna de densidad es de 191 726,0 g/cm²; bajo B2, de 185 842,7 g/cm². La diferencia es de 5 883,4 g/cm² (3,07 % relativo), consistente con Δρ = 1,453 g/cm³ (3,285 − 1,832) multiplicado por los 40,49 m de cuerda compartida. Esta es una estimación en línea recta: no incorpora dispersión múltiple, ni la eficiencia de detección real, ni el promedio angular real de una medición muográfica; sirve para fijar el orden de magnitud del efecto de la decisión B1 frente a B2 en un tramo, no para predecir un mapa de detección.

## 9. Tabla de las 19 geometrías con defectos

De las 19 geometrías del catálogo, seis presentan un defecto demostrado. El cálculo de este documento coincide con la auditoría del repositorio de revisión (`auditoria-oe1.json`) en las 19 geometrías, sin excepción.

| Geometría | Defecto | Este cálculo | Auditoría de revisión | Coincide |
|---|---|---|---|---|
| geo-gen-01 | conducto (0) sale lateralmente del edificio | exceso 15,1494 m en z = 386,5 m | exceso ≈ 15,1494 m | sí |
| geo-test-01 | conducto (0) y cavidad (1) se intersectan | volumen 6 888,8 m³ (k = 625 092 / 4 000 000) | intersección con testigo interior | sí |
| geo-test-03 | conducto (0) sale lateralmente; anomalía 2 cruza la base | exceso 10,3591 m en z = 344,9 m; z mínimo de la anomalía 2 = −5,10 m | exceso ≈ 10,3591 m; z mínimo −5,10 m | sí |
| geo-train-06 | conducto (0) y cuerpo denso (1) se intersectan | volumen 83 641,9 ± 44,7 m³ | intersección con testigo interior | sí |
| geo-train-08 | conducto (0) y cuerpo denso (2) se intersectan | volumen 111 691,4 m³ (k = 1 524 588 / 4 000 000) | intersección con testigo interior | sí |
| geo-train-11 | anomalías 0 y 1 se intersectan | volumen 28 900,7 m³ (k = 1 212 821 / 4 000 000) | intersección con testigo interior | sí |

Las 13 geometrías restantes (geo-test-02, geo-train-01 a 05, 07, 09, 10, 12, geo-val-01 a 03) no presentan intersección entre anomalías ni salida del edificio en ninguno de los dos cálculos; la mayoría se certifica por cajas envolventes disjuntas o por una distancia analítica exacta esfera–esfera o esfera–conducto, no sólo por la ausencia de muestras Monte Carlo positivas.

## 10. Límites

El volumen y los rangos de la intersección de la sección 3 son estimaciones Monte Carlo (error estándar binomial reportado junto a cada valor); no son cálculos analíticos cerrados, salvo la contención del conducto y las distancias de separación entre esferas y entre esfera y conducto, que sí son exactas. La diferencia de 0,1 m entre el vértice del cono de Geant4 y el vértice del cono analítico introduce una franja de volumen pequeño pero no nulo donde ambos motores pueden diferir; se cuantificó en la sección 6 y no afecta la conclusión sobre la intersección conducto–cuerpo denso, muy alejada del vértice. Este documento no simula navegación de Geant4 ni transporte de partículas: los números de la sección 8 son geométricos, no un resultado de corrida. La decisión B1 se contrasta después con el control geométrico del catálogo corregido y con el piloto comparativo de simulación A/B (geometría recibida frente a corregida); este documento cubre únicamente el diagnóstico geométrico de `geo-train-06` y la comparación con el catálogo completo.

## 11. Reproducción

```
python scripts/analysis/oe1_geometry_audit.py \
  --out muografia-documentada/objetivo-1/entregas/2026-09-29-geo-train-06/diagnostico/auditoria-geometrica-oe1.json
```

ejecutado desde la raíz del repositorio `muography-dl-reconstruction`, con los valores por defecto: semilla = 20260929, N = 4 000 000 muestras por par de anomalías, catálogo en `scripts/simulation/geometry_catalog/geometries/`. Sha-256 del script: `d6f92664096b800d0860acd0f585d97c1f6d6616df1bb7f89786d76e7c22382c`. Sha-256 de `geo-train-06.json`: `c8f6c1352af1f7564356cffbd98e26fd6a5881e5ece15a0ab6f2ed60c8ea26ed`. Script versionado en el repositorio de código `muography-dl-reconstruction`, rama `fix/oe1-geometry-csg`, commit `18dd1fc` (base `b88fa57`). La salida completa, con metadatos de entorno (versión de Python y de NumPy) y el detalle por geometría, queda en `diagnostico/auditoria-geometrica-oe1.json`; la salida de consola, en `diagnostico/auditoria-geometrica-oe1.txt`.

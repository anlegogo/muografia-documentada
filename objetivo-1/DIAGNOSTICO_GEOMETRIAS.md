# Diagnóstico local de las geometrías del OE1

## Resultado

Se identificaron defectos geométricos en **seis de las 19 geometrías**, coincidentes con las seis identificadas en los logs históricos. Cuatro contienen intersecciones entre anomalías; dos contienen anomalías que sobresalen del edificio. `geo-test-03` presenta dos salidas distintas. No se ha cuantificado todavía el efecto sobre los conteos.

| Geometría | Defecto demostrado | Evidencia local |
|---|---|---|
| geo-train-06 | Conducto 0 y cuerpo denso 1 intersectan | Punto interior común `(21.6125, -37.25, 137.8)` m. |
| geo-train-08 | Conducto 0 y anomalía 2 intersectan | Punto interior común `(46.04375, -3.425, 160.9)` m. |
| geo-train-11 | Anomalías 0 y 1 intersectan | Punto interior común `(-12.18125, -9.14375, 133.0)` m. |
| geo-test-01 | Conducto 0 y cavidad 1 intersectan | Punto interior común `(-29.26875, -27.63125, 155.4)` m. |
| geo-gen-01 | Conducto 0 sobresale lateralmente del cono | Exceso radial en su extremo superior: aproximadamente 15,1494 m. |
| geo-test-03 | Conducto 0 sobresale lateralmente; anomalía 2 cruza la base | Exceso radial superior: aproximadamente 10,3591 m; cota mínima de anomalía 2: −5,1 m. |

Índices desde cero, como `anomaly_0` en Geant4. Los excesos radiales son medidas analíticas a altura fija, no distancias normales a la superficie ni las profundidades aleatorias impresas en los logs.

## Método y límites

La herramienta [auditar_oe1.py](../herramientas/auditar_oe1.py) usa los parámetros JSON y las formas alineadas del código recibido. Para las intersecciones busca puntos estrictamente interiores a ambos sólidos; cada testigo se valida con las desigualdades de las formas. Para separación utiliza cajas envolventes y, cuando corresponde, distancias exactas esfera/esfera o esfera/cilindro. Una malla sin testigo se declara no resuelta, nunca separada automáticamente.

Para contención, el radio Geant4 es `R(z)=R−(R−0,1)z/H`, pues su vértice tiene radio 0,1 m. Para un conducto vertical, el máximo radio ocupado es `sqrt(cx²+cy²)+r`; compararlo con el radio del cono en `z1` prueba las salidas laterales. Para esferas y elipsoides se usan cotas suficientes y extremos verticales. Los contactos exactamente en z=0 se registran por separado; no se clasifican por sí solos como salida.

La evidencia por cada una de las 19 geometrías está en [auditoria-oe1.json](evidencias/auditoria-oe1.json). Los controles locales no simulan tolerancias, navegación, dispersión ni otras colocaciones del detector. La ausencia de defectos en este análisis acotado no certifica toda la geometría Geant4.

## Causa en el código recibido

- [DetectorConstruction.cc](originales/scripts/simulation/geant4_app/src/DetectorConstruction.cc), líneas 56–61: construcción y colocación del edificio.
- Mismo archivo, líneas 76–91: las anomalías se construyen completas y se colocan como hijas hermanas del cono; no hay recorte ni sustracción de sus intersecciones.
- [geometry.py](originales/scripts/simulation/surrogate/geometry.py), líneas 65–66: el motor analítico recorta las anomalías al edificio y la última anomalía de la lista prevalece donde coinciden varias.

Por tanto, **compartir un JSON no garantiza que ambos motores representen el mismo campo de materiales**. El orden de asignación del motor analítico constituye una regla de prioridad; los sólidos hermanos superpuestos de Geant4 no implementan esa regla.

La documentación de [Geant4](https://geant4.web.cern.ch/documentation/dev/bfad_html/ForApplicationDevelopers/Detector/Geometry/geomOverlap.html) distingue tanto intersecciones entre volúmenes hermanos como salidas de una hija de su madre. Su control por muestreo tiene resolución configurable; terminar la corrida no resuelve una advertencia de geometría.

## Caso inicial propuesto

`geo-train-06`, vista 0. El log recibido `b-09-0-29628.out` informa una intersección entre `anomaly_1` y `anomaly_0` de 19,5003 m en un punto muestreado, y después `RUN DONE`. Esto permite relacionar defecto del catálogo, construcción y ejecución histórica. El punto interior de la auditoría es independiente del punto muestreado por Geant4.

Seguir las [instrucciones para estudiantes](INSTRUCCIONES_ESTUDIANTES.md). No se ha movido una anomalía ni modificado una densidad por iniciativa de esta auditoría: debe justificarse primero el escenario físico pretendido.

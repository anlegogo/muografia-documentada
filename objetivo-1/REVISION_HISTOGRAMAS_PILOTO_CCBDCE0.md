# Revisión de histogramas del piloto — ccbdce0

2026-10-02, Colombia. Se revisó la entrega estudiantil `ccbdce0` de la rama `oe1/justificacion-fisica-produccion`. La revisión se limita al piloto de geo-train-06, con seis vistas y 211 millones de primarios por vista; no autoriza la campaña.

## Verificación realizada

- Se extrajeron los archivos mediante `git archive --format=zip ccbdce0`, preservando los bytes Git. Coinciden las 27 huellas de los inventarios `fusion.sha256` e `imagenes.sha256`, publicados previamente en `b125cb3`.
- Se repitió `herramientas/evaluar_piloto_angular.py` sobre la carpeta `fusion`, con el diseño congelado `evidencias/piloto-propuesto-siete-actividades/diseno-piloto.json` y la referencia `evidencias/preparacion-siete-actividades/cielo-ideal-margen-5.json`. Se verifican N, semillas, geometría, tablas, máscaras y receta exigidos por el evaluador.
- Coinciden la estructura, los conteos y las decisiones del JSON recibido. La mayor diferencia numérica es 2,95 × 10⁻¹⁴, inferior a la tolerancia absoluta de comparación 10⁻¹⁰. Una primera comparación con igualdad binaria de todos los flotantes detectó estas diferencias de redondeo; no se encontró una discrepancia científica.
- Las seis imágenes NPZ contienen exactamente los conteos uint32 y coordenadas de sus CSV, sin remuestreo ni saturación.
- Entorno local: Python 3.12.14, NumPy 2.4.4 y SciPy 1.18.1. No se ejecutó Geant4 ni se reconstruyeron los 36 bloques individuales: se verificaron los productos fusionados entregados.

[Verificación y estadísticas](evidencias/revision-piloto-ccbdce0/verificacion.json) · [Evaluación local completa](evidencias/revision-piloto-ccbdce0/evaluacion-local.json).

## Resultados confirmados

Las 90 regiones de borde cumplen el criterio simultáneo establecido para las seis vistas del piloto. Esto respalda ese criterio para esta geometría, sin extender automáticamente su cobertura estadística a 114 vistas.

| Vista | Mediana de cuentas en ROI | Percentil 10 | ROI con ≥100 cuentas | Proyección lineal a 344 M: ROI con ≥100 |
|---:|---:|---:|---:|---:|
| 0 | 122 | 63,3 | 63,93 % | 93,03 % |
| 1 | 127 | 62,0 | 63,11 % | 90,98 % |
| 2 | 121 | 62,0 | 65,16 % | 90,16 % |
| 3 | 123,5 | 63,0 | 63,93 % | 90,57 % |
| 4 | 127 | 63,3 | 63,11 % | 90,98 % |
| 5 | 126 | 61,3 | 63,11 % | 89,75 % |

Se usan 244 ROI de 4 × 4 píxeles por vista, seleccionadas por columna nominal del cono homogéneo. No son estadísticas por píxel ni de toda la imagen. Las anomalías forman parte del transporte, aunque no de la selección de ROI.

## Interpretación de 211 M frente a 344 M

La propuesta de 344 M tiene respaldo como dimensionamiento aproximado: escalar las cuentas observadas por 344/211 sitúa alrededor del 90 % de las ROI por encima de 100. En la vista 5 queda 89,75 % y el percentil 10 proyectado es 99,94. Por tanto, no debe presentarse como garantía de que todas las vistas superarán un umbral exacto del 90 %. El cálculo 211 × 100/61,3 da 344,21 M, pero redondearlo tampoco resuelve la incertidumbre estadística ni las diferencias entre geometrías.

La proyección multiplica conteos observados; no simula una realización nueva ni incorpora incertidumbre predictiva. La mejora aproximada del ruido relativo al pasar de 211 a 344 M es del 22 %, a cambio de un 63 % más de transporte. Los 100 conteos y el 90 % son una propuesta de suficiencia para regiones agregadas, no requisitos originales aprobados ni una referencia sin ruido.

Se recomienda conservar 344 M por vista como presupuesto candidato si se prioriza mejorar las referencias en roca. Antes de emitir el manifiesto definitivo deben quedar registrados el criterio de suficiencia aceptado, el presupuesto y la evaluación por geometría. El criterio simultáneo del piloto cubre seis vistas; si se pretende una afirmación simultánea para las 114, su evaluación debe definirse antes de ejecutar. No se propone otra simulación para repetir la verificación ya completada.

La referencia futura sigue siendo finita y ruidosa; los 9.120 pares por adelgazamiento no equivalen a realizaciones independientes de referencias sin ruido. La representatividad de los escenarios y las limitaciones de fuente/transporte permanecen documentadas en la definición del producto.

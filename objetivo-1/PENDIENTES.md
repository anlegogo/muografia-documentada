# Pendientes del OE1

Estado consolidado al 2026-10-02, Colombia. **P-01 a P-04 continúan abiertos**, con avances diferentes. La integración angular en SC3 ya fue recibida y revisada; no sigue pendiente repetir la prueba de 1.000 muones.

| ID | Avance respaldado | Qué falta para cerrar |
|---|---|---|
| P-01 · geometría y datos corregidos | Se identificaron seis geometrías afectadas; se recibió evidencia de controles geométricos de B. Etapas 1, complemento y etapa 2 revisados; se cuantificó el efecto observado en el caso estudiado, con resultado estadístico inconcluso. | Decidir el alcance de sustitución y producir referencias compatibles con la definición final. No extrapolar equivalencia a todo el catálogo ni mezclar mallas antiguas y nuevas. |
| P-02 · entorno reproducible | Receta SC3 ampliada recibida: Geant4 11.4.2, GCC 14.2.0, versiones de datos físicos y configuración de compilación. Entorno Python de análisis documentado. | Fijar la versión de producción y revisar su trazabilidad de extremo a extremo. No declarar equivalente el Docker histórico 11.3.2. |
| P-03 · reproducción de la cadena | Se reprodujeron los 9.120 pares históricos y se implementó una alternativa local versionada para lectura, ROI, representación y empaquetado, con 41 pruebas. | Lanzador y fusión recibidos con prueba SC3; corregir T-01/T-02/T-03 de la revisión del 2 de octubre y fijar ficha definitiva. |
| P-04 · aceptación y normalización física | Malla angular corregida y comprobada; regiones analíticas contrastadas; discrepancia conceptual entre convergencia del plano y aceptación del panel delimitada. | Justificar el observable, el plano de 600 m, generación espacial, aceptación angular y relación de conteos con exposición. Revisar respaldo existente y definir un control dirigido solo si es necesario. |

El pendiente principal es P-04. Ya se recibió respaldo de SC3 y una configuración candidata, pero la convergencia de planos grandes no demuestra equivalencia con el panel físico.

## Siguiente entrega necesaria

La entrega `f9a77ef` fue revisada: [resultados, observaciones y responsables](REVISION_FISICA_PRODUCCION_2026-10-02.md). Corregir los finales de línea/huellas, la validación y agregación de bloques, y la compatibilidad de la nueva configuración. Precisar observable y normalización; el criterio de bordes sigue abierto. No repetir genéricamente la solicitud anterior ni lanzar la campaña grande. Decidir P0 después de revisar esos puntos.

## Evidencia de referencia

- [Corrida angular de 1.000 primarios](REVISION_MALLA_ANGULAR_2026-10-01.md).
- [Auditoría completa de etapa 2](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md).
- [Aceptación del plano](REVISION_ACEPTACION_PLANO.md).
- [Diagnóstico de geometrías](DIAGNOSTICO_GEOMETRIAS.md).
- [Preparación de producción](PREPARACION_PRODUCCION_OE1.md).

Las seis geometrías históricamente afectadas son geo-gen-01, geo-test-01, geo-test-03, geo-train-06, geo-train-08 y geo-train-11. El plan de 36 referencias sustituidas y 78 reutilizadas era condicional a conservar el observable y la malla. La adopción de az-edges-v1 obliga a revisar esa compatibilidad; no autoriza reutilización por cambiar las etiquetas.

Las observaciones históricas y sus fechas se conservan en la [bitácora](BITACORA.md), los informes correspondientes y el historial Git. Esta página expresa el estado actual, no una nueva calificación académica.

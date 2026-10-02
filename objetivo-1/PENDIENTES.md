# Pendientes del OE1

Estado consolidado al 2026-10-01, Colombia. **P-01 a P-04 continúan abiertos**, con avances diferentes. La integración angular en SC3 ya fue recibida y revisada; no sigue pendiente repetir la prueba de 1.000 muones.

| ID | Avance respaldado | Qué falta para cerrar |
|---|---|---|
| P-01 · geometría y datos corregidos | Se identificaron seis geometrías afectadas; se recibió evidencia de controles geométricos de B. Etapas 1, complemento y etapa 2 revisados; se cuantificó el efecto observado en el caso estudiado, con resultado estadístico inconcluso. | Decidir el alcance de sustitución y producir referencias compatibles con la definición final. No extrapolar equivalencia a todo el catálogo ni mezclar mallas antiguas y nuevas. |
| P-02 · entorno reproducible | Registros SC3 respaldan Geant4 11.4.2 y GCC 14.2.0 en la corrida angular; código y tablas coinciden con el parche. Entorno Python de análisis documentado. | Completar receta de compilación y paquetes de datos físicos, bibliotecas/opciones y configuración de producción. No declarar equivalente el Docker histórico 11.3.2. |
| P-03 · reproducción de la cadena | Se reprodujeron los 9.120 pares históricos y se implementó una alternativa local versionada para lectura, ROI, representación y empaquetado, con 41 pruebas. | La alternativa de transporte/ejecución de campaña final y su ficha definitiva aún no están fijadas; recuperar antecedentes que sean necesarios para justificar física y operación. |
| P-04 · aceptación y normalización física | Malla angular corregida y comprobada; regiones analíticas contrastadas; discrepancia conceptual entre convergencia del plano y aceptación del panel delimitada. | Justificar el observable, el plano de 600 m, generación espacial, aceptación angular y relación de conteos con exposición. Revisar respaldo existente y definir un control dirigido solo si es necesario. |

El pendiente principal es P-04. Las herramientas no pueden sustituir una definición física ni producir el respaldo de SC3 que aún no está compartido.

## Siguiente entrega necesaria

Solicitar los archivos, comandos, semillas y conteos de la convergencia de planos 100/300/600 m y de cualquier tamaño adicional, junto con la explicación de qué representa la imagen y cómo se normaliza el conteo. Añadir la receta del entorno y ejecución. **No pedir otra corrida de integración angular ni una campaña grande todavía.**

La [cadena local](CADENA_LOCAL_OE1.md) contiene el procedimiento y el mensaje preparado. La búsqueda en la historia disponible no localizó el runbook ni el paquete específico de convergencia; eso no prueba que no existan en SC3.

## Evidencia de referencia

- [Corrida angular de 1.000 primarios](REVISION_MALLA_ANGULAR_2026-10-01.md).
- [Auditoría completa de etapa 2](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md).
- [Aceptación del plano](REVISION_ACEPTACION_PLANO.md).
- [Diagnóstico de geometrías](DIAGNOSTICO_GEOMETRIAS.md).
- [Preparación de producción](PREPARACION_PRODUCCION_OE1.md).

Las seis geometrías históricamente afectadas son geo-gen-01, geo-test-01, geo-test-03, geo-train-06, geo-train-08 y geo-train-11. El plan de 36 referencias sustituidas y 78 reutilizadas era condicional a conservar el observable y la malla. La adopción de az-edges-v1 obliga a revisar esa compatibilidad; no autoriza reutilización por cambiar las etiquetas.

Las observaciones históricas y sus fechas se conservan en la [bitácora](BITACORA.md), los informes correspondientes y el historial Git. Esta página expresa el estado actual, no una nueva calificación académica.

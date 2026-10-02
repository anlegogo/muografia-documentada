# Pendientes del OE1

> Estado actual: [revisión 01a9871](REVISION_INTEGRACION_OBSERVABLE_01A9871.md). Prueba de herramientas sobre dos bloques en SC3 aceptada; 78 pruebas locales previas. Definición física propuesta, con ajustes de referencia de cielo y diseño estadístico pendientes.

> Datos ya reanalizados: [panel/plano y bordes con corte de energía](DIAGNOSTICO_OBSERVABLE_Y_DECISION.md). La siguiente decisión está acotada a la definición física; no pedir otra comparación 100/600 para repetir lo ya demostrado.

> La prueba recibida cubre publicación, fusión y exportación de dos bloques; falta su integración en el lanzador automático de campaña. No repetir la comprobación ya recibida.

Estado consolidado al 2026-10-02, Colombia. **P-01 a P-04 continúan abiertos**, con avances diferentes. La integración angular en SC3 ya fue recibida y revisada; no sigue pendiente repetir la prueba de 1.000 muones.

| ID | Avance respaldado | Qué falta para cerrar |
|---|---|---|
| P-01 · geometría y datos corregidos | Se identificaron seis geometrías afectadas; se recibió evidencia de controles geométricos de B. Etapas 1, complemento y etapa 2 revisados; se cuantificó el efecto observado en el caso estudiado, con resultado estadístico inconcluso. | Decidir el alcance de sustitución y producir referencias compatibles con la definición final. No extrapolar equivalencia a todo el catálogo ni mezclar mallas antiguas y nuevas. |
| P-02 · entorno reproducible | Receta SC3 ampliada recibida: Geant4 11.4.2, GCC 14.2.0, versiones de datos físicos y configuración de compilación. Entorno Python de análisis documentado. | Fijar la versión de producción y revisar su trazabilidad de extremo a extremo. No declarar equivalente el Docker histórico 11.3.2. |
| P-03 · reproducción de la cadena | Se reprodujeron los 9.120 pares históricos. Cadena local ampliada a 78 pruebas; publicación/fusión/exportación verificadas en SC3 con dos bloques. T-01 aclarado: objetos Git íntegros. | Integrar herramientas en el lanzador automático de producción y fijar ficha definitiva. |
| P-04 · aceptación y normalización física | Malla comprobada, regiones analíticas contrastadas y propuesta explícita de conteo direccional sintético con exposición convencional. | Acordar definición final, justificar referencia de cielo, fuente y bordes con corte. Si se requiere C3, corregir estadística y soporte espacial/angular antes de ejecutar. |

El pendiente principal es P-04. Ya se recibió respaldo de SC3 y una configuración candidata, pero la convergencia de planos grandes no demuestra equivalencia con el panel físico.

## Siguiente entrega necesaria

La entrega `01a9871` responde a las dos tareas solicitadas: herramientas en SC3 y propuesta de imagen. Corresponde acordar el producto con la dirección y ajustar el protocolo sobre papel: 1.600 cuentas no satisfacen los intervalos simultáneos propuestos y parte de la referencia de cielo es extrapolada. No ejecutar C3 con el diseño actual ni lanzar la campaña grande. La necesidad de equivalencia instrumental depende de la afirmación que se decida respaldar. Decidir P0 después de cerrar esos puntos; véase la revisión actual para cifras y acciones.

## Evidencia de referencia

- [Corrida angular de 1.000 primarios](REVISION_MALLA_ANGULAR_2026-10-01.md).
- [Auditoría completa de etapa 2](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md).
- [Aceptación del plano](REVISION_ACEPTACION_PLANO.md).
- [Diagnóstico de geometrías](DIAGNOSTICO_GEOMETRIAS.md).
- [Preparación de producción](PREPARACION_PRODUCCION_OE1.md).

Las seis geometrías históricamente afectadas son geo-gen-01, geo-test-01, geo-test-03, geo-train-06, geo-train-08 y geo-train-11. El plan de 36 referencias sustituidas y 78 reutilizadas era condicional a conservar el observable y la malla. La adopción de az-edges-v1 obliga a revisar esa compatibilidad; no autoriza reutilización por cambiar las etiquetas.

Las observaciones históricas y sus fechas se conservan en la [bitácora](BITACORA.md), los informes correspondientes y el historial Git. Esta página expresa el estado actual, no una nueva calificación académica.

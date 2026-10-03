# Pendientes del OE1

> Estado 2026-10-03, posterior a e037d09: [datos f395570 verificados](REVISION_DATOS_F395570.md). Recibidos los histogramas y NPZ, reproducida la evaluación y comprobados los 9.120 pares. Ya no se solicita su entrega ni generación. Permanecen la ficha/informe final, revisión de distribución y valoración académica de representatividad.

> Actualización 2026-10-03: [campaña e037d09 revisada](REVISION_CAMPANA_E037D09.md). La ejecución está respaldada por registros y resúmenes. Siguiente entrega: histogramas fusionados y NPZ completos; después revisión directa, pares y ficha final. Las siete vistas bajo la meta se conservan; no se ordena transporte adicional.

> Estado posterior: [preparación completa de las siete actividades](PREPARACION_CAMPANA_114.md). P-03: empaquetado del piloto y evaluación de campaña comprobados localmente. P-01/P-04: decidir presupuesto y meta de calidad, ejecutar y revisar las referencias finales. El piloto no es el escenario de mayor columna nominal.

> Actualización posterior — 2026-10-02: [piloto ccbdce0 reproducido desde los histogramas](REVISION_HISTOGRAMAS_PILOTO_CCBDCE0.md). La entrega respalda el flujo ejecutado en SC3 y el criterio de bordes para seis vistas. Quedan el criterio de suficiencia en roca, el presupuesto y la decisión de campaña; 344 M es una propuesta. Los estados anteriores se conservan como antecedente.

> Estado actual: [siete actividades locales completadas](ENTREGA_SIETE_ACTIVIDADES.md), con 103 pruebas. Referencia ideal sin extrapolación, evaluadores, diseño condicional y lanzador listos. La comprobación de dos bloques en SC3 ya fue aceptada; falta verificar allí el nuevo flujo y revisar receta y acordar criterio/presupuesto; el alcance idealizado ya fue adoptado.

> Datos ya reanalizados: [panel/plano y bordes con corte de energía](DIAGNOSTICO_OBSERVABLE_Y_DECISION.md). La siguiente decisión está acotada a la definición física; no pedir otra comparación 100/600 para repetir lo ya demostrado.

> La prueba recibida cubre publicación, fusión y exportación de dos bloques; falta su integración en el lanzador automático de campaña. No repetir la comprobación ya recibida.

Estado consolidado al 2026-10-02, Colombia. **P-01 a P-04 continúan abiertos**, con avances diferentes. La integración angular en SC3 ya fue recibida y revisada; no sigue pendiente repetir la prueba de 1.000 muones.

| ID | Avance respaldado | Qué falta para cerrar |
|---|---|---|
| P-01 · geometría y datos corregidos | Se identificaron seis geometrías afectadas; se recibió evidencia de controles geométricos de B. Etapas 1, complemento y etapa 2 revisados; se cuantificó el efecto observado en el caso estudiado, con resultado estadístico inconcluso. | Decidir el alcance de sustitución y producir referencias compatibles con la definición final. No extrapolar equivalencia a todo el catálogo ni mezclar mallas antiguas y nuevas. |
| P-02 · entorno reproducible | Receta SC3 ampliada recibida: Geant4 11.4.2, GCC 14.2.0, versiones de datos físicos y configuración de compilación. Entorno Python de análisis documentado. | Fijar la versión de producción y revisar su trazabilidad de extremo a extremo. No declarar equivalente el Docker histórico 11.3.2. |
| P-03 · reproducción de la cadena | Se reprodujeron los 9.120 pares históricos. Cadena local ampliada a 103 pruebas; worker/lanzador implementados. Publicación/fusión/exportación verificadas en SC3 con dos bloques. T-01 aclarado: objetos Git íntegros. | Comprobar el nuevo flujo de ejecución/cola en SC3 y fijar ficha definitiva. |
| P-04 · aceptación y normalización física | Malla y regiones comprobadas; alcance idealizado adoptado, referencia ideal y evaluadores estadísticos implementados; piloto condicional dimensionado. | Incorporar al informe la definición adoptada, justificar representatividad de fuente y límites de referencia, evaluar bordes con corte. C3 solo si se exige equivalencia instrumental, con dominio y tasas revisados. |

El pendiente principal es P-04. Ya se recibió respaldo de SC3 y una configuración candidata, pero la convergencia de planos grandes no demuestra equivalencia con el panel físico.

## Siguiente entrega necesaria

Los ajustes locales ya están implementados: [definición adoptada y criterios de cierre](DEFINICION_PRODUCTO_OE1.md), [referencias y estadística](DISENO_ESTADISTICO_Y_REFERENCIAS.md) y [guía operativa](GUIA_SIGUIENTE_ETAPA_OE1.md). Estudiantes: comprobar nuevo flujo en SC3 sin transporte y incorporar al informe el alcance idealizado adoptado. Dirección y estudiantes: acordar criterio y presupuesto antes del piloto. C3 queda como vía condicional para una afirmación instrumental adicional; no se ejecuta por rutina. La campaña final se decide con los resultados del piloto, no con las pruebas de software.

## Evidencia de referencia

- [Corrida angular de 1.000 primarios](REVISION_MALLA_ANGULAR_2026-10-01.md).
- [Auditoría completa de etapa 2](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md).
- [Aceptación del plano](REVISION_ACEPTACION_PLANO.md).
- [Diagnóstico de geometrías](DIAGNOSTICO_GEOMETRIAS.md).
- [Preparación de producción](PREPARACION_PRODUCCION_OE1.md).

Las seis geometrías históricamente afectadas son geo-gen-01, geo-test-01, geo-test-03, geo-train-06, geo-train-08 y geo-train-11. El plan de 36 referencias sustituidas y 78 reutilizadas era condicional a conservar el observable y la malla. La adopción de az-edges-v1 obliga a revisar esa compatibilidad; no autoriza reutilización por cambiar las etiquetas.

Las observaciones históricas y sus fechas se conservan en la [bitácora](BITACORA.md), los informes correspondientes y el historial Git. Esta página expresa el estado actual, no una nueva calificación académica.

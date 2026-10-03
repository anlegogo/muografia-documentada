# Muografía: documentación y seguimiento académico

**Campaña reportada completa:** [revisión e037d09](objetivo-1/REVISION_CAMPANA_E037D09.md). Registros de 1.026 bloques terminados; 1.710 intervalos de borde recalculados y conformes; 107/114 vistas alcanzan la meta descriptiva de roca. Faltan los histogramas/NPZ para revisión directa y la generación de los 9.120 pares.

**Preparación de campaña completada:** [siete actividades, criterios, presupuesto y guía de ejecución](objetivo-1/PREPARACION_CAMPANA_114.md). Comparación de 19 geometrías, manifiesto candidato de 114 vistas, 480 pares del piloto verificados y 106 pruebas satisfactorias. No se autoriza envío por esta preparación.

**Piloto recibido y reproducido:** [revisión de los histogramas ccbdce0](objetivo-1/REVISION_HISTOGRAMAS_PILOTO_CCBDCE0.md). Se verificaron las seis vistas, 27 huellas y 90 regiones de borde. Los 344 M por vista siguen siendo un presupuesto candidato; la campaña no queda autorizada por esta revisión.

Réplica de trabajo de Andrés Leonardo González Gómez para el material de Reinaldo Cárdenas Tirado y Daniel Andrés Pinto Ortega, UIS / GOTS. Alcance exclusivo: **objetivo específico 1, simulación y generación de datos**.

## Estado actual

**Preparación local posterior completada:** [entrega de las siete actividades](objetivo-1/ENTREGA_SIETE_ACTIVIDADES.md), con definición de producto, referencia ideal de cielo, diseño estadístico, evaluación de bordes, automatización y [guía única para estudiantes](objetivo-1/GUIA_SIGUIENTE_ETAPA_OE1.md). **103 pruebas locales satisfactorias.** El [alcance idealizado quedó adoptado por la dirección](objetivo-1/DEFINICION_PRODUCTO_OE1.md#lista-única-de-criterios-de-cierre). Quedan su incorporación al informe y la comprobación operativa en SC3; el piloto calculado y la campaña son condicionales, no órdenes de ejecución.

Como antecedente, la [actualización 01a9871](objetivo-1/REVISION_INTEGRACION_OBSERVABLE_01A9871.md) respaldó la prueba de herramientas en SC3 sobre dos bloques, con 200.000 primarios y 69.995 registros con corte. Se reprodujo su análisis y se corrigió la atribución sobre finales de línea: los objetos Git originales estaban bien. Las correcciones y propuestas posteriores están reunidas en la entrega de siete actividades; **la campaña final sigue pendiente** del acuerdo científico y la evaluación del piloto.

Comenzar por la entrega de siete actividades y su guía. El [balance de preparación local anterior](objetivo-1/BALANCE_PREPARACION_LOCAL.md) conserva el antecedente de la cadena y las probabilidades de fuente; las revisiones anteriores preservan evidencia y cronología.

También está disponible la [publicación verificada de bloques](objetivo-1/PUBLICACION_VERIFICADA_BLOQUES.md), probada frente a fallos de copia y guardado. Esas herramientas ya se probaron en SC3 con dos bloques; el nuevo lanzador y worker están implementados y probados localmente, pendientes de verificación operativa allí.

| Evidencia / recurso | Qué contiene |
|---|---|
| [Revisión de la corrida angular](objetivo-1/REVISION_MALLA_ANGULAR_2026-10-01.md) | Integración satisfactoria en SC3, con 24 controles y 31 contrastes propios. |
| [Aceptación del plano de conteo](objetivo-1/REVISION_ACEPTACION_PLANO.md) | Pregunta física pendiente y por qué convergencia del plano no basta. |
| [Cadena local](objetivo-1/CADENA_LOCAL_OE1.md) | Verificación, exportación, representación, ROI y paquetes de menor conteo. |
| [Auditoría completa de etapa 2](objetivo-1/AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md) | Auditoría de 48,7 millones de registros de transporte; comparación estadística inconclusa, sin ampliación automática. |
| [Pendientes](objetivo-1/PENDIENTES.md) | Condiciones actuales de cierre de P-01 a P-04. |
| [Matriz del objetivo](objetivo-1/MATRIZ_CUMPLIMIENTO.md) | Qué está verificado y qué falta. |
| [Índice](docs/INDICE.md) | Documentos y revisiones históricas. |

## Datos y versiones

El conjunto histórico tiene 19 geometrías, 114 vistas y 9.120 pares reducidos, cuya reproducción se verificó. No es todavía el conjunto corregido final. De la malla nueva hay pruebas de integración y controles, aún no un conjunto final aprobado; no se completan vistas ausentes con copias ni se reetiquetan matrices antiguas.

`objetivo-1/originales/` conserva el material recibido. `objetivo-1/evidencias/` contiene las verificaciones. `herramientas/` incluye auditores y herramientas nuevas de preparación; `objetivo-1/correcciones/` conserva el parche entregado. Los ensayos y entregas congelados permanecen en sus ramas.

Los NPZ históricos y logs grandes no forman parte del historial Git de esta réplica; restaurarlos según [procedencia](docs/PROCEDENCIA.md) y verificar sus huellas. Los derivados nuevos se generan en carpetas de trabajo separadas. Para los scripts nuevos consultar [versiones Python probadas](requirements-oe1-local.txt).

El seguimiento histórico permanece en [CHANGELOG](CHANGELOG.md) y [bitácora](objetivo-1/BITACORA.md). No se incorporan entrenamiento de redes ni evaluaciones de OE2/OE3.

# Muografía: documentación y seguimiento académico

Réplica de trabajo de Andrés Leonardo González Gómez para el material de Reinaldo Cárdenas Tirado y Daniel Andrés Pinto Ortega, UIS / GOTS. Alcance exclusivo: **objetivo específico 1, simulación y generación de datos**.

## Estado actual

La [actualización 01a9871 fue revisada](objetivo-1/REVISION_INTEGRACION_OBSERVABLE_01A9871.md) al **2026-10-02**: queda respaldada la prueba de nuestras herramientas en SC3 sobre dos bloques existentes, con 200.000 primarios y 69.995 registros con corte. Se reprodujo el nuevo análisis del observable y se corrigió nuestra atribución anterior sobre finales de línea: los objetos Git originales estaban bien. **La campaña final sigue pendiente** de acordar la definición física y corregir la referencia de cielo y el diseño estadístico del control propuesto.

Comenzar por el [balance de preparación local](objetivo-1/BALANCE_PREPARACION_LOCAL.md): cadena técnica corregida, probabilidades de fuente calculadas, manifiestos revisados y **78 pruebas locales satisfactorias**. La definición candidata y las dependencias pendientes están reunidas allí. Las revisiones anteriores conservan la evidencia y la cronología.

También está disponible la [publicación verificada de bloques](objetivo-1/PUBLICACION_VERIFICADA_BLOQUES.md), probada frente a fallos de copia y guardado. La suite local reúne **78 pruebas satisfactorias**. Las herramientas ya se probaron en SC3 con dos bloques; su uso dentro del lanzador automático de producción continúa pendiente.

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

`objetivo-1/originales/` conserva el material recibido. `objetivo-1/evidencias/` contiene nuestras verificaciones. `herramientas/` incluye auditores y herramientas nuevas de preparación; `objetivo-1/correcciones/` conserva el parche entregado. Los ensayos y entregas congelados permanecen en sus ramas.

Los NPZ históricos y logs grandes no forman parte del historial Git de esta réplica; restaurarlos según [procedencia](docs/PROCEDENCIA.md) y verificar sus huellas. Los derivados nuevos se generan en carpetas de trabajo separadas. Para los scripts nuevos consultar [versiones Python probadas](requirements-oe1-local.txt).

El seguimiento histórico permanece en [CHANGELOG](CHANGELOG.md) y [bitácora](objetivo-1/BITACORA.md). No se incorporan entrenamiento de redes ni evaluaciones de OE2/OE3.

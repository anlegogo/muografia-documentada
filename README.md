# Muografía: documentación y seguimiento académico

Réplica de trabajo de Andrés Leonardo González Gómez para el material de Reinaldo Cárdenas Tirado y Daniel Andrés Pinto Ortega, UIS / GOTS. Alcance exclusivo: **objetivo específico 1, simulación y generación de datos**.

## Estado actual

La entrega de justificación física y producción fue revisada al **2026-10-02**: se reprodujeron sus seis análisis y la fusión de dos bloques de integración, y se contrastaron los histogramas/metadatos de 19 corridas de control (92 millones de primarios). Hay una propuesta de regenerar las 114 vistas, pero **la receta aún no se declara validada y la campaña final no está habilitada**: quedan observaciones físicas y la adopción de las correcciones técnicas en el flujo de los estudiantes.

Comenzar por la [revisión actual y acciones concretas](objetivo-1/REVISION_FISICA_PRODUCCION_2026-10-02.md). Las [correcciones locales de fusión y configuración](objetivo-1/CORRECCIONES_LOCALES_FUSION_CONFIGURACION.md) ya incorporan los campos nuevos y reúnen **56 pruebas satisfactorias**; se comprobaron sobre los dos bloques reales. La adopción en SC3 sigue pendiente.

Avance adicional: [diagnóstico del observable y decisión física](objetivo-1/DIAGNOSTICO_OBSERVABLE_Y_DECISION.md), con los datos ya conservados y **60 pruebas locales**. No requiere repetir corridas para obtener estos resultados.

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

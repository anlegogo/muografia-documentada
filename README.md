# Muografía: documentación y seguimiento académico

Réplica de trabajo de Andrés Leonardo González Gómez para el material de Reinaldo Cárdenas Tirado y Daniel Andrés Pinto Ortega, UIS / GOTS. Alcance exclusivo: **objetivo específico 1, simulación y generación de datos**.

## Estado actual

La corrección angular fue aplicada y probada por los estudiantes en SC3: **1.000 primarios, 750 registros**, entrega revisada. La nueva cadena local de lectura, representación, regiones y empaquetado está implementada y tiene **41 pruebas satisfactorias**. La aceptación física del plano de conteo y la normalización temporal siguen pendientes: **el OE1 no está cerrado y la campaña final no está definida**.

Comenzar por [cadena local preparada y siguiente entrega necesaria](objetivo-1/CADENA_LOCAL_OE1.md). Allí están los comandos, resultados, límites y un mensaje preparado para los estudiantes.

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

El conjunto histórico tiene 19 geometrías, 114 vistas y 9.120 pares reducidos, cuya reproducción se verificó. No es todavía el conjunto corregido final. De la malla nueva se recibió una vista de prueba; no se completan vistas ausentes con copias ni se reetiquetan matrices antiguas.

`objetivo-1/originales/` conserva el material recibido. `objetivo-1/evidencias/` contiene nuestras verificaciones. `herramientas/` incluye auditores y herramientas nuevas de preparación; `objetivo-1/correcciones/` conserva el parche entregado. Los ensayos y entregas congelados permanecen en sus ramas.

Los NPZ históricos y logs grandes no forman parte del historial Git de esta réplica; restaurarlos según [procedencia](docs/PROCEDENCIA.md) y verificar sus huellas. Los derivados nuevos se generan en carpetas de trabajo separadas. Para los scripts nuevos consultar [versiones Python probadas](requirements-oe1-local.txt).

El seguimiento histórico permanece en [CHANGELOG](CHANGELOG.md) y [bitácora](objetivo-1/BITACORA.md). No se incorporan entrenamiento de redes ni evaluaciones de OE2/OE3.

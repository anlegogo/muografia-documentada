# Objetivo específico 1: guía del material

**Paso actual:** [complemento R2-01 revisado](REVISION_COMPLEMENTO_R2_01_2026-10-01.md). Se reprodujo el análisis de los 72 transportes y se verificó la asignación de material de B en los 36 pares dirigidos. Falta dimensionar y acordar la etapa 2 con fuente representativa; OE1 y P-01…P-04 no se cierran con esta prueba.

**Ejecución recibida:** R2-01 fue corrido por los estudiantes en SC3 el 30 de septiembre y revisado localmente el 1 de octubre. [Resultados y límites](REVISION_COMPLEMENTO_R2_01_2026-10-01.md). Las entregas permanecen en su rama y el protocolo v1.0 se conserva como registro histórico.

Consultar primero [alcance](ALCANCE.md) y [matriz de cumplimiento](MATRIZ_CUMPLIMIENTO.md).

Nueva revisión: [diagnóstico geométrico](DIAGNOSTICO_GEOMETRIAS.md), [reproducción de pares](REVISION_DATOS.md), [instrucciones SC3](INSTRUCCIONES_ESTUDIANTES.md) y [plantilla de reporte](PLANTILLA_ENTREGA_OE1.md).

| Material | Ubicación | Lectura correcta |
|---|---|---|
| Geometrías | [Catálogo JSON](originales/scripts/simulation/geometry_catalog/geometries) | 19 escenarios; incluye particiones de datos, sin evaluar modelos. |
| Transporte Monte Carlo | [Aplicación Geant4](originales/scripts/simulation/geant4_app) | Código fuente recibido; no recompilado en esta incorporación. |
| Generador y dependencias | [EcoMug](originales/scripts/simulation/ecomug_standalone), [terceros](originales/scripts/simulation/third_party) | Conservar atribuciones. |
| Motor analítico | [Surrogate](originales/scripts/simulation/surrogate) | Antecedente de validación; no confundir con la campaña Geant4 final. |
| Entorno y ejecución | [Docker](originales/scripts/simulation/docker), [SC3](originales/scripts/cluster) | Configuración histórica; requiere revisión de entorno. |
| Preparación y controles | [Análisis](originales/scripts/analysis) | Generación de pares, particiones, validación de flujo y física. |
| Campaña recibida | [Conteos y metadatos](originales/data/campaign-geant4) | 114 vistas; binarios incluidos localmente. |
| Pares preparados | [Shards](originales/dataset/shards) | 19 archivos NPZ y sus metadatos. |
| Manifiestos | [Resultados de datos](originales/results/dataset) | Fuente de las cantidades y las huellas declaradas. |
| Comparación de motores | [Resultados de simulación](originales/results/simulation) | Resultado recibido, distinto de una nueva reproducción. |
| Figuras OE1 | [Etapas 06–11](originales/figures/results) | Figuras recibidas; su presencia no prueba regeneración. |
| Registros | [Logs](originales/logs/simulation) | 199 archivos, incluidos duplicados y ensayos previos. |
| Bitácora de autores | [Bitácora de simulación](originales/bitacora-simulacion.md) | Compilada retrospectivamente el 28 de septiembre de 2026. |

Los documentos de seguimiento son [datos](DATOS.md), [reproducción](REPRODUCCION.md), [pendientes](PENDIENTES.md) y [bitácora de revisión](BITACORA.md).

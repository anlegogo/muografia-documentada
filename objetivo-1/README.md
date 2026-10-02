# Objetivo específico 1: guía del material

**Preparación actual:** [alcance de producción y decisiones de normalización](PREPARACION_PRODUCCION_OE1.md). Inventario verificado de 114 referencias; 36 candidatas a regenerar y 78 de reutilización condicionada. Primero resolver la definición del observable y la receta de producción.

**Paso actual:** [auditoría completa de etapa 2](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md). Verificados los 85 archivos, las 27 listas y los 55 registros completos; conteos e intervalo reproducidos. Resultado estadístico inconcluso. Preparar producción B resolviendo entorno, normalización y alcance; las precisiones de interpretación E2-01/E2-02/E2-04 quedan documentadas. OE1 y P-01…P-04 siguen abiertos.

**Ejecución recibida:** etapa 2 realizada en SC3 por los estudiantes y [auditada íntegramente](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md); no se añaden corridas ni se inicia producción definitiva con esta revisión. Se preservan las entregas en sus ramas y los diseños congelados.

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

# Decisiones de organización

| ID | Decisión | Motivo |
|---|---|---|
| D-001 | Incorporar solo OE1. | Delimitar la revisión solicitada. |
| D-002 | Mantener rutas internas bajo `objetivo-1/originales/`. | Los programas resuelven rutas relativas a su propia ubicación; moverlos por tema rompería dependencias. |
| D-003 | Crear historial propio de la selección y conservar el clon fuente completo fuera de la réplica. | Evitar incorporar OE2/OE3 mediante el historial y mantener procedencia verificable. |
| D-004 | Conservar `scripts/training/muography_dataset.py`. | `build_dataset.py` importa su preprocesamiento; se incluye como dependencia de datos, sin entrenadores ni modelos. |
| D-005 | Copiar los 19 metadatos también junto a los shards. | `partition_freeze.py` los busca allí; los originales recibidos están en `results/dataset/shards/`. Ambas copias son idénticas. |
| D-006 | Mantener NPZ y logs en disco fuera de Git. | Evitar inflar el historial; los manifiestos permiten verificar y restaurar. |
| D-007 | Preservar fuentes y advertencias sin corregirlas en esta incorporación. | El efecto físico exige un experimento y comparación registrados. |

Estas decisiones documentan la organización actual; no redefinen los objetivos académicos aprobados.

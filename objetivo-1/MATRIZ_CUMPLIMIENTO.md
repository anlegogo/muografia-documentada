# Matriz de cumplimiento del OE1

Valoración técnica de revisión, no calificación académica definitiva. «Verificado» se limita al control descrito.

| ID | Aspecto | Evidencia | Estado | Condición pendiente |
|---|---|---|---|---|
| OE1-01 | Escenarios volcánicos definidos | 19 JSON del catálogo y figuras etapa 07 | Verificado: archivos presentes | Resolver coherencia de geometrías solapadas: P-01. |
| OE1-02 | Simulación Monte Carlo ejecutada | Aplicación Geant4, 114 vistas, manifiesto y logs | Verificado: entrega e integridad; ejecución histórica documentada | No hay nueva ejecución local de Geant4; P-01/P-02. |
| OE1-03 | Diferentes niveles de conteo | Shards, metadatos y `build_dataset.py` | Verificado: 50 %, 10 %, 5 %, 1 %; 20 realizaciones por vista y fracción | No se regeneraron los pares en esta incorporación. |
| OE1-04 | Datos organizados y trazables | Particiones por geometría, semillas y SHA-256 | Verificado: integridad y particiones declaradas | Conservar versión al recibir cambios. |
| OE1-05 | Representatividad y validación física | Controles analíticos recibidos, comparación de motores y logs | Parcial | Cuantificar efectos de solapamientos y supuestos físicos; P-01/P-04. |
| OE1-06 | Reproducción independiente | Código, entorno histórico y registros | Parcial | Resolver diferencias de entorno e insumos ausentes; P-02/P-03. |

**Conclusión:** la generación del conjunto está respaldada. El cierre de su validación física continúa pendiente; ordenar o verificar hashes no resuelve ese pendiente.

Consultar [inventario](inventario/archivos.json), [evidencia previa de campaña](evidencias/integridad-campana-previa.json), [advertencias](evidencias/advertencias-simulacion.json) y [pendientes](PENDIENTES.md).

# Matriz de cumplimiento del OE1

**Paso actual:** [protocolo del segundo ensayo v1.0](PROTOCOLO_SEGUNDO_ENSAYO_OE1.md), diseñado desde la revisión. La etapa 1 está definida; etapa 2 y cierre físico siguen pendientes.

Valoración técnica de revisión, no calificación académica definitiva. «Verificado» se limita al control descrito.

**Revisión del 29 de septiembre:** [entrega del piloto](REVISION_ENTREGA_2026-09-29.md) revisada con observaciones. Corrección geométrica con evidencia favorable; impacto físico aún inconcluso. Ver [encargo vigente](DISENO_SIGUIENTE_ENSAYO_OE1.md).

| ID | Aspecto | Evidencia | Estado | Condición pendiente |
|---|---|---|---|---|
| OE1-01 | Escenarios volcánicos definidos | Catálogo y controles T1 recibidos de variante corregida | Controles favorables: 114 casos B sin solapamiento declarado | Delimitar corrección y cuantificar impacto: P-01. |
| OE1-02 | Simulación Monte Carlo ejecutada | Aplicación Geant4, 114 vistas, manifiesto y logs | Verificado: entrega e integridad; ejecución histórica documentada | No hay nueva ejecución local de Geant4; P-01/P-02. |
| OE1-03 | Diferentes niveles de conteo | Shards, metadatos y auditoría local | Verificado: 9.120 pares regenerados en memoria e idénticos; semillas y límites comprobados | La validez física de las referencias sigue dependiendo de P-01/P-04. |
| OE1-04 | Datos organizados y trazables | Particiones por geometría, semillas y SHA-256 | Verificado: integridad y particiones declaradas | Conservar versión al recibir cambios. |
| OE1-05 | Representatividad y validación física | Controles analíticos recibidos, comparación de motores y logs | Parcial | Cuantificar efectos de solapamientos y supuestos físicos; P-01/P-04. |
| OE1-06 | Reproducción independiente | Reproducción SC3 entregada y comparación local contra conteos originales | Histograma de geo-train-06, vista 0, idéntico; alcance parcial | Otros casos/entornos e insumos ausentes: P-02/P-03. |

**Conclusión:** la generación del conjunto está respaldada. El cierre de su validación física continúa pendiente; ordenar o verificar hashes no resuelve ese pendiente.

Ampliación: [diagnóstico de las seis geometrías afectadas](DIAGNOSTICO_GEOMETRIAS.md), [comprobación de preparación de datos](REVISION_DATOS.md) e [instrucciones de ejecución](INSTRUCCIONES_ESTUDIANTES.md).

Consultar [inventario](inventario/archivos.json), [evidencia previa de campaña](evidencias/integridad-campana-previa.json), [advertencias](evidencias/advertencias-simulacion.json) y [pendientes](PENDIENTES.md).

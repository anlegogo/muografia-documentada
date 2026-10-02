# Matriz de cumplimiento del OE1

**Paso actual:** [auditoría completa de etapa 2](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md). Verificados los 85 archivos, las 27 listas y los 55 registros completos; conteos e intervalo reproducidos. Resultado estadístico inconcluso. Preparar producción B resolviendo entorno, normalización y alcance; las precisiones de interpretación E2-01/E2-02/E2-04 quedan documentadas. OE1 y P-01…P-04 siguen abiertos.

**Ejecución recibida:** etapa 2 realizada en SC3 por los estudiantes y [auditada íntegramente](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md); no se añaden corridas ni se inicia producción definitiva con esta revisión. Se preservan las entregas en sus ramas y los diseños congelados.

Valoración técnica de revisión, no calificación académica definitiva. «Verificado» se limita al control descrito.

**Revisión del 29 de septiembre:** [entrega del piloto](REVISION_ENTREGA_2026-09-29.md) revisada con observaciones. Corrección geométrica con evidencia favorable; impacto físico aún inconcluso. El encargo de diseño enlazado en esa revisión es histórico; el seguimiento actual figura arriba.

| ID | Aspecto | Evidencia | Estado | Condición pendiente |
|---|---|---|---|---|
| OE1-01 | Escenarios volcánicos definidos | Catálogo y controles T1 recibidos de variante corregida | Controles favorables: 114 casos B sin solapamiento declarado | Delimitar corrección y cuantificar impacto: P-01. |
| OE1-02 | Simulación Monte Carlo ejecutada | Aplicación Geant4, 114 vistas, manifiesto y logs | Verificado: entrega e integridad; ejecución histórica documentada | No hay nueva ejecución local de Geant4; P-01/P-02. |
| OE1-03 | Diferentes niveles de conteo | Shards, metadatos y auditoría local | Verificado: 9.120 pares regenerados en memoria e idénticos; semillas y límites comprobados | La validez física de las referencias sigue dependiendo de P-01/P-04. |
| OE1-04 | Datos organizados y trazables | Particiones por geometría, semillas y SHA-256 | Verificado: integridad y particiones declaradas | Conservar versión al recibir cambios. |
| OE1-05 | Representatividad y validación física | Controles analíticos recibidos, comparación de motores y logs | Parcial | Cuantificar efectos de solapamientos y supuestos físicos; P-01/P-04. |
| OE1-06 | Reproducción independiente | Histograma histórico y análisis de etapa 1 reproducidos; 600.000 pares A/B contrastados y 13 histogramas reconstruidos desde crudos | Verificado para el análisis y los archivos revisados; sin nueva ejecución Geant4 local | Cobertura de transporte y otros casos/entornos: R2-01, P-01/P-02/P-03. |

**Conclusión:** la generación del conjunto está respaldada. El cierre de su validación física continúa pendiente; ordenar o verificar hashes no resuelve ese pendiente.

Ampliación: [diagnóstico de las seis geometrías afectadas](DIAGNOSTICO_GEOMETRIAS.md), [comprobación de preparación de datos](REVISION_DATOS.md) e [instrucciones de ejecución](INSTRUCCIONES_ESTUDIANTES.md).

Consultar [inventario](inventario/archivos.json), [evidencia previa de campaña](evidencias/integridad-campana-previa.json), [advertencias](evidencias/advertencias-simulacion.json) y [pendientes](PENDIENTES.md).

# Bitácora del OE2

## 2026-10-03 — Revisión inicial autorizada por la dirección

- Actividad: revisión del código publicado por los estudiantes y diagnóstico local de compatibilidad con dataset-v2. Se conserva la autoría estudiantil de la implementación y simulación; la revisión se incorpora como seguimiento de la dirección.
- Entradas: repositorio original b88fa576494cb8a664c46b8c94c5918c5097d616, contraste de entrenamiento con 3315f82 y distribución Drive de 2026-10-03. Consulta de actualización documental 800ab86 en la rama estudiantil de la réplica, sin fusión.
- Procedimiento: inspección de arquitectura, pérdidas, lector, checkpoints, configuración y registros; ejecución de `herramientas/revisar_base.py` según el comando del [informe](README.md).
- Evidencia: [JSON](evidencias/revision-2026-10-03.json), con huellas y entorno. Comparados 7.200 pares de 90 vistas; forward de generador/crítico satisfactorio; reproducidas dependencia de referencia y discrepancia de GP.
- Incidencias de revisión: primeras consultas de archivos de entrenamiento se hicieron desde la réplica documental y no encontraron esos archivos; se corrigió la ruta al repositorio original. Primera ejecución del diagnóstico falló por exigir igualdad exacta a cero en aritmética float32; se adoptó tolerancia de 1e-8 para GP teóricamente nulo y 1e-5 relativo para su valor analítico. La repetición terminó con código cero. No se modificó la implementación estudiantil para obtener ese resultado.
- Límites: sin entrenamiento, sin inferencia sobre test/generalization, sin validación de GPU ni nueva evaluación de pesos históricos. El cierre del OE1 no cambia.
- Resultado: OE2-P01 a OE2-P04 pendientes, con criterios de cierre y orden propuesto. La siguiente actividad es una corrección versionada y una prueba breve antes de consumir recursos de SC3.

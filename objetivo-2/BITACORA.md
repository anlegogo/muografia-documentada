# Bitácora del OE2

## 2026-10-03 — Revisión inicial autorizada por la dirección

- Actividad: revisión del código publicado por los estudiantes y diagnóstico local de compatibilidad con dataset-v2. Se conserva la autoría estudiantil de la implementación y simulación; la revisión se incorpora como seguimiento de la dirección.
- Entradas: repositorio original b88fa576494cb8a664c46b8c94c5918c5097d616, contraste de entrenamiento con 3315f82 y distribución Drive de 2026-10-03. Consulta de actualización documental 800ab86 en la rama estudiantil de la réplica, sin fusión.
- Procedimiento: inspección de arquitectura, pérdidas, lector, checkpoints, configuración y registros; ejecución de `herramientas/revisar_base.py` según el comando del [informe](README.md).
- Evidencia: [JSON](evidencias/revision-2026-10-03.json), con huellas y entorno. Comparados 7.200 pares de 90 vistas; forward de generador/crítico satisfactorio; reproducidas dependencia de referencia y discrepancia de GP.
- Incidencias de revisión: primeras consultas de archivos de entrenamiento se hicieron desde la réplica documental y no encontraron esos archivos; se corrigió la ruta al repositorio original. Primera ejecución del diagnóstico falló por exigir igualdad exacta a cero en aritmética float32; se adoptó tolerancia de 1e-8 para GP teóricamente nulo y 1e-5 relativo para su valor analítico. La repetición terminó con código cero. No se modificó la implementación estudiantil para obtener ese resultado.
- Límites: sin entrenamiento, sin inferencia sobre test/generalization, sin validación de GPU ni nueva evaluación de pesos históricos. El cierre del OE1 no cambia.
- Resultado: OE2-P01 a OE2-P04 pendientes, con criterios de cierre y orden propuesto. La siguiente actividad es una corrección versionada y una prueba breve antes de consumir recursos de SC3.

## 2026-10-03 — Corrección autorizada de los tres puntos

- Se creó una implementación derivada de b88fa57, conservando originales y atribución estudiantil. Se corrigieron pérdidas, lector, contrato de normalización y recuperación de checkpoints.
- P01–P03 resueltos para el entrenamiento sobre la distribución fijada; [documentación v1](CORRECCIONES_V1.md) y [evidencia](evidencias/correcciones-v1.json). Preparación: 90 vistas/7.200 pares comparados; escala calculada únicamente con train.
- Primera ejecución: 16 controles satisfactorios. Tras comprobar portabilidad, se fijaron finales LF en manifiesto y fuentes, se normalizaron saltos de línea al identificar código y se añadió una prueba de independencia de la referencia a través del lector. Repetición final: 17 controles satisfactorios, incluida reanudación exacta.
- Incidencias: la consulta adicional al repositorio citado como muography-thesis no pudo ejecutarse mediante gh porque ese ejecutable no está disponible. El convertidor histórico permanece no recuperado; la verificación independiente contra paquetes fuente evita depender de su ejecución para integrar los datos. La ayuda CLI emitió un aviso de caché de fuentes de Matplotlib sin permisos en el perfil de Windows; terminó correctamente y no afectó los controles numéricos.
- Se separó selección del mejor SSIM sin redondear del umbral de paciencia. Los resultados son pruebas técnicas CPU de dos pasos, sin apertura de imágenes reservadas y sin conclusión de calidad.
- Siguiente paso: protocolo OE2-P04 y prueba GPU, antes del entrenamiento prolongado.

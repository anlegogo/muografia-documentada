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

## 2026-10-03 — Diseño del piloto OE2-P04

- Autorización de la dirección para preparar protocolo, configuraciones y comandos SC3. Se fijó comparación al 5 % entre U-Net L1 y cWGAN-GP, semilla 2026100301, lote 4 y normalización v1.
- Dos etapas: comprobación técnica de dos épocas con parada/reanudación deliberada, y piloto de hasta 30 épocas con 1.440 pares train/360 val, paciencia 8 y validación por época.
- Se añadieron ejecutor externo y resumen de registros; no se modifica la implementación corregida ni su identidad. Se registra baseline sin red, entorno, memoria CUDA y tiempos.
- Evidencia: [resumen técnico local](evidencias/protocolo-piloto-local.json), [protocolo](PROTOCOLO_PILOTO_F05.md) e [instrucciones](INSTRUCCIONES_PILOTO_SC3.md). Ambos métodos se ejecutan y reanudan en CPU para verificar comandos; esta comprobación no aprueba GPU ni calidad.
- Próximo paso: estudiantes ejecutan A en SC3 y, si pasa, B con autonomía dentro de los límites definidos. Se requiere revisión de resultados antes de ampliar a otras fracciones y repeticiones.
- Resultado local: veinte controles no GPU satisfactorios entre ambos métodos; se comprobó el rechazo de la entrega CPU como aceptación GPU y la coherencia de las cuatro configuraciones. Las dos redes aún empeoran el SSIM de entrada después de cuatro actualizaciones; se registra expresamente sin convertir la prueba técnica en evidencia de calidad. [Verificación del protocolo](evidencias/verificacion-protocolo-v1.json).

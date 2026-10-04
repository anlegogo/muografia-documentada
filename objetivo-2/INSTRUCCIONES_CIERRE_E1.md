# Siguiente entrega: consolidación y discusión de E1

**Actualización de prioridad — 2026-10-04:** la dirección solicitó avanzar directamente. Reproducir el diagnóstico y consolidar E1 ya no son requisitos previos. Ejecutar la [evaluación final](INSTRUCCIONES_EVALUACION_FINAL_OE2.md); la redacción puede avanzar en paralelo. La prohibición anterior de abrir reservas queda sustituida únicamente para el bloque congelado EF-01. Se conserva debajo la guía histórica.

Fecha: 2026-10-04. **La ejecución GPU de E1 y su auditoría terminaron.** Esta guía sustituye el encargo de ejecutar E1; no solicita otro entrenamiento ni requiere alquilar GPU. Véase la [revisión y diagnóstico](REVISION_E1_804CE85.md).

## Propósito

Convertir el ensayo en un resultado reproducible y explicable para el informe del OE2. Se comprobó una reducción del error del borde y un aumento del sesgo interior en geometría 1. La siguiente entrega debe explicar ambos resultados, sin escoger únicamente la semilla favorable ni presentar el ensayo como aceptación física.

## Trabajo autónomo

1. Actualizar la copia de `main` conservando las ramas y los cambios locales. Crear una rama nueva de entrega, por ejemplo `oe2/cierre-documental-e1`, y registrar su commit base. Mantener accesible la entrega original `804ce85`; no fusionarla a ciegas sobre la copia de trabajo.
2. Reproducir en CPU el diagnóstico con el comando de la revisión. Reutilizar los datos y las seis predicciones finales ya disponibles; el diagnóstico no necesita volver a entrenar ni descargar los 18 checkpoints si ya están respaldados. Comparar las tablas completas con `evidencias/diagnostico-interiores-e1.json`: 252 sesgos comprobados, 126 filas regionales y 378 filas por banda. Para cifras usar diferencia absoluta `1e-12`; no exigir igualdad binaria de JPEG entre versiones de Matplotlib. Ante discrepancia conservar comando, entorno y salida, y reportarla sin alterar las tolerancias.
3. Preparar `DISCUSION_E1.md` en una nueva carpeta de entrega. Incluir propósito, C0/C1, seis continuaciones de cinco épocas, resultados de las tres parejas, excepciones por vista y límites. Explicar por qué un borde más preciso puede coexistir con exceso de cuentas en roca y conducto. No afirmar que los mapas demuestran el mecanismo causal. Se puede partir del [borrador de discusión](DISCUSION_E1_BORRADOR.md).
4. Incorporar un reconocimiento explícito de la fe de erratas: 5.910.537.694 bytes y correspondencia de los siete logs. Enlazar el documento corregido desde la nueva entrega; conservar originales y sus huellas.
5. Revisar el [índice de artefactos ya preparado](INDICE_ARTEFACTOS_E1.md), que incluye las seis parejas de pesos/predicciones, semillas, tamaños, enlaces y SHA-256. Registrar el commit de revisión y confirmar que otra persona del grupo puede abrir los enlaces. No rehacer el inventario ni renombrar o sustituir binarios.
6. Subir por Git los textos, JSON/CSV del diagnóstico, registro de comparación y figuras necesarias. Los pesos y predicciones permanecen en Drive. Informar rama y commit de entrega. Los dos estudiantes pueden distribuirse reproducción y redacción, y revisar mutuamente el resultado.

Estas actividades pueden completarse sin una aprobación intermedia entre pasos. Si falla un control, se detiene únicamente la parte dependiente y se reporta el fallo; la redacción puede continuar con resultados identificados como pendientes.

## Criterio de entrega terminada

- Reproducción concordante o discrepancia localizada con evidencia suficiente para revisarla.
- Las tres parejas y las dieciocho vistas por pareja están representadas; no se omiten anomalías ni excepciones.
- Figuras y tablas enlazadas; unidades y normalización coherentes; no se confunden cuentas con densidad.
- Fe de erratas reconocida e índice de artefactos accesible.
- No se alteran coeficientes, semillas, épocas, criterios ni particiones.

## Qué sigue después

La dirección revisará la consolidación y fijará el alcance de la evaluación final. Antes de abrir test/generalización deberán quedar registrados modelos y huellas, fracción, comparadores, métricas, regla de selección o comparación del conjunto completo y tratamiento de la exposición previa al catálogo. Una evaluación descriptiva y una afirmación de calidad comparable son conclusiones distintas; el criterio de esta última debe quedar justificado antes de examinar reservas.

No se autoriza aquí ampliar entrenamiento, buscar un coeficiente en validación ni abrir reservas. Si se decide otra intervención, deberá tener hipótesis y presupuesto propios; estos mapas no demuestran cuál sería su valor óptimo. El trabajo actual aporta una discusión completa del experimento, no una nueva ronda de pruebas por defecto.

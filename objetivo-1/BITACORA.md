# Bitácora de nuestra revisión del OE1

## Revisión técnica y encargo SC3 — 2026-09-28, Colombia

- Entrada: mismo catálogo y datos incorporados; no se consultó una nueva entrega de estudiantes.
- Se examinó la construcción de sólidos, la asignación del campo analítico y el submuestreo binomial.
- Procedimiento: `python herramientas/auditar_oe1.py`; evidencia en `evidencias/auditoria-oe1.json`, con fecha UTC y versiones.
- Se probaron puntos interiores a anomalías superpuestas y cotas geométricas. Se reprodujeron los 9.120 pares en memoria sin cambiar las fuentes.
- Durante el desarrollo del auditor se corrigió una expectativa inicial de dimensiones 64×64: la cabecera y los datos especifican 256×256. El resultado final utiliza ese contrato y no atribuye ese error del auditor a los estudiantes.
- Se preparó un piloto original/corregido para geo-train-06 vista 0 y tres semillas, más plantilla de resultados. Geant4 no se ejecutó localmente.
- Pendientes: ejecución y justificación física por estudiantes; P-01/P-02/P-03/P-04 siguen abiertos.
- Verificación final: 567/567 archivos recibidos conservan sus huellas; auditor de pares sin errores; tres pruebas de herramientas aprobadas (intersección/separación, salida del cono y comparador con rechazo de presupuesto inconsistente); sintaxis Bash del ejecutor y enlaces Markdown comprobados. No se probó envío real de trabajos SLURM ni compilación del esquema C++.

## Incorporación inicial — registro UTC 2026-09-29T03:08:48.514624+00:00

- Solicitud: organizar una réplica local documentada usando únicamente material relacionado con OE1.
- Entrada: revisión `b88fa576494cb8a664c46b8c94c5918c5097d616` y paquete compartido ya descargado y auditado.
- Actividad: selección de fuentes, datos, figuras y logs; conservación de bytes y rutas; inventario SHA-256; creación de documentación y verificador.
- Evidencia previa incorporada: comprobación de 114 vistas y registro de advertencias de simulación. Estos análisis preceden a esta organización y no representan una nueva ejecución Geant4.
- Evidencia de esta incorporación: [verificación local](evidencias/verificacion-local.json), generada por la herramienta de integridad.
- Resultado científico: generación respaldada; validación física pendiente según [matriz](MATRIZ_CUMPLIMIENTO.md).
- Siguiente paso de investigación: cerrar P-01/P-02 con un procedimiento controlado antes de atribuir validez física completa a la campaña.

La [bitácora de autores](originales/bitacora-simulacion.md) se mantiene independiente y sin cambios.

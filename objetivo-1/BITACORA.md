# Bitácora de nuestra revisión del OE1

## Preparación local del complemento R2-01 — 2026-09-30, Colombia

- Por solicitud del director se prepara localmente el [complemento R2-01](COMPLEMENTO_R2_01.md), sin transporte Geant4.
- Se definen 12 trayectorias y tres semillas por variante: 72 transportes técnicos, separados de la fuente representativa.
- En desarrollo, una primera propuesta no retroproyectaba al panel físico de 1,2 m; el validador la rechazó. Se corrigieron las direcciones antes de congelar la lista. El intento descartado permanece en tmp, fuera de la entrega.
- Lista final: validador de estudiantes OK, 108 rectas de sensibilidad mantienen la entrada, 12 cruces profundos contrastados con su referencia; discrepancia máxima de longitud 9,8 × 10⁻¹² m.
- Se comprueba sintaxis Bash del ejecutor; su funcionamiento Geant4/SLURM está pendiente en SC3. Se conserva el alcance de R2-01 y P-01…P-04.

## Revisión independiente de etapa 1 — 2026-09-30, Colombia

- Responsable de transporte: Daniel y Reinaldo en SC3. Revisión: análisis local independiente, sin nueva ejecución Geant4.
- Entradas: entrega `3a49770`, código `3315f82`, paquete Drive con TAR y seis listas de primarios.
- Procedimiento y comandos: [revisión de etapa 1](REVISION_ETAPA_1_2026-09-30.md), sección 6. Entorno: Python 3.12.14, NumPy 2.4.4, pandas 3.0.6.
- Resultado: 405 comprobaciones del análisis reproducidas y 156 controles propios sin fallos; 600.000 pares verificados, repetición A/A idéntica y 13 histogramas reconstruidos.
- Limitación: un cruce en producción; los 20 cruces sintéticos también entran desde el elipsoide. R2-01 requiere complemento antes de ampliar. P-01…P-04 permanecen abiertos.
- Evidencia: `evidencias/revision-etapa1-3a49770.json` y `evidencias/reproduccion-etapa1-3a49770.json`. Se conserva el fallo de descarga inicial del conector: tiempo agotado; descarga directa y huellas posteriores correctas.

## Diseño aportado por la revisión — 2026-09-29, Colombia

- Por solicitud del director se define el protocolo del segundo ensayo v1.0; sustituye pedir a los estudiantes un diseño desde cero.
- Etapa 1: dos geometrías, una vista, tres réplicas A/B y repetición técnica A/A; 13 corridas de 100.000 primarios, con trazabilidad individual.
- Se fijan observable, archivos y controles; el margen físico, la incertidumbre y el tamaño de etapa 2 se decidirán tras revisar etapa 1. No se ejecutó ni se autoriza por este registro una campaña completa.

## Ampliación de controles independientes — 2026-09-29, Colombia

- Cuadratura de las cuatro intersecciones conocidas: geo-test-01, geo-train-06, geo-train-08 y geo-train-11.
- Las cuatro estimaciones son compatibles con los valores y errores estándar entregados (discrepancia máxima 1,13 EE). Dos tolerancias del integrador difieren menos de 0,023 m³ en cada caso.
- Evidencia: `evidencias/intersecciones-independientes.json`; interpretación en `CONTROL_FISICO_LOCAL.md`. No se modifica el encargo de los estudiantes ni se ejecuta transporte Geant4.

## Control geométrico independiente — 2026-09-29, Colombia

- Se integró el volumen común conducto/elipsoide de geo-train-06 mediante cuadratura, con dos tolerancias. Resultado: 83.663,703 m³, compatible con la estimación entregada.
- Se contrastaron volumen restante y cuerpo denso; se documentó la diferencia de densidad del aire entre modelos, conservando la coincidencia de clase de material.
- Evidencia y límites en `CONTROL_FISICO_LOCAL.md`; no se ejecutó Geant4 ni se cambió el encargo vigente.

## Primera entrega revisada y solicitud de diseño — 2026-09-29, Colombia

- Fuente: rama `oe1/geo-train-06-piloto`, revisión `712c78664074732a612b47a8fa4a7fe45f8c4746`.
- Evidencia de recálculo incorporada: `evidencias/revision-entrega-712c786.json`. Coinciden 120 huellas, histogramas/metadatos de piloto y reproducción de una vista histórica. No se ejecutó Geant4 localmente.
- Se publica revisión con observaciones O-01…O-05; no se declara cerrado el OE1 ni se fusiona la rama de resultados.
- Encargo: propuesta del siguiente ensayo, con observable, correspondencia de primarios, incertidumbre, control y presupuesto, antes de nuevas corridas de producción.

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

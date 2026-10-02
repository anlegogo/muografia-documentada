# Matriz de cumplimiento del OE1

> Avance posterior a la revisión: [fusión y compatibilidad corregidas localmente](CORRECCIONES_LOCALES_FUSION_CONFIGURACION.md), 56 pruebas y contraste con los dos bloques reales. Las observaciones físicas siguen abiertas; adoptar la alternativa en SC3 requiere actualizar las herramientas allí.

> Actualización 2026-10-02: se recibió y revisó la entrega física/producción. Consultar la [revisión vigente](REVISION_FISICA_PRODUCCION_2026-10-02.md) antes de aplicar solicitudes o estados anteriores. La ampliación posterior está documentada en las correcciones locales enlazadas arriba.

Estado consolidado al 2026-10-01, Colombia. Valoración técnica, no calificación académica. «Verificado» se limita a la evidencia descrita.

| ID | Aspecto | Evidencia y estado | Pendiente |
|---|---|---|---|
| OE1-01 | Escenarios volcánicos | Catálogo de 19 geometrías; diagnóstico propio y controles favorables recibidos de la construcción B. Parcial para el conjunto final. | Alcance y sustitución de referencias: P-01. |
| OE1-02 | Simulación Monte Carlo | 114 referencias históricas; etapas 1/2 auditadas; integración de malla nueva ejecutada por estudiantes en SC3, 1.000 primarios. Verificado para los archivos/ejecuciones revisados. | Campaña corregida definitiva y receta reproducible: P-01/P-02. |
| OE1-03 | Niveles de conteo | 9.120 pares históricos reproducidos. Reducción binomial nueva implementada y probada, con 80 pares por vista y sin recorte uint16. | Alimentarla con referencias finales físicamente justificadas: P-04. |
| OE1-04 | Organización y trazabilidad | Lectura, exportación, gráficos, ROI y empaquetado versionados; huellas, procedencia, semillas y particiones por geometría. Verificado mediante 41 pruebas y una referencia nueva real. | Ejecutar la cadena sobre la campaña completa y publicar su ficha final. |
| OE1-05 | Representatividad y validación física | Controles geométricos y código revisados; contraste de regiones sobre 393.216 rayos. Parcial. | Aceptación del plano, muestreo espacial/angular y exposición: P-04. |
| OE1-06 | Reproducción independiente | Auditoría de 48,7 millones de registros de etapa 2; corrección angular y entrega verificadas; nueva alternativa local de preparación probada. | No se reprodujo Geant4 localmente; falta cerrar la receta de campaña y su alcance: P-02/P-03. |

**El OE1 sigue abierto por la validación física y la definición/producción del conjunto final**, no por ausencia de herramientas de organización. No se asigna un porcentaje global de avance sin una rúbrica acordada.

Consultar [cadena local y siguiente entrega](CADENA_LOCAL_OE1.md), [pendientes](PENDIENTES.md), [auditoría de etapa 2](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md), [corrida angular](REVISION_MALLA_ANGULAR_2026-10-01.md) y [aceptación física](REVISION_ACEPTACION_PLANO.md).

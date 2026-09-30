# Pendientes del OE1

**Paso actual:** [revisión independiente de etapa 1](REVISION_ETAPA_1_2026-09-30.md), con 405 comprobaciones reproducidas y 156 controles propios sin fallos. Falta el complemento R2-01 de entrada desde el conducto y el dimensionamiento de etapa 2. P-01…P-04 siguen abiertos; el [protocolo v1.0](PROTOCOLO_SEGUNDO_ENSAYO_OE1.md) se conserva sin cambios.

**Preparación local completada:** [complemento R2-01](COMPLEMENTO_R2_01.md), con 12 primarios dirigidos, controles geométricos y ejecutor para 72 transportes en SC3. La lista fue validada localmente; su transporte sigue pendiente.

Todos los siguientes puntos permanecen abiertos; no se asigna a los estudiantes una actividad como realizada sin evidencia.

**Estado al 29 de septiembre:** la [primera entrega revisada](REVISION_ENTREGA_2026-09-29.md) respalda controles geométricos favorables de B en 114 casos y la reproducción exacta de una vista histórica. P-01 avanza en corrección geométrica, pero conserva pendiente el impacto físico y la decisión de regeneración; P-02 avanza para ese entorno/caso SC3, sin certificar otros entornos. P-03/P-04 continúan abiertos. El nuevo encargo es una [propuesta de ensayo](DISENO_SIGUIENTE_ENSAYO_OE1.md), no repetir las 114 vistas.

**Actualización de revisión:** el [diagnóstico local](DIAGNOSTICO_GEOMETRIAS.md) demuestra intersecciones en cuatro geometrías y salidas del edificio en otras dos. Los [9.120 pares se reprodujeron](REVISION_DATOS.md); ese resultado no cierra P-01. Las [instrucciones de SC3](INSTRUCCIONES_ESTUDIANTES.md) preparan el siguiente ensayo.

| ID | Hallazgo / necesidad | Evidencia | Condición de cierre |
|---|---|---|---|
| P-01 | Advertencias de solapamiento de volúmenes Geant4 | 68 de 199 logs incluyen GeomVol1002, contando duplicados; seis geometrías identificadas en el registro | Revisar construcción geométrica, ejecutar controles sin solapamientos y comparar conteos/contrastes antes y después. Cuantificar impacto y decidir qué datos deben regenerarse. |
| P-02 | Entornos históricos diferentes | Dockerfile declara v11.3.2; entorno SC3 y datos declaran 11.4.2 | Documentar y comprobar el entorno que reproduce la campaña, incluidas dependencias y generador. No asumir equivalencia entre versiones. |
| P-03 | Reproducción histórica incompleta | Bitácora refiere `run_campaign.py`, `run_pilot.py`, `dataset/DATASHEET.md` y documentos de etapas no presentes; piloto gráfico depende de CSV histórico no entregado | Obtener originales si son necesarios para repetir esos pasos, o documentar una alternativa reproducible claramente identificada como nueva. |
| P-04 | Transferencia de controles analíticos a campaña Geant4 | Validación surrogate y comparación entre motores recibidas | Identificar controles aplicables al transporte final y justificar sensibilidad al flujo, área de generación y normalización temporal; no extrapolar automáticamente el éxito del surrogate. |

Geometrías con advertencias identificadas: `geo-gen-01`, `geo-test-01`, `geo-test-03`, `geo-train-06`, `geo-train-08`, `geo-train-11`. La corrección de trazado de ROI mencionada en la revisión global no corrige por sí misma la construcción de volúmenes Geant4. El efecto sobre resultados no se ha cuantificado: no se afirma que todos los datos sean inválidos ni que las advertencias sean inocuas.

[Detalle de advertencias](evidencias/advertencias-simulacion.json). Una futura corrección tendrá código, datos derivados y comparación separados de los originales.

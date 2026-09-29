# Pendientes del OE1

Todos los siguientes puntos permanecen abiertos; no se asigna a los estudiantes una actividad como realizada sin evidencia.

| ID | Hallazgo / necesidad | Evidencia | Condición de cierre |
|---|---|---|---|
| P-01 | Advertencias de solapamiento de volúmenes Geant4 | 68 de 199 logs incluyen GeomVol1002, contando duplicados; seis geometrías identificadas en el registro | Revisar construcción geométrica, ejecutar controles sin solapamientos y comparar conteos/contrastes antes y después. Cuantificar impacto y decidir qué datos deben regenerarse. |
| P-02 | Entornos históricos diferentes | Dockerfile declara v11.3.2; entorno SC3 y datos declaran 11.4.2 | Documentar y comprobar el entorno que reproduce la campaña, incluidas dependencias y generador. No asumir equivalencia entre versiones. |
| P-03 | Reproducción histórica incompleta | Bitácora refiere `run_campaign.py`, `run_pilot.py`, `dataset/DATASHEET.md` y documentos de etapas no presentes; piloto gráfico depende de CSV histórico no entregado | Obtener originales si son necesarios para repetir esos pasos, o documentar una alternativa reproducible claramente identificada como nueva. |
| P-04 | Transferencia de controles analíticos a campaña Geant4 | Validación surrogate y comparación entre motores recibidas | Identificar controles aplicables al transporte final y justificar sensibilidad al flujo, área de generación y normalización temporal; no extrapolar automáticamente el éxito del surrogate. |

Geometrías con advertencias identificadas: `geo-gen-01`, `geo-test-01`, `geo-test-03`, `geo-train-06`, `geo-train-08`, `geo-train-11`. La corrección de trazado de ROI mencionada en la revisión global no corrige por sí misma la construcción de volúmenes Geant4. El efecto sobre resultados no se ha cuantificado: no se afirma que todos los datos sean inválidos ni que las advertencias sean inocuas.

[Detalle de advertencias](evidencias/advertencias-simulacion.json). Una futura corrección tendrá código, datos derivados y comparación separados de los originales.

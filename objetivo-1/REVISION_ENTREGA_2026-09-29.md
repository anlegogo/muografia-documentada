# Revisión de la primera entrega OE1 — 29 de septiembre de 2026

**Estado: revisada con observaciones; validación física del OE1 abierta.** Esta revisión registra evidencia y límites; no aprueba una nueva campaña ni fusiona el código de los estudiantes.

## Entrega examinada

Autores de la entrega: Reinaldo Cárdenas Tirado y Daniel Andrés Pinto Ortega. Rama `oe1/geo-train-06-piloto`, revisión fija [`712c78664074732a612b47a8fa4a7fe45f8c4746`](https://github.com/anlegogo/muografia-documentada/tree/712c78664074732a612b47a8fa4a7fe45f8c4746/objetivo-1/entregas/2026-09-29-geo-train-06). Su carpeta contiene informe, parches, registros de entorno/compilación, controles geométricos, reproducción histórica y piloto A/B. `main` conserva por separado los originales y esta revisión.

## Comprobaciones independientes realizadas

| Aspecto | Evidencia contrastada | Resultado y alcance |
|---|---|---|
| Integridad de la entrega | Manifiesto frente a archivos versionados | 120/120 huellas coinciden. La exportación Windows alteró finales de línea de 71 textos; se verificaron los blobs Git y se restauró la copia de revisión a esos bytes antes del contraste. No se atribuye esa conversión local a los estudiantes. |
| Reproducción histórica | Histograma entregado frente a NPZ original de geo-train-06, vista 0 | Igualdad elemento a elemento; 27.209.253 detectados. Reproducibilidad respaldada para ese caso, no para todos los entornos ni geometrías. |
| Control geométrico T1 | Tabla de 228 ejecuciones y 228 resúmenes del archivo de logs | A: 36 salidas con defecto y 78 sin defecto; B: 114 sin defecto declarado. Evidencia favorable de la corrección bajo el muestreo usado; no prueba matemática universal de navegación. |
| Piloto | Seis histogramas, metadatos, registros y huellas por corrida | Un millón de eventos por corrida; sumas coincidentes con metadatos; A registra GeomVol1002, B no registra GeomVol1002/GeomNav. |
| Comparación A/B | Diferencia directa de histogramas | Primeras dos semillas: igualdad completa. Tercera: dos píxeles distintos, diferencia absoluta total de dos cuentas; total global igual. |
| Región R_int | Máscara entregada aplicada a histogramas | Conteos 2, 0 y 2 por semilla en cada variante: cuatro eventos acumulados por variante. No basta para estimar un efecto físico pequeño con precisión. |

Los artefactos fuente se consultan en la revisión fija enlazada arriba. Los recálculos de revisión están en [evidencia independiente](evidencias/revision-entrega-712c786.json). No se compiló ni ejecutó Geant4 localmente. El examen de parches y resultados no sustituye una revisión completa de todo el código de diagnóstico ni reproduce todos los análisis de ROI de los autores.

## Observaciones que deben atenderse

**O-01 — Separar corrección geométrica e impacto físico.** La entrega respalda la eliminación de advertencias en los controles ejecutados y mejora la trazabilidad. El piloto sigue siendo inconcluso sobre el cambio físico. Igualdad de conteos globales no demuestra equivalencia de distribuciones o de efectos locales.

**O-02 — No identificar eventos mediante diferencias agregadas.** Dos píxeles con diferencias −1/+1 son compatibles con un desplazamiento de bin, pero también con cambios compensados de varios eventos. Sin correspondencia de primarios y registros individuales, escribir «diferencia neta de dos celdas»; no afirmar que se identificó un único evento ni que todos los demás fueron idénticos. La igualdad de semillas no prueba esa correspondencia.

**O-03 — Revisar el cálculo de presupuesto.** El cociente 1/3.000.000 obtenido interpretando diferencias de bins no constituye una tasa medida de eventos cambiados. Tampoco permite asegurar que sea una estimación conservadora para cruces de frontera de una ROI: pueden existir cancelaciones invisibles en histogramas. Los escenarios de presupuesto de la entrega son exploratorios y no se aprueban para ejecución. El cálculo definitivo debe corresponder al observable, a su incertidumbre y a una diferencia físicamente relevante definida antes del ensayo.

**O-04 — Preservar el alcance de la corrección.** La regla «última anomalía del JSON prevalece» tiene una justificación de consistencia con el motor analítico que debe conservarse expresamente. El parche usa un margen de recorte de 1 mm: documentar su efecto o cota y evitar describirlo como identidad geométrica exacta en las superficies. Los casos combinados de recorte y múltiples sustracciones que el propio parche declara no ensayados siguen fuera de la evidencia disponible.

**O-05 — Registrar los controles y el entorno.** Conservar el ensayo sin defecto geométrico como control del nuevo diagnóstico. La reproducción histórica resuelve parte importante de P-02 en SC3 para un caso; no acredita el Docker de otra versión ni cierra P-03/P-04.

## Disposición de seguimiento

- Primera entrega: **revisada con observaciones**. Reconocer las comprobaciones satisfactorias y conservar también fallos/reintentos reportados.
- P-01: controles geométricos favorables; impacto físico y decisión de regeneración pendientes.
- P-02: entorno SC3 y reproducción de un caso respaldados; alcance limitado documentado.
- P-03/P-04: siguen abiertos.
- Siguiente entrega: **propuesta de ensayo**, siguiendo [DISEÑO_SIGUIENTE_ENSAYO_OE1.md](DISENO_SIGUIENTE_ENSAYO_OE1.md). Requiere revisión del director antes de nuevas corridas de producción. No repetir las 114 vistas por esta instrucción.

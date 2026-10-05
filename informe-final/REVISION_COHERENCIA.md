# Revisión de coherencia de la integración

Fecha: 2026-10-04, Colombia. Revisión editorial sobre los resultados congelados; no se repiten evaluaciones científicas ni se modifican sus criterios.

## Propuesta y balance

La fuente aprobada es `Plan_trabajo_grado.pdf`, SHA-256 `7404530659aab451897ac1eb0be05c8fe7ce9b5c96b0131b18fc638684d51084`. Se contrastó la transcripción de sus objetivos con la extracción conservada y con la [revisión directa](../docs/REVISION_PROPUESTA_APROBADA.md). No se adopta como literal la inserción de «(cGAN)» del informe histórico OE2. El objetivo 2 se refiere a redes generativas adversarias condicionales; la sigla se utiliza como abreviatura del texto explicativo.

| Aspecto | Decisión incorporada | Evidencia |
|---|---|---|
| Objetivos y alcance | OE1 cerrado idealizado; calidad comparable OE2 parcial; OE3 experimental cerrado y científico parcial. | Registros de cierre y revisión de propuesta. |
| Unidad de análisis | 19 geometrías, 114 vistas, 9.120 pares; no se confunden realizaciones con escenarios. | Ficha OE1 y capítulo 3. |
| Presupuesto | 344 millones de primarios por vista; no por píxel ni eventos detectados. | Receta y ficha. |
| Particiones | 12/3/3 más una de generalización; adaptación respecto de 70/15/15. | Se conserva la separación original por geometría; no se redistribuyen datos tras evaluar. |
| Entrenamiento | Originales seleccionados en época 5, ejecuciones de 12/13 épocas; seis continuaciones de cinco épocas. | Síntesis y protocolo OE2. |
| Fracciones | Entrenamiento al 5 %; evaluación multifracción de los mismos pesos. | OE3-C1. |
| Transformación | Logaritmo natural, escala fija de entrenamiento e inversa antes de métricas de cuentas. | Definiciones y fórmulas del capítulo 3. |
| Q | Porcentaje en tablas; fracción en CSV; sesgo regional agregado, no error de densidad. | Síntesis OE2 y CSV auditado. |
| Contraste | La tabla local actual usa soporte multifracción y error antes de promediar. No se copia como equivalente el contraste C2 histórico. | Auditoría OE3-C1. |
| SNR/CNR | Dispersión espacial y signo explícitos; donantes únicos para desviación de fondo. | Protocolo local. |
| Factor | Referente 50 %, no 100 %; conjunto vacío implica nulo/no demostrado. | 768 filas por vista. |
| Razón 2:1 | Comparación descriptiva SSIM/PSNR, sin declararla factor físico aceptado. | Desglose OE3. |
| Opacidad | X en g/cm², C_N adimensional; densidad nominal distinta de material efectivo. | Diagnóstico nominal. |
| Figuras | Seis figuras existentes, introducidas antes de aparecer y con selección/escala explicadas. | Fuentes OE1, OE2 y OE3 enlazadas. |
| Integridad | Recálculo de métricas no equivale a nueva inferencia GPU ni a nueva campaña Geant4. | Auditorías. |

## Ajustes frente a textos históricos

Se reemplaza en esta integración el alcance histórico «solo 5 % evaluado» por la distinción entre entrenamiento al 5 % y evaluación en cuatro fracciones. Se conserva la fecha y la integridad de los informes anteriores, sin reescribir entregas estudiantiles.

La exposición previa de las reservas y el carácter posterior del benchmark permanecen explícitos. No se presentan los umbrales como originales de la propuesta, ni los casos de generalización como una población de volcanes. Se conservan las siete excepciones de roca y las seis filas nominales con advertencia de material.

Los valores de contraste de la tabla C2 histórica no se trasladan a las nuevas tablas: sus soportes y orden de agregación difieren. Las tablas 4.1–4.3 proceden de una única síntesis auditada; SSIM/PSNR/Q no se filtran por el soporte local.

## Verificación documental

La [verificación editorial](VERIFICACION.json) registra comprobaciones de estructura, enlaces a archivos, conteos y consistencia de las tablas con la fuente. El [registro de fuentes](FUENTES.json) conserva el árbol base y las identidades Git de las fuentes utilizadas. Las cifras publicadas se redondean solo para lectura; el CSV mantiene precisión.

Esta revisión no es una segunda auditoría numérica de las predicciones ni una compilación de LaTeX. Las imágenes se reutilizan sin modificación desde las figuras previamente documentadas; no se afirma una nueva inspección de los datos originales.

## Estado editorial

Queda preparado y revisado el núcleo experimental: metodología, resultados, discusión y conclusiones de los tres objetivos. OE3-P04 avanza a integración del núcleo completada en el repositorio. Persisten la maquetación institucional y la revisión/presentación por autores, que no requieren nuevas corridas. La elaboración de texto no cambia el cumplimiento científico parcial del cierre experimental.

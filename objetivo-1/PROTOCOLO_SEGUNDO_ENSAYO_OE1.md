# Protocolo del segundo ensayo OE1 — versión 1.0

**Fecha:** 29 de septiembre de 2026 (Colombia). **Diseño de la revisión/director; implementación y ejecución:** Daniel y Reinaldo en SC3. **Estado:** primera etapa definida para preparación y ejecución diagnóstica; segunda etapa condicionada a revisar sus resultados. No se aprueba repetir la campaña de 114 vistas.

Este protocolo sustituye el encargo de redactar un diseño desde cero. Los estudiantes deben comprobar su viabilidad técnica y documentar cualquier desviación antes de ejecutar. «Recursos de cómputo» significa eventos, corridas, procesadores, memoria, almacenamiento y tiempo; no es un presupuesto económico.

## 1. Pregunta y alcance

¿Cuánto cambia la probabilidad de detección en la región angular del solapamiento al sustituir la geometría recibida A por la corregida B, manteniendo los mismos muones iniciales y las demás condiciones?

Caso principal: `geo-train-06`, vista 0. Control: `geo-train-01`, vista 0. A conserva el defecto únicamente como referencia histórica de diagnóstico; no se considera una geometría físicamente válida. B aplica la regla de prioridad documentada, sin modificar densidades ni posiciones del catálogo. Conservar la referencia al margen de recorte de 1 mm y las diferencias de densidad del aire entre motores. No intervienen redes neuronales ni métricas de OE2/OE3.

## 2. Preparación y condiciones comunes

1. Conservar A/B y las fuentes originales. Crear una rama y carpeta nuevas para la instrumentación y estas corridas. Identificar revisiones y diferencias de código; no sobrescribir el primer piloto.
2. Usar Geant4 11.4.2 y el entorno SC3 documentado. Mantener FTFP_BERT, cortes, secundarios, generador/tablas y detector del piloto. Registrar módulos, compilador y huellas de ejecutables, catálogo y tablas.
3. Separar la instrumentación de la corrección geométrica. Comprobar que registrar eventos no cambia sus condiciones iniciales ni consume números aleatorios usados por el transporte; si los consume, corregirlo o aislar el flujo aleatorio.
4. Ejecutar los controles geométricos de B con resolución/tolerancia registradas. Una advertencia nueva, resultado truncado o discrepancia de entradas bloquea la comparación y debe reportarse. Los defectos históricos de A se conservan expresamente como parte del diagnóstico.

## 3. Muones iniciales reproducibles

Generar una lista de primarios por caso y réplica **antes** de ejecutar A/B, mediante el mismo modelo de fuente del piloto. Guardar identificación, posición (m), dirección unitaria, energía con tipo y unidad explícitos (por ejemplo, cinética en GeV) y especie/carga. Ambos ejecutables deben leer exactamente esa lista, con igual asignación identificador→primario. No basta compartir la semilla.

Separar las semillas de generación y de transporte. Registrar ambas; si se comparten números aleatorios de transporte entre A/B, indicar cómo se reinician por evento y verificar que cambiar la geometría no impide la correspondencia de primarios. No exigir igualdad de las trayectorias finales: esa es parte del fenómeno que se estudia.

Antes del transporte, comprobar igualdad de identificadores y condiciones iniciales A/B, ausencia de duplicados y número esperado. Usar un hilo por proceso en esta primera etapa para simplificar trazabilidad. Una futura ampliación multihilo deberá verificar de nuevo ese contrato.

## 4. Primera etapa: verificar instrumentación y recoger diagnóstico

| Parámetro | Valor propuesto para esta etapa |
|---|---|
| Geometrías | geo-train-06 y geo-train-01 |
| Vista | 0 en ambas |
| Variantes | A y B |
| Réplicas independientes | 3 por caso y variante |
| Primarios por corrida | 100.000 |
| Identificadores de réplica / semillas de fuente propuestas | 2026092901, 2026092902, 2026092903 |
| Transporte | Documentar semillas independientes de la fuente; mismo esquema en A/B |
| Hilos | 1 por proceso |
| Corridas principales | 12; 1.200.000 transportes en total |

Añadir una repetición exacta A/A del control `geo-train-01`, primera réplica, con 100.000 eventos, mismos primarios y estado/semillas de transporte. Total de la etapa: **13 corridas y 1.300.000 transportes**. La repetición técnica no cuenta como réplica estadística independiente.

Este tamaño comprueba la instrumentación; **no está dimensionado para detectar un efecto físico pequeño**. Cero eventos en la ROI no constituye un fallo si todos los contratos se cumplen. Si SC3 requiere otros recursos o la instrumentación aumenta mucho el coste, informar el ajuste propuesto; no multiplicar los eventos por iniciativa de esta instrucción.

### Registros mínimos por primario y variante

- Caso, réplica, identificador estable y huella de la lista de primarios.
- Detección sí/no; bin final o valor ausente para no detectados; pertenencia a ROI.
- Cruce sí/no de la región tridimensional original de intersección conducto/elipsoide; longitud acumulada dentro de ella (m), material asignado y energía de entrada/salida cuando sea aplicable.
- Estado de finalización, para distinguir no detección de una corrida incompleta.

La región 3D debe definirse por las primitivas originales y calcularse en coordenadas comunes a A/B; no por un volumen que desaparece en la geometría corregida. Especificar cómo se detectan cruces dentro de un paso y su error geométrico, especialmente cuando ambos extremos del paso están fuera. Un indicador que solo examina extremos puede omitir un cruce. Preparar controles analíticos de trayectorias que atraviesan, rozan y evitan la región antes de interpretar este diagnóstico.

Conservar **todos los primarios**, incluidos no detectados. Para cada variante, sumar registros y reconstruir su histograma; debe coincidir exactamente con la salida ordinaria de esa misma corrida. A/A con estado completo idéntico debe reproducirse; una discrepancia requiere explicación y corrección antes de usar diferencias A/B. El control A/B sin defecto se analiza aparte: una diferencia no implica automáticamente un error, pero debe explicarse antes de atribuir diferencias del caso afectado al solapamiento.

## 5. Observable principal y diagnósticos secundarios

Usar la máscara `R_int` de la entrega `712c786`, sin redefinirla viendo resultados nuevos. Congelar su huella, dimensiones, orientación y relación con bins. Para `geo-train-01`, aplicar esa misma máscara angular como control; no denominarla región de una intersección inexistente.

Para cada primario i, definir `Y_A,i` y `Y_B,i` iguales a 1 si se detecta dentro de R_int, y 0 en caso contrario. Observable principal:

`Delta = promedio(Y_B,i − Y_A,i)`

Unidad: cambio de probabilidad de detección en la ROI por primario generado. Reportar también `10^6 × Delta` como cuentas por millón de primarios, indicando el denominador.

Registrar por réplica los cuatro conteos de transición: 0→0, 0→1, 1→0 y 1→1. Su suma debe ser N; la diferencia neta es `(n01−n10)/N`. Esto mide transiciones verificadas y evita deducirlas de diferencias agregadas de píxeles.

Secundarios: eficiencia total, matriz de cambios de bin, histogramas normalizados, número de primarios que cruzan la región 3D y longitudes/materiales recorridos. Si se analiza solo quienes cruzan, definir la selección común —por ejemplo, unión de identificadores que cruzan en A o B— y mostrar su denominador. Ese análisis condicional no sustituye el observable principal sobre todos los primarios.

## 6. Segunda etapa: estimación física, pendiente de dimensionamiento

Después de revisar la primera etapa, fijar por escrito **antes de nuevas corridas**:

- Margen de diferencia físicamente relevante y justificación; no deducirlo del resultado más favorable del piloto. No se establece un porcentaje arbitrario como requisito del plan aprobado.
- Método e intervalo de incertidumbre compatible con conteos escasos y pares, incluidas transiciones nulas. No usar desviación entre tres réplicas igual a cero como incertidumbre cero.
- Tamaño fijo de eventos y réplicas nuevas independientes, o reglas explícitas de un diseño secuencial. Los datos de desarrollo se mantienen separados del ensayo confirmatorio.
- Tiempo, procesadores, memoria y almacenamiento estimados con el coste medido en la primera etapa. Verificar límite de eventos por ejecución y fraccionamiento por bloques del simulador.

La decisión del director fijará esos valores en una versión 1.1 del protocolo. **La versión 1.0 no autoriza todavía ejecutar esta segunda etapa.** No se usará como tasa medida la suposición de «un evento cambiado» deducida del primer piloto.

Reglas de interpretación de la segunda etapa: intervalo enteramente dentro del margen justificado → evidencia de equivalencia acotada a ese observable/caso; intervalo que indique una diferencia relevante → evaluar regeneración y ampliación; intervalo que no permita ninguna conclusión → resultado inconcluso. Un efecto estadísticamente distinto de cero puede ser pequeño y no relevante; no confundir ambas preguntas. Ninguna conclusión de una vista certifica las 114 vistas.

## 7. Entrega y criterio de avance

Crear una carpeta nueva de entrega en su rama y presentar `RESULTADOS_ETAPA_1.md`, con:

1. Revisión de implementación, comandos, entorno y cambios respecto a este protocolo.
2. Contrato y huellas de primarios; prueba de correspondencia A/B y repetición A/A.
3. Pruebas del detector de cruces 3D, controles geométricos y reconstrucción de histogramas.
4. Tabla por corrida con N, transiciones, cruces, detectados, avisos y tiempo; archivos con registros o enlace a almacenamiento compartido y manifiesto SHA-256.
5. Fallos/reintentos y limitaciones, sin ocultar los resultados nulos.
6. Propuesta de margen, incertidumbre y recursos para la etapa 2, apoyada en lo observado y distinguiendo datos de supuestos.

Se revisarán primero los contratos y controles técnicos. Solo si son suficientes se dimensionará la etapa 2. Continúan abiertos P-01/P-04; el volumen geométrico ya contrastado no reemplaza esta medición del transporte.

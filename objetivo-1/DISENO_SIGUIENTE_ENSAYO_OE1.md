# Segundo encargo OE1 — diseñar el ensayo antes de ampliar simulaciones

**Destinatarios:** Daniel y Reinaldo. **Entrega solicitada ahora:** propuesta breve en Markdown y estimación de recursos; no una campaña nueva. Alcance exclusivo: simulación y generación de datos del OE1.

## Pregunta que debe responder el diseño

¿La corrección geométrica cambia los conteos o su distribución en una magnitud físicamente relevante para las imágenes muográficas, con una incertidumbre que permita decidir?

La primera entrega demuestra avances geométricos y reproducibilidad de un caso. El piloto tiene pocos conteos en la región afectada; no determina todavía el tamaño del efecto. Leer primero las observaciones [O-01 a O-05](REVISION_ENTREGA_2026-09-29.md).

## Contenido obligatorio de la propuesta

### 1. Observable, región y diferencia relevante

- Proponer **un observable principal**, con fórmula, unidades y normalización: por ejemplo, probabilidad de detección en una ROI fija por primario generado. Separar observables secundarios y diagnósticos.
- Fijar región de interés, orientación, máscara y huella antes de las nuevas corridas. Si se cambia la ROI previa, justificarlo y conservar ambas versiones; no elegirla viendo qué diferencia resulta mayor.
- Definir una diferencia mínima relevante o margen de equivalencia con justificación física. Un porcentaje sobre una cuenta próxima a cero puede ser inestable: considerar una escala absoluta por primario o exposición claramente definida.
- Explicar a qué vistas/geometrías aplicaría una conclusión favorable. Un caso no certifica toda la campaña.

### 2. Correspondencia de eventos y diagnóstico del transporte

Proponer una identificación estable de cada primario (corrida, semilla/archivo de entrada, identificador del evento y del primario), y registrar posición inicial, dirección, energía y carga. Verificar que los primarios de A y B coinciden antes de interpretar diferencias pareadas. Si el generador no asegura correspondencia, proponer reproducción de una lista común de primarios o un diseño independiente con su incertidumbre correspondiente.

Definir cómo se identificarán los primarios cuyas trayectorias atraviesan la región geométrica original del solapamiento. No confundir el cruce de esa región tridimensional con caer en una ROI angular del detector. A y B pueden recorrer trayectorias distintas; registrar el cruce por variante y distinguir ambos casos. Para un análisis condicional usar una selección predefinida, como la unión de los identificadores que cruzan en A o B, e indicar el denominador; ese análisis no reemplaza el observable principal sobre todos los primarios.

Para el diagnóstico, proponer los campos mínimos: cruce/no cruce, longitud recorrida en la región y material asignado, detección/no detección, bin final y pertenencia a la ROI. Incluir primarios no detectados para evitar sesgo de selección. Un registro reducido por evento o contadores de transiciones pueden ser suficientes; estimar su coste sin guardar todas las trayectorias por defecto.

Compartir semillas no garantiza ni primarios idénticos ni transporte pareado válido. Si se usan números aleatorios comunes, documentar cómo se mantiene la correspondencia con los hilos y la asignación de eventos, y qué puede cambiar tras la corrección.

### 3. Incertidumbre y presupuesto

- Si hay pares válidos, definir una variable por primario para el observable (p. ej., indicador de detección en ROI de B menos el de A) y registrar cambios 0→1 y 1→0 por separado. Las diferencias netas de histogramas no dan esos conteos.
- Definir la unidad de replicación, número de réplicas y procedimiento para intervalos con conteos escasos o cero cambios. No interpretar desviación muestral cero con tres réplicas como incertidumbre nula.
- Calcular un rango de presupuesto basado en el margen elegido y en supuestos explícitos; mostrar sensibilidad a supuestos. No usar la tasa de «un evento cambiado» del piloto como una medición establecida.
- Indicar si se busca detectar una diferencia o demostrar equivalencia dentro de un margen. Ausencia de significación no demuestra equivalencia.
- Si se propone un diseño secuencial, fijar tamaños de etapas, reglas de parada y tratamiento estadístico antes de observar las nuevas diferencias.

### 4. Caso afectado y control

Mantener inicialmente `geo-train-06`, vista 0, para continuidad; incluir `geo-train-01` como control sin defectos identificados en el catálogo revisado. Mantener entre variantes física, generador, entradas, detector, presupuesto y entorno. Definir antes del ensayo qué desviaciones del control obligan a investigar la instrumentación o cambios ajenos a la geometría.

El control no permite inferir que otras geometrías afectadas sean equivalentes. Proponer cuándo sería necesario ampliar a otras vistas y a los defectos de salida del edificio, distintos del solapamiento entre anomalías.

### 5. Recursos y trazabilidad

Presentar eventos por corrida, variantes, réplicas, hilos, memoria, almacenamiento y rango de tiempo de pared/horas de CPU; distinguir estimaciones de mediciones. Verificar límites de eventos y particionamiento por bloques de la aplicación antes de plantear corridas grandes.

Registrar revisión del código y cambios de instrumentación por separado de la corrección geométrica. Conservar la versión inicial, parches, parámetros, máscaras, comandos y huellas. La instrumentación debe comprobarse con ensayos mínimos después de la revisión del diseño; no presentar resultados sintéticos de prueba como transporte científico.

## Formato de respuesta sugerido

Crear `PROPUESTA_SEGUNDO_ENSAYO.md` en la carpeta de su entrega, dentro de su rama de trabajo, con estas secciones:

1. Respuesta a O-01…O-05 (corrección documental, evidencia o limitación).
2. Observable principal, ROI y margen relevante.
3. Correspondencia de primarios y diagnóstico de cruces.
4. Incertidumbre, réplicas y regla de decisión.
5. Casos, controles y variables conservadas.
6. Presupuesto por etapa y recursos.
7. Limitaciones y decisiones que solicitan al director.

No rellenar como aprobado el diseño por anticipado. No cambiar originales ni borrar el primer piloto. Pueden preparar código y pruebas de diagnóstico de bajo coste para revisión, claramente identificadas; **esta solicitud no autoriza aumentar la campaña de producción**.

## Qué revisaremos antes de ejecutar

| Criterio | Evidencia esperada |
|---|---|
| Pregunta medible | Observable, unidad, denominador, ROI y margen justificados. |
| Comparación válida | Correspondencia comprobable de primarios o diseño independiente explícito. |
| Precisión interpretable | Método compatible con conteos escasos, réplicas y presupuesto. |
| Control de cambios | Caso sin defecto, entorno y modificaciones separados. |
| Coste acotado | Primera etapa razonable, criterio de parada y límites de recursos. |
| Conclusión delimitada | Qué resultado permitiría decidir, qué sería inconcluso y qué quedaría fuera. |

**Estado del diseño: pendiente de entrega y revisión.** Con una propuesta suficiente, el director definirá el ensayo acotado a ejecutar; con sus resultados se decidirá la ampliación y el alcance de una eventual regeneración de datos.

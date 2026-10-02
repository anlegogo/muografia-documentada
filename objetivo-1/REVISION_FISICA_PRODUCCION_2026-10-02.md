# Revisión de la justificación física y propuesta de producción

> Avance posterior a la revisión: [fusión y compatibilidad corregidas localmente](CORRECCIONES_LOCALES_FUSION_CONFIGURACION.md), 56 pruebas y contraste con los dos bloques reales. Las observaciones físicas siguen abiertas; adoptar la alternativa en SC3 requiere actualizar las herramientas allí.

Revisión del director, 2026-10-02, Colombia. Rama de los estudiantes: `oe1/justificacion-fisica-produccion`, commit **f9a77eff49c01bfd073c00d7d62414e3ce962f9d** (ocho commits sobre `18aa5b1`). [Entrega congelada](https://github.com/anlegogo/muografia-documentada/tree/f9a77eff49c01bfd073c00d7d62414e3ce962f9d/objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion).

**Dictamen: avance sustancial y resultados numéricos reproducibles, con observaciones que impiden declarar validada la receta o habilitar la campaña final.** Se recuperó parte del respaldo histórico, se documentó el entorno, se ejecutaron controles nuevos y existe una propuesta de producción. No basta resolver C6 para dar por cerrada la física. La rama se conserva sin fusionar en `main`.

## Qué se comprobó localmente

- Se revisaron 19 corridas de control, que suman **92 millones de primarios transportados**. Los 19 histogramas tienen dimensiones y conteos coherentes con sus metadatos; los códigos de salida conservados son cero. No son 92 millones de historias independientes: hay reutilización de semillas y regresiones.
- Se ejecutaron los seis análisis Python de la entrega en una copia temporal. Se compararon **3.045 valores numéricos**, sin discrepancias a tolerancia absoluta/relativa de `1e-10`. Esto reproduce los cálculos de los estudiantes; no constituye por sí solo una validación independiente de sus modelos físicos.
- Para reproducir el plan se reconstruyeron los 114 CSV históricos desde los `ref_counts` de los NPZ conservados. Los **114 SHA-256 coinciden** con `campaign-manifest.csv` al usar la representación CSV con CRLF. No se sustituyeron ni modificaron los originales.
- Se repitió la fusión de los dos bloques de integración, normalizando finales de línea únicamente en una copia de trabajo: **200.000 primarios y 69.995 registros con el corte energético**. La matriz coincide con la entregada y se exporta con nuestra herramienta.
- Se reprodujeron tres carencias mediante entradas de prueba: la fusión acepta una semilla incorrecta en el manifiesto; acepta el mismo bloque repetido; nuestro empaquetador no distingue cambios de `oe1_controles` y `reference_histogram` en su firma de compatibilidad. Estas pruebas no describen manipulación de las corridas reales.

[Evidencia estructurada de la revisión](evidencias/revision-fisica-f9a77ef.json). Entorno local: Python 3.12.14, NumPy 2.4.4 y Matplotlib 3.11.1. No se recompiló ni ejecutó Geant4 localmente, no se accedió a SC3 y no se lanzó producción.

## Avances que sí quedan respaldados

1. **Respaldo histórico:** se distinguen las corridas conservadas de la serie antigua de dos millones de eventos cuyos archivos faltan. La nueva serie es evidencia nueva; no recupera retrospectivamente los datos perdidos.
2. **Contención en planos grandes:** para la configuración estudiada, las diferencias entre 600 y 1.200 m son pequeñas. Con inyección junto al cono se reporta y reproduce diferencia cero en esa muestra. Esto respalda la comparación entre esos dos tamaños; no prueba una asíntota matemática ni equivalencia con un panel pequeño.
3. **Nueva configuración candidata:** inyección próxima al cono, margen angular de 5° y registro de muones con energía cinética superior a 3 GeV. El corte de 3 GeV satisface su criterio de razón entre planos de 100 y 600 m en las bandas de roca examinadas.
4. **Entorno:** se aportan módulos, Geant4 11.4.2, GCC 14.2.0, versiones de datos físicos y configuración de compilación. Es un avance concreto de P-02.
5. **Plan:** se propone regenerar las 114 vistas, sin mezclar referencias antiguas con el observable nuevo. Se reproduce la estimación de **8.304,64 horas-núcleo para k=10**; sigue siendo condicional al factor de conteo extrapolado desde geo-train-01/vista 0. No es un presupuesto aprobado ni una garantía de tiempo de pared.

## Observaciones a resolver

### F-01 · La independencia respecto al tamaño de un plano grande no demuestra equivalencia con el detector

En `PUNTOS_NO_DEMOSTRADOS.md`, C1 pregunta por equivalencia con el panel físico, pero contrasta **100 m frente a 600 m**; C3 se descarta porque C1 cumple. Ese paso lógico no está demostrado. Ambos planos pueden capturar casi todos los muones de una fuente restringida y seguir representando un observable diferente del panel de 1,2 m con fuente espacial amplia. Es precisamente la distinción del [control conceptual anterior](REVISION_ACEPTACION_PLANO.md).

La frase sobre desplazamiento de pocos metros y paralaje de un píxel se presenta sin una cota medida para el observable final. C1 se limita además a una geometría homogénea y una vista. El piloto de conteos en geo-train-06 no sustituye automáticamente una comparación de aceptación espacial.

**Acción:** conservar el resultado de contención y retirar por ahora las conclusiones de equivalencia y «C3 no necesaria». Definir si el producto es un estimador direccional idealizado o cuentas de un detector físico. Si se afirma lo segundo, presentar una demostración cuantitativa o un control dirigido con fuente, pesos, referencia y tolerancia apropiados. No implica ordenar sin revisión las 6.600 horas-núcleo estimadas para C3.

### F-02 · La mejora en cielo abierto no cierra por sí sola la normalización

El 99,97 % de C2 corresponde al conteo **sin corte energético**, con los rayos que no intersectan roca inyectados aproximadamente a un metro del panel. La producción propuesta usa E_cin > 3 GeV y una superficie de inyección que depende de la geometría y la dirección. Son definiciones que deben conservarse explícitamente.

Acercar la fuente reduce las pérdidas previas y cambia el experimento. La eficiencia cercana a uno no demuestra que el espectro EcoMug y la integral de Guan representen la misma distribución normalizada en la nueva superficie. La propia entrega documenta diferencias de forma y umbral. Tampoco convierte por sí sola «300 días convencionales» en 300 días de un detector real.

**Acción:** completar C6 junto con una definición de superficie de fuente, distribución conjunta de energía/dirección, área, corte de detección y conversión de conteos a exposición. Se puede adoptar una convención de conjunto sintético, pero debe distinguirse de una calibración física del detector. No se prescribe aquí un factor correctivo ni una tasa alternativa sin esa definición.

### F-03 · El criterio de bordes sigue abierto y debe evaluarse para el observable elegido

Se reproduce una desviación máxima de **1,65 puntos porcentuales**, por encima del umbral de 1 pp. La media pequeña no satisface un criterio aplicado al máximo. La desviación estándar empírica de columnas interiores no es una demostración de ausencia de sesgo.

Además, `controles_sc3.py` evalúa C4 con `h["full"]["0"]` (sin corte), mientras la referencia de producción tiene corte de 3 GeV. El margen también extrapola pesos de filas fuera de las tablas. El piloto deberá especificar qué magnitud contrasta, su expectativa y cómo trata la incertidumbre y las múltiples filas/columnas.

**Acción:** dejar C4 pendiente y preparar su evaluador para la configuración completa. Cerrar F-01/F-02 antes de comprometer una producción grande. No declarar que C6 es el único pendiente.

### T-01 · Los finales de línea rompen la verificación exacta de la entrega

De 200 entradas en los cuatro `salidas.sha256` de controles, **181 no coinciden con los bytes versionados**. Las 181 coinciden al convertir CRLF a LF; no hay discrepancias restantes en ese conjunto. Los histogramas de los dos bloques de integración presentan el mismo problema, por lo que `fusionar_v1.py` falla directamente sobre la entrega extraída de Git.

**Acción:** conservar de forma explícita los bytes de SC3 y su manifiesto, o registrar una conversión con ambos juegos de huellas y procedencia. Establecer atributos Git apropiados. No silenciar ni omitir la verificación SHA. La normalización local usada en esta revisión quedó limitada a copias y no modifica la evidencia original.

### T-02 · La fusión conserva metadatos de un bloque y admite manifiestos inconsistentes

En la entrega real, la vista fusionada declara `detected_all_energies=65050`, aunque la suma correcta es **130190**. Incluso queda por debajo de los 69995 registros con corte. `mean_ekin_detected_gev` y `seconds_per_event` también se heredan del primer bloque; deben agregarse con su semántica correcta o etiquetarse/eliminarse cuando no se pueda obtener la magnitud del conjunto. La media energética disponible es de todos los registros, no de la selección E > 3 GeV.

Las pruebas negativas comprueban que cambiar una semilla del manifiesto sin cambiar el metadato, o repetir una fila/bloque, termina con código cero. La fusión toma las semillas del manifiesto sin contrastarlas y puede contar dos veces un mismo archivo. Comparar conjuntos de hashes de entrada no reemplaza validar la identidad y configuración de cada bloque.

**Acción:** rechazar duplicados y contradicciones de geometría, vista, bloque y semilla; validar formas, conteos y configuración; calcular los agregados con precisión. Incorporar pruebas negativas antes de usarlo para una campaña. No se encontró evidencia de bloques duplicados en la pequeña entrega real.

### T-03 · Nuestra cadena debe reconocer la configuración nueva

El exportador conserva `oe1_controles` y `reference_histogram`, pero la firma de compatibilidad de nuestro `empaquetar_angular_v1.py` no los incluye. El mismo ejecutable puede funcionar con diferente inyección, margen, plano y selección energética. Cambiar esos campos deja la firma actual idéntica: una mezcla podría pasar los controles técnicos.

**Acción de nuestra parte:** extender el contrato y sus pruebas para la configuración nueva, incluyendo definición de fuente/normalización cuando se acuerde. Las 41 pruebas anteriores siguen respaldando el contrato anterior; no certifican estos campos nuevos. Exportar correctamente una vista no prueba todavía el empaquetado de seis vistas con la receta nueva.

## Siguiente entrega acotada

1. Estudiantes: corregir T-01/T-02 y ajustar las conclusiones de C1/C2/C3/C5 al alcance realmente demostrado.
2. Estudiantes y dirección: fijar la definición del producto (F-01/F-02) y el evaluador del piloto (F-03), con criterios previos. El criterio de 100 cuentas es por ROI de 4×4 píxeles, no una precisión del 10 % por píxel.
3. Nuestra parte: adaptar la compatibilidad de la cadena a esa definición y revisar la nueva entrega.
4. Solo después, decidir el piloto P0 y, según sus resultados, el número de muones y la campaña P1. No se requiere repetir los 19 controles por los errores de documentación/fusión ni descartar sus datos.

La entrega representa un avance importante del OE1. La campaña final sigue pendiente, pero ahora las decisiones y correcciones están mejor delimitadas; ya no corresponde solicitar de nuevo, de forma genérica, toda la evidencia de SC3.

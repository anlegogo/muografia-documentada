# Balance de preparación local del OE1

> Avance posterior: [publicación verificada con pruebas de fallos](PUBLICACION_VERIFICADA_BLOQUES.md). Suite ampliada a 78 pruebas; adopción en SC3 y física todavía pendientes.

2026-10-02. Consolida lo realizado después de la entrega `f9a77ef`, con autorización del director. **La cadena local está preparada y probada para el alcance técnico descrito; la interpretación física y la operación de producción en SC3 siguen abiertas.** No se lanzaron transportes nuevos ni se modificó la rama estudiantil.

## Qué ya podemos dar por adelantado

| Frente | Resultado verificable |
|---|---|
| Datos entregados | Seis análisis reproducidos; 19 corridas contrastadas; dos bloques reales de integración procesados. |
| Fusión y trazabilidad | Rechazo de bloques repetidos o inconsistentes; agregados corregidos; huellas exactas o conversión CRLF→LF comprobada y registrada. |
| Imágenes y pares | Lectura, coordenadas, regiones, representación y empaquetado; la compatibilidad incluye la configuración nueva. No se mezclan datos antiguos por cambiar etiquetas. |
| Aceptación espacial | Comparación adicional del panel de 1,2 m y planos grandes con los mismos primarios y corte energético. Delimita la pregunta pendiente sin repetir corridas. |
| Bordes | Diagnóstico aplicado al corte de 3 GeV; se distingue del resultado sin corte y de una prueba estadística de equivalencia. |
| Fuente | Probabilidades calculadas directamente desde las tablas y el algoritmo de ampliación angular; comparación de convenciones de área. |
| Campaña | Revisión offline de alcance, semillas, bloques y presupuestos de los manifiestos k=1/k=10; verificación estricta de los bloques existentes. |
| Definición del producto | [Ficha candidata](contratos/receta-candidata-f9a77ef.json) con lo conocido y las decisiones abiertas; no es una aprobación física. |

**69 pruebas locales satisfactorias**, incluidas nueve nuevas: cuatro de probabilidades de fuente y cinco de preparación de campaña. [Registro](evidencias/pruebas-preparacion-integral.txt) y [huellas/entorno](evidencias/validacion-preparacion-integral.json). El número de pruebas no mide el porcentaje de cumplimiento del OE1.

## Normalización: cálculo nuevo sin simulación

[auditar_fuente_angular.py](../herramientas/auditar_fuente_angular.py) reproduce el algoritmo de `PrimaryGeneratorAction.cc` del parche v3 y la interpolación de cuantiles de `FluxTables.cc`. Usa las tablas angulares v1 con las huellas de la entrega. Tiene en cuenta el paso calculado a partir de los centros redondeados del archivo, el redondeo del número de filas extra y la intersección con los bordes nominales.

Con margen de 5°:

| Magnitud | Valor |
|---|---:|
| Probabilidad de generar dentro de la ventana nominal | **0,6841465610** |
| Fracción observada en c02, 2 millones de primarios | 0,684176 |
| Diferencia, en desviaciones estándar del conteo nominal binomial | 0,090 |
| Masa de generación en filas de elevación extrapoladas | **20,1825 %** |
| Probabilidad de usar el espectro de la banda extrema por estar fuera de 2–47° | **20,5255 %** |
| Probabilidad de energía cinética inicial >3 GeV dentro de la ventana nominal | 54,9091 % |
| Área proyectada vertical / área normal, bajo la convención nominal de tablas | 0,7845532 |

Aquí sí es apropiado un contraste binomial para *dentro/fuera de la ventana al generar*: cada primario tiene una pertenencia definida antes del transporte. Esto es distinto de las razones por píxel entre llegadas y generación nominal, donde existe migración.

La fracción analítica evita usar el ruido de una corrida corta para dimensionar el número total generado. Manteniendo **provisionalmente** el mismo S0 convencional, resultan 52.670.103 primarios por vista para k=1 y 526.701.031 para k=10, frente a 526.678.368 del manifiesto estudiantil k=10: una diferencia de 22.663 eventos por vista, aproximadamente 0,0043 %. **No se modifican los manifiestos congelados ni se aprueba ese N para producción.** La fórmula es N_generados ≈ k·S0 / P(ventana nominal).

El 20 % extrapolado no demuestra un sesgo ni exige descartar datos. Identifica una hipótesis: los pesos fuera de la tabla son una extensión lineal y el espectro de momento se toma de la banda extrema. Debe justificarse si se usa para representar flujo físico. La probabilidad inicial de energía >3 GeV no es la probabilidad de detectarlo con esa energía después de atravesar roca.

La razón de áreas tampoco es un factor correctivo aplicado: cuantifica dos convenciones posibles. No se decide que un panel vertical deba reemplazar al estimador de área normal. S0, el espectro y la superficie de referencia requieren una definición conjunta.

[Resultados completos y huellas](evidencias/probabilidades-fuente-angular.json).

## Campaña: qué se verificó sin acceso a SLURM

[preparar_campana_angular.py](../herramientas/preparar_campana_angular.py) es una revisión previa **offline**. No envía trabajos ni consulta la cola. Valida identidades, semillas únicas, seis vistas por geometría, índices de bloques sin huecos y presupuestos iguales por vista. Si recibe un directorio de bloques, reutiliza el mismo validador estricto que la fusión; no considera un bloque publicado solo porque existan `exit_code.txt` y `salida.sha256`.

| Manifiesto recibido | Vistas | Bloques | Primarios totales | Resultado |
|---|---:|---:|---:|---|
| k=1 | 114 | 228 | 6.004.133.418 | Estructura completa; ejecución no inspeccionada. |
| k=10 | 114 | 1.596 | 60.041.333.952 | Estructura completa; ejecución no inspeccionada. |
| Integración | 1 | 2 | 200.000 | Ambos bloques verificados; faltan cinco vistas para un paquete de esa geometría. |

La herramienta crea una identidad de campaña derivada del contenido del manifiesto y propone nombres de trabajo con ese identificador, para distinguir filas con el mismo número en campañas diferentes. La propuesta no modifica el lanzador de SC3.

El informe siempre conserva `submission_authorized=false`, `physical_validation=false` y `queue_inspected=false`. Un manifiesto completo no prueba que exista cómputo disponible ni que la campaña haya corrido. [Informes de las tres comprobaciones](evidencias/preflight-campana-f9a77ef.json).

### Observaciones operativas aún pendientes de adopción

El lanzador de los estudiantes sigue identificando trabajos solo por número de fila y considera publicados archivos cuya mera presencia comprueba. Su script de bloque no activa salida automática ante todos los errores de shell y puede continuar después de un fallo en operaciones de promoción/publicación. No se sustituyó ese flujo remoto ni se afirma que esté corregido porque el preflight local pase.

Al actualizarlo, deben: usar identidad de campaña, validar un bloque antes de omitirlo, conservar el fallo si copia/movimiento/hash/publicación falla, publicar de forma controlada, y evitar reintentos automáticos ilimitados. La integración con el sistema de colas y los fallos de archivos debe verificarse en su entorno SC3. Puede realizarse con un ejecutable de prueba que falle deliberadamente, antes de consumir transporte Geant4. **No se prescribe aquí otra campaña de física.**

## Definición candidata lista para revisar

La [ficha JSON](contratos/receta-candidata-f9a77ef.json) conserva procedencia de código/parche, binario reportado, tablas, inyección, margen, corte, malla y pares. Describe lo que el código hace, incluida la búsqueda de la superficie del cono en pasos de 0,5 m y la generación a un metro del panel si no encuentra intersección muestreada. No afirma una intersección analítica exacta ni que ese procedimiento esté físicamente aprobado.

Sus campos `source_definition` y `normalization` son una propuesta de documentación compatible con nuestra comparación técnica de metadatos. **No se añaden retrospectivamente a las corridas existentes como si hubieran sido parte de su ejecución**, ni se cambia la definición del objetivo para declarar terminado el trabajo.

## Qué falta y quién puede resolverlo

| Pendiente | Siguiente acción concreta | Dependencia |
|---|---|---|
| Significado físico de la imagen | Acordar estimador direccional o cuentas del panel; revisar la ficha y el alcance del informe. | Decisión científica de dirección y estudiantes. |
| Equivalencia espacial, si se afirma detector físico | Justificación cuantitativa o comparación con fuente espacial adecuada y pesos. La comparación 100/600 no la sustituye. | Modelo de referencia y posiblemente control dirigido en SC3. |
| Fuente y exposición | Explicar superficie, espectro, extrapolación, energía total/cinética y área; decidir qué significan los días convencionales. | Justificación científica, no una corrección automática de código. |
| Bordes con el observable final | Referencia y criterio simultáneo de equivalencia con incertidumbre; dimensionar N a partir de esa comparación. | Diseño acordado y evidencia adicional si la actual no basta. |
| Operación en SC3 | Adoptar herramientas corregidas y comprobar publicación/cola/fallos con el entorno real. | Acceso de los estudiantes a SC3. |
| Conjunto final | Ejecutar alcance y presupuesto aprobados; verificar 114 referencias y 9.120 pares si se mantiene ese catálogo. | Resolución de las decisiones anteriores. |

La guía para los criterios físicos está en [diagnóstico del observable y decisión](DIAGNOSTICO_OBSERVABLE_Y_DECISION.md). Por ahora no falta otra repetición genérica de los controles existentes: falta responder esas preguntas y adoptar las herramientas disponibles.

## Comandos de revisión local

Desde la raíz de nuestra réplica, con carpetas reales de tablas v1 y de la entrega:

```console
python herramientas/auditar_fuente_angular.py TABLAS_V1 --salida PROBABILIDADES_NUEVAS.json
python herramientas/preparar_campana_angular.py ENTREGA/produccion/manifiesto-receta-k10.csv --informe PREFLIGHT_NUEVO.json
python herramientas/preparar_campana_angular.py ENTREGA/datos/sc3/prueba-integracion/manifiesto-prueba.csv --geometrias geo-train-06 --bloques ENTREGA/datos/sc3/prueba-integracion/oe1-v1-prueba --aceptar-crlf --informe INTEGRACION_NUEVA.json
python -m unittest discover -s herramientas -p "test_*angular*.py" -v
```

La integración retorna código 1 por alcance multivista incompleto, aunque ambos bloques sean válidos; el informe distingue las dos cosas. Los informes deben ser nuevos. El análisis de fuente no genera tablas nuevas ni modifica la normalización. Las pruebas se ejecutaron en Python 3.12.14 y NumPy 2.4.4, sin ejecutar Geant4 o SLURM.

# Preparación de producción del OE1

**Nuevo control local:** [muestreo angular](CONTROL_MUESTREO_ANGULAR.md). Se cuantifica una diferencia en las columnas de borde entre el muestreo de la fuente y la distribución nominal. Resolver la convención angular antes de fijar qué referencias reutilizar.

Revisión: 2026-10-01, Colombia. **Estado: parcial; plan condicionado, no orden de ejecución.** Continúa la [auditoría completa de etapa 2](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md). El resultado inconcluso de A/B no exige ampliar automáticamente el ensayo ni impide elegir una geometría B correctamente construida. Tampoco certifica la normalización física de la campaña.

## Lo que adelantamos localmente

Se verificaron identidad y SHA-256 de las 114 referencias NPZ contra sus metadatos. El [inventario por vista](evidencias/preparacion-produccion/alcance-produccion.csv) conserva huellas de geometría, metadatos y referencia histórica; no sustituye los originales. El [resumen reproducible](evidencias/preparacion-produccion/preparacion-produccion.json) contiene resultados y huellas de tablas.

| Alcance provisional | Referencias | Pares derivados |
|---|---:|---:|
| Seis geometrías afectadas: candidatas a regenerar con B | 36 | 2.880 |
| Otras trece geometrías: reutilización condicionada | 78 | 6.240 |
| Conjunto completo | 114 | 9.120 |

Las seis son `geo-gen-01`, `geo-test-01`, `geo-test-03`, `geo-train-06`, `geo-train-08`, `geo-train-11`. Cada geometría tiene seis vistas. Cada referencia genera 80 pares por reducción binomial: cuatro fracciones y veinte realizaciones. Esos pares no requieren 80 transportes nuevos.

Las 36 referencias históricas suman **1.302.336.227 primarios**. Es una escala de trabajo, no un presupuesto aprobado ni una predicción de tiempo. El N de producción se fijará junto con la definición de exposición y precisión requerida. No extrapolar directamente el tiempo del ensayo instrumentado al ejecutable de producción.

**Condición del alcance:** las 78 referencias solo se reutilizan si se demuestra compatibilidad de fuente, espectro, normalización, detector, física, entorno y construcción geométrica. La reproducción de una vista de control no demuestra compatibilidad de todas. Si cambia la definición del observable o la aceptación, revisar las 114 vistas; no mezclar referencias con normalizaciones distintas bajo una misma versión de datos.

## Qué encontramos al revisar la normalización

Fuentes: código de estudiantes `d8ca749`, archivos `scripts/simulation/geant4_app/{muography_sim.cc,src/PrimaryGeneratorAction.cc,src/FluxTables.cc,src/DetectorConstruction.cc,src/SteppingAction.cc}`; generador histórico [build_generator_tables.py](originales/scripts/analysis/build_generator_tables.py), [imaging.py](originales/scripts/simulation/surrogate/imaging.py) y [bitácora histórica](originales/bitacora-simulacion.md). La auditoría de etapa 2 registra la procedencia de los ejecutables.

1. **Verificado en código:** los pesos de dirección proceden del surrogate, con la convención `Phi_int × A × dOmega × T`. El espectro de momento procede de tablas condicionales de EcoMug. La comparación entre motores comparte esa convención y por sí sola no la valida independientemente.
2. **Verificado numéricamente:** la suma de la tabla es 36.175.379,99; el metadato anterior al redondeo declara 36.175.379,91628132. La diferencia relativa es 2,04 × 10⁻⁹, compatible con la serialización de pesos. Las tres huellas coinciden con las tablas de etapa 2. Esto comprueba consistencia interna, no que representen 30 días de un detector real.
3. **Verificado en código:** `--days D` obtiene N mediante Poisson con media `TotalCounts30d × D/30`; el modo de lista usa su número de filas. Los 24 millones de pares del ensayo son un tamaño experimental fijo, no una nueva medición de 30 días.
4. **Verificado en código:** se elige un punto de impacto nominal uniforme en un panel de 1,2 × 1,2 m y se retrocede para inyectar el primario. Después se registra su entrada en un plano de 600 × 600 m y se clasifica por dirección de llegada. No se exige que termine en el panel pequeño.
5. **Reportado por autores:** el plano grande se justifica mediante compensación de muones dispersados hacia fuera y hacia dentro; se reporta convergencia al aumentar el plano. **Pendiente de justificación:** bajo qué condiciones esa compensación representa el observable deseado en escenarios volcánicos heterogéneos. La estabilización del conteo con el tamaño del plano no demuestra por sí sola equivalencia con la aceptación de un detector pequeño.

No se propone multiplicar o dividir los conteos por la razón entre las áreas de ambos planos: eso no se deduce del muestreo utilizado. Tampoco se modifica automáticamente el factor angular. Primero se debe definir si el producto es un estimador direccional idealizado o la cuenta esperada de un detector físico, y justificar su aceptación, unidades y exposición para ese producto.

## Siguiente entrega concreta de los estudiantes

Primero, una entrega de documentación y código; no otra campaña masiva:

1. **Definir el dato final:** explicar qué representa un píxel, qué superficie y direcciones acepta, qué se cuenta como detección, y qué significa «30 días». Derivar la normalización desde el flujo con unidades y aclarar si el área es efectiva o geométrica, incluida la convención angular. Referenciar el origen y disponibilidad de las tablas y sus insumos.
2. **Justificar el plano de conteo:** aportar los resultados existentes que respaldan el plano grande y explicar el supuesto de compensación. Si no bastan para el observable elegido, proponer un único control dirigido con criterio de decisión fijado antes de ejecutarlo. No repetir A/B para intentar obtener equivalencia.
3. **Congelar una receta de producción B:** commit, compilador y opciones, Geant4 11.4.2, paquetes de datos físicos y variables de entorno, lista de física, semillas, tablas, geometrías, ejecutable con huella, comandos, partición en bloques y fusión. No tratar el Dockerfile 11.3.2 como entorno equivalente demostrado. Aclarar qué instrumentación se conserva o desactiva.
4. **Responder las precisiones E2-01/E2-02/E2-04** del informe completo: corregir el lenguaje sobre igualdad, energía final y cambios fuera del cruce registrado; investigar primero con código y evidencia existente. Estas precisiones no alteran el intervalo ya auditado.

Con esa entrega revisada se fija el alcance final, se completa un manifiesto ejecutable con N y semillas por bloque, se estima CPU/almacenamiento y se organiza la campaña. Evitar registros por muon indiscriminados para miles de millones de primarios: definir qué evidencia conserva producción y cómo se audita. Registrar histogramas, metadatos, logs, estados, comandos, huellas y ubicación persistente; comprobar las copias antes de liberar temporales.

## Cierre previsto

Una vez resueltas las decisiones anteriores: ejecutar el manifiesto B acordado; verificar geometría y terminación; auditar conteos y fusión; regenerar los pares de las referencias sustituidas; comprobar semillas, particiones, tipos y sumas; publicar una ficha de datos versionada con trazabilidad histórica → referencia B → pares. Documentar la limitación de que los pares reducidos comparten su referencia y no son simulaciones independientes.

P-01 se cierra con decisión y ejecución documentada de sustitución; P-02 con receta reproducible comprobada; P-03 con una alternativa nueva de ejecución y empaquetado reproducibles o los originales necesarios; P-04 con el observable y sus controles físicos justificados. Ninguno se cierra solo con este inventario. La meta es completar el conjunto de datos del OE1, sin introducir entrenamiento de redes.

## Reproducir nuestra preparación

Desde la raíz de la réplica, con Python y los NPZ restaurados:

```console
python herramientas/preparar_alcance_produccion.py --salida objetivo-1/evidencias/preparacion-produccion
```

Usa biblioteca estándar, verifica 114 huellas y comprueba suma y positividad de los 256 pesos; falla ante una identidad o huella discrepante. La lista de seis geometrías procede del diagnóstico previo. No ejecuta Geant4, no prueba aceptación física y no cambia los originales.

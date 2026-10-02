# Entrega de las siete actividades de preparación del OE1

2026-10-02. Trabajo local realizado con autorización de la dirección, sobre la entrega estudiantil `01a9871`. **Se completó la preparación documental, analítica y de software de las siete actividades.** No se ejecutaron nuevos transportes ni se declara aprobada la campaña; las decisiones académicas y comprobaciones SC3 están identificadas en la guía.

| Actividad | Entrega terminada | Límite que permanece explícito |
|---|---|---|
| 1. Definición del conjunto | [Producto principal, campos y afirmaciones permitidas](DEFINICION_PRODUCTO_OE1.md), con [ficha operativa](contratos/receta-operativa-siete-actividades.json). | Recomendación concreta para adopción académica, no equivalencia con detector ni cierre automático de OE1. |
| 2. Referencia de cielo | Cálculo tabulado para las 256 filas y análisis de sensibilidad de los 7.122 píxeles afectados. | Referencia ideal sin transporte; no calibración física de cielo. |
| 3. Diseño estadístico C3 | Evaluador binomial simultáneo, presupuesto de cuentas en ambos brazos, comprobación de potencia con datos sintéticos y escenarios de coste. | Condicional a exigir equivalencia instrumental y definir la fuente amplia; no se autoriza esa corrida. |
| 4. Necesidad de C3 | Decisión recomendada: no imponer equivalencia instrumental al producto idealizado; detallar qué afirmación la exigiría. | La elección debe constar expresamente en el informe académico. |
| 5. Bordes | Evaluador implementado, aplicado a c01/c02 y extendido al piloto de seis vistas con máscaras y semillas congeladas. | Datos actuales inconclusos; criterio nuevo documentado como retrospectivo, sin aprobación oportunista. |
| 6. Automatización | Worker, wrapper SLURM y lanzador de una pasada; publicación verificada, bloqueo e intenciones persistentes. Normalización convencional validada y agregada. | Pruebas locales con cola/simulador sintéticos; faltan comprobaciones del entorno real SC3. |
| 7. Instrucciones | [Guía única para estudiantes](GUIA_SIGUIENTE_ETAPA_OE1.md): tareas inmediatas sin muones, decisión, piloto condicional, entregables y reglas de continuación. | El piloto y P1 no arrancan automáticamente. |

## Resultados que cambian la decisión

- Es posible eliminar la extrapolación del cielo como **referencia ideal de cálculo**, pero no afirmar que se haya medido el cielo físico oculto por la roca.
- En c02 las 15 regiones de borde quedan inconclusas con el nuevo análisis simultáneo. En c01, tres quedan dentro y doce inconclusas. No corresponde afirmar que ya se cumpla el criterio.
- C3 con 1.600 cuentas no estaba dimensionada para su criterio. El método conservador preparado exige muchas más cuentas y tiene un coste elevado; esto refuerza la necesidad de decidir primero qué afirmación se pretende validar.
- Hay un piloto alternativo documentado: 211 millones por vista, seis vistas de geo-train-06, unos 187,3 h-núcleo bajo la tasa de c01. Es un escenario revisable **antes** de ejecutar, no un presupuesto mínimo ni aprobado.

## Verificación realizada

**103 pruebas locales satisfactorias**, incluyendo 25 nuevas. Cubren límites estadísticos frente a inversión independiente, cobertura binomial, casos de inconclusión/diferencia, referencia sintética conocida, bordes, evaluación del piloto, ejecución/publicación fallida, bloqueo, duplicación y respuestas ambiguas de la cola. [Registro](evidencias/pruebas-siete-actividades.txt).

La fusión actual reproduce las huellas originales de los dos bloques reales: 200.000 primarios, 69.995 registros seleccionados y 130.190 sin corte. Los campos nuevos de normalización se agregan y validan en pruebas separadas; no se añadieron a las corridas viejas. La estructura del manifiesto piloto también fue comprobada offline. Se verificaron las huellas de herramientas/manifiesto contra los objetos Git preparados, la sintaxis Bash y los enlaces de los documentos: [registro de validación](evidencias/validacion-siete-actividades.json).

[Análisis de cielo/bordes/C3](DISENO_ESTADISTICO_Y_REFERENCIAS.md), [resultados](evidencias/preparacion-siete-actividades/resumen.json), [diseño piloto](evidencias/piloto-propuesto-siete-actividades/diseno-piloto.json). Los 20.000 experimentos estadísticos de planificación son binomiales sintéticos, no transportes Geant4.

La siguiente tarea de estudiantes es **comprobar la integración operativa y responder a la definición propuesta**, sin repetir el ensayo de dos bloques y sin lanzar C3 por rutina. Después se acuerda el piloto y se usan sus resultados para dimensionar la campaña final.

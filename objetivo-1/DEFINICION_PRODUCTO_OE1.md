# Definición propuesta del producto del OE1

2026-10-02. Versión de trabajo preparada por la dirección a partir de `01a9871`. Esta definición hace concreta la opción recomendada; **no declara aprobado el modelo físico ni terminado el OE1**. La elección académica queda visible para que dirección y estudiantes la incorporen expresamente al informe. No cambia los archivos históricos ni sus etiquetas.

## Producto principal recomendado

Un conjunto de **imágenes de conteos direccionales sintéticos de muones transmitidos por escenarios volcánicos idealizados**, acompañado de realizaciones de menor conteo del mismo observable. La unidad es una matriz de 256 × 256 enteros: cada entrada cuenta primarios que alcanzan el plano de registro con energía cinética mayor que 3 GeV y dirección final dentro de ese píxel.

La receta candidata conserva: geometrías corregidas, Geant4 11.4.2/FTFP_BERT y solo primarios, impactos nominales sobre un panel de 1,2 m, inyección junto al cono, margen angular de 5°, plano de registro de 600 m y malla `az-edges-v1`. El plano es una superficie de registro computacional; **no se presenta como un detector físico de 1,2 m**. La fuente usa pesos de dirección derivados de Guan y cuantiles de momento de EcoMug, incluida su extensión fuera de la ventana; ese modelo híbrido se declara como hipótesis del conjunto, no como flujo físico calibrado.

Se recomienda conservar el catálogo de 19 escenarios × 6 vistas = 114 referencias y cuatro fracciones × 20 realizaciones por referencia = 9.120 pares. El conjunto corregido debe producirse con una sola definición compatible. El catálogo histórico no se convierte en el nuevo por renombrarlo.

## Qué representa cada campo

| Campo | Significado y uso |
|---|---|
| `counts_ref` | Conteos seleccionados de la referencia; uint32, sin recorte de saturación. |
| `events_transported` | Número fijo de primarios transportados, incluidos los de fuera de la ventana nominal. |
| `nominal_in_window` | Suma del histograma de direcciones iniciales dentro de la ventana; distinto del conteo detectado. |
| `conventional_exposure_days` | 30 × `nominal_in_window` / 36.034.069,911914065. Etiqueta convencional basada en el S0 heredado; no días de un detector real. |
| `exposure_days` | Permanece en −1: el simulador se ejecuta con N fijo. No sustituirlo por la etiqueta convencional. |
| Respuesta normalizada ideal | C_ij / [N_generados × p_ideal,ij], con referencia tabulada sin transporte y el mismo margen/corte. Diagnóstico adimensional; no llamarlo automáticamente transmisión física. |
| Conteos reducidos | Adelgazamiento binomial por píxel con fracciones 0,5; 0,1; 0,05; 0,01 y semillas registradas. Son realizaciones condicionadas a la misma referencia finita. |

Una fracción f reduce en promedio las cuentas y su escala convencional por f. No equivale a demostrar una corrida independiente de exactamente f·N primarios; tampoco convierte la referencia en una verdad sin ruido. Separar geometrías entre entrenamiento/validación/prueba antes de formar pares para evitar que variantes de la misma referencia crucen particiones.

`nominal_in_window` se conoce exactamente para la realización registrada, pero fluctúa entre ejecuciones con N fijo. El generador y la interpretación física añaden incertidumbre de modelo; no se afirma que la exposición esté libre de incertidumbre porque el contador se conozca.

## Referencia de cielo disponible sin más transporte

[referencia_cielo_angular.py](../herramientas/referencia_cielo_angular.py) integra los cuantiles de momento y la distribución angular implementada sobre cada fila, incluyendo el jitter, las bandas espectrales, el margen y los bordes nominales. Calcula dos probabilidades por primario generado: pertenecer al píxel y pertenecer a él con energía cinética inicial >3 GeV. No usa los conteos de roca para fijar su denominador.

Esta referencia está definida en las 256 filas y elimina la necesidad de prolongar una eficiencia observada desde 6,94° hacia abajo. **No incluye pérdidas en aire, decaimiento, dispersión ni migración angular.** Permite una normalización ideal reproducible del conjunto y un diagnóstico del código; no sustituye una referencia física sin volcán si se pretende afirmar transmisión calibrada. No se recorta la respuesta normalizada a [0,1]: la migración o el ruido pueden producir valores superiores a uno.

Los datos existentes no permiten medir una referencia de cielo a las elevaciones ocultas por la roca. Para exigir interpretación física adicional habría que justificar analíticamente el transporte de aire o contrastar una referencia sin roca con fuente/superficie explícitas. La identidad que reconstruye C a partir de una eficiencia calculada del propio C no es esa validación independiente.

## Qué exige C3 y qué no

**Para el producto idealizado recomendado, C3 no es una condición automática de equivalencia instrumental, porque esa equivalencia queda fuera de sus afirmaciones.** Siguen siendo necesarias la trazabilidad de fuente, las comprobaciones geométricas y de transporte, la evaluación de bordes con corte y la suficiencia de conteos en roca. Excluir una afirmación instrumental no exime de justificar por qué los escenarios y el transporte son representativos del OE1.

Si el informe pretende afirmar «estas imágenes son lo que mediría el detector de 1,2 m», entonces sí necesita demostrar la contribución de muones generados fuera del panel, fijar aceptación y resolución del instrumento y una referencia física compatible. C3 es una vía posible; [su diseño corregido](DISENO_ESTADISTICO_Y_REFERENCIAS.md) es condicional y no se ordena ejecutarlo por defecto.

La decisión recomendada es adoptar el producto principal idealizado y dejar la equivalencia instrumental como extensión. Debe quedar expresada en el informe académico, con las limitaciones anteriores; no se interpreta el silencio como aceptación ni se inicia P1 por esta propuesta.

## Contrato listo para el flujo nuevo

La [ficha operativa propuesta](contratos/receta-operativa-siete-actividades.json) registra fuente, normalización, geometrías y hashes de herramientas. El ejecutor añade esos campos solamente a nuevas ejecuciones, junto con el contador nominal. La fusión valida y suma ambos contadores y la exposición convencional; no altera retrospectivamente los bloques recibidos. El empaquetador distingue las definiciones presentes de las ausentes.

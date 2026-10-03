# Protocolo OE2-P04: piloto de entrenamiento al 5 %

**Versión 1, 2026-10-03. Estado: preparado para ejecución en GPU; resultados SC3 pendientes.** La dirección autorizó el diseño del piloto. No se lanza en esta etapa la campaña propuesta de 24 entrenamientos. El OE1 permanece cerrado.

## Pregunta y resultado esperado

Se busca establecer si la implementación corregida puede entrenarse de forma estable con los datos del OE1 y si la componente adversaria aporta una mejora respecto de la misma U-Net entrenada únicamente con L1. También se compara con la entrada sin red, corregida por la fracción de conteo y normalizada con el mismo contrato.

El piloto debe entregar curvas, ejemplos, checkpoints, tiempos y uso de memoria. No constituye una demostración definitiva de generalización ni de fidelidad física. La elección de 5 % es un punto inicial común a ambos métodos; no se selecciona por resultados de los conjuntos reservados.

## Datos y comparaciones fijadas

Se utiliza el [contrato de datos v1](evidencias/contrato-datos-v1.json) y la [normalización corregida](CORRECCIONES_V1.md). Su SHA-256 se comprueba automáticamente. Para la fracción 0,05 hay **1.440 pares train y 360 pares val**, distribuidos entre 12 y 3 geometrías respectivamente. Todas las realizaciones de una geometría permanecen en su partición. No se abren imágenes de test/generalization ni se usan para seleccionar hiperparámetros.

| Elemento | U-Net L1 | cWGAN-GP |
|---|---|---|
| Generador | `unet_dc_5` | El mismo |
| Crítico | Ninguno | `patch_critic_70` |
| Pérdida del generador | 100 × L1 | 100 × L1 + adversaria |
| Penalización GP | No aplica | 10 × GP del promedio por muestra |
| Actualizaciones | Una del generador por lote | Cinco del crítico y una del generador por lote |
| Optimizador | Adam, lr=0,0001; betas=(0; 0,9) | Los mismos valores para G y D |
| Lote | 4 | 4 |
| Semilla | 2026100301 | La misma |
| Transformación | `train_log_bounded_v1` | La misma |
| Aumentos / nuevos adelgazamientos | Desactivados | Desactivados |

Se inicializa desde cero: no se transfieren pesos históricos ni los de la prueba técnica. El presupuesto se iguala en épocas y exposición del generador a los datos, no en tiempo de cómputo; el crítico agrega trabajo. La semilla fija controla una comparación inicial, pero una sola repetición no mide variabilidad entre entrenamientos.

## Etapa A: comprobación técnica

Se ejecutan las configuraciones `tecnica-unet` y `tecnica-cgan`: 8 pares train, 8 val, lote 4 y dos épocas. Los primeros pares se toman de las particiones respectivas; esta selección pequeña no es representativa del catálogo. Se interrumpe deliberadamente al terminar la primera época y se reanuda la segunda con la misma configuración.

El ejecutor se niega a continuar si no hay CUDA, salvo que se solicite explícitamente una prueba local CPU. Se fija `CUBLAS_WORKSPACE_CONFIG` antes de inicializar CUDA y se conservan las operaciones deterministas del motor. Un error de operación determinista no se resuelve desactivando esa protección sin documentar una nueva versión.

**Se permite avanzar a B cuando ambos métodos:** completan las dos épocas en GPU, guardan `last.pt` y `best.pt`, reanudan sin duplicar épocas, producen pérdidas/gradientes/métricas finitas y superan el resumen automático. El registro debe identificar GPU, versiones, identidad de código y contrato de datos. No se exige mejorar SSIM en esta prueba técnica.

Si aparece un error de memoria, huellas, reanudación o valores no finitos, se detiene esa ejecución y se conserva el error. No se reduce el lote solo para uno de los métodos ni se cambian semillas, GP o normalización para lograr una aprobación. Un lote alternativo requiere configuraciones nuevas para ambos métodos, nueva identificación y repetición de A. No se reanuda el experimento anterior con parámetros distintos.

## Etapa B: piloto con todos los pares al 5 %

Tras aceptar A, se ejecutan `piloto-unet` y `piloto-cgan` en directorios nuevos y desde cero. Se permite completar ambos métodos sin solicitar una nueva decisión intermedia, siempre que A sea satisfactoria y haya asignación de cómputo disponible.

- Máximo de 30 épocas; 360 lotes por época y método.
- Validación completa de los 360 pares al terminar cada época.
- Parada tras ocho validaciones consecutivas sin mejorar al menos 0,001 respecto de la referencia de paciencia. Este umbral se usa para detener, no para seleccionar `best.pt`.
- `best.pt` conserva el máximo SSIM de validación sin redondear; `last.pt` sirve para reanudar. Las métricas impresas se redondean y pueden mostrar empates que no existen internamente.
- Figuras de entrada, predicción y referencia cada cinco épocas. Si la parada ocurre antes, se informa la ausencia de figuras periódicas y se revisa el checkpoint; no se prolonga solo para producir una figura.

Los 30 ciclos son un límite exploratorio y no una afirmación de convergencia. Si la curva sigue mejorando al alcanzar el límite, se registra como resultado del piloto; no se extiende silenciosamente esa ejecución. No se activan aún las demás fracciones ni la campaña completa.

## Lectura de los resultados y decisiones

El resumen compara el mejor SSIM de cada método con la entrada sin red sobre los mismos pares val. Registra PSNR en las curvas, tiempos y memoria. Son métricas de la representación normalizada v1: no deben compararse directamente con las tablas históricas.

**Aceptación técnica no equivale a calidad.** Un piloto que termina con métricas finitas puede mostrar que la red empeora la entrada. Si ocurre, se entrega igualmente y se revisan pérdidas, curvas y ejemplos antes de ampliar. No se descarta ni se oculta la repetición.

La revisión posterior debe examinar continuidad de estructuras, contraste, bordes y posibles patrones artificiales en las figuras. Esta inspección es cualitativa; por sí sola no certifica fidelidad física. Las métricas regionales en coordenadas originales y la inversión a conteos deberán fijarse en el protocolo de evaluación posterior, sin seleccionar regiones a partir de resultados de test.

Se distinguen tres decisiones al recibir los resultados:

1. **Fallo técnico:** corregir y repetir con versión identificada.
2. **Funcionamiento correcto, calidad inconclusa o deteriorada:** revisar el diseño con train/val y plantear el siguiente experimento; no ampliar automáticamente.
3. **Funcionamiento correcto y mejora prometedora sin artefactos evidentes:** estimar presupuesto y fijar la campaña principal. Esto todavía no demuestra ventaja estadística de la cGAN.

## Presupuesto y campaña posterior

Por método, 30 épocas representan como máximo 10.800 actualizaciones del generador. La cGAN agrega hasta 54.000 actualizaciones del crítico. Estos valores no son transportes de muones ni nuevas simulaciones Geant4.

El ejecutor registra memoria CUDA máxima asignada y reservada y tiempo por sesión. Las curvas registran tiempo por época, que no incluye toda la escritura posterior de checkpoints. Por ello se debe reportar también duración total del trabajo en el planificador de SC3. Para estimar, usar el promedio de épocas después de la primera y contrastarlo con tiempo total dividido por épocas completadas.

La campaña propuesta de dos métodos × cuatro fracciones × tres semillas suma 24 entrenamientos **adicionales**, si el protocolo final se confirma. Un cálculo inicial del costo es

\[
T_{\mathrm{campaña}}\approx 12E_U t_U+12E_C t_C,
\]

donde E es el máximo de épocas por método y t el tiempo por época medido incluyendo gastos de guardado mediante el tiempo total. Es una estimación, no una reserva garantizada: las fracciones, la parada temprana y la concurrencia pueden cambiar el costo. El piloto no se cuenta retrospectivamente como una de las tres repeticiones confirmatorias después de usarlo para ajustar el diseño.

## Ejecución y entrega

Los comandos exactos y la lista de entrega figuran en [instrucciones para SC3](INSTRUCCIONES_PILOTO_SC3.md). Se conservan configuraciones JSON en [configuraciones/piloto-v1](configuraciones/piloto-v1/tecnica-cgan.json). La [verificación local](evidencias/protocolo-piloto-local.json) prueba la interfaz y los dos métodos en CPU; no acredita el entorno GPU.

El cierre de OE2-P04 requiere recibir y revisar la ejecución GPU, fijar el protocolo principal y obtener evidencia de entrenamiento y desempeño. Publicar este diseño no cierra el OE2.

## Comprobación local de preparación

Se ejecutaron los cuatro comandos de la etapa A con la opción explícita CPU: ambos métodos completaron dos épocas, con dos lotes por época, y recuperaron su checkpoint tras la interrupción. Las veinte comprobaciones no relacionadas con GPU del resumen fueron satisfactorias. Los indicadores GPU permanecen falsos, como corresponde. Se verificó además que el mismo informe CPU sea rechazado si se solicita aceptación GPU; las [huellas y controles del protocolo](evidencias/verificacion-protocolo-v1.json) fijan las cuatro configuraciones y los dos ejecutores.

Después de solo cuatro actualizaciones del generador, ambos modelos dieron menor SSIM que la entrada: 0,5480 para U-Net y 0,4412 para cGAN, frente a 0,7264 sin red en los ocho pares de validación técnica. Se conserva este resultado sin interpretarlo como comparación de modelos entrenados. La calidad no se considera aprobada; esta prueba verifica ejecución y recuperación, no convergencia.

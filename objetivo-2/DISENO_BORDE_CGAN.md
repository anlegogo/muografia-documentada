# Ensayo E1: integración del término espacial de borde

Fecha: 2026-10-04, America/Bogota. **Estado: verificado en CPU; pendiente de comprobación GPU.** Diseño fijado antes de recibir resultados nuevos de GPU. No se declara aceptación física ni cierre del OE2.

## Pregunta y variantes

El [diagnóstico espacial](DIAGNOSTICO_ESPACIAL_CGAN.md) encontró que conservar el total del borde puede coexistir con errores en sus píxeles. Se pregunta si una penalización espacial reduce ese error sin perder conservación regional, contraste y calidad de imagen.

En este ensayo C0 es el control regional y C1 añade borde. **Ambas variantes conservan el término regional de peso uno**: C0 no tiene el significado del C0 histórico. El experimento, las configuraciones, semillas, fuentes y esquema de aceptación son distintos.

\[
L_G^{C0}=L_{\mathrm{adv}}+100L_1+L_{\mathrm{reg}},\qquad
L_G^{C1}=L_G^{C0}+0{,}629L_{\mathrm{borde}},
\]
\[
L_{\mathrm{borde}}=\frac1B\sum_b
\frac{\sum_{p\in R_b}|\widehat c_{bp}-c_{bp}|}{\sum_{p\in R_b}c_{bp}},
\qquad
\widehat c=\exp(sz/(1-z))-1.
\]

Se conserva la escala train \(s=8{,}239329427901795\). Las máscaras solo intervienen en entrenamiento, sin entradas nuevas al generador. Se rechazan soporte menor de veinte píxeles, referencia vacía y valores no finitos, sin pseudocuentas ni recortes.

## Coeficiente fijado con train

Se registró el [diseño del perfil](configuraciones/borde-cgan-v1/perfil.spec.json) antes de ejecutarlo: doce lotes de cuatro imágenes, uno por geometría train, vistas 0, 1, 3 y 5, realización 0. Se conservaron los pesos originales, modo evaluación con autograd y cero pasos de optimizador.

Para \(r_j=\|\nabla_\theta L_{\mathrm{borde},j}\|_2/\|\nabla_\theta L_G^{C0,j}\|_2\), la regla fijada fue
\[
\lambda=\frac{\lfloor1000\min(1,\;0{,}10/\operatorname{mediana}(r),\;0{,}25/\max(r))\rfloor}{1000}.
\]

La mediana fue 0,158781944 y el máximo 0,241277801: **lambda = 0,629**. El cociente ponderado mediano queda en 0,09987 y el máximo en 0,15176. Los presupuestos 10 % y 25 % son decisiones conservadoras de escala del gradiente, no tolerancias físicas ni garantías durante la optimización. No se buscó el coeficiente que favoreciera val.

Los gradientes son finitos y las huellas G/D permanecieron idénticas. Se conserva la oposición local observada en la geometría 04. El resultado solo describe esos lotes y el checkpoint inicial. [Evidencia](evidencias/perfil-gradientes-borde.json) y [script ejecutado](herramientas/perfilar_gradientes_borde_cgan.py).

## Diseño ejecutable

| Elemento | Decisión |
|---|---|
| Parejas y semillas | B1: 2026100411; B2: 2026100412; B3: 2026100413 |
| Inicialización | Mismos G/D originales de época 5, SHA-256 e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0 |
| Variantes | C0: regional 1, borde 0; C1: regional 1, borde 0,629 |
| Datos | Fracción 0,05; 1.440 train y 360 val; reservas sin abrir |
| Optimización | Adam nuevo, lr 1e-5, betas (0; 0,9), lote 4; cinco D por G, GP 10 |
| Selección | Quinta época adicional, sin parada temprana ni selección por mejor SSIM |
| Prueba técnica | Ocho train/ocho val, dos épocas, continua y recuperada por variante/pareja |
| Presupuesto técnico | Doce ejecuciones completas equivalentes; 48 actualizaciones G y 240 D |
| Piloto | Seis continuaciones de cinco épocas; 10.800 G y 54.000 D |

Las seis configuraciones de [borde-cgan-v1](configuraciones/borde-cgan-v1/B1-C0.json) están fijadas por huella. Son continuaciones condicionadas al mismo checkpoint, no réplicas independientes desde cero. No eliminan la exposición anterior a val.

Puede utilizarse una GPU por pareja, conservándola para ambas variantes. Con tres GPU deben coincidir modelo y entorno. Las tres evaluaciones se realizan en un único dispositivo para conservar la misma referencia inicial.

## Decisión prospectiva

Se conservan los ocho controles anteriores: Q menor, ningún Q por geometría peor, cielo no peor, borde no peor, 23 contrastes comunes, contraste no peor, SSIM no peor y PSNR no peor. **Se añade reducción estricta del error espacial de borde**, la pregunta específica de E1. No basta que el borde permanezca igual.

La concordancia descriptiva exige los nueve controles en las tres parejas, con cifras sin redondear. Se conservan las 18 vistas, las 24 combinaciones de anomalía, soportes y casos no estimables. Un resultado desfavorable no autoriza cambiar coeficiente, semillas o duración ni descartar escenarios.

Incluso con concordancia, physical_acceptance permanece falso. No se obtienen automáticamente tolerancias físicas absolutas ni una evaluación final independiente. Los resultados y controles de R1–R3 no se modifican.

## Integración y comprobaciones

Se separaron ejecutor, auditor, evaluador y síntesis para E1. El componente aislado conserva su archivo y huella originales; su encabezado describe el estado previo, mientras esta integración lo incorpora explícitamente al nuevo ejecutor. Peso de borde cero conserva exactamente el valor y el gradiente de la pérdida regional anterior. También se comprobó un paso completo con redes pequeñas: mismos G/D, ambos Adam y RNG. La red completa se verifica con las doce ejecuciones técnicas.

Se registran edge y weighted_edge por época. La recuperación rechaza cambios de rama, pareja, coeficiente, fuentes, datos o entorno. Las aceptaciones históricas y CPU no habilitan el piloto GPU. Se conserva la política corregida de gradientes del crítico.

Se superaron **35 controles**: 18 de contratos, gradientes y síntesis; siete de orquestación; diez sobre artefactos reales. Las **doce ejecuciones de las redes completas en CPU** finalizaron con recuperación exacta en B1, B2 y B3, sumando 48 actualizaciones G y 240 D. Se verificaron G, D, ambos optimizadores, RNG, historial numérico y predicciones.

Las tres evaluaciones técnicas y la síntesis se ejecutaron correctamente, sin conclusión de calidad. Se verificó la regeneración de exportaciones sin reentrenar y el rechazo de parejas mezcladas, optimizador/crítico alterados, reanudación incompatible, piloto CPU y aceptación histórica. El inventario técnico contiene 150 archivos y 43 archivos destinados a Drive, 3.389.371.861 bytes en total. Estos son los artefactos locales de dos épocas; la entrega GPU de técnica más piloto tendrá los 55 archivos de Drive descritos en la guía.

El soporte se comprobó en las 90 vistas train/val: mínimo 2.228 píxeles y 768.684 cuentas de referencia en borde. Este control verifica denominadores, no fija el coeficiente ni evalúa calidad.

[Evidencia de integración](evidencias/integracion-borde-cgan.json), [inventario CPU](evidencias/inventario-borde-cpu.json) y [soporte de borde](evidencias/soporte-borde.json). **No se ejecutaron aquí CUDA ni continuaciones de cinco épocas.**

## Estado y siguiente paso

E1-01 y E1-02 están verificados en el alcance del diagnóstico anterior. E1-03 queda verificado como diseño de ingeniería: perfil de 48 muestras train, regla previa y seis configuraciones. E1-04 queda verificado en CPU; pendiente de comprobación GPU. **E1-05 continúa pendiente: nueva aceptación GPU y después las seis continuaciones.**

La [guía de ejecución](INSTRUCCIONES_BORDE_CGAN.md) permite que los estudiantes completen ese bloque con autonomía. No amplía a otras fracciones ni autoriza épocas adicionales. La aceptación física y el cierre del OE2 siguen pendientes.

## Reproducción e incidencias

El perfil recibe --datos, --mascaras, --pesos y --salida. La salida debe ser nueva. El encabezado heredado del script menciona cuatro muestras, pero el bucle, diseño y evidencia fijan doce lotes de cuatro; se conserva el archivo exacto ejecutado y su huella.

La guía documenta los controles y la reproducción CPU. Entorno: Python 3.12.14, PyTorch 2.6.0+cpu, NumPy 2.3.5, dos hilos y determinismo. Se corrigieron la lectura UTF-8 del generador local de archivos y la creación explícita de la carpeta del orquestador detectada por el control con procesos simulados. Se conservan esas incidencias y las comprobaciones finales. No se reparó el índice Git antiguo ni se contrató GPU.


# Diagnóstico espacial y preparación del ajuste E1

Fecha de revisión: 2026-10-04, America/Bogota. Base: 866e286, posterior a la entrega f6518ff. **Estado: diagnóstico y componente experimental verificados localmente; integración y ensayo pendientes. No preparado para GPU.**

## Pregunta y alcance

La repetición R1–R3 mostró deterioro del error de borde en las tres parejas, aunque Q mejoró en dos. Se examinó si conservar el total regional puede ocultar errores de distribución espacial. Se reutilizaron las seis predicciones finales verificadas, las referencias y las máscaras fijadas. No se entrenó, no se modificaron pesos y no se abrieron imágenes test/generalization.

Se trata de un análisis exploratorio posterior a la observación del resultado. No cambia los ocho controles del ensayo concluido ni introduce umbrales para aprobarlo. La [revisión anterior](REVISION_REPETICION_F6518FF.md) conserva sus conclusiones.

## Diferencia entre total regional y error espacial

Para la realización \(k\), la región de borde \(R\), la predicción \(\widehat c_{kp}\) y la referencia \(c_p\), se definen

\[
C_R=\sum_{p\in R}c_p,\quad
B_{Rk}=\frac{\sum_{p\in R}(\widehat c_{kp}-c_p)}{C_R},\quad
A_{Rk}=\frac{\sum_{p\in R}|\widehat c_{kp}-c_p|}{C_R}.
\]

Se comparan \(\langle|B_{Rk}|\rangle_k\), error del total regional, y \(\langle A_{Rk}\rangle_k\), error píxel a píxel. El primero **no** es \(|\langle B_{Rk}\rangle_k|\), utilizado dentro de Q. Ambos se distinguen en los archivos de evidencia.

Si \(P_k\) es la suma de los residuos positivos y \(N_k\) la magnitud de los negativos, entonces

\[
A_{Rk}-|B_{Rk}|=\frac{P_k+N_k-|P_k-N_k|}{C_R}
=\frac{2\min(P_k,N_k)}{C_R}\ge0.
\]

La diferencia mide errores de signo opuesto que se compensan al sumar las cuentas. No es una medida de incertidumbre.

El término regional existente utiliza

\[
\ell_R=\left|\log(1+\overline{\widehat c}_R)-\log(1+\overline c_R)\right|.
\]

Por construcción, este término de una región permanece invariable al redistribuir sus cuentas conservando la suma. Esto no implica invariancia de toda la función de entrenamiento: L1, el crítico y las otras máscaras también intervienen y pueden detectar el cambio.

## Resultado sobre la entrega

Se analizaron 468 combinaciones de pareja, variante, vista y región; cada una resume veinte realizaciones. Los errores medios reproducen los del evaluador anterior con diferencias menores de 1e-12.

| Pareja | Error del total del borde C0 → C1 | Error píxel a píxel C0 → C1 | Vistas donde mejora el total y empeoran los píxeles |
|---|---:|---:|---:|
| R1 | 1,950 % → 0,625 % | 10,882 % → 11,448 % | 11/18 |
| R2 | 2,388 % → 1,062 % | 10,652 % → 11,121 % | 17/18 |
| R3 | 4,744 % → 2,453 % | 10,882 % → 10,967 % | 12/18 |

El total regional del borde mejora en las tres parejas, mientras el error espacial medio empeora en las tres. En 40 de las 54 combinaciones pareja/vista coinciden mejora del total y deterioro espacial; también mejora allí el término logarítmico regional. El error espacial aumenta en 47/54 combinaciones. Las 54 combinaciones reutilizan las mismas 18 vistas: no son 54 vistas distintas ni observaciones independientes.

El término logarítmico de borde disminuye de 0,01970 a 0,00622 en R1, de 0,02421 a 0,01052 en R2 y de 0,04862 a 0,02479 en R3. La diferencia entre error espacial y error del total aumenta 1,890; 1,794 y 2,376 puntos porcentuales, respectivamente.

Se verificó además un contraejemplo con la función original: una región de veinte píxeles, diez con una cuenta y diez con nueve, conserva cien cuentas al intercambiar ambos grupos. La pérdida regional permanece en el redondeo numérico de cero (8,89e-16), pero el error espacial relativo es 1,6, es decir, 160 %. Este control demuestra una limitación matemática del término; no demuestra que esa sea la única causa del comportamiento del entrenamiento adversario.

[Evidencia JSON](evidencias/diagnostico-espacial-cgan.json) y [tabla completa](evidencias/diagnostico-espacial-cgan.csv).

## Componente experimental E1

Se propone estudiar un término que actúe directamente sobre el error espacial del borde:

\[
L_{\mathrm{borde}}=\frac1B\sum_{b=1}^{B}
\frac{\sum_{p\in R_b}|\widehat c_{bp}-c_{bp}|}
{\sum_{p\in R_b}c_{bp}},
\qquad
L_G^{E1}=L_G^{C1}+\lambda_{\mathrm{borde}}L_{\mathrm{borde}}.
\]

Se conservan la inversión \(\widehat c=\exp(sz/(1-z))-1\), la escala fijada en train y la máscara geométrica de borde. Cada imagen pesa igual. El denominador vacío, el soporte menor de veinte píxeles y una inversión no finita se rechazan; no se añaden pseudocuentas ni se recortan predicciones. Las máscaras se utilizan solo durante entrenamiento; no se añaden entradas al generador.

El [componente aislado](herramientas/perdida_espacial_borde_experimental.py) coincide con el indicador espacial evaluado para cada imagen. No sustituye la conservación regional ni garantiza contraste, ausencia de sesgo o mejora de SSIM. Está fuera del ejecutor vigente: la formulación y las identidades del ensayo anterior permanecen intactas.

Las [nueve pruebas analíticas](herramientas/test_perdida_espacial_borde.py) verifican solución exacta, redistribución de cuentas, sesgo conocido, ponderación por imagen, gradiente por diferencias finitas, exclusión de píxeles fuera de la máscara y rechazo de soporte, referencia o rango inválidos. [Registro de comprobación](evidencias/verificacion-componente-borde.json).

## Sondeo con la red real

Se calcularon gradientes respecto de los parámetros del generador original en cuatro muestras train previamente incluidas en la prueba técnica: geometrías 01, 02, 04 y 10, vista 0, realización 0. Se utilizó modo evaluación con autograd, una imagen por cálculo y el crítico original congelado. Se comparó el gradiente de \(L_G^{C1}\) con el del término de borde de peso uno.

| Geometría train | Norma del gradiente C1 | Norma del gradiente de borde | Cociente borde/C1 | Coseno entre gradientes |
|---|---:|---:|---:|---:|
| 01 | 25,060 | 6,141 | 0,245 | 0,380 |
| 02 | 72,042 | 8,200 | 0,114 | 0,705 |
| 04 | 40,412 | 6,266 | 0,155 | −0,114 |
| 10 | 44,058 | 9,404 | 0,213 | 0,055 |

Los gradientes son finitos; las huellas de todos los estados del generador y del crítico permanecieron idénticas. Se realizaron **cero pasos de optimizador**. El coseno negativo de la geometría 04 muestra oposición local entre ambos términos, por lo que añadir el término no asegura una mejora conjunta.

Este sondeo no representa lotes de entrenamiento, cinco actualizaciones del crítico, recuperación CUDA ni evolución entre épocas. Tampoco selecciona un coeficiente óptimo. [Evidencia del sondeo](evidencias/sondeo-gradientes-borde.json).

## Preparación del siguiente ensayo

La hipótesis de trabajo es que una penalización espacial explícita pueda reducir la compensación de errores del borde sin perder la mejora regional. Se propone comparar E0, continuación con la pérdida C1 vigente, contra E1, idéntica continuación con el término espacial añadido. Ambas deben partir del mismo checkpoint original de época 5, con nuevos optimizadores y datos, duración y selección final idénticos. No corresponde comparar E1 exclusivamente con el mejor resultado histórico ni reutilizar pesos técnicos para el piloto.

| Pendiente | Estado | Criterio de cierre |
|---|---|---|
| E1-01: diagnóstico espacial | Verificado | Reproducción de errores, identidad de compensación y contraejemplo; evidencia enlazada. |
| E1-02: componente aislado y sondeo | Verificado en el alcance local indicado | Nueve controles analíticos, gradientes finitos y pesos idénticos; sin validación de entrenamiento. |
| E1-03: coeficiente y diseño ejecutable | Pendiente | Examinar gradientes en lotes train representativos de las doce geometrías y fijar una sola regla/coeficiente, semillas y presupuesto antes de observar resultados nuevos de val. |
| E1-04: integración y recuperación CPU | Pendiente | Identidad versionada, registro del término, equivalencia exacta con peso cero, rechazo de cambios de configuración y recuperación completa del nuevo bucle. |
| E1-05: prueba GPU y comparación | Pendiente | Nueva aceptación del código/entorno y ejecución de todas las ramas fijadas; no reutilizar la aceptación histórica. |
| OE2: aceptación científica | Pendiente | Justificar tolerancias físicas y evaluación final; el componente y el diagnóstico no cierran el objetivo. |

La comparación prospectiva deberá conservar Q por geometría, cielo, borde, contraste, SSIM y PSNR, además del nuevo desglose espacial. Los ocho controles anteriores se conservan como referencia descriptiva; no se relajan retrospectivamente. No se fija aquí una tolerancia física porque el conjunto actual no establece por sí solo cuánto error es admisible para el uso muográfico. Esa tolerancia debe justificarse por la sensibilidad requerida en cuentas y contraste, distinguiendo ruido de las referencias y sesgo del modelo.

El próximo trabajo local es E1-03/E1-04. **Todavía no se solicita a los estudiantes iniciar otra corrida.** Una vez cerradas esas etapas se podrán entregar instrucciones ejecutables y acotadas. No se prescribe más tiempo de GPU para el ensayo anterior.

## Reproducción

Desde la raíz del repositorio, con las dependencias CPU de la revisión anterior:

~~~bash
python objetivo-2/herramientas/diagnosticar_error_espacial_cgan.py \
  --datos /ruta/insumos --binarios /ruta/binarios \
  --entrega /ruta/entrega/datos/cgan-repeticion-f05 \
  --auditoria /ruta/revision-independiente.json \
  --salida /ruta/diagnostico-nuevo

python objetivo-2/herramientas/test_perdida_espacial_borde.py -v

python objetivo-2/herramientas/sondear_gradientes_borde_cgan.py \
  --datos /ruta/insumos --mascaras /ruta/binarios/mascaras-ajuste-v1 \
  --pesos /ruta/cgan-original-epoca5.pt \
  --salida /ruta/sondeo-nuevo.json
~~~

Los archivos de salida deben ser nuevos. El diagnóstico verifica el manifiesto y las huellas de predicciones; el sondeo verifica el checkpoint y la identidad de los datos/máscaras. Los textos de evaluación deben corresponder a la entrega fijada. Entorno registrado: Python 3.12.14, NumPy 2.3.5 y PyTorch 2.6.0+cpu. Se trabajó en una copia temporal de C:; no se reparó la copia Git antigua de D:. No se registraron fallos de ejecución en estas comprobaciones.

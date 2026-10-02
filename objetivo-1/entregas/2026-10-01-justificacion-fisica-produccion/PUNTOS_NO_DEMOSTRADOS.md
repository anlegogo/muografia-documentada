# Puntos no demostrados y comprobaciones propuestas

Cada punto indica la pregunta que se resuelve, qué se compara y el criterio de resultado satisfactorio, fijado antes de ejecutar. Ninguna de estas comprobaciones se ejecutó en esta entrega. Las duraciones se estiman con el tiempo medido de la campaña histórica: 0,737 ms de núcleo por evento, es decir, unos 64 s de pared para 2·10⁶ eventos en 24 núcleos *legacy*.

Las comprobaciones C1 a C3 condicionan la producción, porque pueden cambiar el ejecutable o la definición del dato. C4 a C6 condicionan la interpretación y el informe.

## C1. Contaminación de los píxeles de roca por muones blandos dispersados

**Lo que está demostrado.** En los píxeles de roca, el conteo depende del plano (figura 2; `comparacion-planos.json`). La razón entre los planos de 100 m y 600 m es 0,870 en cielo abierto, pero baja a 0,38 para columnas de 1–2·10⁵ g/cm² y a 0,25 por encima de 2·10⁵ g/cm². Con el plano de 600 m, el conteo en las columnas de roca ≥ 10⁴ g/cm² supera entre 3,1 y 6,8 veces la expectativa CSDA del surrogate, mientras que en cielo abierto es 0,77 veces esa expectativa. Los 3.483.882 muones que se ganan al pasar de 100 m a 600 m tienen una energía cinética media estimada de 0,86 GeV. Un muón de 100 GeV o más se desplaza menos de 1 m (figura 3, derecha), así que esos registros son muones blandos con desplazamientos de decenas a cientos de metros.

**Lo que no está demostrado.** No se ha demostrado que un detector físico de 1,2 m registre esa componente con la misma tasa. La equivalencia entre el plano grande y el panel exige que la materia atravesada no cambie apreciablemente entre líneas paralelas separadas por el desplazamiento. Con 50 m de desplazamiento a 1 km del edificio, el paralaje es de unos 2,9°, es decir, 12 píxeles.

**Pregunta.** ¿Existe un observable en el que el plano grande y el panel físico coincidan, de modo que la imagen deje de depender del tamaño del plano?

**Comparación.** El ejecutable instrumentado registra la energía cinética al cruzar el plano, ya disponible en `SteppingAction` como `post->GetKineticEnergy()`, y genera un histograma por cada umbral E_corte ∈ {0; 0,5; 1; 3} GeV. Se usan geo-train-01, vista 0, N = 2·10⁶, semilla 777 y planos de 100 m y 600 m. Son ocho histogramas en dos corridas de unos 64 s cada una. En macropíxeles de 8×8 se compara la razón 100/600 por banda de columna de roca, igual que en la figura 2.

**Criterio.** Se adopta el menor E_corte para el que la razón 100/600 en todas las bandas de roca sea ≥ 0,98, con incertidumbre de Poisson ≤ 0,01. Con ese corte, la razón de cielo abierto debe quedar dentro de ±1 punto porcentual del modelo de la figura 3. Si ningún corte cumple, el estimador direccional no está justificado para los píxeles de roca, y la alternativa pasa a ser C3.

## C2. Doble descuento del aire en la normalización

**Lo que está demostrado.** S0 integra el flujo de Guan por encima de 0,798 GeV, que es el umbral de 3 km de aire calculado con los parámetros CSDA de roca estándar. Después, el generador inyecta el espectro EcoMug, que también es de nivel del mar, entre 1,96 y 2,8 km aguas arriba, y Geant4 lo transporta por ese aire (`consistencia-espectro.json`). Ponderado por S0, el 6,6 % de los muones generados está por debajo del umbral de S0, y el transporte por aire elimina otro 19,5 % por frenado y decaimiento (2,5 % a 2–5°, 27 % a 44–47°). En cielo abierto, la exposición efectiva del trabajo 29484 es de 23,1 días equivalentes, con rango por fila de 12,1 a 27,7, frente a los 30 declarados (figura 4, derecha).

**Pregunta.** ¿El espectro inyectado representa el flujo en el punto de inyección o en el detector? Si representa el flujo en el detector, ¿debe transportarse por el aire previo?

**Comparación.** Se proponen dos variantes del generador con la misma semilla y N = 2·10⁶: (a) la actual; (b) retroceso solo hasta salir del cilindro que contiene el edificio, con el radio base de la geometría más un margen de 50 m, en lugar de `R_inicio = D + R + 300 m`. En ambas se mide la eficiencia de cielo abierto por fila y la razón entre el conteo de roca y S0.

**Criterio.** Se considera consistente la variante en la que el conteo de cielo abierto dividido por la tasa inyectada por fila es ≥ 0,97 en las filas de 20 a 42°, con la pérdida restante explicada por el decaimiento en el tramo de aire residual según el modelo de la figura 3 (±1 punto porcentual). Si se adopta (b), S0 se recalcula con el umbral del rango generado (+6,2 %, figura 4) y se vuelve a ejecutar C1.

## C3. Equivalencia del estimador con un detector físico (alternativa a C1)

**Pregunta.** Si no se adopta un corte de energía, ¿coincide el estimador actual con un panel físico que recibe también muones vecinos?

**Comparación.** Esta es la referencia propuesta por la dirección (`REVISION_ACEPTACION_PLANO.md`): impactos nominales uniformes sobre un cuadrado de 300 m de lado, con conteo solo en el panel central, y se compara con el estimador actual en macropíxeles de 8×8. Para el panel físico de 1,44 m², la dilución es (300/1,2)² = 62.500. Con un panel de 10×10 m, cuyo paralaje de 0,57° es inferior a un macropíxel, la dilución es de 900 y obtener la estadística del plano de 600 m en las bandas de roca de 3·10⁴–10⁵ g/cm² requiere unos 3,2·10¹⁰ eventos (900 × 3,6·10⁷), es decir, unas 6.600 h-núcleo.

**Criterio.** Las razones por banda de roca entre la referencia y el estimador deben ser compatibles con 1 a 2σ. Dado el coste, solo se recomienda si C1 no encuentra un corte válido.

## C4. Pérdida por migración angular en los bordes de la ventana

**Lo que está demostrado.** El generador inyecta direcciones solo dentro de la ventana de la imagen, de 2 a 47° de elevación y de −30 a +30° de azimut, y el contador registra en esa misma ventana. Los muones que se dispersan hacia fuera se pierden, pero no entra ninguno desde fuera. Con el plano de 600 m, el residuo medido menos el modelo es de −11,0 puntos porcentuales en las filas por encima de 44° y llega a −32 en la fila superior (medido 40,2 %, modelo 71,9 %) (figura 3, centro).

**Pregunta.** ¿Qué margen angular de generación elimina el déficit en los bordes?

**Comparación.** Se genera en una ventana ampliada en Δ ∈ {2; 5}° por cada lado, con pesos de fila y espectro extendidos, y se cuenta en la ventana nominal. Se usa N = 2·10⁶ en cada caso.

**Criterio.** Se adopta el menor Δ con el que la eficiencia de cielo abierto en las cinco filas y columnas de borde coincide con la tendencia de las filas interiores (ajuste lineal en 30–42°) dentro de 1 punto porcentual.

## C5. Asíntota del plano

**Lo que está demostrado.** La afirmación «menos de 0,5 % de la asíntota» se apoya en tres valores de un comentario de código: 64,2; 73,07 y 73,81 %. Sus histogramas, comandos y salidas no se conservan (sección 1 del README). El modelo gaussiano predice que el plano de 600 m retiene todo salvo 0,07 puntos porcentuales del núcleo de dispersión. Sin embargo, en las filas interiores el valor medido queda 0,90 puntos porcentuales por debajo del modelo, de modo que las colas no gaussianas pueden ser mayores. La cota no queda demostrada.

**Comparación.** Si C1 no adopta un corte de energía: plano de 1.200 m frente a 600 m, con N = 2·10⁶ y semilla 777.

**Criterio.** |ε₁₂₀₀ − ε₆₀₀| < 0,1 punto porcentual en total, y razón por banda de roca compatible con 1 dentro de 2σ. Si C1 adopta un corte, esta comprobación se hace con ese mismo corte.

## C6. Convención de área y significado de «30 días»

**Lo que está demostrado.** S0 usa A = 1,44 m² perpendicular a cada dirección, sin proyección. Un panel vertical real aporta A·cos(el)·cos(az), lo que reduce S0 un 21,5 % (factor medio 0,785). Interpretar la energía del umbral como cinética en lugar de total cambia S0 un −2,1 %. Es una decisión de definición, no de simulación.

**Pregunta.** ¿El píxel es una cuenta esperada de un detector vertical o un flujo direccional multiplicado por el área normal?

**Comparación.** No requiere corrida. Se documenta la decisión y se recalcula S0 con `scripts/exposicion_equivalente.py`, ajustando la variante.

**Criterio.** La ficha de datos declara la convención, y S0, N y la exposición equivalente se recalculan con ella. No se mezclan referencias con convenciones distintas en una misma versión.

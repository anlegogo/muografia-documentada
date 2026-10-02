# Revisión local de la aceptación del plano de conteo

2026-10-01, Colombia. **Avance conceptual de P-04; no constituye validación física ni una nueva corrida.**

## Qué resolvimos

Separamos dos preguntas que requieren evidencias distintas:

1. ¿Un plano de conteo suficientemente grande recoge casi todos los muones de la muestra generada que podrían llegar a ese plano?
2. ¿El conteo obtenido representa lo que registraría un detector físico pequeño situado en ese lugar?

La convergencia al aumentar el tamaño del plano aborda la primera pregunta. **No demuestra por sí sola la segunda.** La compensación entre muones que se dispersan hacia fuera y vecinos que se dispersan hacia dentro necesita justificar sus supuestos espaciales y angulares.

## Evidencia disponible del proyecto

En `PrimaryGeneratorAction.cc` de `d8ca749` (sin cambio de esta regla en `0dea8e1`), el impacto nominal se elige en un panel de 1,2×1,2 m y la posición inicial se obtiene retrocediendo sobre la dirección elegida. En `DetectorConstruction.cc` el volumen que registra llegadas mide 600×600 m. En `SteppingAction.cc` se cuenta según dirección al entrar al plano y se termina la trayectoria del primario. El contador admite muones que ya no llegan al panel pequeño.

Los comentarios de código y la [bitácora histórica](originales/bitacora-simulacion.md) reportan, para geo-train-01 vista 0, eficiencias de registro de 64,2 %, 73,07 % y 73,81 % con lados de plano 100, 300 y 600 m. Entre los dos últimos valores hay 0,74 puntos porcentuales, aproximadamente 1,013 % respecto al valor de 300 m. Esos tres números no proporcionan por sí solos una cota de distancia a una asíntota desconocida.

La bitácora menciona menos de 0,5 % respecto de la asíntota. **No reproducimos aquí esa cota:** en la selección local y en el árbol de código `0dea8e1` consultado no identificamos un paquete específico con todos los resultados de convergencia, tamaños mayores y método de estimación que la sustente. No afirmamos que ese respaldo no exista en SC3. El archivo de comparación Geant4/surrogate disponible es otra evidencia: compartir una convención de aceptación no la verifica independientemente.

## Comprobación matemática propia

Como ejemplo deliberadamente simplificado, consideramos una coordenada lateral x, un panel P de ancho 1,2 y un desplazamiento de llegada de +10 o −10 con igual probabilidad. La supervivencia T(x) puede variar entre el centro y los alrededores. **Son cantidades elegidas para un contraejemplo, no parámetros medidos del volcán.** No se modelan energía ni dirección final; los resultados se expresan en unidades arbitrarias.

El conteo con impacto nominal restringido al panel y plano grande S es proporcional a:

\[
C_S=\int_{x\in P}T(x)\,\Pr(x+\Delta\in S)\,dx.
\]

El conteo en el panel físico, incluyendo los posibles muones vecinos, es proporcional a:

\[
C_P=\int_{x\in\mathbb{R}}T(x)\,\Pr(x+\Delta\in P)\,dx.
\]

Aquí se supone densidad incidente uniforme por unidad lateral. Si T es constante y el desplazamiento tiene la misma distribución en todo x, un plano S que recoge todos los desplazamientos del panel da el mismo resultado. Si T cambia espacialmente, esa igualdad no está garantizada.

| Caso matemático | Plano grande | Panel pequeño con vecinos | Cociente |
|---|---:|---:|---:|
| T=0,7 en todas partes | 0,84 | 0,84 | 1 |
| T=1 en el centro, 0,5 fuera | 1,20 | 0,60 | 2 |
| T=0,5 en el centro, 1 fuera | 0,60 | 1,20 | 0,5 |

En los tres casos el resultado del plano grande es idéntico para anchos 100, 300 y 600: converge perfectamente. Sin embargo, los dos casos heterogéneos no coinciden con el panel físico. **Los cocientes 2 y 0,5 no estiman el error del repositorio y no son factores de corrección.** Solo muestran que la convergencia del plano no basta para demostrar compensación en general.

Calculamos integrales exactas con números racionales y las contrastamos con cuadratura independiente de 12.000 puntos por intervalo: nueve combinaciones, error máximo menor de 3,3×10⁻¹³. [Código reproducible](../herramientas/control_compensacion_plano.py) y [resultados identificados como ejemplo matemático](evidencias/control-compensacion-plano.json).

```console
python herramientas/control_compensacion_plano.py --salida NUEVO_INFORME.json
```

La documentación oficial de Geant4 distingue el registro de cantidades del muestreo que modifica frecuencias y exige que un estimador con muestreo sesgado conserve la media del muestreo análogo para el mismo observable. Es un principio de validación, no una certificación de este modelo: [Event Biasing Techniques, Geant4 11.4](https://geant4.web.cern.ch/documentation/dev/bfad_html/ForApplicationDevelopers/Fundamentals/biasing.html). Nuestro contraejemplo es una derivación propia; no procede de esa documentación.

## Siguiente paso bien delimitado

Antes de pedir otra ejecución, revisar con los estudiantes:

- **Observable previsto:** si la imagen representa llegadas al panel físico o un estimador direccional idealizado, y qué afirmaciones permite esa elección respecto del OE1 y del informe. No cambiar la interpretación solo para evitar una validación pendiente.
- **Respaldo existente:** datos, comandos, semillas, tamaños de plano y errores de la serie de convergencia; derivación de la compensación espacial y angular y de la normalización temporal.
- **Control faltante, si lo hay:** comparar el estimador actual con una referencia que contemple impactos nominales en una región espacial suficientemente amplia y registre llegadas al panel físico, con pesos/normalización acordes con la generación. Ampliar el área de generación no es lo mismo que ampliar el plano que cuenta. No comparar números brutos con diferente número o densidad de primarios.

Para ese eventual control, definir previamente casos homogéneos y con variación espacial, cantidades comparables, tolerancia vinculada al uso de los datos, incertidumbre y convergencia del área de generación. No fijamos todavía N ni comandos: faltan la definición del observable y la derivación del estimador de referencia. No basta reducir el plano de conteo a 1,2 m conservando una fuente restringida al panel, pues así se omitirían posibles contribuciones vecinas.

No repetimos la corrección angular ni la etapa 2. No sustituimos tablas ni descartamos los datos históricos. Ahora P-04 tiene una pregunta física concreta y una razón demostrada para distinguirla de la convergencia numérica. Este es el pendiente principal antes de fijar la campaña final.

## Precisión adicional sobre la normalización de la fuente

La lectura local de `surrogate/imaging.py`, `surrogate/flux_model.py` y `build_generator_tables.py` permite identificar la tasa heredada: se obtiene `lambda/transmission = phi_sky × A × dOmega × T`, donde `phi_sky` ya utiliza el umbral analítico de una columna de aire. Con los valores del código, 3.000 m y 0,001225 g/cm³, la columna es 367,5 g/cm² y `E_min=(a/b)*expm1(b*X)` da **0,7980614314 GeV**.

La tabla condicional de momentos usada en Geant4 incluye, en sus 16 bandas, valores mínimos que al convertir a energía cinética quedan entre aproximadamente 0,405 y 0,489 GeV. [Diagnóstico y huellas](evidencias/diagnostico-normalizacion-fuente.json). La conversión aplicada es `sqrt(p²+m_mu²)-m_mu`, con masa 0,1056583745 GeV, igual a la del generador. Los valores de la parametrización de flujo también requieren aclarar su convención de energía.

**No concluimos que exista doble descuento de pérdidas ni calculamos un factor corrector con estos números.** Precisamos la pregunta: ¿a qué superficie, espectro y convención energética corresponde la tasa que se usa para fijar N, y cómo se conecta con los primarios inyectados antes de transportar por aire? Esto forma parte de P-04 y de la misma justificación de exposición solicitada; no exige por sí solo otro ensayo ni invalida la comparación A/B realizada con fuente compartida.

# Diseño del ajuste acotado de conservación de cuentas

Fecha: 2026-10-03, Colombia. **Estado vigente: integración y entrenamiento técnico con recuperación verificados en CPU; comprobación GPU y piloto A/B pendientes.** La [guía operativa](INSTRUCCIONES_AJUSTE_CUENTAS_F05.md) contiene los comandos del nuevo ejecutor y la evidencia. No se ha realizado el ensayo completo de cinco épocas. Las especificaciones históricas no son configuraciones del ejecutor del piloto v1.

## Problema y pregunta

La [evaluación geométrica](EVALUACION_GEOMETRICA_PILOTO_F05.md) mostró que reducir el error de imagen no garantiza conservar las cuentas regionales. En la U-Net seleccionada se observaron sesgos medios de −16,97 % en roca sin anomalía, −36,07 % en cavidad y −59,96 % en cuerpo denso. Las cifras pertenecen a validación y no son errores de densidad.

Se propone comprobar si añadir un término de conservación regional reduce ese sesgo sin deteriorar cielo, bordes y contraste. Es una hipótesis de ajuste; el diagnóstico no demuestra la causa del sesgo y el nuevo término no garantiza su corrección.

La primera comparación se limita a U-Net. Incorporar simultáneamente cambios adversarios impediría separar sus efectos. La cGAN actual permanece como referencia congelada; una eventual extensión del ajuste a cGAN requiere una decisión posterior y no está incluida en este ensayo.

## Comparación controlada

Ambas ramas parten del mismo generador U-Net de época 5, ya verificado. No se compara una red continuada únicamente contra otra que no tuvo oportunidad de continuar.

| Elemento | A: control | B: ajuste regional |
|---|---|---|
| Pesos iniciales | Mismo best.pt U-Net de época 5 | Los mismos |
| Pérdida | \(100L_1\) | \(100L_1+L_{\mathrm{reg}}\) |
| Arquitectura / fracción | unet_dc_5 / 0,05 | Iguales |
| Datos | 1.440 pares train / 360 val | Iguales |
| Optimizador | Adam nuevo, lr \(10^{-5}\), betas (0; 0,9) | Igual |
| Semilla | 2026100302 | Igual |
| Lote / aumentos | 4 / desactivados | Iguales |
| Duración | Cinco épocas adicionales | Igual |
| Selección principal | Checkpoint al terminar la quinta época adicional | Igual |

Se reinician los estados del optimizador y los generadores aleatorios de ambas ramas de forma idéntica; se conservan únicamente los pesos del generador inicial. Esta es una continuación controlada con optimizador nuevo, no la reanudación del piloto antiguo. Las dos ramas deben tener exactamente el mismo orden de muestras y condiciones de determinismo.

La semilla nueva no convierte el ensayo en una réplica independiente desde cero: ambos modelos heredan el mismo entrenamiento y la selección previa sobre validación. No se reclamarán intervalos de variabilidad entre entrenamientos.

No hay parada temprana por SSIM ni selección retrospectiva de la época que favorezca el resultado. Las curvas se registran cada época, pero la comparación primaria usa la quinta época adicional. Si hay fallo técnico o se agota el tiempo, el ensayo se declara incompleto y no se sustituye por una época anterior. El último checkpoint completo puede servir para reanudar la misma rama con identidad compatible.

Las dos [especificaciones A](configuraciones/ajuste-cuentas-v1/ajuste-control.spec.json) y [B](configuraciones/ajuste-cuentas-v1/ajuste-regional.spec.json) solo difieren en identificador, nombre de rama experimental y peso del término regional. Incluyen estado explícito no preparado para GPU; no deben pasarse a ejecutar_piloto.py ni añadir sus campos al motor suponiendo que serán utilizados.

## Término de pérdida

Las máscaras se obtienen de geometría y coordenadas mediante las reglas del diagnóstico regional: cielo, roca sin anomalía, borde del cono y núcleos de anomalías con longitud mínima de 20 m y erosión de un píxel. Su preparación ya se amplió y verificó sobre las 12 geometrías de train y las tres de val; no se reutilizan máscaras de val como si pertenecieran a train.

Para cada región \(R\), \(z_p\) es la salida normalizada del generador y \(c_p\) la referencia de cuentas de entrenamiento. Se define

\[
t_p=\frac{s z_p}{1-z_p},\qquad
\widehat c_p=\exp(t_p)-1,\qquad
\ell_R=\left|\log(1+\overline{\widehat c}_R)-\log(1+\overline c_R)\right|.
\]

Se mantiene \(s=8,239329427901795\), fijado solo con train. Para evitar formar exponenciales que desborden, se utiliza la identidad exacta

\[
\log(1+\overline{\widehat c}_R)
=\operatorname{logsumexp}_{p\in R}(t_p)-\log|R|.
\]

No se recortan salidas ni se aplica un factor global de corrección. Una salida fuera de \(0\le z<1\), o una pérdida o gradiente no finitos, es un fallo explícito. La estabilidad de logsumexp no garantiza que un gradiente muy grande sea apropiado para optimizar.

Dentro de cada imagen, las regiones se agrupan en cuatro familias: cielo, roca, borde y anomalías. Cada familia no vacía tiene el mismo peso, y cada anomalía válida pesa igual dentro de su familia. Después se promedia entre imágenes:

\[
L_{\mathrm{reg}}
=\frac1B\sum_{b=1}^{B}
\frac1{|\mathcal F_b|}
\sum_{f\in\mathcal F_b}
\frac1{|\mathcal R_{b,f}|}
\sum_{R\in\mathcal R_{b,f}}\ell_R.
\]

Solo participan máscaras con al menos veinte píxeles. Se deben registrar las regiones y familias excluidas por falta de soporte. Una imagen sin regiones válidas se rechaza. El control homogéneo tiene cielo, roca y borde, sin exigirle una anomalía inexistente. Las máscaras no se asumen disjuntas.

El logaritmo suaviza las diferencias de escala entre cielo y roca; el promedio por familias evita que la cantidad de píxeles de cielo domine este término. No equivale a una verosimilitud Poisson ni a una medida de incertidumbre: las referencias tienen ruido y los pares derivan de ellas.

El coeficiente regional se fija en uno como primera hipótesis acotada, antes de la comprobación real. No se calibró para conseguir una mejor cifra en val. Si el ensayo indica que debe cambiar, se documentará un diseño nuevo; no se probarán pesos sucesivos sin registrarlos.

El \(1+\overline c\) pertenece a la transformación de la pérdida, no añade cuentas a los datos. El contraste de evaluación conserva su definición original sin pseudoconteos; un control con cero cuentas sigue produciendo un cociente indefinido.

Las máscaras y las referencias solo intervienen en la pérdida durante entrenamiento. En inferencia el generador recibe únicamente la imagen de baja estadística normalizada. Este ajuste no exige conocer la geometría o la referencia al inferir.

## Qué se medirá y cómo se decidirá

Se conservarán los pesos iniciales, los finales A/B y sus predicciones sobre los mismos 360 pares de val. Se reutilizarán las máscaras y el emparejamiento geométrico del diagnóstico, sin mover regiones según la apariencia del nuevo resultado.

El indicador principal es el sesgo absoluto regional, calculado primero por vista y después por geometría. Para roca y anomalías se informará, por cada geometría \(g\),

\[
Q_g=\frac12\left[
\frac16\sum_v\left|\overline B_{g,v,\mathrm{roca}}\right|
+\frac16\sum_v\frac1{J_g}\sum_{j=1}^{J_g}
\left|\overline B_{g,v,j}\right|
\right],
\qquad Q=\frac13\sum_g Q_g.
\]

Las tres geometrías val tienen anomalías, de modo que \(J_g>0\). \(\overline B\) es el promedio del sesgo firmado entre las veinte realizaciones de esa vista; se toma su magnitud antes de agregar vistas. Así se evita que una sobreestimación compense una subestimación entre vistas. Se informará también la media de \(|B_k|\), que incluye la dispersión entre realizaciones y no es el mismo indicador.

Además se entregarán:

- Sesgo absoluto y error absoluto de cuentas por familia y geometría, incluidos cielo y borde.
- Error absoluto de contraste, primero en las 23 combinaciones comunes con cocientes definidos en las veinte realizaciones de entrada; las 24 combinaciones permanecen en la tabla completa, con los tres ceros declarados.
- SSIM y PSNR por geometría y globales, en la normalización v1.
- Figuras de todas las vistas, con idénticas escalas y residuos, sin seleccionar solo ejemplos favorables.
- Pérdida L1, pérdida regional, contribuciones por familia, norma de gradiente, tiempo y memoria por época.

La decisión es descriptiva y separa tres resultados:

1. **Mejora concordante:** B reduce \(Q\), no aumenta ningún \(Q_g\), y no deteriora nominalmente el error regional de cielo/borde, el error de contraste común, SSIM ni PSNR frente a A. Se considera prometedor para una repetición posterior; no acredita significación ni cierre físico.
2. **Compromiso:** mejora alguna medida y empeora otra. Se identifica dónde ocurre; no se presenta como éxito global ni se ajustan los umbrales para aprobarlo.
3. **Sin mejora regional o fallo técnico:** se conserva la entrega completa y se revisa el diseño. No se amplía automáticamente.

Se comparan valores sin redondear. Diferencias pequeñas no se consideran evidencia sólida de mejora; deben contrastarse con reproducción numérica y variabilidad entre futuras semillas. No se introduce una tolerancia de aceptación física basada en los resultados ya observados. La campaña principal y las particiones reservadas permanecen fuera de esta decisión.

## Etapas y presupuesto

**Ajuste-01 — Integración del ejecutor: verificado en CPU.** La [evidencia de integración](evidencias/integracion-ajuste-v1.json) y el [manifiesto de máscaras](evidencias/manifiesto-mascaras-ajuste-v1.json) acreditan los requisitos siguientes, conservados como criterio de cierre. Debe añadirse una interfaz explícita que entregue, junto a cada imagen, sus cuentas de referencia, identificador de geometría/vista y máscaras correspondientes. No se adivinará la geometría a partir de la imagen ni se buscarán máscaras usando valores predichos. El cálculo de máscaras actual requiere adaptar el caso de catálogo sin anomalías, además de recorrer train; esos casos deben comprobarse antes del lanzamiento.

La implementación deberá rechazar campos desconocidos, identidades incompatibles, carga cruzada A/B y mezcla de datos. Se conservarán las huellas de código, geometrías, máscaras, protocolo, configuración y pesos iniciales. El código v1 y las entregas estudiantiles no se sustituyen silenciosamente.

**Ajuste-02 — Prueba técnica CPU y GPU con recuperación: parcial.** Recuperación exacta verificada en CPU; GPU pendiente. Se conserva el procedimiento requerido: Ocho pares train y ocho val, lote cuatro y dos épocas por rama. Las listas de geometría/vista/realización están fijadas en los JSON. Train incluye caso homogéneo, conducto, cuerpo denso y dos cavidades. Se interrumpe al terminar la primera época y se reanuda la segunda. La prueba debe contrastarse con la ejecución continua, sin duplicar pasos ni perder estados. Con peso regional cero debe conservarse el resultado y el gradiente de la pérdida original.

Se requieren optimización finita, correcta correspondencia máscara/muestra, igualdad de inicialización y orden de datos A/B, conservación/reanudación del optimizador y del RNG, rechazo de cambio de rama/configuración y registro del entorno. La comprobación GPU todavía no está realizada.

**Ajuste-03 — Comparación breve: pendiente.** Tras cerrar la integración y la prueba técnica, se ejecutan cinco épocas por rama desde los pesos originales de época 5, nunca desde los pesos de la prueba técnica. Son 360 lotes por época, 1.800 actualizaciones por rama y 3.600 en total. Las dos ejecuciones técnicas recuperadas suman ocho actualizaciones; sus dos referencias continuas añaden otras ocho. La batería completa requiere 16 actualizaciones, aclaración del presupuesto inicial de ocho. Son actualizaciones de red, no transportes de muones ni nuevas corridas Geant4.

No se promete una duración de pared a partir del piloto previo: el término regional agrega cómputo y utiliza operaciones en doble precisión para estabilidad. Se medirá tiempo y memoria en la prueba técnica, y se estimará la duración antes de asignar GPU. Las ramas pueden ejecutarse secuencialmente en una GPU. No se contratan recursos ni se reserva SC3 en esta preparación.

La entrega de A/B debe incluir especificaciones efectivas, registros completos, checkpoint inicial identificado, last/final con huella, estados de recuperación, predicciones val, tabla por imagen/región, resumen y figuras. Los pesos grandes se distribuyen por Drive con hashes; no se incorporan a Git.

## Comprobaciones iniciales del diseño

Este apartado conserva la evidencia anterior a la integración. La comprobación posterior del bucle completo y la recuperación se documenta en la [guía vigente](INSTRUCCIONES_AJUSTE_CUENTAS_F05.md).

Se implementó el [componente de pérdida](herramientas/perdida_cuentas_regionales.py) sin modificar el motor v1. Se superaron nueve pruebas: solución exacta, sesgo conocido, referencias cero, equivalencia del control de peso cero, gradiente por diferencias finitas, ponderación por familias, soporte insuficiente, rechazo de rango inválido y estabilidad cerca de uno. [Evidencia](evidencias/verificacion-diseno-ajuste-v1.json).

Se verificó además el paso por la U-Net completa de 20.543.809 parámetros y retropropagación sobre dos pares de geo-train-06/vista 0, realizaciones 0 y 1, con huellas de geometría, shard, pesos y manifiesto contrastadas. Se obtuvieron \(L_1=0,00925712\), \(L_{\mathrm{reg}}=0,12890505\) y pérdida total \(1,05461722\). La norma del gradiente del término regional fue 7,48147 y la del total 40,37737; ambas finitas. Se verificó que todos los parámetros permanecieron idénticos: cero pasos de optimizador.

Esta comprobación usó modo eval con gradientes habilitados, CPU, PyTorch 2.6.0+cpu y NumPy 2.3.5. No valida el bucle de entrenamiento, recuperación, rendimiento GPU ni las 12 geometrías de train. [Evidencia con pesos reales](evidencias/verificacion-perdida-red-real-v1.json).

Incidencias: la utilidad automática de comprobación de gradientes requería SymPy ausente; se sustituyó por diferencias finitas centrales explícitas y las nueve pruebas terminaron correctamente. Se corrigió lectura UTF-8 explícita de las geometrías en Windows. Se utilizó el entorno aislado de las revisiones previas; no se reparó la copia local de Git.

## Reproducción disponible

Desde la raíz del repositorio, en un entorno con NumPy y PyTorch 2.6.0 compatibles:

```powershell
python objetivo-2/herramientas/verificar_diseno_ajuste.py --especificaciones objetivo-2/configuraciones/ajuste-cuentas-v1 --salida trabajo/verificacion-diseno-ajuste.json
python objetivo-2/herramientas/comprobar_perdida_con_pesos.py --repo . --datos trabajo/drive-2026-10-03 --pesos trabajo/pesos/unet-best.pt --salida trabajo/verificacion-perdida-real.json
```

El directorio de salida debe existir. Los parámetros opcionales torch-dir, insumos y modulos permiten repetir el procedimiento en un entorno aislado con copias verificadas, como se hizo en esta revisión. Los comandos anteriores verifican el diseño y la retropropagación; no entrenan.

El lanzamiento ya dispone de [comandos verificados en CPU](INSTRUCCIONES_AJUSTE_CUENTAS_F05.md). Los JSON ejecucion-A.json y ejecucion-B.json son configuraciones del nuevo ejecutor; las especificaciones anteriores se conservan como antecedente. Antes del piloto se exige la comprobación técnica en GPU y la aceptación generada por el revisor.

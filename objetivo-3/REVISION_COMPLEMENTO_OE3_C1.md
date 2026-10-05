# Revisión del complemento OE3-C1

Revisión de la dirección: 2026-10-04, Colombia. Entrega de estudiantes: 2026-10-04, rama `oe3/complemento-oe3-f05`, commit `5c3b0ee6cc305d13b34f70b19c82c63489794206`. Código de ejecución: `39d8fd3e398a540ea42e025fce8c42fa25986dfa`. Se conserva la entrega original y se documenta la revisión por separado.

## Alcance y conclusión

El complemento evalúa los ocho modelos congelados al 1 %, 5 %, 10 % y 50 % de los conteos, con la normalización de entrenamiento y las particiones originales. El 5 % se reutiliza de EF-01; las demás fracciones son nuevas inferencias de los estudiantes. No se entrenaron modelos nuevos, no se seleccionó una semilla y no se ejecutó otra simulación de muones.

**Ningún modelo alcanza conjuntamente los umbrales SSIM y PSNR del referente sin red al 50 %, en ninguna vista y en ninguna fracción evaluada.** Por ello no existe un mínimo muestreado que satisfaga ese benchmark y no se demuestra un factor de reducción bajo esa regla. El valor debe conservarse como nulo/no demostrado; no debe sustituirse por cero, uno o un cociente nominal de conteos.

Se trata del benchmark operativo definido en el [protocolo](PROTOCOLO_COMPLEMENTO_OE3.md), después de conocer los resultados históricos y antes de las inferencias nuevas. No era un umbral numérico de la propuesta aprobada, una tolerancia geofísica ni una validación confirmatoria independiente. Un resultado negativo bajo esta regla es admisible y no obliga a modificarla o a entrenar hasta obtener éxito.

## Integridad y reproducción

Se descargaron 298 archivos. Coinciden las huellas SHA-256 de los 294 archivos del manifiesto y de las **96 matrices NPY**, que suman **3.019.911.168 bytes y 11.520 predicciones nuevas**. Todas son float32, de forma 120 × 256 × 256, finitas y dentro del intervalo admitido. Los manifiestos y el resumen de Drive coinciden byte a byte con los blobs de la entrega Git.

Se reprodujeron en CPU las 17.280 filas de imagen, 4.536 regionales, 216 contrastes, 39.096 filas locales y 2.160 registros entre realizaciones, usando las predicciones recibidas y el bloque f05 conservado. Coinciden estructura, estados, exclusiones y valores dentro de la tolerancia numérica registrada. La mayor diferencia absoluta entre números es 7.105e-15; la mayor diferencia escalada por max(1, |valor|) es 2.554e-15. No se exige identidad binaria entre JSON de entornos distintos.

Además se recalculó el benchmark desde la tabla de imágenes: **0 de 768** combinaciones modelo/fracción/vista satisfacen simultáneamente SSIM y PSNR. Se conserva el [desglose por vista](evidencias/revision-complemento-c1/benchmark_por_vista.csv).

La ejecución GPU corresponde a los estudiantes, en una NVIDIA L40S de RunPod. La revisión local de la dirección recalcula las métricas sobre las matrices entregadas; no vuelve a inferir ni acredita mediante una repetición propia el rendimiento temporal de la GPU. Las ocho pruebas técnicas entregadas tienen diferencia máxima cero respecto de las cuatro imágenes de control al 5 %.

## Calidad global y conservación de cuentas

Para la cGAN original se obtiene:

| Partición | Entrada | SSIM | PSNR (dB) | Q (%) |
|---|---:|---:|---:|---:|
| Prueba | 1 % | 0,8124 | 29,264 | 45,279 |
| Prueba | 5 % | 0,8342 | 31,170 | 14,566 |
| Prueba | 10 % | 0,8378 | 31,213 | 15,732 |
| Prueba | 50 % | 0,7761 | 27,255 | 38,996 |
| Generalización | 1 % | 0,8040 | 29,069 | 52,203 |
| Generalización | 5 % | 0,8252 | 31,047 | 16,959 |
| Generalización | 10 % | 0,8304 | 31,174 | 10,179 |
| Generalización | 50 % | 0,7644 | 27,274 | 29,066 |

Q es el indicador regional de cuentas definido en EF-01; no es error de densidad ni una probabilidad de detección. La [tabla completa](evidencias/revision-complemento-c1/sintesis_metricas.csv) incluye entrada, U-Net, cGAN y las seis continuaciones, sin selección posterior de modelos.

La figura siguiente presenta los promedios por partición y el error de contraste sobre soporte común. Las líneas unen puntos medidos para facilitar la lectura; no interpolan factores de adquisición. Las seis continuaciones se conservan como líneas grises, con sus cifras individuales en la tabla. No se confunde un promedio con el criterio de aceptación por vista.

![Calidad y contraste del complemento](evidencias/revision-complemento-c1/curvas-complemento.svg)

En los promedios de ambas particiones, todos los modelos tienen SSIM y PSNR menores al 50 % que al 5 % y que la entrada sin red al 50 %. La transferencia de los pesos entrenados al 5 % resulta limitada; estos datos no permiten atribuir por sí solos el deterioro a un mecanismo causal específico. No equivalen a evaluar modelos entrenados para cada fracción.

La mejora de similitud al 1 % frente a entradas ruidosas coexiste con errores Q elevados. Por ello no se transforma esa mejora en una afirmación de conservación física o de equivalencia con exposiciones largas. El resultado descriptivo anterior cGAN 5 % frente a entrada 10 % conserva sus límites y no reemplaza el benchmark cuando este no se satisface.

## Anomalías: análisis con soporte común

Se usa la referencia de alta estadística una sola vez por región/vista, aunque esté registrada en cada fracción. Las métricas locales mantienen exactamente las definiciones del protocolo. Los soportes comunes de las cuatro fracciones son 30 combinaciones anomalía/vista para SNR y 32 para CNR y contraste. No se rellenan con ceros los casos no estimables.

Para cada método se promedian las veinte realizaciones de cada región/vista, después los casos de cada geometría y finalmente las geometrías con igual peso dentro de la partición. Las tres geometrías de prueba permanecen separadas de la única geometría de generalización. Las realizaciones no se tratan como volcanes independientes; no se reporta significación estadística ni intervalo de confianza geológico.

Esta síntesis es descriptiva y posterior a la entrega; no añade una condición de aceptación. El error absoluto se calcula por realización antes de promediar. No debe igualarse directamente con promedios anteriores que usaban otro soporte o calculaban el error después de promediar el contraste. Las tablas originales se conservan; SSIM, PSNR y Q mantienen su agregación original y no se filtran por el soporte común local.

La siguiente tabla muestra la cGAN original y la entrada sin red sobre el mismo soporte de contraste, conservando todas las fracciones. El error y la inversión de signo se calculan antes de promediar las realizaciones, para evitar cancelar errores de signos opuestos.

| Partición | Conteos | Método | Error absoluto de contraste | Inversiones de signo (%) |
|---|---:|---|---:|---:|
| Prueba | 1 % | Entrada | 0.51541 | 40.63 |
| Prueba | 1 % | cGAN | 0.11490 | 44.19 |
| Prueba | 5 % | Entrada | 0.17073 | 38.12 |
| Prueba | 5 % | cGAN | 0.07557 | 43.54 |
| Prueba | 10 % | Entrada | 0.11326 | 36.81 |
| Prueba | 10 % | cGAN | 0.08441 | 43.50 |
| Prueba | 50 % | Entrada | 0.03470 | 18.95 |
| Prueba | 50 % | cGAN | 0.14863 | 44.38 |
| Generalización | 1 % | Entrada | 0.56918 | 42.27 |
| Generalización | 1 % | cGAN | 0.11660 | 50.91 |
| Generalización | 5 % | Entrada | 0.15881 | 40.00 |
| Generalización | 5 % | cGAN | 0.07864 | 44.09 |
| Generalización | 10 % | Entrada | 0.11908 | 34.55 |
| Generalización | 10 % | cGAN | 0.07785 | 43.64 |
| Generalización | 50 % | Entrada | 0.04010 | 18.64 |
| Generalización | 50 % | cGAN | 0.15759 | 50.00 |

En el soporte común de contraste (21 combinaciones en prueba y 11 en generalización), la cGAN al 5 % reduce el error absoluto respecto de la entrada de 0,17073 a 0,07557 en prueba y de 0,15881 a 0,07864 en generalización. Sin embargo, la proporción ponderada de inversiones de signo aumenta de 38,12 % a 43,54 % y de 40,00 % a 44,09 %, respectivamente. No son porcentajes de volcanes detectados, sino frecuencias descriptivas respecto del signo de la referencia sobre las realizaciones y casos incluidos.

También al 5 %, el error absoluto de SNR espacial frente a la referencia disminuye de 0,64966 a 0,18043 en prueba y de 0,65088 a 0,09720 en generalización. En cambio, el error de CNR aumenta de 0,05672 a 0,06458 y de 0,07090 a 0,08251. Los soportes de SNR y CNR son diferentes y se publican explícitamente. La mejora de un indicador no demuestra preservación uniforme de las anomalías.

La primera versión del comparador local trató los vectores almacenados dentro de celdas CSV como texto y se detuvo ante diferencias de redondeo. Se corrigió únicamente su lectura como listas numéricas y se mantuvo la tolerancia. No se cambiaron el evaluador científico, las predicciones ni las tablas entregadas.

El error de contraste es |C_N,pred − C_N,ref| y es adimensional. La inversión de signo se cuenta cuando su producto es estrictamente negativo, sin añadir después un umbral para eliminar desacuerdos. Las cifras son descriptivas: una referencia próxima a cero puede volver sensible la clasificación de signo. Un SNR espacial alto puede reflejar suavizado y menor dispersión, por lo que se interpreta junto con error, signo y cuentas, sin atribuirle una probabilidad de detección.

La [metodología ejecutable y los soportes](evidencias/revision-complemento-c1/metodo_sintesis.json) acompañan la tabla. El contraste comparado es de transmisión en cuentas: no se reconstruye opacidad X = integral rho(l) dl. Los cocientes de cuentas no tienen las unidades de X y no pueden convertirse en densidad sin una relación de transmisión/calibración explícita.

## Estado de pendientes y siguiente decisión

| Pendiente | Estado tras esta revisión | Evidencia y límite |
|---|---|---|
| OE3-P01 | verificado | Curvas descriptivas originales conservadas. |
| OE3-P02 | parcial | Benchmark operativo documentado y aplicado sin relajarlo; no acredita aceptación física ni predefinición original. |
| OE3-P05 | verificado | Evaluación multifracción de los ocho pesos existentes, integridad y reproducción local. |
| OE3-P06 | parcial | SNR/CNR y contraste de cuentas calculados y revisados. Persiste la diferencia entre este indicador sustituto y contraste cuantitativo de opacidad. |
| OE3-P03 | parcial | Pregunta del benchmark resuelta con resultado negativo: no se demuestra reducción bajo su regla. No se ha demostrado un factor físico positivo. |
| OE3-P04 | pendiente | Libro/informe final aplazado por indicación de la dirección. |

La ejecución y auditoría de **este complemento** pueden darse por terminadas. No corresponde declarar automáticamente pleno cumplimiento del objetivo 3 ni afirmar un factor positivo. Tampoco se recomienda encargar otro entrenamiento o repetir inferencias solo porque el resultado sea desfavorable.

La siguiente decisión es metodológica: registrar el alcance logrado y la desviación respecto del contraste de opacidad previsto. Si se exige esa magnitud cuantitativa, debe definirse una calibración o inversión apropiada, con entradas y criterio físico explícitos, como trabajo diferente de este complemento. No se exige una campaña de campo que la propuesta no estableció. La entrega actual permite documentar los límites del modelo sin continuar indefinidamente la búsqueda de un resultado favorable.

## Fuentes y reproducción

- [Entrega original](entregas/2026-10-04-complemento-oe3-f05/RESULTADOS_COMPLEMENTO_OE3.md).
- [Distribución de Drive](https://drive.google.com/drive/folders/12RB9qJ32WjUWGFBQRxuvIiZ7szTM9IbO).
- [Integridad de archivos](evidencias/revision-complemento-c1/integridad.json) y [comparación de reproducción](evidencias/revision-complemento-c1/reproduccion.json).
- [Guía de inferencia y evaluación](INSTRUCCIONES_COMPLEMENTO_OE3.md), que conserva el procedimiento original.
- [Auditoría y síntesis](herramientas/auditar_complemento_c1.py) y [figura](herramientas/figura_complemento_c1.py).

Para reproducir esta revisión, verificar primero los SHA-256 de `manifiesto.sha256` y `binarios.sha256` de la descarga, ejecutar `evaluate` con el código congelado y un directorio de informe nuevo según la guía y comparar ambos informes:

```bash
python objetivo-3/herramientas/auditar_complemento_c1.py \
  --reported /ruta/descarga/informe --reproduced /ruta/reproduccion \
  --config objetivo-3/configuraciones/complemento-v1.json \
  --output /ruta/revision
python objetivo-3/herramientas/figura_complemento_c1.py --directory /ruta/revision
```

La comparación numérica usa tolerancias absoluta y relativa de 10⁻¹⁰ para diferencias entre entornos; no son márgenes de calidad científica. Identidades, estados, exclusiones y filas deben coincidir. Las matrices grandes permanecen fuera de Git y se conservan mediante inventarios y huellas.

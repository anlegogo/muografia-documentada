# Cierre experimental y documental del objetivo específico 3

Fecha: 2026-10-04, Colombia. Base revisada: `d7c865a78a30f030ba0633bbc50fb0b6155e2143`.

**Estado vigente: ejecución y revisión experimental cerradas; cumplimiento científico parcial, con resultado negativo para el benchmark y limitaciones explícitas.** Se atiende la solicitud de la dirección de concluir el trabajo realizable con la evidencia disponible. No se declara cumplimiento pleno de la propuesta, aprobación institucional ni demostración de un factor físico positivo.

## Objetivo evaluado

La [propuesta aprobada y su revisión](../docs/REVISION_PROPUESTA_APROBADA.md) establecen:

> Evaluar el desempeño del modelo entrenado y determinar el factor de reducción del tiempo de adquisición alcanzable con el esquema propuesto, comparando la calidad de las imágenes mejoradas por el modelo frente a imágenes obtenidas con tiempos de exposición prolongados.

La evaluación se completa para los ocho modelos congelados y las cuatro fracciones disponibles. La ausencia de una fracción aceptada se informa como resultado; no se modifica el criterio para obtener un factor favorable.

## Evidencia definitiva

| Componente | Evidencia | Resultado |
|---|---|---|
| Modelos y ejecución | [Protocolo OE3-C1](PROTOCOLO_COMPLEMENTO_OE3.md), código `39d8fd3e398a540ea42e025fce8c42fa25986dfa`; entrega `5c3b0ee6cc305d13b34f70b19c82c63489794206` | Ocho pesos entrenados/continuados al 5 %, evaluados al 1 %, 5 %, 10 % y 50 %. No equivale a entrenar para cada fracción. |
| Integridad y reproducción | [Auditoría](REVISION_COMPLEMENTO_OE3_C1.md), [integridad](evidencias/revision-complemento-c1/integridad.json), [reproducción](evidencias/revision-complemento-c1/reproduccion.json) | 96 matrices nuevas, 11.520 predicciones; 3.840 predicciones al 5 % reutilizadas. Métricas reproducidas, diferencia absoluta máxima 7,105 × 10⁻¹⁵. |
| Calidad por vista | [768 comparaciones](evidencias/revision-complemento-c1/benchmark_por_vista.csv) | Ninguna satisface conjuntamente SSIM y PSNR del referente sin red al 50 %. |
| Métricas locales | [Síntesis y soportes](evidencias/revision-complemento-c1/metodo_sintesis.json), [tabla](evidencias/revision-complemento-c1/sintesis_metricas.csv) | SNR, CNR y contraste de cuentas calculados; mejoras y deterioros documentados, sin conservación uniforme de anomalías demostrada. |
| Opacidad | [Diagnóstico nominal](OPACIDAD_NOMINAL_Y_ALCANCE.md) | 54 filas, 48 elegibles; referencia geométrica nominal, sin reconstrucción cuantitativa de opacidad desde las predicciones. |

Las tres geometrías de prueba y la única de generalización se mantienen separadas. Las veinte realizaciones por vista no se consideran veinte geometrías independientes. Las referencias tienen estadística finita y se comparten entre realizaciones.

## Factor de reducción: resultado y significado

Sea F = {0,01; 0,05; 0,10; 0,50}. Para cada modelo m y vista v se verifica simultáneamente:

SSIM(m,f,v) ≥ SSIM(entrada,0,50,v), y PSNR(m,f,v) ≥ PSNR(entrada,0,50,v),

usando las medias de las veinte realizaciones y las definiciones congeladas. Una fracción aceptada para una partición debe satisfacer ambas desigualdades en todas sus vistas. Si el conjunto de fracciones aceptadas no es vacío, se define f_min como su mínimo muestreado y R = 0,50/f_min, bajo proporcionalidad entre conteos y exposición.

El conjunto es vacío para todos los modelos: **f_min y R se conservan nulos/no demostrados**. No son cero ni uno; tampoco se deducen 20× de la entrada al 5 %. No se interpola entre fracciones ni se concluye imposibilidad para cualquier otra arquitectura, entrenamiento o conjunto de datos.

El benchmark es una convención operativa declarada después de conocer resultados históricos y antes de las inferencias nuevas. No constituye un umbral numérico original de la propuesta ni una aceptación geofísica independiente.

La comparación descriptiva cGAN al 5 % frente a entrada al 10 % sigue siendo favorable en SSIM/PSNR en las 24 vistas. Su razón nominal 2:1 se conserva como comparación de métricas, sin sustituir el resultado negativo frente al referente al 50 % ni acreditarse como reducción física aceptada.

## Alcance físico y desviaciones que quedan registradas

El [producto adoptado del OE1](../objetivo-1/DEFINICION_PRODUCTO_OE1.md) y su [ficha](../objetivo-1/FICHA_CONJUNTO_OE1.md) describen conteos direccionales sintéticos. La receta conserva fuente no calibrada instrumentalmente, exposición convencional y referencia ideal sin transporte. El cierre no exige una campaña de campo adicional que la propuesta no estableció, ni convierte las etiquetas de exposición en días físicos.

La revisión de la receta identifica código base, parche y huella de binario reportado, pero no reconstruye localmente ese binario ni acredita la densidad efectiva de cada material de producción. En el diagnóstico de opacidad permanecen señaladas seis filas de la anomalía 2 de `geo-gen-01`: el catálogo declara 0,048 g/cm³ y el constructor conservado sustituye densidades menores de 0,05 por G4_AIR. No se equipara esa densidad nominal con la efectiva del transporte. No se atribuye a este hallazgo el deterioro de las redes ni se ordena repetir la campaña.

El contraste de cuentas C_N = μ_A/μ_B − 1 es adimensional. La opacidad X = ∫ρ(l) dl tiene unidades de g/cm². El cálculo nominal de X a partir del catálogo no prueba que el modelo recupere X. La evaluación cuantitativa de opacidad prevista en la metodología permanece **parcial**: se dispone de indicadores de cuentas y referencia geométrica, pero no de una inversión validada. Esta desviación queda explícita en el cierre; no se resuelve cambiando el nombre del indicador.

La cGAN al 5 % reduce el error de contraste de cuentas, pero aumenta la frecuencia descriptiva de inversiones de signo y el error de CNR en los soportes comunes. Una mejora global de similitud o del SNR espacial no permite afirmar preservación general de detectabilidad.

## Disposición final de los pendientes

Se distingue el estado de evidencia del estado operativo. Finalizar una actividad no convierte un resultado parcial en cumplimiento científico pleno.

| ID | Estado de evidencia | Disposición al cierre |
|---|---|---|
| OE3-P01 | verificado | Curvas y comparaciones disponibles; actividad terminada. |
| OE3-P02 | parcial | Benchmark aplicado y su carácter posterior declarado. Sin umbral físico validado; limitación documentada, sin reajuste para obtener éxito. |
| OE3-P03 | parcial | Pregunta operativa resuelta con resultado negativo; factor positivo y mínimo aceptable no demostrados. No se agenda otra corrida para forzar un factor. |
| OE3-P05 | verificado | Evaluación multifracción recibida, íntegra y reproducida; actividad terminada. |
| OE3-P06 | parcial | Métricas locales y diagnóstico nominal terminados; inversión de opacidad no realizada. Se registra como limitación y trabajo futuro, no como compromiso cumplido. |
| OE3-P04 | pendiente | Integración y redacción del informe final; tarea editorial posterior, separada del cierre experimental. |

Este registro sustituye las instrucciones operativas anteriores de continuar preparando o repitiendo OE3-C1. Los documentos y entregas históricos se conservan con su fecha; sus pendientes no constituyen nuevos encargos vigentes.

## Continuidad para estudiantes y documento final

No queda asignada otra simulación, entrenamiento o inferencia dentro del protocolo cerrado. Corresponde conservar los paquetes de datos, pesos y predicciones identificados por sus manifiestos e incorporar al informe las tablas, figuras, metodología y conclusiones ya revisadas. El presente registro no afirma que esa integración editorial ya esté realizada ni que la tesis esté aprobada.

La conclusión que debe preservarse es: **se evaluó el desempeño de los modelos y se delimitó su aplicabilidad; se observaron mejoras de similitud a baja estadística, pero no se demostró un factor de reducción bajo el benchmark adoptado ni equivalencia cuantitativa de opacidad.**

Una nueva investigación sobre calibración/inversión o entrenamiento multifracción requeriría una pregunta y protocolo propios. No se considera una condición para volver a ejecutar indefinidamente el complemento concluido.

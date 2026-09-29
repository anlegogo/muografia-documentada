# Alcance del OE1

## Objetivo aprobado

> Generar un conjunto de datos sintéticos de imágenes muográficas por transmisión, con diferentes niveles de estadística de conteo, mediante simulación Monte Carlo que reproduzca escenarios representativos de exploración volcánica.

Fuente: `Plan_trabajo_grado.pdf`, página física 11 / impresa 9, conservado en la carpeta de trabajo superior. Esta transcripción no modifica el plan.

## Incluido

Geometrías volcánicas; flujo y generación de muones; transporte y formación de histogramas; campaña sintética; reducción de conteos; construcción y partición del conjunto de datos; metadatos, integridad y controles de simulación. Se incluye el motor analítico como antecedente identificado.

## Límite de esta incorporación

No se incorporan entrenamiento de redes, pesos ni evaluación comparativa de modelos. Los nombres train/val/test/generalization se conservan porque identifican la partición del conjunto de datos. El módulo de acceso/preprocesamiento alojado originalmente en `scripts/training/` es una dependencia de la generación de pares.

## Criterios de seguimiento

La [matriz](MATRIZ_CUMPLIMIENTO.md) descompone el objetivo en verificaciones prácticas; no añade requisitos oficiales. Distingue existencia de datos, consistencia del conjunto y validez física. No exige datos de campo para un objetivo formulado en términos de simulación.

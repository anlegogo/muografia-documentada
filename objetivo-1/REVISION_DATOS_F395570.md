# Revisión directa de datos — f395570

2026-10-03, Colombia. Se descargó la nueva entrega de la rama estudiantil sin fusionarla en main. Incluye los 114 histogramas fusionados, sus metadatos, las 114 imágenes NPZ, manifiestos de pares, huellas de contenido y un enlace de Drive.

## Resultado verificado

- **477 huellas coinciden:** 248 archivos de fusión y 229 de imágenes, contra los inventarios anteriores. Se usaron los bytes de `git archive f395570`, evitando cambios de finales de línea.
- Se repitió `evaluar_campana_114.py` desde los histogramas con el plan, receta y máscaras congelados. Coinciden estructura, decisiones y valores; diferencia máxima entre flotantes 4,97 × 10⁻¹⁴ frente a tolerancia 10⁻¹⁰. Las 114 referencias son técnicamente completas.
- Las 114 imágenes NPZ preservan exactamente los conteos uint32 y las coordenadas de los histogramas.
- Se regeneraron **9.120 pares en memoria**, con NumPy 2.4.4 y semilla maestra 20260805. Coinciden las 342 huellas de contenido publicadas: referencia, conteos reducidos y fracciones para cada una de las 114 vistas. Se comprobaron formas, tipo uint32 y ausencia de conteos reducidos mayores que su referencia. Esta comprobación no afirma identidad de los archivos comprimidos de Drive.
- Las particiones se conservaron por geometría: 12 de entrenamiento, 3 de validación, 3 de prueba y 1 de generalización. Las realizaciones de cada referencia permanecen en su partición; comparten la incertidumbre de la referencia finita.
- Desde los píxeles se confirman **1.710 regiones de borde dentro del criterio** y **107/114 vistas que cumplen la meta descriptiva de roca**. Las siete restantes son las ya documentadas; no se eliminaron ni se propone ampliar N para cruzar la meta.
- Globalmente, **20.713 de 21.816 ROI** alcanzan 100 cuentas: **94,944 %**. Este porcentaje agregado no sustituye el indicador por vista ni convierte las siete excepciones en cumplimientos.

[Verificación y huellas de contenido](evidencias/revision-datos-f395570/verificacion.json) · [Evaluación completa desde los píxeles](evidencias/revision-datos-f395570/evaluacion-local.json).

## Alcance de esta comprobación

Se verificó el producto de conteos y su reproducción determinista bajo el alcance idealizado del OE1. No se reejecutó Geant4 ni se demostró equivalencia con un detector real. Las condiciones de fuente, transporte y referencia ideal mantienen sus limitaciones documentadas.

El [enlace de Drive publicado por estudiantes](https://drive.google.com/drive/folders/10gRmkWqmCqN3qOf2gfOWCDG4bcC7zhaT) queda localizado, pero no se descargó ni se comprobaron sus permisos o bytes. No fue necesario para reproducir los pares desde las referencias de Git. No se ha auditado la conversión `dataset-v2` ni el código de otro repositorio: reentrenar modelos queda fuera del OE1.

La afirmación de reproducción en otra máquina se recoge como reportada por estudiantes; adicionalmente se realizó la regeneración local aquí descrita. Los pares completos no se guardaron de nuevo en disco durante esta revisión: se regeneró y verificó cada matriz en memoria contra las huellas esperadas.

## Actualización de pendientes

Quedan resueltas la recepción de matrices, su evaluación directa y la comprobación de reproducibilidad de los 9.120 pares. No se necesita solicitar otra vez estos datos ni otra campaña para esas verificaciones.

El siguiente trabajo es consolidar la ficha final del conjunto y el informe académico: procedencia, receta efectiva AMD, particiones, interpretación de las imágenes y excepciones de calidad. Debe comprobarse también la copia de distribución si se va a utilizar Drive como archivo de entrega. La representatividad académica y el cierre formal del OE1 no se sustituyen por los controles de integridad.

La sección «Siguiente paso» del informe estudiantil aún dice formar los pares, mientras el cuerpo del mismo documento ya informa su generación y reproducción. Se recomienda actualizarla a revisión y cierre documental del conjunto. No se modifica el documento original de estudiantes.

## Procedimiento reproducible

Entorno: Python 3.12.14, NumPy 2.4.4 y SciPy 1.18.1. Extracción: `git archive --format=zip f395570 objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/datos/sc3/campana-114`, descomprimida en `tmp/revision-f395570` del espacio de trabajo. Se usaron las herramientas de main sin modificar.

El [script de revisión](evidencias/revision-datos-f395570/revisar_f395570.py) registra el procedimiento. Para repetirlo, copiarlo a `tmp/revisar_f395570.py` junto a la extracción indicada y ejecutarlo con el entorno local del proyecto. Produce `tmp/revision-f395570-verificacion.json` y `tmp/revision-f395570-evaluacion.json`. La huella de cada arreglo concatena `dtype.str`, la representación de su forma y los bytes contiguos en orden C, según la convención publicada; no depende de la compresión ZIP.

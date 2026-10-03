# Revisión de la campaña reportada en e037d09

2026-10-03, Colombia. Se revisó la rama estudiantil `oe1/justificacion-fisica-produccion`, commit `e037d09`. La campaña reportada contiene 114 vistas de 344 M de primarios: 39.216 M en total. Se conserva el acuerdo de que el 90 % de ROI con 100 cuentas es una meta descriptiva, no una regla de eliminación ni de ampliación automática.

## Evidencia comprobada

- Se verificaron las 25 huellas de `salidas.sha256` sobre los bytes extraídos mediante `git archive`.
- Los registros `sacct` contienen 1.029 trabajos de campaña: 1.026 completados con código 0:0 y tres fallidos, filas 120–122. Cada una de las 1.026 filas tiene exactamente una ejecución completada. Los autores atribuyen los fallos a cuota de `/home`; esa causa se recoge como reportada, no como diagnóstico local del clúster.
- Intervalo de ejecución: 2 de octubre 18:10:27 a 3 de octubre 09:48:49, aproximadamente 15 h 38 min. La suma de tiempo asignado × hilos, incluyendo los tres fallos, es 2.356,73 hilo-horas. No se equipara automáticamente a núcleos físicos ni al rendimiento de legacy.
- El JSON contiene 114 combinaciones únicas de geometría/vista, sin errores ni faltantes declarados. El inventario declara 114 NPZ y 9.120 pares objetivo; **los pares aún no están generados**.
- Se recalcularon los 1.710 intervalos de borde mediante cuantiles beta a partir de los conteos regionales reportados, con α=0,05/(114×16). Coinciden con tolerancia absoluta 10⁻¹⁰; todos quedan dentro de ±1 pp. Máximo extremo absoluto: 0,932696 pp.
- Coinciden las referencias de hashes de los histogramas/metadatos del evaluador con el inventario de fusión. Esto comprueba coherencia de los informes, no sustituye verificar los archivos originales.
- Se ejecutó la suite de la rama extraída: **107 pruebas satisfactorias**, Python local, sin conexión SC3. Las pruebas cubren las funciones ensayadas; no certifican por sí solas la ejecución paralela real o la visibilidad NFS.

[Verificación estructurada](evidencias/revision-campana-e037d09/verificacion.json) · [Salida de las pruebas](evidencias/revision-campana-e037d09/pruebas.txt).

## Meta de roca

El informe registra 107/114 vistas con al menos 90 % de ROI nominales 4×4 que alcanzan 100 cuentas. Las restantes son:

| Geometría | Vista | Porcentaje reportado |
|---|---:|---:|
| geo-test-03 | 1 | 89,64 % |
| geo-test-03 | 5 | 89,19 % |
| geo-train-06 | 3 | 89,34 % |
| geo-train-09 | 1 | 89,81 % |
| geo-train-09 | 4 | 89,81 % |
| geo-train-09 | 5 | 89,32 % |
| geo-train-12 | 2 | 89,74 % |

Estos resultados son coherentes con conservar todas las imágenes bajo el acuerdo registrado. No se recomienda repetir la campaña ni ampliar esas vistas solo para cruzar el 90 %. La comparación de la mediana global del catálogo con la proyección previa del piloto debe interpretarse con cuidado: aquella proyección correspondía únicamente a geo-train-06, no al promedio de las 19 geometrías.

## Cambios operativos

La rama añade opciones de partición, tiempo y memoria al lanzador, verificación paralela de bloques y una ruta explícita para mantener el worker de la réplica original. Se inspeccionó el diff: no modifica el evaluador, la receta física ni el worker de transporte respecto a la preparación de main. El ciclo v5 tolera bloqueos transitorios durante tres pasadas; no vuelve a enviar automáticamente una fila que conserva un registro previo. La rama no se fusionó en main ni se alteraron sus evidencias.

La portabilidad AMD y la identidad de histogramas de una prueba corta se reportan en el acuerdo estudiantil. La presente revisión no reejecuta Geant4 ni extiende esa observación a identidad binaria universal entre procesadores/hilos.

## Lo que falta para cerrar la revisión

En esta entrega se encuentran los informes y hashes, pero no los 114 histogramas fusionados ni los 114 NPZ de la campaña. Sus ubicaciones SC3 están declaradas: `oe1-114-344M-fusion` (~32 MB) y `oe1-114-344M-imagenes` (~11 MB). Se requiere compartir ambas carpetas completas, con metadatos, `entradas.sha256` y los informes existentes, mediante la rama o un archivo recuperable con huella. No se necesitan nuevas simulaciones para ello.

Con esos archivos se podrá verificar cada hash y repetir la evaluación desde los píxeles, confirmar las siete vistas y auditar la exportación. Después corresponde generar y verificar los 9.120 pares, preservar las particiones por geometría y completar la ficha de datos y el informe del OE1. No usar `target_pairs: 9120` como evidencia de que los pares ya existen.

La propuesta estudiantil de convertir al formato de entrenamiento y reentrenar no se incorpora a esta tarea: el trabajo autorizado continúa limitado al OE1. La revisión no declara cerrado el objetivo ni validación física completa.

## Reproducción

Se extrajeron `herramientas`, `objetivo-1/evidencias`, `objetivo-1/contratos` y la evidencia SC3 desde `e037d09` a una carpeta de revisión separada. Comando de pruebas: `python -m unittest discover -s RUTA_EXTRAIDA/herramientas -p 'test_*angular*.py' -v`. Los intervalos se reconstruyeron con `scipy.stats.beta.ppf`, las sumas de asignación con los registros `sacct` filtrados por trabajos `oe1-`, y las huellas con SHA-256 sobre bytes Git. No se evaluaron matrices ausentes ni se modificaron resultados de estudiantes.

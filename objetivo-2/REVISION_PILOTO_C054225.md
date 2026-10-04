# Revisión del piloto OE2 al 5 % — c054225

> **Actualización 2026-10-03:** ya se recibieron y verificaron los dos pesos seleccionados y se reprodujo su inferencia. Véase la [revisión posterior](REVISION_PESOS_PILOTO_F05.md), que también matiza la alerta visual de la zona candidata. El texto siguiente conserva el estado histórico de la primera revisión.

**2026-10-03. Resultado: registros del piloto coherentes y ejecución GPU documentada; calidad física e inferencia independiente pendientes.** No procede ampliar automáticamente a la campaña de 24 entrenamientos.

Se revisó la rama `oe2/piloto-f05`, commit c054225, con la [entrega estudiantil](https://github.com/anlegogo/muografia-documentada/blob/c054225/objetivo-2/entregas/2026-10-03-piloto-f05/RESULTADOS_PILOTO_F05.md). La rama solo añade la entrega, sin modificar el código del protocolo. No se fusionó en `main`; esta revisión conserva su procedencia.

## Comprobaciones independientes

- 110/110 huellas coinciden con los objetos originales de Git. La extracción local mediante `git archive` convirtió finales de línea de 67 archivos; se contrastaron los bytes del commit y se confirmó que no existe discrepancia en el repositorio. No se corrigieron ni sustituyeron originales.
- Las cuatro configuraciones coinciden con las publicadas; coinciden las identidades de implementación, normalización, manifiesto y ejecutor UTF-8. La configuración también reproduce su huella `config_sha8`.
- Los registros y sus copias en `record/` coinciden; épocas, número de pasos, tamaños de validación y métricas finitas son coherentes. Los ocho códigos de salida entregados son cero.
- Etapa técnica: dos épocas por método, con una interrupción registrada por `stop_file` y posterior finalización. No se inspeccionaron los estados internos de los checkpoints porque aún no están distribuidos.
- Etapa piloto: 12 épocas U-Net y 13 cGAN, ambas terminadas por parada temprana. La mejor época declarada es 5. El redondeo de la curva U-Net muestra empate entre épocas 5 y 7; sin pesos ni valores internos completos no se verifica nuevamente la selección estricta. Los promedios del CSV coinciden con el mejor valor registrado.
- CSV: 360 pares únicos, tres geometrías, seis vistas por geometría y veinte realizaciones por vista. Se reprodujeron medias, diferencias, resultados por geometría y los intervalos bootstrap publicados.
- Se recalcularon SSIM y PSNR de la entrada sin red sobre los 360 pares locales: diferencia absoluta máxima con el CSV igual a cero. Las columnas de predicciones se verifican aritméticamente, pero su inferencia no se repitió.

[Evidencia JSON](evidencias/revision-c054225.json) y [procedimiento reproducible](herramientas/revisar_entrega_piloto.py). No se ejecutaron scripts de la entrega ni se abrieron imágenes de test/generalization.

## Resultado numérico

| Método | SSIM medio val | PSNR medio val, dB | Épocas | Tiempo de sesión reportado |
|---|---:|---:|---:|---:|
| Entrada sin red | 0,751812 | 24,1677 | — | — |
| U-Net L1 | 0,843671 | 32,9037 | 12 | 200,6 s |
| cWGAN-GP | 0,822792 | 31,1041 | 13 | 1.134,0 s |

Ambas redes mejoran la entrada en las métricas definidas; la cGAN queda 0,020879 puntos de SSIM y 1,799573 dB de PSNR por debajo de la U-Net. La ordenación aparece en las 18 referencias y en las tres geometrías. Corresponde a una semilla y a selección sobre validación; no es un resultado de prueba independiente ni una superioridad universal de arquitectura.

El bootstrap recibido agrupa las veinte realizaciones por referencia, lo que evita tratarlas como imágenes independientes. Sin embargo, las seis vistas de una misma geometría también comparten escenario: remuestrear 18 referencias no representa íntegramente esa dependencia. Los intervalos se reproducen, pero deben leerse como descriptivos condicionados a esas referencias y esa semilla. No deben utilizarse como evidencia de generalización a otras geometrías; tampoco corrigen el efecto de haber seleccionado el checkpoint con esta misma validación.

## Entorno y desviación declarada

La ejecución se realizó en RunPod, con dos NVIDIA L40S y PyTorch 2.6.0+cu118; no en SC3. Se reporta indisponibilidad de GPU y cuota limitada en SC3. El código se extrajo mediante `git archive`, por lo que `git_commit` aparece como `unknown`; la huella de implementación y el commit de procedencia documentado permiten contrastar la versión.

Se considera evidencia del funcionamiento en ese entorno CUDA. **No verifica instalación, rendimiento ni disponibilidad de SC3.** Los tiempos no se deben extrapolar directamente a las Titan X. La ejecución simultánea de los dos métodos se realizó, según los registros, en GPU distintas y directorios separados, sin cambio de lote o configuración.

## Imágenes y límites de la interpretación

Se inspeccionaron las figuras U-Net de épocas 5 y 10 y cGAN de época 5. En U-Net se observan bandas en la región inferior y un punto oscuro evidente en época 10, más tenue en la época 5 seleccionada. Es un indicio que debe examinarse sobre arreglos numéricos y varias vistas, no una identificación física confirmada. La figura de época 10 no corresponde al checkpoint seleccionado.

La cGAN presenta textura granular y no muestra ese punto evidente en los ejemplos inspeccionados. La apariencia de textura no demuestra recuperación de señal física. No basta atribuir su peor SSIM a ruido no coincidente: esa explicación requiere comprobar predicciones, residuos y regiones. Las figuras solo muestran cuatro realizaciones de una vista de geo-val-01; no permiten certificar ausencia de artefactos en todo el conjunto.

## Pendientes antes de ampliar

1. **OE2-P04a — Distribución de pesos: pendiente.** Se entregaron huellas y tamaños de ocho archivos, pero el informe indica que el enlace de Drive se añadirá después. Se requieren al menos los dos `best.pt` del piloto para repetir inferencia; conservar y distribuir también los demás checkpoints conforme al protocolo.
2. **OE2-P04b — Verificación independiente de predicciones: pendiente de pesos.** Comparar huellas, contrato, normalización y estados; reproducir métricas en val y revisar las vistas completas. No abrir test/generalization para decidir ajustes.
3. **OE2-P04c — Evaluación regional y artefactos: pendiente.** Definir regiones y medidas de contraste/residuo en coordenadas originales, con reglas fijadas antes de comparar ajustes; examinar la posible estructura artificial y la conservación de señales. No declarar superioridad física por suavidad o textura.
4. **OE2-P04d — Diseño principal y presupuesto: pendiente.** Decidir si conviene ajustar el componente adversario, repetir semillas o modificar el protocolo una vez completada la revisión. La campaña de 24 entrenamientos permanece propuesta, sin inicio automático.

Se adopta la lectura prudente de los estudiantes: funcionamiento técnico documentado, mejora de imagen según las métricas usadas y aporte adversario aún no demostrado. El objetivo 2 permanece abierto; el cierre del objetivo 1 no cambia.

## Reproducción local

Extraer la carpeta de entrega del commit c054225 en una ubicación de trabajo, conservar los datos locales verificados y ejecutar desde la raíz de la réplica:

```powershell
python objetivo-2/herramientas/revisar_entrega_piloto.py --entrega trabajo/revision-c054225/objetivo-2/entregas/2026-10-03-piloto-f05 --datos trabajo/drive-2026-10-03 --git-ref c054225 --salida trabajo/revision-piloto.json
```

La opción `--git-ref` comprueba huellas contra los bytes de Git y permite distinguir las conversiones locales CRLF/LF. La identidad del ejecutor se calcula con UTF-8 explícito, evitando diferencias debidas a la codificación predeterminada de Windows. El script no sustituye la verificación de pesos ni valida su disponibilidad a partir de una lista de huellas.

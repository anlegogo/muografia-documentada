# Revisión de la entrega de etapa 2 — 1 de octubre de 2026

**Actualización posterior del 1 de octubre:** [auditoría íntegra completada](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md). El contenido que sigue conserva el estado de la revisión preliminar o de las instrucciones originales; el seguimiento actual está en la auditoría completa.

**Estado: revisión documental, de código y de resultados agregados completada, con observaciones. Auditoría íntegra de registros grandes pendiente.** Entrega: rama `oe1/segundo-ensayo-etapa-2`, revisión `f88de14`; preparación `0135072`, resultados `3e23f3b`. Código de estudiantes: `d8ca749`, rama `oe1/stage2`. Se conserva la entrega sin fusionar ni modificar.

## Dictamen

El resultado confirmatorio **inconcluso** es coherente con el protocolo v1.1. Se reprodujo el agregado desde los 24 bloques entregados y se contrastaron independientemente los histogramas, conteos, filas seleccionadas e intervalo. Esto no equivale a releer los 48,7 millones de registros individuales.

La etapa proporciona evidencia útil: aparecen efectos de la corrección en la fuente representativa. No demuestra que el efecto sea despreciable ni justifica nuevas corridas automáticas. Es razonable preparar la producción corregida B, condicionada a completar auditoría de datos y controles pendientes de entorno, normalización y otras geometrías.

## Evidencia contrastada localmente

- Manifiesto de 1.061 archivos de la entrega: huellas verificadas. En 56 archivos de texto (`.gitattributes` y 55 `.status`) la extracción Windows convirtió LF a CRLF; concuerdan al normalizar LF. Sin normalización en CSV/JSON científicos.
- 55 metadatos e histogramas: 48,7 millones de transportes declarados; sus totales y conteos ROI concuerdan. Las verificaciones internas de metadatos son declaraciones del simulador, no sustituyen nuestra lectura de crudos. En control sin anomalías `variant_matches_geometry=null` es no aplicable, no un fallo.
- 24 bloques de un millón de pares; cuatro CSV agregados reproducidos byte a byte. Se regeneró el agregado con el código de autores y nuestro calculador.
- Mapas reconstruidos sumando los histogramas principales: A=18.053.098, B=18.053.099 detecciones; ROI=67/70. Las 23 celdas distintas cambian como máximo una cuenta. Las filas de diez cambios de píxel y tres cambios de detección explican exactamente el mapa diferencial.
- 151 filas seleccionadas de cruce, 51 etiquetadas desde conducto y 100 desde cuerpo denso según material en A. B asigna A1 dentro de 1 µm en las 151 filas recibidas. El lado real en B sigue sin observarse directamente con el registro agregado.
- Las 12 pruebas del analizador de estudiantes pasan localmente. Un primer intento falló por extracción local incompleta de las tablas de simulación; se incorporó `scripts/simulation` del mismo commit y se repitió sin modificar el código.
- [Auditoría propia](evidencias/revision-resumen-etapa2-f88de14.json): 1.247 controles satisfactorios en este alcance limitado.

## Resultado principal

| Magnitud | Recalculada |
|---|---:|
| Pares principales | 24.000.000 |
| n00 / n01 / n10 / n11 | 23.999.929 / 4 / 1 / 66 |
| Diferencia neta ROI | +3 cuentas |
| Delta por millón de primarios | +0,125 |
| Intervalo conservador 95 %, por millón | [−0,229200; +0,469439] |
| Margen prefijado, por millón | ±0,273660 |
| Decisión según v1.1 | Inconcluso |

El intervalo no está dentro del margen ni completamente fuera de él. «Pequeño» solo puede describir la estimación puntual con su unidad y referencia; no presentar el efecto como demostrado irrelevante. La escala histórica de 30 días sigue siendo una referencia de conteo, pendiente de justificación de normalización temporal en P-04.

## Observaciones para corregir en el informe

**E2-01 — No confundir ausencia de discordancia seleccionada con identidad física.** `discordance_table` compara únicamente `detected`, `status`, `iel`, `iaz`, `in_rint` y `rng1`. No compara materiales, longitudes ni energías. Por eso «37 solo cambian rng1» significa solo dentro de esas seis columnas.

Contraejemplo ya presente en su CSV: réplica 120, ID 212035, clasificado fuera de las 50 discordancias. En A recorre ~37,206 m como A0 y sale de Z con ~18,508 GeV; en B recorre ~37,198 m como A1 y sale con ~6,117 GeV. Ambos terminan DECAY y no son detectados. No es un muón físicamente idéntico, aunque no cambie la clasificación final. Corregir la celda «1 idéntico» del grupo conducto y limitar las afirmaciones de igualdad/ausencia de cambios al conjunto de campos efectivamente comparado. Esto no altera los cinco cambios de pertenencia a ROI ni su intervalo.

**E2-02 — Separar energía de salida y pérdida dentro de Z.** Al recalcular las 51 filas de entrada desde conducto, B tiene menor energía de salida en 43; al comparar `(Ein−Eout)B−(Ein−Eout)A`, tiene mayor pérdida en 45 y menor en 6 (tolerancia 10⁻⁹ GeV). La frase «B pierde más en 43 y menos en 7» no representa esa magnitud ni cubre las 51 filas. Corregir cálculo/denominador y conservar el carácter interpolado de energías de borde.

**E2-03 — Registrar la desviación operativa como tal.** No se cumplió la condición literal de disponer de 30 GiB persistentes: los estudiantes documentaron tmpfs, exportación por archivos, descarga con SHA y concurrencia por nodo. El cambio está explicado antes del transporte y no demuestra por sí mismo alteración científica, pero no debe marcarse como cumplimiento literal de ese requisito. La carpeta compartida de Drive es accesible y contiene archivos grandes; la preservación íntegra debe verificarse antes del cierre técnico. Para producción definitiva fijar retención y espacio efectivos sin depender de un único ejemplar temporal.

## Qué está comprobado y qué falta

**Comprobado aquí:** coherencia de archivos Git, histogramas, tablas seleccionadas, agregado, intervalo y pruebas del analizador. Los registros SLURM aportan evidencia de finalización de trabajos y del orden controles→principal.

**Reportado por estudiantes, pendiente de auditoría integral propia:** integridad y correspondencia evento a evento de las 27 listas y los 55 registros completos. La entrega enlaza 85 archivos grandes, aproximadamente 6,69 GB comprimidos, fuera de Git. Se verificó acceso a la carpeta mediante Google Drive; esta revisión no los descargó ni recalculó sus 85 hashes. No hay un bloqueo de acceso demostrado. Los controles A/A y A/B completos siguen respaldados por sus informes, no por una nueva comparación propia de cada fila.

## Siguiente paso hacia OE1

1. Resolver E2-01/E2-02 con el material ya disponible y verificar íntegramente los datos grandes. No requiere transporte nuevo.
2. Preparar producción con B: congelar entorno y scripts (P-02/P-03), justificar fuente/área/normalización (P-04), y revisar qué evidencia geométrica y física falta para los casos de recorte e intersecciones múltiples. No extrapolar geo-train-06/vista 0 a todo el catálogo.
3. La propuesta de regenerar seis geometrías por seis vistas es un alcance candidato de 36 imágenes de referencia. Reutilizar las 78 restantes exige evidencia de que su geometría y configuración son compatibles con la producción congelada; el control de geo-train-01 no certifica automáticamente las otras doce geometrías.
4. Regenerar las referencias afectadas y sus reducciones de conteo, verificar pares/metadatos y preservar las versiones históricas. La decisión final de producción se documenta antes de lanzar; esta revisión no inicia nuevas corridas ni cierra OE1/P-01…P-04.

## Reproducción de esta revisión

Extraer la entrega `f88de14` y `scripts/analysis` más `scripts/simulation` del código `d8ca749`. Usar Python local con numpy, pandas y scipy. Variables de ruta siguientes son marcadores:

```text
python CODIGO/scripts/analysis/oe1_stage2_analysis.py aggregate --blocks-dir ENTREGA/analisis/bloques --controls ENTREGA/analisis/controles.json --corridas REPO/objetivo-1/ensayos/etapa-2-v1.1/corridas.csv --calculator REPO/herramientas/planificar_etapa2_oe1.py --mask ROI --out REPRODUCCION_NUEVA
python REPO/herramientas/revisar_resumen_etapa2.py ENTREGA REPRODUCCION_NUEVA ROI SALIDA_JSON
```

Pruebas: configurar `OE1_STAGE2_CALCULATOR` con la ruta absoluta al calculador y ejecutar `python -m unittest discover -s CODIGO/scripts/analysis/tests -p test_oe1_stage2_analysis.py -v`.

El [auditor de resumen](../herramientas/revisar_resumen_etapa2.py) incluye explícitamente su limitación: no lee crudos grandes. La revisión no altera el diseño estadístico ni la entrega de los estudiantes.

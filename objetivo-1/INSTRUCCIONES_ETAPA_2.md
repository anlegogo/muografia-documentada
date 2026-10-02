# Qué hacer ahora: etapa 2 de OE1

**Actualización posterior del 1 de octubre:** [auditoría íntegra completada](AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md). El contenido que sigue conserva el estado de la revisión preliminar o de las instrucciones originales; el seguimiento actual está en la auditoría completa.

El complemento confirmó que la corrección cambia el material atravesado por los muones en los casos dirigidos a la zona problemática. El siguiente paso consiste en medir cuánto afecta eso a los conteos usando la fuente habitual de la simulación.

El [protocolo v1.1](PROTOCOLO_ETAPA_2_OE1_V1_1.md) fija el diseño y el [manifiesto](ensayos/etapa-2-v1.1/corridas.csv) identifica cada corrida. No hay que repetir toda la campaña de imágenes.

1. **Preparar el espacio y los scripts.** Se requiere una ubicación con al menos 30 GiB libres y cuota suficiente, conservando todos los registros. Confirmar cuánto tiempo permanecerán disponibles. Adaptar los scripts de etapa 1 al nuevo manifiesto, sin cambiar los binarios ni la fuente. Documentar esto en `PREPARACION_ETAPA_2.md` y guardar el commit antes de transportar.
2. **Generar y verificar las listas.** Son 24 listas de un millón de muones para el modelo 6, vista 0, y tres listas de 100.000 para el modelo 1 como control. Las semillas están fijadas. Cada lista se utiliza sin cambios en la versión anterior A y la corregida B.
3. **Corran primero los controles.** Son seis corridas A/B del modelo 1 y una repetición idéntica A/A. Verifiquen que no haya diferencias inesperadas ni registros faltantes. Si falla algo, conserven el intento y reporten el problema antes de seguir.
4. **Completar los 24 bloques principales en A y B.** Son 48 corridas del modelo 6. No son muones dirigidos como en el complemento. No aumentar ni reducir el tamaño según los resultados parciales.
5. **Entregar los resultados completos.** Comparar cuántos muones llegan a la región de interés en ambas versiones, cuántos solo en una y cuáles cambian de píxel. Incluir listas, registros, histogramas, tiempos, huellas y comandos o enlace verificable a los archivos grandes. El informe se llama `RESULTADOS_ETAPA_2.md`.

En total: **55 corridas y 48,7 millones de transportes**, porque cada muón principal pasa por las dos versiones. Se estiman unas **11,4 horas CPU de transporte** con el coste anterior, más preparación y análisis; la espera del supercomputador es aparte.

El resultado puede mostrar un cambio pequeño, un cambio relevante o resultar inconcluso. Los tres se reportan. El propósito es decidir con evidencia cómo actualizar los datos definitivos, sin seguir ampliando simulaciones automáticamente.

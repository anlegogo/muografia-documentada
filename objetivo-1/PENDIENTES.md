# Pendientes del OE1

Estado consolidado: 2026-10-03. Los histogramas y NPZ ya fueron recibidos; su evaluación se reprodujo y los 9.120 pares se regeneraron con contenido coincidente. La ficha, las figuras y la síntesis académica están preparadas. No se vuelve a solicitar una entrega ni una simulación ya verificadas.

| ID | Antes | Estado vigente y condición restante |
|---|---|---|
| P-01 · geometría y datos corregidos | Faltaban referencias compatibles con la malla y receta finales. | **Resuelto técnicamente:** 114 referencias nuevas y compatibles; no se reutilizaron por renombrado las históricas. [Revisión](REVISION_DATOS_F395570.md). |
| P-02 · entorno reproducible | Faltaba fijar y documentar la configuración de producción. | **Resuelto documentalmente para la campaña recibida:** entorno AMD, versiones, binario, tablas, manifiesto y semillas registrados en la [ficha](FICHA_CONJUNTO_OE1.md). No implica recompilación o ejecución Geant4 independiente local. |
| P-03 · reproducción de la cadena | Faltaban integración operativa, posproceso completo y niveles de conteo finales. | **Resuelto para las comprobaciones definidas:** registro de 1.026 bloques, evaluación de 114 matrices y 9.120 pares reproducidos. No requiere repetir piloto ni campaña. |
| P-04 · aceptación y normalización física | Faltaban definición de observable, evaluación de bordes y estadística de roca. | **Parcial:** alcance adoptado, bordes verificados y meta descriptiva documentada, incluidas siete excepciones. Falta incorporar la [síntesis](SINTESIS_RESULTADOS_OE1.md) al informe y revisar académicamente representatividad y limitaciones. La exposición sigue siendo convencional; equivalencia instrumental fuera del alcance. |
| P-05 · copia de distribución | Enlace Drive reportado, sin verificación de sus archivos. | **Resuelto para la copia revisada el 2026-10-03:** 753 archivos recuperados y 2.291 controles satisfactorios. [Verificación independiente](REVISION_DISTRIBUCION_DRIVE.md). Conservar inventarios y acceso al conjunto. |

## Próximo paso

Integrar la síntesis y las figuras al informe de estudiantes, conservar sus atribuciones y revisar la conclusión del objetivo a la luz del alcance idealizado. La dirección realiza la valoración académica; el software no declara validación física general. Drive ya se verificó de forma independiente. No se identifica otra corrida necesaria para cerrar estas comprobaciones.

La conversión dataset-v2 y el entrenamiento de redes no forman parte de este cierre del OE1. Los 9.120 pares comparten referencias finitas y no deben presentarse como simulaciones independientes de alta estadística.

Los estados anteriores están en la [bitácora](BITACORA.md), los informes fechados y el historial Git; se retiraron de esta página los avisos operativos vencidos. Esta actualización no altera originales, entregas ni recetas congeladas.

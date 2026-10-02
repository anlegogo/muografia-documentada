# Revisión de entrega: malla azimutal v1

Fecha de ejecución y revisión: 2026-10-01, Colombia (el entorno registra 2026-10-02 03:29 UTC, equivalente a 22:29 del día anterior en Colombia).

**Resultado: entrega conforme para la comprobación técnica solicitada.** La compilación y ejecución en SC3 quedan respaldadas por los registros recibidos; aquí reprodujimos el análisis de sus salidas y contrastamos código y huellas. No repetimos la compilación ni el transporte localmente.

## Entrega y resultado

- Rama de documentación: `oe1/malla-angular-v1-smoke`, commit `90abb96`, posterior a `9381bb5`. El último commit corrige el manifiesto de huellas; verificamos la versión corregida.
- [Informe de estudiantes](https://github.com/anlegogo/muografia-documentada/blob/90abb96/objetivo-1/entregas/2026-10-01-malla-angular-v1/RESUMEN.md).
- Código: `Dp100131/muography-dl-reconstruction`, rama `propuesta/malla-angular-v1`, commit `0dea8e1e1f8ad1e52ee2024e4c6c968748214a32`, derivado de `d8ca749`.
- SC3: trabajo SLURM 30616, nodo guane01, Geant4 11.4.2 y GCC 14.2.0 según entorno y log. SLURM registra COMPLETED 0:0, cinco segundos de trabajo; el simulador reporta aproximadamente 0,453 s de transporte.
- Caso: `geo-train-01`, vista 0, semilla 2026100107, un hilo. **1.000 primarios generados y transportados; 750 registrados en los píxeles.**

El histograma es 256×256, contiene enteros no negativos y suma 750, igual que los metadatos y el log. Los metadatos declaran `az-edges-v1`, paso 0,234375°, límites −30° y +30° y primer centro −29,8828125°. El código de salida real del simulador es cero. El log termina con RUN DONE y no contiene los patrones de error buscados; los controles de solapamiento del edificio y detector reportan OK.

Los 750 registros no son un valor esperado obligatorio ni una eficiencia instrumental validada. No asignamos una causa única a los otros 250 eventos sin información adicional. Esta muestra pequeña no debe producir necesariamente columnas uniformes tras transporte.

## Verificación independiente

El [revisor local](../herramientas/revisar_smoke_angular.py) reproduce exactamente el informe entregado: **24 controles, cero fallidos**. [Informe reproducido](evidencias/revision-angular-90abb96.json).

Además, [31 contrastes de integridad y procedencia](evidencias/contraste-angular-90abb96.json), todos satisfactorios:

- Las 14 huellas del manifiesto coinciden con los archivos en Git.
- Los diez archivos de código del parche coinciden byte a byte con las huellas preparadas por nosotros.
- La geometría y las tres tablas coinciden con las huellas de entradas declaradas en SC3.
- El cambio respecto de la base contiene únicamente los diez archivos del parche y las tres tablas nuevas.
- La referencia remota corresponde al commit declarado; el informe del revisor coincide con nuestra reproducción.

El ejecutable tiene huella reportada `a29e5277bc051823ab9a9eed387553914302b2e527d290d317be78b9a76e008b`. No recibimos ni ejecutamos ese binario: su correspondencia con el código compilado se apoya en la trazabilidad entregada, no en una compilación independiente.

Las seis pruebas Python constan satisfactorias en la entrega y ya habían pasado en nuestra preparación local. Se recibe ahora el resultado PASS de la prueba C++ que usa el mismo encabezado del contador: límites, centros, bordes, valores inválidos y 1.048.576 direcciones. Es evidencia de ejecución reportada por los estudiantes, no una prueba C++ realizada en nuestro equipo.

## Observación operativa menor

El script SLURM guarda correctamente el código del simulador, pero su último `echo` puede hacer que el trabajo figure COMPLETED aunque una futura corrida del simulador falle. Para futuras ejecuciones, terminar propagando el código capturado, por ejemplo `exit "$(cat results/angular-v1-smoke/exit_code.txt)"`. En esta entrega el código guardado es cero y el log y los conteos concuerdan: **no requiere repetir esta corrida**.

## Qué queda resuelto y qué sigue

La corrección angular supera la comprobación de integración solicitada. No hace falta aumentar N ni repetir A/B para cerrar esta comprobación. Preservamos la entrega en su rama; no se fusiona automáticamente con main ni se sustituyen datos históricos.

El siguiente trabajo es preparar el uso de esta malla en las herramientas que leen, representan y empaquetan imágenes, incluidas ROI y metadatos, y resolver la justificación del plano de conteo de 600 m y su normalización temporal. Usar primero código, derivaciones y evidencia existente; si falta un control físico, definir su propósito y criterio antes de ejecutarlo. Todavía no se autoriza una campaña masiva ni se decide reutilizar las 78 vistas históricas.

P-04 sigue abierto. Esta corrida tampoco cierra por sí sola P-01, P-02 o P-03. Consultar la [preparación de producción](PREPARACION_PRODUCCION_OE1.md) para el alcance condicionado del conjunto final.

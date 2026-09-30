# Registro de cambios

## Protocolo del segundo ensayo v1.0 — 2026-09-29

- Diseño documentado desde la revisión: etapa técnica acotada, primarios comunes, observable principal y entregables.
- Se sustituye el encargo de diseño desde cero; la etapa física de mayor estadística permanece condicionada a revisión.
- Se aclara que los recursos de cómputo no constituyen presupuesto económico.

## Extensión del control geométrico — 2026-09-29

- Se contrastan independientemente los volúmenes de las cuatro intersecciones conocidas del catálogo y sus fracciones del volumen del conducto.
- Se registran límites de interpretación: volumen no equivale a sensibilidad muográfica ni a efecto en conteos; el siguiente ensayo permanece pendiente de diseño.

## Control independiente adicional — 2026-09-29

- Se incorpora cálculo de volumen por cuadratura y contraste con la entrega, sin modificar fuentes originales.
- Se documentan coincidencias y límites de la asignación de materiales, incluida la densidad del aire.

## Revisión de entrega y encargo de diseño — 2026-09-29, Colombia

- Se documenta la revisión independiente de la entrega `712c786`, con observaciones y evidencia de recálculo.
- Se actualizan seguimiento, matriz e índice; el primer encargo queda identificado como histórico.
- Se solicita el diseño del segundo ensayo antes de ampliar simulaciones; sin fusión de resultados ni cierre del OE1.

## Revisión técnica del OE1 y preparación de instrucciones — 2026-09-28, Colombia

- Diagnóstico analítico del catálogo: intersecciones entre anomalías en cuatro geometrías y salidas del edificio en otras dos.
- Reproducción en memoria de 9.120 pares: coincidencia exacta, semillas consistentes y sin saturación uint16.
- Se incorporan diagnóstico, revisión de datos, instrucciones para SC3 y plantilla de entrega.
- Se añaden auditor local, ejecutor de piloto y comparador; su ejecución Geant4/SLURM queda pendiente en SC3.
- No se modifica ningún archivo original ni se declara cerrada la validación física.

## Publicación privada en GitHub

- Destino autorizado: `anlegogo/muografia-documentada`; rama `main`.
- Se registra la organización inicial con la identidad GitHub verificada del director, preservando la atribución del material recibido.
- Los datos NPZ y logs se mantienen fuera del historial; su restauración e integridad se documentan en `docs/PROCEDENCIA.md`.

## Incorporación inicial — 2026-09-29T03:08:48.514624+00:00

- Se incorpora una selección local del OE1 desde `b88fa576494cb8a664c46b8c94c5918c5097d616`.
- Se preservan 567 archivos originales con inventario de procedencia y SHA-256.
- Se documentan alcance, datos, cumplimiento, reproducción, pendientes y decisiones.
- Se incluyen datos y logs en disco, excluidos del historial Git.
- Se incorpora un verificador de integridad de solo lectura sobre originales.
- No se modifica código científico ni se ejecuta una nueva campaña. No se incorporan OE2/OE3.

# Ficha del conjunto de datos recibido

Fuente principal: [splits.json](originales/results/dataset/splits.json) y [manifiesto de campaña](originales/results/dataset/campaign-manifest.csv).

| Propiedad | Valor |
|---|---|
| Versión declarada | v1.0; congelamiento 2026-08-31T21:46:27+00:00 |
| Motor declarado | Geant4 11.4.2; generador guiado por tablas |
| Geometrías / vistas | 19 / 114 (6 vistas por geometría) |
| Eventos transportados / detectados | 4.124.005.421 / 3.025.131.757 |
| Referencia nominal | 30 días por vista; equivalencia dependiente de los supuestos del flujo |
| Fracciones / realizaciones | 0,50; 0,10; 0,05; 0,01 / 20 por fracción y vista |
| Pares totales | 9.120; no todos son de entrenamiento |
| Particiones | 12 geometrías train; 3 val; 3 test; 1 generalization |
| Pares por partición | 5.760 / 1.440 / 1.440 / 480 |
| Semilla maestra | 20260805 |

Cada vista cruda contiene `counts_ref`; el NPZ entregado de Geant4 no contiene un mapa de opacidad. Cada shard agrupa `ref_counts`, `low_counts` y `fractions`. El código declara dimensiones `(vistas, H, W)` y `(vistas, fracciones, realizaciones, H, W)`. Los metadatos registran semillas y procedimiento.

Para Geant4 se aplica **submuestreo binomial** a los conteos de referencia: cada evento se conserva con probabilidad f. El motor analítico usa otra rama con muestreo Poisson de su mapa de tasas; no deben confundirse. Las realizaciones derivadas de una misma vista no son escenarios volcánicos independientes.

La normalización del módulo original utiliza el máximo de la referencia. Es un contrato de preprocesamiento que debe declararse; los datos almacenados son conteos crudos. La separación por geometría evita compartir una misma geometría entre particiones, pero por sí sola no demuestra todas las formas posibles de independencia experimental.

Para integridad de archivos usar [inventario](inventario/archivos.json). Para validez física consultar [pendientes](PENDIENTES.md).

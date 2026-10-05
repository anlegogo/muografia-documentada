# Datos de entrada de las figuras

No se versionan aquí los binarios grandes. Para regenerar las figuras:

- `imagenes/`: copiar las 114 imágenes `.npz` y sus `.meta.json` desde `muografia-documentada`, rama
  `oe1/justificacion-fisica-produccion` (commit en `ORIGEN_COMMIT.txt`), carpeta
  `objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/datos/sc3/campana-114/imagenes/`.
  Los scripts las verifican contra `imagenes.sha256`.
- `geo-train-08_view0_pairs.npz`: copiar desde la carpeta `pares/` de la copia de distribución del
  conjunto (Drive `oe1-campana-114`). El script lo verifica contra `huellas-contenido.json`.

Los JSON de esta carpeta (evaluación, huellas, inventario y catálogo) son copias sin cambios del mismo commit.

# Congelamiento previo a las 13 corridas

Antes de lanzar las 13 corridas de producción quedan fijos los cuatro elementos de la tabla. Ninguno puede cambiar desde ese punto.

| Elemento | Dónde | SHA-256 |
|---|---|---|
| Herramientas de análisis | commit `3315f82ffa1a3be604897e34e2319b379f500655` de `muography-dl-reconstruction` | de cada archivo, abajo |
| Especificación de R_int (195 píxeles) | `analisis/roi/` | `R_int.mask.txt`: `e76dcbe5926f9f4aeb61c556729d15c64124cd50a8577dca6beee9ffa317c5fd` |
| Manifiesto de 13 corridas | `manifiesto-corridas.tsv` | `0a9acf6455469044a8c90b812921185b7dcf24c24d22c501b1c787005e79a402` |
| Huellas esperadas de las entradas (20 líneas) | `entradas-esperadas.sha256` | `eb144327e46699bb3d0192a00da3644b8919224f3677e015990b82f83b5d0dd4` |

Huellas de las herramientas, tomadas de `primarios/herramientas.sha256` (coinciden con los archivos del commit):

- `oe1_stage1_analysis.py`: `e08d3355e32257fda2330b3c73600aebb46983b61eff71d143a96d07163173a3`
- `oe1_stage1_common.py`: `1575b1e64d0431da50f708c4735930fe3b2457fce7cf2b1f5a29fed5d371fb3e`
- `oe1_stage1_roi.py`: `e9b2de31191e569ca92c4b3bb51bc31f1ffed9b90f31e35441beb5e29b9b1105`

Las rutas de `entradas-esperadas.sha256` son las de SC3, así que `sha256sum -c` se ejecuta allí.

Regla del paso 10 del README: si cualquiera de estos elementos cambia, el intento queda anulado. Se corrige, se repiten los pasos 5 a 9 y se inicia un intento nuevo.

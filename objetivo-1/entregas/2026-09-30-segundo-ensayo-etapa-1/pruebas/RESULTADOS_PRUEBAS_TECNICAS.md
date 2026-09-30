# Resultados de las pruebas técnicas de la etapa 1

1. El registro por muón no altera la simulación. Con registro completo y con registro mínimo, los 2.000 muones de T-R dan el mismo histograma y el mismo estado del generador al terminar cada muón (`rng1`).
2. La detección de cruces funciona como se espera. `test_region_crossing` pasa sus 453.607 comprobaciones y T-S clasifica correctamente 60 de 60 muones sintéticos en A2 y en B2.

## 1. ¿El registro altera la simulación?

- `T-R`: `hist.csv` con el mismo SHA-256 en `--muon-log full` y `min`; mismos `id`; `rng1` igual en todos (0 distintos); identidad, estado y bin iguales.
- `T-L` (A y B): binarios del piloto frente a A2 y B2 en modo legado, `hist.csv` idéntico byte a byte; `meta.json` igual salvo tiempos; sin la clave `oe1_etapa1` ni `_muones.csv`.
- `T-M`: con otra semilla maestra (1026092995 frente a 1026092990), `rng0`, `rng1`, `hist.csv` y `_muones.csv` idénticos byte a byte.
- `T-P`: al sustituir las primeras 100 filas de la lista, los `id` ≥ 100 conservan `rng0`, `rng1` y todo el resultado; las 100 filas sustituidas cambian de primario.

Alcance: T-R, T-M y T-P usan B2 en geo-train-06 con 2.000 muones; la conclusión se extiende a A2 porque P2 es el mismo parche en A2 y en B2, y T-S y T-F ejecutan A2 en modo lista con registro completo.

## 2. ¿La detección de cruces funciona como se espera?

- C1 a C9, R1 y V: 453.607 comprobaciones en `test_region_crossing`, 0 fallidas (compilación normal y con ASan/UBSan); R1 pasa con seis semillas; 0 avisos del compilador.
- `T-S` en A2 y en B2: clasificación 60/60, longitudes 20/20 (diferencia máxima 0,185 %, margen ±1 %), materiales 60/60.
- K-ROI: el centroide de Z cae en el píxel (34, 135), dentro de R_int; su espejo, (34, 120), queda fuera; la masa de L_Z es 0,9694 en R_int y 0 en el espejo; Jaccard 0,9949.

También pasan T-F (análisis sin contratos fallidos, tabla de 5 corridas, STOPPED, OTHER y ABORTED en 0) y el resto de K0: banco sintético (13 escenarios), salida anticipada (32 de 32), inercia del modo legado, 223 pruebas de Python en SC3 (9 omitidas) y auditoría de aleatorios en A2 y B2.

`analisis-TF/mapas-etapa1.npz` tiene hora de modificación 20:00:24 UTC, 1 min 42 s después del resto de `analisis-TF/`, que es de 19:58:42 UTC; es compatible con una escritura diferida del sistema de archivos compartido. Al repetir el mismo análisis por separado, sus seis arreglos y todas las tablas coinciden; en `contratos.json` solo cambian la fecha y la forma de las rutas.

## Trabajos en SC3 (30 de septiembre de 2026, partición legacy)

| Trabajo | Qué | Nodo | Inicio UTC | Fin UTC | Resultado |
|---|---|---|---|---|---|
| 30563 | Compilación de A2 y B2 | guane01 | 19:31:12 | 19:32:02 | OK, 0 avisos |
| 30564 | K0, intento 1 | guane01 | 19:33:21 | 19:35:07 | falló por la disposición de carpetas (`k0-intento-1/`) |
| 30565 | K0, intento 2 | guane01 | 19:37:31 | 19:54:46 | OK (`k0/`) |
| 30567 | Preparación (K2, K1, K-ROI) | guane02 | 19:56:06 | 19:56:57 | OK |
| 30568 | Pruebas técnicas | guane02 | 19:58:12 | 19:58:43 | OK |

## Dónde está cada evidencia en `pruebas/`

| Evidencia | Archivos |
|---|---|
| T-R, T-L, T-M, T-P | `T-R.json`, `T-L-A.json`, `T-L-B.json`, `T-M.json`, `T-P.json` |
| T-S y T-F | `T-S-A.json`, `T-S-B.json`, `T-F.json`, `analisis-TF/`, `analisis-TF.txt` |
| C1 a C9, R1, V | `k0/cruces/pruebas-cruces.json`, `k0/cruces.log` |
| Resto de K0 | `k0/` (`banco-sintetico.log`, `salida-anticipada.log`, `inercia-legado.log`, `pruebas-python.log`, `auditoria-aleatorios-A2.log`, `auditoria-aleatorios-B2.log`) |
| K-ROI | `kroi.txt`, `kroi/kroi.json` |
| Veredicto, estado y entorno | `resumen-pruebas-tecnicas.json`, `estado-pruebas-tecnicas.txt`, `entorno.txt` |
| Corridas técnicas sin procesar | `crudos-tecnicos-01.tar.gz` y su `.sha256` |

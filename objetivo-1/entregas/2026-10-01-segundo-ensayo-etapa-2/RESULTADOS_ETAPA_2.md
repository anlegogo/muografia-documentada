# Resultados de la etapa 2 de OE1 (protocolo v1.1)

1 de octubre de 2026 (Colombia, UTC−5). Diseño: [PROTOCOLO_ETAPA_2_OE1_V1_1.md](../../PROTOCOLO_ETAPA_2_OE1_V1_1.md) e [INSTRUCCIONES_ETAPA_2.md](../../INSTRUCCIONES_ETAPA_2.md), sobre `main` en `ae29a17`. Preparación: [PREPARACION_ETAPA_2.md](PREPARACION_ETAPA_2.md), commiteada en `0135072` antes del primer transporte.

## Resumen

- **Categoría de cierre: inconcluso.**
  - En R_int de `geo-train-06`, vista 0, con N = 24.000.000 pares, Δ = (n01 − n10)/N = (4 − 1)/N = **+0,125 cuentas por millón de primarios**.
  - El intervalo conservador del 95 % es **[−0,229; +0,469] por millón**. Su extremo superior supera el margen M = 0,274 por millón, así que el intervalo no queda dentro de (−M, +M) ni fuera de él.
- **Contratos y controles en verde:** las 55 corridas terminaron bien, los 24 bloques principales son válidos y la compuerta de controles pasó (A/A idéntica y A/B idénticos en `geo-train-01`).
- **El efecto se concentra donde predecía el mecanismo de R2-01.**
  - De los 24 millones de pares, 151 cruzan Z: 51 entran desde el conducto y 100 desde el cuerpo denso.
  - Los 100 que entran por el cuerpo denso son idénticos en A y B.
  - Todas las diferencias salen de los que entran por el conducto, que en A atraviesan Z como conducto: 50 discordancias, las 5 transiciones de R_int, las 3 de detección total y los 10 cambios de píxel.
  - B asigna Z al cuerpo denso en los 151 cruces.
- **Propuesta:** producir los datos definitivos con la geometría corregida B, sin esperar a demostrar equivalencia con A, y declarar el impacto histórico en este caso como pequeño pero no acotado al margen.

## 1. Ejecución

| Elemento | Valor |
|---|---|
| Código | `muography-dl-reconstruction`, rama `oe1/stage2`, commit `d8ca749`. Binarios A2 `a07d83c4…` y B2 `ae761866…`, sin cambios |
| Trabajos SLURM | 30599 (listas, guane02); 30601 (controles, guane01); 30602 (M1, réplicas 101–112, guane02); 30603 (M2, réplicas 113–124, guane03). [`slurm/sacct.txt`](slurm/sacct.txt) |
| Entorno | Partición `legacy`, `gnu14/14.2.0` y `geant4/11.4.2`. Un proceso de un hilo por corrida y todas las de un grupo a la vez en su nodo; A y B de cada bloque comparten nodo |
| Manifiesto ejecutado | 55 corridas según [`corridas.csv`](../../ensayos/etapa-2-v1.1/corridas.csv): 48 principales (24 listas de 1.000.000), 6 de control (3 listas de 100.000) y una repetición A/A |
| Resultado de las corridas | 55 de 55 OK, en el primer intento y sin reintentos ([`estado.tsv`](corridas/m1-intento-01/estado.tsv) de cada grupo) |
| Recursos medidos | Transporte: 12,08 h de CPU (estimación del protocolo: 11,44 h, rango 7,91–12,35). Cada corrida de 1.000.000 tardó entre 874 y 906 s de pared; la RSS máxima fue de 521 MB |
| Desviación | Solo de almacenamiento: no había 30 GiB en SC3, se trabajó en `/tmp` del nodo con exportación verificada ([PREPARACION §1](PREPARACION_ETAPA_2.md)). El diseño científico no cambió |

## 2. Controles (compuerta previa al principal)

[`controles.json`](analisis/controles.json): estado OK y ningún contrato fallido o no verificable.

- **K6:** las 7 corridas de control están completas y en orden.
- **K7 (A/A de r201):** hist y registro por muón idénticos byte a byte, meta igual salvo los tiempos, y el mismo nodo.
- **K8 (A frente a B en `geo-train-01`, réplicas 201–203):** histogramas y registros idénticos salvo la columna `variant`, y meta igual salvo las claves esperadas.
- **K9 (a):** `prim_fnv` y `rng0` son iguales en todos los pares.
- **Transiciones de R_int en los controles:** n01 = n10 = 0 en las tres réplicas.

## 3. Contratos del principal

En los 24 bloques se cumplen todos los contratos bloqueantes ([`analisis/bloques/`](analisis/bloques/)):
- **K6** en las 48 corridas:
  - 1.000.000 filas e IDs 0…N−1;
  - `prim_fnv` recalculado desde la lista;
  - sin ABORTED;
  - histograma reconstruido igual a `hist.csv` en las 65.536 celdas;
  - `in_rint` igual al recalculado;
  - B sin avisos;
  - procedencia, semillas y firma de geometría correctas.
- **K9 (a):** `prim_fnv` y `rng0` iguales para todo ID.
- **K9 (c):** en B, `lz_a0` y `lz_rock` ≤ 1 µm.

La [verificación de integridad](analisis/verificacion-integridad.json) descomprime cada registro y cada lista descargados y compara su SHA-256 con el registrado en SC3 y con las listas congeladas. Resultado, sin ningún fallo:
- 55 de 55 corridas con su `SHA256SUMS` correcto;
- 55 de 55 registros por muón (16,4 GB sin comprimir) iguales a los originales;
- 27 de 27 listas iguales a las congeladas.

## 4. Resultado confirmatorio (R_int)

[`resultados-etapa2.json`](analisis/agregado/resultados-etapa2.json) y [`transiciones-por-bloque.csv`](analisis/agregado/transiciones-por-bloque.csv). El intervalo se calculó con la función `interval()` del [calculador del director](../../../herramientas/planificar_etapa2_oe1.py).

| Conteo | Valor |
|---|---|
| N (pares) | 24.000.000 |
| n00 / n01 / n10 / n11 | 23.999.929 / **4** / **1** / 66 |
| Cuentas en R_int: A / B | 67 / 70 |
| Δ por millón | +0,125 |
| Intervalo conservador 95 % por millón (Clopper–Pearson al 97,5 % para p01 y para p10, por unión) | [−0,2292; +0,4694] |
| Margen M por millón | ±0,2737 |
| Categoría numérica | **inconcluso** (el extremo superior supera +M) |

- **Por bloque:** solo 4 de los 24 bloques tienen alguna discordancia en R_int: r101 (0→1), r109 (0→1), r112 (0→1) y r121 (0→1 y 1→0).
- **Variación entre bloques, solo descriptiva:** Δ media 0,125 por millón, desviación estándar 0,338 y rango 0 a 1. El protocolo (§3) no la usa como intervalo.
- **Detección total, exploratoria:** m01 = 2 y m10 = 1, es decir Δ = +0,042 por millón, con intervalo [−0,259; +0,338]. Los 18.053.098 detectados en A frente a 18.053.099 en B dan una eficiencia de 0,752.

## 5. Cambios espaciales y cruces de Z

- **Mapas** ([`mapas-etapa2.png`](analisis/agregado/mapas-etapa2.png), [`mapas-etapa2.npz`](analisis/agregado/mapas-etapa2.npz)): A/N, B/N y (B−A)/N. Solo difieren 23 de las 65.536 celdas, todas alrededor de R_int, y en ninguna por más de una cuenta en 24 millones.
- **Cambios de píxel** ([`cambios-pixel-agregado.csv`](analisis/agregado/cambios-pixel-agregado.csv)):
  - 10 pares detectados en ambas variantes caen en un píxel distinto;
  - 5 de ellos están dentro de R_int en las dos.
  - El Δ neto no los muestra.
- **Unión U de cruces de Z** ([`cruces-agregado.csv`](analisis/agregado/cruces-agregado.csv)): 151 muones, que cruzan en A y en B, es decir unos 6,3 por millón.

| Lado observado en A | Cruces | Idénticos A/B | Discordantes | ΔE de salida de Z (B − A) |
|---|---|---|---|---|
| Cuerpo denso (`mat_in` = A1) | 100 | 100 | 0 | 0 en los 100 |
| Conducto (`mat_in` = A0) | 51 | 1 | 50 | mediana −8,6 GeV; B pierde más en 43 y menos en 7 |

- **Material de B:** en los 151 cruces toda la longitud en Z es A1, dentro de 1 µm.
- **Las 50 discordancias** ([`discordantes-agregado.csv`](analisis/agregado/discordantes-agregado.csv)) son de muones que cruzan Z por el conducto:
  - 37 solo cambian el estado aleatorio final (`rng1`);
  - las demás cambian la detección (2 de DECAY a DET y 1 de DET a MU_CAPTURE), el píxel o la pertenencia a R_int.
  - No hay ninguna discordancia de muones que no crucen Z.

## 6. Evaluación de cada criterio

| Criterio (protocolo) | Resultado |
|---|---|
| §2 Configuración congelada: binarios, catálogos, tablas, máscara, un hilo, sin cambios de instrumentación | Cumple ([preparación §2](PREPARACION_ETAPA_2.md)) |
| §2 y §8.3 Listas congeladas antes de transportar y la misma lista en A y B | Cumple: 27 listas con SHA, regeneradas y verificadas antes de cada trabajo |
| §3 Tamaño fijo: 55 corridas, 48,7 M de transportes, N = 24 M | Cumple, sin bloques añadidos ni quitados |
| §6 Una sola evaluación confirmatoria con las 24 listas válidas | Cumple: una única agregación, con 24 de 24 bloques |
| §7 Controles (3 A/B y A/A) antes del principal | Cumple: todos idénticos |
| §7 N filas, IDs únicos, SHA, FNV, rng0 y estados válidos | Cumple en las 55 corridas |
| §7 Histograma reconstruido, máscara e índices | Cumple en las 55 corridas |
| §7 B sin avisos nuevos; A solo con el defecto declarado | Cumple (K2 y K6) |
| §7 Transiciones, cambios de bin y píxel distinto dentro de R_int | Informados en §4 y §5 |
| §7 Cruces con la selección común U | 151 cruces, con lado, longitudes, materiales y energía |
| §5 y §6 Regla de cierre | **Inconcluso**: [−0,229; +0,469] toca la región por encima de +M |

## 7. Cuantificación del impacto

- **Cambio en cuentas de R_int:** +3 netas (67 → 70) en 24 millones de primarios, es decir +0,125 por millón.
  - Escalado a la imagen de referencia de 30 días (36.174.382 primarios y 98 cuentas en R_int), el cambio esperado es de unas +4,5 cuentas, con intervalo [−8,3; +17,0].
  - El ruido Poisson de esa imagen es √98 ≈ 9,9 cuentas.
- **El efecto no está acotado por debajo del margen:** con 95 % de confianza conservadora, el cambio neto podría llegar a 1,7 veces M.
- **Alcance del mecanismo:** solo afecta a muones que entran en la intersección desde el conducto, unos 2,1 por millón de primarios en este caso. En ellos, A subestima la densidad atravesada (1,832 frente a 3,285 g/cm³).

## 8. Propuesta de actualización de los datos de OE1

1. **Regenerar con la geometría corregida B** las imágenes de `geo-train-06` y de las otras cinco geometrías señaladas con solapes, en sus seis vistas. Seguir el protocolo §6: la producción con B no exige demostrar equivalencia, y el resultado no permite declarar despreciable el impacto en este caso.
2. **Mantener sin regenerar las geometrías sin solapes**, siempre que su firma de volúmenes A = B se compruebe con K2 y K8. El control `geo-train-01` muestra identidad exacta entre A y B cuando no hay solape.
3. **Conservar las imágenes históricas de A solo como referencia** y documentar el impacto de este caso como «inconcluso, no acotado al margen M», con Δ e intervalo.
4. **Antes de producir:** congelar el entorno de producción (P-02/P-03), justificar la normalización de conteos (P-04) y verificar las imágenes nuevas a nivel de cuentas y reducciones, como pide el protocolo §9.

**Fase siguiente:** no se generaron datos definitivos. `INSTRUCCIONES_ETAPA_2.md` no incluye esa fase, y el protocolo §9 la deja para después de la revisión de estos resultados.

## 9. Datos y archivos

- **Datos grandes, fuera de Git:**
  - qué son: 85 archivos, 6,69 GB comprimidos (los 55 registros por muón, las 27 listas y 3 paquetes de archivos pequeños);
  - dónde están: en la [carpeta compartida del proyecto](https://drive.google.com/drive/folders/1yDAqmIiffuive-M9Esm4_KbHn65qQDja?usp=sharing) `para-drive-oe1-etapa2` ([`datos-compartidos/ENLACE.txt`](datos-compartidos/ENLACE.txt)), con su lista [`SHA256SUMS.txt`](datos-compartidos/SHA256SUMS.txt);
  - cómo comprobarlos: después de descargarlos, ejecutar `sha256sum -c ../SHA256SUMS.txt` dentro de la carpeta `datos/` (85 archivos).
- **En esta carpeta:**
  - [`corridas/`](corridas/): de los tres grupos, comandos, `run.log`, meta, histogramas, `SHA256SUMS`, estado, entorno, manifiesto, huellas esperadas y análisis por bloque;
  - [`preparacion/`](preparacion/): listas congeladas, validación y K2;
  - [`analisis/`](analisis/): bloques, controles, agregado e integridad;
  - [`slurm/`](slurm/): salidas y `sacct`.
- **Límites:**
  - una ROI, una vista y una geometría; no se extrapola a las 114 vistas ni a otras geometrías;
  - las longitudes en Z son cuerdas de paso y las energías en sus bordes se interpolan;
  - el intervalo es conservador y no óptimo;
  - la variación entre bloques es solo descriptiva.

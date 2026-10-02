# Resultados del piloto de seis vistas (geo-train-06)

2026-10-02 (Colombia). Tras acordar con la dirección el diseño y el presupuesto del piloto, se ejecutó el [piloto propuesto](../../DISENO_ESTADISTICO_Y_REFERENCIAS.md#piloto-de-seis-vistas-propuesta-calculada-no-orden-de-ejecución) con el flujo de la [guía](../../GUIA_SIGUIENTE_ETAPA_OE1.md) y las herramientas de `c9442d6`, sin modificar. Se usó la integración descrita en [RESULTADOS_INTEGRACION_OPERATIVA.md](RESULTADOS_INTEGRACION_OPERATIVA.md), con el envoltorio `python-oe1` (D-01).

**Resultado.** Los 36 bloques terminaron y se publicaron sin fallos. La fusión, la evaluación, la exportación y el empaquetado terminaron con código 0. **Las 90 regiones de borde (15 por vista) quedan dentro de la tolerancia de ±1 pp con el intervalo completo.** En las ROI de roca, la mediana es de 121 a 127 cuentas por vista y el 63–65 % de las ROI alcanza 100 cuentas. Ninguna herramienta declara validación física ni habilita producción (`physical_validation: false`, `production_authorized: false`).

## 1. Ejecución

| Elemento | Valor |
|---|---|
| Manifiesto | 36 filas, geo-train-06, vistas 0–5, seis bloques por vista, 211.000.000 primarios por vista, 1.266.000.000 en total. SHA-256 `36d072c16d4f51a1772984114c1ab9a873501aa4b17aab14562fb7272a6d9a8d` |
| Envío | [lanzar_piloto.sh](verificacion/lanzar_piloto.sh): una pasada de `lanzar_campana_angular.py --enviar --python ~/oe1-trabajo/entorno/python-oe1 --threads 24 --max-trabajos 4`. 31 pasadas entre 13:18 y 15:35; nueve enviaron cuatro filas cada una y el resto encontró la cola llena. Cada fila se envió una vez y ninguna quedó en `blocked_prior_attempts` |
| Cupo | 4 trabajos y 4 nodos por usuario (QoS `normal` de SC3, `maxjobspu=4`, `maxtrespu=node=4`) |
| Trabajos | 30643–30646 y siguientes hasta 30679, 36 en total; todos `COMPLETED 0:0` en la partición `legacy`, nodos guane01–guane05 ([sacct-piloto.txt](datos/sc3/piloto-v2/piloto-resultados/sacct-piloto.txt)) |
| Duración | 798 s de media por bloque (mínimo 794, máximo 802). Primer inicio 13:18:13 y último fin 15:45:13 |
| Cómputo medido | **191,6 h-núcleo** (36 × 798 s × 24), frente a 187,3 estimadas con la tasa de c01 (+2,3 %) |

## 2. Comprobación de los bloques

[revisar_bloques_piloto.sh](verificacion/revisar_bloques_piloto.sh), de solo lectura, sobre los 36 bloques publicados. Para cada uno comprueba que la semilla y los primarios transportados coincidan con el manifiesto, que el histograma sea de 256 × 256, que las sumas del histograma con corte y sin corte coincidan con `detected_in_bins` y `detected_all_energies`, que el corte no supere al histograma sin corte en ningún píxel, que `exposure_days = −1` y que el recibo de publicación esté verificado. **36 de 36 cumplen.**

Contraste interno: `nominal_in_window` / eventos vale 0,6842 por bloque, igual a la probabilidad nominal de la ficha (0,6841). Cada bloque suma 20,03 días convencionales y cada vista 120,18.

## 3. Evaluación del piloto

[evaluacion-piloto-v2.json](datos/sc3/piloto-v2/piloto-resultados/evaluacion-piloto-v2.json), producido por `evaluar_piloto_angular.py` con el diseño congelado y la referencia ideal de cielo con margen de 5°. Error familiar del 5 % para las seis vistas (α = 0,05/6 por vista) y tolerancia de ±1 pp. Se evaluó una sola vez, con el N fijado.

| Vista | Regiones dentro de tolerancia | Región con mayor extremo del intervalo | Diferencia (pp) | Intervalo (pp) | Días convencionales |
|---:|---:|---|---:|---|---:|
| 0 | 15/15 | column_2 | +0,285 | [−0,246; +0,820] | 120,18 |
| 1 | 15/15 | column_2 | −0,187 | [−0,716; +0,345] | 120,19 |
| 2 | 15/15 | column_3 | −0,345 | [−0,873; +0,186] | 120,19 |
| 3 | 15/15 | column_255 | −0,407 | [−0,935; +0,124] | 120,18 |
| 4 | 15/15 | column_252 | +0,282 | [−0,249; +0,816] | 120,17 |
| 5 | 15/15 | column_255 | +0,287 | [−0,244; +0,821] | 120,18 |

`all_border_regions_equivalent: true`. Según la guía, esto respalda el criterio de respuesta en los bordes, no todas las hipótesis físicas. El contraste mide la no uniformidad respecto de la fuente ideal sin transporte y no separa la migración angular del transporte en aire.

## 4. Conteos en roca

ROI de 4 × 4 píxeles seleccionadas por la columna nominal del cono homogéneo (244 por vista). Las anomalías se ignoran en la selección, pero se transportan.

| Vista | Mediana | Percentil 10 | Fracción con ≥ 100 cuentas |
|---:|---:|---:|---:|
| 0 | 122,0 | 63,3 | 0,639 |
| 1 | 127,0 | 62,0 | 0,631 |
| 2 | 121,0 | 62,0 | 0,652 |
| 3 | 123,5 | 63,0 | 0,639 |
| 4 | 127,0 | 63,3 | 0,631 |
| 5 | 126,0 | 61,3 | 0,631 |

No se fijó de antemano un umbral de suficiencia; estas cifras sirven para dimensionar la campaña. Con 211 millones de primarios por vista, alrededor de un tercio de las ROI de roca queda por debajo de 100 cuentas, es decir, con un error relativo de Poisson mayor que el 10 %.

## 5. Productos y huellas

| Producto | Ubicación en SC3 | Huella |
|---|---|---|
| Bloques publicados (36 directorios, 468 archivos) | `~/muography-scratch/oe1-piloto-v2-publicados` (26 MB) | [bloques-publicados.sha256](datos/sc3/piloto-v2/piloto-resultados/bloques-publicados.sha256): `7cb15c0b…`  |
| Fusión por vista | `~/muography-scratch/oe1-piloto-v2-fusion` (1,7 MB) | [revision-fusion.json](datos/sc3/piloto-v2/piloto-resultados/revision-fusion.json) `0fc8db37…`; histogramas en [fusion.sha256](datos/sc3/piloto-v2/piloto-resultados/fusion.sha256) |
| Imágenes exportadas (NPZ) | `~/muography-scratch/oe1-piloto-v2-imagenes` (584 kB) | [revision-exportacion.json](datos/sc3/piloto-v2/piloto-resultados/revision-exportacion.json) `46588dad…`; [imagenes.sha256](datos/sc3/piloto-v2/piloto-resultados/imagenes.sha256) |
| Inventario | — | [inventario-piloto-v2.json](datos/sc3/piloto-v2/piloto-resultados/inventario-piloto-v2.json) `8bf67b04…`: 6 de 6 referencias, `technical_complete: true`, `errors: []` |
| Evaluación | — | `evaluacion-piloto-v2.json` `d57e4853…` |

**Histogramas en el repositorio.** Los histogramas fusionados de las seis vistas (256 × 256, E_cin > 3 GeV) y sus metadatos están en [datos/sc3/piloto-v2/fusion/geo-train-06/](datos/sc3/piloto-v2/fusion/geo-train-06/). Las imágenes exportadas (`counts_ref` en `uint32`, con los bordes y centros de azimut y elevación) están en [datos/sc3/piloto-v2/imagenes/](datos/sc3/piloto-v2/imagenes/). Ambas copias coinciden byte a byte con `fusion.sha256` e `imagenes.sha256`. Los 36 bloques individuales, que incluyen los histogramas sin corte y la generación nominal (26 MB), permanecen en SC3 con sus huellas en `bloques-publicados.sha256`.

Conteos fusionados con corte por vista: 73.882.961; 73.888.094; 73.888.460; 73.877.504; 73.872.248 y 73.874.396. Sin corte: de 137.486.309 a 137.505.724. La fusión verificó cada bloque sin aceptar conversiones CRLF.

El empaquetado se ejecutó como indica la guía, sin `--salida`, así que verificó el inventario sin generar los 480 pares de estas seis referencias.

Evidencia: [datos/sc3/piloto-v2/](datos/sc3/piloto-v2/). Incluye `piloto/` (las 31 pasadas del lanzador con su salida, su código de salida y la cola) y `piloto-resultados/` (comandos, salidas, códigos de salida, `.operacion` con identidad, registros y logs SLURM, y 105 archivos en `salidas.sha256`, `b93efe76…`). Scripts ejecutados: [posproceso_piloto.sh](verificacion/posproceso_piloto.sh) y los dos anteriores.

## 6. Lectura y propuesta

1. **Bordes.** El criterio acordado se cumple en las seis vistas con el N fijado de antemano. No se extiende este resultado a otras geometrías sin evaluarlas.
2. **Estadística en roca.** Con N = 211 millones por vista, el percentil 10 ronda las 62 cuentas. Si los conteos escalan linealmente con N (supuesto, no medido), que el 90 % de las ROI llegue a 100 cuentas requeriría unos 1,63 × 211 ≈ 344 millones de primarios por vista.
3. **Coste de la campaña.** Con la tasa medida (31,9 h-núcleo por vista de 211 millones), las 114 vistas costarían unas 3.640 h-núcleo con N = 211 millones y unas 5.940 con N ≈ 344 millones. Con 96 núcleos simultáneos equivalen a unas 38 y 62 horas de reloj, sin contar la espera en cola. La tasa se midió en geo-train-06; otras geometrías pueden diferir.
4. **Siguiente decisión.** Fijar N por vista para la campaña de 114 referencias (211 millones u otro valor justificado por la estadística en roca) antes de generar su manifiesto. La guía indica que no hay paso automático a las 114 vistas.

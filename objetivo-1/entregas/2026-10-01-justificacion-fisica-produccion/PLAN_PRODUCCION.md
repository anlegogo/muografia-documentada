# Plan de producción del conjunto de imágenes del OE1 (malla az-edges-v1, receta validada)

Las cifras salen de `resultados/plan-produccion.json` (`scripts/plan_produccion.py`). Ese script combina tres fuentes: los 114 histogramas y metadatos de la campaña histórica (huellas verificadas), los 194 registros SLURM de esa campaña y el impacto medido de la receta en los controles de SC3 (`resultados/controles-sc3.json`). **No se lanzó la producción.** La cadena completa sí se probó en SC3 con dos bloques pequeños (sección 5).

## 1. Receta validada

La receta queda fijada por las comprobaciones de [PUNTOS_NO_DEMOSTRADOS.md](PUNTOS_NO_DEMOSTRADOS.md):

| Elemento | Valor | Respaldo |
|---|---|---|
| Ejecutable | Árbol `angular-v1` (`0dea8e1`, malla v1 + geometría B) + `controles-oe1-v3.patch`, compilado con el mismo `CMAKE_BUILD_TYPE` que `build-az-edges-v1` | Sin opciones, el binario es bit a bit idéntico al de producción (r01, a00, c00) |
| Inyección | 1 m antes de que la línea de mira entre en roca (`OE1C_INJECT=cone`) | C2: cielo abierto 99,97 % |
| Margen de generación | 5° por lado (`OE1C_MARGIN_DEG=5`); el 68,42 % de los primarios cae en la ventana | C4: sesgo medio de borde −0,07 pp |
| Plano de conteo | 600 m (`OE1C_PLANE_HALF_M=300`) | C5: diferencia de 0 pp frente a 1.200 m |
| Observable (imagen de referencia) | Muones con E_cin > 3 GeV al cruzar el plano, por dirección de llegada | C1: imagen independiente del plano; conserva el 83,5 % del conteo en roca |
| Normalización | k · S0_v1 inyecciones nominales en la ventana = k · 30 días convencionales | Sección 2b del README; convención de área pendiente (C6) |

> **Actualización 2026-10-02:** la revisión de la dirección deja abiertos F-01 (equivalencia con el panel, control C3), F-02 (normalización y etiqueta de T) y F-03 (bordes con el observable final), además de C6. Ver [IMAGEN_FINAL_OBSERVABLE.md](IMAGEN_FINAL_OBSERVABLE.md). Este plan sigue siendo condicional; no autoriza P0 ni P1.

## 2. Geometrías y vistas; qué se reutiliza

Se generan **las 114 vistas** (19 geometrías × 6). Ninguna referencia histórica se reutiliza:

- La malla v1 cambia la asignación a columnas, y sin direcciones por evento no se puede reasignar.
- Seis geometrías cambian con la corrección B.
- El observable cambia: inyección, margen y corte. En el resto del catálogo, el conteo histórico en las ROI de roca estaba inflado entre 3 y 7 veces por muones blandos que dependen del plano (C1).

Sí se reutilizan:

- El catálogo de geometrías.
- Las tablas `tables-az-edges-v1` (huellas 76698ac1…, 7161c8ad…, 65cf778e…).
- El código `0dea8e1` con el parche.
- La cadena local del director (lectura, ROI, empaquetado).
- Los 9.120 pares históricos, que se conservan como versión distinta y no se mezclan con la nueva.

## 3. Criterio para el número de muones

**Unidad estadística.** Una ROI es un bloque de 4×4 píxeles (0,94° × 0,70°) cuya dirección central atraviesa entre 3·10⁴ y 10⁵ g/cm² de roca. Son 21.816 ROI en las 114 vistas.

**Conteo esperado con la receta.** Es el conteo histórico por ROI multiplicado por el factor medido en geo-train-01, 0,124 (mediana de 152 ROI comparando la receta con E > 3 GeV frente a la configuración histórica, mismos 2·10⁷ primarios). Que ese factor valga para geometrías con anomalías es un supuesto; se verifica en P0.

**Criterio propuesto.** El 90 % de las ROI debe alcanzar **100 cuentas (precisión de Poisson del 10 %)** en la referencia. Eso exige k = 9,5. Alcanzar 400 cuentas (5 %) exigiría k = 37,9.

| k | Exposición equivalente | Generados por vista | Bloques por vista | Horas-núcleo | Pared con 4 trabajos | ROI ≥ 100 cuentas | ROI ≥ 400 cuentas | Mediana ROI (referencia / fracción 0,01) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 120 d | 210.671.347 | 6 | 3.322 | 34,6 h | 63,4 % | 10,8 % | 135 / 1,3 |
| 8 | 240 d | 421.342.694 | 11 | 6.644 | 69,2 h | 86,6 % | 32,8 % | 269 / 2,7 |
| **10** | **300 d** | **526.678.368** | **14** | **8.305** | **86,5 h** | **90,8 %** | 42,3 % | 336 / 3,4 |
| 16 | 480 d | 842.685.389 | 22 | 13.287 | 138,4 h | 96,1 % | 63,4 % | 538 / 5,4 |
| 32 | 960 d | 1.685.370.778 | 43 | 26.575 | 276,8 h | 99,3 % | 86,6 % | 1.077 / 10,8 |

**Recomendación: k = 10.** El coste es de 0,728 ms de núcleo por evento dentro de la ventana, medido en c02 (0,498 ms por evento generado dividido entre la fracción en ventana, 0,684). La campaña histórica midió 0,737 ± 0,033 ms con la receta anterior. La pared supone cuatro trabajos simultáneos, el límite de envío observado; la campaña histórica perdió el 41 % del cómputo en 80 trabajos duplicados, y el lanzador nuevo lo evita (sección 5).

**Niveles de submuestreo.** Se aplican las fracciones 0,5; 0,1; 0,05 y 0,01 con 20 realizaciones binomiales cada una, lo que da 80 pares por vista y 9.120 en total. Con k = 10 equivalen a 150; 30; 15 y 3 días convencionales. La mediana por ROI en la fracción 0,01 es de unas 3,4 cuentas, que corresponde al régimen de baja estadística del OE1. Los pares de una vista comparten la referencia.

**Almacenamiento.** Por bloque se guardan tres CSV (imagen con corte, imagen sin corte y direcciones nominales) de unos 274 kB cada uno: 1,31 GB para k = 10. El NPZ de pares ocupa 4,27 MB comprimido por vista (medido con k = 1); con k = 10 crece con los conteos, sin superar 21 MB por vista (2,4 GB en total). No se guarda información por evento.

## 4. Archivos y comandos exactos

Archivos en `produccion/`:

- `preparar_arbol_receta.sh`: construye `~/oe1-trabajo/produccion-receta` como copia de `angular-v1` + parche v3 y compila en `build-receta/`.
- `manifiesto-receta-k10.csv` (1.596 bloques de 37.619.884 eventos) y `manifiesto-receta-k1.csv` (228 bloques, para P0). La semilla se construye como 20261001·10⁶ + índice_geometría·10⁴ + vista·10³ + bloque, con el catálogo en orden alfabético.
- `bloque_v1.sbatch`: ejecuta una fila con la receta. Promueve el histograma con E > 3 GeV a `<stem>_hist.csv` y conserva `_hist_sin_corte.csv` y `_gen.csv`. Ajusta `detected_in_bins` y registra entorno, `receta.env`, huellas de entrada (incluido el parche), comando, log y código de salida, que propaga al terminar.
- `lanzar_v1.py`: envía solo filas no publicadas ni encoladas, con bloqueo de archivo y como máximo cuatro trabajos.
- `fusionar_v1.py`: suma exacta por vista, con verificación de huellas, eventos y entradas.
- `prueba_integracion.sh`: la prueba de la sección 5.

En SC3 (guane), una vez decidido C6:

```bash
scp -r produccion sc3-toctoc:~/oe1-trabajo/produccion-v1
ssh sc3-toctoc
ssh guane
cd ~/oe1-trabajo/produccion-v1
srun -p legacy -N1 -n1 -c24 -t 00:30:00 bash preparar_arbol_receta.sh    # ya ejecutado el 2026-10-02 (trabajo 30627)

# Piloto P0: geo-train-06 (geometría con anomalías), seis vistas, k = 1, unas 44 h-núcleo
awk -F, 'NR==1 || $2=="geo-train-06"' manifiesto-receta-k1.csv > manifiesto-p0.csv
python3 lanzar_v1.py --manifiesto $PWD/manifiesto-p0.csv --salida $HOME/muography-scratch/oe1-receta-p0 --dry-run
python3 lanzar_v1.py --manifiesto $PWD/manifiesto-p0.csv --salida $HOME/muography-scratch/oe1-receta-p0
python3 fusionar_v1.py --manifiesto manifiesto-p0.csv --salida $HOME/muography-scratch/oe1-receta-p0 \
    --destino $HOME/muography-scratch/oe1-receta-p0-fusion

# P1: 114 vistas, k = 10 (o el k que resulte de P0)
python3 lanzar_v1.py --manifiesto $PWD/manifiesto-receta-k10.csv --salida $HOME/muography-scratch/oe1-receta-k10
python3 fusionar_v1.py --manifiesto manifiesto-receta-k10.csv --salida $HOME/muography-scratch/oe1-receta-k10 \
    --destino $HOME/muography-scratch/oe1-receta-k10-fusion
```

En P0 se comprueban tres cosas antes de P1:

- (i) El factor de conteo por ROI de la receta en geo-train-06, comparado con su histórico; si difiere en más del 20 % de 0,124, se recalcula k.
- (ii) C4 con 5,3·10⁷ primarios por vista (26 veces los de la comprobación): las desviaciones de borde deben quedar ≤ 1 pp.
- (iii) Todas las vistas deben pasar por el exportador y el empaquetador del director.

En la réplica local, con las carpetas fusionadas copiadas desde SC3:

```console
python herramientas/preparar_imagen_angular_v1.py FUSION/geo-train-06/geo-train-06_view0_hist.csv --salida IMAGENES_V1
python herramientas/empaquetar_angular_v1.py IMAGENES_V1 --geometrias geo-train-06 --informe INVENTARIO_P0.json --salida PAQUETE_P0
```

## 5. Prueba de integración ejecutada (2026-10-02)

`prueba_integracion.sh` lanzó con `lanzar_v1.py` dos bloques de geo-train-06, vista 0, con 10⁵ primarios cada uno (trabajos 30628 y 30629, COMPLETED 0:0, 7 y 9 s):

- Los dos bloques se publicaron con `exit_code` 0, `salida.sha256`, `receta.env` y `entradas.sha256`.
- El encadenamiento (`CHAIN=1`) no reenvió ningún bloque: «pendientes=0».
- `fusionar_v1.py` produjo la vista (200.000 primarios y 69.995 registros con E > 3 GeV).
- `herramientas/preparar_imagen_angular_v1.py`, del director, la exportó sin errores y reconoció la procedencia de la malla v1, el binario y las tablas.

Toda la evidencia está en `datos/sc3/prueba-integracion/`. Estas imágenes son de prueba y no forman parte del conjunto.

# Plan de producción del conjunto de imágenes del OE1 (malla az-edges-v1)

Las cifras proceden de `resultados/plan-produccion.json`, que se obtiene con `scripts/plan_produccion.py` a partir de los 114 metadatos fusionados, los 194 registros SLURM de la campaña del 30–31 de agosto y los 114 histogramas (huellas verificadas contra `datos/sc3/campaign-manifest.csv`). **No se lanza producción en esta entrega.**

## 1. Condiciones previas

La producción depende de C1, C2 y C4 de [PUNTOS_NO_DEMOSTRADOS.md](PUNTOS_NO_DEMOSTRADOS.md). Cualquiera de ellas puede cambiar el ejecutable (corte de energía, punto de inyección o margen angular) y, con él, el conteo en roca que fija N. Por eso la producción se hace en dos etapas:

1. **Etapa P0 (piloto de producción):** geo-train-01, seis vistas, k = 1, con el ejecutable que resulte de C1, C2 y C4. Sirve para medir el tiempo por evento del ejecutable final y el percentil 10 del conteo por ROI. Con el ejecutable actual cuesta 44 h-núcleo y unos 19 min de pared por vista.
2. **Etapa P1:** las 114 vistas con el k que resulte de P0, según el criterio de la sección 3.

## 2. Geometrías y vistas a generar; qué se reutiliza

Se generan **las 114 vistas** (19 geometrías × 6 vistas). Ninguna referencia histórica se reutiliza como referencia de la nueva versión, por dos motivos:

- **Corrección angular.** Los histogramas históricos asignan cada dirección al centro más próximo con paso de 60/255°; las columnas extremas tienen la mitad de ancho. La malla v1 usa 256 intervalos iguales de 60/256°. Como no se conservan direcciones por evento, la reasignación no es exacta: cualquier redistribución entre columnas introduciría una correlación artificial entre píxeles vecinos.
- **Corrección geométrica.** Afecta a seis geometrías (geo-gen-01, geo-test-01, geo-test-03, geo-train-06, geo-train-08, geo-train-11). El árbol `angular-v1` (commit `0dea8e1`) contiene un `DetectorConstruction.cc` idéntico al de la variante B, verificado en SC3 con `diff -rq`. Producir con ese ejecutable aplica ambas correcciones.

Sí se reutilizan:

- El catálogo de 19 geometrías.
- Las tablas `tables-az-edges-v1`, cuyas huellas coinciden con la entrega `90abb96`: `row_weights_30d.txt` 76698ac1…, `p_cdf.txt` 7161c8ad…, `meta.json` 65cf778e….
- El ejecutable `build-az-edges-v1/muography_sim` (SHA-256 a29e5277…), mientras C1, C2 y C4 no lo modifiquen.
- La cadena local de lectura y empaquetado del director.
- Los 9.120 pares históricos, que se conservan como versión distinta y no se mezclan con la nueva.

## 3. Criterio para el número de muones

**Unidad estadística.** Una ROI es un bloque de 4×4 píxeles (0,94° × 0,70°) cuya dirección central atraviesa entre 3·10⁴ y 10⁵ g/cm² de roca. Es el rango en el que la transmisión es medible y donde se sitúan las anomalías del catálogo. Las 114 vistas suman 21.816 ROI de este tipo.

**Criterio propuesto.** El 90 % de las ROI debe alcanzar 400 cuentas en la referencia, es decir, una precisión de Poisson del 5 %. La reducción binomial no se ve limitada por este criterio: la fracción 0,01 conserva la baja estadística buscada, con unas 2,7 cuentas medianas por ROI para k = 1.

Con los datos históricos (k = 1, 30 d convencionales), la mediana es de 271 cuentas por ROI y el percentil 10 de 85. El k necesario por vista tiene una mediana de 3,6, un percentil 90 de 6,6 y un máximo de 7,1 (figura 6).

**Advertencia cuantificada.** Con el plano de 600 m y sin corte de energía, entre el 82 % y el 85 % del conteo en esa banda de columna excede la expectativa CSDA de transmisión: el conteo medido es entre 5,7 y 6,8 veces la expectativa. Esa componente es compatible con los muones blandos dispersados de C1. Si C1 adopta un corte, el conteo por ROI bajará y el k necesario subirá en una proporción similar. Por eso k se fija tras P0 con la regla k = 400 / p10(conteo por ROI en P0), redondeada hacia arriba a una potencia de 2.

| k | Exposición equivalente | Eventos por vista | Bloques | Horas-núcleo (rango por dispersión entre vistas) | Pared con 4 trabajos simultáneos | ROI con 400 cuentas (datos históricos) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 30 d | 36.034.070 | 114 | 841 (766–925) | 8,8 h | 33,1 % |
| 2 | 60 d | 72.068.140 | 228 | 1.682 (1.532–1.850) | 17,5 h | 63,9 % |
| 4 | 120 d | 144.136.280 | 456 | 3.363 (3.064–3.700) | 35,0 h | 86,8 % |
| 8 | 240 d | 288.272.560 | 912 | 6.727 (6.128–7.400) | 70,1 h | 96,3 % |

Las horas-núcleo se calculan con 0,737 ± 0,033 ms de núcleo por evento: media y desviación entre las 114 vistas, partición *legacy*, 24 hilos. La incertidumbre de la media es de ±0,4 %. La pared supone cuatro trabajos simultáneos, el límite de envío observado. La campaña histórica tardó 19,9 h y consumió 1.443 h-núcleo para k = 1, porque 80 de sus 194 trabajos fueron duplicados: un 41 % de cómputo repetido por carreras del encadenamiento. El lanzador nuevo serializa los envíos con un bloqueo de archivo y comprueba la cola antes de cada envío.

**Niveles de submuestreo.** Se aplican las fracciones 0,5; 0,1; 0,05 y 0,01 con 20 realizaciones binomiales cada una, lo que da 80 pares por vista y 9.120 en total. Con k = 1 equivalen a 15; 3; 1,5 y 0,3 días convencionales. Los pares de una misma vista comparten la referencia y no son simulaciones independientes.

**Almacenamiento (medido).** Un histograma CSV ocupa unos 274 kB por bloque. El NPZ de pares ocupa 4,27 MB comprimido por vista (medido en seis vistas con k = 1; rango 4,12–4,32 MB) y 21 MB sin comprimir. El total con k = 1 es de 0,03 GB de histogramas y 0,49 GB de pares (2,4 GB sin comprimir). Con k > 1 los histogramas escalan con el número de bloques (0,25 GB con k = 8), y el NPZ comprimido crece con los conteos, sin superar la cota sin comprimir de 2,4 GB. No se conserva información por evento.

## 4. Archivos y comandos exactos

Archivos en `produccion/`:

- `manifiesto-v1-k1.csv` (114 filas) y `manifiesto-v1-k2.csv` (228 filas), con las columnas fila, geometría, vista, bloque, semilla y eventos. La semilla se construye como 20261001·10⁶ + índice_geometría·10⁴ + vista·10³ + bloque, con el catálogo en orden alfabético y la misma regla que la campaña histórica. Los bloques no superan 4·10⁷ eventos (unos 25 min en 24 núcleos, por debajo del límite de 1 h). Para otros k se regenera con `scripts/plan_produccion.py`.
- `bloque_v1.sbatch`: ejecuta una fila del manifiesto. Registra el entorno, las huellas de las entradas (`entradas.sha256`, en el formato que espera `herramientas/preparar_imagen_angular_v1.py`), el comando, el log y el código de salida. Publica el bloque de forma atómica y **termina con el código real del simulador**.
- `lanzar_v1.py`: lanzador idempotente que envía solo filas no publicadas y no encoladas, con un máximo de cuatro trabajos.
- `fusionar_v1.py`: suma exacta de bloques por vista cuando k > 1. Comprueba código de salida, huellas, número de eventos e igualdad de entradas.

En SC3 (guane), una vez cerradas las condiciones de la sección 1:

```bash
# 0. Copiar produccion/ a SC3 y comprobar el ejecutable y las tablas
scp -r produccion sc3-toctoc:~/oe1-trabajo/produccion-v1
ssh sc3-toctoc
ssh guane
cd ~/oe1-trabajo/angular-v1
sha256sum build-az-edges-v1/muography_sim scripts/simulation/geant4_app/tables-az-edges-v1/*
#    esperado: a29e5277..., 65cf778e..., 7161c8ad..., 76698ac1... (o las huellas del ejecutable resultante de C1/C2/C4)

# 1. Etapa P0: las seis vistas de geo-train-01 (filas 24-29 del manifiesto k1)
awk -F, 'NR==1 || $2=="geo-train-01"' ~/oe1-trabajo/produccion-v1/manifiesto-v1-k1.csv > ~/oe1-trabajo/produccion-v1/manifiesto-p0.csv
python3 ~/oe1-trabajo/produccion-v1/lanzar_v1.py --manifiesto ~/oe1-trabajo/produccion-v1/manifiesto-p0.csv \
    --salida /home/$USER/muography-scratch/oe1-v1-p0 --dry-run
python3 ~/oe1-trabajo/produccion-v1/lanzar_v1.py --manifiesto ~/oe1-trabajo/produccion-v1/manifiesto-p0.csv \
    --salida /home/$USER/muography-scratch/oe1-v1-p0

# 2. Etapa P1 con el k fijado (ejemplo k = 2); el encadenamiento rellena la cola sin intervención
python3 ~/oe1-trabajo/produccion-v1/lanzar_v1.py --manifiesto ~/oe1-trabajo/produccion-v1/manifiesto-v1-k2.csv \
    --salida /home/$USER/muography-scratch/oe1-v1-k2

# 3. Fusión (solo k > 1) en una carpeta nueva
python3 ~/oe1-trabajo/produccion-v1/fusionar_v1.py --manifiesto ~/oe1-trabajo/produccion-v1/manifiesto-v1-k2.csv \
    --salida /home/$USER/muography-scratch/oe1-v1-k2 --destino /home/$USER/muography-scratch/oe1-v1-k2-fusion
```

En la réplica local, con la cadena del director (`objetivo-1/CADENA_LOCAL_OE1.md`) y las carpetas copiadas desde SC3, para cada vista:

```console
python herramientas/preparar_imagen_angular_v1.py FUSION/geo-train-01/geo-train-01_view0_hist.csv --salida IMAGENES_V1
python herramientas/empaquetar_angular_v1.py IMAGENES_V1 --informe INVENTARIO_V1.json --salida PAQUETE_V1
```

`entradas.sha256` debe estar en la misma carpeta que el histograma; `fusionar_v1.py` y `bloque_v1.sbatch` lo dejan allí. Antes de liberar los temporales de SC3 se comprueban las copias con `sha256sum -c salida.sha256` en cada bloque.

Ni `bloque_v1.sbatch` ni `lanzar_v1.py` se han ejecutado en SC3. Se verificó la sintaxis (`bash -n`, `py_compile`), y `fusionar_v1.py` se probó con bloques sintéticos (dos bloques de una vista; suma y metadatos correctos). La primera ejecución real es la etapa P0.

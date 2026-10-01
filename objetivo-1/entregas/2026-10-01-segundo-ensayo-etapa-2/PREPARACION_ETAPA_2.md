# Preparación de la etapa 2 de OE1 (protocolo v1.1)

1 de octubre de 2026 (Colombia, UTC−5). Este documento registra la preparación que exige el [protocolo v1.1](../../PROTOCOLO_ETAPA_2_OE1_V1_1.md), sección 8. Se commitea antes del primer transporte.

| Elemento | Valor |
|---|---|
| Repositorio del director | `main` en `ae29a17` (protocolo, instrucciones y manifiesto). Huellas del plan verificadas: `corridas.csv` `6fa79254…`, `dimensionamiento.json` `a2c92493…` |
| Código | `muography-dl-reconstruction`, rama `oe1/stage2`, commit `d8ca749`, hijo directo de `3315f82` (herramientas de la etapa 1) |
| Binarios | A2 `a07d83c4…` (`fdaef4b`) y B2 `ae761866…` (`9bb43f3`), los de la etapa 1, sin recompilar |
| Entorno SC3 | Partición `legacy` (8 nodos de 24 CPU y 95,5 GB), módulos `gnu14/14.2.0` y `geant4/11.4.2`, Python 3.9.25 con numpy 1.23.5 |

## 1. Espacio, cuota y retención

El protocolo pide al menos 30 GiB libres y dentro de cuota. Esa ubicación **no existe** para este usuario:

- **`/home`** tiene una cuota de 20 GiB, con 19.888 MB ocupados y unos 593 MB libres (`quota -s` en [entorno.txt](preparacion/listas-congeladas/entorno.txt)).
- **Grupo SIMON:** no tiene carpeta propia en `/scratch` ni en `/mnt/san/scratch`; ahí solo hay carpetas de los grupos CAGE, students, FIRST, GIEMA y LEAM.
- **Disco local** del equipo de los estudiantes: 26,6 GB libres.
- **`/tmp` de los nodos de cálculo:** es `tmpfs` de 47 GB, respaldado por la memoria del nodo, y se pierde al terminar cada trabajo.

**Decisión de los estudiantes (1 de octubre):** ejecutar la etapa completa con una desviación **solo de almacenamiento**. El diseño científico no cambia: corridas, semillas, tamaño, controles e intervalo. El esquema es este:

1. Cada trabajo escribe listas y registros en el `/tmp` del nodo.
2. Comprime los registros por muón y las listas con `gzip -n`; el SHA-256 del CSV original queda en el `SHA256SUMS` de cada corrida.
3. Exporta los archivos uno por uno a un búfer en `~/oe1-trabajo/etapa2/salida`. Solo copia si después quedan al menos 150 MB de cuota libres, y nunca exporta dos trabajos a la vez.
4. En el equipo local, `pull_bundles.py` descarga cada archivo, verifica su SHA-256 y solo entonces lo borra de SC3.

**Retención:**
- los datos completos quedan en la carpeta local `para-drive-oe1-etapa2/`, hasta que los estudiantes los suban al almacenamiento compartido con su lista SHA-256;
- en SC3 quedan, en `~/oe1-trabajo/etapa2/registro/`, todos los archivos pequeños: estados, comandos, logs, metadatos, histogramas y análisis por bloque;
- en `/home` de SC3 no conocemos ninguna política de purga.

**Memoria:** como `/tmp` es `tmpfs`, lo que se escribe allí cuenta como memoria. Cada trabajo principal pide 80 GB, con unos 12 GB previstos en `/tmp` más 24 procesos de transporte.

## 2. Entorno, huellas y controles geométricos

Los ocho insumos congelados coinciden con [entradas-congeladas.sha256](preparacion/listas-congeladas/entradas-congeladas.check):
- binarios A2 y B2;
- catálogos `geo-train-06` `c8f6c135…` y `geo-train-01` `ff3c69ab…`;
- tablas `93ce67ab…`, `7161c8ad…` y `7ac4b6a9…`;
- máscara `R_int.mask.txt` `e76dcbe5…`.

K2 (`--check-geometry` con semilla 20260929), en el trabajo 30599:

| Binario | Caso | Estado | Solapes | ANOMALY-CSG (clipped=no) | G4Exception |
|---|---|---|---|---|---|
| A2 | geo-train-06 | OVERLAPS (solape histórico declarado) | 2 | 0 | 9 líneas |
| A2 | geo-train-01 | OK | 0 | 0 | 0 |
| B2 | geo-train-06 | OK | 0 | 2 (2) | 0 |
| B2 | geo-train-01 | OK | 0 | 0 | 0 |

## 3. Listas congeladas (trabajo SLURM 30599, guane02, 2 min 44 s)

- **Qué son:** las 27 listas del manifiesto, generadas con `--write-primaries`:
  - 24 de 1.000.000 primarios de `geo-train-06` (réplicas 101–124);
  - 3 de 100.000 de `geo-train-01` (réplicas 201–203).
  - Ocupan 3,56 GB en total.
- **A2 y B2 generan listas idénticas** (`cmp`), y sus sidecars solo difieren en `binary_sha256`.
- **`--check-primaries`:**
  - da salidas idénticas en A2 y en B2;
  - `status=OK` en las 27;
  - 27 FNV canónicos distintos;
  - `n=1000000` en las principales.
- **Validador de la etapa 1** (estructura, geometría y modelo de fuente):
  - veredicto OK en las 27 listas;
  - 22 pruebas por lista, 594 en total, ninguna con p < 1e-4;
  - p mínima: 0,0020 (`geo-train-06` r105).
  - No se regeneró ninguna lista.
- **Huellas:** [listas.sha256](preparacion/listas-congeladas/listas.sha256) (listas y sidecars); sidecars en [sidecars/](preparacion/listas-congeladas/sidecars/).
- **En los trabajos de transporte:** cada trabajo regenera sus listas con A2 y la misma semilla, y se detiene con código 4, sin transportar, si alguna lista o sidecar no tiene el SHA-256 congelado aquí.

## 4. Scripts, ensayo en seco y pruebas

Los scripts nuevos están en `d8ca749`. Los archivos de la etapa 1 no se modificaron: en SC3 son idénticos byte a byte a los de la etapa 1 (`principal.sbatch` `0a8d720e…`, `env_stage1.sh` `92603b63…`, `run_timed.py` `236b331c…`).

| Archivo | Función |
|---|---|
| `scripts/cluster/oe1_stage2/listas.sbatch` | Trabajo L de esta sección |
| `scripts/cluster/oe1_stage2/corridas.sbatch` | Un grupo de réplicas en un trabajo y un nodo. Regenera y verifica listas, ejecuta `run_one` de la etapa 1 sin cambios, analiza en el nodo, comprime y exporta |
| `scripts/cluster/oe1_stage2/pull_bundles.py` | Descarga local con verificación SHA-256 |
| `scripts/analysis/oe1_stage2_analysis.py` | `plan`, `block`, `controls` y `aggregate`. Reutiliza K6–K9 de la etapa 1 y la función `interval()` del calculador del director |
| `scripts/analysis/tests/test_oe1_stage2_analysis.py` | 12 pruebas |

- **Ensayo en seco:** [55 órdenes](preparacion/listas-congeladas/ensayo-en-seco-55-ordenes.txt), todas con SHA congelado; `plan` confirma 55 corridas, 48.700.000 transportes, 24.000.000 pares principales y 27 listas.
- **Pruebas del analizador:** las 12 pasan. Cubren:
  - el manifiesto del protocolo y una semilla alterada;
  - conteos nulos y una discordancia hacia R_int;
  - un ID repetido, filas faltantes y un histograma incorrecto (los tres bloquean el bloque);
  - controles idénticos y una diferencia A/B en `geo-train-01` (cierra la compuerta);
  - un bloque faltante o inválido, o controles fallidos (los tres dan «no interpretable»);
  - el intervalo, igual al del calculador del director.
- **Límite de eventos:** en modo lista, N es el número de filas, y `BeamOn(static_cast<G4int>(events))` (`muography_sim.cc:494`) admite hasta 2.147.483.647. Un millón por corrida está dentro del límite.

## 5. Recursos SLURM, concurrencia y recuperación

| Trabajo | Réplicas | Corridas | CPU / memoria / tiempo |
|---|---|---|---|
| C, controles | 201–203 y A/A de r201 | 7 | 8 / 16 GB / 30 min |
| M1 | 101–112 | 24 | 24 / 80 GB / 3 h |
| M2 | 113–124 | 24 | 24 / 80 GB / 3 h |

- **Concurrencia:** un proceso de un hilo por corrida, todos a la vez dentro del nodo (`xargs -P`), como en la etapa 1. A y B de cada bloque, y la repetición A/A, comparten nodo. No hay multihilo dentro del simulador.
- **Límites del QOS `normal`:** 4 trabajos y 4 nodos por usuario.
- **Orden:** primero C, que es la compuerta de K6, K7 y K8. Solo si pasa, se lanzan M1 y M2 a la vez, en dos nodos.
- **Recuperación:** un fallo se conserva y la unidad se relanza con las mismas entradas y semillas en `INTENTO` nuevo, sin reutilizar salidas parciales; los registros de todos los intentos se entregan. No se añaden bloques ni se cambia el tamaño según los resultados.

# Resultados del complemento R2-01: entrada al solape desde ambos lados

30 de septiembre de 2026 (Colombia, UTC−5). Diseño: [COMPLEMENTO_R2_01.md](../../COMPLEMENTO_R2_01.md), commit `7c1a4e2`. Responde al hallazgo R2-01 de la [revisión de la etapa 1](../../REVISION_ETAPA_1_2026-09-30.md).

## Resumen

- **B asigna toda la intersección Z al cuerpo denso (A1) también cuando el muón entra por el conducto.** En los 36 pares, la longitud en Z de B es la de A1. La longitud asignada a otro material no supera 9 × 10⁻¹⁴ m, frente a la tolerancia de 1 µm.
- **La entrada por el conducto quedó cubierta en transporte real.** En A, los IDs 0 a 5 entran a Z navegando el conducto (`mat_in = A0`, con `lz_a0_m = lz_m`) en las 3 semillas. Los IDs 6 a 11 entran por el cuerpo denso (`mat_in = A1`), como estaba planificado.
- **Diferencias entre A y B según el lado:**
  - del lado del conducto, A y B difieren en el material de Z (A0 frente a A1) y, en consecuencia, en la energía: B pierde más energía en 17 de 18 pares, con una mediana de 75 GeV;
  - del lado del cuerpo denso, A y B son idénticos en los 18 pares.
- **Efecto en la detección:** a 10 TeV, ningún muón cambia de detectado a no detectado entre A y B; 3 de los 18 pares del lado del conducto se desplazan un píxel. Con 12 trayectorias dirigidas no se estima la frecuencia del efecto ni su impacto en la imagen.

## 1. Identificación y ejecución

| Elemento | Valor |
|---|---|
| Commits | Repo del director `7c1a4e2`: diseño, insumos, generador y ejecutor. Código: A2 `fdaef4b`, B2 `9bb43f3` y comparación `0d97beb` ([`codigo/commits.txt`](codigo/commits.txt)) |
| Insumos | [Lista](../../ensayos/complemento-r2-01-v1/geo-train-06_v0_r10_r201.primarios.csv) `ae8318a7…` (12 μ⁻ de 10 TeV), metadatos `05457ab6…`, trayectorias esperadas `fdf3f7b5…`, ejecutor `d3a27235…`. Copiados a SC3 con `git archive` y comprobados con `sha256sum -c` ([`verificacion/insumos-sc3.sha256`](verificacion/insumos-sc3.sha256)) |
| Binarios y entradas fijas | A2 `a07d83c4…` y B2 `ae761866…` (los de la etapa 1, sin cambios); catálogo `c8f6c135…`; R_int `e76dcbe5…`; tablas `93ce67ab…`, `7161c8ad…` y `7ac4b6a9…`. El ejecutor los verificó antes de correr ([`entorno.txt`](corridas/intento-01/entorno.txt)) |
| Entorno | SC3, partición `legacy`, nodo guane01; módulos `gnu14/14.2.0` y `geant4/11.4.2`; `G4TaskRunManager` con un hilo trabajador |
| Trabajo SLURM | 30580. Enviado a las 21:43:52 y terminado a las 21:44:06, en 13 s; `COMPLETED 0:0` ([`slurm/sacct.txt`](slurm/sacct.txt), [`slurm/r201.sbatch`](slurm/r201.sbatch)) |
| Corridas | 6 (A2 y B2 × semillas 1026093011, 1026093012 y 1026093013), es decir 72 transportes, todas `PROCESO_OK` ([`estado.tsv`](corridas/intento-01/estado.tsv)) |
| Desviaciones | Ninguna respecto al diseño. Detalles de la ejecución: el sbatch es propio y solo carga los módulos de la etapa 1 y define las 7 variables del ejecutor; SLURM asignó 2 CPU lógicas a la petición de 1, pero los seis procesos son de un hilo y secuenciales. |

## 2. Verificación de las 12 rectas antes del transporte

La verificación es independiente del generador del director y usa la referencia analítica de cruces de los estudiantes ([`verificacion-geometrica-r201.json`](verificacion/verificacion-geometrica-r201.json)). Las 12 rectas cumplen lo siguiente:

- **Recorrido:** pasan por el centro del panel, parten a 1809,7 m de radio horizontal y atraviesan Z en profundidad.
- **Lado de entrada:** el planificado. IDs 0 a 5 desde el conducto, IDs 6 a 11 desde el cuerpo denso.
- **Medidas en Z:** la longitud va de 22,25 m a 42,41 m; la separación mínima entre las entradas a las dos primitivas es de 6,81 m (ID 1).
- **Sensibilidad:** las 720 rectas paralelas por trayectoria, desplazadas 2,5 cm y 5 cm en 360 direcciones, conservan el lado.
- **Coincidencia con el diseño:** las longitudes y los puntos de entrada y salida coinciden con `trayectorias-esperadas.json` dentro de 10⁻⁶ m.

El generador del director reproduce byte a byte los cuatro archivos de la lista ([`regeneracion-lista.txt`](verificacion/regeneracion-lista.txt)).

## 3. Contrato técnico

Resultado: OK, sin fallos bloqueantes ([`contratos-r201.json`](analisis/contratos-r201.json)).

- **A y B leen la misma lista.**
  - `check-A2.txt` y `check-B2.txt` son idénticos: `status=OK`, `n=12`, SHA-256 `ae8318a7…` y FNV `c11af894c81614a5`.
  - Las 72 filas registran esa huella de la lista.
  - El `prim_fnv` de cada ID coincide con el recalculado desde la lista.
- **Mismo estado inicial en cada par:** `prim_fnv` y `rng0` son iguales en los 36 pares.
- **Completitud de cada corrida:**
  - hay 12 IDs y no hay filas ABORTED ni archivos `.part`;
  - el histograma reconstruido desde las filas detectadas es igual a `hist.csv`;
  - `in_rint` coincide con el valor recalculado;
  - el `SHA256SUMS.txt` de cada corrida es correcto.
- **Avisos de geometría:** B no tiene `G4Exception`, `GeomVol1002` ni `GeomNav`. A muestra el aviso histórico `GeomVol1002`, que es el esperado.
- **Control que no aplica:** la comparación con la eficiencia de detección de la campaña se marca «no aplica», porque una lista dirigida de 10 TeV no es una muestra de la fuente.

## 4. Resultados por trayectoria

Cada fila resume las 3 semillas. Los rangos van de mínimo a máximo, y ΔE es la energía al salir de Z en B menos la de A. Los datos completos están en [`trayectorias-r201.csv`](analisis/trayectorias-r201.csv) (12 filas) y [`pares-r201.csv`](analisis/pares-r201.csv) (36 pares).

| ID | Lado de la recta | Lado observado en A | Material de Z en A | Material de Z en B | Longitud en Z (m) | ΔE B − A (GeV) | Detección A → B | Mismo píxel A/B |
|---|---|---|---|---|---|---|---|---|
| 0 | conducto | conducto (3/3) | A0 | A1 | 28,27 a 28,38 | −1228 a −11 | 1 → 1 (3/3) | 1/3 |
| 1 | conducto | conducto (3/3) | A0 | A1 | 31,94 a 31,99 | −51 a +87 | 1 → 1 (3/3) | 2/3 |
| 2 | conducto | conducto (3/3) | A0 | A1 | 25,42 a 25,54 | −2906 a −74 | 1 → 1 (3/3) | 3/3 |
| 3 | conducto | conducto (3/3) | A0 | A1 | 29,82 a 29,97 | −931 a −82 | 1 → 1 (3/3) | 3/3 |
| 4 | conducto | conducto (3/3) | A0 | A1 | 22,12 a 22,35 | −174 a −64 | 1 → 1 (3/3) | 3/3 |
| 5 | conducto | conducto (3/3) | A0 | A1 | 27,67 a 27,85 | −464 a −8 | 1 → 1 (3/3) | 3/3 |
| 6 | cuerpo denso | cuerpo denso (3/3) | A1 | A1 | 36,64 a 36,66 | 0 | 1 → 1 (3/3) | 3/3 |
| 7 | cuerpo denso | cuerpo denso (3/3) | A1 | A1 | 36,73 a 37,19 | 0 | 1 → 1 (2/3); 0 → 0 (1/3) | 2/2 detectados |
| 8 | cuerpo denso | cuerpo denso (3/3) | A1 | A1 | 40,85 a 40,87 | 0 | 1 → 1 (3/3) | 3/3 |
| 9 | cuerpo denso | cuerpo denso (3/3) | A1 | A1 | 40,92 a 40,94 | 0 | 1 → 1 (3/3) | 3/3 |
| 10 | cuerpo denso | cuerpo denso (3/3) | A1 | A1 | 42,32 a 42,32 | 0 | 1 → 1 (3/3) | 3/3 |
| 11 | cuerpo denso | cuerpo denso (3/3) | A1 | A1 | 42,41 a 42,41 | 0 | 1 → 1 (3/3) | 3/3 |

«Material de Z» indica a qué volumen asigna el registro toda la longitud en Z:
- **IDs 0 a 5:** en A, `lz_a0_m = lz_m`; en B, `lz_a1_m = lz_m`, con a lo sumo 9 × 10⁻¹⁴ m fuera de A1.
- **IDs 6 a 11:** `lz_a1_m = lz_m` en ambas variantes.

## 5. Lectura

- **Cobertura.** Las trayectorias transportadas conservan la entrada planificada en las 3 semillas. En A se distingue el lado por el material del primer tramo profundo en Z: A0 en los 18 pares del conducto y A1 en los 18 del cuerpo denso.
- **Material en B.** B asigna toda Z a A1 en los 36 pares, en ambos lados de entrada. No hizo falta recurrir a la escala de desplazamiento lateral para explicar ninguna diferencia.
- **Lado de entrada en B.** En el registro agregado de B no se observa, porque toda Z es A1. Se infiere de tres hechos:
  - el estado inicial común con A (`prim_fnv` y `rng0` iguales);
  - la separación de al menos 6,81 m entre las entradas a las dos primitivas;
  - un desplazamiento lateral cerca de Z de 0,0033 mm como máximo.
- **Diagnóstico de A.** Cuando el muón llega por el conducto, A asigna la intersección al conducto (A0, 1,832 g/cm³). B la asigna al cuerpo denso (A1, 3,285 g/cm³). Esa es la navegación defectuosa que motivó la corrección y no constituye una referencia física.
- **Energía.**
  - Del lado del conducto, B sale de Z con menos energía en 17 de 18 pares: mediana −75 GeV y rango de −2906 a +87 GeV. La dispersión es la de las pérdidas radiativas a energías de TeV.
  - La energía interpolada al entrar a Z difiere entre A y B hasta en 23 GeV (0,3 %). Se debe a que en B el conducto recortado añade una frontera y cambia los pasos previos a Z. Es un diagnóstico, no una medición exacta.
  - Del lado del cuerpo denso, la energía de entrada y de salida coincide exactamente en A y B.
- **Detección y píxel.**
  - Hay 35 pares detectados en ambas variantes.
  - El par restante (ID 7, semilla 1026093013) llegó a Z con 87 GeV, tras una pérdida catastrófica, y quedó capturado igual en A y en B.
  - Tres pares del conducto cambian un píxel después de divergir en Z: ID 0 en las semillas 1026093011 (acimut +1) y 1026093012 (elevación −1), e ID 1 en la semilla 1026093011 (acimut +1).
- **Longitud.**
  - Las longitudes de cuerda transportadas quedan dentro de ±0,6 % de la recta y dentro del rango de las rectas desplazadas 5 cm.
  - La excepción es el ID 7 en la semilla 1026093013 (+1,2 %, el muón de baja energía). Es un dato de diagnóstico.
- **Consistencia entre semillas.** Para los 12 IDs, en las 3 semillas se repiten:
  - el cruce,
  - el lado observado,
  - los materiales en Z.

  El píxel varía en un bin entre semillas en algunos IDs, y el ID 7 se captura en una de ellas. Ambas cosas responden al carácter aleatorio del transporte.

## 6. Límites

- **Alcance.** Las 12 trayectorias dirigidas de 10 TeV describen el mecanismo en esta zona; no son una muestra de la fuente. No se deriva una tasa ni un efecto sobre las imágenes, y estos datos no se agrupan con las 13 corridas de la etapa 1.
- **Lado en B.** Se infiere; no se observa en el registro agregado.
- **Longitudes y energías.** Las longitudes son de cuerdas de paso y las energías en los bordes de Z se interpolan dentro del paso. Ninguna es una reconstrucción exacta de la trayectoria.
- **Pasos cercanos a Z.** No se registraron. La revisión los pedía para R2-01, pero el complemento los deja condicionados a que el registro agregado no baste y prohíbe cambiar la instrumentación. En A, el registro agregado bastó para establecer la entrada.

## 7. Conclusión

Con la misma lista y el mismo estado aleatorio inicial en A y B, B asignó la intersección entre el conducto y el cuerpo denso al cuerpo denso en las 36 comparaciones, entrara el muón por el conducto o por el cuerpo denso. La geometría original la asignó al conducto en los 18 casos de entrada por el conducto y al cuerpo denso en los 18 de control, como se esperaba. La corrección cambia, por lo tanto, el material que atraviesan esos muones y su pérdida de energía en Z; a 10 TeV no cambia su detección y solo desplaza un píxel en 3 de 18 pares. Con esto quedan cubiertos los dos lados de entrada y documentada la asignación de material de B, que era lo que pedía R2-01. La frecuencia de estos cruces con la fuente representativa y su efecto en la imagen quedan para la etapa 2.

## Archivos

- [`corridas/intento-01/`](corridas/intento-01/): salida completa del ejecutor. Contiene `entorno.txt`, `check-A2.txt`, `check-B2.txt`, `estado.tsv` y `FINALIZADO.txt`. Cada una de las 6 corridas incluye `comando.txt`, `run.log`, `*_muones.csv`, `*_hist.csv`, `*.meta.json` y `SHA256SUMS.txt`.
- [`slurm/`](slurm/): sbatch, salida del trabajo 30580 y `sacct`.
- [`verificacion/`](verificacion/): verificación geométrica de las rectas, regeneración de la lista y huellas de los insumos copiados a SC3.
- [`analisis/`](analisis/): contratos, pares, trayectorias, resumen por lado y el comando de análisis.
- [`codigo/commits.txt`](codigo/commits.txt): commits y huellas de los binarios y del script de comparación.
- [`MANIFIESTO.sha256`](MANIFIESTO.sha256): SHA-256 de todos los archivos de esta carpeta.

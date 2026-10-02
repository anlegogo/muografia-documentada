# Resultados de la integración operativa en SC3

2026-10-02 (Colombia). Se atiende la [guía de la siguiente etapa](../../GUIA_SIGUIENTE_ETAPA_OE1.md): incorporar `main` en la rama de entrega, comprobar en SC3 las pruebas y el plan de lanzamiento del flujo nuevo, e incorporar al informe el [alcance acordado](../../DEFINICION_PRODUCTO_OE1.md) con sus limitaciones.

**No se transportaron muones ni se envió ningún trabajo de producción.** Conforme a la guía, no se repitió la prueba de los dos bloques, no se ejecutó C3 y el lanzador se usó sin `--enviar`. Las herramientas de la dirección se usaron sin modificar.

**Resultado.** Los tres pasos de la guía terminan con código de salida 0 en SC3. La revisión del plan de lanzamiento detectó, sin embargo, que los trabajos planificados habrían usado un intérprete sin NumPy y habrían fallado antes de simular (dificultad D-01). La causa está en el entorno del equipo y se corrigió allí; con la corrección, el cuerpo del script SLURM se reprodujo en un nodo de cómputo, sin `--ejecutar`, con resultado correcto.

## 1. Versiones

| Elemento | Valor |
|---|---|
| `main` (dirección) | `3178d837b9f017c713eb370123265d7c025d13dd`; cuatro commits nuevos desde `c4b6e4c`: `c55582b`, `9ad1ae0`, `9b944c2`, `3178d83` |
| Rama de entrega antes | `01a98718ba381797f6d4616e25d42ad533cad6f1` |
| Merge probado en SC3 | `c9442d67a4b504bee5f1691b5822659360c8fd9f` (`git merge --no-ff origin/main`, sin conflictos: `main` no modifica ningún archivo de esta carpeta y la rama solo modifica esta carpeta) |
| Réplica en SC3 | `~/oe1-trabajo/integracion-c9442d6/replica`, extraída con `git archive` de `c9442d6` (50 MB). Las 53 herramientas coinciden con los blobs de Git ([herramientas-vs-git.txt](datos/sc3/integracion-operativa-c9442d6/salidas/herramientas-vs-git.txt)) |
| Manifiesto del piloto | SHA-256 `36d072c16d4f51a1772984114c1ab9a873501aa4b17aab14562fb7272a6d9a8d` |
| Ficha operativa | SHA-256 `db9e5caab4c599afc00430452bea190eb2f50b1fa6a49cc5f027f3a5e6659e90` |
| Árbol de la receta | `~/oe1-trabajo/produccion-receta`: ejecutable `00145f7e…`, parche v3 `4e7b24dd…`, tres tablas, 19 geometrías y seis herramientas de ejecución; **30 de 30 huellas iguales a la ficha** ([ficha-vs-arbol.stdout.txt](datos/sc3/integracion-operativa-c9442d6/salidas/ficha-vs-arbol.stdout.txt)). El ejecutable no se recompiló |

## 2. Entorno

Nodo de acceso `guane.sc3.uis.edu.co`, usuario `dapintoo`, Linux 5.14.0-687.39.1.el9_8, SLURM 25.11.8. Tras `module purge; module load gnu14/14.2.0 geant4/11.4.2`, `module list` muestra solo esos dos módulos ([entorno.txt](datos/sc3/integracion-operativa-c9442d6/salidas/entorno.txt)).

| Componente | SC3 | Entorno de referencia de las herramientas |
|---|---|---|
| GCC | 14.2.0 | — |
| CMake | 3.31.8 | — |
| Geant4 | 11.4.2 | 11.4.2 (receta) |
| Python | 3.13.13 (`~/muography-train/venv`) | 3.12.14 |
| NumPy | 2.5.2 | 2.4.4 |
| SciPy | 1.18.1 | 1.18.1 |
| Matplotlib | 3.11.1 | 3.11.1 |

SciPy ya estaba en el entorno del proyecto; no se instaló nada. Python y NumPy difieren del entorno de referencia ([requirements-oe1-local.txt](../../../requirements-oe1-local.txt)); las 103 pruebas pasan con las versiones de SC3.

## 3. Resultado por paso

Tres ejecuciones consecutivas, cada una con su script, sus salidas y su inventario de huellas:

1. [integracion_operativa.sh](verificacion/integracion_operativa.sh): los pasos de la guía con sus comandos (12:49–12:50).
2. [diagnostico_interprete.sh](verificacion/diagnostico_interprete.sh): diagnóstico de D-01 (12:51).
3. [integracion_operativa_envoltorio.sh](verificacion/integracion_operativa_envoltorio.sh): los mismos pasos con la corrección del entorno (12:52–12:53).

Comandos de la primera ejecución, desde la raíz de la réplica (rutas absolutas en los archivos `*.comando.txt`):

```bash
PY="$HOME/muography-train/venv/bin/python"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
TEMPORAL="$HOME/muography-scratch/oe1-piloto-v2-intentos"
SALIDA="$HOME/muography-scratch/oe1-piloto-v2-publicados"
DISENO="$REPO/objetivo-1/evidencias/piloto-propuesto-siete-actividades"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
MAN="$DISENO/manifiesto-piloto-propuesto.csv"

srun -p legacy -N1 -n1 -c2 -t 00:10:00 "$PY" -m unittest discover -s herramientas -p 'test_*angular*.py' -v
"$PY" herramientas/preparar_campana_angular.py "$MAN" --geometrias geo-train-06 --informe "$OUT/preflight-piloto-v2.json"
"$PY" herramientas/operar_bloque_angular.py --manifiesto "$MAN" --fila 0 --arbol "$ARBOL" --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" --threads 24
"$PY" herramientas/lanzar_campana_angular.py --manifiesto "$MAN" --arbol "$ARBOL" --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" --python "$PY" --threads 24 --max-trabajos 4
```

En la tercera ejecución, `PY="$HOME/oe1-trabajo/entorno/python-oe1"`.

| Paso | Resultado | Veredicto |
|---|---|---|
| Pruebas unitarias (guía, paso 2) | Trabajo **30636** (`legacy`, guane02, 2 CPU, COMPLETED 0:0, 20 s): `Ran 103 tests in 12.422s`, `OK`. Con el envoltorio, trabajo **30640** (COMPLETED 0:0, 16 s): 103 pruebas, `OK` | Cumple |
| Preflight del manifiesto | Código 0, `errors: []`, 36 bloques, 6 vistas, 1.266.000.000 primarios, `technical_manifest_complete: true`. El informe es igual como JSON al [preflight de la dirección](../../evidencias/piloto-propuesto-siete-actividades/preflight.json); difiere solo en el salto de línea final (5.210 frente a 5.211 bytes). SHA-256 `f51b8212…` | Cumple |
| Worker en modo descripción (sin `--ejecutar`) | Código 0, `status: dry_run`; comprueba las huellas de ejecutable, parche, geometría, tablas y herramientas contra la ficha y describe el comando del simulador de la fila 0 | Cumple |
| Plan de lanzamiento (sin `--enviar`) | Código 0, `submitted: false`, `queue_jobs: 0`, `free_slots: 4`, filas 0–3 planificadas, `blocked_prior_attempts: []`, `verified: []` | Cumple como plan. El intérprete del comando planificado era incorrecto (D-01); corregido en la tercera ejecución |
| Aceptación de la cola (complemento) | `sbatch --test-only` sobre el comando planificado de la fila 0: código 0, «Job 30641 to start at 2026-10-02T12:52:59 a using 24 processors on nodes guane02 in partition legacy». No encola: `squeue` queda vacío y `sacct` no registra ese identificador | Cumple |
| Cuerpo de `bloque_verificado_angular.sbatch` en nodo de cómputo, sin `--ejecutar` (complemento) | Trabajo **30642** (guane02, COMPLETED 0:0, 1 s), desde el `--chdir` planificado y con los once argumentos planificados: módulos cargados, comprobación de `--sha-manifiesto` y `--sha-receta`, `status: dry_run` | Cumple |
| Envío, simulación, publicación, fusión, evaluación, exportación y empaquetado del piloto | No ejecutados (sección 5) | No ejecutado |

Los dos complementos no forman parte de la guía. Se añadieron para comprobar la interacción con SLURM y con los nodos de cómputo sin enviar trabajos ni transportar muones.

Al terminar, la cola del usuario está vacía y lo único nuevo bajo `~/muography-scratch` es el directorio vacío `oe1-piloto-v2-publicados.operacion/`, que crea el lanzador al consultar; no contiene `campaign.json`, registros de envío ni bloqueo ([estado-operacion.txt](datos/sc3/integracion-operativa-c9442d6/salidas-correccion/estado-operacion.txt)). No existen `oe1-piloto-v2-publicados/` ni `oe1-piloto-v2-intentos/`. El cómputo total usado fue de 39 s de reloj en trabajos de 2 CPU (30636, 30638, 30639, 30640 y 30642).

## 4. Plan de lanzamiento y metadatos

Comando planificado para la fila 0 tras la corrección ([lanzador.stdout.txt](datos/sc3/integracion-operativa-c9442d6/salidas-correccion/lanzador.stdout.txt), SHA-256 `f1ce5515…`):

```text
sbatch --parsable --job-name=oe1-2984cba98893-0 --partition=legacy --nodes=1 --ntasks=1
  --cpus-per-task=24 --time=00:55:00 --chdir=/home/dapintoo/oe1-trabajo/produccion-receta
  --output=/home/dapintoo/muography-scratch/oe1-piloto-v2-publicados.operacion/logs/%x-%j.out
  <réplica>/herramientas/bloque_verificado_angular.sbatch <manifiesto> 0 <árbol> <temporal> <salida>
  <ficha> /home/dapintoo/oe1-trabajo/entorno/python-oe1 24 <réplica>/herramientas/operar_bloque_angular.py
  36d072c1…9a8d db9e5caa…9e90
```

Comprobaciones sobre el plan, el manifiesto, el preflight y la ficha:

- **Rutas y huellas.** Las huellas del manifiesto y de la ficha que viajan en el comando son las de la sección 1. El árbol, las tablas y la geometría coinciden con la ficha.
- **Cola y cupos.** Cero trabajos propios, cuatro cupos, cuatro filas planificadas (0 a 3). Sin intentos previos ni bloques publicados.
- **Nombres.** `oe1-<12 hex de la identidad>-<fila>`. La identidad incluye las rutas y el intérprete: fue `c7468eb13461…` con la ruta resuelta del venv y `2984cba98893…` con el envoltorio (observación D-05).
- **Geometría, vistas, semillas y eventos.** El manifiesto tiene 36 filas de geo-train-06, vistas 0 a 5 con seis bloques cada una, 36 semillas distintas (de 20261002400000 a 20261002405005) y 35.166.667 o 35.166.665 primarios por bloque, que suman 211.000.000 por vista. El comando del worker para la fila 0 lleva `--view 0 --seed 20261002400000 --events 35166667 --threads 24` y las tablas `tables-az-edges-v1`, igual que el manifiesto.
- **Malla angular.** `meta.json` de las tablas registra `n_azimuth_columns = 256` entre −30° y +30° con la convención `az-edges-v1` (256 intervalos iguales de 60/256°) y `n_elevation_rows = 256`. La ficha fija la imagen en 256 × 256, `uint32`, con elevación `legacy-centers-2-47` (256 centros equiespaciados entre 2° y 47°).
- **Tiempo límite.** 55 min por bloque. El coste orientativo del diseño (187,26 h-núcleo para 36 bloques, con la tasa de c01) equivale a unos 13 min por bloque con 24 hilos. El rendimiento en geo-train-06 con la receta no está medido.

No hay histograma ni registro de simulación nuevos que contrastar, porque no se simuló. La coherencia entre histograma, metadatos y recibos quedó comprobada con dos bloques reales en el trabajo 30631 ([VERIFICACION_BLOQUES.md](VERIFICACION_BLOQUES.md)), y las 103 pruebas la cubren con dobles sintéticos.

## 5. Pasos no ejecutados

La guía reserva `--enviar` para después de acordar el diseño y el presupuesto del piloto, y la ficha registra `pilot_execution_authorized: false` y `production_authorized: false`. Por eso no se ejecutaron el envío, la simulación, la publicación, la fusión (`fusionar_bloques_angular.py`), la evaluación (`evaluar_piloto_angular.py`), la exportación ni el empaquetado del piloto: todos requieren bloques publicados. Quedan sin comprobar en SC3, con muones reales, la escritura concurrente de cuatro trabajos sobre el almacenamiento compartido, los registros de intención y los recibos del flujo nuevo, y el tiempo real por bloque.

## 6. Dificultades

| Id | Problema | Causa | Solución y estado |
|---|---|---|---|
| D-01 | El comando `sbatch` planificado llevaba como intérprete `/opt/ohpc/pub/software/conda_categories/machine_learning/bin/python3.13`, que no tiene NumPy, SciPy ni Matplotlib. Con ese intérprete el worker termina con código 1 (`ModuleNotFoundError: No module named 'numpy'`) y las pruebas dan `Ran 20 tests`, `FAILED (errors=12)` (trabajo **30639**, FAILED 1:0). Con `--enviar`, los cuatro trabajos habrían fallado antes de simular y sus filas habrían quedado en `blocked_prior_attempts`. Los tres pasos de la guía no lo detectan: todos devuelven 0 | El lanzador aplica `Path.resolve()` a `--python`. En el entorno del equipo, `venv/bin/python` es un enlace simbólico al intérprete base; al resolverlo se pierde el venv ([interprete.txt](datos/sc3/integracion-operativa-c9442d6/salidas-diagnostico/interprete.txt), trabajo **30638** en nodo de cómputo) | **Aplicada, en el entorno del equipo.** Envoltorio [python-oe1](verificacion/python-oe1) (archivo regular, SHA-256 `bbe37fee…`) instalado en `~/oe1-trabajo/entorno/`, que ejecuta el intérprete del venv y sobrevive a `resolve()`. Verificado: 103 pruebas (30640), plan con el envoltorio y cuerpo del sbatch en nodo (30642). Debe usarse como `--python` desde el primer envío, porque la ruta forma parte de la identidad de la campaña. Alternativa en la herramienta, no aplicada porque las herramientas recibidas no se modifican: que el lanzador conserve la ruta sin resolver o que el preflight compruebe las importaciones del intérprete planificado |
| D-02 | El venv no funciona desde el nodo `toctoc` (código 127) y allí no hay `squeue`, `sbatch`, `sacct` ni `srun` ([toctoc.txt](datos/sc3/integracion-operativa-c9442d6/toctoc.txt)) | El intérprete base del venv existe en `guane` y en el nodo de cómputo, no en `toctoc` | Todos los pasos se ejecutan desde `guane`. Resuelta por procedimiento |
| D-03 | No hay clon Git de la réplica en SC3 | El repositorio es privado y no se ha configurado un clon en el clúster | Copia con `git archive` del commit probado, con finales de línea LF, y comprobación de las 53 herramientas contra los blobs de Git. El directorio `integracion-c9442d6/replica` no se edita; sus rutas forman parte de la identidad de la campaña y deben mantenerse si se envía el piloto. Resuelta |
| D-04 | Python 3.13.13 y NumPy 2.5.2 en SC3, frente a 3.12.14 y 2.4.4 del entorno de referencia | Entorno preexistente del proyecto en SC3 | Registrado. Las 103 pruebas pasan; no se cambian versiones |
| D-05 | El preflight sugiere nombres `oe1-3351cc58a320-<fila>` y el lanzador usa `oe1-2984cba98893-<fila>` | Identidades distintas: la del preflight depende del manifiesto; la del lanzador incluye además ficha, herramientas, rutas, intérprete e hilos | Observación, sin corrección. Al conciliar con `squeue` y `sacct` deben usarse los nombres del lanzador |

## 7. Alcance acordado

El alcance acordado el 2026-10-02 es el idealizado de [DEFINICION_PRODUCTO_OE1.md](../../DEFINICION_PRODUCTO_OE1.md): el conjunto del OE1 está formado por **imágenes sintéticas de transmisión en escenarios volcánicos idealizados, con distintos niveles de conteo**. Esta definición sustituye, donde difieran, a la propuesta de [IMAGEN_FINAL_OBSERVABLE.md](IMAGEN_FINAL_OBSERVABLE.md): se conserva su opción (a), el estimador direccional, y dejan de ser requisito la opción derivada del detector y el control C3.

**Imagen de transmisión.** La magnitud de la imagen es el conteo direccional C_ij: una matriz de 256 × 256 enteros (`uint32`, sin saturación) en la que cada entrada cuenta los muones primarios que, tras atravesar el escenario, alcanzan el plano de registro con energía cinética mayor que 3 GeV y dirección final dentro del píxel. «Transmisión» designa la modalidad (muones que atraviesan el edificio, frente a la muografía por dispersión) y no una fracción calibrada.

- *Relación con el estimador direccional.* C_ij es el estimador de la opción (a): impactos nominales uniformes sobre un panel de 1,2 m, registro en un plano computacional de 600 m y clasificación por dirección de llegada. Su valor esperado sigue E[C_ij] = T · A⊥ · ΔΩ_ij · Φ_ij · ε_ij, con A⊥ = 1,44 m² normal a cada dirección.
- *Forma adimensional.* La respuesta normalizada ideal, C_ij / (N_generados · p_ideal,ij), usa la referencia de cielo tabulada sin transporte, con el mismo margen y el mismo corte. Reemplaza al cociente con la eficiencia de cielo extrapolada, que afectaba a las 28 filas por debajo de 6,94° y a 7.122 de los 16.322 píxeles de roca con columna de al menos 10.000 g/cm². Es un diagnóstico; no se presenta como transmisión física calibrada y no se recorta a [0, 1].
- *Relación con la exposición.* El simulador se ejecuta con N fijo y `exposure_days` permanece en −1. La escala es convencional: T = 30 d · `nominal_in_window` / 36.034.069,911914065, donde `nominal_in_window` cuenta los primarios generados dentro de la ventana nominal (probabilidad 0,6841 por primario transportado). Para una vista del piloto propuesto, 211.000.000 primarios corresponden a un valor esperado de unos 120 días convencionales. No son días de un detector real.

**Escenarios volcánicos idealizados.** 19 geometrías sintéticas (12 de entrenamiento, 3 de validación, 3 de prueba y 1 de generalización) con seis vistas cada una: 114 referencias. Cada una es un edificio cónico de roca de densidad uniforme; 18 contienen entre una y tres anomalías internas (conducto, cavidad o cuerpo denso) y una, geo-train-01, no contiene ninguna. Los 19 archivos del catálogo coinciden con las huellas de la ficha, y el transporte usa la geometría corregida. La idealización abarca el transporte y la fuente: Geant4 11.4.2 con FTFP_BERT y solo primarios; fuente híbrida con pesos de dirección derivados de Guan y cuantiles de momento de EcoMug, declarada como hipótesis del conjunto; inyección junto al cono, margen angular de 5° y malla `az-edges-v1`. No representan la topografía ni la estructura de un volcán concreto.

**Niveles de conteo.** Cada referencia se acompaña de realizaciones de menor conteo del mismo observable, obtenidas por submuestreo: adelgazamiento binomial por píxel, k_ij ~ Binomial(C_ij, f), con f = 0,5; 0,1; 0,05 y 0,01, y 20 realizaciones por fracción con semillas registradas: 114 × 4 × 20 = 9.120 pares. Una fracción f reduce en promedio los conteos y la exposición convencional por f. Las realizaciones están condicionadas a la misma referencia finita: no equivalen a corridas independientes de f·N primarios y la referencia no es una verdad sin ruido. Las geometrías se separan entre particiones antes de formar los pares.

**Relación con el OE1.** El objetivo pide un conjunto sintético de imágenes muográficas por transmisión con distintos niveles de estadística de conteo, obtenido por simulación Monte Carlo de escenarios volcánicos. El producto acordado cubre cada término: imagen de muones transmitidos, simulación Monte Carlo con Geant4, escenarios volcánicos sintéticos y niveles de conteo por submuestreo. Su uso es entrenar y evaluar la mejora de imágenes de bajo conteo frente a su referencia de conteo alto, tarea que depende de la estadística de conteo y de la estructura de la imagen, no de la calibración absoluta de un instrumento.

**Fuera del alcance.**

- La equivalencia con el detector físico de 1,2 m y el control C3; el plano de 600 m no se presenta como detector.
- Un flujo calibrado y una duración física de la exposición.
- Una referencia de cielo medida: la ideal no incluye pérdidas en aire, decaimiento, dispersión ni migración angular.
- Secundarios, fondo y respuesta instrumental (eficiencia, resolución, aceptación).
- La validación del modelo físico: el alcance acordado no la declara ni da por terminado el OE1.

Siguen vigentes, como limitaciones, la justificación de representatividad (A-02), el criterio de bordes con corte y la suficiencia de conteos en roca (A-05).

## 8. Pendientes y propuesta de continuación

Respecto de los [criterios A-01 a A-08](../../DEFINICION_PRODUCTO_OE1.md#lista-única-de-criterios-de-cierre): A-01, alcance incorporado en este informe; A-04, comprobado sin muones, con D-01 corregida y lo indicado en la sección 5 por comprobar. Los demás siguen abiertos.

Pendientes:

- D-01 y D-05: definir si el envoltorio se mantiene como requisito del entorno o si la corrección pasa al lanzador.
- Criterio de bordes, suficiencia de conteos en roca y presupuesto del piloto (geo-train-06, seis vistas, 36 bloques, 187 h-núcleo orientativas): la guía pide fijarlos antes de enviar.
- Representatividad de escenarios, fuente y transporte (A-02).
- El resumen, los pendientes y la propuesta del [README](README.md) y de [PLAN_PRODUCCION.md](PLAN_PRODUCCION.md) aún describen C3 y el piloto P0 anterior; deben actualizarse con el alcance acordado.

Propuesta para continuar, una vez fijados el criterio y el presupuesto del piloto:

1. Ejecutar el lanzador con `--enviar` y `--python ~/oe1-trabajo/entorno/python-oe1`, sin editar la réplica, el manifiesto, la ficha ni el ejecutable; repetirlo cuando haya cupos; conservar `.operacion`, recibos, registros y `sacct`.
2. Con todos los bloques publicados, ejecutar la fusión, la evaluación de las seis vistas, la exportación y el empaquetado con los comandos de la guía, y entregar tiempos, conteos en roca y evaluación.
3. Con el piloto evaluado, dimensionar la campaña de 114 referencias y 9.120 pares.

## 9. Evidencia

En [datos/sc3/integracion-operativa-c9442d6/](datos/sc3/integracion-operativa-c9442d6/), con los bytes de SC3:

| Carpeta o archivo | Contenido | SHA-256 |
|---|---|---|
| `salidas/` | Primera ejecución: 37 archivos | `salidas.sha256`: `14330a471eb0999df80fcb01f9610a165aa81d843b5f9c1c3469cb4684d6d456` |
| `salidas-diagnostico/` | Diagnóstico de D-01: 23 archivos | `salidas.sha256`: `ad90aa6324da69cf63b18ce94907dd81e947e2f5ab7f515ef1ba660ed1a5322c` |
| `salidas-correccion/` | Tercera ejecución: 30 archivos | `salidas.sha256`: `e016cb700a5688d30f6e7dc45b4c3b3146b3d60fdd37c55a7c0956ebcdcd6ff1` |
| `integracion_operativa.sh` | Script ejecutado | `2dec7b81a905c9639cb9d537b25b980477bb6efd62c49ae8010f7c77e12a1ee7` |
| `diagnostico_interprete.sh` | Script ejecutado | `6993437bdd7ef9bf0cb52657b9d86552c9057d8e9eec40cf71c8db1d10a842c8` |
| `integracion_operativa_envoltorio.sh` | Script ejecutado | `524882bbc20a5df46891b5722d37cec3e6aeabfcf6f0d7f56b118be622bb7d89` |
| `python-oe1` | Envoltorio instalado | `bbe37feefbbfb4802308247e481514698f6e9b294ea8999786118cd0f09d13e7` |
| `herramientas.git.sha256` | Huellas de los blobs de Git de `herramientas/` en `c9442d6` | `acf2de3854354f1370949514d13eff9ceb5c08df9ab37f7e8dabb81cea7bdb4e` |
| `toctoc.txt` | Comprobación de D-02 en el nodo `toctoc` (13:02) | `47c2f31bd780796e1a3769ccb1c13e93b445d75422bab3f3d18a55e8d1e90b06` |

Cada carpeta de salidas contiene, por paso, el comando (`*.comando.txt`), la salida estándar, la salida de error y el código de salida, además de `sacct.txt` y el estado de la cola antes y después. Los originales permanecen en `~/oe1-trabajo/integracion-c9442d6/` de SC3.

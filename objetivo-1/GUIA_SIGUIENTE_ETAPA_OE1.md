# Guía de la siguiente etapa para Daniel y Reinaldo

2026-10-02. Esta guía reúne las tareas posteriores a `01a9871`. **La prueba de los dos bloques ya fue aceptada; no deben repetirla ni producir muones para demostrarla otra vez.** El propósito siguiente es dejar el proceso automático funcionando y acordar una imagen con interpretación explícita, antes de producir las 114 vistas.

## Actividades inmediatas sin nuevas simulaciones

1. Incorporar la actualización de `main` en su rama de entrega y leer la [definición propuesta](DEFINICION_PRODUCTO_OE1.md). Dejar en el informe una respuesta explícita: adoptar el conjunto idealizado con sus limitaciones, o explicar por qué se necesita equivalencia con un detector. No basta cambiar el nombre del producto: justificar su relación con el OE1.
2. En su entorno Python del proyecto, ejecutar las pruebas abajo. No usan Geant4: el simulador y la cola de las pruebas son dobles sintéticos. Conservar versiones, salida completa y código de salida. Si falta SciPy, instalarlo en el entorno del proyecto, sin cambiar módulos o paquetes globales. Entorno local probado: Python 3.12.14, NumPy 2.4.4, SciPy 1.18.1; las versiones SC3 deben registrarse y verificarse, no presumirse equivalentes.
3. Revisar el plan de lanzamiento sin `--enviar`: comprobar rutas, huellas, trabajos ya en cola, cupos y nombres con identidad de campaña. Resolver cualquier discrepancia antes de pedir transporte. La ficha conserva el hash del ejecutable reportado por los estudiantes; si se recompiló, documentar código/parche/compilador y revisar la ficha como nueva versión, no reemplazar el hash solo para evitar el error.
4. Entregar un breve `RESULTADOS_INTEGRACION_OPERATIVA.md`: commit usado, entorno, resultado de pruebas, plan de lanzamiento, decisiones sobre el observable y limitaciones. No hace falta otra justificación extensa ni repetir las 19 corridas.

Desde la raíz de esta réplica en SC3 (sustituir las rutas por las reales):

```bash
set -euo pipefail
PY="$HOME/muography-train/venv/bin/python"
REPO="$PWD"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
TEMPORAL="$HOME/muography-scratch/oe1-piloto-v2-intentos"
SALIDA="$HOME/muography-scratch/oe1-piloto-v2-publicados"
DISENO="$REPO/objetivo-1/evidencias/piloto-propuesto-siete-actividades"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"

# Puede hacerse en una asignación corta; no transporta muones.
srun -p legacy -N1 -n1 -c2 -t 00:10:00 "$PY" -m unittest discover \
  -s herramientas -p 'test_*angular*.py' -v

"$PY" herramientas/preparar_campana_angular.py \
  "$DISENO/manifiesto-piloto-propuesto.csv" --geometrias geo-train-06 \
  --informe "$HOME/preflight-piloto-v2.json"

# Consulta squeue y describe sbatch; NO lo envía.
"$PY" herramientas/lanzar_campana_angular.py \
  --manifiesto "$DISENO/manifiesto-piloto-propuesto.csv" --arbol "$ARBOL" \
  --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" \
  --python "$PY" --threads 24 --max-trabajos 4
```

El preflight confirma estructura, no autorización física ni disponibilidad de recursos. Los nombres de informes deben ser nuevos. Registrar stdout/stderr y el código de salida; un archivo de log existente no prueba éxito.

## Cómo funciona el proceso preparado

El lanzador consulta la cola y hace una sola pasada, hasta el límite indicado. Una raíz de publicación queda vinculada a una configuración. Antes de omitir un bloque verifica sus datos y recibo completo. Antes de enviar una fila guarda la intención de envío; si `sbatch` responde de forma ambigua, conserva el registro y **no reenvía automáticamente**. No utiliza `CHAIN=1` ni rellena la cola desde un trabajo que acaba de fallar.

El worker comprueba ejecutable, parche, geometría, tablas y herramientas; elimina opciones `OE1C_` heredadas e impone la receta registrada. Ejecuta en una carpeta de intento nueva, conserva logs y metadatos originales, promueve el histograma con corte, cuenta la generación nominal, valida y publica con las herramientas ya probadas. Un error de simulación, corte, copia o publicación deja fallo, conserva el intento y no genera un bloque válido aparente. El script SLURM recibe la ruta absoluta del worker: no depende del directorio donde SLURM copie el `.sbatch`.

No editar el checkout, manifiesto, ficha o binario mientras haya trabajos enviados. Los hashes de manifiesto/ficha se verifican de nuevo al arrancar; la ficha verifica las dependencias del worker. Mantener el directorio `.operacion` junto a la salida: contiene identidad, intenciones, IDs de trabajo y logs.

Si aparece una fila en `blocked_prior_attempts`, revisar su registro y `sacct`/`squeue`. **No borrar el registro ni un bloqueo para intentar otra vez mientras exista posibilidad de que el trabajo siga activo.** Tras confirmar el estado terminal y la ausencia de publicación válida, conservar registro e intento fallido como evidencia y acordar un reintento explícito. No reintentar de forma ilimitada. No reemplazar un bloque publicado discrepante.

Las pruebas locales cubren esos casos con fallos simulados, pero no certifican las particularidades de permisos, almacenamiento compartido o SLURM de SC3. Esa verificación operativa es la tarea de esta etapa.

## Cuándo pasar al piloto con muones

Primero deben quedar acordados el producto, las limitaciones de la referencia ideal, el criterio de bordes y el presupuesto. **El manifiesto propuesto no es una orden de ejecución.** No lanzar C3 por defecto: su necesidad depende de la afirmación instrumental que se decida sostener.

Hay un piloto completamente especificado para valorar: geo-train-06, seis vistas, 211 millones de primarios por vista, 36 bloques en total; coste orientativo 187 horas-núcleo. El [diseño estadístico](DISENO_ESTADISTICO_Y_REFERENCIAS.md) explica por qué ese número es mayor que el piloto anterior y sus hipótesis. Es una opción conservadora, no un mínimo ni una promesa de resultado favorable.

Una vez aceptado ese alcance, el comando anterior con **`--enviar`** realiza los envíos que quepan. Repetir manualmente el lanzador cuando haya cupos para continuar las filas restantes; las filas ya registradas no se duplican. No cambiar semillas o N después de inspeccionar los bordes. No pasar de un piloto inconcluso a «seguir hasta aprobar».

## Qué entregar del piloto y cómo evaluarlo

Conservar los bloques completos, recibos, `.operacion`, manifiesto, ficha, entradas, comandos, logs y registros `sacct`. No subir resultados grandes sin su inventario de hashes y ubicación recuperable. En la rama de entrega, incluir la evaluación de las seis vistas y un resumen de tiempos, conteos en roca y decisiones.

Una vez publicados todos los bloques, crear destinos nuevos:

```bash
FUSION="$HOME/muography-scratch/oe1-piloto-v2-fusion"
"$PY" herramientas/fusionar_bloques_angular.py \
  --manifiesto "$DISENO/manifiesto-piloto-propuesto.csv" \
  --salida "$SALIDA" --destino "$FUSION"

"$PY" herramientas/evaluar_piloto_angular.py --fusion "$FUSION" \
  --diseno "$DISENO/diseno-piloto.json" \
  --referencia "$REPO/objetivo-1/evidencias/preparacion-siete-actividades/cielo-ideal-margen-5.json" \
  --salida "$HOME/evaluacion-piloto-v2.json"

IMAGENES="$HOME/muography-scratch/oe1-piloto-v2-imagenes"
"$PY" herramientas/preparar_imagen_angular_v1.py \
  "$FUSION"/geo-train-06/*_hist.csv --salida "$IMAGENES"
"$PY" herramientas/empaquetar_angular_v1.py "$IMAGENES" \
  --geometrias geo-train-06 --informe "$HOME/inventario-piloto-v2.json"
```

- **Equivalente:** el intervalo completo de cada región queda entre −1 y +1 pp bajo el contraste definido. Respalda ese criterio de respuesta, no todas las hipótesis físicas.
- **Inconcluso:** el intervalo cruza un límite. Entregarlo tal cual; revisar precisión/modelo antes de decidir más cómputo.
- **Fuera de tolerancia:** un intervalo queda completamente fuera. Revisar la causa; no corregir imágenes por multiplicadores elegidos para hacerlas pasar.

En cualquier caso se revisan las seis vistas, la estadística en roca y los tiempos reales. **No hay salto automático a las 114 vistas.** Si el piloto es aceptado, la siguiente decisión es el tamaño de la campaña; después se producen, auditan y documentan las 114 referencias y sus 9.120 pares.

## Reproducción local de la preparación realizada

`ENTREGA` es una extracción de la entrega congelada en `01a9871`; `TABLAS` son `tables-az-edges-v1` con los hashes de la ficha, no las tablas azimutales históricas. Los originales se conservan en esta réplica. Desde su raíz:

```bash
"$PY" herramientas/analizar_preparacion_angular.py --entrega "$ENTREGA" \
  --tablas "$TABLAS" --originales objetivo-1/originales/scripts --salida NUEVO_ANALISIS
"$PY" herramientas/preparar_piloto_angular.py --tablas "$TABLAS" \
  --geometria objetivo-1/originales/scripts/simulation/geometry_catalog/geometries/geo-train-06.json \
  --helper "$ENTREGA/scripts/comun.py" --salida NUEVO_DISENO
```

No se necesita ejecutar estos análisis otra vez en SC3 para aceptar las mismas cifras: se incluyen para reproducibilidad y para distinguir los cálculos locales de las tareas operativas pendientes.

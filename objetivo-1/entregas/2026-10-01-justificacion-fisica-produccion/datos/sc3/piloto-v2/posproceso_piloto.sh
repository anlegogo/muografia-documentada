#!/bin/bash
# Post-processing of the geo-train-06 pilot with the director's tools (c9442d6,
# unmodified), in the order and with the commands of GUIA_SIGUIENTE_ETAPA_OE1.md:
# fusion, evaluation of the six views, export and packaging. All destinations are
# new. Run on guane after the 36 blocks are published:
#   bash -l posproceso_piloto.sh
set -uo pipefail
BASE="$HOME/oe1-trabajo/integracion-c9442d6"
REPO="$BASE/replica"
OUT="$BASE/piloto-resultados"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
SALIDA="$HOME/muography-scratch/oe1-piloto-v2-publicados"
FUSION="$HOME/muography-scratch/oe1-piloto-v2-fusion"
IMAGENES="$HOME/muography-scratch/oe1-piloto-v2-imagenes"
DISENO="$REPO/objetivo-1/evidencias/piloto-propuesto-siete-actividades"
MAN="$DISENO/manifiesto-piloto-propuesto.csv"
cd "$REPO" || exit 2
for d in "$OUT" "$FUSION" "$IMAGENES"; do test ! -e "$d" || { echo "$d ya existe"; exit 2; }; done
mkdir -p "$OUT"
type module >/dev/null 2>&1 || source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2
{
  date '+%Y-%m-%dT%H:%M:%S%z'; echo "node=$(hostname)"; module list 2>&1
  "$PY" -c "import sys, numpy, scipy; print('python', sys.version.split()[0]); print('numpy', numpy.__version__); print('scipy', scipy.__version__)"
} > "$OUT/entorno.txt" 2>&1
(cd herramientas && sha256sum -c "$BASE/herramientas.git.sha256") > "$OUT/herramientas-vs-git.txt" 2>&1

run() {  # name, command...
  local n="$1"; shift
  printf '%q ' "$@" > "$OUT/$n.comando.txt"; echo >> "$OUT/$n.comando.txt"
  "$@" > "$OUT/$n.stdout.txt" 2> "$OUT/$n.stderr.txt"
  echo $? > "$OUT/$n.exit_code.txt"
  echo "$n exit=$(cat "$OUT/$n.exit_code.txt")"
}

run fusion "$PY" herramientas/fusionar_bloques_angular.py --manifiesto "$MAN" --salida "$SALIDA" --destino "$FUSION"
run evaluacion "$PY" herramientas/evaluar_piloto_angular.py --fusion "$FUSION" --diseno "$DISENO/diseno-piloto.json" \
  --referencia "$REPO/objetivo-1/evidencias/preparacion-siete-actividades/cielo-ideal-margen-5.json" \
  --salida "$OUT/evaluacion-piloto-v2.json"
run exportacion "$PY" herramientas/preparar_imagen_angular_v1.py "$FUSION"/geo-train-06/*_hist.csv --salida "$IMAGENES"
run empaquetado "$PY" herramientas/empaquetar_angular_v1.py "$IMAGENES" --geometrias geo-train-06 --informe "$OUT/inventario-piloto-v2.json"

sacct -X -S 2026-10-02T13:00 -u "$(id -un)" -P -o JobID,JobName,Partition,AllocCPUS,State,ExitCode,Elapsed,Start,End,NodeList \
  --name="$(seq -s, -f 'oe1-2984cba98893-%g' 0 35)" > "$OUT/sacct-piloto.txt" 2>&1
cp -r "$SALIDA.operacion" "$OUT/operacion"
(cd "$SALIDA" && find . -type f | sort | xargs sha256sum) > "$OUT/bloques-publicados.sha256"
(cd "$FUSION" && find . -type f | sort | xargs sha256sum) > "$OUT/fusion.sha256"
(cd "$IMAGENES" && find . -type f | sort | xargs sha256sum) > "$OUT/imagenes.sha256"
find "$FUSION" "$IMAGENES" -maxdepth 1 -type f -name '*.json' -exec cp {} "$OUT/" \;
(cd "$OUT" && find . -type f ! -name salidas.sha256 | sort | xargs sha256sum) > "$OUT/salidas.sha256"
du -sh "$SALIDA" "$FUSION" "$IMAGENES" > "$OUT/tamanos.txt"

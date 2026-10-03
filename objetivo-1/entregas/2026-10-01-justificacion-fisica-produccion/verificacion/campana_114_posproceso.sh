#!/bin/bash
# Post-processing of the 114-view campaign with the director's tools (replica
# 7c120ce, unmodified), in the order and with the commands of
# PREPARACION_CAMPANA_114.md section 7: fusion, evaluation of the 114 views,
# export and inventory. Pairs are NOT formed here (they are formed after the
# quality review, with NumPy 2.4.4). All destinations are new.
# Run on guane once the 1,026 blocks are verified:
#   bash -l campana_114_posproceso.sh
set -uo pipefail
BASE="$HOME/oe1-trabajo/campana-114-7c120ce"
REPO="$BASE/replica"
OUT="$BASE/posproceso"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
PLAN="$REPO/objetivo-1/evidencias/preparacion-campana-114"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
REF="$REPO/objetivo-1/evidencias/preparacion-siete-actividades/cielo-ideal-margen-5.json"
SALIDA="$HOME/muography-scratch/oe1-114-344M-publicados"
FUSION="$HOME/muography-scratch/oe1-114-344M-fusion"
IMAGENES="$HOME/muography-scratch/oe1-114-344M-imagenes"
cd "$REPO" || exit 2
pgrep -f "^bash -l campana_114_lanzar_v[0-9].sh ciclo" && { echo "el ciclo de envio sigue activo"; exit 2; }
test -z "$(squeue -h -u "$(id -un)")" || { echo "hay trabajos en cola"; exit 2; }
for d in "$OUT" "$FUSION" "$IMAGENES"; do test ! -e "$d" || { echo "$d ya existe"; exit 2; }; done
mkdir -p "$OUT"
type module >/dev/null 2>&1 || source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2
{
  date '+%Y-%m-%dT%H:%M:%S%z'; echo "node=$(hostname)"; module list 2>&1
  "$PY" -c "import sys, numpy, scipy; print('python', sys.version.split()[0]); print('numpy', numpy.__version__); print('scipy', scipy.__version__)"
  quota -s 2>&1 | tail -1
} > "$OUT/entorno.txt" 2>&1
(cd herramientas && sha256sum -c "$BASE/herramientas.git.sha256") > "$OUT/herramientas-vs-git.txt" 2>&1

run() {  # name, command...
  local n="$1"; shift
  printf '%q ' "$@" > "$OUT/$n.comando.txt"; echo >> "$OUT/$n.comando.txt"
  local t0; t0=$(date +%s)
  "$@" > "$OUT/$n.stdout.txt" 2> "$OUT/$n.stderr.txt"
  echo $? > "$OUT/$n.exit_code.txt"
  echo "$n exit=$(cat "$OUT/$n.exit_code.txt") segundos=$(( $(date +%s) - t0 ))"
}

run fusion "$PY" herramientas/fusionar_bloques_angular.py --manifiesto "$PLAN/manifiesto-114-344M.csv" --salida "$SALIDA" --destino "$FUSION"
run evaluacion "$PY" herramientas/evaluar_campana_114.py --fusion "$FUSION" --plan "$PLAN/plan.json" --receta "$RECETA" \
  --referencia "$REF" --salida "$OUT/evaluacion-114-344M.json"
run exportacion "$PY" herramientas/preparar_imagen_angular_v1.py "$FUSION"/*/*_hist.csv --salida "$IMAGENES"
run inventario "$PY" herramientas/empaquetar_angular_v1.py "$IMAGENES" --informe "$OUT/inventario-114-344M.json"

sacct -X -S 2026-10-02T18:00 -u "$(id -un)" -P -o JobID,JobName,Partition,AllocCPUS,ReqMem,State,ExitCode,Elapsed,Start,End,NodeList \
  > "$OUT/sacct-campana.txt" 2>&1
(cd "$SALIDA" && find . -type f | sort | xargs sha256sum) > "$OUT/bloques-publicados.sha256"
(cd "$FUSION" && find . -type f | sort | xargs sha256sum) > "$OUT/fusion.sha256"
(cd "$IMAGENES" && find . -type f | sort | xargs sha256sum) > "$OUT/imagenes.sha256"
du -sh "$SALIDA" "$FUSION" "$IMAGENES" > "$OUT/tamanos.txt"
(cd "$OUT" && find . -type f ! -name salidas.sha256 | sort | xargs sha256sum) > "$OUT/salidas.sha256"

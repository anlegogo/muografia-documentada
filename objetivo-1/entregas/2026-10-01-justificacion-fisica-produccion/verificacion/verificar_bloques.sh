#!/bin/bash
# Verification of the two existing integration blocks (rows 108 and 109,
# geo-train-06 view 0) with the director's tools at commit c4b6e4c, used
# unmodified. No muon is simulated. Run on guane:
#   srun -p legacy -N1 -n1 -c2 -t 00:10:00 --job-name=oe1-verificacion bash verificar_bloques.sh
set -uo pipefail
RAIZ="$HOME/oe1-trabajo/verificacion-c4b6e4c"
PY="$HOME/muography-train/venv/bin/python"
MAN="$HOME/oe1-trabajo/produccion-v1/manifiesto-prueba.csv"
BLOQUES="$HOME/muography-scratch/oe1-v1-prueba"
OUT="$RAIZ/salidas"
PUB="$HOME/muography-scratch/oe1-v1-prueba-publicados-c4b6e4c"
cd "$RAIZ" || exit 2
test ! -e "$OUT" || { echo "salidas/ ya existe"; exit 2; }
test ! -e "$PUB" || { echo "$PUB ya existe"; exit 2; }
mkdir -p "$OUT"
{
  date -u
  echo "job=${SLURM_JOB_ID:-sin-slurm} node=$(hostname) cwd=$RAIZ"
  module list 2>&1
  "$PY" --version
  "$PY" -c "import numpy, sys; print('numpy', numpy.__version__); print(sys.executable)"
} > "$OUT/entorno.txt" 2>&1
(cd herramientas && sha256sum *.py) > "$OUT/herramientas.sha256"
sha256sum "$MAN" > "$OUT/manifiesto.sha256"
find "$BLOQUES" -type f | sort | xargs sha256sum > "$OUT/bloques.sha256"
run() {  # name, command...
  local n="$1"; shift
  printf '%q ' "$@" > "$OUT/$n.comando.txt"; echo >> "$OUT/$n.comando.txt"
  "$@" > "$OUT/$n.stdout.json" 2> "$OUT/$n.stderr.txt"
  echo $? > "$OUT/$n.exit_code.txt"
  echo "$n exit=$(cat "$OUT/$n.exit_code.txt")"
}
run fusion "$PY" herramientas/fusionar_bloques_angular.py --manifiesto "$MAN" --salida "$BLOQUES" --destino "$OUT/fusion"
run exportacion "$PY" herramientas/preparar_imagen_angular_v1.py "$OUT/fusion/geo-train-06/geo-train-06_view0_hist.csv" --salida "$OUT/imagenes"
run publicacion-108 "$PY" herramientas/publicar_bloque_angular.py --manifiesto "$MAN" --fila 108 --origen "$BLOQUES" --destino "$PUB"
run publicacion-109 "$PY" herramientas/publicar_bloque_angular.py --manifiesto "$MAN" --fila 109 --origen "$BLOQUES" --destino "$PUB"
run publicacion-108-repetida "$PY" herramientas/publicar_bloque_angular.py --manifiesto "$MAN" --fila 108 --origen "$BLOQUES" --destino "$PUB"
find "$BLOQUES" -type f | sort | xargs sha256sum > "$OUT/bloques-despues.sha256"
cmp -s "$OUT/bloques.sha256" "$OUT/bloques-despues.sha256" && echo "bloques sin cambios" || echo "BLOQUES CAMBIARON"
find "$PUB" -type f | sort | xargs sha256sum > "$OUT/publicados.sha256"

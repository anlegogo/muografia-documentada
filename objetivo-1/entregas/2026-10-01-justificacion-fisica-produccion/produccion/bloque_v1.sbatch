#!/bin/bash
#SBATCH --job-name=oe1v1
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --time=00:55:00
#SBATCH --output=logs/%x-%j.out
# Production block for the az-edges-v1 image set (one manifest row).
# Not executed in this delivery. Run from the angular-v1 source tree
# (commit 0dea8e1, binary build-az-edges-v1) once the checks of
# PUNTOS_NO_DEMOSTRADOS.md that gate production are closed.
#
# Required exported variables:
#   MANIFIESTO  absolute path to manifiesto-v1-k*.csv
#   FILA        row index in the manifest
#   SALIDA      absolute output root (one directory per geometry/view/block)
# Optional: CHAIN=1 to refill the queue through lanzar_v1.py at the end.

set -uo pipefail
: "${MANIFIESTO:?}" "${FILA:?}" "${SALIDA:?}"
ARBOL="${ARBOL:-$HOME/oe1-trabajo/angular-v1}"
cd "$ARBOL" || exit 2
module purge
module load gnu14/14.2.0 geant4/11.4.2

IFS=, read -r fila geo vista bloque semilla eventos < <(awk -F, -v f="$FILA" 'NR > 1 && $1 == f' "$MANIFIESTO")
[[ "${fila:-}" == "$FILA" ]] || { echo "fila $FILA ausente en $MANIFIESTO"; exit 2; }

DEST="$SALIDA/$geo/view$vista/block$(printf '%04d' "$bloque")"
if [[ -f "$DEST/exit_code.txt" && "$(cat "$DEST/exit_code.txt")" == "0" && -f "$DEST/salida.sha256" ]]; then
  echo "bloque ya publicado: $DEST"
  exit 0
fi
TMP="$SALIDA/.tmp/$geo-view$vista-block$bloque-$SLURM_JOB_ID"
mkdir -p "$TMP" logs

BIN=build-az-edges-v1/muography_sim
TAB=scripts/simulation/geant4_app/tables-az-edges-v1
GEOJ=scripts/simulation/geometry_catalog/geometries/$geo.json
{
  date -u
  echo "job=$SLURM_JOB_ID node=$(hostname) fila=$FILA cwd=$(pwd)"
  module list 2>&1
  geant4-config --version
  c++ --version | head -1
} > "$TMP/entorno.txt" 2>&1
sha256sum "$BIN" "$GEOJ" "$TAB"/meta.json "$TAB"/row_weights_30d.txt "$TAB"/p_cdf.txt > "$TMP/entradas.sha256"
CMD=("$BIN" --geometry "$GEOJ" --view "$vista" --tables "$TAB" --seed "$semilla"
     --events "$eventos" --threads "$SLURM_CPUS_PER_TASK" --out "$TMP")
printf '%q ' "${CMD[@]}" > "$TMP/comando.txt"
echo >> "$TMP/comando.txt"

"${CMD[@]}" > "$TMP/run.log" 2>&1
estado=$?
echo "$estado" > "$TMP/exit_code.txt"

if [[ $estado -eq 0 ]]; then
  sha256sum "$TMP/${geo}_view${vista}_hist.csv" "$TMP/${geo}_view${vista}.meta.json" > "$TMP/salida.sha256"
  mkdir -p "$(dirname "$DEST")"
  [[ -e "$DEST" ]] && mv "$DEST" "$DEST.intento-previo-$SLURM_JOB_ID"
  mv "$TMP" "$DEST"
  echo "bloque publicado: $DEST"
else
  echo "simulador terminó con código $estado; se conserva $TMP"
fi

if [[ "${CHAIN:-0}" == "1" ]]; then
  python3 "$(dirname "$MANIFIESTO")/lanzar_v1.py" --manifiesto "$MANIFIESTO" --salida "$SALIDA" \
      --excluir-job "$SLURM_JOB_ID" || true
fi
exit "$estado"

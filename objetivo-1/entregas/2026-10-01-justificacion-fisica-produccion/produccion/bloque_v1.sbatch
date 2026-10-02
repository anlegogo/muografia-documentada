#!/bin/bash
#SBATCH --job-name=oe1v1
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --time=00:55:00
#SBATCH --output=logs/%x-%j.out
# Production block for the az-edges-v1 image set (one manifest row) with the
# recipe validated by checks C1, C2, C4 and C5 (jobs 30621-30626):
# injection 1 m before the line of sight enters rock, 5 deg generation
# margin, 600 m counting plane and kinetic-energy cut E > 3 GeV at the plane.
# The cut histogram becomes <stem>_hist.csv (reference image); the uncut
# histogram is kept as <stem>_hist_sin_corte.csv. Not executed in this delivery.
# ARBOL: angular-v1 tree (commit 0dea8e1) with controles/controles-oe1-v3.patch
# applied and built in build-receta/ (see PLAN_PRODUCCION.md, section 4).
#
# Required exported variables:
#   MANIFIESTO  absolute path to manifiesto-receta-k*.csv
#   FILA        row index in the manifest
#   SALIDA      absolute output root (one directory per geometry/view/block)
# Optional: CHAIN=1 to refill the queue through lanzar_v1.py at the end.

set -uo pipefail
: "${MANIFIESTO:?}" "${FILA:?}" "${SALIDA:?}"
ARBOL="${ARBOL:-$HOME/oe1-trabajo/produccion-receta}"
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

BIN=build-receta/muography_sim
export OE1C_INJECT=cone OE1C_MARGIN_DEG=5 OE1C_PLANE_HALF_M=300 OE1C_ECUTS_GEV=3
TAB=scripts/simulation/geant4_app/tables-az-edges-v1
GEOJ=scripts/simulation/geometry_catalog/geometries/$geo.json
{
  date -u
  echo "job=$SLURM_JOB_ID node=$(hostname) fila=$FILA cwd=$(pwd)"
  module list 2>&1
  geant4-config --version
  c++ --version | head -1
} > "$TMP/entorno.txt" 2>&1
sha256sum "$BIN" "$GEOJ" "$TAB"/meta.json "$TAB"/row_weights_30d.txt "$TAB"/p_cdf.txt controles-oe1-v3.patch > "$TMP/entradas.sha256"
env | grep '^OE1C_' | sort > "$TMP/receta.env"
CMD=("$BIN" --geometry "$GEOJ" --view "$vista" --tables "$TAB" --seed "$semilla"
     --events "$eventos" --threads "$SLURM_CPUS_PER_TASK" --out "$TMP")
printf '%q ' "${CMD[@]}" > "$TMP/comando.txt"
echo >> "$TMP/comando.txt"

"${CMD[@]}" > "$TMP/run.log" 2>&1
estado=$?
echo "$estado" > "$TMP/exit_code.txt"

if [[ $estado -eq 0 ]]; then
  # promote the E > 3 GeV histogram to reference image and keep metadata consistent
  mv "$TMP/${geo}_view${vista}_hist.csv" "$TMP/${geo}_view${vista}_hist_sin_corte.csv"
  mv "$TMP/${geo}_view${vista}_hist_ecut3.csv" "$TMP/${geo}_view${vista}_hist.csv"
  python3 - "$TMP/${geo}_view${vista}_hist.csv" "$TMP/${geo}_view${vista}.meta.json" <<'PY' || estado=5
import json, sys
total = sum(int(v) for line in open(sys.argv[1]) for v in line.split(","))
meta = json.load(open(sys.argv[2]))
meta["detected_all_energies"] = meta["detected_in_bins"]
meta["detected_in_bins"] = total
meta["reference_histogram"] = "kinetic energy at the counting plane > 3 GeV"
json.dump(meta, open(sys.argv[2], "w"), indent=1)
PY
  echo "$estado" > "$TMP/exit_code.txt"
fi
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

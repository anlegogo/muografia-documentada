#!/bin/bash
#SBATCH --job-name=muo-smoke
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=00:55:00
#SBATCH --output=%x-%j.out
# Optional (fill before submitting):
# #SBATCH --mail-type=END,FAIL
# #SBATCH --mail-user=your_email@correo.uis.edu.co

# Smoke test: one catalog geometry, small event count, timing measurement.
# Submit from $MUOGRAPHY_SIM_HOME:  sbatch cluster/sc3/smoke_test.sbatch

set -euo pipefail
source "$SLURM_SUBMIT_DIR/cluster/sc3/env.sh"

GEO="${GEO:-geo-train-01}"
VIEW="${VIEW:-0}"
SEED="${SEED:-20260805}"
# Either a fixed EVENTS count (benchmark) or DAYS of calibrated exposure.
EVENTS="${EVENTS:-}"
DAYS="${DAYS:-}"
if [[ -z "$EVENTS" && -z "$DAYS" ]]; then EVENTS=100000; fi
BUDGET_ARGS=()
[[ -n "$EVENTS" ]] && BUDGET_ARGS+=(--events "$EVENTS")
[[ -n "$DAYS" ]] && BUDGET_ARGS+=(--days "$DAYS")

RUN_DIR="$MUOGRAPHY_SCRATCH/smoke-$SLURM_JOB_ID"
mkdir -p "$RUN_DIR"
cd "$RUN_DIR"

BIN="$SLURM_SUBMIT_DIR/build_sc3/muography_sim"
CATALOG="$SLURM_SUBMIT_DIR/simulation/geometry_catalog/geometries"
TABLES="$SLURM_SUBMIT_DIR/simulation/geant4_app/tables"

echo "node=$(hostname) geo=$GEO view=$VIEW events=${EVENTS:-auto} days=${DAYS:--} seed=$SEED threads=$SLURM_CPUS_PER_TASK"
time "$BIN" --geometry "$CATALOG/$GEO.json" --view "$VIEW" \
     --tables "$TABLES" "${BUDGET_ARGS[@]}" --seed "$SEED" --out "$RUN_DIR" \
     --threads "$SLURM_CPUS_PER_TASK"

ls -la "$RUN_DIR"
# Keep results: copy back to home (scratch is purged automatically)
DEST="$SLURM_SUBMIT_DIR/results/smoke-$SLURM_JOB_ID"
mkdir -p "$DEST"
cp "$RUN_DIR"/*.csv "$RUN_DIR"/*.json "$DEST/"
echo "results copied to $DEST"

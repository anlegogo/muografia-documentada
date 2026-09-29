#!/bin/bash
#SBATCH --job-name=oe1-ctrl-t2t4
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=00:55:00
#SBATCH --output=/home/dapintoo/oe1-trabajo/salidas/control-geometrico/slurm/%x-%j.out

# Plan step 3, work unit U7, tasks T2 and T4 (geo-train-06 only), variants
# A and B. T2: --dump-geometry --volume-stat + 7 probes + 2 slices (view 0
# — the diagnostic targets the edifice/anomaly geometry, which is not
# rotated by --view, so a single view is representative and used for both
# variants; recorded here explicitly since the task text does not pin a
# view for T2). T4: normal run, geo-train-06 view 0, 10000 events, 8
# threads, seed 2026092900, for B (locked criterion) and A (reference —
# A is expected to print GeomVol1002 at construction).

ROOT="$HOME/oe1-trabajo"
CATALOGO="$ROOT/catalogo"
TABLAS="$ROOT/tablas"
OUT="$ROOT/salidas/control-geometrico"
REG="$OUT/registro-t2-t4.txt"
GEO="geo-train-06"
GEO_JSON="$CATALOGO/${GEO}.json"
VIEW=0
SEED_DIAG=20260929
SEED_T4=2026092900
EVENTS_T4=10000
THREADS_T4=8
VOLSTAT_N=10000000

mkdir -p "$OUT/t2/A" "$OUT/t2/B" "$OUT/t4/A" "$OUT/t4/B" "$OUT/slurm"

source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2

set -u
set -o pipefail

BIN_A="$ROOT/build-A/muography_sim"
BIN_B="$ROOT/build-B/muography_sim"

PROBES=(
  "21.354,-30.722,137.795"
  "20.3,-24.5,300"
  "20.3,-24.5,40"
  "21.35,-30.7,90"
  "32.2,-130,137.8"
  "200,0,50"
  "0,0,420"
)
SLICE_Y="-30.7:-150:150:0:420:1"
SLICE_Z="137.8:-150:150:-200:150:1"

{
  echo "=== oe1-ctrl-t2t4 (T2, T4) — $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  echo "job_id=${SLURM_JOB_ID:-none} node=$(hostname)"
  echo "--- module list ---"
  module list 2>&1
  echo "--- geant4-config --version ---"
  geant4-config --version
  echo "--- binary sha256 ---"
  sha256sum "$BIN_A" "$BIN_B"
  echo "--- geometry ---"
  sha256sum "$GEO_JSON"
  echo "--- fixed parameters ---"
  echo "geometry=$GEO view=$VIEW seed_diag=$SEED_DIAG seed_t4=$SEED_T4 " \
       "events_t4=$EVENTS_T4 threads_t4=$THREADS_T4 volume_stat_n=$VOLSTAT_N"
  echo "probes: ${PROBES[*]}"
  echo "slice-y: $SLICE_Y"
  echo "slice-z: $SLICE_Z"
} > "$REG" 2>&1

run_diag() {
  local variant="$1" bin="$2"
  local outdir="$OUT/t2/$variant"
  local log="$outdir/diag.log"
  local cmd=("$bin" --geometry "$GEO_JSON" --view "$VIEW" --tables "$TABLAS" \
    --seed "$SEED_DIAG" --dump-geometry --volume-stat "$VOLSTAT_N")
  for p in "${PROBES[@]}"; do
    cmd+=(--probe "$p")
  done
  cmd+=(--slice-y "$SLICE_Y" --slice-z "$SLICE_Z" --out "$outdir")
  {
    echo "=== T2 diagnostic variant=$variant — $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
    echo "command: ${cmd[*]}"
  } > "$log"
  "${cmd[@]}" >> "$log" 2>&1
  local rc=$?
  echo "exit_code=$rc" >> "$log"
  echo "t2 variant=$variant exit_code=$rc" >> "$REG"
}

run_t4() {
  local variant="$1" bin="$2"
  local outdir="$OUT/t4/$variant"
  local log="$outdir/run.log"
  local cmd=("$bin" --geometry "$GEO_JSON" --view "$VIEW" --tables "$TABLAS" \
    --seed "$SEED_T4" --out "$outdir" --events "$EVENTS_T4" --threads "$THREADS_T4")
  {
    echo "=== T4 normal run variant=$variant — $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
    echo "command: ${cmd[*]}"
  } > "$log"
  "${cmd[@]}" >> "$log" 2>&1
  local rc=$?
  echo "exit_code=$rc" >> "$log"
  echo "t4 variant=$variant exit_code=$rc" >> "$REG"
}

run_diag A "$BIN_A"
run_diag B "$BIN_B"
run_t4 A "$BIN_A"
run_t4 B "$BIN_B"

echo "=== T2/T4 sbatch done ==="

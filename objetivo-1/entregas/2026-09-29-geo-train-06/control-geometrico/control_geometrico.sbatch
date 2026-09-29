#!/bin/bash
#SBATCH --job-name=oe1-ctrl-t1
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=48G
#SBATCH --time=00:55:00
#SBATCH --output=/home/dapintoo/oe1-trabajo/salidas/control-geometrico/slurm/%x-%j.out

# Plan step 3, work unit U7, task T1: --check-geometry on all 19 catalog
# geometries x 6 views x {A, B} = 228 initialisations, resolution 100000,
# tolerance 0. Locked criterion: B must report 0 overlaps in all 114 runs;
# A must report overlaps in exactly the 6 defective geometries (all 6 views
# each) and 0 overlaps in the other 13 x 6 = 78 runs. Any other outcome is
# investigated and reported (this script does not judge pass/fail; it only
# produces the complete, non-truncated logs and the exit-code/wall-time
# TSV that oe1_geometry_check_report.py evaluates against the criterion).

ROOT="$HOME/oe1-trabajo"
CATALOGO="$ROOT/catalogo"
TABLAS="$ROOT/tablas"
OUT="$ROOT/salidas/control-geometrico"
STATUSDIR="$OUT/status-t1"
REG="$OUT/registro-t1.txt"
SEED=20260929
RES=100000
TOL=0

mkdir -p "$OUT/A" "$OUT/B" "$STATUSDIR" "$OUT/slurm"

# lmod's own scripts reference unset variables, so `set -u` is enabled only
# after modules are loaded (never before sourcing lmod).
source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2

set -u
set -o pipefail

{
  echo "=== oe1-ctrl-t1 (T1) — $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  echo "job_id=${SLURM_JOB_ID:-none} node=$(hostname)"
  echo "--- module list ---"
  module list 2>&1
  echo "--- geant4-config --version ---"
  geant4-config --version
  echo "--- binary sha256 ---"
  sha256sum "$ROOT/build-A/muography_sim" "$ROOT/build-B/muography_sim"
  echo "--- fixed parameters ---"
  echo "seed=$SEED resolution=$RES tolerance=$TOL threads=1"
  echo "--- catalog (19 geometries) ---"
  ls "$CATALOGO"/*.json | sort
} > "$REG" 2>&1

BIN_A="$ROOT/build-A/muography_sim"
BIN_B="$ROOT/build-B/muography_sim"

TASKS="$OUT/tasks-t1.tsv"
: > "$TASKS"
for geo_path in "$CATALOGO"/*.json; do
  geo=$(basename "$geo_path" .json)
  for view in 0 1 2 3 4 5; do
    printf "A\t%s\t%s\t%s\t%s\n" "$geo" "$view" "$BIN_A" "$geo_path" >> "$TASKS"
    printf "B\t%s\t%s\t%s\t%s\n" "$geo" "$view" "$BIN_B" "$geo_path" >> "$TASKS"
  done
done

N_TASKS=$(wc -l < "$TASKS")
echo "n_tasks=$N_TASKS (expected 228)" >> "$REG"

run_one() {
  local variant="$1" geo="$2" view="$3" bin="$4" geo_path="$5"
  local log="$OUT/$variant/${geo}_view${view}.log"
  local t0 t1 rc wall
  t0=$(date +%s.%N)
  "$bin" --geometry "$geo_path" --view "$view" --tables "$TABLAS" \
    --seed "$SEED" --check-geometry > "$log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.3f", b-a}')
  printf "%s\t%s\t%s\t%s\t%s\n" "$variant" "$geo" "$view" "$rc" "$wall" \
    > "$STATUSDIR/${variant}_${geo}_view${view}.status"
}
export -f run_one
export OUT TABLAS SEED STATUSDIR

# Never stop on exit code 1 (expected for variant A on the 6 defective
# geometries): xargs itself does not abort on a non-zero child exit code,
# and run_one captures rc explicitly rather than propagating it.
cat "$TASKS" | xargs -P 24 -L 1 bash -c 'run_one "$@"' _

# Assemble the final TSV from the per-task status files (avoids a shared-
# file write race across 24 concurrent workers).
RESUMEN="$OUT/resultados-t1.tsv"
{
  printf "variant\tgeometry\tview\texit_code\twall_s\n"
  for f in "$STATUSDIR"/*.status; do
    cat "$f"
  done | sort -k1,1 -k2,2 -k3,3n
} > "$RESUMEN"

N_DONE=$(ls "$STATUSDIR"/*.status 2>/dev/null | wc -l)
echo "n_status_files=$N_DONE (expected 228)" >> "$REG"
echo "resumen_tsv=$RESUMEN" >> "$REG"

# Quick sanity summary in the slurm .out (full evaluation happens locally
# in oe1_geometry_check_report.py against resumen-solapes.csv).
echo "=== quick summary (exit codes) ==="
awk -F'\t' 'NR>1{c[$1"_"$4]++} END{for (k in c) print k, c[k]}' "$RESUMEN" | sort

echo "=== T1 sbatch done ==="

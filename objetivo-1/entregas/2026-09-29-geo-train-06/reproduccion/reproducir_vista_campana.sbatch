#!/usr/bin/env bash
#SBATCH --job-name=oe1-reproduccion
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=16G
#SBATCH --time=00:55:00
# Reproduccion de una vista de la campana (P-02): binario A0 (fuentes del bundle),
# mismos parametros que el bloque historico b-09-0 (geo-train-06, vista 0,
# --days 30, semilla 20260805090000, 24 hilos). No reutiliza carpetas.
set -euo pipefail
: "${BIN:?ruta absoluta}" "${GEOMETRY:?ruta absoluta}" "${TABLES:?ruta absoluta}" "${OUTDIR:?ruta absoluta nueva}"
mkdir "$OUTDIR"
{
  date -u
  echo "binary=$BIN"; echo "geometry=$GEOMETRY"; echo "tables=$TABLES"; echo "threads=$SLURM_CPUS_PER_TASK"; echo "job=${SLURM_JOB_ID:-manual}"; echo "node=$(hostname)"
  module list 2>&1 || true
  geant4-config --version || true
} > "$OUTDIR/entorno.txt"
sha256sum "$BIN" "$GEOMETRY" "$TABLES/row_weights_30d.txt" "$TABLES/p_cdf.txt" "$TABLES/meta.json" > "$OUTDIR/entradas.sha256"
CMD=("$BIN" --geometry "$GEOMETRY" --view 0 --tables "$TABLES" --days 30 --seed 20260805090000 --threads "$SLURM_CPUS_PER_TASK" --out "$OUTDIR")
printf '%q ' "${CMD[@]}" > "$OUTDIR/comando.txt"; printf '\n' >> "$OUTDIR/comando.txt"
"${CMD[@]}" > "$OUTDIR/run.log" 2>&1
test -s "$OUTDIR/geo-train-06_view0_hist.csv"; test -s "$OUTDIR/geo-train-06_view0.meta.json"
(cd "$OUTDIR" && sha256sum geo-train-06_view0_hist.csv geo-train-06_view0.meta.json run.log comando.txt > SHA256SUMS)
echo "REPRODUCCION TERMINADA"

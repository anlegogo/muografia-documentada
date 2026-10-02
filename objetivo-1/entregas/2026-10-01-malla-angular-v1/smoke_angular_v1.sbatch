#!/usr/bin/env bash
#SBATCH --job-name=oe1-angular-v1
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
# Corrida de integracion de la malla azimutal v1 (1.000 primarios, 1 hilo).
# Ejecuta literalmente el bloque de objetivo-1/correcciones/malla-angular-v1/README.md
# desde la raiz de la rama propuesta/malla-angular-v1. No reutiliza carpetas.
set -uo pipefail
cd "$HOME/oe1-trabajo/angular-v1"
test ! -e results/angular-v1-smoke || { echo "carpeta de salida ya existe"; exit 2; }
module load gnu14/14.2.0 geant4/11.4.2
mkdir -p results/angular-v1-smoke
{
  date -u
  echo "job=${SLURM_JOB_ID:-manual}"; echo "node=$(hostname)"; echo "cwd=$(pwd)"
  module list 2>&1 || true
  geant4-config --version || true
  c++ --version | head -1
} > results/angular-v1-smoke/entorno.txt
sha256sum build-az-edges-v1/muography_sim scripts/simulation/geometry_catalog/geometries/geo-train-01.json scripts/simulation/geant4_app/tables-az-edges-v1/* > results/angular-v1-smoke/entradas.sha256
echo "build-az-edges-v1/muography_sim --geometry scripts/simulation/geometry_catalog/geometries/geo-train-01.json --view 0 --tables scripts/simulation/geant4_app/tables-az-edges-v1 --seed 2026100107 --events 1000 --threads 1 --out results/angular-v1-smoke" > results/angular-v1-smoke/comando.txt
if build-az-edges-v1/muography_sim --geometry scripts/simulation/geometry_catalog/geometries/geo-train-01.json --view 0 --tables scripts/simulation/geant4_app/tables-az-edges-v1 --seed 2026100107 --events 1000 --threads 1 --out results/angular-v1-smoke > results/angular-v1-smoke/run.log 2>&1; then
  printf "0\n" > results/angular-v1-smoke/exit_code.txt
else
  run_status=$?
  printf "%s\n" "$run_status" > results/angular-v1-smoke/exit_code.txt
fi
echo "CORRIDA TERMINADA exit=$(cat results/angular-v1-smoke/exit_code.txt)"

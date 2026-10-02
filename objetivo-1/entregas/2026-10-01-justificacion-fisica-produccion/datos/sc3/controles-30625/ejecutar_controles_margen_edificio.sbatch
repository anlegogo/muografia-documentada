#!/bin/bash
#SBATCH --job-name=oe1-controles-margen
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --time=00:20:00
#SBATCH --output=%x-%j.out
# Check C4 combined with the edifice injection of C2 (geo-train-01, view 0,
# 2e6 primaries per run, seed 777, 600 m plane). Reuses the executable built
# by job 30621 (ejecutar_controles.sbatch) after checking its SHA-256.
#
# Usage (guane):
#   mkdir ~/oe1-trabajo/controles-c1c5-margen && cd ~/oe1-trabajo/controles-c1c5-margen
#   cp RUTA/ejecutar_controles_margen_edificio.sbatch .
#   sbatch ejecutar_controles_margen_edificio.sbatch

set -uo pipefail
WORK="$SLURM_SUBMIT_DIR"
cd "$WORK" || exit 2
test ! -e resultados || { echo "resultados/ ya existe; se exige carpeta nueva"; exit 2; }
module purge
module load gnu14/14.2.0 geant4/11.4.2
BASE="$HOME/oe1-trabajo/angular-v1"
CTRL="$HOME/oe1-trabajo/controles-c1c5/build-controles/muography_sim"
ESPERADO=$(awk -v b="$CTRL" '$2 == b {print $1}' "$HOME/oe1-trabajo/controles-c1c5/resultados/entradas.sha256")
mkdir -p resultados
[[ -n "$ESPERADO" && "$(sha256sum "$CTRL" | cut -d' ' -f1)" == "$ESPERADO" ]] || { echo "binario distinto del de 30621"; exit 3; }
TAB="$BASE/scripts/simulation/geant4_app/tables-az-edges-v1"
GEOJ="$BASE/scripts/simulation/geometry_catalog/geometries/geo-train-01.json"
{
  date -u
  echo "job=$SLURM_JOB_ID node=$(hostname) cwd=$WORK"
  module list 2>&1
} > resultados/entorno.txt 2>&1
sha256sum "$CTRL" "$GEOJ" "$TAB"/* > resultados/entradas.sha256
CORTES="0.5,1,2,3,5"
CORRIDAS=(
  "m01-edificio-margen-2deg|OE1C_INJECT=edifice OE1C_MARGIN_DEG=2 OE1C_PLANE_HALF_M=300 OE1C_ECUTS_GEV=$CORTES"
  "m02-edificio-margen-5deg|OE1C_INJECT=edifice OE1C_MARGIN_DEG=5 OE1C_PLANE_HALF_M=300 OE1C_ECUTS_GEV=$CORTES"
)
fallos=0
for c in "${CORRIDAS[@]}"; do
  IFS='|' read -r nombre vars <<< "$c"
  out="resultados/$nombre"
  mkdir -p "$out"
  cmd=(env $vars "$CTRL" --geometry "$GEOJ" --view 0 --tables "$TAB" --seed 777
       --events 2000000 --threads "$SLURM_CPUS_PER_TASK" --out "$out")
  printf '%q ' "${cmd[@]}" > "$out/comando.txt"; echo >> "$out/comando.txt"
  "${cmd[@]}" > "$out/run.log" 2>&1
  st=$?
  echo "$st" > "$out/exit_code.txt"
  [[ $st -eq 0 ]] || fallos=$((fallos + 1))
  echo "$nombre exit=$st $(grep 'RUN DONE' "$out/run.log")"
done
(cd resultados && find . -name '*.csv' -o -name '*.meta.json' | sort | xargs sha256sum) > resultados/salidas.sha256
echo "fallos=$fallos"
exit "$fallos"

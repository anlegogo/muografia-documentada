#!/bin/bash
#SBATCH --job-name=oe1-controles
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --time=01:00:00
#SBATCH --output=%x-%j.out
# Short physical checks C1, C2, C4 and C5 (geo-train-01, view 0, 2e6
# primaries per run, seed 777). Builds the patched executable in a separate
# tree; never touches the production tree ~/oe1-trabajo/angular-v1.
#
# Usage (guane):
#   mkdir ~/oe1-trabajo/controles-c1c5 && cd ~/oe1-trabajo/controles-c1c5
#   cp RUTA/controles-oe1.patch RUTA/ejecutar_controles.sbatch .
#   sbatch ejecutar_controles.sbatch

set -uo pipefail
BASE="$HOME/oe1-trabajo/angular-v1"
WORK="$SLURM_SUBMIT_DIR"
cd "$WORK" || exit 2
test ! -e resultados || { echo "resultados/ ya existe; se exige carpeta nueva"; exit 2; }
module purge
module load gnu14/14.2.0 geant4/11.4.2

mkdir -p resultados
{
  date -u
  echo "job=$SLURM_JOB_ID node=$(hostname) cwd=$WORK"
  module list 2>&1
  geant4-config --version
  c++ --version | head -1
  cmake --version | head -1
} > resultados/entorno.txt 2>&1

# 1. Patched source tree (copy of the production tree + controles-oe1.patch)
mkdir -p scripts
cp -r "$BASE/scripts/simulation" scripts/simulation
rm -rf scripts/simulation/geant4_app/build*
patch -p1 --forward < controles-oe1.patch > resultados/parche.log 2>&1 || { echo "parche fallido"; exit 3; }
TIPO=$(sed -n 's/^CMAKE_BUILD_TYPE:STRING=//p' "$BASE/build-az-edges-v1/CMakeCache.txt")
cp "$BASE/build-az-edges-v1/CMakeCache.txt" resultados/CMakeCache-produccion.txt
cmake -S scripts/simulation/geant4_app -B build-controles -DCMAKE_BUILD_TYPE="$TIPO" > resultados/cmake-config.log 2>&1 \
  && cmake --build build-controles -j "$SLURM_CPUS_PER_TASK" > resultados/cmake-build.log 2>&1 \
  || { echo "compilacion fallida"; exit 4; }

PROD="$BASE/build-az-edges-v1/muography_sim"
CTRL="$WORK/build-controles/muography_sim"
TAB="$BASE/scripts/simulation/geant4_app/tables-az-edges-v1"
GEOJ="$BASE/scripts/simulation/geometry_catalog/geometries/geo-train-01.json"
sha256sum "$PROD" "$CTRL" "$GEOJ" "$TAB"/* controles-oe1.patch > resultados/entradas.sha256
CORTES="0.5,1,2,3,5"
N=2000000
SEMILLA=777

# name|binary|environment
CORRIDAS=(
  "r00-produccion|$PROD|"
  "r01-parche-por-defecto|$CTRL|"
  "r02-plano-1.2m|$CTRL|OE1C_PLANE_HALF_M=0.6 OE1C_ECUTS_GEV=$CORTES"
  "r03-plano-100m|$CTRL|OE1C_PLANE_HALF_M=50 OE1C_ECUTS_GEV=$CORTES"
  "r04-plano-300m|$CTRL|OE1C_PLANE_HALF_M=150 OE1C_ECUTS_GEV=$CORTES"
  "r05-plano-600m|$CTRL|OE1C_PLANE_HALF_M=300 OE1C_ECUTS_GEV=$CORTES"
  "r06-plano-1200m|$CTRL|OE1C_PLANE_HALF_M=600 OE1C_ECUTS_GEV=$CORTES"
  "r07-edificio-100m|$CTRL|OE1C_INJECT=edifice OE1C_PLANE_HALF_M=50 OE1C_ECUTS_GEV=$CORTES"
  "r08-edificio-600m|$CTRL|OE1C_INJECT=edifice OE1C_PLANE_HALF_M=300 OE1C_ECUTS_GEV=$CORTES"
  "r09-margen-2deg|$CTRL|OE1C_MARGIN_DEG=2 OE1C_PLANE_HALF_M=300 OE1C_ECUTS_GEV=$CORTES"
  "r10-margen-5deg|$CTRL|OE1C_MARGIN_DEG=5 OE1C_PLANE_HALF_M=300 OE1C_ECUTS_GEV=$CORTES"
)
fallos=0
for c in "${CORRIDAS[@]}"; do
  IFS='|' read -r nombre bin vars <<< "$c"
  out="resultados/$nombre"
  mkdir -p "$out"
  cmd=(env $vars "$bin" --geometry "$GEOJ" --view 0 --tables "$TAB" --seed "$SEMILLA"
       --events "$N" --threads "$SLURM_CPUS_PER_TASK" --out "$out")
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

#!/bin/bash
#SBATCH --job-name=oe1-controles-anidados
#SBATCH --partition=legacy
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --time=01:15:00
#SBATCH --output=%x-%j.out
# Nested-square checks C1, C2 and C5 (geo-train-01, view 0, 2e7 primaries
# per run, seed 777): one 1200 m plane records the 1.2/100/300/600 m squares
# with the same muons, so plane ratios are nested binomial fractions. Builds the patched executable in a separate
# tree; never touches the production tree ~/oe1-trabajo/angular-v1.
#
# Usage (guane):
#   mkdir ~/oe1-trabajo/controles-c1c5-v2 && cd ~/oe1-trabajo/controles-c1c5-v2
#   cp RUTA/controles-oe1-v2.patch RUTA/ejecutar_controles_anidados.sbatch .
#   sbatch ejecutar_controles_anidados.sbatch

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

# 1. Patched source tree (copy of the production tree + controles-oe1-v2.patch)
mkdir -p scripts
cp -r "$BASE/scripts/simulation" scripts/simulation
rm -rf scripts/simulation/geant4_app/build*
patch -p1 --forward < controles-oe1-v2.patch > resultados/parche.log 2>&1 || { echo "parche fallido"; exit 3; }
TIPO=$(sed -n 's/^CMAKE_BUILD_TYPE:STRING=//p' "$BASE/build-az-edges-v1/CMakeCache.txt")
cp "$BASE/build-az-edges-v1/CMakeCache.txt" resultados/CMakeCache-produccion.txt
cmake -S scripts/simulation/geant4_app -B build-controles -DCMAKE_BUILD_TYPE="$TIPO" > resultados/cmake-config.log 2>&1 \
  && cmake --build build-controles -j "$SLURM_CPUS_PER_TASK" > resultados/cmake-build.log 2>&1 \
  || { echo "compilacion fallida"; exit 4; }

PROD="$BASE/build-az-edges-v1/muography_sim"
CTRL="$WORK/build-controles/muography_sim"
TAB="$BASE/scripts/simulation/geant4_app/tables-az-edges-v1"
GEOJ="$BASE/scripts/simulation/geometry_catalog/geometries/geo-train-01.json"
sha256sum "$PROD" "$CTRL" "$GEOJ" "$TAB"/* controles-oe1-v2.patch > resultados/entradas.sha256
CORTES="0.5,1,2,3,5"
SUB="0.6,50,150,300"
SEMILLA=777

# name|binary|environment
# name|binary|events|environment
CORRIDAS=(
  "a00-parche-v2-por-defecto|$CTRL|2000000|"
  "a01-anidado-actual|$CTRL|20000000|OE1C_PLANE_HALF_M=600 OE1C_SUBPLANES_M=$SUB OE1C_ECUTS_GEV=$CORTES"
  "a02-anidado-edificio|$CTRL|20000000|OE1C_INJECT=edifice OE1C_PLANE_HALF_M=600 OE1C_SUBPLANES_M=$SUB OE1C_ECUTS_GEV=$CORTES"
)
fallos=0
for c in "${CORRIDAS[@]}"; do
  IFS='|' read -r nombre bin N vars <<< "$c"
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

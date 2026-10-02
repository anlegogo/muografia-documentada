#!/bin/bash
# Builds the production tree for the validated recipe: copy of the angular-v1
# tree (commit 0dea8e1) + controles-oe1-v3.patch, compiled with the same
# CMAKE_BUILD_TYPE as build-az-edges-v1. Run on a compute node:
#   srun -p legacy -N1 -n1 -c24 -t 00:30:00 bash preparar_arbol_receta.sh
set -euo pipefail
BASE="$HOME/oe1-trabajo/angular-v1"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
PARCHE="$(cd "$(dirname "$0")" && pwd)/controles-oe1-v3.patch"
test ! -e "$ARBOL" || { echo "$ARBOL ya existe"; exit 2; }
module purge
module load gnu14/14.2.0 geant4/11.4.2
mkdir -p "$ARBOL/scripts"
cp -r "$BASE/scripts/simulation" "$ARBOL/scripts/simulation"
rm -rf "$ARBOL"/scripts/simulation/geant4_app/build*
cp "$PARCHE" "$ARBOL/controles-oe1-v3.patch"
cd "$ARBOL"
patch -p1 --forward < controles-oe1-v3.patch
TIPO=$(sed -n 's/^CMAKE_BUILD_TYPE:STRING=//p' "$BASE/build-az-edges-v1/CMakeCache.txt")
cmake -S scripts/simulation/geant4_app -B build-receta -DCMAKE_BUILD_TYPE="$TIPO" > cmake-config.log 2>&1
cmake --build build-receta -j "${SLURM_CPUS_PER_TASK:-8}" > cmake-build.log 2>&1
sha256sum build-receta/muography_sim controles-oe1-v3.patch | tee receta.sha256

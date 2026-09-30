#!/usr/bin/env bash
# OE1 stage 1, gate K0 (rest), README.md step 6, inside ONE srun allocation on SC3. No transport.
# Second attempt (verificacion/k0-NN): the tests run in the REPOSITORY layout, extracted with `git archive` from
# the exact commits, as in development. The first attempt (verificacion/k0, job 30564) compiled against the pilot
# bundle layout of fuentes/A2, where third_party/ sits at the bundle root, so json.hpp was not found, and the Python
# fixtures could not find ../simulation/geant4_app/tables. Nothing in the code under test changed.
#   repo-A2    = git archive fdaef4b (A2)    scripts/simulation/{geant4_app,third_party,geometry_catalog}
#   repo-tools = git archive 3315f82 (TOOLS) scripts/analysis + scripts/simulation/{geant4_app,third_party,geometry_catalog}
#   orig2      = git archive 9520170 (A)     scripts/simulation/{geant4_app,third_party}
# The P2 files of repo-A2 are checked against registro/P2-instrumentacion.sha256, the list prepare_sources.sh used
# for fuentes/A2, so the code tested here is the code that was built. The early-exit test runs on the REAL binaries.
# usage: K0_NN=02 srun -p legacy -N1 -c8 --mem=8G -t 01:00:00 bash k0_etapa1_v2.sh
set -u -o pipefail
source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2
export PYTHONDONTWRITEBYTECODE=1
E1="$HOME/oe1-trabajo/etapa1"
U="$HOME/oe1-trabajo/subida-etapa1"
APP="$U/repo-A2/scripts/simulation/geant4_app"
ORIG="$U/orig2/scripts/simulation/geant4_app"
K0="$E1/verificacion/k0-${K0_NN:?set K0_NN}"
SCR="${TMPDIR:-/tmp}/oe1-k0-${SLURM_JOB_ID:-nojob}"
[[ -n "${SLURM_JOB_ID:-}" ]] || { echo "run inside srun" >&2; exit 2; }
mkdir "$K0" || { echo "$K0 exists" >&2; exit 3; }
mkdir -p "$SCR" || exit 2
cp -p "$0" "$K0/k0_etapa1_v2.sh"
{
  echo "SLURM_JOB_ID=$SLURM_JOB_ID host=$(hostname) inicio=$(date -u '+%Y-%m-%d %H:%M:%S') UTC scratch=$SCR"
  g++ --version | head -n 1
  echo "geant4 $(geant4-config --version)"
  python3 --version
  python3 -c 'import numpy; print("numpy", numpy.__version__)'
} > "$K0/entorno.txt" 2>&1
rc=0
{
  echo "A2=fdaef4b8aad259f17043ef0fc6fdccc295e3b8e2 TOOLS=3315f82ffa1a3be604897e34e2319b379f500655 A=95201700ce090aea5bdce9b0d3816a55f389b4fc"
  ( cd "$U" && sha256sum repo-A2.tar repo-tools.tar orig2-9520170.tar )
  echo "--- P2 files of repo-A2 against registro/P2-instrumentacion.sha256"
  ( cd "$U/repo-A2/scripts" && sha256sum -c "$E1/registro/P2-instrumentacion.sha256" ) || echo "P2 CHECK FAILED"
  echo "--- frozen catalog against the repository catalog"
  for g in geo-train-06 geo-train-01; do
    sha256sum "$HOME/oe1-trabajo/catalogo/$g.json" "$U/repo-A2/scripts/simulation/geometry_catalog/geometries/$g.json"
  done
} > "$K0/procedencia.txt" 2>&1
grep -q 'P2 CHECK FAILED' "$K0/procedencia.txt" && { echo "procedencia rc=1" | tee -a "$K0/resumen.txt"; rc=1; }
keep() {  # copy the small text outputs of a scratch folder
  mkdir "$K0/$2"
  rsync -a --max-size=2m --include='*/' --include='*.json' --include='*.out' --include='*.log' --include='*.txt' \
        --include='*.tsv' --include='*.csv' --exclude='*' "$1/" "$K0/$2/"
}
step() {  # step NAME CMD...: log in NAME.log, rc in resumen.txt
  local name="$1"; shift
  echo "=== $name $(date -u '+%H:%M:%S')"
  "$@" > "$K0/$name.log" 2>&1
  local r=$?
  echo "$name rc=$r" | tee -a "$K0/resumen.txt"
  [[ $r -eq 0 ]] || rc=1
}
step cruces env CATALOG="$HOME/oe1-trabajo/catalogo" bash "$APP/tests/build_tests.sh" "$SCR/cruces"
keep "$SCR/cruces" cruces
step banco-sintetico bash "$APP/tests/g4/build_g4_tests.sh" "$SCR/g4"
keep "$SCR/g4" banco-sintetico
step salida-anticipada bash "$APP/tests/g4/early_exit.sh" "$E1/build/A2/muography_sim" "$E1/build/B2/muography_sim" \
     "$HOME/oe1-trabajo/catalogo/geo-train-06.json" "$HOME/oe1-trabajo/tablas" "$SCR/early"
keep "$SCR/early" salida-anticipada
step inercia-legado bash "$APP/tests/g4/legacy_inertness.sh" "$ORIG" "$SCR/legacy"
keep "$SCR/legacy" inercia-legado
step pruebas-python bash -c "cd '$U/repo-tools/scripts/analysis' && python3 -B -m unittest discover -s tests -t ."
step auditoria-aleatorios-A2 bash "$E1/herramientas/audit_rng.sh" --diff "$E1/registro/P2-instrumentacion.diff" \
     --build-dir "$E1/build/A2"
step auditoria-aleatorios-B2 bash "$E1/herramientas/audit_rng.sh" --diff "$E1/registro/P2-instrumentacion.diff" \
     --build-dir "$E1/build/B2"
rm -rf "$SCR"
echo "fin=$(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> "$K0/entorno.txt"
echo "TOTAL rc=$rc" | tee -a "$K0/resumen.txt"
( cd "$K0" && find . -type f ! -name SHA256SUMS -print0 | LC_ALL=C sort -z | xargs -0 sha256sum > SHA256SUMS )
exit $rc

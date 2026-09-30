#!/usr/bin/env bash
# OE1 stage 1, gate K0 (rest), README.md step 6, inside ONE srun allocation on SC3. No transport:
#   1. standalone crossing-detector tests (release and ASan/UBSan, R1 over six seeds): pruebas-cruces.json
#   2. Geant4-linked synthetic list-mode harness (13 scenarios, no run manager, no BeamOn)
#   3. early exits on the REAL binaries (exit 4 before BeamOn, empty --out)
#   4. legacy-inertness probe (pre-P2 tree of commit 9520170 against P2)
#   5. Python unit tests of the analysis tools
#   6. static RNG audit of the lines P2 adds, with nm over each build
# Heavy intermediates (the R1 segment files, test binaries) stay in node-local scratch; the logs, summaries and
# JSON files are copied to ~/oe1-trabajo/etapa1/verificacion/k0 with a SHA256SUMS list.
# usage: srun -p legacy -N1 -c8 --mem=8G -t 01:00:00 bash k0_etapa1.sh
set -u -o pipefail
source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2
export PYTHONDONTWRITEBYTECODE=1
E1="$HOME/oe1-trabajo/etapa1"
U="$HOME/oe1-trabajo/subida-etapa1"
APP="$E1/fuentes/A2/simulation/geant4_app"
K0="$E1/verificacion/k0"
SCR="${TMPDIR:-/tmp}/oe1-k0-${SLURM_JOB_ID:-nojob}"
[[ -n "${SLURM_JOB_ID:-}" ]] || { echo "run inside srun" >&2; exit 2; }
mkdir "$K0" || { echo "$K0 exists" >&2; exit 3; }
mkdir -p "$SCR" || exit 2
cp -p "$0" "$K0/k0_etapa1.sh"
{
  echo "SLURM_JOB_ID=$SLURM_JOB_ID host=$(hostname) inicio=$(date -u '+%Y-%m-%d %H:%M:%S') UTC scratch=$SCR"
  g++ --version | head -n 1
  echo "geant4 $(geant4-config --version)"
  python3 --version
  python3 -c 'import numpy; print("numpy", numpy.__version__)'
} > "$K0/entorno.txt" 2>&1
rc=0
keep() {  # copy the small text outputs of a scratch folder
  mkdir "$K0/$2"
  rsync -a --max-size=2m --include='*/' --include='*.json' --include='*.out' --include='*.log' --include='*.txt' \
        --include='*.tsv' --include='*.csv' --exclude='*' "$1/" "$K0/$2/"
}
step() {  # step NAME CMD...: log in k0/NAME.log, rc in resumen.txt
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
step inercia-legado bash "$APP/tests/g4/legacy_inertness.sh" "$U/orig/scripts/simulation/geant4_app" "$SCR/legacy"
keep "$SCR/legacy" inercia-legado
step pruebas-python bash -c "cd '$U/subida/analysis' && python3 -B -m unittest discover -s tests -t ."
step auditoria-aleatorios-A2 bash "$E1/herramientas/audit_rng.sh" --diff "$E1/registro/P2-instrumentacion.diff" \
     --build-dir "$E1/build/A2"
step auditoria-aleatorios-B2 bash "$E1/herramientas/audit_rng.sh" --diff "$E1/registro/P2-instrumentacion.diff" \
     --build-dir "$E1/build/B2"
rm -rf "$SCR"
echo "fin=$(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> "$K0/entorno.txt"
echo "TOTAL rc=$rc" | tee -a "$K0/resumen.txt"
( cd "$K0" && find . -type f ! -name SHA256SUMS -print0 | LC_ALL=C sort -z | xargs -0 sha256sum > SHA256SUMS )
exit $rc

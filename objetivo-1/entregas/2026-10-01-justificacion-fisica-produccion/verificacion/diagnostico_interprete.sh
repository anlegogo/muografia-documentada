#!/bin/bash
# Diagnosis of the interpreter that the planned sbatch command would use. The
# launcher resolves --python with Path.resolve(); the team's venv exposes python
# as a symlink, so the planned command carries the base interpreter path instead
# of the venv path. This script records what each interpreter provides. It does
# not modify any tool, transports no muon and submits nothing. Run on guane:
#   bash -l diagnostico_interprete.sh
set -uo pipefail
BASE="$HOME/oe1-trabajo/integracion-c9442d6"
REPO="$BASE/replica"
OUT="$BASE/salidas-diagnostico"
PY="$HOME/muography-train/venv/bin/python"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
TEMPORAL="$HOME/muography-scratch/oe1-piloto-v2-intentos"
SALIDA="$HOME/muography-scratch/oe1-piloto-v2-publicados"
DISENO="$REPO/objetivo-1/evidencias/piloto-propuesto-siete-actividades"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
MAN="$DISENO/manifiesto-piloto-propuesto.csv"
cd "$REPO" || exit 2
test ! -e "$OUT" || { echo "salidas-diagnostico/ ya existe"; exit 2; }
mkdir -p "$OUT"
INICIO="$(date '+%Y-%m-%dT%H:%M:%S')"
type module >/dev/null 2>&1 || source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2
RESUELTO="$("$PY" -c "import sys; from pathlib import Path; print(Path(sys.argv[1]).resolve())" "$PY")"

run() {  # name, command...
  local n="$1"; shift
  printf '%q ' "$@" > "$OUT/$n.comando.txt"; echo >> "$OUT/$n.comando.txt"
  "$@" > "$OUT/$n.stdout.txt" 2> "$OUT/$n.stderr.txt"
  echo $? > "$OUT/$n.exit_code.txt"
  echo "$n exit=$(cat "$OUT/$n.exit_code.txt")"
}
VERSIONES='import sys
print("executable", sys.executable)
print("prefix", sys.prefix)
print("base_prefix", sys.base_prefix)
print("python", sys.version.split()[0])
for name in ("numpy", "scipy", "matplotlib"):
    try:
        module = __import__(name)
        print(name, module.__version__, module.__file__)
    except Exception as exc:
        print(name, "NO DISPONIBLE:", type(exc).__name__, exc)'

{ date '+%Y-%m-%dT%H:%M:%S%z'; echo "node=$(hostname)"; ls -l "$PY"; echo "resolved=$RESUELTO"; cat "$(dirname "$(dirname "$PY")")/pyvenv.cfg"; } > "$OUT/interprete.txt" 2>&1
run versiones-venv "$PY" -c "$VERSIONES"
run versiones-resuelto "$RESUELTO" -c "$VERSIONES"
# Same interpreters on a compute node, as a batch job would see them.
run versiones-resuelto-nodo srun -p legacy -N1 -n1 -c2 -t 00:05:00 "$RESUELTO" -c "$VERSIONES"
# Worker in describe mode and unit tests with the interpreter of the planned command.
run worker-fila0-resuelto "$RESUELTO" herramientas/operar_bloque_angular.py --manifiesto "$MAN" --fila 0 --arbol "$ARBOL" --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" --threads 24
run pruebas-resuelto srun -p legacy -N1 -n1 -c2 -t 00:10:00 "$RESUELTO" -m unittest discover -s herramientas -p 'test_*angular*.py' -v

sleep 5
sacct -u "$(id -un)" -S "$INICIO" -X -P -o JobID,JobName,Partition,AllocCPUS,State,ExitCode,Elapsed,Start,End,NodeList,SubmitLine > "$OUT/sacct.txt" 2>&1
squeue -h -u "$(id -un)" -o '%i|%j|%T|%P' > "$OUT/squeue-despues.txt" 2>&1
(cd "$OUT" && find . -type f ! -name salidas.sha256 | sort | xargs sha256sum) > "$OUT/salidas.sha256"

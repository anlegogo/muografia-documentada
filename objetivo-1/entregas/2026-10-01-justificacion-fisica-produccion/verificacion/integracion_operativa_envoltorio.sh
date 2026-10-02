#!/bin/bash
# Second pass of the operational integration check, after the interpreter
# finding: the same director's tools (c9442d6, unmodified) receive --python as a
# regular wrapper file that runs the team's venv. The body of
# bloque_verificado_angular.sbatch is then reproduced on a compute node without
# --ejecutar, so the worker stays in describe mode. No muon is transported and
# nothing is submitted to the queue. Run on guane (login node):
#   bash -l integracion_operativa_envoltorio.sh
set -uo pipefail
BASE="$HOME/oe1-trabajo/integracion-c9442d6"
REPO="$BASE/replica"
OUT="$BASE/salidas-correccion"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
TEMPORAL="$HOME/muography-scratch/oe1-piloto-v2-intentos"
SALIDA="$HOME/muography-scratch/oe1-piloto-v2-publicados"
DISENO="$REPO/objetivo-1/evidencias/piloto-propuesto-siete-actividades"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
MAN="$DISENO/manifiesto-piloto-propuesto.csv"
USUARIO="$(id -un)"
cd "$REPO" || exit 2
test -x "$PY" || { echo "falta el envoltorio $PY"; exit 2; }
test ! -e "$OUT" || { echo "salidas-correccion/ ya existe"; exit 2; }
mkdir -p "$OUT"
INICIO="$(date '+%Y-%m-%dT%H:%M:%S')"
touch "$OUT/inicio.marca"
type module >/dev/null 2>&1 || source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2
{
  date '+%Y-%m-%dT%H:%M:%S%z'
  echo "node=$(hostname) user=$USUARIO cwd=$PWD"
  module list 2>&1
  ls -l "$PY"
  sha256sum "$PY"
  cat "$PY"
  "$PY" -c "import sys; from pathlib import Path; print('resolved', Path(sys.argv[1]).resolve())" "$PY"
  "$PY" -c "import sys, numpy, scipy, matplotlib; print('executable', sys.executable); print('prefix', sys.prefix); print('python', sys.version.split()[0]); print('numpy', numpy.__version__); print('scipy', scipy.__version__); print('matplotlib', matplotlib.__version__)"
} > "$OUT/entorno.txt" 2>&1
(cd herramientas && sha256sum -c "$BASE/herramientas.git.sha256") > "$OUT/herramientas-vs-git.txt" 2>&1
echo $? > "$OUT/herramientas-vs-git.exit_code.txt"
squeue -h -u "$USUARIO" -o '%i|%j|%T|%P' > "$OUT/squeue-antes.txt" 2>&1

run() {  # name, command...
  local n="$1"; shift
  printf '%q ' "$@" > "$OUT/$n.comando.txt"; echo >> "$OUT/$n.comando.txt"
  "$@" > "$OUT/$n.stdout.txt" 2> "$OUT/$n.stderr.txt"
  echo $? > "$OUT/$n.exit_code.txt"
  echo "$n exit=$(cat "$OUT/$n.exit_code.txt")"
}

run pruebas srun -p legacy -N1 -n1 -c2 -t 00:10:00 "$PY" -m unittest discover -s herramientas -p 'test_*angular*.py' -v
run preflight "$PY" herramientas/preparar_campana_angular.py "$MAN" --geometrias geo-train-06 --informe "$OUT/preflight-piloto-v2.json"
run lanzador "$PY" herramientas/lanzar_campana_angular.py --manifiesto "$MAN" --arbol "$ARBOL" --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" --python "$PY" --threads 24 --max-trabajos 4
{ ls -laR "$SALIDA.operacion" 2>&1; echo "--"; ls -ld "$SALIDA" "$TEMPORAL" 2>&1; } > "$OUT/estado-operacion.txt"

# SLURM validation of the first planned sbatch command (no job is queued).
run sbatch-test-only "$PY" - "$OUT/lanzador.stdout.txt" <<'PYEOF'
import json, subprocess, sys
plan = json.load(open(sys.argv[1], encoding='utf-8'))
cmd = plan['planned'][0]['command']
cmd = cmd[:1] + ['--test-only'] + cmd[1:]
r = subprocess.run(cmd, capture_output=True, text=True)
print(json.dumps({'command': cmd, 'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}, indent=2))
sys.exit(r.returncode)
PYEOF

# Body of bloque_verificado_angular.sbatch with the eleven planned arguments, on
# a compute node and from the planned --chdir, without `exec` and without
# --ejecutar: modules, wrapper, worker, hashes of manifest and recipe.
run bloque-sin-ejecutar "$PY" - "$OUT/lanzador.stdout.txt" <<'PYEOF'
import json, subprocess, sys
plan = json.load(open(sys.argv[1], encoding='utf-8'))
cmd = plan['planned'][0]['command']
index = next(i for i, x in enumerate(cmd) if x.endswith('bloque_verificado_angular.sbatch'))
args = cmd[index + 1:]
if len(args) != 11:
    sys.exit('se esperaban once argumentos')
chdir = next(x for x in cmd if x.startswith('--chdir='))
body = ('set -euo pipefail; module purge; module load gnu14/14.2.0 geant4/11.4.2; '
        'echo "node=$(hostname) job=$SLURM_JOB_ID cwd=$PWD" >&2; module list 2>&1 | cat >&2; '
        '"$7" "$9" --manifiesto "$1" --fila "$2" --arbol "$3" --temporal "$4" --salida "$5" '
        '--receta "$6" --threads "$8" --sha-manifiesto "${10}" --sha-receta "${11}"')
srun = ['srun', '-p', 'legacy', '-N1', '-n1', '-c2', '-t', '00:05:00', chdir, 'bash', '-lc', body, 'bloque'] + args
r = subprocess.run(srun, capture_output=True, text=True)
print(json.dumps({'command': srun, 'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}, indent=2))
sys.exit(r.returncode)
PYEOF

sleep 5
squeue -h -u "$USUARIO" -o '%i|%j|%T|%P' > "$OUT/squeue-despues.txt" 2>&1
sacct -u "$USUARIO" -S "$INICIO" -X -P -o JobID,JobName,Partition,AllocCPUS,State,ExitCode,Elapsed,Start,End,NodeList > "$OUT/sacct.txt" 2>&1
find "$HOME/muography-scratch" -newer "$OUT/inicio.marca" 2>/dev/null | sort > "$OUT/scratch-nuevos.txt"
(cd "$OUT" && find . -type f ! -name salidas.sha256 | sort | xargs sha256sum) > "$OUT/salidas.sha256"

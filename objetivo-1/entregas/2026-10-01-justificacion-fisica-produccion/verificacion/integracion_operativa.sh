#!/bin/bash
# Operational integration check of the director's campaign tools (main 3178d83,
# merged into the delivery branch at c9442d6), used unmodified. No muon is
# transported and nothing is submitted to the queue. Run on guane (login node):
#   bash -l integracion_operativa.sh
# Only the unit tests use an allocation (srun), as in GUIA_SIGUIENTE_ETAPA_OE1.md.
set -uo pipefail
BASE="$HOME/oe1-trabajo/integracion-c9442d6"
REPO="$BASE/replica"
OUT="$BASE/salidas"
PY="$HOME/muography-train/venv/bin/python"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
TEMPORAL="$HOME/muography-scratch/oe1-piloto-v2-intentos"
SALIDA="$HOME/muography-scratch/oe1-piloto-v2-publicados"
DISENO="$REPO/objetivo-1/evidencias/piloto-propuesto-siete-actividades"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
MAN="$DISENO/manifiesto-piloto-propuesto.csv"
TABLAS="$ARBOL/scripts/simulation/geant4_app/tables-az-edges-v1"
USUARIO="$(id -un)"
cd "$REPO" || exit 2
test ! -e "$OUT" || { echo "salidas/ ya existe"; exit 2; }
mkdir -p "$OUT"
INICIO="$(date '+%Y-%m-%dT%H:%M:%S')"
touch "$OUT/inicio.marca"

# Environment requested for the team's SC3 workflow.
type module >/dev/null 2>&1 || source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2
{
  date -u
  date '+%Y-%m-%dT%H:%M:%S%z'
  echo "node=$(hostname) user=$USUARIO cwd=$PWD"
  uname -srm
  module list 2>&1
  gcc --version | head -1
  cmake --version | head -1
  echo "geant4 $(geant4-config --version)"
  echo "python_executable=$(readlink -f "$PY")"
  "$PY" --version
  "$PY" -c "import numpy, scipy, matplotlib; print('numpy', numpy.__version__); print('scipy', scipy.__version__); print('matplotlib', matplotlib.__version__)"
  sbatch --version
  env | grep -E '^(OE1C_|PYTHONPATH=)' | sort
} > "$OUT/entorno.txt" 2>&1

# Tool bytes against the Git blobs of c9442d6 (list produced locally with git cat-file).
(cd herramientas && sha256sum -c "$BASE/herramientas.git.sha256") > "$OUT/herramientas-vs-git.txt" 2>&1
echo $? > "$OUT/herramientas-vs-git.exit_code.txt"
(cd herramientas && sha256sum -- *.py *.sbatch *.sh) > "$OUT/herramientas.sha256"
sha256sum "$MAN" "$RECETA" "$DISENO/diseno-piloto.json" > "$OUT/contratos.sha256"
cp "$TABLAS/meta.json" "$OUT/tablas-meta.json"
squeue -h -u "$USUARIO" -o '%i|%j|%T|%P' > "$OUT/squeue-antes.txt" 2>&1

run() {  # name, command...
  local n="$1"; shift
  printf '%q ' "$@" > "$OUT/$n.comando.txt"; echo >> "$OUT/$n.comando.txt"
  "$@" > "$OUT/$n.stdout.txt" 2> "$OUT/$n.stderr.txt"
  echo $? > "$OUT/$n.exit_code.txt"
  echo "$n exit=$(cat "$OUT/$n.exit_code.txt")"
}

# Recipe inputs and runtime tools against the hashes registered in the recipe.
run ficha-vs-arbol "$PY" - "$RECETA" "$ARBOL" "$REPO/herramientas" <<'PYEOF'
import hashlib, json, sys
from pathlib import Path
recipe, tree, tools = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
d = json.loads(recipe.read_text(encoding='utf-8'))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
tables = tree / 'scripts/simulation/geant4_app/tables-az-edges-v1'
geos = tree / 'scripts/simulation/geometry_catalog/geometries'
checks = [(tree / 'build-receta/muography_sim', d['reported_binary_sha256']),
          (tree / 'controles-oe1-v3.patch', d['patch_sha256'])]
checks += [(tables / n, h) for n, h in d['table_sha256'].items()]
checks += [(geos / n, h) for n, h in d['geometry_sha256'].items()]
checks += [(tools / n, h) for n, h in d['runtime_tool_sha256'].items()]
rows = [{'path': str(p), 'expected': h, 'found': sha(p) if p.exists() else None} for p, h in checks]
bad = [r for r in rows if r['found'] != r['expected']]
print(json.dumps({'checked': len(rows), 'mismatches': bad, 'entries': rows}, indent=2))
sys.exit(1 if bad else 0)
PYEOF

# Steps of the guide, in its order and with its commands.
run pruebas srun -p legacy -N1 -n1 -c2 -t 00:10:00 "$PY" -m unittest discover -s herramientas -p 'test_*angular*.py' -v
run preflight "$PY" herramientas/preparar_campana_angular.py "$MAN" --geometrias geo-train-06 --informe "$OUT/preflight-piloto-v2.json"
# Worker in its default describe mode (no --ejecutar): prints the simulator command of row 0.
run worker-fila0 "$PY" herramientas/operar_bloque_angular.py --manifiesto "$MAN" --fila 0 --arbol "$ARBOL" --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" --threads 24
# Launch plan without --enviar: queries squeue and describes sbatch; does not submit.
run lanzador "$PY" herramientas/lanzar_campana_angular.py --manifiesto "$MAN" --arbol "$ARBOL" --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" --python "$PY" --threads 24 --max-trabajos 4
{ ls -laR "$SALIDA.operacion" 2>&1; echo "--"; ls -ld "$SALIDA" "$TEMPORAL" 2>&1; } > "$OUT/estado-operacion.txt"

# Team complement: SLURM validation of the first planned sbatch command with
# --test-only (partition, CPUs and time limit are checked; no job is queued).
run sbatch-test-only "$PY" - "$OUT/lanzador.stdout.txt" <<'PYEOF'
import json, subprocess, sys
plan = json.load(open(sys.argv[1], encoding='utf-8'))
cmd = plan['planned'][0]['command']
cmd = cmd[:1] + ['--test-only'] + cmd[1:]
r = subprocess.run(cmd, capture_output=True, text=True)
print(json.dumps({'command': cmd, 'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}, indent=2))
sys.exit(r.returncode)
PYEOF

sleep 5
squeue -h -u "$USUARIO" -o '%i|%j|%T|%P' > "$OUT/squeue-despues.txt" 2>&1
sacct -u "$USUARIO" -S "$INICIO" -X -P -o JobID,JobName,Partition,AllocCPUS,State,ExitCode,Elapsed,Start,End,NodeList,SubmitLine > "$OUT/sacct.txt" 2>&1
find "$HOME/muography-scratch" -newer "$OUT/inicio.marca" 2>/dev/null | sort > "$OUT/scratch-nuevos.txt"
(cd "$OUT" && find . -type f ! -name salidas.sha256 | sort | xargs sha256sum) > "$OUT/salidas.sha256"

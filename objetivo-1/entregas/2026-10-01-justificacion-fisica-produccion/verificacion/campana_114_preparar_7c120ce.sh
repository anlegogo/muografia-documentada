#!/bin/bash
# Pre-submission checks of the 114-view campaign (PREPARACION_CAMPANA_114.md,
# section 7, step 3) on the replica of commit 7c120ce (launcher with --memoria), with the amd partition.
# Nothing is transported and nothing is queued. Run on guane:
#   bash -l campana_114_preparar.sh
set -uo pipefail
BASE="$HOME/oe1-trabajo/campana-114-7c120ce"
REPO="$BASE/replica"
OUT="$BASE/preparacion"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
PLAN="$REPO/objetivo-1/evidencias/preparacion-campana-114"
MAN="$PLAN/manifiesto-114-344M.csv"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
TEMPORAL="$HOME/muography-scratch/oe1-114-344M-intentos"
SALIDA="$HOME/muography-scratch/oe1-114-344M-publicados"
OPCIONES=(--threads 64 --max-trabajos 4 --particion amd --tiempo 00:15:00 --memoria 8G)
cd "$REPO" || exit 2
test ! -e "$OUT" || { echo "preparacion/ ya existe"; exit 2; }
for d in "$TEMPORAL" "$SALIDA"; do test ! -e "$d" || { echo "$d ya existe"; exit 2; }; done
mkdir -p "$OUT"
type module >/dev/null 2>&1 || source /etc/profile.d/lmod.sh
module purge
module load gnu14/14.2.0 geant4/11.4.2
{
  date '+%Y-%m-%dT%H:%M:%S%z'; echo "node=$(hostname) user=$(id -un)"; module list 2>&1
  "$PY" -c "import sys, numpy, scipy; print('python', sys.version.split()[0]); print('numpy', numpy.__version__); print('scipy', scipy.__version__)"
  sbatch --version
} > "$OUT/entorno.txt" 2>&1
(cd herramientas && sha256sum -c "$BASE/herramientas.git.sha256") > "$OUT/herramientas-vs-git.txt" 2>&1
echo $? > "$OUT/herramientas-vs-git.exit_code.txt"
sha256sum "$MAN" "$RECETA" "$PLAN/plan.json" > "$OUT/contratos.sha256"

run() {  # name, command...
  local n="$1"; shift
  printf '%q ' "$@" > "$OUT/$n.comando.txt"; echo >> "$OUT/$n.comando.txt"
  "$@" > "$OUT/$n.stdout.txt" 2> "$OUT/$n.stderr.txt"
  echo $? > "$OUT/$n.exit_code.txt"
  echo "$n exit=$(cat "$OUT/$n.exit_code.txt")"
}

run ficha-vs-arbol "$PY" - "$RECETA" "$ARBOL" "$REPO/herramientas" <<'PYEOF'
import hashlib, json, sys
from pathlib import Path
recipe, tree, tools = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
d = json.loads(recipe.read_text(encoding='utf-8'))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
tables = tree / 'scripts/simulation/geant4_app/tables-az-edges-v1'
geos = tree / 'scripts/simulation/geometry_catalog/geometries'
checks = [(tree / 'build-receta/muography_sim', d['reported_binary_sha256']), (tree / 'controles-oe1-v3.patch', d['patch_sha256'])]
checks += [(tables / n, h) for n, h in d['table_sha256'].items()]
checks += [(geos / n, h) for n, h in d['geometry_sha256'].items()]
checks += [(tools / n, h) for n, h in d['runtime_tool_sha256'].items()]
rows = [{'path': str(p), 'expected': h, 'found': sha(p) if p.exists() else None} for p, h in checks]
bad = [r for r in rows if r['found'] != r['expected']]
print(json.dumps({'checked': len(rows), 'mismatches': bad}, indent=2))
sys.exit(1 if bad else 0)
PYEOF
run preflight "$PY" herramientas/preparar_campana_angular.py "$MAN" --informe "$OUT/preflight-114-344M.json"
run lanzador "$PY" herramientas/lanzar_campana_angular.py --manifiesto "$MAN" --arbol "$ARBOL" \
  --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" --python "$PY" "${OPCIONES[@]}"
run sbatch-test-only "$PY" - "$OUT/lanzador.stdout.txt" <<'PYEOF'
import json, subprocess, sys
plan = json.load(open(sys.argv[1], encoding='utf-8'))
cmd = plan['planned'][0]['command']
cmd = cmd[:1] + ['--test-only'] + cmd[1:]
r = subprocess.run(cmd, capture_output=True, text=True)
print(json.dumps({'command': cmd, 'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}, indent=2))
sys.exit(r.returncode)
PYEOF
for n in legacy:guane02 amd:exadell amd:smexa; do
  srun -p "${n%%:*}" -w "${n##*:}" -N1 -n1 -c1 -t 00:02:00 lscpu > "$OUT/lscpu-${n##*:}.txt" 2>&1
done
sinfo -N -h -p amd -o '%N %C %e %t' > "$OUT/sinfo-amd.txt" 2>&1
squeue -h -p amd -o '%i %u %C %T %M %l %r %S' > "$OUT/squeue-amd.txt" 2>&1
(cd "$OUT" && find . -type f ! -name salidas.sha256 | sort | xargs sha256sum) > "$OUT/salidas.sha256"

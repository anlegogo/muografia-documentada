#!/bin/bash
# Equivalence check before switching the campaign cycle to the launcher with
# parallel block verification. Both launchers run without --enviar on the same
# state (cycle stopped, nothing submitted in between); the plan must be identical:
# campaign id, verified rows, blocked rows and every planned sbatch command.
# Run on guane with the cycle stopped:
#   bash -l campana_114_validar_lanzador_v2.sh
set -uo pipefail
BASE="$HOME/oe1-trabajo/campana-114-7c120ce"
REPO="$BASE/replica"
V2="$BASE/herramientas-v2"
OUT="$BASE/validacion-lanzador-v2"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
PLAN="$REPO/objetivo-1/evidencias/preparacion-campana-114"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
ARGS=(--manifiesto "$PLAN/manifiesto-114-344M.csv" --arbol "$HOME/oe1-trabajo/produccion-receta"
      --temporal "$HOME/muography-scratch/oe1-114-344M-intentos" --salida "$HOME/muography-scratch/oe1-114-344M-publicados"
      --receta "$RECETA" --python "$PY" --threads 64 --max-trabajos 4 --particion amd --tiempo 00:15:00 --memoria 8G)
test ! -e "$OUT" || { echo "validacion ya existe"; exit 2; }
pgrep -f "^bash -l campana_114_lanzar_v[0-9].sh ciclo" && { echo "hay un ciclo activo"; exit 2; }
mkdir -p "$OUT"
(cd "$V2" && sha256sum -- *) > "$OUT/herramientas-v2.sha256"
(cd "$REPO/herramientas" && sha256sum -- *) > "$OUT/herramientas-replica.sha256"
cd "$REPO" || exit 2
t0=$(date +%s.%N)
"$PY" herramientas/lanzar_campana_angular.py "${ARGS[@]}" > "$OUT/anterior.json" 2> "$OUT/anterior.err"; echo "anterior exit=$?"
t1=$(date +%s.%N)
OE1_HERRAMIENTAS="$REPO/herramientas" OE1_VERIFICACION_PROCESOS=8 "$PY" "$V2/lanzar_campana_angular.py" "${ARGS[@]}" > "$OUT/nuevo.json" 2> "$OUT/nuevo.err"; echo "nuevo exit=$?"
t2=$(date +%s.%N)
"$PY" - "$OUT/anterior.json" "$OUT/nuevo.json" "$t0" "$t1" "$t2" <<'PYEOF' | tee "$OUT/comparacion.txt"
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
t0, t1, t2 = map(float, sys.argv[3:6])
keys = ['campaign_id', 'submitted', 'verified', 'blocked_prior_attempts', 'queue_jobs', 'free_slots']
same = all(a[k] == b[k] for k in keys) and [p['command'] for p in a['planned']] == [p['command'] for p in b['planned']]
print('verificadas', len(a['verified']), len(b['verified']), '| planificadas', [p['row'] for p in a['planned']], [p['row'] for p in b['planned']])
print(f'duracion anterior {t1 - t0:.1f} s | nuevo {t2 - t1:.1f} s')
print('IDENTICOS' if same else 'DIFERENTES')
PYEOF

#!/bin/bash
# Submission passes of the 114-view campaign (replica 7c120ce, amd partition),
# as recorded in ACUERDO_CAMPANA_114.md. Run on guane:
#   bash -l campana_114_lanzar.sh una N        # one pass with at most N jobs
#   bash -l campana_114_lanzar.sh ciclo N      # one pass per minute until done or stopped
# The cycle stops when all 1,026 blocks are verified, when a row appears in
# blocked_prior_attempts or when the launcher fails. Create $LOG/DETENER to stop it.
set -uo pipefail
BASE="$HOME/oe1-trabajo/campana-114-7c120ce"
REPO="$BASE/replica"
LOG="$BASE/envios"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
PLAN="$REPO/objetivo-1/evidencias/preparacion-campana-114"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
TEMPORAL="$HOME/muography-scratch/oe1-114-344M-intentos"
SALIDA="$HOME/muography-scratch/oe1-114-344M-publicados"
MODO="${1:-}"; MAX="${2:-4}"
cd "$REPO" || exit 2
mkdir -p "$LOG"
pasada() {
  local sello rc
  sello="$(date '+%Y%m%dT%H%M%S')"
  "$PY" herramientas/lanzar_campana_angular.py --manifiesto "$PLAN/manifiesto-114-344M.csv" \
    --arbol "$ARBOL" --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" --python "$PY" \
    --threads 64 --max-trabajos "$MAX" --particion amd --tiempo 00:15:00 --memoria 8G --enviar \
    > "$LOG/lanzador-$sello.stdout.json" 2> "$LOG/lanzador-$sello.stderr.txt"
  rc=$?
  echo "$rc" > "$LOG/lanzador-$sello.exit_code.txt"
  if [ "$rc" -ne 0 ]; then echo "$sello PARADA lanzador exit=$rc"; return 2; fi
  "$PY" - "$LOG/lanzador-$sello.stdout.json" "$sello" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1]))
sent = [p['row'] for p in d['planned']]
print(f"{sys.argv[2]} enviadas={sent} verificadas={len(d['verified'])}/1026 bloqueadas={d['blocked_prior_attempts']} cola_previa={d['queue_jobs']}", flush=True)
sys.exit(3 if d['blocked_prior_attempts'] else (4 if len(d['verified']) == 1026 else 0))
PYEOF
}
case "$MODO" in
una) pasada ;;
ciclo)
  rm -f "$LOG/DETENER"
  while [ ! -e "$LOG/DETENER" ]; do
    pasada >> "$LOG/ciclo.log" 2>&1
    rc=$?
    if [ "$rc" -eq 4 ]; then echo "$(date '+%Y%m%dT%H%M%S') COMPLETO" >> "$LOG/ciclo.log"; break; fi
    if [ "$rc" -ne 0 ]; then echo "$(date '+%Y%m%dT%H%M%S') PARADA codigo=$rc" >> "$LOG/ciclo.log"; break; fi
    sleep 60
  done ;;
*) echo "uso: campana_114_lanzar.sh una|ciclo [max_trabajos]"; exit 2 ;;
esac

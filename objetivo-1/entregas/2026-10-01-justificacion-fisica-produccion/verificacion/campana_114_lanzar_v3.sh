#!/bin/bash
# Submission passes of the 114-view campaign (replica 7c120ce, amd partition),
# as recorded in ACUERDO_CAMPANA_114.md. Run on guane:
#   bash -l campana_114_lanzar_v3.sh una N        # one pass with at most N jobs
#   bash -l campana_114_lanzar_v3.sh ciclo N      # one pass per minute until done or stopped
# The cycle stops when all 1,026 blocks are verified, when a row stays in
# blocked_prior_attempts or when the launcher fails. Create $LOG/DETENER to stop it.
# v3: same as v2 with a 10 s pause between passes (passes grow with the number of
# verified blocks: 20 s at 170 blocks).
# v2: /home is NFS; a block published on a compute node may not be visible on guane
# for some seconds (row 28, 2026-10-02 18:38). A blocked row is re-checked with a
# pass without --enviar after 90 s; the cycle stops only if it is still blocked.
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
pasada() {  # $1 = --enviar, or nothing for a pass without submission
  local sello rc
  sello="$(date '+%Y%m%dT%H%M%S')"
  [ -n "${1:-}" ] || sello="${sello}_sin_envio"
  "$PY" herramientas/lanzar_campana_angular.py --manifiesto "$PLAN/manifiesto-114-344M.csv" \
    --arbol "$ARBOL" --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" --python "$PY" \
    --threads 64 --max-trabajos "$MAX" --particion amd --tiempo 00:15:00 --memoria 8G ${1:-} \
    > "$LOG/lanzador-$sello.stdout.json" 2> "$LOG/lanzador-$sello.stderr.txt"
  rc=$?
  echo "$rc" > "$LOG/lanzador-$sello.exit_code.txt"
  if [ "$rc" -ne 0 ]; then echo "$sello PARADA lanzador exit=$rc"; return 2; fi
  "$PY" - "$LOG/lanzador-$sello.stdout.json" "$sello" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1]))
sent = [p['row'] for p in d['planned']] if d['submitted'] else []
print(f"{sys.argv[2]} enviadas={sent} verificadas={len(d['verified'])}/1026 bloqueadas={d['blocked_prior_attempts']} cola_previa={d['queue_jobs']}", flush=True)
sys.exit(3 if d['blocked_prior_attempts'] else (4 if len(d['verified']) == 1026 else 0))
PYEOF
}
case "$MODO" in
una) pasada --enviar ;;
ciclo)
  rm -f "$LOG/DETENER"
  while [ ! -e "$LOG/DETENER" ]; do
    pasada --enviar >> "$LOG/ciclo.log" 2>&1
    rc=$?
    if [ "$rc" -eq 3 ]; then
      sleep 90
      pasada >> "$LOG/ciclo.log" 2>&1
      rc=$?
      [ "$rc" -ne 0 ] || echo "$(date '+%Y%m%dT%H%M%S') bloqueo no confirmado tras 90 s (visibilidad NFS); se continua" >> "$LOG/ciclo.log"
    fi
    if [ "$rc" -eq 4 ]; then echo "$(date '+%Y%m%dT%H%M%S') COMPLETO" >> "$LOG/ciclo.log"; break; fi
    if [ "$rc" -ne 0 ]; then echo "$(date '+%Y%m%dT%H%M%S') PARADA codigo=$rc" >> "$LOG/ciclo.log"; break; fi
    sleep 10
  done ;;
*) echo "uso: campana_114_lanzar_v3.sh una|ciclo [max_trabajos]"; exit 2 ;;
esac

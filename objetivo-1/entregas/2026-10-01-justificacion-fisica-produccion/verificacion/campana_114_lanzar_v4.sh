#!/bin/bash
# Submission passes of the 114-view campaign (replica 7c120ce, amd partition),
# as recorded in ACUERDO_CAMPANA_114.md. Run on guane:
#   bash -l campana_114_lanzar_v4.sh ciclo N      # passes every 10 s until done or stopped
# v4: /home is NFS and a block published on a compute node can be invisible on guane
# for some seconds, so a row may appear in blocked_prior_attempts right after its
# job ends. The launcher still submits the other rows in that pass, so the cycle no
# longer pauses: it stops only if the same row is reported blocked in three
# consecutive passes (about three minutes), when the launcher fails, or when all
# 1,026 blocks are verified. Create $LOG/DETENER to stop it.
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
  "$PY" - "$LOG/lanzador-$sello.stdout.json" "$sello" "$LOG/bloqueadas-ultima.txt" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1]))
sent = [p['row'] for p in d['planned']]
blocked = d['blocked_prior_attempts']
open(sys.argv[3], 'w').write(' '.join(map(str, blocked)))
print(f"{sys.argv[2]} enviadas={sent} verificadas={len(d['verified'])}/1026 bloqueadas={blocked} cola_previa={d['queue_jobs']}", flush=True)
sys.exit(3 if blocked else (4 if len(d['verified']) == 1026 else 0))
PYEOF
}
case "$MODO" in
ciclo)
  rm -f "$LOG/DETENER"
  previa1=""; previa2=""
  while [ ! -e "$LOG/DETENER" ]; do
    pasada >> "$LOG/ciclo.log" 2>&1
    rc=$?
    if [ "$rc" -eq 3 ]; then
      actual="$(cat "$LOG/bloqueadas-ultima.txt")"
      persistente=""
      for fila in $actual; do
        case " $previa1 " in *" $fila "*) case " $previa2 " in *" $fila "*) persistente="$persistente $fila";; esac;; esac
      done
      if [ -n "$persistente" ]; then
        echo "$(date '+%Y%m%dT%H%M%S') PARADA filas bloqueadas en tres pasadas seguidas:$persistente" >> "$LOG/ciclo.log"; break
      fi
      previa2="$previa1"; previa1="$actual"; rc=0
    else
      previa2=""; previa1=""
    fi
    if [ "$rc" -eq 4 ]; then echo "$(date '+%Y%m%dT%H%M%S') COMPLETO" >> "$LOG/ciclo.log"; break; fi
    if [ "$rc" -ne 0 ]; then echo "$(date '+%Y%m%dT%H%M%S') PARADA codigo=$rc" >> "$LOG/ciclo.log"; break; fi
    sleep 10
  done ;;
*) echo "uso: campana_114_lanzar_v4.sh ciclo [max_trabajos]"; exit 2 ;;
esac

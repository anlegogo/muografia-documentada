#!/bin/bash
# One pass of the director's launcher for the geo-train-06 pilot (36 blocks),
# with --enviar, as in GUIA_SIGUIENTE_ETAPA_OE1.md. Repeat when slots free up;
# rows already recorded are never resubmitted by the launcher. Run on guane:
#   bash -l lanzar_piloto.sh
set -uo pipefail
BASE="$HOME/oe1-trabajo/integracion-c9442d6"
REPO="$BASE/replica"
LOG="$BASE/piloto"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
TEMPORAL="$HOME/muography-scratch/oe1-piloto-v2-intentos"
SALIDA="$HOME/muography-scratch/oe1-piloto-v2-publicados"
DISENO="$REPO/objetivo-1/evidencias/piloto-propuesto-siete-actividades"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
cd "$REPO" || exit 2
mkdir -p "$LOG"
SELLO="$(date '+%Y%m%dT%H%M%S')"
"$PY" herramientas/lanzar_campana_angular.py --manifiesto "$DISENO/manifiesto-piloto-propuesto.csv" \
  --arbol "$ARBOL" --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" \
  --python "$PY" --threads 24 --max-trabajos 4 --enviar \
  > "$LOG/lanzador-$SELLO.stdout.json" 2> "$LOG/lanzador-$SELLO.stderr.txt"
RC=$?
echo "$RC" > "$LOG/lanzador-$SELLO.exit_code.txt"
squeue -h -u "$(id -un)" -o '%i|%j|%T|%M|%N' > "$LOG/squeue-$SELLO.txt" 2>&1
echo "pasada=$SELLO exit=$RC"
"$PY" -c "import json,sys; d=json.load(open(sys.argv[1])); print('submitted', [p['row'] for p in d['planned']], 'verified', len(d['verified']), 'blocked', d['blocked_prior_attempts'], 'queue_before', d['queue_jobs'])" "$LOG/lanzador-$SELLO.stdout.json" 2>/dev/null || cat "$LOG/lanzador-$SELLO.stderr.txt"
cat "$LOG/squeue-$SELLO.txt"

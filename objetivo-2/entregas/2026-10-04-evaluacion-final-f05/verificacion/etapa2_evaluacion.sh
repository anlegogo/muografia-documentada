#!/bin/bash
# Evaluación conjunta en CPU, una sola vez, con informe nuevo.
source /workspace/comun.sh
source "$W/venv/bin/activate"; cd "$W/repo"
marca ETAPA2_INICIO
python "$SCRIPT" evaluate --data "$DATA" --weights "$WEIGHTS" --output "$OUT" --report "$OUT/informe-v1" > "$OUT/registro/evaluate.log" 2>&1 \
  && marca "ETAPA2_OK $(tail -1 "$OUT/registro/evaluate.log")" || { marca "ETAPA2_FALLO $(tail -2 "$OUT/registro/evaluate.log" | tr '\n' ' ')"; exit 1; }

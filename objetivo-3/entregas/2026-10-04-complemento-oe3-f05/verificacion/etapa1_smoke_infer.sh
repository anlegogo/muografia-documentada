#!/bin/bash
# Para cada modelo: prueba técnica (smoke) y, si pasa, inferencia de 1 %, 10 % y 50 % (una GPU).
source /workspace/comun.sh
source "$W/venv/bin/activate"; cd "$W/repo"
marca ETAPA1_INICIO
(
set -euo pipefail
for MODEL in "${MODELS[@]}"; do
  python "$SCRIPT" smoke "${COMMON_ARGS[@]}" --model "$MODEL" --device cuda:0 2>&1 | tee "$OUT/registro/smoke-$MODEL.log"
  echo "$(date -u +%FT%TZ) SMOKE_OK $MODEL" | tee -a "$W/estado.log"
  python "$SCRIPT" infer "${COMMON_ARGS[@]}" --model "$MODEL" --device cuda:0 2>&1 | tee "$OUT/registro/infer-$MODEL.log"
  echo "$(date -u +%FT%TZ) MODELO_OK $MODEL" | tee -a "$W/estado.log"
done
) > "$W/etapa1.consola" 2>&1 && marca ETAPA1_OK || { marca "ETAPA1_FALLO $(tail -3 "$W/etapa1.consola" | tr '\n' ' ')"; exit 1; }

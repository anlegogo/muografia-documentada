#!/bin/bash
# Inferencia de los ocho modelos con una GPU (bucle literal de la guía).
source /workspace/comun.sh
source "$W/venv/bin/activate"; cd "$W/repo"
marca ETAPA1_INICIO
(
set -euo pipefail
export CUDA_VISIBLE_DEVICES=0
for MODEL in unet_original cgan_original B1_C0 B1_C1 B2_C0 B2_C1 B3_C0 B3_C1; do
  python "$SCRIPT" infer --data "$DATA" --weights "$WEIGHTS" \
    --output "$OUT" --model "$MODEL" --device cuda 2>&1 | tee "$OUT/registro/infer-$MODEL.log"
  echo "$(date -u +%FT%TZ) MODELO_OK $MODEL" | tee -a "$W/estado.log"
done
) > "$W/etapa1.consola" 2>&1 && marca ETAPA1_OK || { marca "ETAPA1_FALLO $(tail -2 "$W/etapa1.consola" | tr '\n' ' ')"; exit 1; }

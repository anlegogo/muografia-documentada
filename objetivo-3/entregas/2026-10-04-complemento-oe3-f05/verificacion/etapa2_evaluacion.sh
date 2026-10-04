#!/bin/bash
# Evaluación conjunta en CPU, una sola vez, con informe nuevo; luego manifiesto SHA-256 de la salida.
source /workspace/comun.sh
source "$W/venv/bin/activate"; cd "$W/repo"
marca ETAPA2_INICIO
python "$SCRIPT" evaluate "${COMMON_ARGS[@]}" --report "$OUT/informe" > "$OUT/registro/evaluate.log" 2>&1 \
  && marca "ETAPA2_OK $(tail -1 "$OUT/registro/evaluate.log")" || { marca "ETAPA2_FALLO $(tail -3 "$OUT/registro/evaluate.log" | tr '\n' ' ')"; exit 1; }
cp "$W/estado.log" "$W/instalar.log" "$W/pesos.log" "$W/etapa1.consola" "$OUT/registro/" 2>/dev/null || true
cd "$W/trabajo" && find complemento-oe3-v1 -type f ! -name 'manifiesto.sha256' -print0 | sort -z | xargs -0 sha256sum > complemento-oe3-v1/manifiesto.sha256
marca "MANIFIESTO_OK $(wc -l < complemento-oe3-v1/manifiesto.sha256) archivos"

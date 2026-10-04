#!/bin/bash
# Bloque 3 de la guía: evaluación y síntesis, las tres parejas en el mismo dispositivo (GPU 0).
source /workspace/comun.sh
source "$W/venv/bin/activate"
cd "$W/repo"
marca ETAPA3_INICIO
(
set -euo pipefail
export CUDA_VISIBLE_DEVICES=0
for PAR in R1 R2 R3; do
  E="$SALIDAS/$PAR/evaluacion"
  python objetivo-2/herramientas/evaluar_ajuste_cgan.py \
    "${COMUN[@]}" --pareja "$PAR" --etapa piloto --dispositivo cuda \
    --control "$SALIDAS/$PAR/piloto/C0" --regional "$SALIDAS/$PAR/piloto/C1" \
    --salida "$E" --figuras 2>&1 | tee "$SALIDAS/$PAR/evaluacion.log"
  python objetivo-2/herramientas/analizar_compromiso_cgan.py \
    --datos "$DATA" --mascaras "$MASCARAS" \
    --comparacion "$E/comparacion-cgan.json" --anomalias "$E/anomalias-cgan.json" \
    --predicciones-iniciales "$E/predicciones-cgan-inicial.npy" \
    --salida "$SALIDAS/$PAR/compromiso" 2>&1 | tee "$SALIDAS/$PAR/compromiso.log"
done
python objetivo-2/herramientas/resumir_repeticion_cgan.py \
  --raiz "$SALIDAS" --etapa piloto --salida "$SALIDAS/sintesis-repeticion.json"
) > "$SALIDAS/bloque3-consola.log" 2>&1
RC=$?
[ $RC -eq 0 ] && marca ETAPA3_OK || marca "ETAPA3_FALLO $(tail -3 "$SALIDAS/bloque3-consola.log" | tr '\n' ' ')"
exit $RC

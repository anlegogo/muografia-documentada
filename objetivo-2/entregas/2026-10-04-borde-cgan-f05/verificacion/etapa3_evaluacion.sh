#!/bin/bash
# Evaluación (las tres parejas en la GPU 0), síntesis e inventario de entrega de la guía.
source /workspace/comun.sh
source "$W/venv/bin/activate"
cd "$W/repo"
marca ETAPA3_INICIO
(
set -euo pipefail
export CUDA_VISIBLE_DEVICES=0
for PAR in B1 B2 B3; do
  python $ORQ "${COMMON[@]}" --fase evaluacion --pareja "$PAR"
done
python $ORQ "${COMMON[@]}" --fase sintesis
) > "$OUT/evaluacion-sintesis-consola.log" 2>&1 || { marca "ETAPA3_FALLO $(tail -2 "$OUT/evaluacion-sintesis-consola.log" | tr '\n' ' ')"; exit 1; }
marca SINTESIS_OK
# La consola del inventario queda fuera de la raíz para no inventariar un archivo en escritura.
python objetivo-2/herramientas/inventariar_entrega_borde.py \
  --raiz "$OUT" --mascaras "$MASKS" --etapa piloto \
  --salida "$OUT/inventario-entrega.json" > "$W/inventario.consola" 2>&1 \
  && marca "INVENTARIO_OK $(tail -1 "$W/inventario.consola")" \
  || { marca "INVENTARIO_FALLO $(tail -2 "$W/inventario.consola" | tr '\n' ' ')"; exit 1; }
marca ETAPA3_OK

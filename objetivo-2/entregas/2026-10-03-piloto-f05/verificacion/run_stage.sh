#!/bin/bash
# Run the director's pilot commands verbatim, saving stdout, stderr and exit code
# of each step. Stage A stops at the first failure.
#   bash run_stage.sh tecnica            (GPU 0, sequential)
#   bash run_stage.sh piloto-unet 0      (one method on one GPU)
#   bash run_stage.sh piloto-cgan 1
#   bash run_stage.sh resumen-piloto
set -uo pipefail
cd /workspace/repo
source /workspace/venv/bin/activate
export OE2_DATA=/workspace/datos-oe1
export OE2_OUT=/workspace/resultados-oe2
LOG=/workspace/logs
mkdir -p "$OE2_OUT" "$LOG"

run() {  # name, command...
  local n="$1"; shift
  printf '%q ' "$@" > "$LOG/$n.comando.txt"; echo >> "$LOG/$n.comando.txt"
  date -u '+%Y-%m-%dT%H:%M:%SZ' > "$LOG/$n.inicio.txt"
  "$@" > "$LOG/$n.stdout.txt" 2> "$LOG/$n.stderr.txt"
  local rc=$?
  echo $rc > "$LOG/$n.exit_code.txt"
  date -u '+%Y-%m-%dT%H:%M:%SZ' > "$LOG/$n.fin.txt"
  echo "$n exit=$rc"
  return $rc
}

E=objetivo-2/herramientas/ejecutar_piloto.py
case "$1" in
  tecnica)
    export CUDA_VISIBLE_DEVICES=0
    run a1-tecnica-unet-corte python $E --config tecnica-unet --data-root "$OE2_DATA" --out-root "$OE2_OUT" --stop-after-epoch 1 || exit 1
    run a2-tecnica-unet-reanudacion python $E --config tecnica-unet --data-root "$OE2_DATA" --out-root "$OE2_OUT" --resume auto || exit 1
    run a3-tecnica-cgan-corte python $E --config tecnica-cgan --data-root "$OE2_DATA" --out-root "$OE2_OUT" --stop-after-epoch 1 || exit 1
    run a4-tecnica-cgan-reanudacion python $E --config tecnica-cgan --data-root "$OE2_DATA" --out-root "$OE2_OUT" --resume auto || exit 1
    run a5-resumen-tecnico python objetivo-2/herramientas/resumir_piloto.py --stage tecnica --out-root "$OE2_OUT" --output "$OE2_OUT/resumen-tecnico.json"
    ;;
  piloto-unet|piloto-cgan)
    export CUDA_VISIBLE_DEVICES="$2"
    run "b-$1" python $E --config "$1" --data-root "$OE2_DATA" --out-root "$OE2_OUT"
    ;;
  resumen-piloto)
    run b-resumen-piloto python objetivo-2/herramientas/resumir_piloto.py --stage piloto --out-root "$OE2_OUT" --output "$OE2_OUT/resumen-piloto.json"
    ;;
esac

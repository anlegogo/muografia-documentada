#!/bin/bash
# Single entry point for the cGAN C0/C1 continuation on the pod. Runs the
# director's commands from INSTRUCCIONES_CONTINUACION_CGAN_F05.md verbatim, in
# order: masks -> technical GPU check (4 runs + acceptance) -> 5-epoch C0/C1
# (sequential, one GPU) -> evaluation with figures. Every step stores command,
# stdout, stderr, exit code and UTC start/end in $W/logs. Idempotent: a step
# whose exit code is 0 is skipped; an unfinished arm is resumed with --reanudar.
#   bash lanzar.sh /workspace
set -uo pipefail
W="${1:-/workspace}"
cd "$W/repo" || exit 2
source "$W/venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0
DATA="$W/insumos"
PESOS="$W/insumos/pesos/cgan-best.pt"
MASCARAS="$W/trabajo/mascaras-ajuste-v1"
SALIDAS="$W/trabajo/cgan-ajuste-v1"
LOG="$W/logs"
H=objetivo-2/herramientas
mkdir -p "$LOG" "$W/trabajo"

run() {  # name, command...
  local n="$1"; shift
  if [ -f "$LOG/$n.exit_code.txt" ] && [ "$(cat "$LOG/$n.exit_code.txt")" = 0 ]; then
    echo "$n ya completado"; return 0; fi
  printf '%q ' "$@" > "$LOG/$n.comando.txt"; echo >> "$LOG/$n.comando.txt"
  date -u '+%Y-%m-%dT%H:%M:%SZ' > "$LOG/$n.inicio.txt"
  "$@" > "$LOG/$n.stdout.txt" 2> "$LOG/$n.stderr.txt"
  local rc=$?
  echo $rc > "$LOG/$n.exit_code.txt"
  date -u '+%Y-%m-%dT%H:%M:%SZ' > "$LOG/$n.fin.txt"
  echo "$n exit=$rc $(date -u '+%H:%M:%S')"
  return $rc
}

completed() {
  python -c "import json,sys;s=json.load(open('$1/summary.json'));sys.exit(0 if s['completed'] else 1)" 2>/dev/null
}

[ -d "$MASCARAS" ] || run 01-mascaras python $H/datos_ajuste.py --datos "$DATA" --salida "$MASCARAS" || exit 1

for RAMA in C0 C1; do
  run "02-tecnica-$RAMA-continua" python $H/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-continua" || exit 1
  run "03-tecnica-$RAMA-corte" python $H/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --parar-tras 1 || exit 1
  run "04-tecnica-$RAMA-reanudacion" python $H/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --reanudar || exit 1
done

run 05-aceptacion-gpu python $H/revisar_ajuste_cgan.py --C0-continua "$SALIDAS/tecnica/C0-continua" --C0-recuperada "$SALIDAS/tecnica/C0-recuperada" --C1-continua "$SALIDAS/tecnica/C1-continua" --C1-recuperada "$SALIDAS/tecnica/C1-recuperada" --exigir-gpu --salida "$SALIDAS/aceptacion-gpu-cgan.json" || exit 1

for RAMA in C0 C1; do
  D="$SALIDAS/piloto/$RAMA"
  if [ -f "$D/summary.json" ] && completed "$D"; then echo "piloto $RAMA ya completado"; continue; fi
  if [ -f "$D/last.pt" ]; then
    n=$(ls "$LOG" | grep -c "^06-piloto-$RAMA.*exit_code" || true)
    run "06-piloto-$RAMA-reanudacion-$n" python $H/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa piloto --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$D" --aceptacion-gpu "$SALIDAS/aceptacion-gpu-cgan.json" --reanudar || exit 1
  else
    run "06-piloto-$RAMA" python $H/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa piloto --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$D" --aceptacion-gpu "$SALIDAS/aceptacion-gpu-cgan.json" || exit 1
  fi
done

run 07-evaluacion python $H/evaluar_ajuste_cgan.py --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --control "$SALIDAS/piloto/C0" --regional "$SALIDAS/piloto/C1" --etapa piloto --dispositivo cuda --salida "$SALIDAS/evaluacion-piloto" --figuras || exit 1
(cd "$SALIDAS" && find . \( -name '*.pt' -o -name '*.npy' \) | sort | xargs sha256sum) > "$W/binarios.sha256"
echo LANZAMIENTO_COMPLETO

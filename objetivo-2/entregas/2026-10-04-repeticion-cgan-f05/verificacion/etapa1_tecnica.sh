#!/bin/bash
# Bloque 1 de la guía: comprobación GPU por pareja, en paralelo (una pareja por GPU).
source /workspace/comun.sh
source "$W/venv/bin/activate"
cd "$W/repo"
marca ETAPA1_INICIO

tecnica(){  # comandos literales del bloque 1 para una pareja
  set -euo pipefail
  PAR=$1
  T="$SALIDAS/$PAR/tecnica"
  mkdir -p "$T"
  for RAMA in C0 C1; do
    python objetivo-2/herramientas/ejecutar_ajuste_cgan.py \
      "${COMUN[@]}" --pareja "$PAR" --rama "$RAMA" --etapa tecnica \
      --salida "$T/$RAMA-continua" 2>&1 | tee "$T/$RAMA-continua.log"
    python objetivo-2/herramientas/ejecutar_ajuste_cgan.py \
      "${COMUN[@]}" --pareja "$PAR" --rama "$RAMA" --etapa tecnica \
      --salida "$T/$RAMA-recuperada" --parar-tras 1 2>&1 | tee "$T/$RAMA-interrumpida.log"
    python objetivo-2/herramientas/ejecutar_ajuste_cgan.py \
      "${COMUN[@]}" --pareja "$PAR" --rama "$RAMA" --etapa tecnica \
      --salida "$T/$RAMA-recuperada" --reanudar 2>&1 | tee "$T/$RAMA-recuperada.log"
  done
  python objetivo-2/herramientas/revisar_ajuste_cgan.py --pareja "$PAR" \
    --C0-continua "$T/C0-continua" --C0-recuperada "$T/C0-recuperada" \
    --C1-continua "$T/C1-continua" --C1-recuperada "$T/C1-recuperada" \
    --exigir-gpu --salida "$SALIDAS/$PAR/aceptacion-gpu.json" \
    2>&1 | tee "$SALIDAS/$PAR/auditoria-gpu.log"
}

declare -A PID
for PAR in R1 R2 R3; do
  mkdir -p "$SALIDAS/$PAR"
  ( export CUDA_VISIBLE_DEVICES=${GPU[$PAR]}; tecnica "$PAR" ) > "$SALIDAS/$PAR/bloque1-consola.log" 2>&1 &
  PID[$PAR]=$!
  marca "TECNICA_LANZADA $PAR GPU${GPU[$PAR]}"
done
FALLO=0
for PAR in R1 R2 R3; do
  if wait "${PID[$PAR]}"; then marca "TECNICA_FIN $PAR rc=0 $(tail -1 "$SALIDAS/$PAR/auditoria-gpu.log")"
  else marca "TECNICA_FALLO $PAR $(tail -3 "$SALIDAS/$PAR/bloque1-consola.log" | tr '\n' ' ')"; FALLO=1; fi
done
for PAR in R1 R2 R3; do
  python - "$SALIDAS/$PAR/aceptacion-gpu.json" <<'PY' || FALLO=1
import json,sys
a=json.load(open(sys.argv[1]))
ok=a.get('technical_checks_passed') is True and a.get('gpu_accepted') is True and a.get('exact_recovery') is True
print(sys.argv[1],'gpu_accepted',a.get('gpu_accepted'),'exact_recovery',a.get('exact_recovery'))
sys.exit(0 if ok else 1)
PY
done
[ $FALLO -eq 0 ] && marca ETAPA1_ACEPTADA_TRES || marca ETAPA1_NO_ACEPTADA
exit $FALLO

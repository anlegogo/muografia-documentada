#!/bin/bash
# Bloque 2 de la guía: seis continuaciones de cinco épocas, una pareja por GPU en paralelo.
source /workspace/comun.sh
source "$W/venv/bin/activate"
cd "$W/repo"
set -euo pipefail
for PAR in R1 R2 R3; do
  test -f "$SALIDAS/$PAR/aceptacion-gpu.json"
done
set +e
marca ETAPA2_INICIO

piloto(){  # comandos literales del bloque 2 para una pareja
  set -euo pipefail
  PAR=$1
  mkdir -p "$SALIDAS/$PAR/piloto"
  for RAMA in C0 C1; do
    python objetivo-2/herramientas/ejecutar_ajuste_cgan.py \
      "${COMUN[@]}" --pareja "$PAR" --rama "$RAMA" --etapa piloto \
      --salida "$SALIDAS/$PAR/piloto/$RAMA" \
      --aceptacion-gpu "$SALIDAS/$PAR/aceptacion-gpu.json" \
      2>&1 | tee "$SALIDAS/$PAR/piloto/$RAMA.log"
  done
}

declare -A PID
for PAR in R1 R2 R3; do
  ( export CUDA_VISIBLE_DEVICES=${GPU[$PAR]}; piloto "$PAR" ) > "$SALIDAS/$PAR/bloque2-consola.log" 2>&1 &
  PID[$PAR]=$!
  marca "PILOTO_LANZADO $PAR GPU${GPU[$PAR]}"
done
FALLO=0
for PAR in R1 R2 R3; do
  if wait "${PID[$PAR]}"; then marca "PILOTO_FIN $PAR rc=0"
  else marca "PILOTO_FALLO $PAR $(tail -3 "$SALIDAS/$PAR/bloque2-consola.log" | tr '\n' ' ')"; FALLO=1; fi
done
[ $FALLO -eq 0 ] && marca ETAPA2_OK || marca ETAPA2_CON_FALLOS
exit $FALLO

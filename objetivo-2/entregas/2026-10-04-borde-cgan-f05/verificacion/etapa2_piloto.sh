#!/bin/bash
# Fase piloto de la guía: cada pareja en su misma GPU (C0 y luego C1), en paralelo.
source /workspace/comun.sh
source "$W/venv/bin/activate"
cd "$W/repo"
marca ETAPA2_INICIO
declare -A PID
for PAR in B1 B2 B3; do
  ( export CUDA_VISIBLE_DEVICES=${GPU[$PAR]}
    python $ORQ "${COMMON[@]}" --fase piloto --pareja "$PAR" ) > "$OUT/$PAR-piloto-consola.log" 2>&1 &
  PID[$PAR]=$!
  marca "PILOTO_LANZADO $PAR GPU${GPU[$PAR]}"
done
FALLO=0
for PAR in B1 B2 B3; do
  if wait "${PID[$PAR]}"; then marca "PILOTO_FIN $PAR rc=0"
  else marca "PILOTO_FALLO $PAR $(tail -2 "$OUT/$PAR-piloto-consola.log" | tr '\n' ' ')"; FALLO=1; fi
done
[ $FALLO -eq 0 ] && marca ETAPA2_OK || marca ETAPA2_CON_FALLOS
exit $FALLO

#!/bin/bash
# Fase técnica de la guía: una pareja por GPU, en paralelo, raíz compartida.
source /workspace/comun.sh
source "$W/venv/bin/activate"
cd "$W/repo"
marca ETAPA1_INICIO
declare -A PID
for PAR in B1 B2 B3; do
  ( export CUDA_VISIBLE_DEVICES=${GPU[$PAR]}
    python $ORQ "${COMMON[@]}" --fase tecnica --pareja "$PAR" ) > "$OUT/$PAR-tecnica-consola.log" 2>&1 &
  PID[$PAR]=$!
  marca "TECNICA_LANZADA $PAR GPU${GPU[$PAR]}"
done
FALLO=0
for PAR in B1 B2 B3; do
  if wait "${PID[$PAR]}"; then marca "TECNICA_FIN $PAR rc=0"
  else marca "TECNICA_FALLO $PAR $(tail -2 "$OUT/$PAR-tecnica-consola.log" | tr '\n' ' ')"; FALLO=1; fi
done
for PAR in B1 B2 B3; do
  python - "$OUT/$PAR/aceptacion-gpu.json" "$PAR" <<'PY' || FALLO=1
import json,sys
a=json.load(open(sys.argv[1]))
ok=a.get('schema')=='oe2-cgan-borde-gate-v1' and a.get('pair')==sys.argv[2] and a.get('gpu_accepted') is True and a.get('exact_recovery') is True
print(sys.argv[2],'gpu_accepted',a.get('gpu_accepted'),'exact_recovery',a.get('exact_recovery'),'pair',a.get('pair'))
sys.exit(0 if ok else 1)
PY
done
[ $FALLO -eq 0 ] && marca ETAPA1_ACEPTADA_TRES || marca ETAPA1_NO_ACEPTADA
exit $FALLO

#!/bin/bash
# Portability check of the recipe on the amd partition. One block of 5 million
# primaries (geo-train-06, view 0, fixed seed) is submitted twice with the same
# manifest: legacy with 24 threads and amd with 64 threads. Identical histograms
# show that the binary runs on the AMD nodes and that the result depends neither
# on the partition nor on the thread count. Uses a separate copy of the replica
# with the launcher that accepts --particion/--tiempo. Run on guane:
#   bash -l prueba_amd.sh enviar     # submit both jobs
#   bash -l prueba_amd.sh comparar   # compare once both have finished
set -uo pipefail
BASE="$HOME/oe1-trabajo/prueba-amd"
REPO="$BASE/replica"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
RECETA="$REPO/objetivo-1/contratos/receta-operativa-siete-actividades.json"
MAN="$BASE/manifiesto-prueba-amd.csv"
SCR="$HOME/muography-scratch/oe1-prueba-amd"
case "${1:-}" in
enviar)
  test -d "$REPO" || { echo "falta la réplica de prueba"; exit 2; }
  test ! -e "$MAN" || { echo "la prueba ya fue enviada"; exit 2; }
  printf 'fila,geometria,vista,bloque,semilla,eventos\n0,geo-train-06,0,0,20261002900000,5000000\n' > "$MAN"
  sha256sum "$MAN" "$REPO/herramientas/lanzar_campana_angular.py" > "$BASE/entradas.sha256"
  cd "$REPO" || exit 2
  for P in legacy:24 amd:64; do
    PART="${P%%:*}"; HILOS="${P##*:}"
    "$PY" herramientas/lanzar_campana_angular.py --manifiesto "$MAN" --arbol "$ARBOL" \
      --temporal "$SCR/$PART-intentos" --salida "$SCR/$PART-publicados" --receta "$RECETA" \
      --python "$PY" --threads "$HILOS" --max-trabajos 4 --particion "$PART" --enviar \
      > "$BASE/lanzador-$PART.stdout.json" 2> "$BASE/lanzador-$PART.stderr.txt"
    echo "$PART exit=$?"
  done
  squeue -h -u "$(id -un)" -o '%i|%j|%T|%P|%C|%N'
  ;;
comparar)
  B="geo-train-06/view0/block0000"; S="geo-train-06_view0"
  for PART in legacy amd; do
    echo "== $PART"; cat "$SCR/$PART-publicados/$B/exit_code.txt" 2>&1
    (cd "$SCR/$PART-publicados/$B" && sha256sum "${S}_hist.csv" "${S}_hist_sin_corte.csv" "${S}_gen.csv")
  done
  "$PY" - "$SCR/legacy-publicados/$B/$S.meta.json" "$SCR/amd-publicados/$B/$S.meta.json" <<'PYEOF'
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
print('claves distintas en metadatos:', diff)
for k in ('threads', 'wall_seconds', 'seconds_per_event', 'detected_in_bins', 'detected_all_energies', 'nominal_in_window'):
    print(k, a.get(k), b.get(k))
PYEOF
  for PART in legacy amd; do
    ID=$(cat "$SCR/$PART-publicados.operacion/0.json" | "$PY" -c 'import json,sys;print(json.load(sys.stdin).get("job_id"))')
    sacct -X -j "$ID" -P -o JobID,JobName,Partition,AllocCPUS,State,ExitCode,Elapsed,NodeList | tail -1
  done
  ;;
*) echo "uso: prueba_amd.sh enviar|comparar"; exit 2;;
esac

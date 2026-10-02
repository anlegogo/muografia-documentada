#!/bin/bash
# Integration test of the production chain (not a production run): two blocks
# of 1e5 primaries for geo-train-06 view 0, launched with lanzar_v1.py,
# then merged with fusionar_v1.py once both blocks are published.
#   bash prueba_integracion.sh lanzar     # on guane
#   bash prueba_integracion.sh fusionar   # after the two jobs finished
set -euo pipefail
cd "$(dirname "$0")"
SALIDA="$HOME/muography-scratch/oe1-v1-prueba"
case "${1:-}" in
  lanzar)
    test ! -e manifiesto-prueba.csv || { echo "manifiesto-prueba.csv ya existe"; exit 2; }
    { head -1 manifiesto-receta-k1.csv
      awk -F, -v OFS=, '$2 == "geo-train-06" && $3 == 0 {$6 = 100000; print}' manifiesto-receta-k1.csv
    } > manifiesto-prueba.csv
    cat manifiesto-prueba.csv
    python3 lanzar_v1.py --manifiesto "$PWD/manifiesto-prueba.csv" --salida "$SALIDA" --dry-run
    python3 lanzar_v1.py --manifiesto "$PWD/manifiesto-prueba.csv" --salida "$SALIDA"
    ;;
  fusionar)
    python3 lanzar_v1.py --manifiesto "$PWD/manifiesto-prueba.csv" --salida "$SALIDA" --dry-run
    python3 fusionar_v1.py --manifiesto manifiesto-prueba.csv --salida "$SALIDA" --destino "$SALIDA-fusion"
    ;;
  *) echo "uso: $0 lanzar|fusionar"; exit 2 ;;
esac

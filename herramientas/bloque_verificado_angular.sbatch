#!/bin/bash
# Arguments are paths passed by lanzar_campana_angular.py, not shell fragments.
set -euo pipefail
[[ $# -eq 11 ]] || { echo 'Se requieren once argumentos' >&2; exit 2; }
module purge
module load gnu14/14.2.0 geant4/11.4.2
exec "$7" "$9" --manifiesto "$1" --fila "$2" \
  --arbol "$3" --temporal "$4" --salida "$5" --receta "$6" --threads "$8" \
  --sha-manifiesto "${10}" --sha-receta "${11}" --ejecutar

#!/bin/bash
# Etapa 0: código, entorno, datos, máscaras y registro inicial de la guía.
set -uo pipefail
source /workspace/comun.sh
cd "$W"
marca ETAPA0_INICIO
[ -d "$W/repo" ] || git clone -q --branch oe2/repeticion-cgan-f05 "$W/repo.bundle" "$W/repo" || { marca CLONE_FALLO; exit 1; }
bash "$W/instalar_entorno.sh" "$W" > "$W/instalar.log" 2>&1 || { marca INSTALAR_FALLO; exit 1; }
marca ENTORNO_OK
python3 "$W/sincronizar_datos.py" "$W/fuentes-drive.tsv" "$DATA" > "$W/datos.log" 2>&1 || { marca DATOS_FALLO; exit 1; }
marca DATOS_OK "$(tail -1 "$W/datos.log")"
source "$W/venv/bin/activate"
cd "$W/repo"
if [ ! -d "$MASCARAS" ]; then
  python objetivo-2/herramientas/datos_ajuste.py --datos "$DATA" --salida "$MASCARAS" > "$W/mascaras.log" 2>&1 || { marca MASCARAS_FALLO; exit 1; }
fi
marca MASCARAS_OK

# Bloque de preparación literal de la guía.
set -euo pipefail
export CUDA_VISIBLE_DEVICES=0
test ! -e "$SALIDAS"
mkdir -p "$SALIDAS"
git rev-parse HEAD > "$SALIDAS/commit.txt"
git status --porcelain > "$SALIDAS/estado-git.txt"
test ! -s "$SALIDAS/estado-git.txt"
# El venv de uv no trae pip: se usa uv pip freeze como en las entregas anteriores.
python -m pip freeze > "$SALIDAS/entorno.txt" 2>/dev/null || uv pip freeze --python "$(command -v python)" > "$SALIDAS/entorno.txt"
unset CUDA_VISIBLE_DEVICES
nvidia-smi > "$SALIDAS/gpu.txt"
marca ETAPA0_OK "$(cat "$SALIDAS/commit.txt")"

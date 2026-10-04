#!/bin/bash
# Etapa 0: código, entorno, datos, máscaras y registro inicial.
set -uo pipefail
source /workspace/comun.sh
cd "$W"
marca ETAPA0_INICIO
[ -d "$W/repo" ] || git clone -q --branch oe2/borde-cgan-f05 "$W/repo.bundle" "$W/repo" || { marca CLONE_FALLO; exit 1; }
bash "$W/instalar_entorno.sh" "$W" > "$W/instalar.log" 2>&1 || { marca INSTALAR_FALLO; exit 1; }
marca ENTORNO_OK
python3 "$W/sincronizar_datos.py" "$W/fuentes-drive.tsv" "$DATA" > "$W/datos.log" 2>&1 || { marca DATOS_FALLO; exit 1; }
marca DATOS_OK "$(tail -1 "$W/datos.log")"
source "$W/venv/bin/activate"
cd "$W/repo"
if [ ! -d "$MASKS" ]; then
  python objetivo-2/herramientas/datos_ajuste.py --datos "$DATA" --salida "$MASKS" > "$W/mascaras.log" 2>&1 || { marca MASCARAS_FALLO; exit 1; }
fi
marca MASCARAS_OK
set -euo pipefail
test ! -e "$OUT"
mkdir -p "$OUT/registro"
git rev-parse HEAD > "$OUT/registro/commit.txt"
git status --porcelain > "$OUT/registro/estado-git.txt"
# main 156d4f5 contiene archivos confirmados con CRLF; .gitattributes (eol=lf) los marca como
# modificados sin que cambien. Se acepta solo si los bytes de cada uno son idénticos a HEAD.
while read -r st f; do
  [ "$(git rev-parse "HEAD:$f")" = "$(git hash-object --no-filters "$f")" ] || { marca "GIT_MODIFICADO_REAL $f"; exit 1; }
  echo "$f identico_a_HEAD" >> "$OUT/registro/estado-git-verificado.txt"
done < "$OUT/registro/estado-git.txt"
uv pip freeze --python "$(command -v python)" > "$OUT/registro/entorno.txt"
nvidia-smi > "$OUT/registro/gpu.txt"
marca ETAPA0_OK "$(cat "$OUT/registro/commit.txt")"

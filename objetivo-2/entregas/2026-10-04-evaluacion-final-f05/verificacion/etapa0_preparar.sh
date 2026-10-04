#!/bin/bash
# Preparación: código, entorno, pesos (Drive), datos reservados (copiados), registro y preflight.
set -uo pipefail
source /workspace/comun.sh
cd "$W"; marca ETAPA0_INICIO
[ -d "$W/repo" ] || git clone -q --branch oe2/evaluacion-final-f05 "$W/repo.bundle" "$W/repo" || { marca CLONE_FALLO; exit 1; }
bash "$W/instalar_entorno.sh" "$W" > "$W/instalar.log" 2>&1 || { marca INSTALAR_FALLO; exit 1; }
marca ENTORNO_OK
python3 "$W/sincronizar_datos.py" "$W/fuentes-pesos.tsv" "$W" > "$W/pesos.log" 2>&1 || { marca PESOS_FALLO; exit 1; }
marca PESOS_OK "$(tail -1 "$W/pesos.log")"
python3 - <<'PY'
import json
w={m:f'/workspace/pesos/{m}.pt' for m in ['unet_original','cgan_original','B1_C0','B1_C1','B2_C0','B2_C1','B3_C0','B3_C1']}
json.dump(w,open('/workspace/pesos-evaluacion.json','w'),indent=1)
PY
source "$W/venv/bin/activate"; cd "$W/repo"
set -e
mkdir -p "$OUT/registro"
git rev-parse HEAD > "$OUT/registro/commit.txt"; date -u +%FT%TZ > "$OUT/registro/fecha-inicio.txt"
git status --porcelain > "$OUT/registro/estado-git.txt"
while read -r st f; do [ "$(git rev-parse "HEAD:$f")" = "$(git hash-object --no-filters "$f")" ] || { marca "GIT_MODIFICADO_REAL $f"; exit 1; }; done < "$OUT/registro/estado-git.txt"
uv pip freeze --python "$(command -v python)" > "$OUT/registro/entorno.txt"
nvidia-smi > "$OUT/registro/gpu.txt"; cp "$W/entorno/python-torch.txt" "$OUT/registro/"
python "$SCRIPT" preflight --data "$DATA" --weights "$WEIGHTS" --output "$OUT" > "$OUT/registro/preflight.log" 2>&1
marca "ETAPA0_OK $(cat "$OUT/registro/commit.txt") $(tail -1 "$OUT/registro/preflight.log")"

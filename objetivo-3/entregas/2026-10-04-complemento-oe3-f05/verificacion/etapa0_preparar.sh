#!/bin/bash
# Preparación: código, entorno, pesos (Drive), predicciones 5 %, pruebas y preflight.
set -uo pipefail
source /workspace/comun.sh
cd "$W"; marca ETAPA0_INICIO
[ -d "$W/repo" ] || { git init -q "$W/repo" && git -C "$W/repo" fetch -q "$W/repo.bundle" "refs/remotes/origin/main:refs/heads/main" && git -C "$W/repo" checkout -q --detach "$(cat "$W/commit-esperado.txt")"; } || { marca CLONE_FALLO; exit 1; }
[ "$(git -C "$W/repo" rev-parse HEAD)" = "$(cat "$W/commit-esperado.txt")" ] || { marca COMMIT_DISTINTO; exit 1; }
bash "$W/instalar_entorno.sh" "$W" > "$W/instalar.log" 2>&1 || { marca INSTALAR_FALLO; exit 1; }
marca ENTORNO_OK
python3 "$W/sincronizar_datos.py" "$W/fuentes-pesos.tsv" "$W" > "$W/pesos.log" 2>&1 || { marca PESOS_FALLO; exit 1; }
marca PESOS_OK "$(tail -1 "$W/pesos.log")"
python3 - <<'PY'
import json
w={m:f'/workspace/pesos/{m}.pt' for m in ['unet_original','cgan_original','B1_C0','B1_C1','B2_C0','B2_C1','B3_C0','B3_C1']}
json.dump(w,open('/workspace/pesos-locales.json','w'),indent=1)
PY
mkdir -p "$W/existente" && tar -xf "$W/existente-f05.tar" -C "$W/existente" || { marca EXISTENTE_FALLO; exit 1; }
marca "EXISTENTE_OK $(find "$EXISTING" -name '*.npy' | wc -l) NPY"
source "$W/venv/bin/activate"; cd "$W/repo"
set -e
mkdir -p "$OUT/registro"
git rev-parse HEAD > "$OUT/registro/commit.txt"; date -u +%FT%TZ > "$OUT/registro/fecha-inicio.txt"
git status --porcelain > "$OUT/registro/estado-git.txt"
while read -r st f; do [ "$(git rev-parse "HEAD:$f")" = "$(git hash-object --no-filters "$f")" ] || { marca "GIT_MODIFICADO_REAL $f"; exit 1; }; done < "$OUT/registro/estado-git.txt"
uv pip freeze --python "$(command -v python)" > "$OUT/registro/entorno.txt"
nvidia-smi > "$OUT/registro/gpu.txt"; cp "$W/entorno/python-torch.txt" "$OUT/registro/"
python objetivo-3/herramientas/test_complemento_oe3.py > "$OUT/registro/test-complemento.log" 2>&1
python objetivo-3/herramientas/test_flujo_complemento_oe3.py > "$OUT/registro/test-flujo.log" 2>&1
marca PRUEBAS_OK
python "$SCRIPT" preflight "${COMMON_ARGS[@]}" > "$OUT/registro/preflight.log" 2>&1
marca "ETAPA0_OK $(cat "$OUT/registro/commit.txt") $(tail -1 "$OUT/registro/preflight.log")"

#!/bin/bash
# Pod run of the director's CG-04b gradient separation, following
# DIAGNOSTICO_GRADIENTES_CG04B.md literally after environment and data setup.
set -uo pipefail
W=/workspace
cd $W
git clone -q --branch oe2/continuacion-cgan-f05 $W/repo.bundle $W/repo || exit 1
bash $W/instalar_entorno.sh $W > $W/instalar.log 2>&1 || { echo INSTALAR_FALLO; exit 1; }
python3 $W/sincronizar_datos.py $W/fuentes-drive.tsv $W/insumos > $W/datos.log 2>&1 || { echo DATOS_FALLO; exit 1; }
source $W/venv/bin/activate
cd $W/repo
python objetivo-2/herramientas/datos_ajuste.py --datos $W/insumos --salida $W/trabajo/mascaras-ajuste-v1 > $W/mascaras.log 2>&1 || { echo MASCARAS_FALLO; exit 1; }
set -euo pipefail
export CUDA_VISIBLE_DEVICES=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8
DATOS=$W/insumos
MASCARAS=$W/trabajo/mascaras-ajuste-v1
PESOS=$W/insumos/pesos/cgan-best.pt
SALIDA=$W/cg04b

mkdir "$SALIDA"
git rev-parse HEAD > "$SALIDA/commit.txt"
git status --short > "$SALIDA/git-status.txt"
nvidia-smi > "$SALIDA/nvidia-smi.txt"
python -m pip freeze > "$SALIDA/pip-freeze.txt" 2>/dev/null || uv pip freeze --python "$(command -v python)" > "$SALIDA/pip-freeze.txt"

for RAMA in C0 C1; do
  python objetivo-2/herramientas/aislar_gradientes_cgan.py \
    --rama "$RAMA" --datos "$DATOS" --mascaras "$MASCARAS" \
    --pesos "$PESOS" --salida "$SALIDA/$RAMA" \
    2>&1 | tee "$SALIDA/$RAMA-consola.log"
done
echo CG04B_COMPLETO

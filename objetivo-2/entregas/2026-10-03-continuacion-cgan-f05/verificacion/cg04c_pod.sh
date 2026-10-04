#!/bin/bash
# Pod run of the director's CG-04c GPU check (CORRECCION_GRADIENTES_CG04C.md),
# literal commands after environment and data setup. If the auditor accepts
# exact GPU recovery, continue with the two 5-epoch arms and the evaluation as
# INSTRUCCIONES_CONTINUACION_CGAN_F05.md prescribes for that case.
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
DATA="$W/insumos"
PESOS="$W/insumos/pesos/cgan-best.pt"
MASCARAS="$W/trabajo/mascaras-ajuste-v1"
SALIDAS="$W/cgan-cg04c"
test ! -e "$SALIDAS"
mkdir -p "$SALIDAS"
git rev-parse HEAD > "$SALIDAS/commit.txt"
git status --short > "$SALIDAS/git-status.txt"
python -m pip freeze > "$SALIDAS/pip-freeze.txt" 2>/dev/null || uv pip freeze --python "$(command -v python)" > "$SALIDAS/pip-freeze.txt"
nvidia-smi > "$SALIDAS/nvidia-smi.txt"

for RAMA in C0 C1; do
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-continua" 2>&1 | tee "$SALIDAS/$RAMA-continua.log"
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --parar-tras 1 2>&1 | tee "$SALIDAS/$RAMA-parada.log"
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --reanudar 2>&1 | tee "$SALIDAS/$RAMA-reanudada.log"
done

python objetivo-2/herramientas/revisar_ajuste_cgan.py --C0-continua "$SALIDAS/tecnica/C0-continua" --C0-recuperada "$SALIDAS/tecnica/C0-recuperada" --C1-continua "$SALIDAS/tecnica/C1-continua" --C1-recuperada "$SALIDAS/tecnica/C1-recuperada" --exigir-gpu --salida "$SALIDAS/aceptacion-gpu-cgan.json" 2>&1 | tee "$SALIDAS/auditoria.log"
echo ACEPTACION_GPU_OK

# Accepted: two 5-epoch continuations from the original cGAN checkpoint, then evaluation.
for RAMA in C0 C1; do
  python objetivo-2/herramientas/ejecutar_ajuste_cgan.py --rama "$RAMA" --etapa piloto --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/piloto/$RAMA" --aceptacion-gpu "$SALIDAS/aceptacion-gpu-cgan.json" 2>&1 | tee "$SALIDAS/piloto-$RAMA.log"
done
python objetivo-2/herramientas/evaluar_ajuste_cgan.py --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --control "$SALIDAS/piloto/C0" --regional "$SALIDAS/piloto/C1" --etapa piloto --dispositivo cuda --salida "$SALIDAS/evaluacion-piloto" --figuras 2>&1 | tee "$SALIDAS/evaluacion.log"
echo CG04C_COMPLETO

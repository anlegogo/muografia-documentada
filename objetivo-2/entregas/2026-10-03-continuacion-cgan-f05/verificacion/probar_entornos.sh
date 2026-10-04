#!/bin/bash
# Run C0 technical continuous / cut / resume under candidate environment
# settings and report whether epoch-2 digests coincide.
cd /workspace/repo; source /workspace/venv/bin/activate; export CUDA_VISIBLE_DEVICES=0
H=objetivo-2/herramientas; A="--rama C0 --etapa tecnica --datos /workspace/insumos --mascaras /workspace/trabajo/mascaras-ajuste-v1 --pesos /workspace/insumos/pesos/cgan-best.pt"
probe() {  # name, env assignments...
  local n=$1; shift; local O=/workspace/diag-env/$n; rm -rf $O; mkdir -p $O
  env "$@" python $H/ejecutar_ajuste_cgan.py $A --salida $O/continua > $O/c.log 2>&1
  env "$@" python $H/ejecutar_ajuste_cgan.py $A --salida $O/recuperada --parar-tras 1 > $O/r1.log 2>&1
  env "$@" python $H/ejecutar_ajuste_cgan.py $A --salida $O/recuperada --reanudar > $O/r2.log 2>&1
  python -c "
import json
a=json.load(open('$O/continua/history.json'));b=json.load(open('$O/recuperada/history.json'))
print('$n', 'e1', a[0]['generator_sha256']==b[0]['generator_sha256'], 'e2', a[1]['generator_sha256']==b[1]['generator_sha256'], a[1]['generator_sha256'][:12], b[1]['generator_sha256'][:12])" 2>&1 | tail -1
}
probe base DUMMY=1
probe no_cache PYTORCH_NO_CUDA_MEMORY_CACHING=1
probe cudnn_v7 TORCH_CUDNN_V8_API_DISABLED=1
probe eager CUDA_MODULE_LOADING=EAGER

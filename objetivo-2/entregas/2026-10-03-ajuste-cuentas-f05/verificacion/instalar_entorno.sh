#!/bin/bash
# Pod environment for the count-adjustment trial: Python 3.12 venv with the
# versions verified by the director (PyTorch replaced by its CUDA 11.8 build),
# GPU check and environment record. Usage: bash instalar_entorno.sh /workspace
set -euo pipefail
W="${1:-/workspace}"
mkdir -p "$W/entorno"
command -v uv >/dev/null || pip install --break-system-packages -q uv 2>/dev/null \
  || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
[ -x "$W/venv/bin/python" ] || uv venv --python 3.12 "$W/venv"
uv pip install --python "$W/venv/bin/python" --index-strategy unsafe-best-match \
  --extra-index-url https://download.pytorch.org/whl/cu118 \
  torch==2.6.0+cu118 numpy==2.3.5 scipy==1.18.1 scikit-image==0.26.0 \
  matplotlib==3.11.1 filelock==3.16.1 sympy==1.13.1 networkx==3.4.2 mpmath==1.3.0
"$W/venv/bin/python" - <<'EOF' > "$W/entorno/python-torch.txt"
import sys, torch, numpy, scipy, skimage, matplotlib, filelock
assert torch.cuda.is_available(), 'CUDA no disponible'
cap = torch.cuda.get_device_capability(0)
assert cap < (10, 0), f'Capacidad {cap} no soportada por cu118'
print('python', sys.version.split()[0])
print('torch', torch.__version__, 'cuda', torch.version.cuda, 'cudnn', torch.backends.cudnn.version())
print('numpy', numpy.__version__, 'scipy', scipy.__version__, 'skimage', skimage.__version__,
      'matplotlib', matplotlib.__version__, 'filelock', filelock.__version__)
print('gpus', [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())], 'capability', cap)
x = torch.randn(256, 256, device='cuda'); print('smoke', float((x @ x).sum().isfinite()))
EOF
uv pip freeze --python "$W/venv/bin/python" > "$W/entorno/pip-freeze.txt"
nvidia-smi > "$W/entorno/nvidia-smi.txt"
uname -a > "$W/entorno/uname.txt"
cat "$W/entorno/python-torch.txt"
echo ENTORNO_OK

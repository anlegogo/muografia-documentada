#!/bin/bash
# Build the pilot environment on the pod and record it.
set -euo pipefail
cd /workspace
mkdir -p entorno
command -v uv >/dev/null || pip install --break-system-packages -q uv 2>/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv venv --python 3.12 /workspace/venv
source /workspace/venv/bin/activate
uv pip install --index-strategy unsafe-best-match \
  --extra-index-url https://download.pytorch.org/whl/cu118 \
  torch==2.6.0+cu118 numpy==2.4.4 scipy==1.18.1 scikit-image==0.26.0 matplotlib==3.11.1 gdown
{
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  python --version
  python -c "import torch,numpy;print('torch',torch.__version__,'cuda_runtime',torch.version.cuda,'cudnn',torch.backends.cudnn.version());print('numpy',numpy.__version__);print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]);print('capability',torch.cuda.get_device_capability(0))"
} > entorno/python-torch.txt 2>&1
python -m pip freeze > entorno/pip-freeze.txt 2>/dev/null || uv pip freeze > entorno/pip-freeze.txt
nvidia-smi > entorno/nvidia-smi.txt
uname -a > entorno/uname.txt
echo SETUP_OK

"""Entrada del piloto OE2; ejecutar dentro de una asignación GPU de SC3."""
import argparse
import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path

# Debe definirse antes de inicializar CUDA para operaciones deterministas.
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
os.environ.setdefault('MPLCONFIGDIR', str(Path.cwd()/'trabajo/matplotlib-cache'))
import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'implementacion/scripts/training'))
from engine import Trainer
from metrics import compute_ssim, compute_psnr

MANIFEST_SHA = '80db70d75e5ef2c40955881a87dd46b767137c24cb72dc1aa458a71c1efd8b03'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',required=True,choices=['tecnica-cgan','tecnica-unet','piloto-cgan','piloto-unet'])
    p.add_argument('--data-root',required=True)
    p.add_argument('--out-root',required=True)
    p.add_argument('--resume',choices=['none','auto'],default='none')
    p.add_argument('--stop-after-epoch',type=int)
    p.add_argument('--cpu-test',action='store_true',help='Prueba local, no aceptación GPU')
    args = p.parse_args()
    torch.set_num_threads(2)
    if not args.cpu_test and not torch.cuda.is_available():
        raise RuntimeError('Se requiere GPU CUDA asignada; no se cambia a CPU silenciosamente')
    config = json.loads((ROOT/'configuraciones/piloto-v1'/f'{args.config}.json').read_text())
    config['device'] = 'cpu' if args.cpu_test else 'cuda'
    config.update(data_root=args.data_root,
                  data_manifest=str(ROOT/'evidencias/contrato-datos-v1.json'),
                  data_manifest_sha256=MANIFEST_SHA)
    run_dir = Path(args.out_root)/config['run_id']
    trainer = Trainer(config,run_dir)
    runner_sha = hashlib.sha256(Path(__file__).read_text().encode()).hexdigest()
    environment = {'python':platform.python_version(),'torch':torch.__version__,
                   'numpy':np.__version__,'cuda_runtime':torch.version.cuda,
                   'gpu':torch.cuda.get_device_name() if not args.cpu_test else None,
                   'runner_sha256':runner_sha,'cpu_test':args.cpu_test,
                   'config_name':args.config}
    env_path = run_dir/'piloto-entorno.json'
    if env_path.exists():
        previous = json.loads(env_path.read_text())
        if previous != environment:
            raise ValueError('Entorno/ejecutor distinto: no se reanuda este piloto')
    else:
        env_path.write_text(json.dumps(environment,indent=2)+'\n',encoding='utf-8')
    if args.stop_after_epoch is not None:
        if args.stop_after_epoch < 1:
            raise ValueError('La época de interrupción debe ser positiva')
        append = trainer._append_metrics
        def append_and_stop(record):
            append(record)
            if record['epoch'] >= args.stop_after_epoch:
                trainer.stop_path.touch()
        trainer._append_metrics = append_and_stop
    # Baseline sin red: misma representación, mismos pares de validación.
    baseline_path = run_dir/'baseline-entrada.json'
    if not baseline_path.exists():
        scores,psnr = [],[]
        for x,y in trainer.val_loader:
            for i in range(len(x)):
                xx,yy=x[i,0].numpy(),y[i,0].numpy()
                scores.append(compute_ssim(xx,yy))
                psnr.append(compute_psnr(yy,xx))
        baseline_path.write_text(json.dumps({'n':len(scores),'ssim_mean':float(np.mean(scores)),
            'psnr_mean':float(np.mean(psnr)),'manifest_sha256':MANIFEST_SHA,
            'normalization':trainer.config['normalization']},indent=2)+'\n',encoding='utf-8')
    if not args.cpu_test:
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()
    start=time.perf_counter()
    summary=trainer.train(resume=args.resume)
    if not args.cpu_test:
        torch.cuda.synchronize()
    result={'summary':summary,'elapsed_seconds':time.perf_counter()-start,
            'peak_cuda_allocated_bytes':torch.cuda.max_memory_allocated() if not args.cpu_test else None,
            'peak_cuda_reserved_bytes':torch.cuda.max_memory_reserved() if not args.cpu_test else None,
            'cpu_test':args.cpu_test}
    with (run_dir/'piloto-sesiones.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(result)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()

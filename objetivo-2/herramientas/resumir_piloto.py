"""Valida registros de los dos métodos; no abre datos reservados ni pesos."""
import argparse
import json
import math
from pathlib import Path


def check_run(root, stage, method, allow_cpu=False):
    run = root/f'oe2-v1-{stage}-f05-{method}-s2026100301'
    env=json.loads((run/'piloto-entorno.json').read_text())
    config=json.loads((run/'record/config.json').read_text())['config']
    summary=json.loads((run/'summary.json').read_text())
    rows=[json.loads(x) for x in (run/'metrics.jsonl').read_text().splitlines()]
    base=json.loads((run/'baseline-entrada.json').read_text())
    sessions=[json.loads(x) for x in (run/'piloto-sesiones.jsonl').read_text().splitlines()]
    expected_n=8 if stage=='tecnica' else 360
    checks={
        'gpu':bool(env['gpu']) and not env['cpu_test'],
        'completed':summary['stop_reason'] in ('epochs','early_stop'),
        'epochs_contiguous':[r['epoch'] for r in rows]==list(range(1,len(rows)+1)),
        'expected_epochs':len(rows)==2 if stage=='tecnica' else 1<=len(rows)<=30,
        'validation_size':all(r['val_n']==expected_n for r in rows) and base['n']==expected_n,
        'finite':all(r.get(k) is not None and math.isfinite(r[k]) for r in rows
                     for k in ('gp','l1','adv','grad_norm_g','grad_norm_d','val_ssim','val_psnr')),
        'baseline_finite':all(math.isfinite(base[k]) for k in ('ssim_mean','psnr_mean')),
        'checkpoints':all((run/'checkpoints'/name).is_file() for name in ('last.pt','best.pt')),
        'train_size':config.get('smoke_train_pairs')==8 if stage=='tecnica' else not config.get('smoke_train_pairs'),
        'resume_exercised':any(s['summary']['stop_reason']=='stop_file' for s in sessions) if stage=='tecnica' else True,
    }
    accepted=all(value for key,value in checks.items() if not (allow_cpu and key=='gpu'))
    epoch_seconds=[r['epoch_seconds'] for r in rows[1:]] or [r['epoch_seconds'] for r in rows]
    return {'method':method,'accepted':accepted,'checks':checks,
            'epochs':len(rows),'best_val_ssim':summary['best_val_ssim'],
            'input_val_ssim':base['ssim_mean'],
            'delta_ssim_vs_input':summary['best_val_ssim']-base['ssim_mean'],
            'mean_epoch_seconds_excluding_first_if_possible':sum(epoch_seconds)/len(epoch_seconds),
            'peak_cuda_reserved_bytes':max((s['peak_cuda_reserved_bytes'] or 0) for s in sessions),
            'manifest_sha256':config['data_manifest_sha256'],
            'implementation_sha256':config['implementation_sha256'],
            'normalization':config['normalization']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out-root',type=Path,required=True)
    p.add_argument('--stage',choices=['tecnica','piloto'],required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--allow-cpu-test',action='store_true')
    a=p.parse_args()
    results=[check_run(a.out_root,a.stage,m,a.allow_cpu_test) for m in ('unet','cgan')]
    paired=all(results[0][k]==results[1][k] for k in ('manifest_sha256','implementation_sha256','normalization'))
    report={'stage':a.stage,'technical_checks_passed':paired and all(r['accepted'] for r in results),
            'same_contract':paired,'local_cpu_check_only':a.allow_cpu_test,'runs':results,
            'quality_approved':False,
            'note':'La aceptación técnica no acredita calidad física ni autoriza la campaña de 24 entrenamientos.'}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(report,indent=2))
    if not report['technical_checks_passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()

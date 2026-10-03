"""Revisión independiente de registros/CSV; no ejecuta código de la entrega."""
import argparse
import csv
import hashlib
import json
import math
import sys
import subprocess
from pathlib import Path
import numpy as np

p=argparse.ArgumentParser()
p.add_argument('--entrega',type=Path,required=True)
p.add_argument('--datos',type=Path,required=True)
p.add_argument('--salida',type=Path,required=True)
p.add_argument('--git-ref',help='Verificar bytes de objetos Git sin conversión de finales de línea')
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
report={'sha256_ok':0,'sha256_mismatch':[],'runs':{},'checks':{},
        'weights_available':False,'model_inference_repeated':False,
        'archive_eol_differences':0,'git_ref':a.git_ref}
for line in (a.entrega/'huellas.sha256').read_text().splitlines():
    expected,name=line.split(maxsplit=1)
    name=name.lstrip('*')
    path=(a.entrega/name).resolve()
    assert path.is_relative_to(a.entrega.resolve())
    raw=path.read_bytes()
    if a.git_ref:
        obj=f'{a.git_ref}:objetivo-2/entregas/{a.entrega.name}/'+name.removeprefix('./')
        original=subprocess.run(['git','show',obj],capture_output=True,check=True).stdout
        if raw!=original:
            assert raw.replace(b'\r\n',b'\n')==original.replace(b'\r\n',b'\n')
            report['archive_eol_differences']+=1
        raw=original
    actual=hashlib.sha256(raw).hexdigest()
    if actual==expected:report['sha256_ok']+=1
    else:report['sha256_mismatch'].append(name)
results=a.entrega/'datos/resultados'
reference=json.loads((root/'evidencias/correcciones-v1.json').read_text())
for stage in ('tecnica','piloto'):
    for method in ('unet','cgan'):
        run=results/f'oe2-v1-{stage}-f05-{method}-s2026100301'
        cfg=json.loads((run/'record/config.json').read_text())
        expected=json.loads((root/'configuraciones/piloto-v1'/f'{stage}-{method}.json').read_text())
        assert all(cfg['config'][k]==v for k,v in expected.items())
        assert cfg['config']['implementation_sha256']==reference['implementation_sha256']
        assert cfg['config']['data_manifest_sha256']==reference['manifest_sha256']
        actual_config_hash=hashlib.sha256(json.dumps(cfg['config'],sort_keys=True).encode()).hexdigest()[:8]
        assert actual_config_hash==cfg['config_sha8']
        rows=[json.loads(x) for x in (run/'metrics.jsonl').read_text().splitlines()]
        assert (run/'metrics.jsonl').read_bytes()==(run/'record/metrics.jsonl').read_bytes()
        summary=json.loads((run/'summary.json').read_text())
        assert summary==json.loads((run/'record/summary.json').read_text())
        assert [r['epoch'] for r in rows]==list(range(1,len(rows)+1))
        iterations=2 if stage=='tecnica' else 360
        assert all(r['global_step']==r['epoch']*iterations and r['iterations']==iterations for r in rows)
        assert all(r['val_n']==(8 if stage=='tecnica' else 360) for r in rows)
        assert all(r[k] is not None and math.isfinite(r[k]) for r in rows for k in ('l1','gp','adv','val_ssim','val_psnr','grad_norm_g'))
        assert abs(rows[summary['best_epoch']-1]['val_ssim']-summary['best_val_ssim'])<=.00005
        env=json.loads((run/'piloto-entorno.json').read_text())
        assert env['gpu']=='NVIDIA L40S' and not env['cpu_test']
        assert env['runner_sha256']==hashlib.sha256((root/'herramientas/ejecutar_piloto.py').read_text(encoding='utf-8').encode()).hexdigest()
        sessions=[json.loads(x) for x in (run/'piloto-sesiones.jsonl').read_text().splitlines()]
        if stage=='tecnica':
            assert len(rows)==2 and len(sessions)==2
            assert sessions[0]['summary']['stop_reason']=='stop_file'
        else:
            assert summary['stop_reason']=='early_stop'
        report['runs'][stage+'-'+method]={'epochs':len(rows),'best_epoch':summary['best_epoch'],
            'best_ssim':summary['best_val_ssim'],'stop_reason':summary['stop_reason'],
            'seconds':sum(s['elapsed_seconds'] for s in sessions)}
report['checks']['four_runs_match_config_and_mirrors']=True
exits=list((a.entrega/'datos/logs').glob('*.exit_code.txt'))
assert all(x.read_text().strip()=='0' for x in exits)
report['checks']['exit_codes_zero']=len(exits)
rows=list(csv.DictReader((a.entrega/'datos/analisis-val/metricas-por-imagen-val.csv').open(newline='')))
assert len(rows)==360
expected_keys={(f'geo-val-{g:02d}',str(v),str(k)) for g in range(1,4) for v in range(6) for k in range(20)}
assert {(r['geometry'],r['view'],r['realization']) for r in rows}==expected_keys
published=json.loads((a.entrega/'datos/analisis-val/analisis-val.json').read_text())
clusters=[(r['geometry'],int(r['view'])) for r in rows]
keys=sorted(set(clusters))
rng=np.random.default_rng(20261003)
def verify_stat(values,stat):
    means=np.array([np.mean([v for v,c in zip(values,clusters) if c==k]) for k in keys])
    draws=rng.integers(0,18,size=(10000,18))
    ci=np.percentile(means[draws].mean(axis=1),[2.5,97.5])
    assert np.allclose(ci,stat['ci95'],rtol=0,atol=1e-12)
    assert abs(np.mean(values)-stat['mean'])<1e-12
    assert int((means>0).sum())==stat['clusters_positive']
for metric in ('ssim','psnr'):
    vals={n:np.array([float(r[f'{metric}_{n}']) for r in rows]) for n in ('input','unet','cgan')}
    for name,v in vals.items():verify_stat(v,published['means'][metric][name])
    for left,right in [('unet','input'),('cgan','input'),('cgan','unet')]:
        verify_stat(vals[left]-vals[right],published['paired_differences'][metric][left+'_minus_'+right])
    for gid in ('geo-val-01','geo-val-02','geo-val-03'):
        mask=np.array([r['geometry']==gid for r in rows])
        for n,v in vals.items():assert abs(v[mask].mean()-published['by_geometry'][gid][metric][n])<1e-12
report['checks']['csv_means_differences_geometry_and_bootstrap_reproduced']=True
# Recalcular únicamente baseline de entrada con los datos locales verificados.
sys.path.insert(0,str(root/'implementacion/scripts/training'))
sys.path.insert(0,str(root/'implementacion/scripts/evaluation'))
from muography_dataset import DataContract,MuographyPairs
from metrics import compute_ssim,compute_psnr
contract=DataContract(a.datos,root/'evidencias/contrato-datos-v1.json',reference['manifest_sha256'])
ds=MuographyPairs(contract,'val',.05)
max_error=0.
for i,row in enumerate(rows):
    assert int(row['i'])==i
    assert ds.index[i]==(row['geometry'],int(row['view']),int(row['realization']))
    x,y=ds[i]
    s=compute_ssim(x[0].numpy(),y[0].numpy())
    q=compute_psnr(y[0].numpy(),x[0].numpy())
    max_error=max(max_error,abs(s-float(row['ssim_input'])),abs(q-float(row['psnr_input'])))
assert max_error<1e-10
report['baseline_max_absolute_error']=max_error
report['checks']['baseline_360_recomputed']=True
report['means']={m:{n:published['means'][m][n]['mean'] for n in ('input','unet','cgan')} for m in ('ssim','psnr')}
report['status']='records_checked_weights_pending'
a.salida.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(report,indent=2))

"""Pruebas de contrato y entrenamiento real con interrupción al fin de época."""
import argparse
import gc
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import torch

p = argparse.ArgumentParser()
p.add_argument('--data-root',type=Path,required=True)
p.add_argument('--manifest',type=Path,required=True)
p.add_argument('--work',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a = p.parse_args()
base = Path(__file__).resolve().parents[1]/'implementacion'
sys.path.insert(0,str(base/'scripts/training'))
from muography_dataset import (DataContract,digest,normalize_input,normalize_counts,
                               inverse_counts,MuographyPairs)
from losses import gradient_penalty,critic_score
from engine import Trainer

torch.set_num_threads(2)
a.work.mkdir(parents=True,exist_ok=False)
checks = {}

def rejects(name, fn):
    try:
        fn()
    except (ValueError,RuntimeError):
        checks[name] = True
    else:
        raise AssertionError(f'No rechazó {name}')

class LinearPatches(torch.nn.Module):
    def __init__(self,side,norm):
        super().__init__()
        self.side,self.norm = side,norm
    def forward(self,cond,x):
        z = x.flatten(1).sum(1) * (self.norm / x[0].numel()**.5)
        return z[:,None,None,None].expand(-1,1,self.side,self.side)

for batch in (1,2):
    x = torch.zeros(batch,1,8,8)
    for side in (1,14,30):
        for norm in (1,2):
            gp = float(gradient_penalty(LinearPatches(side,norm),x,x,x).detach())
            assert np.isclose(gp,(norm-1)**2,atol=1e-6)
checks['gp_12_cases_batch_and_patch_invariant'] = True

manifest_sha = digest(a.manifest)
contract = DataContract(a.data_root,a.manifest,manifest_sha)
scale = contract.scale
values = np.array([0,1,100,4000,1000000],dtype=np.float64)
encoded = normalize_counts(values,scale)
assert np.all((encoded>=0)&(encoded<1))
assert np.allclose(inverse_counts(encoded,scale),values,rtol=1e-5,atol=1e-6)
assert np.isfinite(normalize_input(values*0,.01,scale)).all()
for f in (.5,.1,.05,.01):
    assert np.isfinite(normalize_input(values,f,scale)).all()
checks['normalization_roundtrip_zero_and_large_counts'] = True
pair = MuographyPairs(contract,'train',.05,limit=1)
x_before,y_before = pair[0]
gid = pair.index[0][0]
ref,low = pair.cache[gid]
pair.cache[gid] = (ref*2,low)
x_after,y_after = pair[0]
assert torch.equal(x_before,x_after) and not torch.equal(y_before,y_after)
checks['input_independent_of_target_in_dataset'] = True
del pair
rejects('fraction_zero',lambda:normalize_input(values,0,scale))
rejects('fraction_nan',lambda:normalize_input(values,float('nan'),scale))
rejects('negative_counts',lambda:normalize_counts(-values,scale))
rejects('inverse_one_no_silent_clipping',lambda:inverse_counts([1],scale))
rejects('wrong_manifest_hash',lambda:DataContract(a.data_root,a.manifest,'0'*64))
rejects('heldout_not_available',lambda:MuographyPairs(contract,'test',.05))
# Copia mínima independiente para probar alteración de archivos sin tocar fuentes.
changed = a.work/'changed-data'
changed.mkdir()
(changed/'one.txt').write_text('antes')
mini = {'contract':'oe2-v1','normalization':{'scale':scale},
        'files':{'one.txt':digest(changed/'one.txt')}}
mini_path = a.work/'mini.json'
mini_path.write_text(json.dumps(mini))
(changed/'one.txt').write_text('después')
rejects('changed_data_rejected',lambda:DataContract(changed,mini_path,digest(mini_path)))

config = json.loads((base/'scripts/training/configs/smoke_v1.json').read_text())
config.update(data_root=str(a.data_root),data_manifest=str(a.manifest),
              data_manifest_sha256=manifest_sha)
def state_hash(state):
    h = hashlib.sha256()
    for key,value in sorted(state.items()):
        h.update(key.encode())
        h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()

continuous = Trainer(config,a.work/'continuous')
initial = state_hash(continuous.generator.state_dict())
summary_full = continuous.train(resume='none')
expected_g = state_hash(continuous.generator.state_dict())
expected_d = state_hash(continuous.critic.state_dict())
assert initial != expected_g and continuous.global_step == 2
implementation_sha = continuous.code_identity
del continuous
gc.collect()

interrupted = Trainer(config,a.work/'resumed')
original_step = interrupted.train_step
def stop_after_step(*args,**kwargs):
    result = original_step(*args,**kwargs)
    interrupted.stop_path.touch()
    return result
interrupted.train_step = stop_after_step
summary_first = interrupted.train(resume='none')
assert summary_first['last_epoch'] == 1 and summary_first['stop_reason'] == 'stop_file'
del interrupted, original_step
gc.collect()

resumed = Trainer(config,a.work/'resumed')
summary_resume = resumed.train(resume='auto')
assert resumed.global_step == 2
assert state_hash(resumed.generator.state_dict()) == expected_g
assert state_hash(resumed.critic.state_dict()) == expected_d
checks['full_architecture_two_updates_and_exact_resume'] = True
for checkpoint in ('last.pt','best.pt'):
    assert (a.work/'resumed/checkpoints'/checkpoint).exists()
checks['last_and_best_checkpoints_written'] = True
legacy = a.work/'legacy.pt'
torch.save({'epoch':1},legacy)
rejects('legacy_checkpoint_rejected',lambda:resumed.load_checkpoint(legacy))
resumed.code_identity = 'changed-code'
rejects('changed_code_checkpoint_rejected',lambda:resumed.load_checkpoint(a.work/'resumed/checkpoints/last.pt'))
resumed.code_identity = implementation_sha
resumed.data_contract.identity = 'changed-dataset'
rejects('changed_dataset_checkpoint_rejected',lambda:resumed.load_checkpoint(a.work/'resumed/checkpoints/last.pt'))
resumed.data_contract.identity = manifest_sha
original_scale = resumed.data_contract.manifest['normalization']['scale']
resumed.data_contract.manifest['normalization']['scale'] = original_scale+1
rejects('changed_normalization_checkpoint_rejected',lambda:resumed.load_checkpoint(a.work/'resumed/checkpoints/last.pt'))
resumed.data_contract.manifest['normalization']['scale'] = original_scale
logs = {}
for name in ('continuous','resumed'):
    logs[name] = [json.loads(line) for line in (a.work/name/'metrics.jsonl').read_text().splitlines()]
    assert len(logs[name]) == 2
    for row in logs[name]:
        for key in ('gp','l1','adv','grad_norm_g','grad_norm_d','val_ssim'):
            assert row[key] is not None and np.isfinite(row[key])
checks['finite_training_and_validation_metrics'] = True
result = {'status':'passed','checks':checks,'python':platform.python_version(),
          'torch':torch.__version__,'numpy':np.__version__,'device':'cpu','threads':2,
          'manifest_sha256':manifest_sha,'implementation_sha256':implementation_sha,
          'normalization':contract.manifest['normalization'],
          'generator_state_sha256':expected_g,'critic_state_sha256':expected_d,
          'continuous':summary_full,'interrupted':summary_first,'resumed':summary_resume,
          'metrics':logs,'heldout_images_opened':False,
          'scope':'Prueba técnica de dos pasos, no evaluación de calidad'}
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':'passed','checks':len(checks)}))

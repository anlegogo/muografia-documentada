"""Diagnóstico reproducible; no entrena ni abre imágenes test/generalization."""
import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import torch

p = argparse.ArgumentParser()
p.add_argument('--codigo', type=Path, required=True)
p.add_argument('--datos', type=Path, required=True)
p.add_argument('--salida', type=Path, required=True)
a = p.parse_args()
sys.path[:0] = [str(a.codigo.resolve()), str((a.codigo/'scripts/training').resolve())]
import muography_dataset as md
from losses import gradient_penalty
from models import build_generator, build_critic

torch.set_num_threads(2)
torch.manual_seed(20261003)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
r = {'python': platform.python_version(), 'torch': torch.__version__,
     'numpy': np.__version__, 'device': 'cpu', 'seed': 20261003,
     'source_sha256': {}, 'shards': [], 'heldout_images_opened': False}
for name in ['scripts/training/muography_dataset.py', 'scripts/training/losses.py',
             'scripts/training/engine.py', 'scripts/training/configs/e17_final.json',
             'models/unet_generator.py', 'models/patch_critic.py']:
    r['source_sha256'][name] = sha(a.codigo/name)
splits_path = a.datos/'dataset-v2/splits.json'
splits = json.loads(splits_path.read_text())
r['splits_sha256'] = sha(splits_path)
groups = list(splits['splits'].values())
assert len(set(sum(groups, []))) == sum(map(len, groups))
for gid in splits['splits']['train'] + splits['splits']['val']:
    path = a.datos/'dataset-v2/shards'/f'{gid}.npz'
    meta = json.loads(path.with_suffix('.meta.json').read_text())
    with np.load(path, allow_pickle=False) as z:
        ref, low = z['ref_counts'], z['low_counts']
        assert ref.shape == (6,256,256) and low.shape == (6,4,20,256,256)
        assert ref.dtype == np.uint32 and low.dtype == np.uint16
        assert np.allclose(z['fractions'], [.5,.1,.05,.01], rtol=0, atol=1e-8)
        for source in meta['source_views']:
            vi = source['view']
            with np.load(a.datos/'pares'/source['pairs_file'], allow_pickle=False) as q:
                assert np.array_equal(ref[vi], q['counts_ref'])
                assert np.array_equal(low[vi], q['low_counts'])
        r['shards'].append({'geometry':gid, 'sha256':sha(path),
                           'views_equal_to_source':6, 'pairs':480,
                           'ref_max':int(ref.max()), 'low_max':int(low.max())})
# Redirección exclusivamente en memoria para el diagnóstico: el código original
# continúa apuntando a sus rutas históricas y no se modifica.
md.SHARD_DIR = a.datos/'dataset-v2/shards'
md.SPLITS_PATH = splits_path
ds = md.MuographyPairs(geometry_ids=['geo-train-01'], fractions=[.05],
                      input_scaling='ref_equivalent')
x,y = ds[0]
assert torch.isfinite(x).all() and torch.isfinite(y).all()
g,d = build_generator('unet_dc_5').eval(), build_critic('patch_critic_70').eval()
with torch.no_grad():
    output = g(x.unsqueeze(0))
    scores = d(x.unsqueeze(0), output)
assert output.shape == (1,1,256,256) and scores.shape == (1,1,30,30)
assert torch.isfinite(output).all() and torch.isfinite(scores).all()
r['forward'] = {'geometry':'geo-train-01', 'fraction':.05, 'sample':0,
                'random_weights':True, 'generator_shape':list(output.shape),
                'critic_shape':list(scores.shape), 'finite':True,
                'generator_parameters':sum(t.numel() for t in g.parameters())}

class UnitGradientPatchCritic(torch.nn.Module):
    def __init__(self, patches):
        super().__init__()
        self.patches = patches
    def forward(self, cond, image):
        scalar = image.flatten(1).sum(1) / image[0].numel()**.5
        return scalar[:,None,None,None].expand(-1,1,self.patches,self.patches)

r['gradient_penalty'] = []
t = torch.zeros(1,1,8,8)
for side in [1,14,30]:
    critic = UnitGradientPatchCritic(side)
    observed = float(gradient_penalty(critic,t,t,t).detach())
    probe = t.clone().requires_grad_(True)
    score_mean = critic(t,probe).flatten(1).mean(1)
    grad = torch.autograd.grad(score_mean.sum(),probe)[0]
    mean_gp = float(((grad.flatten(1).norm(dim=1)-1)**2).mean())
    assert np.isclose(observed, (side*side-1)**2, rtol=1e-5, atol=1e-8)
    assert abs(mean_gp) < 1e-8
    r['gradient_penalty'].append({'patch_side':side,'published_gp':observed,
                                 'gp_for_mean_score':mean_gp})
low = np.ones((8,8),dtype=np.uint32)
v1,_ = md.preprocess_pair_corrected(low,low*100,.05)
v2,_ = md.preprocess_pair_corrected(low,low*200,.05)
r['normalization'] = {'same_low_different_reference_changes_input':bool(np.any(v1!=v2))}
with np.errstate(divide='ignore',invalid='ignore'):
    empty,_ = md.preprocess_pair_corrected(low*0,low*0,.05)
r['normalization']['empty_reference_is_finite'] = bool(np.isfinite(empty).all())
r['status'] = 'diagnostic_completed_with_findings'
a.salida.parent.mkdir(parents=True,exist_ok=True)
a.salida.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':r['status'],'shards':len(r['shards']),
                  'pairs_compared':sum(s['pairs'] for s in r['shards']),
                  'forward':r['forward'], 'gradient_penalty':r['gradient_penalty'],
                  'normalization':r['normalization']},indent=2))

"""Locate why a resumed cGAN technical run differs from the continuous one on CUDA.

Uses the director's runner functions unchanged (ejecutar_ajuste_cgan.py) and
runs the two-epoch technical stage of one arm several ways inside ONE process:

  continua    epoch 1 -> epoch 2 with the same objects (reference)
  recarga     epoch 1 -> serialize state as the runner does (torch.save of
              G, D, both Adam states and RNG) -> fresh objects built exactly
              as on resume -> load -> epoch 2
  solo_rng    epoch 1 -> restore only the saved RNG state -> epoch 2
  solo_opt    epoch 1 -> reload only both optimizer states into the same
              optimizers -> epoch 2
  solo_redes  epoch 1 -> reload only G and D state dicts -> epoch 2

and prints the generator/critic digests after epoch 2 next to the digests
recorded by the real continuous and recovered runs. Nothing is written in the
run directories. Run from the repository root:
  python diagnosticar_reanudacion_cgan.py --rama C0 --datos D --mascaras M \
      --pesos cgan-best.pt --tecnica SALIDAS/tecnica --salida diag.json
"""
import argparse
import io
import json
import os
import sys
from pathlib import Path

os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
sys.path.insert(0, str(Path('objetivo-2/herramientas').resolve()))
import torch  # noqa: E402
from ejecutar_ajuste_cgan import (Store, build, configure, evaluate, identity, load_initial,  # noqa: E402
                                  restore_rng, rng_state, seed_all, spec, state_digest, train_step)


def run_epoch(G, D, og, od, train, val, store, cfg, device, epoch):
    G.train()
    D.train()
    order = torch.randperm(len(train), generator=torch.Generator().manual_seed(cfg['seed']+epoch)).tolist()
    for pos in range(0, len(order), cfg['batch']):
        rr = [train[k] for k in order[pos:pos+cfg['batch']]]
        train_step(G, D, og, od, store.batch(rr, device), store, cfg)
    evaluate(G, store, val, device)
    if device.type == 'cuda':
        torch.cuda.synchronize()


def serialize(G, D, og, od, device):
    buf = io.BytesIO()
    torch.save({'generator': G.state_dict(), 'critic': D.state_dict(), 'opt_g': og.state_dict(),
                'opt_d': od.state_dict(), 'rng': rng_state(device)}, buf)
    buf.seek(0)
    return torch.load(buf, map_location='cpu', weights_only=True)


def digests(G, D):
    return {'generator': state_digest(G.state_dict()), 'critic': state_digest(D.state_dict())}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rama', choices=['C0', 'C1'], required=True)
    for n in ['datos', 'mascaras', 'pesos', 'tecnica', 'salida']:
        p.add_argument('--'+n, type=Path, required=True)
    a = p.parse_args()
    configure()
    device = torch.device('cuda:0')
    cfg = spec(a.rama)
    store = Store(a.datos, a.mascaras)
    initial = load_initial(a.pesos, cfg, store)
    _, train, val = identity(cfg, a.rama, 'tecnica', store, device, initial)

    def fresh():
        seed_all(cfg['seed'])
        return build(cfg, initial, device)

    results = {}
    for mode in ['continua', 'recarga', 'solo_rng', 'solo_opt', 'solo_redes']:
        G, D, og, od = fresh()
        run_epoch(G, D, og, od, train, val, store, cfg, device, 1)
        c = serialize(G, D, og, od, device)
        if mode == 'recarga':
            G, D, og, od = fresh()
            G.load_state_dict(c['generator'], strict=True)
            D.load_state_dict(c['critic'], strict=True)
            og.load_state_dict(c['opt_g'])
            od.load_state_dict(c['opt_d'])
            restore_rng(c['rng'], device)
        elif mode == 'solo_rng':
            restore_rng(c['rng'], device)
        elif mode == 'solo_opt':
            og.load_state_dict(c['opt_g'])
            od.load_state_dict(c['opt_d'])
        elif mode == 'solo_redes':
            G.load_state_dict(c['generator'], strict=True)
            D.load_state_dict(c['critic'], strict=True)
        run_epoch(G, D, og, od, train, val, store, cfg, device, 2)
        results[mode] = digests(G, D)
        print(mode, results[mode], flush=True)
    recorded = {}
    for kind in ['continua', 'recuperada']:
        h = json.loads((a.tecnica/f'{a.rama}-{kind}'/'history.json').read_text())[-1]
        recorded[kind] = {'generator': h['generator_sha256'], 'critic': h['critic_sha256']}
    report = {'arm': a.rama, 'in_process': results, 'recorded_runs': recorded,
              'matches': {m: {k: r == recorded[k] for k in recorded} for m, r in results.items()}}
    a.salida.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report['matches'], indent=1))


if __name__ == '__main__':
    main()

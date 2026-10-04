"""Corrección numérica posterior a EF-01; conserva predicciones y protocolo original."""
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np

TIE_TOLERANCE_M = 1e-8

def array_hash(a):
    return hashlib.sha256(np.asarray(a, dtype='<i8').tobytes()).hexdigest()

def stable_match(mask, control, lengths, cfg, tolerance=TIE_TOLERANCE_M):
    """Misma elegibilidad; grupos anclados al mínimo y desempate por columna."""
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError('Tolerancia inválida')
    targets, donors = [], []
    for y, x in zip(*np.where(mask)):
        candidates = np.flatnonzero(control[y])
        distances = np.abs(lengths[y, candidates] - lengths[y, x])
        eligible = distances / lengths[y, x] <= cfg['control_cone_length_relative_tolerance']
        candidates, distances = candidates[eligible], distances[eligible]
        order = np.argsort(distances, kind='stable')
        ranked = []
        i = 0
        while i < len(order) and len(ranked) < cfg['control_donors_per_pixel']:
            j = i + 1
            anchor = distances[order[i]]
            while j < len(order) and distances[order[j]] - anchor <= tolerance:
                j += 1
            ranked.extend(sorted(candidates[order[i:j]].tolist()))
            i = j
        selected = ranked[:cfg['control_donors_per_pixel']]
        if len(selected) == cfg['control_donors_per_pixel']:
            targets.append(int(y * mask.shape[1] + x))
            donors.append([int(y * mask.shape[1] + c) for c in selected])
    return np.asarray(targets, dtype=np.int64), np.asarray(donors, dtype=np.int64).reshape(-1, cfg['control_donors_per_pixel'])

class Registry:
    def __init__(self, signature, replay=None):
        self.signature = signature
        self.entries = []
        self.replay = replay
        if replay is not None:
            if replay['protocol_sha256'] != signature or replay['correction_sha256'] != hashlib.sha256(Path(__file__).read_bytes()).hexdigest():
                raise ValueError('Registro de otro protocolo o corrector')
    def __call__(self, mask, control, lengths, cfg):
        context = {'mask_sha256':array_hash(mask), 'control_sha256':array_hash(control),
                   'shape':list(mask.shape), 'donors_per_pixel':cfg['control_donors_per_pixel']}
        if self.replay is None:
            t, d = stable_match(mask, control, lengths, cfg)
            # Sondeos de geometría, sin seleccionar por métricas de imagen.
            checks = []
            for tol in [1e-9, 1e-7]:
                tt, dd = stable_match(mask, control, lengths, cfg, tol)
                checks.append({'test':'tolerance', 'value':tol, 'same_indices':bool(np.array_equal(t,tt) and np.array_equal(d,dd))})
            rng = np.random.default_rng(20261004 + len(self.entries))
            perturb = lengths + rng.uniform(-1e-10,1e-10,lengths.shape)
            tt, dd = stable_match(mask,control,perturb,cfg)
            checks.append({'test':'length_perturbation_m','value':1e-10,'same_indices':bool(np.array_equal(t,tt) and np.array_equal(d,dd))})
            item = {**context,'targets':t.tolist(),'donors':d.tolist(),'indices_sha256':array_hash(np.concatenate([t.ravel(),d.ravel()])), 'sensitivity':checks}
        else:
            if len(self.entries)>=len(self.replay['entries']):raise ValueError('Registro insuficiente')
            item = self.replay['entries'][len(self.entries)]
            if any(item[k]!=v for k,v in context.items()):raise ValueError('Máscaras o configuración distintas')
            t=np.asarray(item['targets'],dtype=np.int64);d=np.asarray(item['donors'],dtype=np.int64).reshape(-1,cfg['control_donors_per_pixel'])
            if array_hash(np.concatenate([t.ravel(),d.ravel()]))!=item['indices_sha256']:raise ValueError('Índices alterados')
            if len(t)!=len(d) or np.any(t<0) or np.any(t>=mask.size) or np.any(d<0) or np.any(d>=mask.size):raise ValueError('Índices inválidos')
            if not np.all(mask.ravel()[t]) or not np.all(control.ravel()[d]):raise ValueError('Soporte incompatible')
        self.entries.append(item)
        return t,d

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['repo','data','weights','predictions','report']:
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--registry-in',type=Path)
    a=p.parse_args()
    sys.path.insert(0,str(a.repo/'objetivo-2/herramientas'))
    sys.path.insert(0,str(a.repo/'objetivo-2/implementacion/scripts/evaluation'))
    import evaluacion_final_oe2 as e
    import evaluar_regiones_geometricas as g
    spec,signature=e.contract(a.repo)
    registry=Registry(signature,e.read(a.registry_in) if a.registry_in else None)
    original=g.match_controls
    g.match_controls=registry
    from types import SimpleNamespace
    try:
        e.evaluate(SimpleNamespace(repo=a.repo,data=a.data,weights=a.weights,output=a.predictions,report=a.report),spec,signature)
    finally:
        g.match_controls=original
    if registry.replay is not None and len(registry.entries)!=len(registry.replay['entries']):raise ValueError('Registro con entradas sobrantes')
    record={'revision':'EF-01-C2','post_hoc_numerical_correction':True,'protocol_sha256':signature,'correction_sha256':e.sha(__file__),'tie_tolerance_m':TIE_TOLERANCE_M,'ordering':'geometry_order, view ascending, anomaly order; tie by column','entries':registry.entries}
    e.write(a.report/'controles.json',record)
    report=e.read(a.report/'evaluacion-final.json')
    report['numerical_correction']={k:v for k,v in record.items() if k!='entries'}
    report['numerical_correction']['registry_sha256']=e.sha(a.report/'controles.json')
    e.write(a.report/'evaluacion-final.json',report)
    # Inventario nuevo: evaluate inventarió antes de agregar la revisión.
    e.write(a.report/'inventario-revision.json',[{'path':x.name,'sha256':e.sha(x),'bytes':x.stat().st_size} for x in sorted(a.report.iterdir()) if x.is_file() and x.name!='inventario-revision.json'])
    print(json.dumps({'registry_entries':len(registry.entries),'sensitivity_failures':sum(not c['same_indices'] for x in registry.entries for c in x['sensitivity'])}),flush=True)

if __name__=='__main__':main()

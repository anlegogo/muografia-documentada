"""Auditoría independiente de la entrega B1-B3 E1, sin entrenar ni abrir reservas."""
import argparse,copy,hashlib,json,math,sys,time
from pathlib import Path
import numpy as np
import torch
import ejecutar_borde_cgan as e
import revisar_borde_cgan as audit
from evaluar_borde_cgan import tables
from resumir_borde_cgan import summarize
from datos_ajuste import Store,digest,read_json,atomic_json
from types import SimpleNamespace


p=argparse.ArgumentParser(description=__doc__)
for name in ['entrega','binarios','datos','pesos','salida','mascaras-referencia']:
    p.add_argument('--'+name,type=Path,required=True)
ARGS=p.parse_args()
ROOT=ARGS.salida;ROOT.mkdir(parents=True,exist_ok=False)
TEXT=ARGS.entrega/'datos/ensayo-borde-e1';BIN=ARGS.binarios
DATA=ARGS.datos;WEIGHTS=ARGS.pesos
e.configure()
hashes={line[66:].strip():line[:64] for line in (ARGS.entrega/'datos/binarios.sha256').read_text(encoding='utf-8').splitlines() if line.strip()}
sizes={line.split(maxsplit=1)[1]:int(line.split(maxsplit=1)[0]) for line in (ARGS.entrega/'datos/binarios.tamanos.txt').read_text(encoding='utf-8').splitlines() if line.strip()}
assert set(hashes)==set(sizes) and len(hashes)==55
expected=[{'path':name,'sha256':h,'bytes':sizes[name]} for name,h in hashes.items()]
by_path={x['path']:x for x in expected}
def wait(p):
    deadline=time.monotonic()+900
    while not p.is_file() and time.monotonic()<deadline:time.sleep(2)
    if not p.is_file():raise FileNotFoundError('Falta un archivo de la entrega: '+str(p))
def match_file(p,relative):
    item=by_path[relative]
    assert p.stat().st_size==item['bytes'] and digest(p)==item['sha256'],relative
def save(result):atomic_json(ROOT/'revision-independiente.json',result)
def compare(x,y,differences,path=''):
    if isinstance(x,dict):
        assert set(x)==set(y),path
        for k in x:compare(x[k],y[k],differences,path+'/'+k)
    elif isinstance(x,list):
        assert len(x)==len(y),path
        for j,(a,b) in enumerate(zip(x,y)):compare(a,b,differences,path+'/'+str(j))
    elif isinstance(x,float):
        assert math.isclose(x,y,rel_tol=1e-12,abs_tol=1e-12),(path,x,y)
        differences.append(abs(x-y))
    else:assert x==y,(path,x,y)

def main():
    result={'schema':'oe2-edge-independent-review-v1','review_date':'2026-10-04','delivery_commit':'804ce85f1bcb1e00d0956ae6bef26e69dd50130a','runtime_commit':'156d4f5699f500c692d466f56c48ca25bda79c0c','complete':False,'gpu_execution_repeated_locally':False,'training_performed':False,'heldout_opened':False,'physical_acceptance':False,'technical_recovery':{},'evaluation':{},'inference':{},'tradeoff':{}}
    for p in TEXT.rglob('*.json'):
        rel=p.relative_to(TEXT)
        if 'piloto' in rel.parts or 'tecnica' in rel.parts:
            dest=BIN/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
    for pair in e.PAIR_SEEDS:
        paths={a+'-'+m:BIN/pair/'tecnica'/(a+'-'+m) for a in ['C0','C1'] for m in ['continua','recuperada']}
        print('Esperando checkpoints tecnicos '+pair,flush=True)
        for folder in paths.values():
            for name in ['last.pt','predicciones-val.npy']:wait(folder/name);match_file(folder/name,str((folder/name).relative_to(BIN)).replace('\\','/'))
        gate=audit.audit_technical(paths,require_gpu=True,pair=pair);declared=read_json(TEXT/pair/'aceptacion-gpu.json')
        assert gate['checkpoint_sha256']==declared['checkpoint_sha256'] and gate['identities']==declared['identities']
        result['technical_recovery'][pair]={'exact_recovery':gate['exact_recovery'],'gpu_artifacts_verified':gate['gpu_accepted'],'checkpoint_sha256':gate['checkpoint_sha256'],'seed':gate['seed']}
        save(result);print('Recuperacion exacta verificada '+pair,flush=True)
    for item in expected:wait(BIN/item['path']);match_file(BIN/item['path'],item['path'])
    result['integrity']={'files':len(expected),'bytes':sum(x['bytes'] for x in expected),'all_sha256_and_sizes_match':True,'manifest':expected}
    store=Store(DATA,BIN/'mascaras-ajuste-v1')
    reference_masks=read_json(ARGS.mascaras_referencia/'manifest.json')
    local=copy.deepcopy(store.manifest);reference=copy.deepcopy(reference_masks)
    for manifest in (local,reference):
        for info in manifest['geometries'].values():info.pop('mask_sha256')
    assert local==reference,'Contenido semantico del manifiesto de mascaras distinto'
    for gid,info in reference_masks['geometries'].items():
        with np.load(ARGS.mascaras_referencia/info['mask_file'],allow_pickle=False) as z:a=z['masks']
        with np.load(BIN/'mascaras-ajuste-v1'/info['mask_file'],allow_pickle=False) as z:b=z['masks']
        assert np.array_equal(a,b),gid
    result['masks_verified']={'geometries':len(reference_masks['geometries']),'arrays_equal_to_previous_verified_cache':True,'compressed_file_identity_separately_verified':True}
    original=e.load_initial(WEIGHTS,e.spec('C0','B1'),store)
    initial_hashes={'initial_generator_sha256':e.state_digest(original[0]),'initial_critic_sha256':e.state_digest(original[1])}
    result['sources']=e.sources();result['local_environment']=e.environment(torch.device('cpu'))
    result['cache_sha256']=store.identity;result['initial_checkpoint_sha256']=digest(WEIGHTS)
    result['inference_tolerances']={'pixel_max_abs':1e-4,'ssim':1e-5,'psnr_db':1e-3,'scope':'CPU versus CUDA inference only; technical recovery requires exact equality.'}
    reports={};initial_cpu=None;initial_metrics=None
    for pair in e.PAIR_SEEDS:
        print('Evaluacion e inferencia '+pair,flush=True)
        keys=[list(x) for x in store.indices('val',e.spec('C0',pair),'piloto')]
        states={a:audit.load_completed(BIN/pair/'piloto'/a,a,'piloto',pair) for a in ['C0','C1']}
        gate=read_json(TEXT/pair/'aceptacion-gpu.json');declared=read_json(TEXT/pair/'evaluacion/comparacion-cgan.json')
        for arm,c in states.items():
            assert c['identity']['cache_sha256']==store.identity
            for k in ['sources','environment','initial_checkpoint_sha256','data_manifest_sha256']:
                assert c['identity'][k]==gate['identities'][0][k]
            for k,v in initial_hashes.items():assert c['identity'][k]==v
            assert read_json(BIN/pair/'piloto'/arm/'indices-val.json')==keys
            assert digest(BIN/pair/'piloto'/arm/'last.pt')==declared['checkpoint_sha256'][arm]
        initial=np.load(BIN/pair/'evaluacion/predicciones-cgan-inicial.npy',allow_pickle=False)
        assert digest(BIN/pair/'evaluacion/predicciones-cgan-inicial.npy')==declared['initial_predictions_sha256']
        pred={a:np.load(BIN/pair/'piloto'/a/'predicciones-val.npy',allow_pickle=False) for a in states}
        calc,rows=tables(store,keys,pred,initial,'piloto');diffs=[]
        for k,v in calc.items():compare(v,declared[k],diffs,k)
        compare(rows,read_json(TEXT/pair/'evaluacion/anomalias-cgan.json')['rows'],diffs,'anomalies')
        result['evaluation'][pair]={'float_fields':len(diffs),'max_abs_difference':max(diffs),'summary':calc['summary'],'decision_checks':calc['decision_checks'],'decision':calc['decision'],'anomaly_diagnostics':calc['anomaly_diagnostics']}
        reports[pair]=declared
        for arm,weights in [('C0',states['C0']['generator']),('C1',states['C1']['generator']),('inicial_cgan',original[0])]:
            reference=initial if arm=='inicial_cgan' else pred[arm]
            if arm=='inicial_cgan' and initial_cpu is not None:z=initial_cpu;metrics=initial_metrics;reused=True
            else:
                G=e.build_generator(e.spec('C0',pair)['generator']);G.load_state_dict(weights,strict=True)
                metrics,z,_=e.evaluate(G,store,keys,torch.device('cpu'));del G;reused=False
                if arm=='inicial_cgan':initial_cpu=z;initial_metrics=metrics
                np.save(ROOT/('cpu-'+pair+'-'+arm+'.npy'),z)
            delta=np.abs(z.astype(np.float64)-reference.astype(np.float64))
            item={'images':len(z),'reused_identical_initial_inference':reused,'pixel_max_abs':float(delta.max()),'pixel_mean_abs':float(delta.mean()),'ssim_difference':abs(metrics['ssim']-calc['summary'][arm]['ssim']),'psnr_difference':abs(metrics['psnr']-calc['summary'][arm]['psnr']),'metrics_cpu':metrics}
            assert item['pixel_max_abs']<=1e-4 and item['ssim_difference']<=1e-5 and item['psnr_difference']<=1e-3,item
            result['inference'][pair+'/'+arm]=item;save(result);print(json.dumps({'inference':pair+'/'+arm,**item}),flush=True)
            del delta
        save(result);del states,pred
    synthesis=summarize(reports,'piloto');declared_summary=read_json(TEXT/'sintesis-borde.json');diffs=[]
    for k,v in synthesis.items():compare(v,declared_summary[k],diffs,k)
    for pair in e.PAIR_SEEDS:assert digest(TEXT/pair/'evaluacion/comparacion-cgan.json')==declared_summary['evaluation_sha256'][pair]
    result['synthesis']=synthesis;result['synthesis_float_fields']=len(diffs)
    result['inference_images_computed']=sum(v['images'] for v in result['inference'].values() if not v['reused_identical_initial_inference'])
    result['complete']=True;save(result);print('AUDITORIA COMPLETA',flush=True)

if __name__=='__main__':main()


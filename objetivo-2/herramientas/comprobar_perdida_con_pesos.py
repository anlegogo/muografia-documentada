"""Paso por red y retropropagación en dos pares train; sin optimizador."""
import argparse,json,sys,io,hashlib
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
for n in ('datos','pesos','salida'):p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--repo',type=Path,default=Path('.'))
p.add_argument('--insumos',type=Path,help='Opcional: copias verificadas de los cinco JSON de entrada')
p.add_argument('--modulos',type=Path,help='Opcional: directorio de unet_generator.py')
p.add_argument('--torch-dir',type=Path)
a=p.parse_args()
if a.torch_dir:sys.path.insert(0,str(a.torch_dir))
sys.path.insert(0,str(a.modulos or a.repo/'objetivo-2/implementacion/models'))
import numpy as np
import torch
from unet_generator import build_generator
from evaluar_regiones_geometricas import rays,masks
from perdida_cuentas_regionales import combined_loss
torch.set_num_threads(2);torch.use_deterministic_algorithms(True);torch.manual_seed(2026100302)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=a.insumos/'contrato-datos-v1.json' if a.insumos else a.repo/'objetivo-2/evidencias/contrato-datos-v1.json'
recipe_path=a.insumos/'receta.json' if a.insumos else a.repo/'objetivo-1/contratos/receta-operativa-siete-actividades.json'
protocol=a.insumos/'protocolo-regiones-v1.json' if a.insumos else a.repo/'objetivo-2/configuraciones/protocolo-regiones-v1.json'
contract=json.loads(manifest.read_text(encoding='utf-8'));recipe=json.loads(recipe_path.read_text(encoding='utf-8'))
cfg=json.loads(protocol.read_text(encoding='utf-8'));S=contract['normalization']['scale']
gp=a.insumos/'geo-train-06.json' if a.insumos else a.repo/'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries/geo-train-06.json'
assert sha(gp)==recipe['geometry_sha256'][gp.name]
g=json.loads(gp.read_text(encoding='utf-8'));sp=a.datos/'dataset-v2/shards/geo-train-06.npz'
assert sha(sp)==contract['files']['dataset-v2/shards/geo-train-06.npz']
assert sha(a.pesos)=='734bc5dc1aa4cdc16a3fa0b6de2d58da7575c5bd0b1fe342bc266283f0e8e57a'
with np.load(sp) as z:
    counts=z['ref_counts'][0].astype(float)
    low=z['low_counts'][0,2,:2].astype(float);assert z['fractions'][2]==.05
    o,d=rays(z['az_centers_deg'],z['el_centers_deg'],0,cfg)
    _,_,regions=masks(g,o,d,cfg)
names=list(regions);families=[0 if k=='cielo' else 1 if k=='roca_sin_anomalia' else 2 if k=='borde_cono' else 3 for k in names]
mm=torch.from_numpy(np.stack([regions[k] for k in names])).unsqueeze(0).expand(2,-1,-1,-1)
def T(c):
    v=np.log1p(c);return (v/(S+v)).astype(np.float32)
x=torch.from_numpy(T(low/.05))[:,None];ref=torch.from_numpy(counts).unsqueeze(0).unsqueeze(0).expand(2,-1,-1,-1)
target=torch.from_numpy(T(counts)).unsqueeze(0).unsqueeze(0).expand(2,-1,-1,-1)
safe=[np._core.multiarray._reconstruct,np.ndarray,np.dtype,np.dtypes.UInt32DType]
with torch.serialization.safe_globals(safe):ckpt=torch.load(io.BytesIO(a.pesos.read_bytes()),map_location='cpu',weights_only=True)
assert ckpt['data_manifest_sha256']==sha(manifest)
assert ckpt['normalization']==contract['normalization'] and ckpt['epoch']==5
net=build_generator('unet_dc_5').eval();net.load_state_dict(ckpt['generator'],strict=True)
out=net(x);loss,parts=combined_loss(out,target,ref,mm,families,S,weight=1)
parts['regional'].backward(retain_graph=True)
regional_norm2=0.
for param in net.parameters():
    assert param.grad is not None and torch.isfinite(param.grad).all()
    regional_norm2+=float(param.grad.double().square().sum())
assert regional_norm2>0
net.zero_grad(set_to_none=True)
loss.backward()
norm2=0.;parameter_count=0
for param in net.parameters():
    assert param.grad is not None and torch.isfinite(param.grad).all()
    norm2+=float(param.grad.double().square().sum());parameter_count+=param.numel()
assert all(torch.equal(net.state_dict()[k],v) for k,v in ckpt['generator'].items())
result={'schema':'oe2-adjustment-real-data-gradient-v1','device':'cpu','torch':torch.__version__,'numpy':np.__version__,'split':'train','geometry':'geo-train-06','view':0,'realizations':[0,1],'model_mode':'eval_with_gradients','optimizer_steps':0,'parameter_count':parameter_count,'parameters_unchanged':True,'loss_total':float(loss.detach()),'loss_l1':float(parts['l1'].detach()),'loss_regional':float(parts['regional'].detach()),'parameter_gradient_norm':norm2**.5,'finite_gradients':True,'support':parts['support'],'regions':names,'region_pixels':{k:int(v.sum()) for k,v in regions.items()},'heldout_opened':False,'inputs_sha256':{'geometry':sha(gp),'shard':sha(sp),'weights':sha(a.pesos),'manifest':sha(manifest),'geometry_source':sha(Path(sys.modules['evaluar_regiones_geometricas'].__file__)),'generator_source':sha(Path(sys.modules['unet_generator'].__file__)),'loss_source':sha(Path(__file__).parent/'perdida_cuentas_regionales.py'),'check_source':sha(Path(__file__))},'limit':'single train geometry; no optimizer, resumption, GPU or quality acceptance'}
result['regional_parameter_gradient_norm']=regional_norm2**.5
a.salida.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))

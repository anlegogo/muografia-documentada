import csv,gc,hashlib,json,sys,platform,io
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Verificación independiente de los dos best.pt sobre val')
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--unet',type=Path,required=True)
p.add_argument('--cgan',type=Path,required=True)
p.add_argument('--entrega',type=Path,required=True)
p.add_argument('--datos',type=Path,required=True)
p.add_argument('--salida',type=Path,required=True)
p.add_argument('--modulos',type=Path,help='Opcional: copias verificadas de unet_generator.py, muography_dataset.py y metrics.py')
p.add_argument('--dependencias',type=Path)
p.add_argument('--torch-dir',type=Path)
args=p.parse_args()
if args.dependencias:sys.path.insert(0,str(args.dependencias))
import numpy as np
from skimage.metrics import structural_similarity,peak_signal_noise_ratio
if args.torch_dir:sys.path.insert(0,str(args.torch_dir))
import torch
out=args.salida;out.mkdir(parents=True,exist_ok=True)
root=args.repo
if args.modulos:
 sys.path.insert(0,str(args.modulos))
 from unet_generator import build_generator
else:
 for sub in ('','scripts/training','scripts/evaluation'):sys.path.insert(0,str(root/'objetivo-2/implementacion'/sub))
 from models import build_generator
from muography_dataset import DataContract,MuographyPairs,digest
from metrics import compute_ssim,compute_psnr
ref=json.loads((root/'objetivo-2/evidencias/correcciones-v1.json').read_text())
contract=DataContract(args.datos,root/'objetivo-2/evidencias/contrato-datos-v1.json',ref['manifest_sha256'])
ds=MuographyPairs(contract,'val',.05)
loader=torch.utils.data.DataLoader(ds,batch_size=4,shuffle=False)
entrega=args.entrega
published=list(csv.DictReader((entrega/'datos/analisis-val/metricas-por-imagen-val.csv').open(newline='')))
expected={'unet':'734bc5dc1aa4cdc16a3fa0b6de2d58da7575c5bd0b1fe342bc266283f0e8e57a','cgan':'e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0'}
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
report={'device':'cpu','torch':torch.__version__,'numpy':np.__version__,'source_module_sha256':{label:hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() for label,module in [('dataset',sys.modules['muography_dataset']),('metrics',sys.modules['metrics'])]},'python':platform.python_version(),'n':360,'heldout_images_opened':False,'models':{}}
safe=[np._core.multiarray._reconstruct,np.ndarray,np.dtype,np.dtypes.UInt32DType]
all_rows=[]
for name,sha in expected.items():
 path=args.unet if name=='unet' else args.cgan
 assert digest(path)==sha
 print('Hash verificado',name,flush=True)
 with torch.serialization.safe_globals(safe):ckpt=torch.load(io.BytesIO(path.read_bytes()),map_location='cpu',weights_only=True)
 assert ckpt['data_manifest_sha256']==ref['manifest_sha256']
 assert ckpt['implementation_sha256']==ref['implementation_sha256']
 assert ckpt['normalization']==contract.manifest['normalization']
 assert ckpt['epoch']==ckpt['best_epoch']==5
 cfg=json.loads((entrega/f'datos/resultados/oe2-v1-piloto-f05-{name}-s2026100301/record/config.json').read_text())
 assert ckpt['config']==cfg['config'] and ckpt['config_sha8']==cfg['config_sha8']
 net=build_generator('unet_dc_5').eval();net.load_state_dict(ckpt['generator'],strict=True)
 predictions=np.zeros((360,256,256),dtype=np.float32)
 vals={'ssim':[],'psnr':[]};diffs={'ssim':[],'psnr':[]};cursor=0
 with torch.inference_mode():
  for x,y in loader:
   z=net(x).numpy()[:,0];assert np.isfinite(z).all();predictions[cursor:cursor+len(x)]=z
   for j in range(len(x)):
    i=cursor+j;gid,vi,k=ds.index[i];row=published[i]
    assert (gid,str(vi),str(k))==(row['geometry'],row['view'],row['realization'])
    s=compute_ssim(z[j],y[j,0].numpy());q=compute_psnr(y[j,0].numpy(),z[j])
    for metric,v in [('ssim',s),('psnr',q)]:vals[metric].append(v);diffs[metric].append(abs(v-float(row[f'{metric}_{name}'])))
    all_rows.append({'model':name,'geometry':gid,'view':vi,'realization':k,'ssim':s,'psnr':q})
   cursor+=len(x)
   if cursor%40==0:print(name,cursor,flush=True)
 np.save(out/f'{name}-predicciones.npy',predictions)
 report['models'][name]={'sha256':sha,'bytes':path.stat().st_size,'epoch':ckpt['epoch'],'contract_matches':True,'configuration_matches':True,'best_ssim_checkpoint':ckpt['best_ssim'],'means':{k:float(np.mean(v)) for k,v in vals.items()},'max_abs_difference_csv':{k:max(v) for k,v in diffs.items()},'range':[float(predictions.min()),float(predictions.max())],'within_tolerance':max(diffs['ssim'])<1e-4 and max(diffs['psnr'])<.01}
 (out/'verificacion.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 del ckpt,net,predictions;gc.collect()
with (out/'metricas-recalculadas.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(all_rows[0]));w.writeheader();w.writerows(all_rows)
report['status']='passed' if all(v['within_tolerance'] for v in report['models'].values()) else 'differences_require_review'
(out/'verificacion.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))

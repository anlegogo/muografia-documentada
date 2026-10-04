"""Sondeo CPU E1 sobre cuatro muestras train fijadas, sin pasos de optimización."""
import argparse,json,math,statistics
from pathlib import Path
import torch
import ejecutar_ajuste_cgan as e
from datos_ajuste import Store,digest
from perdida_espacial_borde_experimental import spatial_edge_count_loss
def norm(gs):return math.sqrt(sum(float(g.double().square().sum()) for g in gs))
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['datos','mascaras','pesos','salida']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args()
 if a.salida.exists():raise FileExistsError(a.salida)
 e.configure();e.seed_all(2026100404)
 store=Store(a.datos,a.mascaras);cfg=e.spec('C1','R1');initial=e.load_initial(a.pesos,cfg,store)
 G=e.build_generator(cfg['generator']);G.load_state_dict(initial[0]);G.eval()
 D=e.build_critic(cfg['critic']);D.load_state_dict(initial[1]);D.eval()
 for par in D.parameters():par.requires_grad_(False)
 before={'G':e.state_digest(G.state_dict()),'D':e.state_digest(D.state_dict())}
 # Primera realización de cada geometría del conjunto técnico ya fijado.
 rows=[[[gid,v,0] for v in [0,1,3,5]] for gid in store.manifest['splits']['train']]
 assert len(rows)==12 and all(r[0] in store.manifest['splits']['train'] for batch in rows for r in batch)
 results=[]
 for row in rows:
  x,y,c,m=store.batch(row,torch.device('cpu'));z=G(x)
  base,_,_=e.generator_objective(D,x,z,y,c,m,store.families,store.scale,cfg)
  edge=spatial_edge_count_loss(z,c,m[:,2:3],store.scale)
  params=tuple(G.parameters())
  gb=torch.autograd.grad(base,params,retain_graph=True)
  ge=torch.autograd.grad(edge,params)
  assert all(torch.isfinite(g).all() for g in gb+ge)
  nb,ne=norm(gb),norm(ge);assert nb>0 and ne>0
  cosine=sum(float((g.double()*h.double()).sum()) for g,h in zip(gb,ge))/(nb*ne)
  assert abs(cosine)<=1+1e-12
  item={'batch':row,'baseline_loss':float(base.detach()),'edge_loss':float(edge.detach()),'baseline_gradient_norm':nb,'edge_gradient_norm':ne,'edge_to_baseline_gradient_ratio_weight_one':ne/nb,'gradient_cosine':cosine}
  results.append(item);print(json.dumps(item),flush=True)
  del gb,ge,base,edge,z
 after={'G':e.state_digest(G.state_dict()),'D':e.state_digest(D.state_dict())};assert after==before
 evidence={'schema':'oe2-edge-gradient-profile-v1','date':'2026-10-04','mode':'eval with autograd; twelve train batches in eval mode',
  'training_performed':False,'optimizer_steps':0,'weights_unchanged':True,'val_images_opened':False,'heldout_opened':False,'gpu_ready':False,
  'initial_checkpoint_sha256':digest(a.pesos),'mask_manifest_sha256':store.identity,'before_state_sha256':before,'after_state_sha256':after,
  'script_sha256':digest(Path(__file__)),'candidate_sha256':digest(Path(__file__).with_name('perdida_espacial_borde_experimental.py')),
  'environment':e.environment(torch.device('cpu')),'samples':results,
  'limitation':'Local gradient directions at initial checkpoint, fixed eval mode and one sample at a time; no critic updates, optimizer, recovery or quality validation. Does not select a coefficient.'}
 ratios=[x['edge_to_baseline_gradient_ratio_weight_one'] for x in results]
 coefficient=math.floor(1000*min(1.,.1/statistics.median(ratios),.25/max(ratios)))/1000
 assert coefficient>0
 evidence.update(selected_lambda=coefficient,ratio_median=statistics.median(ratios),ratio_max=max(ratios),profile_design_sha256=digest(e.ROOT/'objetivo-2/configuraciones/borde-cgan-v1/perfil.spec.json'))
 evidence['limitation']='Twelve train batches, eval mode at initial checkpoint, no optimizer or critic updates. Engineering coefficient, not optimized on val or a physical acceptance tolerance.'
 print(json.dumps({'selected_lambda':coefficient,'ratio_median':statistics.median(ratios),'ratio_max':max(ratios)}),flush=True)
 a.salida.parent.mkdir(parents=True,exist_ok=True);a.salida.write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()




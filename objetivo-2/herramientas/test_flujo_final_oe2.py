"""Integración con matrices sintéticas: inferencia, reuso, evaluación y corrupción."""
import tempfile,json,sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
import torch
import evaluacion_final_oe2 as e

def run():
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);data=root/'data';(data/'dataset-v2/shards').mkdir(parents=True);out=root/'predictions';repo=root/'repo';repo.mkdir();(root/'w').write_bytes(b'fixture-weight')
  weights={'fixture':str(root/'w')};e.write(root/'weights.json',weights)
  gids=['fixture-1','fixture-2','fixture-3','fixture-4'];files={};geoms={}
  for g in gids:
   p=data/f'dataset-v2/shards/{g}.npz';np.savez_compressed(p,ref_counts=np.full((6,256,256),20,dtype=np.uint32),low_counts=np.ones((6,4,20,256,256),dtype=np.uint16),fractions=np.array([.5,.1,.05,.01]),az_centers_deg=np.linspace(-30,30,256),el_centers_deg=np.linspace(2,47,256),az_edges_deg=np.linspace(-30.1,30.1,257),el_edges_deg=np.linspace(1.9,47.1,257));files[str(p.relative_to(data)).replace('\\','/')]=e.sha(p)
   geoms[g]=g+'.json';e.write(repo/geoms[g],{'edifice':{'base_radius_m':300,'height_m':250},'anomalies':[]})
  cfg={'detector_distance_m':1000,'detector_height_m':1.5,'cone_top_radius_m':.1,'rock_sky_margin_pixels':2,'anomaly_min_length_m':20,'core_erosion_pixels':1,'min_matched_pixels':20,'min_match_fraction':.8,'control_cone_length_relative_tolerance':.05,'control_donors_per_pixel':5}
  s={'models':{'fixture':{'sha256':e.sha(root/'w')}},'data_sha256':files,'geometry_order':gids,'geometry_files':geoms,'normalization_scale':8.239,'regional_protocol':cfg,'splits':{'test':gids[:3],'generalization':gids[3:]},'scope':'Synthetic integration fixture only'}
  class Net(torch.nn.Module):
   calls=0
   def forward(self,x):self.calls+=1;return x
  net=Net();a=SimpleNamespace(repo=repo,data=data,weights=root/'weights.json',output=out,model='fixture',device='cpu',report=root/'report')
  with patch.object(e,'load_net',return_value=net):
   e.infer(a,s,'fixture-signature');assert net.calls==120
   e.infer(a,s,'fixture-signature');assert net.calls==120
   try:e.infer(a,s,'other-signature')
   except ValueError:pass
   else:raise AssertionError('Se aceptó identidad distinta')
  e.evaluate(a,s,'fixture-signature');result=e.read(a.report/'evaluacion-final.json');assert len(result['images'])==960 and result['summary']['generalization']['fixture']['Q_macro'] is None
  original=out/'fixture'/(gids[0]+'.npy');original.write_bytes(b'corrupt')
  with patch.object(e,'load_net',return_value=net):
   try:e.infer(a,s,'fixture-signature')
   except ValueError:pass
   else:raise AssertionError('Se reutilizó predicción corrupta')
  a.report=root/'report2'
  try:e.evaluate(a,s,'fixture-signature')
  except ValueError:pass
  else:raise AssertionError('Se evaluó predicción corrupta')
 return {'synthetic_only':True,'heldout_images_opened':False,'checks':['480 predictions','skip completed exports','reject different identity','full evaluation 960 rows including input','homogeneous Q undefined','reject corrupted resume','reject corrupted evaluation']}
if __name__=='__main__':
 result=run();e.write(Path(__file__).with_name('verificacion-flujo-sintetico.json'),result);print(json.dumps(result))

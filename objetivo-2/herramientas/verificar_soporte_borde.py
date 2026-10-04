"""Comprueba soporte y denominador del borde en las 90 vistas train/val, sin inferencia."""
import argparse,json
from pathlib import Path
from datos_ajuste import Store,atomic_json,digest
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['datos','mascaras','salida']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args()
 if a.salida.exists():raise FileExistsError('Salida nueva requerida')
 store=Store(a.datos,a.mascaras);rows=[]
 for split in ['train','val']:
  for gid in store.manifest['splits'][split]:
   refs,_=store.load(gid)
   assert store.manifest['geometries'][gid]['families'][2]==2
   for view in range(6):
    mask=store.masks[gid][view,2];pixels=int(mask.sum());counts=int(refs[view][mask].sum())
    assert pixels>=20 and counts>0,(gid,view,pixels,counts)
    rows.append({'split':split,'geometry':gid,'view':view,'pixels':pixels,'reference_sum':counts})
 assert len(rows)==90
 result={'schema':'oe2-edge-support-v1','views':90,'train_views':72,'val_views':18,'training_performed':False,'heldout_opened':False,'coefficient_fitted_here':False,
 'minimum_pixels':min(x['pixels'] for x in rows),'minimum_reference_sum':min(x['reference_sum'] for x in rows),'cache_sha256':store.identity,'script_sha256':digest(Path(__file__)),'rows':rows}
 a.salida.parent.mkdir(parents=True,exist_ok=True);atomic_json(a.salida,result)
 print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
if __name__=='__main__':main()


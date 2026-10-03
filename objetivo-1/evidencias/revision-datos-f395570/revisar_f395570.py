from pathlib import Path
import sys,json,hashlib,numpy as np
ROOT=Path(__file__).resolve().parents[1]
r=ROOT/'muografia-documentada';sys.path.insert(0,str(r/'herramientas'))
from evaluar_campana_114 import review
from preparar_imagen_angular_v1 import read_image
from empaquetar_angular_v1 import audit,low_counts,FRACTIONS
b=ROOT/'tmp/revision-f395570/objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/datos/sc3/campana-114'
e=r/'objetivo-1/evidencias/preparacion-campana-114';verified=[]
for folder,inventory in [('fusion','fusion.sha256'),('imagenes','imagenes.sha256')]:
    for line in (b/'posproceso'/inventory).read_text().splitlines():
        h,name=line.split(maxsplit=1);f=b/folder/name
        assert hashlib.sha256(f.read_bytes()).hexdigest()==h,str(f)
        verified.append(str(f.relative_to(b)))
result=review(b/'fusion',e/'plan.json',r/'objetivo-1/contratos/receta-operativa-siete-actividades.json',r/'objetivo-1/evidencias/preparacion-siete-actividades/cielo-ideal-margen-5.json')
received=json.loads((b/'posproceso/evaluacion-114-344M.json').read_text());diff=[]
def compare(a,b):
    assert type(a)==type(b)
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:compare(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for c,d in zip(a,b):compare(c,d)
    elif isinstance(a,float):diff.append(abs(a-b));assert abs(a-b)<1e-10
    else:assert a==b,(a,b)
compare(result,received)
scope=sorted(g['geometry'] for g in json.loads((e/'plan.json').read_text())['geometries'])
report,images=audit(list((b/'imagenes').glob('*.npz')),scope)
assert report['technical_complete']
expected=json.loads((b/'huellas-contenido.json').read_text())['pairs']
checks=[];total_roi=0;good_roi=0
for index,image in enumerate(images):
    m=image['meta'];gid=m['geometry_id'];v=m['view_index'];stem=f'{gid}_view{v}'
    _,counts,coords,_,_=read_image(b/'fusion'/gid/(stem+'_hist.csv'))
    assert np.array_equal(counts,image['counts'])
    for k,c in coords.items():assert np.array_equal(c,image['coords'][k])
    lows=low_counts(counts,gid,v)
    assert lows.shape==(4,20,256,256) and lows.dtype==np.uint32 and np.all(lows<=counts)
    fields={}
    for key,a in dict(counts_ref=counts,low_counts=lows,fractions=FRACTIONS).items():
        h=hashlib.sha256();h.update(a.dtype.str.encode());h.update(str(a.shape).encode());h.update(np.ascontiguousarray(a).tobytes())
        fields[key]=h.hexdigest();assert fields[key]==expected[stem+'_pairs.npz'][key],stem
    mask=np.load(e/(gid+'-rock_roi.npy'));values=counts.reshape(64,4,64,4).sum(axis=(1,3))[mask]
    total_roi+=len(values);good_roi+=int(np.sum(values>=100))
    checks.append({'view':stem,'partition':gid.split('-')[1],'content_sha256':fields})
    if (index+1)%20==0:print('Referencias y 80 pares verificados:',index+1,flush=True)
assert len(checks)==114 and len(expected)==114
summary={'commit':'f395570','files_hash_verified':len(verified),'evaluation_reproduced_from_pixels':True,'max_float_difference':max(diff),
    'references':114,'npz_counts_and_coordinates_exact':True,'pairs_regenerated_and_content_verified':9120,'arrays_hashed':342,
    'pairs_saved_to_disk':False,'pair_arrays_compared_in_memory':True,'roi_total':total_roi,'roi_ge100':good_roi,
    'roi_fraction_ge100':good_roi/total_roi,'border_regions_equivalent':1710,'views_rock_goal_met':107,
    'numpy_version':np.__version__,'physical_validation':False,'drive_files_downloaded':False,'dataset_v2_verified':False,
    'checks':checks}
(ROOT/'tmp/revision-f395570-verificacion.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode())
(ROOT/'tmp/revision-f395570-evaluacion.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
print(json.dumps({k:v for k,v in summary.items() if k!='checks'},indent=2),flush=True)

"""Audita un lote y opcionalmente genera pares de conteo v1, sin transporte.

python herramientas/empaquetar_angular_v1.py DIRECTORIO --geometrias geo-train-01 --informe NUEVO.json
Añadir --salida NUEVA_CARPETA para empaquetar: exige las 6 vistas de cada geometría.
Sin --geometrias exige las 19 del catálogo. No declara validación física.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import numpy as np
from preparar_imagen_angular_v1 import coordinates

ROOT=Path(__file__).resolve().parents[1]
FRACTIONS=np.array([.5,.1,.05,.01])
REPLICATES=20


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(path):
    path=Path(path);mp=path.with_suffix('.meta.json')
    m=json.loads(mp.read_text(encoding='utf-8'));coord=coordinates(m)
    gid=m.get('geometry_id');view=m.get('view_index')
    if not isinstance(gid,str) or not re.fullmatch(r'geo-(train|val|test|gen)-\d{2}',gid):
        raise ValueError('identidad de geometría inválida')
    if type(view) is not int or not 0<=view<6 or path.stem!=f'{gid}_view{view}':
        raise ValueError('identidad de vista inválida')
    for key in ['geometry_sha256','binary_sha256','npz_sha256']:
        if not re.fullmatch('[0-9a-f]{64}',str(m.get(key,''))):raise ValueError('falta '+key)
    if sha(path)!=m['npz_sha256']:raise ValueError('NPZ no coincide con su huella')
    tables=m.get('table_sha256',{})
    for name in ['meta.json','row_weights_30d.txt','p_cdf.txt']:
        if not re.fullmatch('[0-9a-f]{64}',str(tables.get(name,''))):raise ValueError('falta huella de tabla '+name)
    for key in ['engine','sampling','physics_note','detector','exposure_days']:
        if key not in m:raise ValueError('falta configuración '+key)
    for key in ['engine','sampling','physics_note']:
        if not isinstance(m[key],str) or not m[key].strip():raise ValueError('configuración vacía '+key)
    for key in ['side_m','distance_m','height_m']:
        value=m['detector'].get(key) if isinstance(m['detector'],dict) else None
        if type(value) not in (int,float) or not np.isfinite(value) or value<0 or (key!='height_m' and value==0):
            raise ValueError('detector incompleto o inválido')
    n=m.get('events_transported');det=m.get('detected_in_bins')
    if type(n) is not int or n<=0 or type(det) is not int or not 0<=det<=n:
        raise ValueError('presupuesto o conteos inválidos')
    exposure=m['exposure_days']
    if type(exposure) not in (int,float) or not np.isfinite(exposure) or (exposure<=0 and exposure!=-1):
        raise ValueError('exposición no reconocida')
    with np.load(path,allow_pickle=False) as z:
        counts=z['counts_ref'].copy()
        if counts.dtype!=np.uint32 or counts.shape!=(256,256) or int(counts.sum(dtype=np.uint64))!=det:
            raise ValueError('matriz de conteos inválida')
        for k,v in coord.items():
            if not np.array_equal(z[k],v):raise ValueError('coordenadas inconsistentes')
    signature={k:m[k] for k in ['grid','binary_sha256','table_sha256','engine','sampling','physics_note','detector','exposure_days']}
    if exposure==-1:signature['fixed_events']=n
    return {'path':path,'meta':m,'coords':coord,'counts':counts,
            'signature':json.dumps(signature,sort_keys=True), 'meta_sha256':sha(mp)}


def audit(paths,expected_geometries):
    if not expected_geometries or len(set(expected_geometries))!=len(expected_geometries):
        raise ValueError('lista de geometrías vacía o repetida')
    report={'schema':'oe1-package-review-v1','physical_validation':False,
            'expected_geometries':sorted(expected_geometries),'errors':[],'missing':[],'references':[]}
    images=[];seen=set();signatures=set();geo_hashes={}
    for p in sorted(map(Path,paths)):
        try:
            image=load(p);m=image['meta'];key=(m['geometry_id'],m['view_index'])
            if key in seen:raise ValueError('vista repetida')
            if key[0] not in expected_geometries:raise ValueError('geometría fuera del alcance')
            if key[0] in geo_hashes and geo_hashes[key[0]]!=m['geometry_sha256']:
                raise ValueError('versiones de geometría mezcladas')
            seen.add(key);geo_hashes[key[0]]=m['geometry_sha256'];signatures.add(image['signature'])
            report['references'].append({'geometry_id':key[0],'view':key[1],
                                         'npz_sha256':m['npz_sha256'],'meta_sha256':image['meta_sha256'],
                                         'counts':m['detected_in_bins']})
            images.append(image)
        except (OSError,ValueError,KeyError,TypeError) as exc:
            report['errors'].append({'file':str(p),'error':str(exc)})
    if len(signatures)>1:report['errors'].append({'error':'mezcla de entorno, binario, tablas, detector o exposición'})
    report['missing']=[{'geometry_id':g,'view':v} for g in sorted(expected_geometries) for v in range(6) if (g,v) not in seen]
    report['technical_complete']=not report['errors'] and not report['missing']
    report['actual_references']=len(images);report['target_references']=6*len(expected_geometries)
    report['target_pairs']=6*len(expected_geometries)*80
    return report,images


def low_counts(counts,gid,view,master=20260805):
    """New stable seed scheme, independent of batch ordering; uint32, no clipping."""
    if type(master) is not int or master<0:raise ValueError('semilla debe ser entero no negativo')
    identity=int.from_bytes(hashlib.sha256(gid.encode()).digest()[:8],'little')
    out=np.empty((4,REPLICATES,*counts.shape),dtype=np.uint32)
    for fi,fraction in enumerate(FRACTIONS):
        streams=np.random.SeedSequence([master,0x415A5631,identity,view,fi]).spawn(REPLICATES)
        for ri,stream in enumerate(streams):
            out[fi,ri]=np.random.default_rng(stream).binomial(counts.astype(np.int64),fraction)
    if np.any(out>counts):raise AssertionError('conteos reducidos exceden referencia')
    return out


def package(paths,geometries,destination,master=20260805):
    if type(master) is not int or master<0:raise ValueError('semilla debe ser entero no negativo')
    report,images=audit(paths,geometries)
    if not report['technical_complete']:raise ValueError('lote incompleto/incompatible: ejecutar auditoría antes de empaquetar')
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=False)
    report.update(state='paquete_tecnico_no_validacion_fisica',master_seed=master,
                  seed_scheme='SeedSequence(master,0x415A5631,sha256(gid)[:8] little-endian,view,fraction_index).spawn(20)',
                  numpy_version=np.__version__,fractions=FRACTIONS.tolist(),realizations=REPLICATES,files=[])
    for image in images:
        m=image['meta'];gid=m['geometry_id'];view=m['view_index'];counts=image['counts']
        lows=low_counts(counts,gid,view,master)
        p=destination/f'{gid}_view{view}_pairs.npz'
        np.savez_compressed(p,counts_ref=counts,low_counts=lows,fractions=FRACTIONS,**image['coords'])
        with np.load(p,allow_pickle=False) as z:
            if not np.array_equal(z['counts_ref'],counts) or not np.array_equal(z['low_counts'],lows):
                raise RuntimeError('fallo de relectura del paquete')
        sidecar=destination/f'{gid}_view{view}.meta.json'
        sidecar.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
        report['files'].append({'name':p.name,'sha256':sha(p),'geometry_id':gid,'view':view,
                                'partition':gid.split('-')[1], 'reference_sha256':m['npz_sha256'],
                                'metadata_name':sidecar.name,'metadata_sha256':sha(sidecar)})
    (destination/'manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directorio',type=Path)
    p.add_argument('--geometrias',nargs='+');p.add_argument('--informe',required=True,type=Path)
    p.add_argument('--salida',type=Path);p.add_argument('--semilla',type=int,default=20260805);a=p.parse_args()
    geometries=a.geometrias or sorted(x.stem for x in (ROOT/'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries').glob('*.json'))
    if a.informe.exists():raise FileExistsError(a.informe)
    paths=list(a.directorio.rglob('*.npz'))
    result=package(paths,geometries,a.salida,a.semilla) if a.salida else audit(paths,geometries)[0]
    with a.informe.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ['references','files']},indent=2))
    raise SystemExit(0 if result['technical_complete'] else 1)

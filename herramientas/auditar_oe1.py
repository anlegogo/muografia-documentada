"""Auditoría derivada OE1. Lee originales; escribe solo evidencias.

Requiere NumPy. Los testigos geométricos prueban intersección; una búsqueda
sin testigo NO prueba separación. No sustituye navegación Geant4.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, itertools, json, platform
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / 'objetivo-1/originales'
OUT = ROOT / 'objetivo-1/evidencias'

def shape(a):
    p=a['params']; kind=a['kind']
    c=np.array([p['cx_m'],p['cy_m'],(p['z0_m']+p['z1_m'])/2 if kind=='conduit' else p['cz_m']])
    axes=np.array([p['radius_m'],p['radius_m'],(p['z1_m']-p['z0_m'])/2]) if kind=='conduit' else np.array([p['radius_m']]*3) if kind=='cavity' else np.array([p['ax_m'],p['ay_m'],p['az_m']])
    return c,axes

def margin(a,points):
    c,s=shape(a); v=(points-c)/s
    return np.maximum((v[...,:2]**2).sum(axis=-1)-1,np.abs(v[...,2])-1) if a['kind']=='conduit' else (v*v).sum(axis=-1)-1

def pair(a,b):
    ca,sa=shape(a); cb,sb=shape(b)
    if a['kind']==b['kind']=='cavity':
        gap=float(np.linalg.norm(ca-cb)-sa[0]-sb[0])
        if gap>=0: return {'estado':'sin intersección interior por distancia entre esferas','separacion_m':gap}
    if {a['kind'],b['kind']}=={'conduit','cavity'}:
        cyl,sph=(a,b) if a['kind']=='conduit' else (b,a)
        cc,sc=shape(cyl); cs,ss=shape(sph)
        distance=float(np.hypot(max(np.linalg.norm(cs[:2]-cc[:2])-sc[0],0),max(abs(cs[2]-cc[2])-sc[2],0)))
        if distance>=ss[0]:
            return {'estado':'sin intersección interior por distancia esfera-cilindro','separacion_m':distance-float(ss[0])}
    lo=np.maximum(ca-sa,cb-sb); hi=np.minimum(ca+sa,cb+sb)
    if np.any(hi<=lo): return {'estado':'sin intersección interior por cajas envolventes'}
    points=np.stack(np.meshgrid(*(np.linspace(l,h,33) for l,h in zip(lo,hi)),indexing='ij'),axis=-1).reshape(-1,3)
    m=np.maximum(margin(a,points),margin(b,points)); idx=int(np.argmin(m))
    if m[idx] < -1e-8:
        return {'estado':'intersección demostrada con testigo interior','testigo_m':points[idx].tolist(),'margen_a':float(margin(a,points[idx])),'margen_b':float(margin(b,points[idx]))}
    return {'estado':'no resuelto: malla sin testigo, requiere Geant4 o análisis adicional'}

def containment(a,ed):
    c,s=shape(a); R=ed['base_radius_m']; H=ed['height_m']; k=(R-0.1)/H
    zmin=float(c[2]-s[2]); zmax=float(c[2]+s[2])
    if a['kind']=='conduit': bound=float(np.linalg.norm(c[:2])+s[0]+k*zmax)
    else: bound=float(np.linalg.norm(c[:2])+k*c[2]+np.sqrt(max(s[0],s[1])**2+(k*s[2])**2))
    state='contenido por cota analítica suficiente' if zmin>=0 and zmax<=H and bound<=R else 'cota insuficiente: requiere análisis'
    witness=None
    if zmin<0:
        witness=[float(c[0]),float(c[1]),zmin]; state='salida del cono demostrada bajo la base'
    elif a['kind']=='conduit' and bound>R:
        unit=c[:2]/np.linalg.norm(c[:2]) if np.linalg.norm(c[:2]) else np.array([1.,0.])
        witness=[*map(float,c[:2]+s[0]*unit),zmax]; state='salida lateral del cono demostrada'
    return {'zmin_m':zmin,'zmax_m':zmax,'margen_radial_suficiente_m':R-bound,
            'estado':state,'testigo_superficie_m':witness,'contacta_base':abs(zmin)<1e-9}

def main():
    geometries=[]; data=[]; errors=[]
    catalogs=sorted((ORIG/'scripts/simulation/geometry_catalog/geometries').glob('*.json'))
    for gi,path in enumerate(catalogs):
        g=json.loads(path.read_text(encoding='utf-8')); gid=g['geometry_id']; anomalies=g['anomalies']
        pairs=[{'indices':[i,j],**pair(anomalies[i],anomalies[j])} for i,j in itertools.combinations(range(len(anomalies)),2)]
        geometries.append({'geometria':gid,'contencion':[{'indice':i,**containment(a,g['edifice'])} for i,a in enumerate(anomalies)],'pares':pairs})
        with np.load(ORIG/f'dataset/shards/{gid}.npz',allow_pickle=False) as z:
            ref=z['ref_counts']; low=z['low_counts']; fractions=z['fractions']
            meta=json.loads((ORIG/f'dataset/shards/{gid}.meta.json').read_text(encoding='utf-8'))
            # GeometryConfig.hh declares kNEl=kNAz=256.
            checks={'shape':ref.shape==(6,256,256) and low.shape==(6,4,20,256,256),
                    'dtype':str(ref.dtype)=='uint32' and str(low.dtype)=='uint16',
                    'fracciones':np.array_equal(fractions,[.5,.1,.05,.01]),
                    'limite_binomial':bool(np.all(low<=ref[:,None,None,:,:])),
                    'referencias_coinciden':True,'semillas_coinciden':True,'pares_reproducidos':True}
            max_unclipped=0; clipped=0; mismatches=0
            for vi in range(6):
                with np.load(ORIG/f'data/campaign-geant4/{gid}/{gid}_view{vi}.npz',allow_pickle=False) as raw:
                    checks['referencias_coinciden'] &= bool(np.array_equal(ref[vi],raw['counts_ref']))
                for fi,f in enumerate(fractions):
                    seeds=np.random.SeedSequence([20260805,11,gi,vi,fi]).spawn(20)
                    checks['semillas_coinciden'] &= [int(s.generate_state(1)[0]) for s in seeds]==meta['seeds'][f'view{vi}_frac{f}']
                    for ki,s in enumerate(seeds):
                        sample=np.random.default_rng(s).binomial(ref[vi].astype(np.int64),f)
                        max_unclipped=max(max_unclipped,int(sample.max())); clipped+=int(np.count_nonzero(sample>65535))
                        mismatches+=int(not np.array_equal(np.minimum(sample,65535),low[vi,fi,ki]))
            checks['pares_reproducidos']=mismatches==0
            row={'geometria':gid,'checks':checks,'forma_ref':list(ref.shape),'forma_low':list(low.shape),'max_ref':int(ref.max()),'max_low':int(low.max()),'max_binomial_sin_recorte':max_unclipped,'pixeles_recortados_reproduccion':clipped,'pares_distintos':mismatches}
            data.append(row)
            errors.extend(f'{gid}: {k}' for k,v in checks.items() if not v)
        print(gid, 'OK' if all(checks.values()) else checks,flush=True)
    result={'fecha_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'numpy':np.__version__,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'geometrias':geometries,'datos':data,'errores_datos':errors,
            'limites':'Geometría ideal alineada según JSON y Geant4; tolerancias/navegación no simuladas. Pares regenerados en memoria, sin modificar originales; no nuevo transporte Monte Carlo.'}
    OUT.mkdir(exist_ok=True)
    (OUT/'auditoria-oe1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    overlaps=[{'geometria':g['geometria'],**p} for g in geometries for p in g['pares'] if 'demostrada' in p['estado']]
    print(json.dumps({'intersecciones':overlaps,'errores_datos':errors,'pares_comprobados':len(data)*480,'pixeles_recortados':sum(x['pixeles_recortados_reproduccion'] for x in data)},ensure_ascii=False,indent=2))
    return bool(errors)

if __name__=='__main__': raise SystemExit(main())

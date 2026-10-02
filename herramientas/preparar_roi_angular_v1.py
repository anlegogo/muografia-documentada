"""ROI geométrica nueva para la intersección conducto/cuerpo denso de geo-train-06.

Rayos rectos centrales de 3000 m; umbral heredado de 20 m. No transporte,
no aceptación de detector, no sustitución de la ROI congelada del ensayo.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from preparar_imagen_angular_v1 import coordinates

ROOT = Path(__file__).resolve().parents[1]
GEO = ROOT/'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries/geo-train-06.json'
GEO_SHA = 'c8f6c1352af1f7564356cffbd98e26fd6a5881e5ece15a0ab6f2ed60c8ea26ed'


def quadratic_interval(a,b,c):
    """Interval where a*t²+b*t+c <= 0 for a>=0 and b=0 when a=0."""
    a,b,c=np.broadcast_arrays(a,b,c)
    disc=b*b-4*a*c
    safe=np.where(a>0,a,1.)
    root=np.sqrt(np.maximum(disc,0))
    lo=(-b-root)/(2*safe);hi=(-b+root)/(2*safe)
    lo=np.where((a==0)&(c<=0),-np.inf,lo)
    hi=np.where((a==0)&(c<=0),np.inf,hi)
    empty=(disc<0)|((a==0)&(c>0))
    return np.where(empty,np.inf,lo),np.where(empty,-np.inf,hi)


def intersection_lengths(origin, directions, cyl, ell, max_length=3000.):
    """Exact ray intervals for a finite vertical cylinder and axis-aligned ellipsoid."""
    d=np.asarray(directions,dtype=float);o=np.asarray(origin,dtype=float)
    if not np.all(np.isfinite(d)) or not np.allclose(np.linalg.norm(d,axis=-1),1,atol=1e-12,rtol=0):
        raise ValueError('direcciones deben ser unitarias y finitas')
    xy=o[:2]-np.array([cyl['cx_m'],cyl['cy_m']])
    low,high=quadratic_interval(np.sum(d[...,:2]**2,axis=-1),
                               2*np.sum(d[...,:2]*xy,axis=-1),np.sum(xy**2)-cyl['radius_m']**2)
    dz=d[...,2];safe=np.where(dz!=0,dz,1.)
    t0=(cyl['z0_m']-o[2])/safe;t1=(cyl['z1_m']-o[2])/safe
    zlo=np.minimum(t0,t1);zhi=np.maximum(t0,t1)
    inside=cyl['z0_m']<=o[2]<=cyl['z1_m']
    zlo=np.where(dz==0,-np.inf if inside else np.inf,zlo)
    zhi=np.where(dz==0,np.inf if inside else -np.inf,zhi)
    center=np.array([ell[k] for k in ['cx_m','cy_m','cz_m']])
    axes=np.array([ell[k] for k in ['ax_m','ay_m','az_m']])
    q=(o-center)/axes;v=d/axes
    elo,ehi=quadratic_interval(np.sum(v*v,axis=-1),2*np.sum(v*q,axis=-1),np.sum(q*q)-1)
    lower=np.maximum(np.maximum(low,zlo),np.maximum(elo,0))
    upper=np.minimum(np.minimum(high,zhi),np.minimum(ehi,max_length))
    return np.maximum(0,upper-lower)


def rays(az_centers,el_centers,view):
    angle=np.deg2rad(view*60)
    origin=np.array([1000*np.cos(angle),1000*np.sin(angle),1.5])
    az=np.deg2rad(az_centers)[None,:]+angle+np.pi
    el=np.deg2rad(el_centers)[:,None]
    x=np.cos(el)*np.cos(az);y=np.cos(el)*np.sin(az)
    z=np.broadcast_to(np.sin(el),x.shape)
    return origin,np.stack([x,y,z],axis=-1)


def run(grid_meta_path,output):
    if hashlib.sha256(GEO.read_bytes()).hexdigest()!=GEO_SHA:
        raise ValueError('esta herramienta está limitada a la geometría auditada geo-train-06')
    meta=json.loads(Path(grid_meta_path).read_text(encoding='utf-8'))
    coords=coordinates(meta)
    g=json.loads(GEO.read_text(encoding='utf-8'))
    cyl,ell=[a['params'] for a in g['anomalies']]
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    report={'estado':'ROI_geometrica_candidata_no_congelada', 'geometry_id':'geo-train-06',
            'geometry_sha256':GEO_SHA,'grid':meta['grid'],
            'plantilla_grid_sha256':hashlib.sha256(Path(grid_meta_path).read_bytes()).hexdigest(),
            'threshold_m':20,'ray_length_m':3000,'detector_distance_m':1000,'detector_height_m':1.5,
            'scope':'interseccion de dos primitivas mediante rayos rectos centrales; no simula muones',
            'views':[]}
    for view in range(6):
        o,d=rays(coords['az_centers_deg'],coords['el_centers_deg'],view)
        lengths=intersection_lengths(o,d,cyl,ell);mask=lengths>=20
        old_o,old_d=rays(np.linspace(-30,30,256),coords['el_centers_deg'],view)
        old_lengths=intersection_lengths(old_o,old_d,cyl,ell);old_mask=old_lengths>=20
        path=output/f'geo-train-06_view{view}_roi.npz'
        np.savez_compressed(path,length_z_m=lengths,roi_z_ge20m=mask,**coords)
        report['views'].append({'view':view,'pixels_new':int(mask.sum()),
                               'pixels_legacy_recomputed':int(old_mask.sum()),
                               'cells_changed':int(np.count_nonzero(mask!=old_mask)),
                               'max_length_m':float(lengths.max()),
                               'roi_npz_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (output/'revision-roi.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--metadatos-malla',required=True,type=Path)
    p.add_argument('--salida',required=True,type=Path)
    a=p.parse_args();print(json.dumps(run(a.metadatos_malla,a.salida),indent=2))

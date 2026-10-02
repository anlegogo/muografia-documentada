"""Conteos descriptivos de una imagen nueva en una ROI candidata compatible.

No infiere transmisión, significación estadística ni tiempo de exposición.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from preparar_imagen_angular_v1 import coordinates


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def analyze(image_path, roi_directory):
    image_path=Path(image_path);roi_directory=Path(roi_directory)
    meta_path=image_path.with_suffix('.meta.json')
    meta=json.loads(meta_path.read_text(encoding='utf-8'))
    roi_meta_path=roi_directory/'revision-roi.json'
    spec=json.loads(roi_meta_path.read_text(encoding='utf-8'))
    if meta.get('geometry_id')!=spec.get('geometry_id'):
        raise ValueError('la imagen y la ROI pertenecen a geometrías diferentes')
    if not meta.get('geometry_sha256') or meta['geometry_sha256']!=spec.get('geometry_sha256'):
        raise ValueError('falta una huella de geometría coincidente; revisar procedencia')
    view=meta.get('view_index')
    if type(view) is not int or not 0<=view<6:
        raise ValueError('vista inválida')
    matches=[v for v in spec['views'] if v['view']==view]
    if len(matches)!=1:raise ValueError('vista ausente o repetida en ROI')
    if image_path.stem!=f"{meta['geometry_id']}_view{view}":
        raise ValueError('nombre de imagen incompatible con metadatos')
    if (meta.get('detector',{}).get('distance_m')!=spec.get('detector_distance_m') or
            meta.get('detector',{}).get('height_m')!=spec.get('detector_height_m')):
        raise ValueError('posición del detector incompatible')
    coords=coordinates(meta);roi_coords=coordinates(spec)
    if any(not np.array_equal(coords[k],roi_coords[k]) for k in coords):
        raise ValueError('mallas incompatibles')
    roi_path=roi_directory/f"{meta['geometry_id']}_view{view}_roi.npz"
    if sha(image_path)!=meta.get('npz_sha256') or sha(roi_path)!=matches[0]['roi_npz_sha256']:
        raise ValueError('huella de archivo incorrecta')
    with np.load(image_path,allow_pickle=False) as image, np.load(roi_path,allow_pickle=False) as roi:
        for k,expected in coords.items():
            if not np.array_equal(image[k],expected) or not np.array_equal(roi[k],expected):
                raise ValueError('coordenadas de matriz incompatibles con metadatos')
        counts=image['counts_ref'];mask=roi['roi_z_ge20m'];length=roi['length_z_m']
        if counts.shape!=(256,256) or counts.dtype!=np.uint32:
            raise ValueError('conteos fuera del contrato uint32 256x256')
        if (mask.shape!=counts.shape or mask.dtype!=np.bool_ or length.shape!=mask.shape
                or not np.all(np.isfinite(length)) or np.any(length<0)
                or spec.get('threshold_m')!=20 or not np.array_equal(mask,length>=20)
                or int(mask.sum())!=matches[0]['pixels_new']):
            raise ValueError('máscara o longitudes incoherentes')
        total=int(counts.sum(dtype=np.uint64));inside=int(counts[mask].sum(dtype=np.uint64))
        if (type(meta.get('detected_in_bins')) is not int or total!=meta['detected_in_bins']
                or type(meta.get('events_transported')) is not int
                or not 0<=total<=meta['events_transported']):
            raise ValueError('conteos y metadatos inconsistentes')
        pixels=int(mask.sum())
    return {'estado':'conteo_descriptivo_ROI_candidata', 'geometry_id':meta['geometry_id'],
            'view_index':view,'pixels_roi':pixels,'counts_total':total,'counts_roi':inside,
            'counts_outside_roi':total-inside,'fraction_of_detected_in_roi':inside/total if total else None,
            'source_sha256':{'image':sha(image_path),'image_meta':sha(meta_path),
                             'roi':sha(roi_path),'roi_meta':sha(roi_meta_path)},
            'limites':'fraccion descriptiva, no transmision ni eficiencia; procedencia de simulacion requiere revision independiente'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('imagen',type=Path);p.add_argument('--regiones',required=True,type=Path)
    p.add_argument('--salida',required=True,type=Path);a=p.parse_args()
    result=analyze(a.imagen,a.regiones)
    with a.salida.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
    print(json.dumps(result,indent=2))

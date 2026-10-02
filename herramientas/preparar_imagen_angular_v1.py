"""Exporta imágenes nuevas con coordenadas explícitas, sin remuestreo ni thinning.

python herramientas/preparar_imagen_angular_v1.py HIST [HIST ...] --salida NUEVA_CARPETA
Solo acepta az-edges-v1. No usar estos NPZ como campaña definitiva sin revisión.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import numpy as np


def coordinates(meta):
    g = meta.get('grid', {})
    expected = {'azimuth_convention':'az-edges-v1', 'n_az':256, 'n_el':256,
                'az_edges_deg':[-30,30], 'az_step_deg':60/256,
                'az_first_center_deg':-29.8828125, 'az_half_deg':30,
                'el_min_deg':2, 'el_max_deg':47,
                'elevation_convention':'legacy-centers-2-47'}
    if any(g.get(k) != v for k,v in expected.items()):
        raise ValueError('malla histórica, desconocida o inconsistente; no mezclar ni relabelar')
    az_edges = np.linspace(-30,30,257)
    el_centers = np.linspace(2,47,256)
    el_edges = np.r_[el_centers[0]-45/510, (el_centers[:-1]+el_centers[1:])/2,
                     el_centers[-1]+45/510]
    return dict(az_edges_deg=az_edges, az_centers_deg=(az_edges[:-1]+az_edges[1:])/2,
                el_edges_deg=el_edges, el_centers_deg=el_centers)


def read_image(hist):
    hist = Path(hist)
    if not hist.name.endswith('_hist.csv'):
        raise ValueError('se requiere un archivo *_hist.csv')
    stem = hist.name[:-9]
    sidecar = hist.with_name(stem+'.meta.json')
    meta = json.loads(sidecar.read_text(encoding='utf-8-sig'))
    if stem != f"{meta.get('geometry_id')}_view{meta.get('view_index')}":
        raise ValueError('nombre de archivo distinto de geometría/vista declaradas')
    provenance = hist.with_name('entradas.sha256')
    if provenance.exists():
        suffix = f"scripts/simulation/geometry_catalog/geometries/{meta['geometry_id']}.json"
        matches = [line.split()[0] for line in provenance.read_text().splitlines()
                   if len(line.split()) == 2 and line.split()[1].replace('\\','/').endswith(suffix)]
        if len(matches)!=1 or not re.fullmatch('[0-9a-f]{64}',matches[0]):
            raise ValueError('manifiesto de entradas sin una huella inequívoca de geometría')
        if meta.get('geometry_sha256', matches[0]) != matches[0]:
            raise ValueError('huellas de geometría contradictorias')
        meta['geometry_sha256']=matches[0]
        meta['geometry_provenance_manifest_sha256']=hashlib.sha256(provenance.read_bytes()).hexdigest()
        entries=[line.split() for line in provenance.read_text().splitlines() if len(line.split())==2]
        def unique_hash(ending):
            found=[h for h,p in entries if p.replace('\\','/').endswith(ending)]
            if len(found)!=1 or not re.fullmatch('[0-9a-f]{64}',found[0]):
                raise ValueError('procedencia incompleta o ambigua: '+ending)
            return found[0]
        meta['binary_sha256']=unique_hash('/muography_sim')
        meta['table_sha256']={name:unique_hash('/tables-az-edges-v1/'+name)
                              for name in ['meta.json','row_weights_30d.txt','p_cdf.txt']}
    coords = coordinates(meta)
    rows = list(csv.reader(hist.read_text(encoding='utf-8-sig').splitlines()))
    if len(rows)!=256 or any(len(r)!=256 for r in rows):
        raise ValueError('dimensiones distintas de 256x256')
    if any(not re.fullmatch(r'[0-9]+',v.strip()) for row in rows for v in row):
        raise ValueError('conteos deben ser enteros no negativos')
    values = [int(v) for row in rows for v in row]
    if max(values) >= 2**32:
        raise ValueError('desbordamiento uint32; no recortar conteos')
    total = sum(values)
    if (type(meta.get('detected_in_bins')) is not int or meta['detected_in_bins']!=total
            or type(meta.get('events_transported')) is not int
            or not 0<=total<=meta['events_transported']):
        raise ValueError('histograma y metadatos no concuerdan')
    return stem, np.array(values,dtype=np.uint32).reshape(256,256), coords, meta, {
        'hist_sha256':hashlib.sha256(hist.read_bytes()).hexdigest(),
        'meta_sha256':hashlib.sha256(sidecar.read_bytes()).hexdigest()}


def export(histograms, destination):
    # Validate the WHOLE input batch before writing: old/new mixtures fail.
    images = [read_image(p) for p in histograms]
    if not images or len({x[0] for x in images})!=len(images):
        raise ValueError('lote vacío o nombres de vista repetidos')
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    report = {'schema':'oe1-image-az-edges-v1',
              'scope':'exportacion sin alterar conteos; no valida fisica ni habilita produccion',
              'images':[]}
    for stem, counts, coords, meta, hashes in images:
        target = destination/(stem+'.npz')
        np.savez_compressed(target, counts_ref=counts, **coords)
        with np.load(target,allow_pickle=False) as z:
            if any(not np.array_equal(z[k],v) for k,v in dict(counts_ref=counts,**coords).items()):
                raise RuntimeError('fallo de relectura NPZ')
        meta['npz_contract']='oe1-image-az-edges-v1: counts_ref uint32 plus explicit angular centers/edges'
        meta['npz_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        meta['source_files']=hashes
        (destination/(stem+'.meta.json')).write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
        report['images'].append(dict(stem=stem,total=int(counts.sum()),
                                     npz_sha256=meta['npz_sha256'],**hashes))
    (destination/'revision-exportacion.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('histogramas',nargs='+',type=Path)
    p.add_argument('--salida',required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(export(a.histogramas,a.salida),indent=2))

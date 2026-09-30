"""Genera 12 primarios sintéticos fijos para cubrir ambos lados de entrada a Z.

Solo biblioteca estándar. No simula transporte ni muestrea la fuente física.
Rechaza otro catálogo y una carpeta de salida existente.
"""
import argparse
import csv
import hashlib
import io
import json
import math
import struct
from pathlib import Path

CATALOG_SHA = 'c8f6c1352af1f7564356cffbd98e26fd6a5881e5ece15a0ab6f2ed60c8ea26ed'
NAME = 'geo-train-06_v0_r10_r201.primarios.csv'
HEADER = 'id,x_m,y_m,z_m,dx,dy,dz,ekin_gev,pdg,charge_e'.split(',')


def primitive_interval(p, d, centre, axes):
    q = [(x-c)/r for x,c,r in zip(p, centre, axes)]
    v = [x/r for x,r in zip(d, axes)]
    a = sum(x*x for x in v)
    b = 2*sum(x*y for x,y in zip(q,v))
    c = sum(x*x for x in q)-1
    disc = b*b-4*a*c
    if a <= 0 or disc <= 0:
        raise ValueError('La trayectoria candidata no atraviesa la primitiva.')
    root = math.sqrt(disc)
    return ((-b-root)/(2*a), (-b+root)/(2*a))


def geometry_check(p, d, cat):
    c,e = [a['params'] for a in cat['anomalies']]
    ci = primitive_interval(p[:2], d[:2], [c['cx_m'],c['cy_m']], [c['radius_m']]*2)
    ei = primitive_interval(p, d, [e['cx_m'],e['cy_m'],e['cz_m']], [e['ax_m'],e['ay_m'],e['az_m']])
    zi = sorted([(c['z0_m']-p[2])/d[2], (c['z1_m']-p[2])/d[2]])
    cylinder = (max(ci[0],zi[0]), min(ci[1],zi[1]))
    lo, hi = max(cylinder[0],ei[0]), min(cylinder[1],ei[1])
    if lo < 0 or hi <= lo:
        raise ValueError('No hay cruce de Z por delante del primario.')
    gap = abs(cylinder[0]-ei[0])
    side = 'desde_conducto' if ei[0] > cylinder[0] else 'desde_elipsoide'
    entry = [x+lo*v for x,v in zip(p,d)]
    exit_point = [x+hi*v for x,v in zip(p,d)]
    return {'lado_entrada_recta':side, 'longitud_recta_Z_m':hi-lo,
            'separacion_entradas_primitivas_m':gap, 'entrada_Z_m':entry, 'salida_Z_m':exit_point}


def build(catalog, out):
    rawcat = catalog.read_bytes()
    if hashlib.sha256(rawcat).hexdigest() != CATALOG_SHA:
        raise ValueError('El catálogo no coincide byte a byte con geo-train-06 de la entrega.')
    if out.exists():
        raise FileExistsError('La carpeta existe; usar una carpeta nueva, sin sobrescribir.')
    cat = json.loads(rawcat)
    records, expected = [], []
    # Las coordenadas son puntos de paso sobre el plano x=20.3 m.
    # Se eligieron geométricamente, sin observar transporte nuevo.
    for wanted, ys in [('desde_conducto',[-16.0,-15.5,-15.0]), ('desde_elipsoide',[-35.0,-30.0,-25.0])]:
        for y in ys:
            for z in [125.0,140.0]:
                impact = [1000.0,0.0,1.5]
                v = [impact[0]-20.3,impact[1]-y,impact[2]-z]
                norm = math.sqrt(sum(t*t for t in v))
                d = [t/norm for t in v]
                hor = math.hypot(d[0],d[1])
                distance = 1809.7/hor
                p = [q-distance*t for q,t in zip(impact,d)]
                g = geometry_check(p,d,cat)
                assert g['lado_entrada_recta'] == wanted
                assert g['longitud_recta_Z_m'] > 20 and g['separacion_entradas_primitivas_m'] > 5
                # Displaced parallel lines are sensitivity checks, not bounds
                # for a stochastic multiple-scattering trajectory.
                probes = []
                normal_y = [-d[1]/hor,d[0]/hor,0.0]
                normal_z = [-d[2]*d[0]/hor,-d[2]*d[1]/hor,hor]
                for dy in [-.05,0,.05]:
                    for dn in [-.05,0,.05]:
                        pp = [p[i]+dy*normal_y[i]+dn*normal_z[i] for i in range(3)]
                        probe = geometry_check(pp,d,cat)
                        assert probe['lado_entrada_recta'] == wanted
                        probes.append(probe['longitud_recta_Z_m'])
                k = len(records)
                records.append([k,*p,*d,10000.0,13,-1])
                expected.append({'id':k,'punto_paso_x20_3_m':[20.3,y,z],**g,
                    'longitudes_9_rectas_desplazadas_min_max_m':[min(probes),max(probes)],
                    'nota_sensibilidad':'9 rectas paralelas desplazadas 0 o ±5 cm por eje transversal; no es cota del transporte.'})
    buf = io.StringIO(newline='')
    writer = csv.writer(buf,lineterminator='\n')
    writer.writerow(HEADER);writer.writerows(records)
    raw = buf.getvalue().encode('utf8')
    fnv = 0xcbf29ce484222325
    for row in records:
        for b in struct.pack('<q7di',int(row[0]),*row[1:8],int(row[8])):
            fnv = ((fnv^b)*0x100000001b3) & ((1<<64)-1)
    side = {'format':'oe1-primarios/1','kind':'sintetico','synthetic':True,
        'geometry_id':'geo-train-06','view_index':0,'base_radius_m':509.7,'start_radius_m':1809.7,
        'case_code':6,'replica':10,'source_seed':None,'n':12,'columns':HEADER,
        'units':{'position':'m, world frame','direction':'unit travel direction',
                 'ekin_gev':'kinetic energy, GeV','pdg':'13 = mu-','charge_e':'elementary charges'},
        'float_format':'Python round-trip text; LF','canon_fnv1a64':f'{fnv:016x}',
        'canon_hash_layout':'FNV-1a-64, little endian int64 id, 7 float64, int32 pdg; sin charge_e',
        'file_sha256':hashlib.sha256(raw).hexdigest(),
        'descripcion':'Complemento técnico R2-01: 6 entradas desde conducto y 6 desde elipsoide; no es muestra del flujo.',
        'generador':'herramientas/preparar_complemento_r2_01.py'}
    design = {'version':'r2-01/1','catalogo_sha256':CATALOG_SHA,'lista_sha256':side['file_sha256'],
        'generador_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'energia_cinetica_GeV':10000,'semillas_transporte':[1026093011,1026093012,1026093013],
        'variantes':['A','B'],'transportes_propuestos':72,
        'estado':'Diseño local; transporte Geant4 pendiente en SC3.',
        'muones':expected}
    out.mkdir(parents=True)
    (out/NAME).write_bytes(raw)
    for name,value in [(NAME+'.meta.json',side),('trayectorias-esperadas.json',design)]:
        (out/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
    files = sorted(out.iterdir())
    (out/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in files),encoding='utf8',newline='\n')
    print(json.dumps({'primarios':12,'transportes_SC3_propuestos':72,'sha256':side['file_sha256'],
                      'geometria':'6 entradas desde cada lado; verificadas 108 rectas de sensibilidad.'},ensure_ascii=False))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalog',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    a=p.parse_args();build(a.catalog,a.out)

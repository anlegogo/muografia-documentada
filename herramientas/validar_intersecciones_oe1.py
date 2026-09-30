"""Cuadratura independiente de las cuatro intersecciones conocidas del catálogo.
Comparación opcional con auditoría JSON de estudiantes; no usa su algoritmo.
"""
import argparse,hashlib,json,math
from pathlib import Path
from datetime import datetime,timezone
from validar_volumen_oe1 import volume

ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries'
CASES=[('geo-test-01',0,1),('geo-train-06',0,1),('geo-train-08',0,2),('geo-train-11',0,1)]

def run(reference=None):
    ref=json.loads(reference.read_text(encoding='utf-8')) if reference else None
    results=[]
    for gid,i,j in CASES:
        source=CAT/(gid+'.json');g=json.loads(source.read_text(encoding='utf-8'))
        a,b=g['anomalies'][i],g['anomalies'][j]
        assert a['kind']=='conduit'
        c=a['params'];e=dict(b['params'])
        if b['kind']=='cavity':
            for axis in ['ax_m','ay_m','az_m']:e[axis]=e['radius_m']
        v1,_=volume(c,e,1e-5);v2,err=volume(c,e,1e-8)
        vc=math.pi*c['radius_m']**2*(c['z1_m']-c['z0_m'])
        vb=4*math.pi*e['ax_m']*e['ay_m']*e['az_m']/3
        assert 0<v2<=min(vc,vb)
        row={'geometria':gid,'indices':[i,j],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'interseccion_m3':v2,'diferencia_tolerancias_m3':abs(v2-v1),'error_estimado_exterior_m3':err,
          'volumen_conducto_m3':vc,'fraccion_conducto_intersectada':v2/vc,
          'densidad_conducto':a['density_g_cm3'],'densidad_prioritaria':b['density_g_cm3']}
        if ref:
            rg=next(x for x in ref['geometries'] if x['geometry_id']==gid)
            rp=next(x for x in rg['pairs'] if x['indices']==[i,j])
            row['estudiantes']={'volumen_m3':rp['volume_m3'],'ee_m3':rp['se_m3'],'diferencia_en_ee':(v2-rp['volume_m3'])/rp['se_m3']}
        results.append(row)
    output={'fecha_utc':datetime.now(timezone.utc).isoformat(),'metodo':'Cuadratura XY independiente de longitud vertical común.',
      'referencia_sha256':hashlib.sha256(reference.read_bytes()).hexdigest() if reference else None,
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'integrador_sha256':hashlib.sha256((ROOT/'herramientas/validar_volumen_oe1.py').read_bytes()).hexdigest(),
      'resultados':results,'limites':'No calcula flujo, opacidad en vistas ni transporte. La fracción de volumen no determina sensibilidad muográfica. No cubre defectos de salida del edificio.'}
    path=ROOT/'objetivo-1/evidencias/intersecciones-independientes.json'
    path.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--referencia',type=Path);a=p.parse_args();run(a.referencia)

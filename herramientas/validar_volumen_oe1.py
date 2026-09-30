"""Control independiente de volumen por cuadratura, sin transporte Geant4.
Requiere NumPy/SciPy; escribe solo evidencia derivada.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,math
import scipy
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries/geo-train-06.json'

def volume(c,e,tol):
    # Integración de la longitud vertical común sobre la intersección XY.
    xmin=max(c['cx_m']-c['radius_m'],e['cx_m']-e['ax_m'])
    xmax=min(c['cx_m']+c['radius_m'],e['cx_m']+e['ax_m'])
    def along_x(x):
        cy=math.sqrt(max(0,c['radius_m']**2-(x-c['cx_m'])**2))
        ex=1-((x-e['cx_m'])/e['ax_m'])**2
        ey=e['ay_m']*math.sqrt(max(0,ex))
        lo=max(c['cy_m']-cy,e['cy_m']-ey); hi=min(c['cy_m']+cy,e['cy_m']+ey)
        if lo>=hi:return 0.
        def along_y(y):
            half=e['az_m']*math.sqrt(max(0,ex-((y-e['cy_m'])/e['ay_m'])**2))
            return max(0,min(c['z1_m'],e['cz_m']+half)-max(c['z0_m'],e['cz_m']-half))
        return quad(along_y,lo,hi,epsabs=tol,epsrel=tol,limit=200)[0]
    return quad(along_x,xmin,xmax,epsabs=tol,epsrel=tol,limit=200)

def main():
    g=json.loads(SOURCE.read_text(encoding='utf-8')); c=g['anomalies'][0]['params']; e=g['anomalies'][1]['params']
    coarse,err1=volume(c,e,1e-5); fine,err2=volume(c,e,1e-8)
    cylinder=math.pi*c['radius_m']**2*(c['z1_m']-c['z0_m'])
    ellipsoid=4*math.pi*e['ax_m']*e['ay_m']*e['az_m']/3
    result={'fecha_utc':datetime.now(timezone.utc).isoformat(),'scipy':scipy.__version__,
      'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'geometria':g['geometry_id'],'metodo':'Cuadratura adaptativa anidada XY de longitud vertical común; sin muestreo Monte Carlo.',
      'interseccion_m3':fine,'interseccion_control_tolerancia_m3':coarse,'diferencia_tolerancias_m3':abs(fine-coarse),
      'estimacion_error_integral_exterior_m3':err2,
      'conducto_completo_m3':cylinder,'conducto_menos_interseccion_m3':cylinder-fine,'cuerpo_denso_m3':ellipsoid,
      'comparacion_reportada':{'interseccion_autores_m3':83641.9,'ee_monte_carlo_autores_m3':44.7,'diferencia_m3':fine-83641.9,
       'conducto_geant4_B_m3':387492.,'ee_geant4_B_m3':90.7,'diferencia_geant4_menos_cuadratura_m3':387492.-(cylinder-fine)},
      'limites':'Dos tolerancias comprueban estabilidad numérica, no constituyen cota rigurosa total. No incluye navegación ni transporte. Supone sólidos alineados del JSON; ambas anomalías están contenidas en el edificio en este caso.'}
    out=ROOT/'objetivo-1/evidencias/volumen-independiente-geo-train-06.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

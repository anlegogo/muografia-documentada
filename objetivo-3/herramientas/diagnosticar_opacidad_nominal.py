"""Diagnóstico geométrico de opacidad nominal en el soporte C2; no inversión."""
import argparse,csv,hashlib,json,sys
from pathlib import Path
import numpy as np

def opacity(rho_rock,rho_anomaly,length_rock_total_m,length_anomaly_m):
 L=np.asarray(length_rock_total_m,dtype=float);a=np.asarray(length_anomaly_m,dtype=float)
 if rho_rock<=0 or rho_anomaly<=0 or np.any(a<0) or np.any(a>L+1e-8):raise ValueError('Dominio físico inválido')
 return 100*(rho_rock*(L-a)+rho_anomaly*a)

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for k in ['repo','data','registry','output']:p.add_argument('--'+k,type=Path,required=True)
 args=p.parse_args();sys.path.insert(0,str(args.repo/'objetivo-2/herramientas'));sys.path.insert(0,str(args.repo/'objetivo-2/implementacion/scripts/evaluation'))
 import evaluacion_final_oe2 as e
 import evaluar_regiones_geometricas as g
 from controles_contraste_v2 import Registry
 spec,signature=e.contract(args.repo);cfg=spec['regional_protocol'];registry=Registry(signature,e.read(args.registry))
 # Casos analíticos dimensionales e identidad: 10 m roca 2.65 = 2650 g/cm².
 for values,expected in [((2.65,2.65,10,4),2650),((2.65,1.,10,4),1990),((2.65,1.,10,0),2650),((2.65,1.,10,10),1000)]:
  assert np.isclose(opacity(*values),expected,atol=1e-10,rtol=0)
 rows=[];sources={};maximum_decomposition_error=0
 for gid in spec['geometry_order']:
  ref,low,coords=e.package(args.data,gid,spec);path=args.repo/spec['geometry_files'][gid];geometry=e.read(path);sources[spec['geometry_files'][gid]]=e.sha(path)
  rho=geometry['edifice']['rock_density_g_cm3']
  for view in range(6):
   origin,direction=g.rays(coords['az_centers_deg'],coords['el_centers_deg'],view,cfg)
   assert np.allclose(np.linalg.norm(direction,axis=-1),1,atol=1e-12,rtol=0)
   L,anomaly_lengths,regions=g.masks(geometry,origin,direction,cfg)
   for index,an in enumerate(geometry['anomalies']):
    name=f"anomalia_{index}_{an['kind']}";mask=regions[name].copy()
    for j,ll in enumerate(anomaly_lengths):
     if j!=index:mask &= ~g.morphology(ll>0,cfg['rock_sky_margin_pixels'],False)
    t,d=registry(mask,regions['roca_sin_anomalia'],L,cfg)
    coverage=len(t)/int(mask.sum()) if mask.any() else 0
    row={'geometry':gid,'view':view,'region':name,'rho_rock_g_cm3':rho,'rho_anomaly_g_cm3':an['density_g_cm3'],'matched_pixels':len(t),'coverage':coverage,'eligible_C2':len(t)>=cfg['min_matched_pixels'] and coverage>=cfg['min_match_fraction']}
    if not len(t):rows.append(row);continue
    # No aplicar una suma ingenua de anomalías superpuestas.
    for j,ll in enumerate(anomaly_lengths):
     assert np.all(ll.ravel()[d]==0),'Donante atraviesa anomalía'
     if j!=index:assert np.all(ll.ravel()[t]==0),'Objetivo atraviesa varias anomalías'
    la=L.ravel()[t];lb=L.ravel()[d];length=anomaly_lengths[index].ravel()[t];ra=an['density_g_cm3']
    # Tabla nominal del JSON. El constructor sustituye rho<0.05 por G4_AIR:
    # conservar el caso y marcarlo, sin inventar una densidad efectiva.
    row['material_override_G4_AIR_in_repository']=bool(ra<.05)
    xa=opacity(rho,ra,la,length);xb=100*rho*lb
    density_term=100*(ra-rho)*float(length.mean());length_term=100*rho*float(la.mean()-lb.mean());difference=float(xa.mean()-xb.mean())
    err=abs(difference-density_term-length_term);maximum_decomposition_error=max(maximum_decomposition_error,err)
    assert err<1e-7
    count_a=float(ref[view].ravel()[t].mean());count_b=float(ref[view].ravel()[d].mean())
    row.update(length_target_m=float(la.mean()),length_control_m=float(lb.mean()),anomaly_length_m=float(length.mean()),X_target_g_cm2=float(xa.mean()),X_control_g_cm2=float(xb.mean()),delta_X_density_g_cm2=density_term,delta_X_control_length_g_cm2=length_term,delta_X_matched_g_cm2=difference,contrast_X_nominal=float(xa.mean()/xb.mean()-1),reference_count_contrast=count_a/count_b-1 if count_b>0 else None,nominal_density_only_sign_changed_by_control=bool(density_term*difference<0))
    rows.append(row)
 assert len(registry.entries)==len(registry.replay['entries'])==54
 args.output.mkdir(parents=True,exist_ok=False)
 with (args.output/'opacidad_nominal.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=sorted(set().union(*(r.keys() for r in rows))));w.writeheader();w.writerows(rows)
 eligible=[r for r in rows if r['eligible_C2']]
 report={'ef01_sha256':signature,'registry_sha256':e.sha(args.registry),'code_sha256':e.sha(Path(__file__)),'geometry_sources':sources,'rows':len(rows),'eligible_rows':len(eligible),'analytic_formula_checks':4,'registry_replay_verified':True,'overlap_excluded_verified':True,'donors_without_anomalies_verified':True,'maximum_opacity_decomposition_residual_g_cm2':maximum_decomposition_error,'eligible_density_term_range_g_cm2':[min(r['delta_X_density_g_cm2'] for r in eligible),max(r['delta_X_density_g_cm2'] for r in eligible)],'eligible_control_changes_sign_of_density_term':sum(r['nominal_density_only_sign_changed_by_control'] for r in eligible),'eligible_material_override_rows':sum(r['material_override_G4_AIR_in_repository'] for r in eligible),'opacity_from_network_reconstructed':False,'transport_calibration_performed':False,'scope':'Opacidad nominal del edificio sobre rayos rectos centrales del JSON; no trayectoria individual de muones, no aire exterior ni inversión de cuentas. Filas rho<0.05 marcadas por sustitución de material: no se presentan como opacidad efectiva Geant4.'}
 e.write(args.output/'resultado.json',report)
 e.write(args.output/'inventario.json',[{'path':f.name,'sha256':e.sha(f),'bytes':f.stat().st_size} for f in sorted(args.output.iterdir())])
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()

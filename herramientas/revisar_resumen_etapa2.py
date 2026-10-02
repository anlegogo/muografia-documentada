"""Audita entrega Git y agregado de etapa 2; NO audita los 48,7 M registros crudos.
Uso: python herramientas/revisar_resumen_etapa2.py ENTREGA REPRODUCCION ROI OUT
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from planificar_etapa2_oe1 import interval

ent, reproduction, mask_path, out = map(Path, sys.argv[1:])
checks=[]; normalizations=[]
def check(name, value): checks.append({'control':name,'ok':bool(value)})
def digest(b): return hashlib.sha256(b).hexdigest()
def read(name): return pd.read_csv(ent/name, keep_default_na=False, float_precision='round_trip')
for line in (ent/'MANIFIESTO.sha256').read_text().splitlines():
    expected,name=line.split(maxsplit=1);p=ent/name.lstrip('*');raw=p.read_bytes()
    ok=digest(raw)==expected
    if not ok and (p.suffix in ('.md','.py','.sh','.sbatch','.status') or p.name=='.gitattributes'):
        ok=digest(raw.replace(b'\r\n',b'\n'))==expected
        if ok: normalizations.append(name)
    check('manifest:'+name,ok)
t=read('analisis/agregado/transiciones-por-bloque.csv')
check('24 replicas', list(t.replica)==list(range(101,125)))
check('N por bloque',(t.N==1000000).all())
check('suma transiciones',(t[['n00','n01','n10','n11']].sum(axis=1)==t.N).all())
counts=[int(t[k].sum()) for k in ('n00','n01','n10','n11')]
result=interval(counts)
reported=json.loads((ent/'analisis/agregado/resultados-etapa2.json').read_text(encoding='utf-8'))
check('intervalo',np.allclose(result['interval95_conservative_per_million'],reported['intervalo_R_int']['interval95_conservative_per_million'],atol=1e-9,rtol=0))
check('categoria',result['decision_numerica']==reported['categoria_de_cierre'])
roi=np.array([[v=='1' for v in line.strip()] for line in mask_path.read_text().splitlines() if line.strip() and not line.startswith('#')],dtype=bool)
sums={v:np.zeros((256,256),dtype=np.int64) for v in ('A','B')}
meta_paths=list((ent/'corridas').rglob('*_view0.meta.json'))
check('55 metadatos',len(meta_paths)==55)
events=0
for p in meta_paths:
    m=json.loads(p.read_text(encoding='utf-8'));events+=m['events_transported']
    h=np.loadtxt(p.with_name(p.name.replace('.meta.json','_hist.csv')),delimiter=',',dtype=np.int64)
    check(str(p.relative_to(ent))+':hist',h.sum()==m['detected_in_bins'])
    check(str(p.relative_to(ent))+':roi',h[roi].sum()==m['oe1_etapa1']['counts']['in_rint'])
    flags=m['oe1_etapa1']['checks']
    check(str(p.relative_to(ent))+':checks',all(v is True or (k=='variant_matches_geometry' and v is None and m['geometry_id']=='geo-train-01') for k,v in flags.items()) and not m['oe1_etapa1']['errors'])
    if m['geometry_id']=='geo-train-06': sums[p.parent.name]+=h
check('48700000 transportes meta',events==48700000)
with np.load(ent/'analisis/agregado/mapas-etapa2.npz') as z:
    for v in ('A','B'): check('suma histogramas mapa '+v,np.array_equal(sums[v],z[v]))
    delta=z['B'].astype(np.int64)-z['A'].astype(np.int64)
    check('23 celdas',np.count_nonzero(delta)==23 and np.abs(delta).max()==1)
    check('ROI 67 70',z['A'][roi].sum()==67 and z['B'][roi].sum()==70)
for name in ('transiciones-por-bloque.csv','cruces-agregado.csv','discordantes-agregado.csv','cambios-pixel-agregado.csv'):
    check('reproduction:'+name,(ent/'analisis/agregado'/name).read_bytes()==(reproduction/name).read_bytes())
cross=read('analisis/agregado/cruces-agregado.csv');disc=read('analisis/agregado/discordantes-agregado.csv');moves=read('analisis/agregado/cambios-pixel-agregado.csv')
check('151 cruces',len(cross)==151 and not cross.duplicated(['replica','id']).any())
check('lados 51 100',dict(cross.A_mat_in.value_counts())=={'A1':100,'A0':51})
check('material B',np.allclose(cross.B_lz_m,cross.B_lz_a1_m,atol=1e-6,rtol=0) and (cross[['B_lz_a0_m','B_lz_rock_m','B_lz_other_m']].abs()<=1e-6).all().all())
check('50 discordancias seleccionadas',len(disc)==50)
check('10 movimientos y 5 internos',len(moves)==10 and ((moves.Y_A==1)&(moves.Y_B==1)).sum()==5)
# Los cambios de detección y de píxel explican el mapa, sin doble contar la ROI.
expected_delta=np.zeros_like(delta)
for row in moves.itertuples():
    expected_delta[row.iel_A,row.iaz_A]-=1;expected_delta[row.iel_B,row.iaz_B]+=1
for row in disc.itertuples():
    if row.estado_A=='DET' and row.estado_B!='DET': expected_delta[row.iel_A,row.iaz_A]-=1
    if row.estado_B=='DET' and row.estado_A!='DET': expected_delta[row.iel_B,row.iaz_B]+=1
check('delta explicado por filas seleccionadas',np.array_equal(delta,expected_delta))
conduit=cross[cross.A_mat_in=='A0'].copy()
conduit['delta_exit']=conduit.B_e_out_gev-conduit.A_e_out_gev
conduit['delta_loss']=(conduit.B_e_in_gev-conduit.B_e_out_gev)-(conduit.A_e_in_gev-conduit.A_e_out_gev)
unlisted=conduit.merge(disc[['replica','id']],on=['replica','id'],how='left',indicator=True)
unlisted=unlisted[unlisted['_merge']=='left_only'].drop(columns='_merge')
output={'fecha':'2026-10-01','alcance':'Entrega Git, histogramas, filas seleccionadas y re-agregación. Sin auditoría íntegra de registros crudos/listas grandes.',
        'checks':checks,'passed':sum(c['ok'] for c in checks),'failed':sum(not c['ok'] for c in checks),'normalizaciones_texto':normalizations,
        'intervalo':result,'energia_51_conducto':{'menor_salida_B':int((conduit.delta_exit < -1e-9).sum()),'mayor_perdida_B':int((conduit.delta_loss>1e-9).sum()),'menor_perdida_B':int((conduit.delta_loss < -1e-9).sum())},
        'cruces_no_incluidos_en_discordancias_seleccionadas':unlisted.to_dict(orient='records')}
out.write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in output.items() if k not in ('checks','cruces_no_incluidos_en_discordancias_seleccionadas')},ensure_ascii=False))
if output['failed']: print([c for c in checks if not c['ok']])
sys.exit(bool(output['failed']))

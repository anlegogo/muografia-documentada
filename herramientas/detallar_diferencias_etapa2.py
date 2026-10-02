"""Extrae valores de las diferencias fuera de Z tras auditar_crudos_etapa2.py.
Uso: python herramientas/detallar_diferencias_etapa2.py CARPETA_AUDITORIA
"""
from pathlib import Path
import json,sys,pandas as pd
root=Path(sys.argv[1])
data=json.loads((root/'auditoria-completa.json').read_text(encoding='utf-8'))
rows=[r for r in data['changed_rows'] if not r['crossed_union']]
details=[]
for rep in sorted({r['replica'] for r in rows}):
    targets={r['id']:r for r in rows if r['replica']==rep}
    group='m1-intento-01' if rep<=112 else 'm2-intento-01'
    cols=sorted({'id','crossed','status','detected','in_rint','iel','iaz','rng0','rng1'}|{c for r in targets.values() for c in r['fields']})
    frames={}
    for v in ['A','B']:
        path=root/group/'geo-train-06'/f'r{rep}'/v/'geo-train-06_view0_muones.csv'
        parts=[]
        for t in pd.read_csv(path,usecols=cols,chunksize=100000,float_precision='round_trip',keep_default_na=False):
            s=t[t.id.isin(targets)]
            if len(s):parts.append(s)
        frames[v]=pd.concat(parts).set_index('id')
    for ident,r in targets.items():
        a=frames['A'].loc[ident];b=frames['B'].loc[ident]
        changes={}
        for c in r['fields']:
            x,y=a[c],b[c]
            if hasattr(x,'item'):x=x.item()
            if hasattr(y,'item'):y=y.item()
            changes[c]={'A':x,'B':y}
            if isinstance(x,(float,int)) and isinstance(y,(float,int)):changes[c]['B_minus_A']=y-x
        details.append({'replica':rep,'id':ident,'status_A':a.status,'status_B':b.status,'fields':changes})
summary={'all_fields_changed':sum(b['all_fields_changed'] for b in data['blocks'] if b['case']=='geo-train-06'),
         'selected_changed':sum(b['selected_changed'] for b in data['blocks'] if b['case']=='geo-train-06'),
         'outside_Z_changed':sum(b['outside_Z_changed'] for b in data['blocks'] if b['case']=='geo-train-06'),
         'outside_Z_details':details}
(root/'diferencias-fuera-Z.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(summary,ensure_ascii=False))

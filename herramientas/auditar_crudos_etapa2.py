"""Auditoría independiente completa OE1 etapa 2 (sin ejecutar Geant4).

python herramientas/auditar_crudos_etapa2.py ENTREGA DATOS_GZ ROI SALIDA_NUEVA
Requiere numpy, pandas, scipy. Conserva CSV descomprimidos en SALIDA_NUEVA.
"""
import gzip, hashlib, json, re, shutil, sys
from pathlib import Path
import numpy as np
import pandas as pd
from revisar_etapa1_oe1 import primary_hashes
from planificar_etapa2_oe1 import interval

ent, data, mask, out = map(Path, sys.argv[1:])
out.mkdir(parents=True,exist_ok=False)
checks=[]; blocks=[]; changed_rows=[]; cross_rows=[]
def check(name, ok):
    checks.append({'control':name,'ok':bool(ok)})
    if not ok: print('FAIL',name,flush=True)
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def shas(p):return {Path(line.split(maxsplit=1)[1].lstrip('*')).name:line.split()[0] for line in p.read_text().splitlines() if line.strip()}
expected=shas(ent/'datos-compartidos/SHA256SUMS.txt')
for name,digest in expected.items():check('descarga:'+name,sha(data/name)==digest)
assert all(c['ok'] for c in checks),'No analizar archivos con integridad incorrecta'
lists=out/'listas';lists.mkdir()
frozen=shas(ent/'preparacion/listas-congeladas/listas.sha256')
def unzip(src,dest,expected_sha):
    dest.parent.mkdir(parents=True,exist_ok=True)
    h=hashlib.sha256()
    with gzip.open(src,'rb') as f,dest.open('wb') as g:
        while b:=f.read(4*1024*1024):h.update(b);g.write(b)
    check('csv:'+dest.name,h.hexdigest()==expected_sha)
for p in sorted(data.glob('*.primarios.csv.gz')):
    name=p.name.removeprefix('i01-').removesuffix('.gz')
    unzip(p,lists/name,frozen[name])
    shutil.copyfile(ent/'preparacion/listas-congeladas/sidecars'/(name+'.meta.json'),lists/(name+'.meta.json'))
roi=np.array([[c=='1' for c in line.strip()] for line in mask.read_text().splitlines() if line.strip() and not line.startswith('#')])
maps={v:np.zeros((256,256),dtype=np.int64) for v in ('A','B')}
selected=['detected','status','iel','iaz','in_rint','rng1']
published_blocks=pd.read_csv(ent/'analisis/agregado/transiciones-por-bloque.csv').set_index('replica')
def chunks(path):return pd.read_csv(path,chunksize=100000,keep_default_na=False,float_precision='round_trip',dtype={'prim_fnv':str,'rng0':str,'rng1':str})
for case,reps in [('geo-train-01',range(201,204)),('geo-train-06',range(101,125))]:
    for rep in reps:
        group='controles-intento-01' if case.endswith('01') else ('m1-intento-01' if rep<=112 else 'm2-intento-01')
        root=ent/'corridas'/group/'intento'/case/f'r{rep}'
        n=100000 if case.endswith('01') else 1000000
        lp=next(lists.glob(f'{case}_v0_r{rep}_*.primarios.csv'))
        lsha=sha(lp); paths={}; hist={v:np.zeros((256,256),dtype=np.int64) for v in ('A','B')}
        for v in ('A','B'):
            rawname=f'{case}_view0_muones.csv';paths[v]=out/group/case/f'r{rep}'/v/rawname
            unzip(data/f'i01-{case}-r{rep}-{v}-muones.csv.gz',paths[v],shas(root/v/'SHA256SUMS')[rawname])
        totals=np.zeros(4,dtype=np.int64);detect=np.zeros(4,dtype=np.int64);offset=0
        fields={}; rngs={v:[] for v in ('A','B')}; fnvs=[]; anyfull=0; outside=0; anyselected=0
        ci=0; cb=0; unioncount=0; pixel=0
        for initial,a,b in zip(chunks(lp),chunks(paths['A']),chunks(paths['B']),strict=True):
            ident=f'{case}/r{rep}/chunk{offset}'
            for t in (initial,a,b): check(ident+':IDs',np.array_equal(t.id,np.arange(offset,offset+len(initial))))
            check(ident+':primary_finite',np.isfinite(initial[['x_m','y_m','z_m','dx','dy','dz','ekin_gev']].to_numpy()).all() and (initial.ekin_gev>0).all())
            check(ident+':primary_direction',np.allclose(np.linalg.norm(initial[['dx','dy','dz']].to_numpy(),axis=1),1,rtol=0,atol=1e-12))
            check(ident+':muon_species',(initial.pdg.abs()==13).all())
            check(ident+':charge',np.array_equal(initial.charge_e,-np.sign(initial.pdg)))
            ph=primary_hashes(initial);fnvs.extend(ph.tolist())
            aa={}; dd={}
            for v,t in [('A',a),('B',b)]:
                check(ident+v+':FNV',np.array_equal(t.prim_fnv,ph))
                check(ident+v+':list_sha',(t.list_sha256==lsha).all())
                check(ident+v+':variant',(t.variant==v).all())
                check(ident+v+':case_replica',(t.geometry_id==case).all() and (t.replica==rep).all())
                check(ident+v+':no_aborted',not (t.status=='ABORTED').any())
                check(ident+v+':known_status',t.status.isin(['DET','DECAY','MU_CAPTURE','OTHER','PLANE_OUT','STOPPED','WORLD_EXIT']).all())
                dd[v]=(t.status=='DET').to_numpy()
                check(ident+v+':detected',np.array_equal(dd[v],t.detected==1))
                ix=t.iel.to_numpy();iy=t.iaz.to_numpy()
                check(ident+v+':indices',((ix[dd[v]]>=0)&(ix[dd[v]]<256)&(iy[dd[v]]>=0)&(iy[dd[v]]<256)).all())
                aa[v]=np.zeros(len(t),dtype=bool);aa[v][dd[v]]=roi[ix[dd[v]],iy[dd[v]]]
                check(ident+v+':ROI',np.array_equal(aa[v],t.in_rint==1))
                np.add.at(hist[v],(ix[dd[v]],iy[dd[v]]),1)
                rngs[v].extend(t.rng0.tolist())
            check(ident+':rng0',np.array_equal(a.rng0,b.rng0))
            totals+=np.bincount(aa['A'].astype(int)*2+aa['B'].astype(int),minlength=4)
            detect+=np.bincount(dd['A'].astype(int)*2+dd['B'].astype(int),minlength=4)
            union=(a.crossed.to_numpy()==1)|(b.crossed.to_numpy()==1)
            ci+=int((a.crossed==1).sum());cb+=int((b.crossed==1).sum());unioncount+=int(union.sum())
            if case.endswith('06'):
                check(ident+':B_material',np.allclose(b.loc[b.crossed==1,'lz_m'],b.loc[b.crossed==1,'lz_a1_m'],atol=1e-6,rtol=0) and (b.loc[b.crossed==1,['lz_a0_m','lz_rock_m','lz_other_m']].abs()<=1e-6).all().all())
            allchange=np.zeros(len(a),dtype=bool);selchange=np.zeros(len(a),dtype=bool)
            for col in a.columns:
                if col=='variant':continue
                diff=a[col].to_numpy()!=b[col].to_numpy();fields[col]=fields.get(col,0)+int(diff.sum());allchange|=diff
                if col in selected:selchange|=diff
            anyfull+=int(allchange.sum());anyselected+=int(selchange.sum());outside+=int((allchange&~union).sum())
            moved=dd['A']&dd['B']&((a.iel.to_numpy()!=b.iel.to_numpy())|(a.iaz.to_numpy()!=b.iaz.to_numpy()));pixel+=int(moved.sum())
            for k in np.flatnonzero(allchange):
                if len(changed_rows)<5000:
                    changed_rows.append({'case':case,'replica':rep,'id':int(a.id.iloc[k]),'crossed_union':bool(union[k]),'selected_discordance':bool(selchange[k]),'fields':[c for c in a.columns if c!='variant' and a[c].iloc[k]!=b[c].iloc[k]]})
            for k in np.flatnonzero(union):
                row={'replica':rep,'id':int(a.id.iloc[k])}
                for v,t in [('A',a),('B',b)]:
                    for c in ['mat_in','lz_m','lz_a0_m','lz_a1_m','e_in_gev','e_out_gev','status','detected','iel','iaz','in_rint']:row[v+'_'+c]=t[c].iloc[k].item() if hasattr(t[c].iloc[k],'item') else t[c].iloc[k]
                cross_rows.append(row)
            offset+=len(initial)
        check(f'{case}/{rep}:N',offset==n)
        check(f'{case}/{rep}:uniqueFNV',len(set(fnvs))==n)
        for v in ('A','B'):
            check(f'{case}/{rep}/{v}:rng0_unique',len(set(rngs[v]))==n and '0000000000000000' not in rngs[v])
            expectedhist=np.loadtxt(root/v/f'{case}_view0_hist.csv',delimiter=',',dtype=np.int64)
            check(f'{case}/{rep}/{v}:hist_all',np.array_equal(hist[v],expectedhist))
            if case.endswith('06'):maps[v]+=hist[v]
        if case.endswith('01'):check(f'{case}/{rep}:control_all_fields',anyfull==0)
        if rep==201:
            rawname=f'{case}_view0_muones.csv';p=out/group/case/f'r{rep}'/'AA'/rawname
            unzip(data/f'i01-{case}-r{rep}-AA-muones.csv.gz',p,shas(root/'AA'/'SHA256SUMS')[rawname])
            check('AA raw byte identity',sha(p)==sha(paths['A']))
        summary={'case':case,'replica':rep,'N':n,'transitions':totals.tolist(),'detection':detect.tolist(),'all_fields_changed':anyfull,'selected_changed':anyselected,'outside_Z_changed':outside,'changed_field_counts':fields,'crossed_A':ci,'crossed_B':cb,'crossed_union':unioncount,'pixel_changes':pixel}
        blocks.append(summary);print(json.dumps({k:v for k,v in summary.items() if k!='changed_field_counts'}),flush=True)
        if case.endswith('06'):
            row=published_blocks.loc[rep]
            check(f'published/r{rep}:transitions',totals.tolist()==[int(row[c]) for c in ('n00','n01','n10','n11')])
            check(f'published/r{rep}:crossings',unioncount==int(row.cruces_union))
            check(f'published/r{rep}:pixels',pixel==int(row.cambian_pixel))
        (out/'progress.json').write_text(json.dumps({'blocks':blocks,'checks_failed':[c for c in checks if not c['ok']]},indent=2))
main=[b for b in blocks if b['case']=='geo-train-06']
counts=np.sum([b['transitions'] for b in main],axis=0).tolist()
published=json.loads((ent/'analisis/agregado/resultados-etapa2.json').read_text(encoding='utf-8'))
check('aggregate transitions',counts==[published['totales'][k] for k in ['n00','n01','n10','n11']])
with np.load(ent/'analisis/agregado/mapas-etapa2.npz') as z:
    for v in ('A','B'):check('aggregate map '+v,np.array_equal(maps[v],z[v]))
result={'fecha':'2026-10-01','scope':'85 compressed files hashed, 27 primary lists and 55 complete logs hashed after decompression; all primary and event rows audited independently in chunks', 'checks':checks,'passed':sum(c['ok'] for c in checks),'failed':sum(not c['ok'] for c in checks),'blocks':blocks,'interval':interval(counts),'changed_rows_limit':5000,'changed_rows':changed_rows,'cross_rows':cross_rows}
(out/'auditoria-completa.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('COMPLETE',result['passed'],result['failed'],flush=True)
sys.exit(bool(result['failed']))

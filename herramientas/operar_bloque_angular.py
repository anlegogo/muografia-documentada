"""Ejecuta una fila en un intento aislado y publica solo tras validación estricta.

Por defecto describe el comando. --ejecutar consume transporte: usar solo con
el alcance científico acordado. No envía trabajos, reintenta ni sobreescribe.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import uuid
from fusionar_bloques_angular import manifest_rows, validate_block
from diagnosticar_observable_angular import matrix
from publicar_bloque_angular import publish, inventory, RECEIPT


def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative_block(row):
    return Path(row['geometria'])/f"view{row['vista']}"/f"block{row['bloque']:04d}"


def existing(manifest,row,destination):
    target=Path(destination)/relative_block(row)
    if not target.exists(): return False
    validate_block(row,destination)
    receipt=json.loads((target/RECEIPT).read_text(encoding='utf-8'))
    if receipt['row']!=row or receipt['manifest_sha256']!=digest(manifest) or receipt['files']!=inventory(target,True):
        raise ValueError('bloque existente distinto: no se omite ni sobrescribe')
    return True


def prepare(manifest,row_id,tree,scratch,destination,recipe,threads):
    rows=manifest_rows(manifest);selected=[r for r in rows if r['fila']==row_id]
    if len(selected)!=1 or type(threads) is not int or threads<1:raise ValueError('fila/threads inválidos')
    row=selected[0];tree=Path(tree).resolve();scratch=Path(scratch).resolve();destination=Path(destination).resolve()
    if scratch.is_relative_to(destination) or destination.is_relative_to(scratch):
        raise ValueError('temporal y publicación requieren raíces separadas')
    definition=json.loads(Path(recipe).read_text(encoding='utf-8'))
    for name,expected in definition.get('runtime_tool_sha256',{}).items():
        if Path(name).name!=name or digest(Path(__file__).with_name(name))!=expected:
            raise ValueError('herramienta distinta de ficha: '+name)
    binary=tree/'build-receta/muography_sim';tables=tree/'scripts/simulation/geant4_app/tables-az-edges-v1'
    geo=tree/'scripts/simulation/geometry_catalog/geometries'/(row['geometria']+'.json')
    inputs={binary:definition['reported_binary_sha256'],geo:definition['geometry_sha256'][geo.name],
            tree/'controles-oe1-v3.patch':definition['patch_sha256']}
    inputs.update({tables/n:h for n,h in definition['table_sha256'].items()})
    for path,expected in inputs.items():
        if digest(path)!=expected:raise ValueError('entrada distinta de ficha: '+str(path))
    controls=definition['oe1_controles']
    expected={'inject':'cone','plane_half_m':300,'edifice_margin_m':50,'margin_deg':5,'ecuts_gev':[3],'subplanes_half_m':[]}
    if controls!=expected:raise ValueError('worker limitado a la receta cone/5deg/600m/E>3')
    attempt=scratch/('intento-'+uuid.uuid4().hex);directory=attempt/relative_block(row)
    command=[str(binary),'--geometry',str(geo),'--view',str(row['vista']),'--tables',str(tables),
             '--seed',str(row['semilla']),'--events',str(row['eventos']),'--threads',str(threads),'--out',str(directory)]
    return row,definition,inputs,attempt,directory,command


def finalize(directory,row,definition=None):
    """Promoción local del corte; conserva histograma y metadatos sin modificar originales."""
    stem=f"{row['geometria']}_view{row['vista']}"
    hist=directory/(stem+'_hist.csv');cut=directory/(stem+'_hist_ecut3.csv');meta=directory/(stem+'.meta.json')
    full=matrix(hist);selected=matrix(cut);m=json.loads(meta.read_text(encoding='utf-8'))
    if (selected>full).any() or int(full.sum())!=m['detected_in_bins']:
        raise ValueError('corte o conteos incoherentes')
    (directory/(stem+'.raw.meta.json')).write_bytes(meta.read_bytes())
    hist.rename(directory/(stem+'_hist_sin_corte.csv'));cut.rename(hist)
    m['detected_all_energies']=m['detected_in_bins'];m['detected_in_bins']=int(selected.sum())
    m['reference_histogram']='kinetic energy at the counting plane > 3 GeV'
    if definition is not None:
        gen=matrix(directory/(stem+'_gen.csv'))
        nominal=int(gen.sum())
        if nominal>row['eventos']:raise ValueError('generación nominal incoherente')
        m['source_definition']=definition['source_definition']
        m['normalization']=definition['normalization']
        m['nominal_in_window']=nominal
        m['conventional_exposure_days']=30*nominal/definition['normalization']['S0_30_conventional_days']
    meta.write_bytes((json.dumps(m,indent=2)+'\n').encode())
    (directory/'salida.sha256').write_bytes(('\n'.join(digest(p)+'  '+p.name for p in (hist,meta))+'\n').encode())


def _run(manifest,row_id,tree,scratch,destination,recipe,threads=24,execute=False):
    row,definition,inputs,attempt,directory,command=prepare(manifest,row_id,tree,scratch,destination,recipe,threads)
    if existing(manifest,row,destination):return {'status':'already_verified','row':row}
    if not execute:return {'status':'dry_run','row':row,'command':command,'physical_validation':False}
    directory.mkdir(parents=True,exist_ok=False)
    phase='prepared'
    try:
        (directory/'entradas.sha256').write_bytes(('\n'.join(h+'  '+p.relative_to(Path(tree).resolve()).as_posix() for p,h in inputs.items())+'\n').encode())
        (directory/'comando.json').write_text(json.dumps(command,indent=2),encoding='utf-8')
        env={k:v for k,v in os.environ.items() if not k.startswith('OE1C_')}
        env.update(OE1C_INJECT='cone',OE1C_MARGIN_DEG='5',OE1C_PLANE_HALF_M='300',OE1C_ECUTS_GEV='3',OE1C_EDIFICE_MARGIN_M='50',OE1C_GEN_HIST='1')
        (directory/'receta.env').write_text('\n'.join(k+'='+v for k,v in sorted(env.items()) if k.startswith('OE1C_'))+'\n')
        (directory/'operacion.json').write_text(json.dumps({'manifest_sha256':digest(manifest),'recipe_sha256':digest(recipe),'worker_sha256':digest(__file__),'threads':threads,'slurm_job_id':env.get('SLURM_JOB_ID'),'definition_status':definition['status']},indent=2))
        phase='simulation'
        with (directory/'run.log').open('wb') as log:
            result=subprocess.run(command,cwd=tree,env=env,stdout=log,stderr=subprocess.STDOUT,check=False)
        if result.returncode:raise RuntimeError('simulador terminó con código '+str(result.returncode))
        if any(digest(p)!=h for p,h in inputs.items()):raise ValueError('entrada cambió durante ejecución')
        phase='finalization';finalize(directory,row,definition)
        (directory/'exit_code.txt').write_text('0\n')
        phase='validation';validate_block(row,attempt)
        phase='publication';receipt=publish(manifest,row_id,attempt,destination)
        return {'status':receipt['status'],'attempt':str(attempt),'receipt':receipt}
    except Exception as exc:
        (directory/'exit_code.txt').write_text('1\n')
        (directory/'fallo.json').write_text(json.dumps({'phase':phase,'error':str(exc)},indent=2),encoding='utf-8')
        raise


def run(manifest,row_id,tree,scratch,destination,recipe,threads=24,execute=False):
    if not execute:return _run(manifest,row_id,tree,scratch,destination,recipe,threads,False)
    selected=[r for r in manifest_rows(manifest) if r['fila']==row_id]
    if len(selected)!=1:raise ValueError('fila inválida')
    row=selected[0];dest=Path(destination).resolve()
    state=dest.parent/(dest.name+'.operacion');state.mkdir(parents=True,exist_ok=True)
    lock=state/(f"{row['geometria']}-{row['vista']}-{row['bloque']}.worker.lock")
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
    try:return _run(manifest,row_id,tree,scratch,destination,recipe,threads,True)
    finally:lock.unlink()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('manifiesto','arbol','temporal','salida','receta'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--fila',type=int,required=True);p.add_argument('--threads',type=int,default=24)
    p.add_argument('--sha-manifiesto');p.add_argument('--sha-receta')
    p.add_argument('--ejecutar',action='store_true');a=p.parse_args()
    if a.sha_manifiesto and digest(a.manifiesto)!=a.sha_manifiesto:raise ValueError('manifiesto cambió después del envío')
    if a.sha_receta and digest(a.receta)!=a.sha_receta:raise ValueError('receta cambió después del envío')
    print(json.dumps(run(a.manifiesto,a.fila,a.arbol,a.temporal,a.salida,a.receta,a.threads,a.ejecutar),indent=2))

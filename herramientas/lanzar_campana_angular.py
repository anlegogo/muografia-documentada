"""Lanzador de una pasada, con identidad de campaña, recibos y registro de envíos.

Por defecto consulta la cola y muestra; --enviar llama sbatch. Nunca se encadena
ni reintenta una fila registrada. Una respuesta ambigua exige conciliación manual.
"""
import argparse
import getpass
import hashlib
import json
import os
from pathlib import Path
import subprocess
from fusionar_bloques_angular import manifest_rows
from operar_bloque_angular import existing, digest, prepare


def launch(manifest,tree,scratch,destination,recipe,python,threads=24,max_jobs=4,submit=False,partition='legacy',time_limit='00:55:00',memory=None):
    if threads<1 or max_jobs<1:raise ValueError('recursos inválidos')
    # Partition, wall-time limit and memory are scheduling options; they are recorded in
    # each planned command but kept out of the campaign identity, so earlier roots stay valid.
    if not partition.replace('_','').isalnum() or not all(x.isdigit() for x in time_limit.replace('-',':').split(':')):
        raise ValueError('partición/tiempo inválidos')
    if memory is not None and not (memory[:-1].isdigit() and memory[-1] in 'MG'):
        raise ValueError('memoria inválida')
    manifest,tree,scratch,destination,recipe,python=map(lambda p:Path(p).resolve(),(manifest,tree,scratch,destination,recipe,python))
    rows=manifest_rows(manifest)
    script=Path(__file__).resolve().with_name('bloque_verificado_angular.sbatch')
    worker=script.with_name('operar_bloque_angular.py')
    identity={'manifest':digest(manifest),'recipe':digest(recipe),'worker':digest(worker),'sbatch':digest(script),
              'destination':str(destination),'tree':str(tree),'scratch':str(scratch),'python':str(python),'threads':threads}
    cid=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    # The same publication root has one owner/configuration, even across different manifests.
    state=destination.parent/(destination.name+'.operacion');state.mkdir(parents=True,exist_ok=True)
    lock=state/'launcher.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
    try:
        owner=state/'campaign.json'
        if owner.exists() and json.loads(owner.read_text())!={'id':cid,'identity':identity}:
            raise ValueError('raíz de publicación vinculada a otra campaña/configuración')
        q=subprocess.run(['squeue','-h','-u',getpass.getuser(),'-o','%i|%j'],capture_output=True,text=True,check=True)
        jobs=[x.split('|') for x in q.stdout.splitlines() if x.strip()]
        if any(len(x)!=2 for x in jobs):raise ValueError('respuesta de cola ilegible')
        queued={x[1].strip() for x in jobs};free=max(0,max_jobs-len(jobs))
        planned=[];blocked=[];verified=[]
        for row in rows:
            if existing(manifest,row,destination):verified.append(row['fila']);continue
            name=f"oe1-{cid[:12]}-{row['fila']}";record=state/(str(row['fila'])+'.json')
            if name in queued:continue
            if record.exists():blocked.append(row['fila']);continue
            if len(planned)>=free:continue
            prepare(manifest,row['fila'],tree,scratch,destination,recipe,threads)
            logdir=state/'logs'
            cmd=['sbatch','--parsable','--job-name='+name,'--partition='+partition,'--nodes=1','--ntasks=1',
                 '--cpus-per-task='+str(threads),'--time='+time_limit]+(['--mem='+memory] if memory else [])+['--chdir='+str(tree),
                 '--output='+str(logdir/'%x-%j.out'),str(script),str(manifest),str(row['fila']),str(tree),str(scratch),str(destination),str(recipe),str(python),str(threads),str(worker),identity['manifest'],identity['recipe']]
            planned.append({'row':row['fila'],'command':cmd,'record':str(record)})
        # Validate all selected commands before the first submission.
        if submit:
            if not owner.exists():
                with owner.open('x') as f:json.dump({'id':cid,'identity':identity},f,indent=2)
            (state/'logs').mkdir(exist_ok=True)
            for item in planned:
                record=Path(item['record'])
                with record.open('x') as f:json.dump(dict(item,status='intent_before_submission'),f,indent=2)
                result=subprocess.run(item['command'],capture_output=True,text=True,check=True)
                job=result.stdout.strip().split(';')[0]
                if not job.isdigit():raise ValueError('sbatch ambiguo: conservar registro y consultar SC3')
                # On write failure the intent remains; no automatic second submission.
                temp=record.with_suffix('.submitted.tmp')
                with temp.open('x') as f:json.dump(dict(item,status='submitted',job_id=job),f,indent=2)
                temp.replace(record)
        return {'campaign_id':cid,'submitted':submit,'planned':planned,'blocked_prior_attempts':blocked,'verified':verified,'queue_jobs':len(jobs),'free_slots':free,'physical_validation':False}
    finally:lock.unlink()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('manifiesto','arbol','temporal','salida','receta','python'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--threads',type=int,default=24);p.add_argument('--max-trabajos',type=int,default=4)
    p.add_argument('--particion',default='legacy');p.add_argument('--tiempo',default='00:55:00')
    p.add_argument('--memoria',help='memoria por trabajo, p. ej. 8G; por defecto la de la partición')
    p.add_argument('--enviar',action='store_true');a=p.parse_args()
    print(json.dumps(launch(a.manifiesto,a.arbol,a.temporal,a.salida,a.receta,a.python,a.threads,a.max_trabajos,a.enviar,a.particion,a.tiempo,a.memoria),indent=2))

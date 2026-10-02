"""Publica un bloque ya generado tras verificar copia e integridad.

No ejecuta simulación ni envía trabajos. Conserva entradas y no sustituye bloques.
Requiere raíces de origen y destino separadas con geo/view/block debajo.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import uuid
from fusionar_bloques_angular import manifest_rows, validate_block

RECEIPT='publicacion-verificada.json'


def inventory(directory, ignore_receipt=False):
    result={}
    for p in sorted(directory.iterdir()):
        if ignore_receipt and p.name==RECEIPT:continue
        if p.is_symlink() or p.is_junction() or not p.is_file():
            raise ValueError('el bloque debe contener archivos regulares, sin enlaces ni subdirectorios')
        result[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def publish(manifest,row_id,source,destination,accept_crlf=False):
    rows=manifest_rows(manifest);selected=[r for r in rows if r['fila']==row_id]
    if len(selected)!=1:raise ValueError('fila inexistente o ambigua')
    r=selected[0];source=Path(source).resolve();destination=Path(destination).resolve()
    if source.is_relative_to(destination) or destination.is_relative_to(source):
        raise ValueError('origen y destino deben ser raíces separadas, no anidadas')
    block=validate_block(r,source,accept_crlf)
    files=inventory(block['directory'])
    if RECEIPT in files:raise ValueError('el origen ya incluye un recibo de publicación')
    relative=Path(r['geometria'])/f"view{r['vista']}"/f"block{r['bloque']:04d}"
    target=destination/relative
    # Reject redirected destination components before any write.
    for p in [destination,*[destination/Path(*relative.parts[:i]) for i in range(1,len(relative.parts)+1)]]:
        if p.is_symlink() or p.is_junction():raise ValueError('destino redirigido')
    target.parent.mkdir(parents=True,exist_ok=True)
    lock=target.with_name(target.name+'.publication.lock');token=uuid.uuid4().hex
    fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f:f.write(token)
    try:
        manifest_hash=hashlib.sha256(Path(manifest).read_bytes()).hexdigest()
        if target.exists():
            validate_block(r,destination,accept_crlf)
            receipt=json.loads((target/RECEIPT).read_text(encoding='utf-8'))
            if (receipt.get('manifest_sha256')!=manifest_hash or receipt.get('row')!=r
                or receipt.get('files')!=files or inventory(target,True)!=files):
                raise ValueError('destino existente distinto; se preserva sin sobrescribir')
            return dict(receipt,status='already_verified')
        # Unique staging root on the same destination filesystem.
        stage=target.parent/('.publication-stage-'+token)
        staged=stage/relative
        staged.mkdir(parents=True,exist_ok=False)
        for name in files:shutil.copyfile(block['directory']/name,staged/name)
        if inventory(staged)!=files or inventory(block['directory'])!=files:
            raise ValueError('la copia o el origen cambió durante la publicación')
        validate_block(r,stage,accept_crlf)
        receipt={'schema':'oe1-verified-publication-v1','status':'published','physical_validation':False,
                 'manifest_sha256':manifest_hash,'row':r,'files':files,
                 'accept_crlf':accept_crlf,'output_hash_checks':block['hashes']}
        (staged/RECEIPT).write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
        # Recheck after writing the receipt, immediately before promotion.
        if inventory(staged,True)!=files:raise ValueError('cambio antes de promover el bloque')
        if target.exists():raise FileExistsError(target)
        staged.rename(target)
        # Only remove now-empty directories, never recursively delete staging data.
        for p in [staged.parent,staged.parent.parent,stage]:
            try:p.rmdir()
            except OSError:pass
        return receipt
    finally:
        if lock.exists() and lock.read_text()==token:lock.unlink()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifiesto',type=Path,required=True);p.add_argument('--fila',type=int,required=True)
    p.add_argument('--origen',type=Path,required=True);p.add_argument('--destino',type=Path,required=True)
    p.add_argument('--aceptar-crlf',action='store_true');a=p.parse_args()
    print(json.dumps(publish(a.manifiesto,a.fila,a.origen,a.destino,a.aceptar_crlf),indent=2))

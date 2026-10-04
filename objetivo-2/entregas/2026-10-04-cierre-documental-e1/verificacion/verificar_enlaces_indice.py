"""Comprueba sin sesión iniciada que los enlaces de Drive del índice de artefactos E1 entregan el archivo binario.

Uso: python verificar_enlaces_indice.py --indice objetivo-2/INDICE_ARTEFACTOS_E1.md --ids ids-drive-e1.json --salida acceso.json
Descarga solo los primeros 1024 bytes de cada enlace; las huellas completas ya constan en la entrega 804ce85.
"""
import argparse, datetime, json, re, urllib.request
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
for n in ['indice', 'ids', 'salida']:
    p.add_argument('--' + n, type=Path, required=True)
a = p.parse_args()
txt = a.indice.read_text(encoding='utf-8')
filas = re.findall(r'\| (B\d) \| (\d+) \| (C\d) \| \[([^\]]+)\]\(https://drive.google.com/file/d/([^/]+)/view\) \| (\d+) \| `([0-9a-f]{64})` \|', txt)
ids = json.loads(a.ids.read_text(encoding='utf-8'))
out = []
for par, semilla, rama, nombre, fid, tam, sha in filas:
    ruta = f'{par}/piloto/{rama}/{nombre}'
    req = urllib.request.Request(f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t', headers={'Range': 'bytes=0-1023'})
    with urllib.request.urlopen(req, timeout=120) as r:
        cab = r.read(1024); estado = r.status
    html = cab.lstrip().lower().startswith(b'<!doctype') or b'<html' in cab[:200].lower()
    firma = 'zip (.pt)' if cab[:2] == b'PK' else ('npy' if cab[:6] == b'\x93NUMPY' else cab[:8].hex())
    out.append({'archivo': ruta, 'id': fid, 'id_coincide_con_carpeta': ids.get(ruta) == fid, 'http': estado,
                'contenido_binario': not html, 'firma': firma, 'bytes_indice': int(tam), 'sha256_indice': sha})
ok = len(out) == 12 and all(x['http'] in (200, 206) and x['contenido_binario'] and x['id_coincide_con_carpeta'] for x in out)
res = {'fecha_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
       'metodo': 'Solicitud anónima de los primeros 1024 bytes de cada enlace del índice.',
       'enlaces': len(out), 'todos_accesibles': ok, 'detalle': out}
a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(json.dumps({'enlaces': len(out), 'todos_accesibles': ok}))

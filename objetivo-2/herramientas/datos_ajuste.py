"""Contrato y máscaras del ajuste acotado; consume solo train/val."""
import hashlib,json,os
from pathlib import Path
import numpy as np
from evaluar_regiones_geometricas import masks,rays

MANIFEST_SHA='80db70d75e5ef2c40955881a87dd46b767137c24cb72dc1aa458a71c1efd8b03'
SPEC_SHA={'A':'596d876f0c5224bcc029d72e7fe7691268313259678a12d2b009a5e1441c5050','B':'3dd6e2c861bea2cec6b0dd3c9e5f6e5a9cb98ea9f71fb90bfdc9a47fad4b34c5'}
ROOT=Path(__file__).resolve().parents[2]

def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def canonical(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')).hexdigest()

def read_json(p):return json.loads(Path(p).read_text(encoding='utf-8'))

def atomic_json(p,value):
    p=Path(p);tmp=p.with_name(p.name+'.tmp')
    with tmp.open('w',encoding='utf-8',newline='\n') as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)

def spec(arm,root=ROOT):
    x=read_json(root/f'objetivo-2/configuraciones/ajuste-cuentas-v1/ejecucion-{arm}.json')
    if canonical(x)!=SPEC_SHA[arm]:raise ValueError('Especificación alterada o con campos desconocidos; requiere otra versión')
    return x

def sources(root=ROOT):
    paths=['objetivo-2/herramientas/'+n for n in ['datos_ajuste.py','ejecutar_ajuste.py','perdida_cuentas_regionales.py','evaluar_regiones_geometricas.py']]
    paths+=['objetivo-2/implementacion/models/unet_generator.py','objetivo-2/implementacion/scripts/evaluation/metrics.py']
    return {p:hashlib.sha256((root/p).read_text(encoding='utf-8').encode('utf-8')).hexdigest() for p in paths}

def prepare(data,out,root=ROOT):
    data=Path(data);out=Path(out)
    mp=root/'objetivo-2/evidencias/contrato-datos-v1.json'
    if digest(mp)!=MANIFEST_SHA:raise ValueError('Manifiesto distinto del contrato')
    contract=read_json(mp);recipe=read_json(root/'objetivo-1/contratos/receta-operativa-siete-actividades.json')
    cfg=read_json(root/'objetivo-2/configuraciones/protocolo-regiones-v1.json')
    gids=contract['splits']['train']+contract['splits']['val']
    if len(gids)!=15 or len(set(gids))!=15:raise ValueError('Particiones incompatibles')
    out.mkdir(parents=True,exist_ok=False)
    report={'schema':'oe2-ajuste-masks-v1','data_manifest_sha256':MANIFEST_SHA,'normalization':contract['normalization'],'splits':{k:contract['splits'][k] for k in ['train','val']},'geometry_protocol':cfg,'geometries':{},'data_files':{},'builder_sources':{n:hashlib.sha256((Path(__file__).parent/n).read_text(encoding='utf-8').encode()).hexdigest() for n in ['datos_ajuste.py','evaluar_regiones_geometricas.py']},'heldout_opened':False}
    for gid in gids:
        gp=root/f'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries/{gid}.json'
        if digest(gp)!=recipe['geometry_sha256'][gp.name]:raise ValueError('Geometría distinta: '+gid)
        g=read_json(gp)
        for suffix in ['.npz','.meta.json']:
            name=f'dataset-v2/shards/{gid}{suffix}'
            if digest(data/name)!=contract['files'][name]:raise ValueError('Datos distintos: '+name)
            report['data_files'][name]=contract['files'][name]
        meta=read_json(data/f'dataset-v2/shards/{gid}.meta.json')
        if meta['geometry_sha256']!=digest(gp):raise ValueError('Geometría/metadatos incompatibles')
        mm=[];pixel_counts=[]
        with np.load(data/f'dataset-v2/shards/{gid}.npz',allow_pickle=False) as z:
            if not np.allclose(z['el_centers_deg'],np.linspace(2,47,256),atol=1e-12,rtol=0):raise ValueError('Elevación incompatible')
            if not np.array_equal(z['az_centers_deg'],(z['az_edges_deg'][:-1]+z['az_edges_deg'][1:])/2):raise ValueError('Azimut incompatible')
            for vi in range(6):
                o,d=rays(z['az_centers_deg'],z['el_centers_deg'],vi,cfg)
                _,_,regions=masks(g,o,d,cfg);names=list(regions)
                mm.append(np.stack([regions[k] for k in names]));pixel_counts.append({k:int(regions[k].sum()) for k in names})
        arr=np.stack(mm);path=out/f'{gid}.npz'
        np.savez_compressed(path,masks=arr)
        report['geometries'][gid]={'geometry_sha256':digest(gp),'mask_file':path.name,'mask_sha256':digest(path),'content_sha256':hashlib.sha256(arr.tobytes()).hexdigest(),'names':names,'families':[0,1,2]+[3]*(len(names)-3),'pixels_by_view':pixel_counts}
    report['max_regions']=max(len(x['names']) for x in report['geometries'].values())
    atomic_json(out/'manifest.json',report)
    return report

class Store:
    def __init__(self,data,cache,root=ROOT):
        self.data=Path(data);self.cache=Path(cache);self.root=root
        mp=root/'objetivo-2/evidencias/contrato-datos-v1.json'
        if digest(mp)!=MANIFEST_SHA:raise ValueError('Contrato alterado')
        self.contract=read_json(mp);self.manifest=read_json(self.cache/'manifest.json')
        m=self.manifest
        if m['schema']!='oe2-ajuste-masks-v1' or m['data_manifest_sha256']!=MANIFEST_SHA:raise ValueError('Caché incompatible')
        if m['splits']!={k:self.contract['splits'][k] for k in ['train','val']}:raise ValueError('Particiones distintas')
        if m['normalization']!=self.contract['normalization']:raise ValueError('Normalización distinta')
        if m['geometry_protocol']!=read_json(root/'objetivo-2/configuraciones/protocolo-regiones-v1.json'):raise ValueError('Protocolo geométrico distinto')
        for n,h in m['builder_sources'].items():
            if hashlib.sha256((Path(__file__).parent/n).read_text(encoding='utf-8').encode()).hexdigest()!=h:raise ValueError('Preparador modificado; regenerar caché')
        expected={k:v for k,v in self.contract['files'].items() if k.startswith('dataset-v2/shards/')}
        if m['data_files']!=expected:raise ValueError('Inventario de datos incompleto')
        for name,h in expected.items():
            if digest(self.data/name)!=h:raise ValueError('Huella de datos distinta: '+name)
        self.masks={};self.arrays={}
        for gid,v in m['geometries'].items():
            if gid not in m['splits']['train']+m['splits']['val']:raise ValueError('Geometría no permitida')
            gp=root/f'objetivo-1/originales/scripts/simulation/geometry_catalog/geometries/{gid}.json'
            if digest(gp)!=v['geometry_sha256']:raise ValueError('Geometría cambiada')
            if v['mask_file']!=gid+'.npz':raise ValueError('Nombre de caché incompatible')
            path=self.cache/v['mask_file']
            if digest(path)!=v['mask_sha256']:raise ValueError('Máscara alterada')
            with np.load(path,allow_pickle=False) as z:raw=z['masks']
            if raw.dtype!=np.bool_ or raw.shape!=(6,len(v['names']),256,256):raise ValueError('Máscara fuera de contrato')
            if hashlib.sha256(raw.tobytes()).hexdigest()!=v['content_sha256']:raise ValueError('Contenido distinto')
            if v['families']!=[0,1,2]+[3]*(len(v['names'])-3):raise ValueError('Familias distintas')
            pad=np.zeros((6,m['max_regions'],256,256),bool);pad[:,:raw.shape[1]]=raw;self.masks[gid]=pad
        if set(self.masks)!=set(m['splits']['train']+m['splits']['val']):raise ValueError('Faltan geometrías')
        self.families=[0,1,2]+[3]*(m['max_regions']-3)
        self.scale=m['normalization']['scale']
        self.identity=digest(self.cache/'manifest.json')

    def load(self,gid):
        if gid not in self.masks:raise ValueError('Conjunto reservado o geometría desconocida')
        if gid not in self.arrays:
            with np.load(self.data/f'dataset-v2/shards/{gid}.npz',allow_pickle=False) as z:
                ref=z['ref_counts'];low=z['low_counts'];fractions=z['fractions']
                if ref.shape!=(6,256,256) or ref.dtype!=np.uint32 or low.shape!=(6,4,20,256,256) or low.dtype!=np.uint16:raise ValueError('Arreglos incompatibles')
                if not np.allclose(fractions,[.5,.1,.05,.01],atol=1e-8,rtol=0):raise ValueError('Fracciones distintas')
                low=low[:,2].copy()
                if np.any(low>ref[:,None]):raise ValueError('Adelgazamiento incoherente')
                self.arrays[gid]=(ref,low)
        return self.arrays[gid]

    def indices(self,split,configuration,stage):
        if split not in ('train','val'):raise ValueError('Partición reservada')
        if stage=='tecnica':rows=[tuple(x) for x in configuration['stages']['technical'][split+'_indices']]
        else:rows=[(g,v,k) for g in self.manifest['splits'][split] for v in range(6) for k in range(20)]
        if len(rows)!=len(set(rows)):raise ValueError('Índices repetidos')
        for g,v,k in rows:
            if g not in self.manifest['splits'][split] or not 0<=v<6 or not 0<=k<20:raise ValueError('Índice incompatible')
        return rows

    def batch(self,rows,device):
        import torch
        xs=[];ys=[];refs=[];ms=[]
        for g,v,k in rows:
            r,l=self.load(g);c=r[v].astype(np.float64)
            x=np.log1p(l[v,k].astype(np.float64)/.05);y=np.log1p(c)
            xs.append((x/(self.scale+x)).astype(np.float32));ys.append((y/(self.scale+y)).astype(np.float32));refs.append(c);ms.append(self.masks[g][v])
        return (torch.from_numpy(np.stack(xs)[:,None]).to(device),torch.from_numpy(np.stack(ys)[:,None]).to(device),torch.from_numpy(np.stack(refs)[:,None]).to(device),torch.from_numpy(np.stack(ms)).to(device))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description='Prepara 90 mapas train/val sin entrenar ni abrir test')
    p.add_argument('--datos',type=Path,required=True);p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args();r=prepare(a.datos,a.salida);print(json.dumps({'geometries':len(r['geometries']),'views':90,'heldout_opened':False}))

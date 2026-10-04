"""Controles funcionales y negativos sobre la batería técnica real."""
import argparse,json,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import torch
from filelock import FileLock
from datos_ajuste import ROOT,Store,spec,sources,digest,read_json,atomic_json
from revisar_ajuste import audit_technical,load_completed

p=argparse.ArgumentParser(description=__doc__)
for n in ['datos','mascaras','pesos','ejecuciones','salida']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args()
store=Store(a.datos,a.mascaras)
paths={k:a.ejecuciones/k for k in ['A-continua','A-recuperada','B-continua','B-recuperada']}

class IntegrationTests(unittest.TestCase):
    def command(self,*extra):
        cmd=[sys.executable,str(ROOT/'objetivo-2/herramientas/ejecutar_ajuste.py'),'--datos',str(a.datos),'--mascaras',str(a.mascaras),'--pesos',str(a.pesos),'--salida',str(paths['A-continua']),'--cpu-test']+list(extra)
        return subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    def test_pair_configuration(self):
        x,y=spec('A'),spec('B')
        self.assertEqual({k for k in x if x[k]!=y[k]},{'arm','run_id','lambda_regional'})
    def test_homogeneous_geometry(self):
        meta=store.manifest['geometries']['geo-train-01']
        self.assertEqual(meta['families'],[0,1,2])
        self.assertFalse(store.masks['geo-train-01'][:,3:].any())
        self.assertTrue(np.all(store.masks['geo-train-01'][:,:3].sum((2,3))>=20))
    def test_all_splits_have_expected_indices(self):
        self.assertEqual(len(store.indices('train',spec('A'),'piloto')),1440)
        self.assertEqual(len(store.indices('val',spec('A'),'piloto')),360)
        self.assertEqual(len(store.masks),15)
    def test_reserved_rejected(self):
        with self.assertRaises(ValueError):store.load('geo-test-01')
        with self.assertRaises(ValueError):store.indices('test',spec('A'),'piloto')
    def test_validation_masks_unchanged(self):
        import hashlib
        old=read_json(ROOT/'objetivo-2/evidencias/evaluacion-regiones-geometricas-v1.json')
        count=0
        for row in old['masks']:
            gid=row['geometry'];vi=row['view']
            for j,name in enumerate(store.manifest['geometries'][gid]['names']):
                self.assertEqual(hashlib.sha256(store.masks[gid][vi,j].tobytes()).hexdigest(),row['mask_content_sha256'][name]);count+=1
        self.assertEqual(count,78)
    def test_unknown_config_rejected(self):
        root=a.salida.parent/'fixture-config';d=root/'objetivo-2/configuraciones/ajuste-cuentas-v1';d.mkdir(parents=True,exist_ok=True)
        x=spec('A');x['campo_ignorado']=123;atomic_json(d/'ejecucion-A.json',x)
        with self.assertRaises(ValueError):spec('A',root)
    def test_changed_mask_rejected(self):
        # Se sustituye solo el cálculo de huella en memoria; ningún archivo se altera.
        from datos_ajuste import digest as original
        def bad(p):return '0'*64 if Path(p)==a.mascaras/'geo-train-01.npz' else original(p)
        with patch('datos_ajuste.digest',side_effect=bad):
            with self.assertRaises(ValueError):Store(a.datos,a.mascaras)
    def test_cpu_gate_not_gpu(self):
        with self.assertRaisesRegex(ValueError,'CPU'):audit_technical(paths,require_gpu=True)
    def test_partial_rejected(self):
        state=torch.load(paths['A-continua']/'last.pt',map_location='cpu',weights_only=True);state['epoch']=1
        with patch('revisar_ajuste.torch.load',return_value=state):
            with self.assertRaisesRegex(ValueError,'pocas'):load_completed(paths['A-continua'],'A','tecnica',sources())
    def test_wrong_arm_resume_rejected(self):
        cp=paths['A-continua']/'last.pt';before=digest(cp)
        r=self.command('--rama','B','--etapa','tecnica','--reanudar')
        self.assertNotEqual(r.returncode,0);self.assertIn('Identidad distinta',r.stderr);self.assertEqual(digest(cp),before)
    def test_pilot_cpu_rejected(self):
        r=self.command('--rama','A','--etapa','piloto')
        self.assertNotEqual(r.returncode,0);self.assertIn('CPU autorizado solo',r.stderr)
    def test_lock_prevents_concurrent_write(self):
        with FileLock(str(paths['A-continua']/'run.lock'),timeout=0):
            r=self.command('--rama','A','--etapa','tecnica','--exportar')
        self.assertNotEqual(r.returncode,0);self.assertIn('Timeout',r.stderr)
    def test_export_does_not_train(self):
        cp=paths['A-continua']/'last.pt';before=digest(cp);pred=digest(paths['A-continua']/'predicciones-val.npy')
        r=self.command('--rama','A','--etapa','tecnica','--exportar')
        self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(digest(cp),before);self.assertEqual(digest(paths['A-continua']/'predicciones-val.npy'),pred)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IntegrationTests))
    report={'schema':'oe2-adjustment-integration-tests-v1','tests':result.testsRun,'passed':result.wasSuccessful(),'failures':len(result.failures),'errors':len(result.errors),'heldout_opened':False,'device':'cpu','scope':'functional and negative checks; no GPU approval'}
    atomic_json(a.salida,report)
    if not result.wasSuccessful():raise SystemExit(1)

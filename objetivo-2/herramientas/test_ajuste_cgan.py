"""Controles matemáticos, separación de actualizaciones y artefactos cGAN."""
import argparse,copy,io,json,subprocess,sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
import torch
import ejecutar_ajuste_cgan as C
import revisar_ajuste_cgan as R
from datos_ajuste import Store,read_json,digest,atomic_json
from losses import generator_loss,gradient_penalty
from filelock import FileLock

ARGS=None
class Maths(unittest.TestCase):
    def setUp(self):
        C.configure();C.seed_all(42)
        self.cfg=C.spec('C0');self.x=torch.rand(2,1,8,8);self.y=torch.rand(2,1,8,8)
        self.z=torch.rand(2,1,8,8).mul(.3).add(.1).requires_grad_()
        self.counts=torch.ones(2,1,8,8,dtype=torch.float64)*4
        self.masks=torch.zeros(2,2,8,8,dtype=torch.bool);self.masks[:,0,:4]=True;self.masks[:,1,4:]=True
        class Critic(torch.nn.Module):
            def __init__(self):super().__init__();self.conv=torch.nn.Conv2d(2,1,1)
            def forward(self,x,z):return self.conv(torch.cat([x,z],1))
        self.D=Critic()
    def test_01_zero_exact(self):
        old,_=generator_loss(self.D,self.x,self.z,self.y,100,1)
        new,_,_=C.generator_objective(self.D,self.x,self.z,self.y,self.counts,self.masks,[0,1],8.,self.cfg)
        self.assertTrue(torch.equal(old,new))
        g0=torch.autograd.grad(old,self.z,retain_graph=True)[0];g1=torch.autograd.grad(new,self.z)[0]
        self.assertTrue(torch.equal(g0,g1))
    def test_02_regional_gradient(self):
        old,_=generator_loss(self.D,self.x,self.z,self.y,100,1)
        new,_,_=C.generator_objective(self.D,self.x,self.z,self.y,self.counts,self.masks,[0,1],8.,C.spec('C1'))
        g=torch.autograd.grad(new-old,self.z)[0]
        self.assertTrue(torch.isfinite(g).all());self.assertGreater(float(g.abs().sum()),0)
    def test_03_gp_average_patch(self):
        class UnitScore(torch.nn.Module):
            def forward(self,x,y):return (y.flatten(1).sum(1)/8.)[:,None,None,None].expand(-1,1,30,30)
        self.assertLess(float(gradient_penalty(UnitScore(),self.x,self.y,self.z.detach())),1e-12)
    def test_04_separate_updates_and_steps(self):
        G=torch.nn.Sequential(torch.nn.Conv2d(1,1,1),torch.nn.Sigmoid())
        og=torch.optim.Adam(G.parameters(),lr=1e-5,betas=(0.,.9),foreach=False)
        od=torch.optim.Adam(self.D.parameters(),lr=1e-5,betas=(0.,.9),foreach=False)
        before_g=copy.deepcopy(G.state_dict());before_d=copy.deepcopy(self.D.state_dict());after_d={}
        def observe(phase,g,d,ag,ad):
            if phase=='after_d':
                self.assertTrue(R.equal_state(g.state_dict(),before_g))
                self.assertFalse(R.equal_state(d.state_dict(),before_d))
                self.assertTrue(all(p.grad is None for p in g.parameters()))
                after_d.update(copy.deepcopy(d.state_dict()))
            else:
                self.assertTrue(R.equal_state(d.state_dict(),after_d))
                self.assertFalse(R.equal_state(g.state_dict(),before_g))
                self.assertTrue(all(p.grad is None for p in d.parameters()))
        parts,_=C.train_step(G,self.D,og,od,(self.x,self.y,self.counts,self.masks),SimpleNamespace(families=[0,1],scale=8.),C.spec('C1'),observe)
        self.assertTrue(all(np.isfinite(v) for v in parts.values()))
        self.assertEqual({float(x['step']) for x in og.state.values()},{1.})
        self.assertEqual({float(x['step']) for x in od.state.values()},{5.})
    def test_05_rng_roundtrip(self):
        import random
        state=C.rng_state(torch.device('cpu'));buf=io.BytesIO();torch.save(state,buf);buf.seek(0)
        saved=torch.load(buf,weights_only=True)
        expected=(random.random(),np.random.rand(3),torch.rand(3))
        C.restore_rng(saved,torch.device('cpu'));actual=(random.random(),np.random.rand(3),torch.rand(3))
        self.assertEqual(expected[0],actual[0]);np.testing.assert_array_equal(expected[1],actual[1]);self.assertTrue(torch.equal(expected[2],actual[2]))
    def test_06_config_only_regional(self):
        a=C.spec('C0');b=C.spec('C1')
        self.assertEqual({k for k in a if a[k]!=b[k]},{'arm','run_id','lambda_regional'})
    def test_07_unknown_config_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'objetivo-2/configuraciones/ajuste-cgan-v1';p.mkdir(parents=True)
            c=C.spec('C0');c['unknown']=1;atomic_json(p/'C0.json',c)
            with patch.object(C,'ROOT',Path(td)):
                with self.assertRaisesRegex(ValueError,'Configuración'):C.spec('C0')
    def test_08_nonfinite_no_step(self):
        before=copy.deepcopy(self.D.state_dict());o=torch.optim.Adam(self.D.parameters(),lr=1e-5)
        with self.assertRaisesRegex(ValueError,'no finita'):C.checked_step(torch.tensor(float('inf')),self.D,o)
        self.assertTrue(R.equal_state(before,self.D.state_dict()));self.assertFalse(o.state)
    def test_09_old_unet_gate_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'gate.json';atomic_json(p,{'schema':'oe2-ajuste-technical-gate-v1','gpu_accepted':True})
            with self.assertRaisesRegex(ValueError,'cGAN'):C.gate_check(p,{})
    def test_10_full_evaluation_fixtures(self):
        from evaluar_ajuste_cgan import tables
        store=Store(ARGS.datos,ARGS.mascaras)
        root=ARGS.predicciones_previas
        if digest(root/'unet-predicciones.npy')!='c4e35ef07c46974b4847ec46ea60173c6f1a44e1c6f33f0639f2aea2e58ec9fc':raise ValueError('Fixture distinta')
        if digest(root/'cgan-predicciones.npy')!='39d087f7eaa93cc85c874adfc84b6fffdd061c60e1f619842b09cd941ac8d091':raise ValueError('Fixture distinta')
        u=np.load(root/'unet-predicciones.npy',mmap_mode='r');g=np.load(root/'cgan-predicciones.npy',mmap_mode='r')
        keys=[list(x) for x in store.indices('val',C.spec('C0'),'piloto')]
        out,rows=tables(store,keys,{'C0':u,'C1':g},u,'piloto')
        self.assertEqual(len(rows),24);self.assertEqual(out['summary']['C0']['common_contrasts'],23)
        self.assertAlmostEqual(out['summary']['C0']['Q'],.2189556555777892,places=12)
        self.assertEqual(out['summary']['C0'],out['summary']['inicial_cgan'])
        self.assertEqual({x['model'] for x in out['regions']},{'entrada','C0','C1'})
        self.assertEqual({x['model'] for x in out['images']},{'entrada','C0','C1'})
        with self.assertRaises(ValueError):tables(store,keys[:-1],{'C0':u[:-1],'C1':g[:-1]},u[:-1],'piloto')
    def test_11_reserved_split_rejected(self):
        store=Store(ARGS.datos,ARGS.mascaras)
        with self.assertRaisesRegex(ValueError,'reservada'):store.indices('test',C.spec('C0'),'piloto')

class Artifacts(unittest.TestCase):
    def run_cli(self,*flags):
        cmd=[sys.executable,str(Path(C.__file__)),'--rama','C0','--etapa','tecnica','--datos',str(ARGS.datos),'--mascaras',str(ARGS.mascaras),'--pesos',str(ARGS.pesos),'--salida',str(ARGS.ejecuciones/'C0-recuperada'),'--cpu-test']+list(flags)
        return subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    def test_12_exact_recovery(self):
        paths={arm+'-'+mode:ARGS.ejecuciones/(arm+'-'+mode) for arm in ['C0','C1'] for mode in ['continua','recuperada']}
        r=R.audit_technical(paths);self.assertTrue(r['exact_recovery']);self.assertFalse(r['gpu_accepted'])
        with self.assertRaisesRegex(ValueError,'CPU'):R.audit_technical(paths,require_gpu=True)
    def test_13_corrupt_critic_rejected(self):
        c=R.load_completed(ARGS.ejecuciones/'C0-continua','C0','tecnica')
        key=next(iter(c['critic']));c['critic'][key].flatten()[0]+=1
        with self.assertRaisesRegex(ValueError,'Huella'):R.validate_state(c)
    def test_14_wrong_optimizer_step_rejected(self):
        c=R.load_completed(ARGS.ejecuciones/'C0-continua','C0','tecnica')
        next(iter(c['opt_d']['state'].values()))['step']+=1
        with self.assertRaisesRegex(ValueError,'Pasos'):R.validate_state(c)
    def test_15_wrong_arm_no_write(self):
        cp=ARGS.ejecuciones/'C0-recuperada/last.pt';h=digest(cp)
        r=self.run_cli('--rama','C1','--reanudar')
        self.assertNotEqual(r.returncode,0);self.assertIn('incompatible',r.stderr);self.assertEqual(h,digest(cp))
    def test_16_cpu_pilot_no_write(self):
        cp=ARGS.ejecuciones/'C0-recuperada/last.pt';h=digest(cp)
        r=self.run_cli('--etapa','piloto');self.assertNotEqual(r.returncode,0);self.assertIn('CPU solo',r.stderr);self.assertEqual(h,digest(cp))
    def test_17_export_without_training(self):
        p=ARGS.ejecuciones/'C0-recuperada';before={n:digest(p/n) for n in ['last.pt','predicciones-val.npy','indices-val.json','exports.json']}
        r=self.run_cli('--exportar');self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(before,{n:digest(p/n) for n in before})
    def test_18_writer_lock(self):
        p=ARGS.ejecuciones/'C0-recuperada';before=digest(p/'last.pt')
        with FileLock(str(p/'.run.lock')):
            r=self.run_cli('--exportar')
        self.assertNotEqual(r.returncode,0);self.assertIn('Timeout',r.stderr);self.assertEqual(before,digest(p/'last.pt'))
    def test_19_complete_resume_rejected(self):
        r=self.run_cli('--reanudar');self.assertNotEqual(r.returncode,0);self.assertIn('ya completa',r.stderr)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ['datos','mascaras','pesos','ejecuciones','predicciones-previas','salida']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--fase',choices=['matematica','artefactos','todo'],default='todo');ARGS=p.parse_args();C.configure()
    suite=unittest.TestSuite()
    for cls,name in [(Maths,'matematica'),(Artifacts,'artefactos')]:
        if ARGS.fase in (name,'todo'):suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    r=unittest.TextTestRunner(verbosity=2).run(suite)
    report={'schema':'oe2-cgan-adjustment-tests-v1','phase':ARGS.fase,'tests':r.testsRun,'passed':r.wasSuccessful(),'failures':len(r.failures),'errors':len(r.errors),'gpu_accepted':False,'heldout_opened':False,'full_evaluation_fixture_is_prior_pilot':True}
    ARGS.salida.parent.mkdir(parents=True,exist_ok=True);atomic_json(ARGS.salida,report)
    raise SystemExit(0 if r.wasSuccessful() else 1)


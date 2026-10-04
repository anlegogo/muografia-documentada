"""Contratos de semillas y rechazo de cruces de la repetición C0/C1."""
import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import ejecutar_borde_cgan as e
import revisar_borde_cgan as r

class Contracts(unittest.TestCase):
    def test_fixed_pairs_and_science(self):
        for pair,seed in e.PAIR_SEEDS.items():
            for arm in ['C0','C1']:
                old=e.spec(arm,'B1');new=e.spec(arm,pair)
                self.assertEqual(new['seed'],seed);self.assertEqual(new['pair'],pair)
                for k in old:
                    if k not in ['seed','run_id','pair']:self.assertEqual(old[k],new[k],k)
            a=e.spec('C0',pair);b=e.spec('C1',pair)
            self.assertEqual({k for k in a if a[k]!=b[k]},{'arm','run_id','lambda_edge'})
    def test_unknown_pair(self):
        with self.assertRaisesRegex(ValueError,'Pareja'):e.spec('C0','R9')
    def test_changed_seed_or_extra_field_rejected(self):
        for key,value in [('seed',2026100303),('unexpected',True),('lambda_gp',0),('lambda_edge',999.)]:
            original=e.read_json
            def read(p):
                x=original(p)
                if 'borde-cgan-v1' in str(p):x[key]=value
                return x
            with patch.object(e,'read_json',side_effect=read):
                with self.assertRaisesRegex(ValueError,'alterada'):e.spec('C0','B1')
    def test_seed_identity_rejected_before_state(self):
        c={'identity':{'arm':'C0','stage':'tecnica','pair':'B1','seed':2026100412}}
        with self.assertRaisesRegex(ValueError,'pareja/semilla'):r.validate_state(c)
    def test_cross_pair_gate_rejected_before_audit(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'gate.json'
            p.write_text(json.dumps({'schema':'oe2-cgan-borde-gate-v1','gpu_accepted':True,'pair':'B1','seed':2026100411}))
            with patch.object(r,'audit_technical') as audit:
                with self.assertRaisesRegex(ValueError,'otra pareja'):e.gate_check(p,{'pair':'B2','seed':2026100412})
                audit.assert_not_called()
    def test_old_gate_rejected_before_audit(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'gate.json';p.write_text(json.dumps({'schema':'oe2-cgan-borde-gate-v1','gpu_accepted':True}))
            with patch.object(r,'audit_technical') as audit:
                with self.assertRaisesRegex(ValueError,'otra pareja'):e.gate_check(p,{'pair':'B1','seed':2026100411})
                audit.assert_not_called()
    def test_cli_pair_not_free_seed(self):
        p=e.parser()
        args=p.parse_args(['--pareja','B3','--rama','C1','--etapa','tecnica','--datos','d','--mascaras','m','--pesos','p','--salida','o'])
        self.assertEqual(args.pareja,'B3');self.assertFalse(hasattr(args,'seed'))

class Summary(unittest.TestCase):
    def fixtures(self):
        from resumir_borde_cgan import decision_checks
        a={'Q':.2,'Q_by_geometry':{f'g{i}':.2 for i in range(3)},'sky_mae':.1,'edge_mae':.2,'common_contrasts':23,'contrast_absolute_error':.2,'ssim':.8,'psnr':30.}
        b={**copy.deepcopy(a),'Q':.1,'Q_by_geometry':{f'g{i}':.1 for i in range(3)},'ssim':.81,'edge_mae':.19}
        result={}
        for pair,seed in e.PAIR_SEEDS.items():
            summary={'C0':copy.deepcopy(a),'C1':copy.deepcopy(b),'inicial_cgan':a,'entrada':a}
            result[pair]={'pair':pair,'seed':seed,'stage':'piloto','quality_evaluation':True,'physical_acceptance':False,'heldout_opened':False,'sources':{},'environment':{},'mask_manifest_sha256':'m','initial_checkpoint_sha256':'i','initial_inference_device':'cuda','summary':summary,'decision_checks':decision_checks(summary)}
        return result
    def test_all_pairs_and_median(self):
        from resumir_borde_cgan import summarize
        r=summarize(self.fixtures(),'piloto')
        self.assertEqual(r['concordant_pairs'],3);self.assertAlmostEqual(r['descriptive_summary']['Q']['median'],-.1)
        self.assertFalse(r['physical_acceptance'])
    def test_missing_pair_rejected(self):
        from resumir_borde_cgan import summarize
        rr=self.fixtures();del rr['B3']
        with self.assertRaisesRegex(ValueError,'completas'):summarize(rr,'piloto')
    def test_wrong_seed_rejected(self):
        from resumir_borde_cgan import summarize
        rr=self.fixtures();rr['B2']['seed']=e.PAIR_SEEDS['B1']
        with self.assertRaisesRegex(ValueError,'Pareja/semilla'):summarize(rr,'piloto')
    def test_unfavorable_pair_kept(self):
        from resumir_borde_cgan import summarize,decision_checks
        rr=self.fixtures();rr['B3']['summary']['C1']['Q']=.3
        rr['B3']['decision_checks']=decision_checks(rr['B3']['summary'])
        r=summarize(rr,'piloto');self.assertEqual(r['concordant_pairs'],2);self.assertEqual(r['pairs_reducing_Q'],2)
        self.assertEqual(r['decision'],'dependencia_de_semilla_o_compromiso')
    def test_false_reported_acceptance_rejected(self):
        from resumir_borde_cgan import summarize
        rr=self.fixtures();rr['B1']['summary']['C1']['ssim']=.7
        with self.assertRaisesRegex(ValueError,'Clasificación'):summarize(rr,'piloto')
    def test_changed_baseline_rejected(self):
        from resumir_borde_cgan import summarize
        rr=copy.deepcopy(self.fixtures());rr['B2']['summary']['inicial_cgan']=dict(rr['B2']['summary']['inicial_cgan'],Q=.5)
        with self.assertRaisesRegex(ValueError,'Referencias'):summarize(rr,'piloto')
    def test_nonfinite_rejected(self):
        from resumir_borde_cgan import summarize
        rr=self.fixtures();rr['B1']['summary']['C1']['Q']=float('nan')
        with self.assertRaisesRegex(ValueError,'no finita'):summarize(rr,'piloto')


class Objective(unittest.TestCase):
    def test_zero_weight_matches_historical_C1_exactly(self):
        import torch
        import ejecutar_ajuste_cgan as old
        e.configure();torch.manual_seed(44)
        class Critic(torch.nn.Module):
            def forward(self,x,z):return 2*z+x
        z=(torch.rand(2,1,8,8)*.2+.1).requires_grad_()
        x=torch.rand_like(z);y=torch.rand_like(z);counts=torch.ones_like(z)*4
        masks=torch.ones(2,4,8,8,dtype=torch.bool)
        before,_,_=old.generator_objective(Critic(),x,z,y,counts,masks,[0,1,2,3],8.,old.spec('C1','R1'))
        after,parts,_=e.generator_objective(Critic(),x,z,y,counts,masks,[0,1,2,3],8.,e.spec('C0','B1'))
        self.assertTrue(torch.equal(before,after))
        self.assertTrue(torch.equal(torch.autograd.grad(before,z,retain_graph=True)[0],torch.autograd.grad(after,z)[0]))
        self.assertEqual(parts['weighted_edge'],0.)
    def test_positive_component_changes_gradient(self):
        import torch
        e.configure();torch.manual_seed(45)
        z=(torch.rand(2,1,8,8)*.2+.1).requires_grad_()
        x=torch.zeros_like(z);y=torch.zeros_like(z);counts=torch.ones_like(z)*4
        masks=torch.ones(2,4,8,8,dtype=torch.bool)
        a,_,_=e.generator_objective(None,x,z,y,counts,masks,[0,1,2,3],8.,e.spec('C0','B1'))
        b,parts,_=e.generator_objective(None,x,z,y,counts,masks,[0,1,2,3],8.,e.spec('C1','B1'))
        g=torch.autograd.grad(b-a,z)[0]
        self.assertTrue(torch.isfinite(g).all());self.assertGreater(float(g.abs().sum()),0)
        self.assertAlmostEqual(float((b-a).detach()),parts['weighted_edge'],places=10)

    def test_zero_full_training_step_matches_historical(self):
        import copy,torch
        from types import SimpleNamespace
        import ejecutar_ajuste_cgan as old
        e.configure();e.seed_all(101)
        class Critic(torch.nn.Module):
            def __init__(self):super().__init__();self.conv=torch.nn.Conv2d(2,1,1)
            def forward(self,x,z):return self.conv(torch.cat([x,z],1))
        g=torch.nn.Sequential(torch.nn.Conv2d(1,1,1),torch.nn.Sigmoid());d=Critic()
        gg=copy.deepcopy(g);dd=copy.deepcopy(d)
        optim=lambda m:torch.optim.Adam(m.parameters(),lr=1e-5,betas=(0.,.9),foreach=False)
        og,od,ogg,odd=optim(g),optim(d),optim(gg),optim(dd)
        batch=(torch.rand(2,1,8,8),torch.rand(2,1,8,8),torch.ones(2,1,8,8)*4,torch.ones(2,4,8,8,dtype=torch.bool))
        store=SimpleNamespace(families=[0,1,2,3],scale=8.)
        rng=e.rng_state(torch.device('cpu'))
        old.train_step(g,d,og,od,batch,store,e.spec('C0','B1'))
        expected=e.rng_state(torch.device('cpu'));e.restore_rng(rng,torch.device('cpu'))
        e.train_step(gg,dd,ogg,odd,batch,store,e.spec('C0','B1'))
        for a,b in [(g.state_dict(),gg.state_dict()),(d.state_dict(),dd.state_dict()),(og.state_dict(),ogg.state_dict()),(od.state_dict(),odd.state_dict()),(expected,e.rng_state(torch.device('cpu')))]:
            self.assertTrue(r.equal_state(a,b))

    def test_historical_gpu_gate_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'g.json';p.write_text(json.dumps({'schema':'oe2-cgan-ajuste-gate-v1','gpu_accepted':True,'pair':'B1','seed':2026100411}))
            with self.assertRaises(ValueError):e.gate_check(p,{'pair':'B1','seed':2026100411})

if __name__=='__main__':unittest.main()

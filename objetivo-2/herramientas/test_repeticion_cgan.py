"""Contratos de semillas y rechazo de cruces de la repetición C0/C1."""
import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import ejecutar_ajuste_cgan as e
import revisar_ajuste_cgan as r

class Contracts(unittest.TestCase):
    def test_fixed_pairs_and_science(self):
        for pair,seed in e.PAIR_SEEDS.items():
            for arm in ['C0','C1']:
                old=e.spec(arm);new=e.spec(arm,pair)
                self.assertEqual(new['seed'],seed);self.assertEqual(new['pair'],pair)
                for k in old:
                    if k not in ['seed','run_id']:self.assertEqual(old[k],new[k],k)
            a=e.spec('C0',pair);b=e.spec('C1',pair)
            self.assertEqual({k for k in a if a[k]!=b[k]},{'arm','run_id','lambda_regional'})
    def test_unknown_pair(self):
        with self.assertRaisesRegex(ValueError,'Pareja'):e.spec('C0','R9')
    def test_changed_seed_or_extra_field_rejected(self):
        for key,value in [('seed',2026100303),('unexpected',True),('lambda_gp',0)]:
            original=e.read_json
            def read(p):
                x=original(p)
                if 'repeticion-cgan-f05' in str(p):x[key]=value
                return x
            with patch.object(e,'read_json',side_effect=read):
                with self.assertRaisesRegex(ValueError,'alterada'):e.spec('C0','R1')
    def test_seed_identity_rejected_before_state(self):
        c={'identity':{'arm':'C0','stage':'tecnica','pair':'R1','seed':2026100402}}
        with self.assertRaisesRegex(ValueError,'pareja/semilla'):r.validate_state(c)
    def test_cross_pair_gate_rejected_before_audit(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'gate.json'
            p.write_text(json.dumps({'schema':'oe2-cgan-ajuste-gate-v1','gpu_accepted':True,'pair':'R1','seed':2026100401}))
            with patch.object(r,'audit_technical') as audit:
                with self.assertRaisesRegex(ValueError,'otra pareja'):e.gate_check(p,{'pair':'R2','seed':2026100402})
                audit.assert_not_called()
    def test_old_gate_rejected_before_audit(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'gate.json';p.write_text(json.dumps({'schema':'oe2-cgan-ajuste-gate-v1','gpu_accepted':True}))
            with patch.object(r,'audit_technical') as audit:
                with self.assertRaisesRegex(ValueError,'otra pareja'):e.gate_check(p,{'pair':'R1','seed':2026100401})
                audit.assert_not_called()
    def test_cli_pair_not_free_seed(self):
        p=e.parser()
        args=p.parse_args(['--pareja','R3','--rama','C1','--etapa','tecnica','--datos','d','--mascaras','m','--pesos','p','--salida','o'])
        self.assertEqual(args.pareja,'R3');self.assertFalse(hasattr(args,'seed'))

class Summary(unittest.TestCase):
    def fixtures(self):
        from resumir_repeticion_cgan import decision_checks
        a={'Q':.2,'Q_by_geometry':{f'g{i}':.2 for i in range(3)},'sky_mae':.1,'edge_mae':.2,'common_contrasts':23,'contrast_absolute_error':.2,'ssim':.8,'psnr':30.}
        b={**copy.deepcopy(a),'Q':.1,'Q_by_geometry':{f'g{i}':.1 for i in range(3)},'ssim':.81}
        result={}
        for pair,seed in e.PAIR_SEEDS.items():
            summary={'C0':copy.deepcopy(a),'C1':copy.deepcopy(b),'inicial_cgan':a,'entrada':a}
            result[pair]={'pair':pair,'seed':seed,'stage':'piloto','quality_evaluation':True,'physical_acceptance':False,'heldout_opened':False,'sources':{},'environment':{},'mask_manifest_sha256':'m','initial_checkpoint_sha256':'i','initial_inference_device':'cuda','summary':summary,'decision_checks':decision_checks(summary)}
        return result
    def test_all_pairs_and_median(self):
        from resumir_repeticion_cgan import summarize
        r=summarize(self.fixtures(),'piloto')
        self.assertEqual(r['concordant_pairs'],3);self.assertAlmostEqual(r['descriptive_summary']['Q']['median'],-.1)
        self.assertFalse(r['physical_acceptance'])
    def test_missing_pair_rejected(self):
        from resumir_repeticion_cgan import summarize
        rr=self.fixtures();del rr['R3']
        with self.assertRaisesRegex(ValueError,'completas'):summarize(rr,'piloto')
    def test_wrong_seed_rejected(self):
        from resumir_repeticion_cgan import summarize
        rr=self.fixtures();rr['R2']['seed']=e.PAIR_SEEDS['R1']
        with self.assertRaisesRegex(ValueError,'Pareja/semilla'):summarize(rr,'piloto')
    def test_unfavorable_pair_kept(self):
        from resumir_repeticion_cgan import summarize,decision_checks
        rr=self.fixtures();rr['R3']['summary']['C1']['Q']=.3
        rr['R3']['decision_checks']=decision_checks(rr['R3']['summary'])
        r=summarize(rr,'piloto');self.assertEqual(r['concordant_pairs'],2);self.assertEqual(r['pairs_reducing_Q'],2)
        self.assertEqual(r['decision'],'dependencia_de_semilla_o_compromiso')
    def test_false_reported_acceptance_rejected(self):
        from resumir_repeticion_cgan import summarize
        rr=self.fixtures();rr['R1']['summary']['C1']['ssim']=.7
        with self.assertRaisesRegex(ValueError,'Clasificación'):summarize(rr,'piloto')
    def test_changed_baseline_rejected(self):
        from resumir_repeticion_cgan import summarize
        rr=copy.deepcopy(self.fixtures());rr['R2']['summary']['inicial_cgan']=dict(rr['R2']['summary']['inicial_cgan'],Q=.5)
        with self.assertRaisesRegex(ValueError,'Referencias'):summarize(rr,'piloto')
    def test_nonfinite_rejected(self):
        from resumir_repeticion_cgan import summarize
        rr=self.fixtures();rr['R1']['summary']['C1']['Q']=float('nan')
        with self.assertRaisesRegex(ValueError,'no finita'):summarize(rr,'piloto')

if __name__=='__main__':unittest.main()

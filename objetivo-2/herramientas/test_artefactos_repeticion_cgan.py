"""Verificación CPU de las tres parejas; requiere las doce ejecuciones técnicas."""
import argparse,io,json,subprocess,sys,unittest
from pathlib import Path
import ejecutar_ajuste_cgan as e
import revisar_ajuste_cgan as a
from datos_ajuste import digest,atomic_json

class Artifacts(unittest.TestCase):
    def folder(self,pair):return ARGS.raiz/pair/ARGS.carpeta_tecnica
    def paths(self,pair):return {arm+'-'+mode:self.folder(pair)/(arm+'-'+mode) for arm in ['C0','C1'] for mode in ['continua','recuperada']}
    def command(self):
        return [sys.executable,str(Path(e.__file__)), '--pareja','R1','--rama','C0','--etapa','tecnica','--cpu-test',
                '--datos',str(ARGS.datos),'--mascaras',str(ARGS.mascaras),'--pesos',str(ARGS.pesos),
                '--salida',str(self.folder('R1')/'C0-recuperada')]
    def cli(self,*extra):return subprocess.run(self.command()+list(extra),capture_output=True,text=True,encoding='utf-8',errors='replace')
    def test_all_three_recoveries(self):
        for pair in e.PAIR_SEEDS:
            gate=a.audit_technical(self.paths(pair),pair=pair)
            self.assertTrue(gate['exact_recovery']);self.assertFalse(gate['gpu_accepted']);self.assertEqual(gate['seed'],e.PAIR_SEEDS[pair])
    def test_cpu_gate_cannot_accept_gpu(self):
        with self.assertRaisesRegex(ValueError,'CPU'):a.audit_technical(self.paths('R1'),require_gpu=True,pair='R1')
    def test_mixed_pair_rejected(self):
        paths=self.paths('R1');paths['C1-recuperada']=self.paths('R2')['C1-recuperada']
        with self.assertRaisesRegex(ValueError,'Pareja'):a.audit_technical(paths,pair='R1')
    def test_corrupt_optimizer_rejected(self):
        c=a.load_completed(self.folder('R1')/'C0-continua','C0','tecnica','R1')
        next(iter(c['opt_d']['state'].values()))['step']+=1
        with self.assertRaisesRegex(ValueError,'Pasos'):a.validate_state(c)
    def test_corrupt_critic_rejected(self):
        c=a.load_completed(self.folder('R1')/'C0-continua','C0','tecnica','R1')
        next(iter(c['critic'].values())).flatten()[0]+=1
        with self.assertRaisesRegex(ValueError,'Huella'):a.validate_state(c)
    def test_current_sources_and_pairing(self):
        ids=[];orders=[]
        for pair in e.PAIR_SEEDS:
            x=a.load_completed(self.folder(pair)/'C0-continua','C0','tecnica',pair)
            y=a.load_completed(self.folder(pair)/'C1-continua','C1','tecnica',pair)
            self.assertEqual(x['identity']['sources'],e.sources())
            for key in ['initial_generator_sha256','initial_critic_sha256','train_indices_sha256','val_indices_sha256','cache_sha256']:
                self.assertEqual(x['identity'][key],y['identity'][key])
            self.assertEqual([h['order_sha256'] for h in x['history']],[h['order_sha256'] for h in y['history']])
            ids.append(x['identity']);orders.append(tuple(h['order_sha256'] for h in x['history']))
        self.assertEqual(len(set(orders)),3)
        for key in ['initial_generator_sha256','initial_critic_sha256','train_indices_sha256','val_indices_sha256','cache_sha256']:
            self.assertEqual(len({x[key] for x in ids}),1)
    def test_wrong_pair_resume_does_not_modify_checkpoint(self):
        p=self.folder('R1')/'C0-recuperada/last.pt';before=digest(p);r=self.cli('--reanudar','--pareja','R2')
        self.assertNotEqual(r.returncode,0);self.assertIn('incompatible',r.stderr);self.assertEqual(before,digest(p))
    def test_completed_resume_rejected(self):
        r=self.cli('--reanudar');self.assertNotEqual(r.returncode,0);self.assertIn('ya completa',r.stderr)
    def test_cpu_pilot_rejected(self):
        r=self.cli('--etapa','piloto');self.assertNotEqual(r.returncode,0);self.assertIn('CPU solo',r.stderr)
    def test_export_reproduces_without_training(self):
        p=self.folder('R1')/'C0-recuperada';before={n:digest(p/n) for n in ['last.pt','predicciones-val.npy','indices-val.json','exports.json']}
        r=self.cli('--exportar');self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(before,{n:digest(p/n) for n in before})

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['raiz','datos','mascaras','pesos','salida']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--carpeta-tecnica',default='tecnica',help='Subcarpeta de cada pareja; usar . si las ejecuciones están directamente allí')
    ARGS=p.parse_args();e.configure();stream=io.StringIO()
    rr=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Artifacts))
    report={'tests':rr.testsRun,'passed':rr.wasSuccessful(),'failures':len(rr.failures),'errors':len(rr.errors),'gpu_accepted':False,'log':stream.getvalue()}
    ARGS.salida.parent.mkdir(parents=True,exist_ok=True);atomic_json(ARGS.salida,report)
    print(stream.getvalue(),flush=True);raise SystemExit(0 if rr.wasSuccessful() else 1)

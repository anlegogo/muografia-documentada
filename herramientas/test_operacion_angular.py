import json
from pathlib import Path
import shutil
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import test_fusionar_bloques_angular as fixtures
import operar_bloque_angular as worker
from lanzar_campana_angular import launch


class OperationTests(unittest.TestCase):
    def setUp(self):
        f=fixtures.MergeTests('test_correct_aggregation_roundtrip_no_overwrite');f.setUp();self.addCleanup(f.doCleanups)
        self.f=f;self.tree=f.root/'tree';self.out=f.root/'published';self.scratch=f.root/'scratch'
        names=['build-receta/muography_sim','controles-oe1-v3.patch','scripts/simulation/geometry_catalog/geometries/geo-train-01.json']
        names += ['scripts/simulation/geant4_app/tables-az-edges-v1/'+n for n in ('meta.json','p_cdf.txt','row_weights_30d.txt')]
        for name in names:
            p=self.tree/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('fixture '+name)
        self.recipe=f.root/'recipe.json'
        d={'status':'synthetic_test_only','reported_binary_sha256':worker.digest(self.tree/names[0]),'patch_sha256':worker.digest(self.tree/names[1]),
           'geometry_sha256':{'geo-train-01.json':worker.digest(self.tree/names[2])},
           'table_sha256':{Path(n).name:worker.digest(self.tree/n) for n in names[3:]},
           'oe1_controles':json.loads((f.dirs[0]/(f.stem+'.meta.json')).read_text())['oe1_controles'],
           'source_definition':{'type':'fixture'},'normalization':{'S0_30_conventional_days':1000,'physical_days_calibrated':False}}
        self.recipe.write_text(json.dumps(d))
        self.env_seen=None

    def simulate(self,cmd,**kwargs):
        d=Path(cmd[-1]);self.env_seen=kwargs['env']
        m=json.loads((self.f.dirs[0]/(self.f.stem+'.meta.json')).read_text())
        m['seed']=int(cmd[cmd.index('--seed')+1]);m['detected_in_bins']=700
        m.pop('detected_all_energies');m.pop('reference_histogram')
        (d/(self.f.stem+'.meta.json')).write_text(json.dumps(m))
        raw=(self.f.dirs[0]/(self.f.stem+'_hist.csv')).read_bytes()
        (d/(self.f.stem+'_hist.csv')).write_bytes(raw)
        (d/(self.f.stem+'_hist_ecut3.csv')).write_bytes(raw)
        (d/(self.f.stem+'_gen.csv')).write_bytes(raw)
        return SimpleNamespace(returncode=0)

    def work(self):return worker.run(self.f.manifest,0,self.tree,self.scratch,self.out,self.recipe,1,True)

    def test_full_lifecycle_and_no_second_simulation(self):
        with patch.dict('os.environ',{'OE1C_SUBPLANES_M':'999','OE1C_UNKNOWN':'bad'}),patch('operar_bloque_angular.subprocess.run',side_effect=self.simulate) as sim:
            self.assertEqual(self.work()['status'],'published')
            self.assertEqual(self.work()['status'],'already_verified');self.assertEqual(sim.call_count,1)
        self.assertNotIn('OE1C_UNKNOWN',self.env_seen);self.assertNotIn('OE1C_SUBPLANES_M',self.env_seen)

    def test_conventional_time_aggregates_and_wrong_nominal_rejected(self):
        from fusionar_bloques_angular import merge, validate_block
        with patch('operar_bloque_angular.subprocess.run',side_effect=self.simulate):
            self.work();worker.run(self.f.manifest,1,self.tree,self.scratch,self.out,self.recipe,1,True)
        dest=self.f.root/'merged';merge(self.f.manifest,self.out,dest)
        meta=json.loads((dest/'geo-train-01'/(self.f.stem+'.meta.json')).read_text())
        self.assertEqual(meta['nominal_in_window'],1400);self.assertEqual(meta['conventional_exposure_days'],42.)
        gen=self.out/'geo-train-01/view0/block0000'/(self.f.stem+'_gen.csv')
        gen.write_bytes(gen.read_bytes().replace(b'700',b'701'))
        with self.assertRaises(ValueError):validate_block(self.f.rows[0],self.out)

    def test_simulator_failure_preserved_and_unpublished(self):
        with patch('operar_bloque_angular.subprocess.run',return_value=SimpleNamespace(returncode=7)):
            with self.assertRaises(RuntimeError):self.work()
        self.assertFalse(self.out.exists());self.assertTrue(list(self.scratch.rglob('fallo.json')))

    def test_missing_cut_never_published(self):
        def sim(cmd,**kwargs):
            r=self.simulate(cmd,**kwargs);(Path(cmd[-1])/(self.f.stem+'_hist_ecut3.csv')).unlink();return r
        with patch('operar_bloque_angular.subprocess.run',side_effect=sim):
            with self.assertRaises(FileNotFoundError):self.work()
        self.assertFalse(self.out.exists())

    def test_publication_failure_returns_failure(self):
        with patch('operar_bloque_angular.subprocess.run',side_effect=self.simulate),patch('operar_bloque_angular.publish',side_effect=OSError('copy failed')):
            with self.assertRaises(OSError):self.work()
        self.assertFalse(self.out.exists())

    def test_hash_mismatch_prevents_execution(self):
        (self.tree/'build-receta/muography_sim').write_text('changed')
        with patch('operar_bloque_angular.subprocess.run') as sim:
            with self.assertRaises(ValueError):self.work()
            sim.assert_not_called()

    def test_worker_lock_prevents_duplicate_transport(self):
        state=self.out.parent/(self.out.name+'.operacion');state.mkdir()
        (state/'geo-train-01-0-0.worker.lock').write_text('busy')
        with patch('operar_bloque_angular.subprocess.run') as sim:
            with self.assertRaises(FileExistsError):self.work()
            sim.assert_not_called()

    def call_launch(self,submit=False):return launch(self.f.manifest,self.tree,self.scratch,self.out,self.recipe,Path(__import__('sys').executable),1,4,submit)

    def test_dry_run_only_queue_and_commands_have_absolute_worker(self):
        with patch('lanzar_campana_angular.subprocess.run',return_value=SimpleNamespace(stdout='')) as proc:
            r=self.call_launch();self.assertEqual(proc.call_count,1)
        self.assertEqual(len(r['planned']),2)
        cmd=r['planned'][0]['command']
        self.assertTrue(Path(cmd[-3]).is_absolute());self.assertEqual(cmd[-2],worker.digest(self.f.manifest))

    def test_submission_intent_prevents_retry_after_ambiguous_sbatch(self):
        calls=[]
        def proc(cmd,**kwargs):
            calls.append(cmd)
            return SimpleNamespace(stdout='' if cmd[0]=='squeue' else 'ambiguous')
        with patch('lanzar_campana_angular.subprocess.run',side_effect=proc):
            with self.assertRaises(ValueError):self.call_launch(True)
            r=self.call_launch(False)
        self.assertEqual(r['blocked_prior_attempts'],[0])
        self.assertEqual(sum(c[0]=='sbatch' for c in calls),1)

    def test_successful_submission_never_duplicates(self):
        def proc(cmd,**kwargs):return SimpleNamespace(stdout='' if cmd[0]=='squeue' else '12345')
        with patch('lanzar_campana_angular.subprocess.run',side_effect=proc) as mocked:
            self.call_launch(True);r=self.call_launch(True)
        self.assertEqual(r['blocked_prior_attempts'],[0,1])
        self.assertEqual(sum(c.args[0][0]=='sbatch' for c in mocked.call_args_list),2)

    def test_squeue_failure_stops_all_submission(self):
        with patch('lanzar_campana_angular.subprocess.run',side_effect=subprocess.CalledProcessError(1,'squeue')):
            with self.assertRaises(subprocess.CalledProcessError):self.call_launch(True)

    def test_other_campaign_same_destination_rejected(self):
        with patch('lanzar_campana_angular.subprocess.run',return_value=SimpleNamespace(stdout='12')):
            # Valid empty queue for first call, then two successful submissions.
            with patch('lanzar_campana_angular.subprocess.run',side_effect=[SimpleNamespace(stdout=''),SimpleNamespace(stdout='12'),SimpleNamespace(stdout='13')]):self.call_launch(True)
        self.f.rows[0]['semilla']=999;self.f.write_manifest()
        with self.assertRaises(ValueError):self.call_launch()

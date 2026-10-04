"""Controles del orquestador: no ejecutan las redes ni contratan recursos."""
import json,tempfile,sys,unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
import orquestar_borde_cgan as o

class Workflow(unittest.TestCase):
 def command(self,root,phase='tecnica'):
  return ['x','--fase',phase,'--pareja','B1','--datos','d','--mascaras','m','--pesos','p','--raiz',str(root)]
 def test_technical_order_and_gate(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td)
   with patch.object(sys,'argv',self.command(root)+['--cpu-test']),patch.object(o.subprocess,'run',return_value=SimpleNamespace(returncode=0)) as run,patch.object(o.review,'audit_technical',return_value={'gpu_accepted':False,'exact_recovery':True}) as audit:
    o.main()
   self.assertEqual(run.call_count,6)
   calls=[x.args[0] for x in run.call_args_list]
   self.assertNotIn('--reanudar',calls[0]);self.assertIn('--parar-tras',calls[1]);self.assertIn('--reanudar',calls[2])
   self.assertTrue(all('--cpu-test' in c for c in calls))
   self.assertFalse(audit.call_args.kwargs['require_gpu'])
   self.assertTrue((root/'B1/aceptacion-cpu.json').is_file())
 def test_failure_stops_before_gate(self):
  with tempfile.TemporaryDirectory() as td:
   with patch.object(sys,'argv',self.command(Path(td))),patch.object(o.subprocess,'run',return_value=SimpleNamespace(returncode=1)) as run,patch.object(o.review,'audit_technical') as audit:
    with self.assertRaises(RuntimeError):o.main()
   self.assertEqual(run.call_count,1);audit.assert_not_called()
 def test_missing_any_gate_prevents_pilot(self):
  with tempfile.TemporaryDirectory() as td:
   with patch.object(sys,'argv',self.command(Path(td),'piloto')),patch.object(o.subprocess,'run') as run:
    with self.assertRaises(FileNotFoundError):o.main()
   run.assert_not_called()
 def test_old_gate_prevents_pilot(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);(root/'B1').mkdir();(root/'B1/aceptacion-gpu.json').write_text(json.dumps({'schema':'oe2-cgan-ajuste-gate-v1','gpu_accepted':True,'pair':'B1'}))
   with patch.object(sys,'argv',self.command(root,'piloto')),patch.object(o.subprocess,'run') as run:
    with self.assertRaises(ValueError):o.main()
   run.assert_not_called()
 def test_existing_technical_folder_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);(root/'B1/tecnica').mkdir(parents=True)
   with patch.object(sys,'argv',self.command(root)),patch.object(o.subprocess,'run') as run:
    with self.assertRaises(FileExistsError):o.main()
   run.assert_not_called()
 def test_cpu_pilot_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   with patch.object(sys,'argv',self.command(Path(td),'piloto')+['--cpu-test']),patch.object(o.subprocess,'run') as run:
    with self.assertRaises(ValueError):o.main()
   run.assert_not_called()

 def test_different_gpu_environment_prevents_pilot(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td)
   for pair in ['B1','B2','B3']:
    (root/pair).mkdir()
    (root/pair/'aceptacion-gpu.json').write_text(json.dumps({'schema':'oe2-cgan-borde-gate-v1','gpu_accepted':True,'pair':pair,'runs':{},'checkpoint_sha256':{}}))
   identity={'sources':{},'environment':{'gpu':'L40S'},'cache_sha256':'m','data_manifest_sha256':'d','initial_checkpoint_sha256':'i'}
   first={'checkpoint_sha256':{},'identities':[identity]}
   second={'checkpoint_sha256':{},'identities':[{**identity,'environment':{'gpu':'another'}}]}
   with patch.object(sys,'argv',self.command(root,'piloto')),patch.object(o.subprocess,'run') as run,patch.object(o.review,'audit_technical',side_effect=[first,second]):
    with self.assertRaisesRegex(ValueError,'entorno/datos'):o.main()
   run.assert_not_called()

if __name__=='__main__':unittest.main()


"""Controles pequeños del auditor geométrico y del comparador, sin Geant4."""
from pathlib import Path
import json
import tempfile
import unittest
import numpy as np
from auditar_oe1 import pair, containment
from comparar_piloto_oe1 import compare


def sphere(x,r=1):
    return {'kind':'cavity','params':{'cx_m':x,'cy_m':0,'cz_m':5,'radius_m':r}}


class ToolsTest(unittest.TestCase):
    def test_overlap_and_separation(self):
        self.assertIn('demostrada',pair(sphere(0),sphere(1))['estado'])
        self.assertIn('sin intersección',pair(sphere(0),sphere(3))['estado'])
        self.assertAlmostEqual(pair(sphere(0),sphere(3))['separacion_m'],1.)

    def test_protruding_conduit(self):
        a={'kind':'conduit','params':{'cx_m':0,'cy_m':0,'z0_m':0,'z1_m':9,'radius_m':3}}
        self.assertIn('demostrada',containment(a,{'base_radius_m':10,'height_m':10})['estado'])

    def test_comparator_and_inconsistent_budget(self):
        # Fixtures contain synthetic counts only; no project data is copied.
        with tempfile.TemporaryDirectory(prefix='oe1-tooltest-') as folder:
            root=Path(folder)
            for seed in (2026092801,2026092802,2026092803):
                for v in ('original','corregida'):
                    d=root/v/str(seed); d.mkdir(parents=True)
                    h=np.ones((256,256),dtype=int)*(1 if v=='original' else 2)
                    np.savetxt(d/'geo-train-06_view0_hist.csv',h,fmt='%d',delimiter=',')
                    m={'seed':seed,'view_index':0,'geometry_id':'geo-train-06','events_transported':1000000,'detected_in_bins':int(h.sum()),'threads':8,'grid':{},'detector':{},'sampling':'fixture','physics_note':'fixture','engine':'fixture'}
                    (d/'geo-train-06_view0.meta.json').write_text(json.dumps(m))
            r=compare(root)
            self.assertAlmostEqual(r['media_delta_eficiencia'],65536/1000000)
            self.assertEqual(r['desviacion_entre_replicas'],0)
            p=root/'corregida/2026092803/geo-train-06_view0.meta.json'
            m=json.loads(p.read_text()); m['events_transported']=999999; p.write_text(json.dumps(m))
            with self.assertRaises(ValueError): compare(root)


if __name__=='__main__': unittest.main()

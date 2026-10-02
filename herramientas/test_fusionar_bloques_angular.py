"""Fixtures sintéticas; no son simulaciones ni evidencia física."""
import copy
import csv
import json
import unittest
import numpy as np
import test_revisar_smoke_angular as fixtures
from fusionar_bloques_angular import merge, sha


class MergeTests(unittest.TestCase):
    def setUp(self):
        f=fixtures.SmokeReviewTests('test_valid_fixture');f.setUp();self.addCleanup(f.doCleanups)
        self.root=f.root;self.source=self.root/'blocks';self.manifest=self.root/'manifest.csv'
        self.rows=[];self.stem='geo-train-01_view0';self.dirs=[]
        for i in range(2):
            d=self.source/'geo-train-01'/'view0'/f'block{i:04d}';d.mkdir(parents=True);self.dirs.append(d)
            m=copy.deepcopy(f.meta)
            m.update(seed=10+i,engine='synthetic',sampling='fixture',physics_note='not_geant4',
                     detector={'distance_m':1000,'height_m':1.5,'side_m':1.2},wall_seconds=2+i,
                     detected_all_energies=800+i*100,mean_ekin_detected_gev=10+i*10,
                     oe1_controles={'inject':'cone','plane_half_m':300,'margin_deg':5,
                       'edifice_margin_m':50,'ecuts_gev':[3],'subplanes_half_m':[]},reference_histogram='E > 3')
            (d/(self.stem+'.meta.json')).write_bytes(json.dumps(m).encode())
            (d/(self.stem+'_hist.csv')).write_bytes(('\n'.join(','.join(r) for r in f.hist)+'\n').encode())
            (d/'exit_code.txt').write_text('0')
            entries={'scripts/simulation/geometry_catalog/geometries/geo-train-01.json':'a'*64,
                     'build/muography_sim':'b'*64}
            entries.update({'scripts/simulation/geant4_app/tables-az-edges-v1/'+n:'c'*64
                            for n in ['meta.json','p_cdf.txt','row_weights_30d.txt']})
            (d/'entradas.sha256').write_text('\n'.join(h+'  '+n for n,h in entries.items()))
            self.rehash(d)
            self.rows.append({'fila':i,'geometria':'geo-train-01','vista':0,'bloque':i,'semilla':10+i,'eventos':1000})
        self.write_manifest()

    def rehash(self,d):
        names=[self.stem+'_hist.csv',self.stem+'.meta.json']
        (d/'salida.sha256').write_text('\n'.join(sha((d/n).read_bytes())+'  '+n for n in names))

    def write_manifest(self):
        with self.manifest.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['fila','geometria','vista','bloque','semilla','eventos'])
            w.writeheader();w.writerows(self.rows)

    def reject(self,**kwargs):
        out=self.root/'rejected'
        with self.assertRaises((ValueError,KeyError)):
            merge(self.manifest,self.source,out,**kwargs)
        self.assertFalse(out.exists())

    def test_correct_aggregation_roundtrip_no_overwrite(self):
        out=self.root/'result';r=merge(self.manifest,self.source,out)
        m=json.loads((out/'geo-train-01'/(self.stem+'.meta.json')).read_text())
        self.assertEqual((m['events_transported'],m['detected_in_bins'],m['detected_all_energies']),(2000,1400,1700))
        self.assertEqual(m['seconds_per_event'],5/2000)
        self.assertAlmostEqual(m['mean_ekin_all_energies_gev'],(800*10+900*20)/1700)
        self.assertNotIn('mean_ekin_detected_gev',m)
        self.assertEqual(m['block_seeds'],[10,11]);self.assertFalse(r['physical_validation'])
        with self.assertRaises(FileExistsError):merge(self.manifest,self.source,out)

    def test_duplicate_block_rejected(self):
        self.rows[1]=dict(self.rows[0]);self.rows[1]['fila']=9;self.rows[1]['semilla']=99
        self.write_manifest();self.reject()

    def test_reused_seed_rejected(self):
        self.rows[1]['semilla']=self.rows[0]['semilla'];self.write_manifest();self.reject()

    def test_wrong_seed_rejected(self):
        self.rows[1]['semilla']=999;self.write_manifest();self.reject()

    def test_wrong_events_rejected(self):
        self.rows[1]['eventos']=999;self.write_manifest();self.reject()

    def test_mixed_recipe_rejected(self):
        p=self.dirs[1]/(self.stem+'.meta.json');m=json.loads(p.read_text());m['oe1_controles']['inject']='legacy'
        p.write_text(json.dumps(m));self.rehash(p.parent);self.reject()

    def test_bad_counts_rejected_even_with_new_hash(self):
        p=self.dirs[1]/(self.stem+'_hist.csv');p.write_text('0,1\n');self.rehash(p.parent);self.reject()

    def test_missing_hash_rejected(self):
        (self.dirs[1]/'salida.sha256').write_text('');self.reject()

    def test_failed_exit_rejected(self):
        (self.dirs[1]/'exit_code.txt').write_text('2');self.reject()

    def test_line_endings_explicit_and_recorded(self):
        p=self.dirs[0]/(self.stem+'_hist.csv');p.write_bytes(p.read_bytes().replace(b'\n',b'\r\n'))
        received=p.read_bytes();self.reject()
        r=merge(self.manifest,self.source,self.root/'converted',True)
        self.assertTrue(r['views'][0]['blocks'][0]['outputs'][0]['crlf_to_lf_verified'])
        self.assertEqual(p.read_bytes(),received)

    def test_conversion_does_not_hide_changed_values(self):
        p=self.dirs[0]/(self.stem+'_hist.csv');p.write_bytes(p.read_bytes().replace(b'700',b'699').replace(b'\n',b'\r\n'))
        self.reject(accept_crlf=True)


if __name__=='__main__':unittest.main()

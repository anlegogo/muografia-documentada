import copy
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
import test_revisar_smoke_angular as fixtures
from preparar_imagen_angular_v1 import coordinates
from empaquetar_angular_v1 import audit,package,low_counts,sha


class PackageTests(unittest.TestCase):
    def setUp(self):
        f=fixtures.SmokeReviewTests('test_valid_fixture');f.setUp();self.addCleanup(f.doCleanups)
        self.root=f.root;self.paths=[]
        m=f.meta
        m.update(geometry_sha256='a'*64,binary_sha256='b'*64,
                 table_sha256={k:'c'*64 for k in ['meta.json','p_cdf.txt','row_weights_30d.txt']},
                 engine='test_only',sampling='synthetic_fixture',physics_note='not_geant4',
                 detector={'side_m':1.2,'distance_m':1000,'height_m':1.5})
        coords=coordinates(m)
        for view in range(6):
            p=self.root/f'geo-train-01_view{view}.npz'
            counts=np.zeros((256,256),np.uint32);counts[2,3]=100+view
            np.savez_compressed(p,counts_ref=counts,**coords)
            meta=copy.deepcopy(m);meta.update(view_index=view,detected_in_bins=100+view,npz_sha256=sha(p))
            p.with_suffix('.meta.json').write_text(json.dumps(meta));self.paths.append(p)

    def test_complete_inventory(self):
        r,_=audit(self.paths,['geo-train-01']);self.assertTrue(r['technical_complete']);self.assertEqual(r['target_pairs'],480)

    def controlled(self):
        for p in self.paths:
            mp=p.with_suffix('.meta.json');m=json.loads(mp.read_text())
            m['oe1_controles']={'inject':'cone','plane_half_m':300,'margin_deg':5,
                               'edifice_margin_m':50,'ecuts_gev':[3],'subplanes_half_m':[]}
            m['reference_histogram']='kinetic energy at the counting plane > 3 GeV'
            mp.write_text(json.dumps(m))

    def test_controlled_inventory(self):
        self.controlled()
        self.assertTrue(audit(self.paths,['geo-train-01'])[0]['technical_complete'])

    def test_changed_recipe_rejected(self):
        self.controlled();p=self.paths[0].with_suffix('.meta.json');base=json.loads(p.read_text())
        for key,value in [('inject','legacy'),('plane_half_m',600),('margin_deg',2),('ecuts_gev',[5])]:
            with self.subTest(key=key):
                m=copy.deepcopy(base);m['oe1_controles'][key]=value;p.write_text(json.dumps(m))
                self.assertFalse(audit(self.paths,['geo-train-01'])[0]['technical_complete'])

    def test_reference_source_normalization_changes_rejected(self):
        self.controlled();p=self.paths[0].with_suffix('.meta.json');base=json.loads(p.read_text())
        for key,value in [('reference_histogram','all energies'),('source_definition',{'surface':'new'}),
                          ('normalization',{'area':'vertical'})]:
            with self.subTest(key=key):
                m=copy.deepcopy(base);m[key]=value;p.write_text(json.dumps(m))
                self.assertFalse(audit(self.paths,['geo-train-01'])[0]['technical_complete'])

    def test_missing_or_invalid_controls_rejected(self):
        self.controlled();p=self.paths[0].with_suffix('.meta.json');base=json.loads(p.read_text())
        for value in [None,{},dict(base['oe1_controles'],margin_deg=float('nan'))]:
            with self.subTest(value=value):
                m=copy.deepcopy(base);m['oe1_controles']=value;p.write_text(json.dumps(m))
                self.assertTrue(audit(self.paths,['geo-train-01'])[0]['errors'])

    def test_missing_views(self):
        r,_=audit(self.paths[:1],['geo-train-01']);self.assertFalse(r['technical_complete']);self.assertEqual(len(r['missing']),5)

    def test_mixed_binary(self):
        p=self.paths[0].with_suffix('.meta.json');m=json.loads(p.read_text());m['binary_sha256']='d'*64;p.write_text(json.dumps(m))
        self.assertFalse(audit(self.paths,['geo-train-01'])[0]['technical_complete'])

    def test_corrupt_reference(self):
        with self.paths[0].open('ab') as f:f.write(b'changed')
        self.assertTrue(audit(self.paths,['geo-train-01'])[0]['errors'])

    def test_duplicate_and_extra_geometry(self):
        self.assertTrue(audit(self.paths+[self.paths[0]],['geo-train-01'])[0]['errors'])
        self.assertTrue(audit(self.paths,['geo-train-02'])[0]['errors'])

    def test_incomplete_does_not_write(self):
        dest=self.root/'incomplete'
        with self.assertRaises(ValueError):package(self.paths[:1],['geo-train-01'],dest)
        self.assertFalse(dest.exists())

    def test_thinning_reproducible_and_no_uint16_clipping(self):
        ref=np.full((3,4),200000,np.uint32)
        a=low_counts(ref,'geo-train-01',0)
        np.testing.assert_array_equal(a,low_counts(ref,'geo-train-01',0))
        self.assertFalse(np.array_equal(a,low_counts(ref,'geo-train-01',1)))
        self.assertEqual(a.dtype,np.uint32);self.assertGreater(a[0].min(),65535)
        self.assertTrue(np.all(a<=ref))
        # Aggregate expectation: f*N, checked against a generous fixed 6-sigma bound.
        for fi,f in enumerate([.5,.1,.05,.01]):
            self.assertLess(abs(a[fi].mean()-200000*f),6*np.sqrt(200000*f*(1-f)/(20*12)))

    def test_package_roundtrip_and_no_overwrite(self):
        out=self.root/'package';r=package(self.paths,['geo-train-01'],out)
        self.assertEqual(len(r['files']),6);self.assertFalse(r['physical_validation'])
        with np.load(out/r['files'][0]['name']) as z:
            self.assertEqual(z['low_counts'].shape,(4,20,256,256))
            np.testing.assert_array_equal(z['low_counts'],low_counts(z['counts_ref'],'geo-train-01',0))
        with self.assertRaises(FileExistsError):package(self.paths,['geo-train-01'],out)


if __name__=='__main__':unittest.main()

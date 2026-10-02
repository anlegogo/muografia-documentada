import json
import tempfile
from pathlib import Path
import unittest
import numpy as np
import test_revisar_smoke_angular as fixtures
from analizar_roi_angular_v1 import analyze,sha
from preparar_imagen_angular_v1 import coordinates


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        f=fixtures.SmokeReviewTests('test_valid_fixture');f.setUp();self.addCleanup(f.doCleanups)
        self.root=f.root;self.meta=f.meta
        self.meta.update(geometry_id='geo-train-06',geometry_sha256='a'*64,
                         detector={'distance_m':1000,'height_m':1.5},detected_in_bins=18)
        self.coords=coordinates(self.meta)
        self.counts=np.zeros((256,256),np.uint32);self.counts[2,3]=7;self.counts[5,6]=11
        self.length=np.zeros((256,256));self.length[2,3]=25
        self.spec=dict(geometry_id='geo-train-06',geometry_sha256='a'*64,grid=self.meta['grid'],
                       detector_distance_m=1000,detector_height_m=1.5,threshold_m=20,
                       views=[dict(view=0,pixels_new=1)])
        self.image=self.root/'geo-train-06_view0.npz';self.roi=self.root/'geo-train-06_view0_roi.npz'
        self.write()

    def write(self):
        np.savez(self.image,counts_ref=self.counts,**self.coords)
        np.savez(self.roi,roi_z_ge20m=self.length>=20,length_z_m=self.length,**self.coords)
        self.meta['npz_sha256']=sha(self.image);self.spec['views'][0]['roi_npz_sha256']=sha(self.roi)
        self.image.with_suffix('.meta.json').write_text(json.dumps(self.meta))
        (self.root/'revision-roi.json').write_text(json.dumps(self.spec))

    def test_known_counts(self):
        r=analyze(self.image,self.root)
        self.assertEqual((r['counts_total'],r['counts_roi'],r['counts_outside_roi']),(18,7,11))
        self.assertAlmostEqual(r['fraction_of_detected_in_roi'],7/18)

    def test_rejects_identity_and_detector_changes(self):
        for key,value in [('geometry_id','geo-train-01'),('geometry_sha256','b'*64),('view_index',1),
                          ('detector',{'distance_m':900,'height_m':1.5})]:
            with self.subTest(key=key):
                old=self.meta[key];self.meta[key]=value;self.write()
                with self.assertRaises(ValueError):analyze(self.image,self.root)
                self.meta[key]=old

    def test_missing_geometry_hash(self):
        self.meta.pop('geometry_sha256');self.write()
        with self.assertRaises(ValueError):analyze(self.image,self.root)

    def test_corrupt_file(self):
        with self.image.open('ab') as f:f.write(b'changed')
        with self.assertRaises(ValueError):analyze(self.image,self.root)

    def test_shifted_coordinates_even_with_valid_hash(self):
        self.coords['az_centers_deg']+=.01;self.write()
        with self.assertRaises(ValueError):analyze(self.image,self.root)

    def test_false_mask_size(self):
        self.spec['views'][0]['pixels_new']=2;self.write()
        with self.assertRaises(ValueError):analyze(self.image,self.root)

    def test_zero_counts(self):
        self.counts[:]=0;self.meta['detected_in_bins']=0;self.write()
        self.assertIsNone(analyze(self.image,self.root)['fraction_of_detected_in_roi'])

    def test_negative_lengths(self):
        self.length[0,0]=-1;self.write()
        with self.assertRaises(ValueError):analyze(self.image,self.root)


if __name__=='__main__':unittest.main()

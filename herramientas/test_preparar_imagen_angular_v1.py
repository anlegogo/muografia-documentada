import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from preparar_imagen_angular_v1 import export, coordinates
import test_revisar_smoke_angular as fixtures


class ImageExportTests(unittest.TestCase):
    def setUp(self):
        self.fixture=fixtures.SmokeReviewTests('test_valid_fixture')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.run_review()
        self.hist=self.fixture.root/'geo-train-01_view0_hist.csv'
        self.target=self.fixture.root/'export'

    def test_roundtrip_preserves_pixels_and_coordinates(self):
        report=export([self.hist],self.target)
        self.assertEqual(report['images'][0]['total'],700)
        with np.load(self.target/'geo-train-01_view0.npz') as z:
            self.assertEqual(z['counts_ref'][1,1],700)
            self.assertEqual(np.count_nonzero(z['counts_ref']),1)
            self.assertEqual(z['az_centers_deg'][0],-29.8828125)
            self.assertEqual(z['az_edges_deg'][-1],30)
            np.testing.assert_allclose(np.diff(z['az_edges_deg']),60/256)
            np.testing.assert_allclose(z['el_centers_deg'],np.linspace(2,47,256))

    def test_rejects_legacy_before_writing(self):
        self.fixture.meta['grid'].pop('azimuth_convention');self.fixture.run_review()
        with self.assertRaises(ValueError):export([self.hist],self.target)
        self.assertFalse(self.target.exists())

    def test_rejects_inconsistent_grid(self):
        self.fixture.meta['grid']['az_step_deg']=60/255
        with self.assertRaises(ValueError):coordinates(self.fixture.meta)

    def test_rejects_uint32_overflow(self):
        self.fixture.hist[1][1]=str(2**32);self.fixture.run_review()
        with self.assertRaises(ValueError):export([self.hist],self.target)

    def test_rejects_overwrite(self):
        export([self.hist],self.target)
        with self.assertRaises(FileExistsError):export([self.hist],self.target)

    def test_rejects_duplicate_view(self):
        with self.assertRaises(ValueError):export([self.hist,self.hist],self.target)
        self.assertFalse(self.target.exists())

    def test_rejects_mixed_batch_without_partial_output(self):
        other=self.fixture.root/'other_hist.csv';other.write_bytes(self.hist.read_bytes())
        meta=dict(self.fixture.meta,grid={})
        other.with_name('other.meta.json').write_text(json.dumps(meta))
        with self.assertRaises(ValueError):export([self.hist,other],self.target)
        self.assertFalse(self.target.exists())


if __name__=='__main__':unittest.main()

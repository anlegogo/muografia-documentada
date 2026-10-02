"""Pruebas sintéticas del revisor; no son resultados Geant4."""
import json
from pathlib import Path
import tempfile
import unittest
from revisar_smoke_angular import review


class SmokeReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.meta = {'geometry_id':'geo-train-01','view_index':0,'seed':2026100107,'threads':1,
                     'events_transported':1000,'ecomug_draws_total':1000,'detected_in_bins':700,
                     'exposure_days':-1,'grid':{'azimuth_convention':'az-edges-v1',
                     'n_az':256,'n_el':256,'az_edges_deg':[-30,30],'az_step_deg':60/256,
                     'az_first_center_deg':-29.8828125,'az_half_deg':30,'el_min_deg':2,'el_max_deg':47,
                     'elevation_convention':'legacy-centers-2-47'}}
        self.hist = [['0']*256 for _ in range(256)]
        self.hist[1][1] = '700'
        (self.root/'run.log').write_text('RUN DONE geo-train-01 view 0\n')
        (self.root/'exit_code.txt').write_text('0\n')

    def run_review(self):
        (self.root/'geo-train-01_view0.meta.json').write_text(json.dumps(self.meta))
        (self.root/'geo-train-01_view0_hist.csv').write_text('\n'.join(','.join(r) for r in self.hist))
        return review(self.root)

    def test_valid_fixture(self):
        self.assertEqual(self.run_review()['estado'], 'conforme_control_tecnico')

    def test_old_grid(self):
        self.meta['grid']['azimuth_convention']='old'
        self.assertEqual(self.run_review()['estado'], 'requiere_revision')

    def test_wrong_count_and_noninteger_metadata(self):
        for value in [999, 1000.0, True]:
            with self.subTest(value=value):
                self.meta['events_transported']=value
                self.assertEqual(self.run_review()['estado'], 'requiere_revision')

    def test_invalid_histogram(self):
        for value in ['-1','1.5','NaN','1001','699']:
            with self.subTest(value=value):
                self.hist[1][1]=value
                self.assertEqual(self.run_review()['estado'], 'requiere_revision')

    def test_truncated_histogram(self):
        self.hist.pop()
        self.assertEqual(self.run_review()['estado'], 'requiere_revision')

    def test_failed_exit(self):
        (self.root/'exit_code.txt').write_text('2')
        self.assertEqual(self.run_review()['estado'], 'requiere_revision')

    def test_error_in_completed_log(self):
        with (self.root/'run.log').open('a') as f:f.write('G4Exception GeomVol1002\n')
        self.assertEqual(self.run_review()['estado'], 'requiere_revision')

    def test_missing_log(self):
        (self.root/'run.log').unlink()
        self.assertEqual(self.run_review()['estado'], 'requiere_revision')


if __name__ == '__main__':
    unittest.main()

import copy
import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from evaluar_piloto_angular import review


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.plan_path=self.root/'diseno.json';self.ref_path=self.root/'ref.json'
        self.plan={'geometry':'geo-train-06','views':[],'events_per_view':6553600000,'blocks_per_view':1,'alpha_per_view':.05/6,
                   'source_table_sha256':{'a':'b'},'geometry_sha256':'geo','mask_sha256':{},'roi_definition':'synthetic fixture'}
        np.save(self.root/'sky.npy',np.ones((256,256),bool));np.save(self.root/'roi.npy',np.ones((64,64),bool))
        for n in ('sky.npy','roi.npy'):self.plan['mask_sha256'][n]=hashlib.sha256((self.root/n).read_bytes()).hexdigest()
        with (self.root/'manifiesto-piloto-propuesto.csv').open('w',newline='') as f:
            writer=csv.writer(f);writer.writerow(['fila','geometria','vista','bloque','semilla','eventos'])
            for v in range(6):
                self.plan['views'].append({'view':v,'sky_mask':'sky.npy','rock_roi_mask':'roi.npy'})
                writer.writerow([v,'geo-train-06',v,0,100+v,self.plan['events_per_view']])
        self.plan['manifest_sha256']=hashlib.sha256((self.root/'manifiesto-piloto-propuesto.csv').read_bytes()).hexdigest()
        self.plan_path.write_text(json.dumps(self.plan))
        self.ref={'margin_deg':5,'kinetic_cut_gev':3,'table_sha256':{'a':'b'},'nominal_probability_per_pixel_by_row':[1/65536]*256,'ideal_selected_probability_per_pixel_by_row':[.5/65536]*256}
        self.ref_path.write_text(json.dumps(self.ref))

    def read(self,path):
        v=int(path.stem.split('view')[1].split('_')[0])
        meta={'events_transported':self.plan['events_per_view'],'geometry_sha256':'geo','table_sha256':{'a':'b'},
              'oe1_controles':{'inject':'cone','plane_half_m':300,'edifice_margin_m':50,'margin_deg':5,'ecuts_gev':[3],'subplanes_half_m':[]},
              'reference_histogram':'kinetic energy at the counting plane > 3 GeV','block_seeds':[100+v]}
        return '',np.full((256,256),50000,dtype=np.uint32),{},meta,{}

    def test_complete_synthetic_pilot_not_production_approval(self):
        with patch('evaluar_piloto_angular.read_image',side_effect=self.read):r=review(self.root,self.plan_path,self.ref_path)
        self.assertTrue(r['all_border_regions_equivalent']);self.assertFalse(r['production_authorized'])
        self.assertEqual(len(r['views']),6);self.assertEqual(r['views'][0]['rock_roi']['median_counts'],800000)

    def test_changed_mask_rejected(self):
        np.save(self.root/'sky.npy',np.zeros((256,256),bool))
        with patch('evaluar_piloto_angular.read_image',side_effect=self.read):
            with self.assertRaises(ValueError):review(self.root,self.plan_path,self.ref_path)

    def test_wrong_seed_or_budget_rejected(self):
        for key,val in [('block_seeds',[999]),('events_transported',1000)]:
            def altered(p):
                r=list(self.read(p));r[3][key]=val;return r
            with patch('evaluar_piloto_angular.read_image',side_effect=altered):
                with self.assertRaises(ValueError):review(self.root,self.plan_path,self.ref_path)

    def test_wrong_reference_rejected(self):
        self.ref['margin_deg']=0;self.ref_path.write_text(json.dumps(self.ref))
        with self.assertRaises(ValueError):review(self.root,self.plan_path,self.ref_path)

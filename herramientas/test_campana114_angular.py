"""Controles de integridad y de ausencia de aprobación automática."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from evaluar_campana_114 import review
from fusionar_bloques_angular import manifest_rows

ROOT=Path(__file__).resolve().parents[1]

class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.base=self.root/'design'
        shutil.copytree(ROOT/'objetivo-1/evidencias/preparacion-campana-114',self.base)
        self.plan=self.base/'plan.json';self.data=json.loads(self.plan.read_text())
        self.recipe=ROOT/'objetivo-1/contratos/receta-operativa-siete-actividades.json'
        self.ref=ROOT/'objetivo-1/evidencias/preparacion-siete-actividades/cielo-ideal-margen-5.json'
        self.fusion=self.root/'fusion';self.fusion.mkdir()

    def run_review(self):return review(self.fusion,self.plan,self.recipe,self.ref)

    def test_empty_campaign_never_passes(self):
        result=self.run_review()
        self.assertEqual(len(result['missing']),114)
        for key in ('technical_complete','all_border_criteria_met','all_rock_descriptive_criteria_met','production_authorized'):
            self.assertFalse(result[key])

    def test_changed_inputs_rejected(self):
        for name in ('manifiesto-114-344M.csv',self.data['geometries'][0]['sky']):
            path=self.base/name;original=path.read_bytes();path.write_bytes(original+b'x')
            with self.assertRaises(ValueError):self.run_review()
            path.write_bytes(original)

    def test_valid_view_and_wrong_seed_or_budget(self):
        g=self.data['geometries'][0];gid=g['geometry'];dest=self.fusion/gid;dest.mkdir()
        (dest/(gid+'_view0_hist.csv')).touch()
        recipe=json.loads(self.recipe.read_text())
        rows=manifest_rows(self.base/'manifiesto-114-344M.csv')
        meta={k:recipe[k] for k in ['table_sha256','oe1_controles','source_definition','normalization','reference_histogram']}
        meta.update(events_transported=344000000,geometry_sha256=g['geometry_sha256'],binary_sha256=recipe['reported_binary_sha256'],
            block_seeds=[r['semilla'] for r in rows if r['geometria']==gid and r['vista']==0],grid={},engine='synthetic test',sampling='fixed',physics_note='synthetic only',detector={'side_m':1.2,'distance_m':1000,'height_m':1.5},exposure_days=-1)
        for field,value in [(None,None),('events_transported',211000000),('block_seeds',[1]),('binary_sha256','wrong')]:
            m=copy.deepcopy(meta)
            if field:m[field]=value
            with patch('evaluar_campana_114.read_image',return_value=('',np.ones((256,256),dtype=np.uint32),{},m,{})):
                result=self.run_review()
            self.assertEqual(len(result['views']),0 if field else 1)
            self.assertEqual(len(result['errors']),1 if field else 0)
            self.assertFalse(result['technical_complete']);self.assertFalse(result['production_authorized'])

if __name__=='__main__':unittest.main()

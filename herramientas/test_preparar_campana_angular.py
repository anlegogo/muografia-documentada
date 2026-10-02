import csv
import json
from pathlib import Path
import tempfile
import unittest
from preparar_campana_angular import preflight
import test_fusionar_bloques_angular as fixtures


class CampaignTests(unittest.TestCase):
    def setUp(self):
        f=fixtures.MergeTests('test_correct_aggregation_roundtrip_no_overwrite');f.setUp();self.addCleanup(f.doCleanups)
        self.f=f

    def test_existing_blocks_verified_but_scope_incomplete(self):
        r=preflight(self.f.manifest,['geo-train-01'],self.f.source)
        self.assertEqual([b['state'] for b in r['blocks']],['verified','verified'])
        self.assertEqual(len(r['missing_views']),5);self.assertFalse(r['submission_authorized'])

    def test_corrupt_not_considered_published(self):
        p=self.f.dirs[0]/(self.f.stem+'_hist.csv');p.write_text('broken')
        r=preflight(self.f.manifest,['geo-train-01'],self.f.source)
        self.assertEqual(r['blocks'][0]['state'],'invalid');self.assertTrue(r['errors'])

    def test_manifest_identity_changes_with_budget(self):
        old=preflight(self.f.manifest,['geo-train-01'])['campaign_id']
        self.f.rows[0]['eventos']=1001;self.f.write_manifest()
        self.assertNotEqual(old,preflight(self.f.manifest,['geo-train-01'])['campaign_id'])

    def test_complete_six_views_offline_not_authorized(self):
        self.f.rows=[{'fila':v,'geometria':'geo-train-01','vista':v,'bloque':0,'semilla':100+v,'eventos':1000} for v in range(6)]
        self.f.write_manifest();r=preflight(self.f.manifest,['geo-train-01'])
        self.assertTrue(r['technical_manifest_complete']);self.assertFalse(r['all_blocks_verified'])
        self.assertFalse(r['submission_authorized']);self.assertEqual(r['total_events'],6000)

    def test_missing_block_index_rejected(self):
        self.f.rows[1]['bloque']=3;self.f.write_manifest()
        self.assertTrue(preflight(self.f.manifest,['geo-train-01'])['errors'])

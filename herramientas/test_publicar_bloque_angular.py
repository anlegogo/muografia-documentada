import json
from pathlib import Path
from unittest.mock import patch
import unittest
import test_fusionar_bloques_angular as fixtures
from publicar_bloque_angular import publish,inventory,RECEIPT


class PublicationTests(unittest.TestCase):
    def setUp(self):
        f=fixtures.MergeTests('test_correct_aggregation_roundtrip_no_overwrite');f.setUp();self.addCleanup(f.doCleanups)
        self.f=f;self.out=f.root/'published';self.target=self.out/'geo-train-01/view0/block0000'

    def run_publish(self):return publish(self.f.manifest,0,self.f.source,self.out)

    def test_success_and_idempotence(self):
        before=inventory(self.f.dirs[0]);r=self.run_publish()
        self.assertEqual(r['status'],'published');self.assertEqual(inventory(self.target,True),before)
        self.assertEqual(self.run_publish()['status'],'already_verified')
        self.assertEqual(inventory(self.f.dirs[0]),before)

    def test_copy_failure_never_publishes(self):
        with patch('publicar_bloque_angular.shutil.copyfile',side_effect=OSError('simulated disk full')):
            with self.assertRaises(OSError):self.run_publish()
        self.assertFalse(self.target.exists())
        self.assertTrue(list(self.target.parent.glob('.publication-stage-*')))

    def test_corrupted_copy_never_publishes(self):
        def corrupt(src,dst):dst.write_bytes(b'corrupt')
        with patch('publicar_bloque_angular.shutil.copyfile',side_effect=corrupt):
            with self.assertRaises(ValueError):self.run_publish()
        self.assertFalse(self.target.exists())

    def test_promotion_failure_never_publishes(self):
        with patch('publicar_bloque_angular.Path.rename',side_effect=OSError('simulated rename failure')):
            with self.assertRaises(OSError):self.run_publish()
        self.assertFalse(self.target.exists())

    def test_receipt_write_failure_never_publishes(self):
        original=Path.write_bytes
        def fail_receipt(path,data):
            if path.name==RECEIPT:raise OSError('simulated receipt write failure')
            return original(path,data)
        with patch('publicar_bloque_angular.Path.write_bytes',new=fail_receipt):
            with self.assertRaises(OSError):self.run_publish()
        self.assertFalse(self.target.exists())

    def test_invalid_exit_never_publishes(self):
        (self.f.dirs[0]/'exit_code.txt').write_text('1')
        with self.assertRaises(ValueError):self.run_publish()
        self.assertFalse(self.target.exists())

    def test_existing_modified_block_not_overwritten(self):
        self.run_publish();p=self.target/(self.f.stem+'_hist.csv');p.write_bytes(b'changed')
        with self.assertRaises(ValueError):self.run_publish()
        self.assertEqual(p.read_bytes(),b'changed')

    def test_lock_prevents_second_publisher(self):
        self.target.parent.mkdir(parents=True)
        lock=self.target.with_name(self.target.name+'.publication.lock');lock.write_text('other-writer')
        with self.assertRaises(FileExistsError):self.run_publish()
        self.assertEqual(lock.read_text(),'other-writer');self.assertFalse(self.target.exists())

    def test_nested_roots_rejected(self):
        with self.assertRaises(ValueError):publish(self.f.manifest,0,self.f.source,self.f.source/'nested')

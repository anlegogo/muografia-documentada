"""Pruebas de localización del diagnóstico, sin entrenamiento ni GPU."""
import json,tempfile,unittest
from pathlib import Path
import numpy as np
import torch
from diagnosticar_recuperacion_cgan import fingerprint,compare,compare_runs

class DiagnosticTests(unittest.TestCase):
    def test_exact(self):
        x={"model":torch.tensor([1.,2.]),"rng":torch.tensor([1,2],dtype=torch.uint8),"step":3}
        self.assertTrue(compare(fingerprint(x),fingerprint(x))["values_equal"])
    def test_weight(self):
        a=fingerprint({"weight":torch.tensor([1.])})
        b=fingerprint({"weight":torch.tensor([1.000001])})
        self.assertEqual(compare(a,b)["different_values"],["/weight"])
    def test_rng(self):
        a=fingerprint({"rng":torch.tensor([1],dtype=torch.uint8)})
        b=fingerprint({"rng":torch.tensor([2],dtype=torch.uint8)})
        self.assertFalse(compare(a,b)["values_equal"])
    def test_metadata_separate(self):
        a=fingerprint(torch.tensor([1.]))
        b=json.loads(json.dumps(a));b[""]["device"]="cuda:0"
        r=compare(a,b);self.assertTrue(r["values_equal"]);self.assertFalse(r["metadata_equal"])
    def test_optimizer_counter(self):
        self.assertFalse(compare(fingerprint({"step":torch.tensor(5.)}),
                                 fingerprint({"step":torch.tensor(6.)}))["values_equal"])
    def test_first_event(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"a",Path(d)/"b"
            for root in (a,b):
                root.mkdir()
                for name,value in [("identity.json",{"arm":"C0"}),("boundary-live.json",{}),("validation.json",{"ssim":.8})]:
                    (root/name).write_text(json.dumps(value))
                np.save(root/"predicciones-val.npy",np.zeros((1,2,2),dtype=np.float32))
            events=[{"event":"forward","leaves":fingerprint(torch.tensor([1.]))},
                    {"event":"gradients","leaves":fingerprint(torch.tensor([2.]))}]
            (a/"trace.jsonl").write_text("\n".join(map(json.dumps,events)))
            events[1]["leaves"]=fingerprint(torch.tensor([3.]))
            (b/"trace.jsonl").write_text("\n".join(map(json.dumps,events)))
            r=compare_runs(a,b);self.assertEqual(r["first_difference"]["event"],"gradients")
            (b/"trace.jsonl").write_text(json.dumps(events[0]))
            with self.assertRaises(ValueError):compare_runs(a,b)
    def test_missing_leaf(self):
        self.assertFalse(compare(fingerprint({"step":2}),{})["values_equal"])

if __name__=="__main__":unittest.main()

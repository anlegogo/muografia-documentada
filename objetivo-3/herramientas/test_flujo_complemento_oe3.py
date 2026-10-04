"""Flujo de exportación con red identidad sintética; no son resultados físicos."""
import unittest,tempfile,json,hashlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
import torch
import complemento_oe3 as c

class CounterNet(torch.nn.Module):
    def __init__(self):super().__init__();self.calls=0
    def forward(self,x):self.calls+=1;return x
def check(ok,msg):
    if not ok:raise ValueError(msg)
def read(p):return json.loads(Path(p).read_text())
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

class Workflow(unittest.TestCase):
 def test_export_resume_and_reject_corruption_and_identity(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);spec=root/'spec.json';write(spec,{'fixture':True});weights=root/'weights.json';write(weights,{'m':'fake'})
   a=SimpleNamespace(output=root/'outputs',model='m',device='cpu',spec=spec,weights=weights,repo=root)
   a.output.mkdir();net=CounterNet()
   e=SimpleNamespace(check=check,read=read,write=write,sha=sha,env=lambda:{'fixture':True},load_net=lambda *args:net,invert=lambda z,s:check(np.isfinite(z).all(),'finite'))
   s={'models':{'m':{'sha256':'fixture'}},'geometry_order':['fixture-geometry'],'normalization_scale':1}
   p={'new_fractions':[.1]};signature='fixture'
   ident=c.identity(a,e,s,signature,'m',.05);write(a.output/'smoke-m.json',{'passed':True,'identity':ident})
   x=np.full((120,8,8),.25,dtype=np.float32)
   with patch.object(c,'preflight',return_value={}),patch.object(c,'fraction_input',return_value=x):
    c.infer(a,e,s,signature,p);self.assertEqual(net.calls,30)
    c.infer(a,e,s,signature,p);self.assertEqual(net.calls,30)
    path=a.output/'f010/m/fixture-geometry.npy';pred=np.load(path);np.testing.assert_array_equal(pred,x)
    original=path.read_bytes();path.write_bytes(b'corrupted')
    with self.assertRaisesRegex(ValueError,'incompatible'):c.infer(a,e,s,signature,p)
    path.write_bytes(original)
    write(a.output/'f010/m/identity.json',{'different':True})
    with self.assertRaisesRegex(ValueError,'Identidad'):c.infer(a,e,s,signature,p)
 def test_missing_smoke_stops_before_export(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);write(root/'spec.json',{'fixture':True})
   a=SimpleNamespace(output=root,model='m',device='cpu',spec=root/'spec.json')
   e=SimpleNamespace(check=check,read=read,sha=sha,env=lambda:{'fixture':True})
   s={'models':{'m':{'sha256':'fixture'}}}
   with patch.object(c,'preflight',return_value={}):
    with self.assertRaises(FileNotFoundError):c.infer(a,e,s,'fixture',{'new_fractions':[.1]})
   self.assertFalse((root/'f010').exists())
if __name__=='__main__':unittest.main()

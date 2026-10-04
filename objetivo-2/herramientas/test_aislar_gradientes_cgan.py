"""Controles matemáticos y de conservación del diagnóstico CG-04b."""
import copy,unittest
import torch
import aislar_gradientes_cgan as d
import ejecutar_ajuste_cgan as e
from diagnosticar_recuperacion_cgan import fingerprint,pack

class Critic(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.w=torch.nn.Parameter(torch.tensor(.7,dtype=torch.float64))
        self.b=torch.nn.Parameter(torch.tensor(.2,dtype=torch.float64))
    def forward(self,x,y):return self.w*y+self.b
class Generator(torch.nn.Module):
    def __init__(self):
        super().__init__();self.w=torch.nn.Parameter(torch.tensor(.4,dtype=torch.float64))
    def forward(self,x):return self.w*x

def setup():
    G=Generator();D=Critic()
    return G,D,torch.optim.Adam(G.parameters()),torch.optim.Adam(D.parameters())

def batch():
    x=torch.arange(8,dtype=torch.float64).reshape(2,1,2,2)/10
    return x,x+.3,x,torch.ones_like(x)

class Tests(unittest.TestCase):
    def test_missing_none(self):
        self.assertFalse(d.exact_values({"/x":None},{}))
    def test_metadata(self):
        a=fingerprint(torch.tensor([1.]));b=copy.deepcopy(a);b[""]["device"]="cuda:0"
        self.assertTrue(d.exact_values(a,b))
    def test_values(self):
        self.assertFalse(d.exact_values(fingerprint(torch.tensor(1.)),fingerprint(torch.tensor(2.))))
    def test_total_and_original(self):
        results={}
        for kind in ("original","total","wasserstein","penalizacion"):
            G,D,og,od=setup();e.seed_all(7)
            results[kind]=d.probe(G,D,og,od,batch(),{"lambda_gp":10},kind,torch.device("cpu"))
        self.assertTrue(d.difference(results["original"][0],results["total"][0])["exact"])
        summed={k:results["wasserstein"][0][k]+results["penalizacion"][0][k] for k in results["total"][0]}
        self.assertLess(d.difference(results["total"][0],summed)["max_abs"],1e-12)
        self.assertIn("b",results["penalizacion"][1]["unused_parameters"])
    def test_no_step(self):
        G,D,og,od=setup();before=copy.deepcopy(pack(G,D,og,od,torch.device("cpu")))
        _,r=d.probe(G,D,og,od,batch(),{"lambda_gp":10},"total",torch.device("cpu"))
        self.assertTrue(r["models_optimizers_unchanged"])
        self.assertEqual(og.state_dict(),before["opt_g"]);self.assertEqual(od.state_dict(),before["opt_d"])
    def test_original_without_observers(self):
        G,D,og,od=setup();e.seed_all(7)
        actual,_=d.probe(G,D,og,od,batch(),{"lambda_gp":10},"original",torch.device("cpu"))
        G,D,og,od=setup();e.seed_all(7);x,y,_,_=batch()
        with torch.no_grad():fake=G(x)
        loss,_=e.critic_loss(D,x,y,fake,10);loss.backward()
        self.assertTrue(d.difference(actual,d.vectors(D)[0])["exact"])
    def test_nonfinite(self):
        with self.assertRaises(ValueError):d.difference({"a":torch.tensor(float("nan"))},{"a":torch.tensor(0.)})
    def test_shape(self):
        with self.assertRaises(ValueError):d.difference({"a":torch.ones(2)},{"a":torch.ones(3)})

if __name__=="__main__":unittest.main()

"""CG-04c: equivalencia matemática y protección del paso separado."""
import copy, unittest
import torch
import ejecutar_ajuste_cgan as e
from gradientes_critico import critic_components,separated_critic_step
from losses import critic_loss

class LinearCritic(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.w=torch.nn.Parameter(torch.tensor(.7,dtype=torch.float64))
        self.b=torch.nn.Parameter(torch.tensor(.2,dtype=torch.float64))
    def forward(self,x,y):return self.w*y+self.b

class Tests(unittest.TestCase):
    def setUp(self):
        e.configure();e.seed_all(17)
        self.x=torch.arange(8,dtype=torch.float64).reshape(2,1,2,2)/10
        self.y=self.x+.3;self.fake=self.x*.4
    def test_analytic_and_unused_gp_bias(self):
        d=LinearCritic();o=torch.optim.SGD(d.parameters(),lr=.01)
        w,p,_=critic_components(d,self.x,self.y,self.fake,10)
        expected=(self.fake-self.y).mean()+10*(d.w.detach()/2-1)
        norm=separated_critic_step(w,p,d,o)
        torch.testing.assert_close(d.w.grad,expected,rtol=0,atol=1e-12)
        self.assertEqual(float(d.b.grad),0.)
        self.assertAlmostEqual(norm,abs(float(expected)),places=12)
        self.assertAlmostEqual(float(d.w.detach()),.7-.01*float(expected),places=12)
    def test_original_math_rng_and_gradients(self):
        old=LinearCritic();new=copy.deepcopy(old)
        e.seed_all(17);loss,parts=critic_loss(old,self.x,self.y,self.fake,10)
        loss.backward();rng=torch.get_rng_state().clone()
        e.seed_all(17);w,p,got=critic_components(new,self.x,self.y,self.fake,10)
        self.assertTrue(torch.equal(loss,w+p));self.assertEqual(parts,got)
        self.assertTrue(torch.equal(rng,torch.get_rng_state()))
        separated_critic_step(w,p,new,torch.optim.SGD(new.parameters(),lr=0.))
        for a,b in zip(old.parameters(),new.parameters()):
            torch.testing.assert_close(a.grad,b.grad,rtol=0,atol=1e-12)
    def test_stale_gradients_replaced_single_adam_step(self):
        d=LinearCritic();o=torch.optim.Adam(d.parameters(),lr=1e-5,foreach=False)
        for param in d.parameters():param.grad=torch.full_like(param,999.)
        w,p,_=critic_components(d,self.x,self.y,self.fake,10)
        separated_critic_step(w,p,d,o)
        self.assertEqual({float(s['step']) for s in o.state.values()},{1.})
        self.assertLess(abs(float(d.w.grad)),10.);self.assertEqual(float(d.b.grad),0.)
    def test_nonfinite_loss_no_step(self):
        d=LinearCritic();o=torch.optim.Adam(d.parameters())
        with self.assertRaisesRegex(ValueError,'Pérdida'):
            separated_critic_step(d.w*float('inf'),d.w.square(),d,o)
        self.assertFalse(o.state);self.assertEqual(float(d.w.detach()),.7)
    def test_nonfinite_gradient_no_step(self):
        d=LinearCritic();o=torch.optim.Adam(d.parameters())
        # Pérdida finita y derivada singular en cero.
        w=(d.w-.7).sqrt()+d.b*0
        with self.assertRaisesRegex(ValueError,'Gradiente'):
            separated_critic_step(w,d.w.square(),d,o)
        self.assertFalse(o.state);self.assertEqual(float(d.w.detach()),.7)
    def test_missing_wasserstein_parameter_rejected(self):
        d=LinearCritic();o=torch.optim.Adam(d.parameters())
        with self.assertRaises(RuntimeError):separated_critic_step(d.w.square(),d.w.square(),d,o)
        self.assertFalse(o.state)
    def test_old_gradient_policy_rejected(self):
        import revisar_ajuste_cgan as r
        c={'identity':{'arm':'C0','stage':'tecnica','seed':2026100303}}
        with self.assertRaisesRegex(ValueError,'Política'):r.validate_state(c)

if __name__=='__main__':unittest.main()

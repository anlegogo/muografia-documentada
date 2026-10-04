"""Pruebas analíticas E1; no entrenan ni abren conjuntos de datos."""
import json,unittest
import torch
from perdida_espacial_borde_experimental import spatial_edge_count_loss as loss
S=8.239329427901795
def norm(c):return torch.log1p(c)/(S+torch.log1p(c))
class Checks(unittest.TestCase):
 def setUp(self):
  self.ref=torch.tensor([1.]*10+[9.]*10,dtype=torch.float64).reshape(1,1,4,5)
  self.mask=torch.ones_like(self.ref,dtype=torch.bool)
 def test_exact(self):self.assertLess(float(loss(norm(self.ref),self.ref,self.mask,S)),1e-14)
 def test_permutation(self):
  self.assertAlmostEqual(float(loss(norm(torch.flip(self.ref,[2,3])),self.ref,self.mask,S)),1.6,places=12)
 def test_known_bias(self):self.assertAlmostEqual(float(loss(norm(self.ref*1.2),self.ref,self.mask,S)),.2,places=12)
 def test_sample_weighting(self):
  ref=torch.cat([self.ref,self.ref*100]);pred=torch.cat([self.ref*1.2,self.ref*100*1.4])
  self.assertAlmostEqual(float(loss(norm(pred),ref,self.mask.repeat(2,1,1,1),S)),.3,places=12)
 def test_gradient_finite_difference(self):
  z=norm(self.ref*1.2).requires_grad_();v=loss(z,self.ref,self.mask,S);grad=torch.autograd.grad(v,z)[0]
  self.assertTrue(torch.isfinite(grad).all())
  delta=torch.zeros_like(z);delta[0,0,0,0]=1e-7
  fd=(loss(z.detach()+delta,self.ref,self.mask,S)-loss(z.detach()-delta,self.ref,self.mask,S))/(2e-7)
  self.assertAlmostEqual(float(grad[0,0,0,0]),float(fd),places=6)
 def test_outside_mask(self):
  ref=torch.cat([self.ref,self.ref],3);mask=torch.cat([self.mask,torch.zeros_like(self.mask)],3)
  pred=torch.cat([self.ref,self.ref*100],3)
  self.assertLess(float(loss(norm(pred),ref,mask,S)),1e-14)
 def test_reject_empty_support(self):
  with self.assertRaises(ValueError):loss(norm(self.ref),self.ref,torch.zeros_like(self.mask),S)
 def test_reject_zero_reference(self):
  with self.assertRaises(ValueError):loss(norm(self.ref),torch.zeros_like(self.ref),self.mask,S)
 def test_reject_invalid_range_and_overflow(self):
  for value in [-.1,1.,float('nan'),.99999]:
   with self.assertRaises(ValueError):loss(torch.full_like(self.ref,value),self.ref,self.mask,S)
if __name__=='__main__':unittest.main()


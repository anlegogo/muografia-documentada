"""Verifica especificaciones y la pérdida; no entrena ni autoriza GPU."""
import argparse,hashlib,json,sys,unittest
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--especificaciones',type=Path,required=True)
p.add_argument('--salida',type=Path,required=True)
p.add_argument('--torch-dir',type=Path)
a=p.parse_args()
if a.torch_dir:sys.path.insert(0,str(a.torch_dir))
import torch
from perdida_cuentas_regionales import regional_log_count_loss,combined_loss
torch.set_num_threads(2)
S=8.239329427901795
def T(c):
    t=torch.log1p(c);return t/(S+t)

class LossTests(unittest.TestCase):
    def test_exact_counts_zero_loss(self):
        c=torch.full((2,1,8,8),3.,dtype=torch.double);m=torch.ones((2,1,8,8),dtype=torch.bool)
        v,_=regional_log_count_loss(T(c),c,m,[0],S)
        self.assertLess(abs(v.item()),1e-12)
    def test_known_bias(self):
        c=torch.full((1,1,8,8),2.,dtype=torch.double);m=torch.ones((1,1,8,8),dtype=torch.bool)
        v,_=regional_log_count_loss(T(c*2),c,m,[1],S)
        self.assertAlmostEqual(v.item(),float(torch.log(torch.tensor(5./3,dtype=torch.double))),12)
    def test_zero_reference_finite(self):
        c=torch.zeros((1,1,8,8),dtype=torch.double);m=torch.ones((1,1,8,8),dtype=torch.bool)
        z=T(c+1).requires_grad_();v,_=regional_log_count_loss(z,c,m,[1],S);v.backward()
        self.assertTrue(torch.isfinite(z.grad).all());self.assertTrue(torch.all(z.grad>0))
    def test_zero_control_weight_equivalent(self):
        c=torch.ones((1,1,8,8),dtype=torch.double);m=torch.ones((1,1,8,8),dtype=torch.bool)
        z=T(c*2).requires_grad_();v,_=combined_loss(z,T(c),c,m,[1],S,weight=0)
        old=100*torch.nn.functional.l1_loss(z,T(c))
        self.assertEqual(v.item(),old.item())
        torch.testing.assert_close(torch.autograd.grad(v,z,retain_graph=True)[0],torch.autograd.grad(old,z)[0],rtol=0,atol=0)
    def test_finite_difference_gradient(self):
        z=torch.full((1,1,5,5),.2,dtype=torch.double,requires_grad=True);c=torch.ones_like(z);m=torch.ones((1,1,5,5),dtype=torch.bool)
        regional_log_count_loss(z,c,m,[1],S)[0].backward()
        expected=[]
        for i in range(z.numel()):
            plus=z.detach().clone();minus=z.detach().clone();plus.flatten()[i]+=1e-6;minus.flatten()[i]-=1e-6
            expected.append((regional_log_count_loss(plus,c,m,[1],S)[0]-regional_log_count_loss(minus,c,m,[1],S)[0])/(2e-6))
        torch.testing.assert_close(z.grad.flatten(),torch.stack(expected),atol=1e-5,rtol=1e-5)
    def test_equal_family_weight(self):
        c=torch.ones((1,1,8,8),dtype=torch.double);pred=c*2;pred[:,:,4:]=4;z=T(pred)
        m=torch.zeros((1,4,8,8),dtype=torch.bool);m[:,0,:4]=True;m[:,1:,4:]=True
        many,_=regional_log_count_loss(z,c,m,[0,3,3,3],S)
        expected=(torch.log(torch.tensor(3./2,dtype=torch.double))+torch.log(torch.tensor(5./2,dtype=torch.double)))/2
        self.assertAlmostEqual(many.item(),expected.item(),12)
    def test_small_region_ignored_and_all_empty_rejected(self):
        c=torch.ones((1,1,8,8),dtype=torch.double);z=T(c);m=torch.zeros((1,2,8,8),dtype=torch.bool);m[:,0]=True;m[:,1,0,0]=True
        v,support=regional_log_count_loss(z,c,m,[0,3],S)
        self.assertEqual(support[0]['valid_regions'],[0])
        with self.assertRaises(ValueError):regional_log_count_loss(z,c,m[:,1:], [3],S)
    def test_invalid_prediction_rejected(self):
        c=torch.ones((1,1,8,8),dtype=torch.double);m=torch.ones((1,1,8,8),dtype=torch.bool)
        for value in (1.,-0.1,float('nan')):
            with self.assertRaises(ValueError):regional_log_count_loss(c*value,c,m,[0],S)
    def test_near_one_no_exp_overflow(self):
        c=torch.ones((1,1,8,8),dtype=torch.double);m=torch.ones((1,1,8,8),dtype=torch.bool)
        z=torch.full_like(c,.999).requires_grad_();v,_=regional_log_count_loss(z,c,m,[0],S);v.backward()
        self.assertTrue(torch.isfinite(v));self.assertTrue(torch.isfinite(z.grad).all())

def validate_specs(root):
    specs=[json.loads((root/n).read_text(encoding='utf-8')) for n in ('ajuste-control.spec.json','ajuste-regional.spec.json')]
    left,right=specs
    changed={k for k in left if left[k]!=right[k]}
    assert changed=={'arm','run_id','lambda_regional'}
    assert [x['lambda_regional'] for x in specs]==[0,1]
    for x in specs:
        assert x['status']=='design_and_loss_verified_not_gpu_ready'
        assert x['initial_checkpoint_sha256']=='734bc5dc1aa4cdc16a3fa0b6de2d58da7575c5bd0b1fe342bc266283f0e8e57a'
        assert x['reserved_splits_allowed'] is False and x['train_split']=='train' and x['selection_split']=='val'
        assert x['epochs']==x['selected_epoch']==5 and x['early_stopping'] is False
        assert x['train_pairs']==1440 and x['val_pairs']==360 and x['batch']==4
        assert x['reset_optimizer'] and x['reset_rng'] and x['seed']==2026100302
        assert x['lambda_l1']==100 and x['normalization_scale']==S and x['region_min_pixels']==20
        assert not x['mass_campaign_authorized']
    return {'identical_except':sorted(changed),'pilot_updates_per_arm':1800,'pilot_total_updates':3600,'gpu_training_ready':False}

if __name__=='__main__':
    config=validate_specs(a.especificaciones)
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(LossTests))
    if not result.wasSuccessful():raise SystemExit(1)
    evidence={'schema':'oe2-adjustment-design-check-v1','torch':torch.__version__,'device':'cpu','tests':result.testsRun,'passed':True,'specification_checks':config,'source_sha256':{n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in ('perdida_cuentas_regionales.py','verificar_diseno_ajuste.py')},'spec_sha256':{n:hashlib.sha256((a.especificaciones/n).read_bytes()).hexdigest() for n in ('ajuste-control.spec.json','ajuste-regional.spec.json')},'scope':'mathematics and specifications only; no trainer integration or CUDA test'}
    a.salida.write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(evidence,indent=2))

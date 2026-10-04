import unittest
import numpy as np
from metricas_locales_oe3 import local_metrics,repeated_contrast_signal,assessed_fraction

class LocalMetricsTests(unittest.TestCase):
    def setUp(self):
        self.t=np.arange(20);self.d=np.tile(np.arange(20,25),(20,1))
        self.c=np.r_[np.linspace(10,20,20),np.arange(2,7)]
    def test_hand_values_and_unique_background(self):
        r=local_metrics(self.c,self.t,self.d)
        self.assertAlmostEqual(r['mean_control_matched'],4.)
        self.assertAlmostEqual(r['contrast_counts'],15/4-1)
        self.assertAlmostEqual(r['sigma_background_unique'],np.sqrt(2.5))
        self.assertAlmostEqual(r['cnr_local_signed'],11/np.sqrt(2.5))
        self.assertEqual(r['unique_background_pixels'],5)
    def test_scale_invariance(self):
        a=local_metrics(self.c,self.t,self.d);b=local_metrics(self.c*20,self.t,self.d)
        for k in ['snr_local_intensity','cnr_local_signed','contrast_counts']:self.assertAlmostEqual(a[k],b[k])
    def test_flat_zero_and_negative(self):
        r=local_metrics(np.zeros(25),self.t,self.d)
        for k in ['snr_local_intensity','cnr_local_signed','contrast_counts']:self.assertIsNone(r[k])
        with self.assertRaises(ValueError):local_metrics(-self.c,self.t,self.d)
        with self.assertRaises(ValueError):local_metrics(self.c*np.nan,self.t,self.d)
    def test_signed_contrast(self):
        r=local_metrics(np.r_[np.linspace(0,1,20),np.arange(2,7)],self.t,self.d)
        self.assertLess(r['cnr_local_signed'],0)
    def test_repeated_not_standard_error(self):
        rows=[{'status':'ok','mean_anomaly':x,'mean_control_matched':1} for x in [2,3,4]]
        self.assertAlmostEqual(repeated_contrast_signal(rows)['snr_contrast_repeated_signed'],2.)
        self.assertIsNone(repeated_contrast_signal([rows[0],rows[0]])['snr_contrast_repeated_signed'])
    def test_incomplete_and_indices(self):
        self.assertEqual(local_metrics(self.c,self.t[:10],self.d[:10])['status'],'insufficient_support')
        with self.assertRaises(ValueError):local_metrics(self.c,self.t,self.d[:10])
        with self.assertRaises(ValueError):local_metrics(self.c,self.t,self.d+100)
    def test_grid_minimum_without_monotonic_assumption(self):
        thresholds={'g':{str(v):{'ssim':.9,'psnr':30} for v in range(6)}}
        rows=[{'model':'m','fraction':f,'geometry':'g','view':v,'ssim':ss,'psnr':31} for f,ss in [(.01,.8),(.05,.95),(.1,.8),(.5,.95)] for v in range(6) for k in range(20)]
        r=assessed_fraction(rows,thresholds,[.01,.05,.1,.5],['m'],['g'])['m']
        self.assertEqual(r['minimum_sampled_fraction'],.05);self.assertEqual(r['nominal_ratio_reference_fraction_to_input'],10)
        self.assertFalse(r['physical_equivalence'])
        with self.assertRaises(ValueError):assessed_fraction(rows[:-1],thresholds,[.01,.05,.1,.5],['m'],['g'])
    def test_no_pass_and_psnr_joint(self):
        thresholds={'g':{str(v):{'ssim':.9,'psnr':30} for v in range(6)}}
        rows=[{'model':'m','fraction':.05,'geometry':'g','view':v,'ssim':.99,'psnr':29} for v in range(6) for k in range(20)]
        self.assertIsNone(assessed_fraction(rows,thresholds,[.05],['m'],['g'])['m']['minimum_sampled_fraction'])
if __name__=='__main__':unittest.main()

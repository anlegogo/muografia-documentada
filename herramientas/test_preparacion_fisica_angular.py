import json
import math
from pathlib import Path
import tempfile
import unittest
import numpy as np
from scipy.stats import binom, binomtest
from referencia_cielo_angular import reference
from estadistica_control_angular import binomial_interval, evaluate_c3, plan_equal_counts
from evaluar_bordes_angular import evaluate


class StatisticalTests(unittest.TestCase):
    def test_intervals_against_independent_scipy_inversion(self):
        for k,n in [(0,20),(20,20),(3,20),(1600,1000000)]:
            got=binomial_interval(k,n,.05)
            expected=binomtest(k,n).proportion_ci(confidence_level=.95,method='exact')
            np.testing.assert_allclose(got,[expected.low,expected.high],atol=1e-11)

    def test_exact_coverage_small_n(self):
        for p in [.01,.2,.5,.9]:
            coverage=sum(binom.pmf(k,25,p) for k in range(26) if binomial_interval(k,25,.05)[0]<=p<=binomial_interval(k,25,.05)[1])
            self.assertGreaterEqual(coverage,.95-1e-12)

    def data(self,c,d):
        return {'one_record_per_primary':True,'fixed_n_before_run':True,
                'bands':[dict(name=str(i),C=c,D=d,N_P=100000000,N_G=10000000000,panel_over_source_area=.01) for i in range(4)]}

    def test_1600_inconclusive_and_large_equal_equivalent(self):
        self.assertFalse(evaluate_c3(self.data(1600,1600))['all_equivalent'])
        self.assertTrue(evaluate_c3(self.data(50000,50000))['all_equivalent'])

    def test_difference_and_zero_not_pass(self):
        self.assertTrue(all(x['decision']=='outside_tolerance' for x in evaluate_c3(self.data(50000,60000))['bands']))
        self.assertFalse(evaluate_c3(self.data(0,0))['all_equivalent'])

    def test_design_grows_with_precision_and_shift(self):
        n=plan_equal_counts()['expected_counts_each_arm_each_band']
        self.assertGreater(n,1600)
        self.assertGreater(plan_equal_counts(tolerance=.025)['expected_counts_each_arm_each_band'],n)
        self.assertGreater(plan_equal_counts(true_ratio=1.02)['expected_counts_each_arm_each_band'],n)

    def test_optional_stopping_rejected(self):
        d=self.data(1000,1000);d['fixed_n_before_run']=False
        with self.assertRaises(ValueError):evaluate_c3(d)


class SkyTests(unittest.TestCase):
    def test_uniform_spectrum_reference_with_and_without_margin(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);el=np.linspace(2,47,256)
            np.savetxt(p/'row_weights_30d.txt',np.c_[el,np.ones(256)],fmt='%.9f')
            (p/'meta.json').write_text('{}')
            (p/'p_cdf.txt').write_text('# band_edges_deg: 2 47\n0 10\n')
            for margin in [0,5]:
                r=reference(p,margin,3)
                q=1-math.sqrt(3*(3+2*.1056583745))/10
                np.testing.assert_allclose(r['ideal_selected_given_nominal_by_row'],q,atol=1e-12)
                self.assertLessEqual(r['nominal_window_probability'],1+1e-10)
            self.assertAlmostEqual(reference(p,0)['nominal_window_probability'],1,places=7)


class BorderTests(unittest.TestCase):
    def inputs(self):
        sky=np.ones((256,256),bool);p=1/65536
        r={'nominal_probability_per_pixel_by_row':[p]*256,'ideal_selected_probability_per_pixel_by_row':[.5*p]*256}
        return np.full((256,256),50000,dtype=np.int64),6553600000,sky,r

    def test_uniform_large_sample_and_edge_deficit(self):
        counts,n,sky,r=self.inputs()
        self.assertTrue(evaluate(counts,n,sky,r)['all_equivalent'])
        counts[:,0]//=2
        result=evaluate(counts,n,sky,r)
        self.assertEqual(result['regions'][0]['decision'],'outside_tolerance')

    def test_sparse_is_inconclusive_and_unphysical_counts_rejected(self):
        counts,n,sky,r=self.inputs();counts[:]=0
        self.assertFalse(evaluate(counts,1,sky,r)['all_equivalent'])
        counts[0,0]=2
        with self.assertRaises(ValueError):evaluate(counts,1,sky,r)

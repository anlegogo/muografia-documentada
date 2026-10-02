import unittest
import numpy as np
from auditar_fuente_angular import extended_rows,above_quantile


class SourceTests(unittest.TestCase):
    def test_zero_margin_exact(self):
        el=np.linspace(2,47,256);w=np.arange(1,257)
        e,v,k=extended_rows(el,w,0);np.testing.assert_array_equal(v,w)
        self.assertEqual(v.sum(),w.sum())

    def test_constant_extension_and_horizon(self):
        e,w,k=extended_rows(np.linspace(2,47,256),np.ones(256),5)
        np.testing.assert_array_equal(w[(k>=0)&(k<256)],np.ones(256))
        self.assertTrue(np.all(w[e<.1]==0));self.assertTrue(np.allclose(w[e>=.1],1))

    def test_quantile_known_distribution(self):
        self.assertEqual(above_quantile([0,10,20],5),.75)
        self.assertEqual(above_quantile([0,10,20],30),0)
        self.assertEqual(above_quantile([0,10,20],-1),1)
        self.assertEqual(above_quantile([0,0,10],0),.5)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):above_quantile([2,1],1)
        with self.assertRaises(ValueError):extended_rows(np.linspace(2,47,256),np.ones(256),-1)

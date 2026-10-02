import unittest
import numpy as np
from diagnosticar_observable_angular import containment,edges


class DiagnosticTests(unittest.TestCase):
    def test_nested_and_empty_bands(self):
        r=containment(np.array([2]),np.array([9]),np.array([10]),np.array([20000]))
        self.assertEqual(r[0]['panel_over_600'],.2);self.assertEqual(r[0]['plane100_over_600'],.9)
        self.assertIsNone(r[1]['panel_over_600'])

    def test_non_nested_rejected(self):
        with self.assertRaises(ValueError):containment(np.array([11]),np.array([9]),np.array([10]),np.array([20000]))

    def test_flat_field_and_known_edge(self):
        g=np.full((256,256),1000);h=np.full_like(g,500);el=np.linspace(2,47,256);sky=np.ones_like(g,dtype=bool)
        r=edges(h,g,el,sky);self.assertAlmostEqual(r['combined_max_abs_pp'],0)
        h[:,0]=400;r=edges(h,g,el,sky)
        self.assertAlmostEqual(r['column_edge_max_abs_pp'],10);self.assertIsNone(r['acceptance_decision'])

    def test_missing_support_rejected(self):
        a=np.ones((256,256));g=a.copy();g[:,0]=0
        with self.assertRaises(ValueError):edges(a,g,np.linspace(2,47,256),np.ones_like(a,dtype=bool))


if __name__=='__main__':unittest.main()

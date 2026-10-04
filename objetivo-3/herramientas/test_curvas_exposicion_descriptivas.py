import unittest
from curvas_exposicion_descriptivas import crossing

class CrossingTests(unittest.TestCase):
    def test_bracket_and_ratios(self):
        x=crossing([.01,.05,.1,.5],[.6,.7,.8,.9],.85)
        self.assertEqual((x['lower_grid_fraction'],x['upper_grid_fraction']),(.1,.5))
        self.assertEqual((x['lower_nominal_ratio_to_f05'],x['upper_nominal_ratio_to_f05']),(2,10))
    def test_no_extrapolation(self):
        self.assertEqual(crossing([.1,.5],[.8,.9],.95)['status'],'above_grid_maximum')
    def test_nonmonotonic_rejected(self):
        self.assertEqual(crossing([.01,.1,.5],[.8,.7,.9],.85)['status'],'nonmonotonic_no_bracket')
    def test_low_end_and_nan(self):
        self.assertIsNone(crossing([.01,.1],[.6,.8],.5)['lower_grid_fraction'])
        self.assertEqual(crossing([.01,.1],[.6,float('nan')],.5)['status'],'not_estimable')

if __name__=='__main__':unittest.main()

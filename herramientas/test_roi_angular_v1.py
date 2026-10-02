import unittest
import numpy as np
from preparar_roi_angular_v1 import intersection_lengths, rays


class ChordTests(unittest.TestCase):
    def setUp(self):
        self.c=dict(cx_m=0,cy_m=0,radius_m=1,z0_m=-1,z1_m=1)
        self.e=dict(cx_m=0,cy_m=0,cz_m=0,ax_m=2,ay_m=2,az_m=2)

    def length(self,o,d):return float(intersection_lengths(o,np.array(d),self.c,self.e))

    def test_diameter_cylinder_limits(self):self.assertAlmostEqual(self.length([-5,0,0],[1,0,0]),2)
    def test_vertical_caps(self):self.assertAlmostEqual(self.length([0,0,-5],[0,0,1]),2)
    def test_origin_inside(self):self.assertAlmostEqual(self.length([0,0,0],[1,0,0]),1)
    def test_away_and_outside(self):
        self.assertEqual(self.length([-5,0,0],[-1,0,0]),0)
        self.assertEqual(self.length([-5,0,3],[1,0,0]),0)
    def test_tangent(self):self.assertEqual(self.length([-5,1,0],[1,0,0]),0)
    def test_ellipsoid_limits(self):
        self.e.update(ax_m=.5,ay_m=.5,az_m=.5)
        self.assertAlmostEqual(self.length([-5,0,0],[1,0,0]),1)
    def test_nonunit_rejected(self):
        with self.assertRaises(ValueError):self.length([0,0,0],[2,0,0])
    def test_six_views_point_toward_axis_and_up(self):
        for view in range(6):
            o,d=rays(np.array([0]),np.array([10]),view)
            self.assertLess(np.dot(o[:2],d[0,0,:2]),0)
            self.assertGreater(d[0,0,2],0)
            self.assertAlmostEqual(np.linalg.norm(d[0,0]),1)


if __name__=='__main__':unittest.main()

import unittest,tempfile,json
from pathlib import Path
import numpy as np
import evaluacion_final_oe2 as e

class Checks(unittest.TestCase):
 def test_inverse_and_zero(self):
  x=np.array([0.,1.,20.,3000.]);np.testing.assert_allclose(e.invert(e.normalize(x,8.239),8.239),x,rtol=1e-12,atol=1e-12)
 def test_invalid_predictions(self):
  for z in [np.array([1.]),np.array([-1.]),np.array([np.nan]),np.array([.999999])]:
   with self.assertRaises(ValueError):e.invert(z,8.239)
 def test_model_set_and_corruption(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'data').write_bytes(b'data');(p/'weight').write_bytes(b'weight');s={'data_sha256':{'data':e.sha(p/'data')},'models':{'m':{'sha256':e.sha(p/'weight')}}}
   self.assertTrue(e.preflight(p,p,{'m':str(p/'weight')},s)['passed'])
   with self.assertRaises(ValueError):e.preflight(p,p,{},s)
   (p/'weight').write_bytes(b'corrupt')
   with self.assertRaises(ValueError):e.preflight(p,p,{'m':str(p/'weight')},s)
 def test_homogeneous_and_missing_region(self):
  images=[{'model':'m','geometry':'g','ssim':1.,'psnr':None,'perfect_match':True} for _ in range(120)]
  regions=[{'model':'m','geometry':'g','view':v,'family':f,'status':'ok','bias_mean':.1,'spatial_mae':.2} for v in range(6) for f in [0,1,2]]
  z=e.summarize(images,regions,[],['m'],['g'])['m'];self.assertIsNone(z['Q_macro']);self.assertAlmostEqual(z['by_geometry']['g']['rock_abs_bias'],.1);self.assertEqual(z['by_geometry']['g']['perfect_matches'],120);self.assertIsNone(z['psnr_macro']);self.assertEqual(z['common_contrasts'],0)
  regions[0]['status']='reference_or_geometry_insufficient';z=e.summarize(images,regions,[],['m'],['g'])['m'];self.assertIsNone(z['by_geometry']['g']['sky_mae'])
 def test_reference_geometry_zero(self):
  cfg={'detector_distance_m':1000,'detector_height_m':1.5,'cone_top_radius_m':.1,'rock_sky_margin_pixels':2,'anomaly_min_length_m':20,'core_erosion_pixels':1,'min_matched_pixels':20,'min_match_fraction':.8,'control_cone_length_relative_tolerance':.05,'control_donors_per_pixel':5}
  ref=np.zeros((256,256));low=np.zeros((20,256,256));coords={'az_centers_deg':np.linspace(-30,30,256),'el_centers_deg':np.linspace(2,47,256)};g={'edifice':{'base_radius_m':300,'height_m':250},'anomalies':[]}
  im,rr,cc=e.analyze_view(ref,low,{},g,coords,0,cfg,8.239);self.assertTrue(all(x['status']!='ok' for x in rr));self.assertEqual(cc,[]);self.assertTrue(all(x['perfect_match'] for x in im))

if __name__=='__main__':unittest.main()

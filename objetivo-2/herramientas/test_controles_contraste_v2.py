import unittest,copy
import numpy as np
from controles_contraste_v2 import stable_match,Registry

class ControlsTest(unittest.TestCase):
    def fixture(self):
        mask=np.zeros((1,9),bool);mask[0,8]=True
        control=~mask
        lengths=np.full((1,9),100.)
        return mask,control,lengths,{'control_cone_length_relative_tolerance':.05,'control_donors_per_pixel':5}
    def test_near_tie_is_ordered_by_column(self):
        m,c,L,cfg=self.fixture();L[0,:8]+=[4e-11,-3e-11,0,2e-11,-1e-11,0,0,0]
        t,d=stable_match(m,c,L,cfg)
        np.testing.assert_array_equal(t,[8]);np.testing.assert_array_equal(d,[[0,1,2,3,4]])
    def test_separated_distances_and_exclusion(self):
        m,c,L,cfg=self.fixture();L[0,:8]=[107,104,103,102,101,100,106,106]
        _,d=stable_match(m,c,L,cfg);np.testing.assert_array_equal(d,[[5,4,3,2,1]])
        cfg['control_donors_per_pixel']=6;t,d=stable_match(m,c,L,cfg);self.assertEqual(len(t),0)
    def test_replay_and_corruption(self):
        import hashlib
        from pathlib import Path
        import controles_contraste_v2 as module
        m,c,L,cfg=self.fixture();r=Registry('test');t,d=r(m,c,L,cfg)
        record={'protocol_sha256':'test','correction_sha256':hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),'entries':r.entries}
        replay=Registry('test',record);tt,dd=replay(m,c,L+1e-12,cfg)
        np.testing.assert_array_equal(t,tt);np.testing.assert_array_equal(d,dd)
        bad=copy.deepcopy(record);bad['entries'][0]['donors'][0][0]=7
        with self.assertRaisesRegex(ValueError,'alterados'):Registry('test',bad)(m,c,L,cfg)
    def test_changed_support_rejected(self):
        import hashlib
        from pathlib import Path
        import controles_contraste_v2 as module
        m,c,L,cfg=self.fixture();r=Registry('test');r(m,c,L,cfg)
        record={'protocol_sha256':'test','correction_sha256':hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),'entries':r.entries}
        c[0,0]=False
        with self.assertRaisesRegex(ValueError,'distintas'):Registry('test',record)(m,c,L,cfg)

if __name__=='__main__':unittest.main()

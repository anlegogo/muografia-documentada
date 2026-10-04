import json, unittest
from pathlib import Path
import numpy as np
from evaluar_regiones_geometricas import cone_interval,anomaly_interval,length,clipped_length,morphology,rays,masks,match_controls

class GeometryTests(unittest.TestCase):
    def test_horizontal_cone(self):
        o=np.array([-20.,0,5]);d=np.array([[1.,0,0],[0,1.,0],[-1.,0,0]])
        np.testing.assert_allclose(length(cone_interval(o,d,10,10,0)),[10,0,0],atol=1e-12)
    def test_axis_cone(self):
        for o,d in [(np.array([0.,0,20]),np.array([[0.,0,-1]])),(np.array([0.,0,-10]),np.array([[0.,0,1]]))]:
            np.testing.assert_allclose(length(cone_interval(o,d,10,10,0)),[10],atol=1e-12)
    def test_sphere_cylinder_and_clip(self):
        o=np.array([-5.,0,1]);d=np.array([[1.,0,0]])
        sphere={'kind':'cavity','params':{'cx_m':0,'cy_m':0,'cz_m':1,'radius_m':2}}
        cyl={'kind':'conduit','params':{'cx_m':0,'cy_m':0,'z0_m':0,'z1_m':2,'radius_m':1}}
        np.testing.assert_allclose(length(anomaly_interval(o,d,sphere)),[4])
        np.testing.assert_allclose(length(anomaly_interval(o,d,cyl)),[2])
        np.testing.assert_allclose(clipped_length(anomaly_interval(o,d,sphere),(np.array([5.]),np.array([6.]))),[1])
    def test_empty_tangent_and_inside(self):
        sphere={'kind':'cavity','params':{'cx_m':0,'cy_m':0,'cz_m':0,'radius_m':2}}
        d=np.array([[1.,0,0]])
        for o,want in [(np.array([-5.,2,0]),0),(np.array([-5.,3,0]),0),(np.zeros(3),2)]:
            np.testing.assert_allclose(length(anomaly_interval(o,d,sphere)),[want],atol=1e-12)
    def test_ellipsoid_diameter_and_cylinder_caps(self):
        ell={'kind':'dense_body','params':{'cx_m':0,'cy_m':0,'cz_m':0,'ax_m':3,'ay_m':4,'az_m':5}}
        np.testing.assert_allclose(length(anomaly_interval(np.array([-10.,0,0]),np.array([[1.,0,0]]),ell)),[6])
        cyl={'kind':'conduit','params':{'cx_m':0,'cy_m':0,'z0_m':0,'z1_m':2,'radius_m':1}}
        np.testing.assert_allclose(length(anomaly_interval(np.array([0.,0,-5]),np.array([[0.,0,1]]),cyl)),[2])
    def test_morphology(self):
        x=np.zeros((9,9),bool);x[3:6,3:6]=True
        self.assertEqual(int(morphology(x,1,True).sum()),1)
        self.assertEqual(int(morphology(x,1,False).sum()),25)
    def test_views(self):
        cfg={'detector_distance_m':1000,'detector_height_m':1.5}
        for v in range(6):
            o,d=rays(np.array([0.]),np.array([0.]),v,cfg)
            np.testing.assert_allclose(o[:2]+1000*d[0,0,:2],[0,0],atol=1e-10)
    def test_matching_no_donors(self):
        x=np.zeros((256,256),bool);x[3,4]=True
        t,d=match_controls(x,np.zeros_like(x),np.ones_like(x,float),{'control_cone_length_relative_tolerance':.05,'control_donors_per_pixel':5})
        self.assertEqual(len(t),0)

def numerical_check(root,protocol):
    cfg=json.loads(protocol.read_text())
    rng=np.random.default_rng(2026100302);results=[]
    az=(np.linspace(-30,30,257)[:-1]+np.linspace(-30,30,257)[1:])/2;el=np.linspace(2,47,256)
    step=.25;ts=(np.arange(12000)+.5)*step
    for gi in range(1,4):
        g=json.loads((root/f'geo-val-{gi:02d}.json').read_text(encoding='utf-8'))
        for vi in range(6):
            o,d=rays(az,el,vi,cfg);L,aa,_=masks(g,o,d,cfg)
            ix=rng.choice(65536,128,replace=False);dr=d.reshape(-1,3)[ix]
            pts=o+ts[None,:,None]*dr[:,None,:]
            H=g['edifice']['height_m'];R=g['edifice']['base_radius_m'];rad=R-(R-.1)*pts[...,2]/H
            con=(pts[...,2]>=0)&(pts[...,2]<=H)&(np.sum(pts[...,:2]**2,axis=-1)<=rad**2)
            errors=[float(np.max(np.abs(con.sum(1)*step-L.ravel()[ix])))]
            for j,an in enumerate(g['anomalies']):
                p=an['params'];q=pts-np.array([p['cx_m'],p['cy_m'],p.get('cz_m',0)])
                if an['kind']=='conduit':
                    inside=(np.sum(q[...,:2]**2,axis=-1)<=p['radius_m']**2)&(pts[...,2]>=p['z0_m'])&(pts[...,2]<=p['z1_m'])
                else:
                    axes=np.repeat(p['radius_m'],3) if an['kind']=='cavity' else np.array([p[k] for k in ('ax_m','ay_m','az_m')])
                    inside=np.sum((q/axes)**2,axis=-1)<=1
                errors.append(float(np.max(np.abs((inside&con).sum(1)*step-aa[j].ravel()[ix]))))
            assert max(errors)<=.5
            results.append({'geometry':g['geometry_id'],'view':vi,'sampled_rays':128,'max_length_error_m':max(errors)})
    return results

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--geometrias',type=Path,required=True)
    p.add_argument('--protocolo',type=Path,required=True)
    p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(GeometryTests)
    r=unittest.TextTestRunner(verbosity=2).run(suite)
    assert r.wasSuccessful()
    check=numerical_check(a.geometrias,a.protocolo)
    result={'analytic_tests':r.testsRun,'success':True,'numerical_step_m':.25,'numerical_comparisons':check,'max_error_m':max(x['max_length_error_m'] for x in check)}
    a.salida.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

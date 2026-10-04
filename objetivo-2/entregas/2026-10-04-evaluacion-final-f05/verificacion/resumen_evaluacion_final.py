import json,sys
d=json.load(open(sys.argv[1]))
def f(v,k=1,n=4): return None if v is None else round(v*k,n)
for split,sm in d['summary'].items():
    print('=====',split)
    for m,x in sm.items():
        print(f"{m:14s} SSIM={f(x['ssim_macro'])} PSNR={f(x['psnr_macro'],1,3)} Q={f(x['Q_macro'],100,3)} contraste={f(x['contrast_absolute_error'])} comunes={x['common_contrasts']}")
        for g,y in x['by_geometry'].items():
            print(f"    {g} ssim={f(y['ssim'])} psnr={f(y['psnr'],1,3)} Q={f(y['Q'],100,3)} {y['Q_status']} cielo={f(y['sky_mae'],100,3)} borde={f(y['edge_mae'],100,3)} roca={f(y['rock_abs_bias'],100,3)} inval={y['invalid_regions']} contr={f(y['contrast_absolute_error'])}")
for split,c in d['predeclared_comparisons'].items():
    for k,v in c.items():
        print(split,k,v['classification'],json.dumps({g:{m:(None if x is None else round(x,4)) for m,x in dd.items()} for g,dd in v['deltas_candidate_minus_baseline'].items()}))

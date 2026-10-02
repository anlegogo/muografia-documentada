"""Contraejemplo matemático 1D; NO es una simulación del volcán ni de Geant4.

Panel de ancho 1.2, desplazamiento lateral +/-10 equiprobable, supervivencia
constante por tramos. Compara inyección sobre panel + scorer grande con
inyección espacial extendida + detección en panel. Unidades arbitrarias.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path

HALF=F(3,5)
SHIFTS=[-F(10),F(10)]


def width(a,b,c,d):return max(F(0),min(b,d)-max(a,c))


def integrated_survival(lo,hi,inside,outside):
    intersection=width(lo,hi,-HALF,HALF)
    return intersection*inside+(hi-lo-intersection)*outside


def exact(inside,outside,scoring_half):
    # All source points used by the large scorer are nominally in the panel.
    large=sum(inside*width(-HALF,HALF,-scoring_half-s,scoring_half-s)/2 for s in SHIFTS)
    # Physical arrivals include source points outside the nominal panel.
    physical=sum(integrated_survival(-HALF-s,HALF-s,inside,outside)/2 for s in SHIFTS)
    return large,physical


def quadrature(inside,outside,scoring_half,n=12000):
    def survival(x):return float(inside if -float(HALF)<=x<=float(HALF) else outside)
    big=small=0.
    step=2*float(HALF)/n
    for i in range(n):
        x=-float(HALF)+(i+.5)*step
        for shift in SHIFTS:
            s=float(shift)
            big+=survival(x)*(abs(x+s)<=float(scoring_half))*.5*step
            small+=survival(x-s)*.5*step
    return big,small


def run():
    cases=[('homogeneo',F(7,10),F(7,10)),('centro_mas_transparente',F(1),F(1,2)),
           ('centro_menos_transparente',F(1,2),F(1))]
    results=[]
    for name,inside,outside in cases:
        records=[]
        for half in [50,150,300]:
            large,physical=exact(inside,outside,F(half))
            qlarge,qphysical=quadrature(inside,outside,F(half))
            error=max(abs(float(large)-qlarge),abs(float(physical)-qphysical))
            if error>1e-9:raise AssertionError('quadrature does not reproduce exact result')
            records.append(dict(scoring_width=2*half,large_scorer=float(large),
                                physical_panel=float(physical),ratio=float(large/physical),
                                quadrature_max_error=error))
        if len({r['large_scorer'] for r in records})!=1:raise AssertionError('not converged')
        if name=='homogeneo' and large!=physical:raise AssertionError('homogeneous mismatch')
        if name!='homogeneo' and large==physical:raise AssertionError('counterexample failed')
        results.append(dict(case=name,survival_inside=float(inside),survival_outside=float(outside),
                            records=records))
    return {'tipo':'ejemplo_matematico_1D_NO_GEANT4_NO_VOLCAN',
            'panel_width':float(2*HALF),'displacement':[-10,10],'units':'arbitrarias',
            'conclusion':'estabilizar conteos con el tamano del scorer no demuestra equivalencia con un panel fisico',
            'limit':'no estima el sesgo del repositorio ni define un factor corrector',
            'cases':results}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args();result=run()
    with a.salida.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

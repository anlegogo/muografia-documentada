"""Intervalos binomiales simultáneos para N fijo y un registro máximo por primario.

Clopper-Pearson y unión de Bonferroni; no supone independencia entre regiones.
Independencia de historias, selección y presupuesto fijados antes de correr.
"""
import argparse
import json
import math
from pathlib import Path
from statistics import NormalDist
from scipy.stats import beta


def binomial_interval(k, n, alpha):
    if type(k) is not int or type(n) is not int or not 0 <= k <= n or n <= 0 or not 0 < alpha < 1:
        raise ValueError('conteos o nivel inválidos')
    return (float(beta.ppf(alpha/2,k,n-k+1)) if k else 0.,
            float(beta.isf(alpha/2,k+1,n-k)) if k<n else 1.)


def classify(lo, hi, target_lo, target_hi):
    if lo >= target_lo and hi <= target_hi: return 'equivalent'
    if hi < target_lo or lo > target_hi: return 'outside_tolerance'
    return 'inconclusive'


def evaluate_c3(data):
    if data.get('one_record_per_primary') is not True or data.get('fixed_n_before_run') is not True:
        raise ValueError('se requieren N fijo e indicador por primario')
    bands=data['bands'];alpha=data.get('alpha',.05);tol=data.get('tolerance',.05)
    if not bands or len({b['name'] for b in bands})!=len(bands) or not 0<tol<1 or not 0<alpha<1:
        raise ValueError('bandas o criterio inválidos')
    result=[]
    for b in bands:
        f=b['panel_over_source_area']
        if not 0 < f <= 1: raise ValueError('fracción de área inválida')
        ci=binomial_interval(b['C'],b['N_P'],alpha/(2*len(bands)))
        di=binomial_interval(b['D'],b['N_G'],alpha/(2*len(bands)))
        lo=di[0]/ci[1]/f
        hi=di[1]/ci[0]/f if ci[0] else None
        ratio=(b['D']/b['N_G'])/(b['C']/b['N_P'])/f if b['C'] else None
        result.append({'name':b['name'],'ratio':ratio,'interval':[lo,hi],
                       'decision':classify(lo,hi,1-tol,1+tol) if hi is not None else 'inconclusive'})
    return {'schema':'oe1-c3-binomial-v1','physical_validation':False,'alpha_family':alpha,
            'method':'Clopper-Pearson on both probabilities, Bonferroni over 2*m probabilities; ratio bounds',
            'bands':result,'all_equivalent':all(r['decision']=='equivalent' for r in result)}


def plan_equal_counts(bands=4,alpha=.05,tolerance=.05,power=.8,true_ratio=1.):
    if type(bands) is not int or bands<1 or not 0<alpha<1 or not 0<tolerance<1 or not 0<power<1 or not 1-tolerance<true_ratio<1+tolerance:
        raise ValueError('parámetros inválidos')
    # Conservative log-normal design approximating our TWO marginal CP bounds.
    # Union bound controls probability of a failed equivalence declaration among bands.
    z=NormalDist().inv_cdf(1-alpha/(4*bands))
    zp=NormalDist().inv_cdf(1-(1-power)/(2*bands))
    distance=min(math.log(true_ratio/(1-tolerance)),math.log((1+tolerance)/true_ratio))
    counts=math.ceil(((2*z+math.sqrt(2)*zp)/distance)**2)
    return {'bands':bands,'alpha':alpha,'tolerance':tolerance,'target_joint_power':power,
            'assumed_true_ratio':true_ratio,'expected_counts_each_arm_each_band':counts,
            'planning_method':'conservative log-normal approximation for simultaneous marginal-binomial ratio intervals',
            'not_a_guarantee':True,'production_authorized':False}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--datos',type=Path);p.add_argument('--salida',required=True,type=Path)
    a=p.parse_args()
    r=evaluate_c3(json.loads(a.datos.read_text(encoding='utf-8'))) if a.datos else plan_equal_counts()
    with a.salida.open('x',encoding='utf-8') as f:json.dump(r,f,indent=2,allow_nan=False)

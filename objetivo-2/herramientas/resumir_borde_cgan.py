"""Síntesis de las tres parejas completas; no selecciona semillas ni acepta física."""
import argparse,math,statistics
from pathlib import Path
from datos_ajuste import read_json,atomic_json,digest
from ejecutar_borde_cgan import PAIR_SEEDS,sources
from revisar_borde_cgan import load_completed

METRICS=('Q','sky_mae','edge_mae','contrast_absolute_error','ssim','psnr')

def decision_checks(summary):
    a,b=summary['C0'],summary['C1']
    if set(a['Q_by_geometry'])!=set(b['Q_by_geometry']) or len(a['Q_by_geometry'])!=3:raise ValueError('Geometrías incompletas')
    return {'Q_reduced':b['Q']<a['Q'],'edge_reduced':b['edge_mae']<a['edge_mae'],
            'each_geometry_not_worse':all(b['Q_by_geometry'][g]<=a['Q_by_geometry'][g] for g in a['Q_by_geometry']),
            'sky_not_worse':b['sky_mae']<=a['sky_mae'],'edge_not_worse':b['edge_mae']<=a['edge_mae'],
            'contrast_support_unchanged':a['common_contrasts']==b['common_contrasts']==23,
            'contrast_not_worse':a['contrast_absolute_error'] is not None and b['contrast_absolute_error'] is not None and b['contrast_absolute_error']<=a['contrast_absolute_error'],
            'ssim_not_worse':b['ssim']>=a['ssim'],'psnr_not_worse':b['psnr']>=a['psnr']}

def summarize(reports,stage):
    if stage not in ('tecnica','piloto') or set(reports)!=set(PAIR_SEEDS):raise ValueError('Se requieren B1, B2 y B3 completas')
    first=reports['B1'];deltas={};checks={}
    for pair,report in reports.items():
        if report['pair']!=pair or report['seed']!=PAIR_SEEDS[pair] or report['stage']!=stage:raise ValueError('Pareja/semilla/etapa incompatible')
        if report['quality_evaluation']!=(stage=='piloto') or report['physical_acceptance'] or report['heldout_opened']:raise ValueError('Alcance de evaluación incompatible')
        for key in ['sources','environment','mask_manifest_sha256','initial_checkpoint_sha256','initial_inference_device']:
            if report[key]!=first[key]:raise ValueError('Evaluaciones no comparables: '+key)
        if report['summary']['inicial_cgan']!=first['summary']['inicial_cgan'] or report['summary']['entrada']!=first['summary']['entrada']:raise ValueError('Referencias diferentes entre parejas')
        deltas[pair]={}
        for metric in METRICS:
            a,b=report['summary']['C0'][metric],report['summary']['C1'][metric]
            if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or not math.isfinite(a+b):raise ValueError('Métrica ausente o no finita')
            deltas[pair][metric]=b-a
        if stage=='piloto':
            checks[pair]=decision_checks(report['summary'])
            if checks[pair]!=report['decision_checks']:raise ValueError('Clasificación incoherente con las métricas')
    aggregate={m:{'values':[deltas[p][m] for p in PAIR_SEEDS],'median':statistics.median(deltas[p][m] for p in PAIR_SEEDS),'min':min(deltas[p][m] for p in PAIR_SEEDS),'max':max(deltas[p][m] for p in PAIR_SEEDS)} for m in METRICS}
    concordant=sum(all(x.values()) for x in checks.values())
    return {'schema':'oe2-cgan-borde-summary-v1','stage':stage,'pairs':list(PAIR_SEEDS),'seeds':PAIR_SEEDS,
            'delta_definition':'C1 minus C0; negative favors Q/errors, positive favors SSIM/PSNR',
            'paired_differences':deltas,'descriptive_summary':aggregate,'checks_by_pair':checks,
            'concordant_pairs':concordant if stage=='piloto' else None,
            'pairs_reducing_Q':sum(deltas[p]['Q']<0 for p in PAIR_SEEDS),
            'decision':('concordancia_agregada_repetida' if concordant==3 else 'dependencia_de_semilla_o_compromiso') if stage=='piloto' else 'solo_comprobacion_tecnica',
            'physical_acceptance':False,'heldout_opened':False,'independent_from_scratch_training':False,
            'limitations':'Tres continuaciones condicionadas al mismo checkpoint. Sin significación ni aceptación física; conservar tablas completas de vistas/anomalías.'}

def run(a):
    reports={};checksums={}
    for pair in PAIR_SEEDS:
        folder=a.raiz/pair/'evaluacion';p=folder/'comparacion-cgan.json';report=read_json(p)
        if report['sources']!=sources():raise ValueError('Fuentes distintas de las evaluadas')
        if digest(folder/'predicciones-cgan-inicial.npy')!=report['initial_predictions_sha256']:raise ValueError('Referencia inicial alterada')
        for arm in ['C0','C1']:
            path=Path(report['run_paths'][arm])
            c=load_completed(path,arm,a.etapa,pair)
            if digest(path/'last.pt')!=report['checkpoint_sha256'][arm]:raise ValueError('Pesos distintos de la evaluación')
            for key in ['sources','environment']:
                if c['identity'][key]!=report[key]:raise ValueError('Identidad distinta: '+key)
            if c['identity']['cache_sha256']!=report['mask_manifest_sha256']:raise ValueError('Máscaras distintas')
            if c['identity']['initial_checkpoint_sha256']!=report['initial_checkpoint_sha256']:raise ValueError('Checkpoint inicial distinto')
        reports[pair]=report;checksums[pair]=digest(p)
    result=summarize(reports,a.etapa);result['evaluation_sha256']=checksums
    if a.salida.exists():raise FileExistsError('Usar una salida nueva para la síntesis')
    a.salida.parent.mkdir(parents=True,exist_ok=True);atomic_json(a.salida,result)
    print(result['decision'])

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--raiz',type=Path,required=True);p.add_argument('--salida',type=Path,required=True)
    p.add_argument('--etapa',choices=['tecnica','piloto'],default='piloto')
    run(p.parse_args())

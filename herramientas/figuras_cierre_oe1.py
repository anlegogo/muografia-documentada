"""Figuras científicas desde la campaña verificada; no modifica datos."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm
from preparar_imagen_angular_v1 import read_image
from empaquetar_angular_v1 import low_counts

ROOT=Path(__file__).resolve().parents[1]

def generate(campaign,out):
    out.mkdir(parents=True,exist_ok=False)
    evidence=ROOT/'objetivo-1/evidencias/preparacion-campana-114'
    plan=json.loads((evidence/'plan.json').read_text(encoding='utf-8'))
    expected={name.removeprefix('./'):h for h,name in (line.split(maxsplit=1) for line in (campaign/'posproceso/fusion.sha256').read_text().splitlines())}
    images={};metrics=[];all_roi=[];fractions=np.empty((19,6));source_hashes={}
    for gi,g in enumerate(plan['geometries']):
        maskpath=evidence/g['rock_roi']
        assert hashlib.sha256(maskpath.read_bytes()).hexdigest()==plan['masks_sha256'][g['rock_roi']]
        mask=np.load(maskpath,allow_pickle=False)
        for view in range(6):
            gid=g['geometry'];stem=f'{gid}_view{view}';p=campaign/'fusion'/gid/(stem+'_hist.csv')
            _,counts,coords,meta,hashes=read_image(p)
            assert hashes['hist_sha256']==expected[gid+'/'+stem+'_hist.csv']
            assert hashes['meta_sha256']==expected[gid+'/'+stem+'.meta.json']
            assert meta['events_transported']==344000000
            source_hashes[stem]=hashes;images[stem]=(counts,coords)
            values=counts.reshape(64,4,64,4).sum(axis=(1,3))[mask]
            fractions[gi,view]=np.mean(values>=100);all_roi.extend(values.tolist())
            metrics.append({'geometry':gid,'view':view,'roi':len(values),'roi_ge100':int(np.sum(values>=100)),
                'fraction_ge100':float(fractions[gi,view]),'q10':float(np.quantile(values,.1)),
                'median':float(np.median(values)),'total_selected':int(counts.sum())})
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    figures=[]
    def save(fig,name):
        for suffix in ('png','pdf'):
            fig.savefig(out/(name+'.'+suffix),dpi=180,bbox_inches='tight')
        plt.close(fig);figures.append(name)
    selected=['geo-train-01_view0','geo-train-06_view3','geo-test-03_view5','geo-gen-01_view0','geo-val-01_view0','geo-train-09_view1']
    maximum=max(int(images[s][0].max()) for s in selected)
    norm=SymLogNorm(linthresh=1,vmin=0,vmax=maximum,base=10)
    fig,axes=plt.subplots(2,3,figsize=(12,8),layout='constrained')
    for ax,stem in zip(axes.flat,selected):
        c,coord=images[stem];im=ax.pcolormesh(coord['az_edges_deg'],coord['el_edges_deg'],c,norm=norm,cmap='viridis',rasterized=True)
        ax.set(title=stem.replace('_view',' · vista '),xlabel='Azimut relativo (°)',ylabel='Elevación (°)')
    fig.colorbar(im,ax=axes.ravel().tolist(),label='Conteos por píxel · escala logarítmica, lineal entre 0 y 1',shrink=.86)
    fig.suptitle('Referencias de transmisión · 344 millones de primarios por vista',fontsize=15)
    save(fig,'01-referencias')
    stem='geo-train-06_view3';c,coord=images[stem];lows=low_counts(c,'geo-train-06',3)
    expected_pairs=json.loads((campaign/'huellas-contenido.json').read_text())['pairs'][stem+'_pairs.npz']
    h=hashlib.sha256();h.update(lows.dtype.str.encode());h.update(str(lows.shape).encode());h.update(np.ascontiguousarray(lows).tobytes())
    assert h.hexdigest()==expected_pairs['low_counts']
    fig,axes=plt.subplots(1,5,figsize=(16,4.7),layout='constrained')
    norm=SymLogNorm(linthresh=1,vmin=0,vmax=int(c.max()),base=10)
    for ax,a,title in zip(axes,[c,*[lows[i,0] for i in range(4)]],['Referencia','f = 0,50','f = 0,10','f = 0,05','f = 0,01']):
        im=ax.pcolormesh(coord['az_edges_deg'],coord['el_edges_deg'],a,norm=norm,cmap='viridis',rasterized=True)
        ax.set(title=title,xlabel='Azimut relativo (°)');ax.set_ylabel('Elevación (°)')
    fig.colorbar(im,ax=axes.tolist(),label='Conteos por píxel · misma escala logarítmica en los cinco paneles',shrink=.85)
    fig.suptitle('geo-train-06 · vista 3 · primera realización de cada fracción\nAdelgazamiento binomial; semilla maestra 20260805',fontsize=14)
    save(fig,'02-pares')
    fig,(ax,cdf)=plt.subplots(1,2,figsize=(13,9),layout='constrained',gridspec_kw={'width_ratios':[1.2,1]})
    im=ax.imshow(fractions*100,vmin=85,vmax=100,cmap='YlGnBu',aspect='auto')
    ax.set_xticks(range(6),[str(i) for i in range(6)]);ax.set_yticks(range(19),[g['geometry'] for g in plan['geometries']]);ax.set(xlabel='Vista',title='ROI con al menos 100 cuentas (%)')
    for gi in range(19):
        for v in range(6):
            val=fractions[gi,v]*100
            ax.text(v,gi,f'{val:.1f}'+('*' if val<90 else ''),ha='center',va='center',fontsize=8,color='white' if val>95 else 'black')
    fig.colorbar(im,ax=ax,label='Porcentaje por vista',shrink=.55)
    values=np.sort(all_roi)
    thresholds,first=np.unique(values,return_index=True)
    survival=(len(values)-first)/len(values)*100
    cdf.step(thresholds,survival,where='pre',color='#17627b',linewidth=2)
    global_fraction=np.mean(values>=100)*100
    cdf.axvline(100,color='#b44420',linestyle='--',label='100 cuentas por ROI')
    cdf.scatter([100],[global_fraction],color='#b44420',zorder=4)
    cdf.annotate(f'{global_fraction:.2f} % global',xy=(100,global_fraction),xytext=(150,80),arrowprops={'arrowstyle':'->'})
    cdf.set(xlabel='Umbral de cuentas por ROI de 4 × 4 píxeles',ylabel='ROI que alcanzan el umbral (%)',title='Distribución global de 21.816 ROI',xlim=(0,float(np.quantile(values,.995))),ylim=(0,103))
    cdf.grid(alpha=.2);cdf.legend(loc='lower left')
    fig.suptitle('Calidad de conteo en roca · 107/114 vistas alcanzan la meta del 90 %\n* Siete vistas bajo la meta, conservadas sin aumentar N',fontsize=14)
    save(fig,'03-calidad-roca')
    result={'source_commit':'f395570','sources':source_hashes,'figures':figures,'metrics':metrics,
        'global_roi':len(all_roi),'global_roi_ge100':int(np.sum(values>=100)),'selected_examples':selected,
        'example_selection':'Fixed heterogeneous examples, including below-goal views; not a representative statistical sample.',
        'pair_example':{'view':stem,'replicate_index':0,'master_seed':20260805,'low_counts_hash_verified':True},
        'limits':'Images are directional primary counts, not density maps or calibrated physical transmission. ROI selection ignores anomalies; simulation retains them.'}
    (out/'datos-figuras.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--campana',type=Path,required=True);p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args();r=generate(a.campana,a.salida);print(json.dumps({'figures':r['figures'],'global_roi':r['global_roi'],'global_roi_ge100':r['global_roi_ge100']}))

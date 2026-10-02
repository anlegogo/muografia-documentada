"""Representación con bordes explícitos; ROI opcional exige compatibilidad."""
import argparse
import os
from pathlib import Path
import numpy as np
cache=Path(__file__).resolve().parents[1]/'trabajo/matplotlib'
cache.mkdir(parents=True,exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(cache))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from empaquetar_angular_v1 import load
from analizar_roi_angular_v1 import analyze


def render(image,output,regions=None):
    output=Path(output)
    if output.exists():raise FileExistsError(output)
    item=load(image);m=item['meta'];c=item['coords'];counts=item['counts']
    if regions is not None:
        analyze(image,regions)  # All identity/geometry/grid checks before plotting.
        path=Path(regions)/f"{m['geometry_id']}_view{m['view_index']}_roi.npz"
        with np.load(path,allow_pickle=False) as z:mask=z['roi_z_ge20m'].copy()
    fig,ax=plt.subplots(figsize=(9,5.3))
    fig.subplots_adjust(left=.10,right=.91,bottom=.19,top=.84)
    mesh=ax.pcolormesh(c['az_edges_deg'],c['el_edges_deg'],counts,shading='flat',cmap='viridis')
    fig.colorbar(mesh,ax=ax,label='Conteos por píxel')
    if regions is not None and mask.any() and not mask.all():
        ax.contour(c['az_centers_deg'],c['el_centers_deg'],mask.astype(float),levels=[.5],colors='white')
    ax.set(xlabel='Azimut relativo (grados)',ylabel='Elevación (grados)',
           title=f"{m['geometry_id']} · vista {m['view_index']} · az-edges-v1\n"
                 f"{m['events_transported']:,} primarios / {m['detected_in_bins']:,} registros")
    fig.text(.5,.035,'Comprobación técnica; no es una validación de aceptación física.',ha='center',fontsize=9)
    fig.savefig(output,dpi=160);plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('imagen',type=Path)
    p.add_argument('--salida',required=True,type=Path);p.add_argument('--regiones',type=Path);a=p.parse_args()
    render(a.imagen,a.salida,a.regiones)

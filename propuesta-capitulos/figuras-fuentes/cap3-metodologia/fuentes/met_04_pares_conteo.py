"""met_04_pares_conteo: entradas reducidas a partir de una referencia finita.

Panels: reference counts and the four binomial-thinned realizations
(fractions 0.5, 0.1, 0.05, 0.01) of geo-train-06, view 3, realization 0.
Selection rule: geometry/view/realization = the pair already used by the
director in the OE1 closing figure 2; geo-train-06 is a training geometry
(no reserved geometry is drawn). Raw counts (NOT rescaled by 1/f, NOT the
network transformation) are drawn with a common symmetric-log colour scale,
used for display only. Cells are exact pcolormesh polygons (vector).

Data (campaign 114, content-identical to delivery commit f395570 of
anlegogo/muografia-documentada):
  datos-oe1-campana-114/pares/geo-train-06_view3_pairs.npz
    file SHA-256 26114600402d9b54235e4f03f824b97993f19d6a3a8833992494bf3d95af08b1
    content SHA-256 (huellas-contenido.json, verified here):
      counts_ref 5cfd1276189145b05a6b097d67f4ec7d492ea082533e37516d91e6c75be87e37
      low_counts eddb17102714a3e5c915a1caf10b72ced22bcfa0b024e70e01d966b8d6e07977
      fractions  757086f23381b51f93f46552e338b416e8763b04ab83213c07001f08a5afeb79
Hash file: branch oe1/justificacion-fisica-produccion (800ab863), path
  objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/datos/sc3/
  campana-114/huellas-contenido.json
Source commit of data: f395570.
"""
import hashlib
import os
import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import SymLogNorm
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo_tesis import C, COUNT_CMAP, apply_comma, plt  # noqa: E402
from guardar_vector import save_native  # noqa: E402

SRC = Path(os.environ.get('DATOS_OE1', r'C:/Users/etherion/Documents/tesis-ing-sistemas/datos-oe1-campana-114')) / 'pares/geo-train-06_view3_pairs.npz'
EXPECT = {'counts_ref': '5cfd1276189145b05a6b097d67f4ec7d492ea082533e37516d91e6c75be87e37',
          'low_counts': 'eddb17102714a3e5c915a1caf10b72ced22bcfa0b024e70e01d966b8d6e07977',
          'fractions': '757086f23381b51f93f46552e338b416e8763b04ab83213c07001f08a5afeb79'}


def content_hash(a):
    h = hashlib.sha256()
    h.update(a.dtype.str.encode())
    h.update(str(a.shape).encode())
    h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


z = np.load(SRC)
for k, v in EXPECT.items():
    assert content_hash(z[k]) == v, k
REAL = 0
ref = z['counts_ref'].astype(float)
fr = z['fractions']
low = {float(f): z['low_counts'][i, REAL].astype(float) for i, f in enumerate(fr)}
azE, elE = z['az_edges_deg'], z['el_edges_deg']
assert azE[0] == -30 and azE[-1] == 30

W, H = 15.0, 9.7
fig = plt.figure(figsize=(W / 2.54, H / 2.54))


def ax_cm(x, y, w, h):
    return fig.add_axes([x / W, y / H, w / W, h / H])


vmax = float(ref.max())
norm = SymLogNorm(linthresh=1, linscale=0.6, vmin=0, vmax=vmax, base=10)


def panel(ax, data, label, ylab=True):
    m = ax.pcolormesh(azE, elE, data, cmap=COUNT_CMAP, norm=norm, rasterized=False,
                      shading='flat', linewidth=0, antialiased=False)
    ax.set_xlim(-30, 30)
    ax.set_ylim(elE[0], elE[-1])
    ax.set_xticks([-20, 0, 20])
    ax.set_yticks([2, 25, 47])
    apply_comma(ax)
    ax.set_xlabel('acimut relativo (°)', labelpad=1)
    if ylab:
        ax.set_ylabel('elevación (°)', labelpad=1)
    else:
        ax.tick_params(labelleft=False)
    ax.text(0.03, 0.96, label, transform=ax.transAxes, va='top', ha='left', fontsize=7.5,
            bbox=dict(fc='white', ec='none', pad=1.2, alpha=0.9))
    return m


# top: reference
axr = ax_cm(1.0, 6.2, 4.6, 3.35)
mesh = panel(axr, ref, '(a) referencia')
# bottom: four fractions
pw, ph, gap, x0, y0 = 3.0, 2.25, 0.5, 1.0, 0.95
labels = [r'(b) 50\,\%', r'(c) 10\,\%', r'(d) 5\,\%', r'(e) 1\,\%']
fvals = ['0{,}5', '0{,}1', '0{,}05', '0{,}01']
for i, f in enumerate(fr):
    x = x0 + i * (pw + gap)
    a = ax_cm(x, y0, pw, ph)
    panel(a, low[float(f)], labels[i], ylab=(i == 0))
    # label + arrow from reference
    cx = x + pw / 2
    fig.text(cx / W, (y0 + ph + 0.08) / H, 'adelgazamiento binomial\n' + r'$f=' + fvals[i] + '$',
             ha='center', va='bottom', fontsize=6.5, linespacing=1.0)
    arr = FancyArrowPatch((3.3 / W, 5.4 / H), (cx / W, (y0 + ph + 0.72) / H),
                          transform=fig.transFigure, arrowstyle='-|>', mutation_scale=7,
                          lw=0.8, color=C['oe1'], shrinkA=1, shrinkB=0)
    fig.add_artist(arr)

# colour bar and note (top right)
cax = ax_cm(7.3, 8.9, 7.0, 0.28)
# Vector colour bar: the stock colorbar embeds a small raster image, so it is
# drawn as 256 rectangles spaced uniformly in the normalised (SymLog) domain.
import numpy as _np
import matplotlib
_norm = mesh.norm
_cmap = mesh.get_cmap()
_t = _np.linspace(0.0, 1.0, 257)
_vals = _norm.inverse(_t)
cax.pcolormesh(_vals, [0, 1], _np.atleast_2d(_t[:-1] + 0.5 / 256), cmap=_cmap,
               vmin=0, vmax=1, shading='flat', rasterized=False, edgecolors='face', linewidth=0)
cax.set_xscale(mesh.norm.__class__.__name__ == 'SymLogNorm' and 'symlog' or 'linear',
               **({'linthresh': _norm.linthresh, 'linscale': _norm._scale.linscale}
                  if mesh.norm.__class__.__name__ == 'SymLogNorm' else {}))
cax.set_xlim(_norm.vmin, _norm.vmax)
cax.set_yticks([])
cax.set_xticks([0, 1, 10, 100, 1000])
cax.set_xticklabels(['0', '1', '10', '100', '1000'])
cax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
cax.xaxis.set_ticks_position('top')
cax.xaxis.set_label_position('bottom')
cax.set_xlabel('conteos por celda (escala logarítmica de visualización)', fontsize=7.5, labelpad=2)
for _s in cax.spines.values():
    _s.set_linewidth(0.4)
fig.text(7.3 / W, 7.6 / H,
         'Conteos sin reescalar por $1/f$ y sin la transformación de la red.\n'
         'Escala común a los cinco paneles; lineal entre 0 y 1.\n'
         'Todas las realizaciones comparten la misma referencia finita.',
         ha='left', va='top', fontsize=7, linespacing=1.15)

out = save_native(fig, 'met_04_pares_conteo')
print(out, out.stat().st_size)

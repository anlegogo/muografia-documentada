"""met_03_malla_angular: correspondence between recorded direction and image coordinates.

(a) schematic of observer, arrival direction, elevation and relative azimuth;
(b) simplified 8x8 grid labelled as a scheme (the real grid is 256x256);
(c) exact edges and centres read from a final NPZ (not from historical images).

Coordinates: datos-oe1-campana-114/imagenes/geo-train-06_view0.npz
  (geo-train-06 is a training geometry; view 0 chosen by the neutral rule
  "first view"; the angular grid is identical for every geometry and view,
  asserted below against the pairs file of geo-train-06 view 3).
  file SHA-256 08cfdd69120ddce0cc7fe20f4f6c433ba695c244c397d39e30bcd0c28ec7d47c
  pairs file used for the cross-check (geo-train-06_view3_pairs.npz):
  file SHA-256 26114600402d9b54235e4f03f824b97993f19d6a3a8833992494bf3d95af08b1
Conventions (meta.json of the campaign): azimuth_convention az-edges-v1,
  elevation_convention legacy-centers-2-47, n_az = n_el = 256.
Data source commit: f395570 (muografia-documentada), campaign 114.
"""
import os
import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch, Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo_tesis import C, plt, save  # noqa: E402

B = Path(os.environ.get('DATOS_OE1', r'C:/Users/etherion/Documents/tesis-ing-sistemas/datos-oe1-campana-114'))
z = np.load(B / 'imagenes/geo-train-06_view0.npz')
azE, azC, elE, elC = (z[k] for k in ('az_edges_deg', 'az_centers_deg', 'el_edges_deg', 'el_centers_deg'))
zp = np.load(B / 'pares/geo-train-06_view3_pairs.npz')
for k in ('az_edges_deg', 'az_centers_deg', 'el_edges_deg', 'el_centers_deg'):
    assert np.array_equal(z[k], zp[k])
assert len(azC) == len(elC) == 256 and len(azE) == len(elE) == 257
assert azE[0] == -30 and azE[-1] == 30
assert np.allclose(elC, np.linspace(2, 47, 256), rtol=0, atol=1e-12)
assert np.allclose(azC, (azE[:-1] + azE[1:]) / 2) and np.allclose(elC, (elE[:-1] + elE[1:]) / 2)
dphi, deps = azE[1] - azE[0], elE[1] - elE[0]


def fm(v, n=4):
    """Number for math mode with decimal comma."""
    return ('-' if v < 0 else '') + f'{abs(v):.{n}f}'.replace('.', '{,}')


W, H = 15.0, 8.0
fig = plt.figure(figsize=(W / 2.54, H / 2.54))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis('off')
col, lc, ink = C['oe1'], C['linea'], C['texto']
FS = 7.5


def T(x, y, s, **k):
    k.setdefault('fontsize', FS)
    k.setdefault('ha', 'center')
    k.setdefault('va', 'center')
    return ax.text(x, y, s, **k)


# ---------------- (a) schematic ----------------
T(0.1, 7.9, '(a)', ha='left', va='top')
ox, oy = 0.9, 5.15
ax.plot([ox, 4.6], [oy, oy], ls=(0, (4, 2)), c=lc, lw=0.7)
T(4.6, oy - 0.25, 'horizonte', ha='right', fontsize=7, color=lc)
eps = np.deg2rad(33)
L = 3.3
tip = (ox + L * np.cos(eps), oy + L * np.sin(eps))
ax.plot([ox, tip[0]], [oy, tip[1]], c=lc, lw=0.7)
p0 = (ox + 0.72 * L * np.cos(eps), oy + 0.72 * L * np.sin(eps))
p1 = (ox + 0.2 * L * np.cos(eps), oy + 0.2 * L * np.sin(eps))
ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=8, lw=1.4, color=col, shrinkA=0, shrinkB=0))
ax.add_patch(Arc((ox, oy), 1.5, 1.5, theta1=0, theta2=33, color=ink, lw=0.7))
T(ox + 1.05, oy + 0.28, r'$\varepsilon$', fontsize=8)
ax.plot([ox], [oy], 'o', ms=3.5, c=ink)
T(ox - 0.05, oy - 0.38, 'observador', ha='left', fontsize=7)
T(tip[0] - 0.05, tip[1] + 0.28, 'dirección de llegada', ha='right', fontsize=7)
T(2.45, 7.65, 'vista lateral', fontsize=7, color=lc)
# top view
tx, ty = 2.45, 0.55
R = 3.0
ang = np.deg2rad(30)
ax.add_patch(Polygon([(tx, ty), (tx - R * np.sin(ang), ty + R * np.cos(ang)), (tx + R * np.sin(ang), ty + R * np.cos(ang))],
                     closed=True, fc=C['neutro'], ec='none', alpha=0.6))
for s in (-1, 1):
    ax.plot([tx, tx + s * R * np.sin(ang)], [ty, ty + R * np.cos(ang)], c=lc, lw=0.6)
ax.plot([tx, tx], [ty, ty + 3.15], ls=(0, (4, 2)), c=lc, lw=0.7)
ph = np.deg2rad(14)
Lp = 2.7
pt = (tx + Lp * np.sin(ph), ty + Lp * np.cos(ph))
ax.plot([tx, pt[0]], [ty, pt[1]], c=lc, lw=0.7)
q0 = (tx + 0.75 * Lp * np.sin(ph), ty + 0.75 * Lp * np.cos(ph))
q1 = (tx + 0.2 * Lp * np.sin(ph), ty + 0.2 * Lp * np.cos(ph))
ax.add_patch(FancyArrowPatch(q0, q1, arrowstyle='-|>', mutation_scale=8, lw=1.4, color=col, shrinkA=0, shrinkB=0))
ax.add_patch(Arc((tx, ty), 1.7, 1.7, theta1=90 - 14, theta2=90, color=ink, lw=0.7))
T(tx + 0.42, ty + 1.02, r'$\varphi$', fontsize=8)
ax.plot([tx], [ty], 'o', ms=3.5, c=ink)
T(tx, ty + 3.4, r'eje de la vista ($\varphi=0$)', fontsize=7)
T(tx - R * np.sin(ang) - 0.05, ty + R * np.cos(ang) + 0.2, r'$-30^\circ$', fontsize=7, ha='right')
T(tx + R * np.sin(ang) + 0.05, ty + R * np.cos(ang) + 0.2, r'$30^\circ$', fontsize=7, ha='left')
T(4.65, 0.55, 'vista superior', fontsize=7, color=lc, ha='right')

# ---------------- (b) simplified grid ----------------
T(5.3, 7.9, '(b)', ha='left', va='top')
gx, gy, gs = 5.75, 1.75, 0.42   # lower-left corner and cell size (cm)
n = 8
ax.add_patch(Rectangle((gx + 2 * gs, gy + 5 * gs), gs, gs, fc=C['neutro'], ec='none'))
for k in range(n + 1):
    ax.plot([gx, gx + n * gs], [gy + k * gs] * 2, c=lc, lw=0.5)
    ax.plot([gx + k * gs] * 2, [gy, gy + n * gs], c=lc, lw=0.5)
ax.add_patch(Rectangle((gx, gy), n * gs, n * gs, fc='none', ec=ink, lw=0.8))
for k in range(n):
    T(gx + (k + 0.5) * gs, gy + n * gs + 0.17, str(k), fontsize=6.5)
    T(gx - 0.17, gy + (k + 0.5) * gs, str(k), fontsize=6.5)
T(gx + n * gs / 2, gy + n * gs + 0.45, r'columna $j$ (acimut crece $\rightarrow$)', fontsize=7)
T(gx - 0.62, gy + n * gs / 2, r'fila $i$ (elevación crece $\rightarrow$)', fontsize=7, rotation=90)
dx, dy = gx + 2.62 * gs, gy + 5.4 * gs
ax.plot([dx], [dy], 'o', ms=3.2, c=col)
ax.plot([dx, dx], [gy, dy], ls=(0, (2, 2)), c=col, lw=0.6)
ax.plot([gx, dx], [dy, dy], ls=(0, (2, 2)), c=col, lw=0.6)
T(dx + 0.12, gy - 0.17, r'$\varphi$', fontsize=7.5, color=col)
T(gx + 0.1, dy - 0.2, r'$\varepsilon$', fontsize=7.5, color=col, ha='left')
T(gx + 0.3, gy + 0.2, r'$(0,0)$', fontsize=6, color=ink)
T(gx + n * gs - 0.04, gy + n * gs - 0.2, r'$(255,255)$', fontsize=5.5, ha='right', color=ink)
T(gx, gy - 0.38, r'$-30^\circ$', fontsize=7)
T(gx + n * gs, gy - 0.38, r'$30^\circ$', fontsize=7)
T(gx + n * gs + 0.08, gy, '$' + fm(elE[0]) + r'^\circ$', fontsize=6.5, ha='left')
T(gx + n * gs + 0.08, gy + n * gs, '$' + fm(elE[-1]) + r'^\circ$', fontsize=6.5, ha='left')
T(gx + n * gs / 2, gy - 0.68, r'acimut relativo $\varphi$ ($^\circ$)', fontsize=7)
T(gx + n * gs / 2 + 0.2, gy - 1.12, r'esquema 8$\times$8; la rejilla real es 256$\times$256', fontsize=6.8, color=lc)
T(gx + n * gs / 2 + 0.2, gy - 1.42, 'origen gráfico abajo a la izquierda', fontsize=6.8, color=lc)

# ---------------- (c) exact values ----------------
T(10.05, 7.9, '(c)', ha='left', va='top')
x0 = 10.15
cx = [x0 + 0.2, x0 + 1.25, x0 + 2.65, x0 + 4.05]


def row(y, cells, bold=False):
    for xx, s in zip(cx, cells):
        T(xx, y, s, fontsize=6.7, fontweight='bold' if bold else 'normal')


def block(y, head, idx, edges, centres, is_i):
    T(x0 + 2.4, y, head, fontsize=7.2)
    row(y - 0.38, ['$i$' if is_i else '$j$', 'borde inf.' if is_i else 'borde izq.', 'centro',
                   'borde sup.' if is_i else 'borde der.'], bold=True)
    ax.plot([x0, x0 + 4.8], [y - 0.55] * 2, c=lc, lw=0.5)
    yy = y - 0.82
    for k in idx:
        row(yy, [str(k), '$' + fm(edges[k]) + '$', '$' + fm(centres[k]) + '$', '$' + fm(edges[k + 1]) + '$'])
        yy -= 0.4
        if k == 1:
            row(yy + 0.03, [r'$\vdots$'] * 4)
            yy -= 0.5
    return yy


y = block(7.45, r'acimut relativo $\varphi$ ($^\circ$), columna $j$', (0, 1, 255), azE, azC, False)
y = block(y - 0.35, r'elevación $\varepsilon$ ($^\circ$), fila $i$', (0, 1, 255), elE, elC, True)
T(x0 + 2.4, y - 0.1, r'$\Delta\varphi=' + fm(dphi) + r'^\circ$, $\Delta\varepsilon=' + fm(deps) + r'^\circ$',
  fontsize=6.5, color=lc)
T(x0 + 2.4, y - 0.4, '257 bordes y 256 centros por eje.', fontsize=6.5, color=lc)
T(x0 + 2.4, y - 0.7, 'Leídos de geo-train-06, vista 0 (NPZ final).', fontsize=6.5, color=lc)

out = save(fig, 'met_03_malla_angular')
print(out, out.stat().st_size)

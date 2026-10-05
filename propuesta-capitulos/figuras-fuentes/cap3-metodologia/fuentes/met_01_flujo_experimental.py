"""met_01_flujo_experimental: secuencia experimental y separacion de particiones."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch
from estilo_tesis import C, figure, save

fig, ax = figure(0.60)
ax.set_xlim(0, 100); ax.set_ylim(-2, 52); ax.axis('off')
BW, BH = 17.6, 10
DASH = (0, (3, 2))


def box(x, y, text, col, w=BW, h=BH, ls='-', pending=False):
    if pending:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.2',
                                    fc='white', ec=col, lw=1.0, ls=ls, zorder=2))
    else:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.2',
                                    fc=col, ec='none', alpha=0.22, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.2',
                                    fc='none', ec=col, lw=1.0, ls=ls, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=7.5,
            color='black', zorder=4, linespacing=1.15)


def arrow(p0, p1, col='black', ls='-', lw=0.9):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=7,
                                 color=col, lw=lw, ls=ls, zorder=1, shrinkA=0, shrinkB=0))


def line(xs_, ys_, col='black', lw=0.9, ls='-', z=1):
    ax.plot(xs_, ys_, color=col, lw=lw, ls=ls, zorder=z, solid_capstyle='butt')


xs = [0, 20.6, 41.2, 61.8, 82.4]
y1, y2 = 40, 20
r1 = [('Catálogo\ny fuente', 'oe1'),
      ('Simulación\nGeant4', 'oe1'),
      ('114 referencias', 'oe1'),
      ('Submuestreo\nde conteos', 'oe1'),
      ('Partición\npor geometría', 'oe1')]
for x, (t, c) in zip(xs, r1):
    box(x, y1, t, C[c])
for a, b in zip(xs[:-1], xs[1:]):
    arrow((a + BW, y1 + BH / 2), (b, y1 + BH / 2))

r2 = [('Escala ajustada\nsolo con\nentrenamiento', 'oe2'),
      ('Entrenamiento\ny selección\ncon validación', 'oe2'),
      ('Ocho modelos\ncongelados', 'oe2'),
      ('Evaluación en\nprueba y\ngeneralización', 'oe3'),
      ('Curvas\ndescriptivas', 'oe3')]
for x, (t, c) in zip(xs, r2):
    box(x, y2, t, C[c])
for a, b in zip(xs[:-1], xs[1:]):
    arrow((a + BW, y2 + BH / 2), (b, y2 + BH / 2))

# Row 1 -> row 2: only train/val part of the partition
ymid = y1 - 5
xr = xs[4] + BW / 2
line([xr, xr], [y1, ymid], col=C['linea'])
line([xr, xs[0] + BW / 2], [ymid, ymid], col=C['linea'])
arrow((xs[0] + BW / 2, ymid), (xs[0] + BW / 2, y2 + BH), col=C['linea'])
ax.text(xs[1] + 3, ymid + 0.7, 'entrenamiento y validación',
        fontsize=7.5, ha='center', va='bottom')

# Frontier
fx = (xs[1] + BW + xs[2]) / 2
line([fx, fx], [-1.5, 31.5], col='black', lw=1.8, z=5)
ax.text(fx - 0.9, 31.7, 'frontera', ha='right', va='bottom', fontsize=7.5, fontweight='bold')
ax.text(fx - 1.2, -1.2, 'zona de ajuste', ha='right', va='bottom', fontsize=7.5)
ax.text(fx + 1.2, -1.2, 'zona congelada', ha='left', va='bottom', fontsize=7.5)

# Reserved partitions
rx, ry, rw, rh = xs[2], 5.0, xs[3] + BW - xs[2] - 0.0, 8.0
yb = ry + rh / 2
ax.add_patch(FancyBboxPatch((rx, ry), rw, rh, boxstyle='round,pad=0,rounding_size=1.2',
                            fc='white', ec='black', lw=1.0, hatch='////', zorder=2))
ax.add_patch(FancyBboxPatch((rx + 3.5, ry + 1.9), rw - 7, rh - 3.8,
                            boxstyle='round,pad=0,rounding_size=1', fc='white', ec='none', zorder=3))
ax.text(rx + rw / 2, ry + rh / 2, 'Prueba y generalización', ha='center', va='center',
        fontsize=7.5, zorder=4)
# partition -> reserved (branch through the gap between evaluation and curves)
gx = (xs[3] + BW + xs[4]) / 2
line([gx, gx], [ymid, yb])
ax.text(gx - 1.0, ymid - 1.0, 'prueba y generalización (reservadas)', fontsize=7.5, ha='right', va='top')
line([gx, rx + rw], [yb, yb])
arrow((gx - 0.01, yb), (rx + rw, yb))
# reserved -> evaluation
arrow((xs[3] + BW / 2, ry + rh), (xs[3] + BW / 2, y2))

# Blocked path into the fitting zone
yb = ry + rh / 2
arrow((rx, yb), (xs[1] + BW / 2, yb), ls=DASH)
cx = fx - 3
line([cx - 1.3, cx + 1.3], [yb - 1.6, yb + 1.6], lw=1.6, z=6)
line([cx - 1.3, cx + 1.3], [yb + 1.6, yb - 1.6], lw=1.6, z=6)
ax.text(xs[0] + 0.5, yb + 0.2, 'sin uso para ajustar\nescala ni pesos', fontsize=7.5,
        ha='left', va='center')

# Pending criterion
box(xs[4], ry - 0.5, 'Criterio final de\nadquisición\n(pendiente)', C['oe3'], h=9, ls=DASH, pending=True)
arrow((xs[4] + BW / 2, y2), (xs[4] + BW / 2, ry - 0.5 + 9), col=C['oe3'], ls=DASH)

hs = [Patch(fc=C['oe1'], alpha=0.22, ec=C['oe1'], label='OE1 generación'),
      Patch(fc=C['oe2'], alpha=0.22, ec=C['oe2'], label='OE2 aprendizaje'),
      Patch(fc=C['oe3'], alpha=0.22, ec=C['oe3'], label='OE3 evaluación'),
      Patch(fc='white', ec='black', hatch='////', label='partición reservada')]
ax.legend(handles=hs, loc='lower center', bbox_to_anchor=(0.5, 0.97), ncol=4,
          frameon=False, fontsize=7.5, handlelength=1.6, columnspacing=1.2)
print(save(fig, 'met_01_flujo_experimental'))

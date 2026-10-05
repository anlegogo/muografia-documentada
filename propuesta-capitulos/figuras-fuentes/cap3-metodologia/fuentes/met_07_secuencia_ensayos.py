"""met_07_secuencia_ensayos: desarrollo experimental y seleccion del conjunto final."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from estilo_tesis import C, figure, save

fig, ax = figure(0.98)
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
DASH = (0, (3, 2))
FS = 7.5


def rbox(x, y, w, h, col=None, tint=0.22, ec=None, ls='-', lw=1.0, z=2):
    if col is not None:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.0',
                                    fc=col, ec='none', alpha=tint, zorder=z))
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.0',
                                fc='none', ec=ec or col or 'black', lw=lw, ls=ls, zorder=z + 1))


def txt(x, y, s, ha='left', va='center', bold=False, size=FS, z=6):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, zorder=z,
            fontweight='bold' if bold else 'normal', linespacing=1.15)


def arrow(p0, p1, col='black', ls='-', lw=0.9):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=7, color=col,
                                 lw=lw, ls=ls, zorder=1, shrinkA=0, shrinkB=0))


LX, LW = 1.8, 58.0
H, GAP = 10.6, 2.0
r1_h = 13.5
y1 = 97.0 - 4.5 - r1_h

rbox(0, 9.0, 61.5, 90.5, ec=C['linea'], ls=DASH, lw=0.8)
txt(1.2, 97.6, 'Antecedentes (ajustes sobre validación)', bold=True)
rbox(63.5, 9.0, 36.5, 90.5, ec='black', lw=1.3)
txt(81.75, 97.6, 'Ocho redes finales', ha='center', bold=True)

# Row 1: pilot
sub_h = (r1_h - 1.5) / 2
yu = y1 + sub_h + 1.5
rbox(LX, yu, LW, sub_h, col=C['unet'])
rbox(LX, y1, LW, sub_h, col=C['cgan'])
txt(LX + 1.2, yu + sub_h / 2, 'Piloto U-Net (L1) desde cero, 5 %; época 5')
txt(LX + 1.2, y1 + sub_h / 2, 'Piloto cGAN desde cero, 5 %; época 5')
txt(LX + LW - 1.0, y1 + r1_h + 1.3, '2026-10-03', ha='right', size=FS)

rows = [
    ('2026-10-03', None, 'Diagnóstico regional en validación',
     'Sesgo de cuentas por región:\ncielo, roca, borde y anomalías'),
    ('2026-10-03', C['unet'], 'Ajuste de cuentas U-Net',
     'Desde los pesos U-Net de época 5.\nA: control (100 L1); B: 100 L1 más término regional'),
    ('2026-10-03/04', C['cgan'], 'Continuaciones cGAN',
     'Desde la cGAN de época 5.\nC0: sin término regional; C1: con término regional'),
    ('2026-10-04', C['cgan'], 'Repetición R1\u2013R3',
     'Tres semillas nuevas, misma cGAN de época 5.\nC0/C1 como en la continuación cGAN'),
    ('2026-10-04', C['cgan'], 'Ensayo espacial E1: B1\u2013B3',
     'Misma cGAN de época 5 (semillas 2026100411\u201313).\nC0: regional; C1: regional más borde (0,629)'),
]
ys = []
ycur = y1 - GAP - H
for d, col, title, body in rows:
    ys.append(ycur)
    if col is None:
        rbox(LX, ycur, LW, H, col=C['neutro'], tint=0.6, ec=C['linea'])
    else:
        rbox(LX, ycur, LW, H, col=col)
    txt(LX + 1.2, ycur + H - 2.6, title, bold=True)
    txt(LX + LW - 1.0, ycur + H - 2.6, d, ha='right')
    txt(LX + 1.2, ycur + H - 5.0, body, va='top')
    ycur -= H + GAP

cx = LX + LW / 2
arrow((cx, y1), (cx, ys[0] + H))
for a, b in zip(ys[:-1], ys[1:]):
    arrow((cx, a), (cx, b + H))

# Final column
FX, FW = 65.0, 33.5
tag_h = 5.4
fy_u = yu + (sub_h - tag_h) / 2
fy_c = y1 + (sub_h - tag_h) / 2
rbox(FX, fy_u, FW, tag_h, col=C['unet'])
txt(FX + FW / 2, fy_u + tag_h / 2, 'U-Net original', ha='center')
rbox(FX, fy_c, FW, tag_h, col=C['cgan'])
txt(FX + FW / 2, fy_c + tag_h / 2, 'cGAN original', ha='center')
arrow((LX + LW, yu + sub_h / 2), (FX, fy_u + tag_h / 2))
arrow((LX + LW, y1 + sub_h / 2), (FX, fy_c + tag_h / 2))

# E1 grid
cw, ch, pitch = 12.0, 3.8, 4.7
gx = [FX + 6.0, FX + 6.0 + cw + 1.4]
gbot = 10.2
gtop = gbot + 3 * pitch - 0.9
txt(gx[0] + cw / 2, gtop + 2.2, 'C0', ha='center', bold=True)
txt(gx[1] + cw / 2, gtop + 2.2, 'C1', ha='center', bold=True)
for i, b in enumerate(['B1', 'B2', 'B3']):
    gy = gbot + (2 - i) * pitch
    txt(FX + 0.6, gy + ch / 2, b, bold=True)
    for j, (xx, mk) in enumerate(zip(gx, ['o', 's'])):
        rbox(xx, gy, cw, ch, col=C['cgan'])
        ax.plot([xx + 2.0], [gy + ch / 2], marker=mk, ms=4.0, mfc=C['cgan'] if j else 'white',
                mec=C['cgan'], mew=1.0, zorder=7, ls='none')
        txt(xx + 3.6, gy + ch / 2, f'{b}\u2013C{j}')
arrow((LX + LW, ys[4] + H / 2), (FX - 0.3, ys[4] + H / 2))

# Shared initial weights
sx = FX + FW - 2.0
arrow((sx, fy_c), (sx, gtop + 4.6), col=C['cgan'], ls=DASH, lw=1.2)
txt(FX + 1.0, 59.0,
    'Pesos iniciales\ncompartidos:\nmismos G y D\nde la cGAN\nde época 5;\noptimizadores\nnuevos; cinco\népocas adicionales;\nselección fija\nde la última',
    ha='left', va='center')
txt(FX + 1.0, 37.0,
    'Los ajustes U-Net,\nlas continuaciones\ncGAN y R1\u2013R3 no\nforman parte de\nlas ocho redes.',
    ha='left', va='center')

rbox(0, 0.2, 100, 6.4, col=C['neutro'], tint=0.6, ec=C['linea'])
txt(50, 3.4, 'C0 y C1 tienen definición propia en cada ensayo. Las continuaciones\n'
             'parten de pesos ya entrenados; no son entrenamiento desde cero.',
    ha='center')
print(save(fig, 'met_07_secuencia_ensayos'))

"""Figure met_06_generador_critico: U-Net generator (unet_dc_5) and conditional patch critic.

Sources (repo muografia-documentada, origin/main = f1094d7ede5e95056ae59fe073a7a5570ab46e69):
  objetivo-2/implementacion/models/unet_generator.py   (UNetDoubleConv5, base=64, 'unet_dc_5')
  objetivo-2/implementacion/models/patch_critic.py     (PatchCritic n_down=3, 'patch_critic_70')
  objetivo-2/implementacion/scripts/training/losses.py (critic_score: patch-map mean per sample)
Shapes, channels and parameter counts were obtained by instantiating both models with
torch (CPU) and running a dummy forward with forward hooks, input (1,1,256,256):
  generator (build_generator('unet_dc_5')): 20 543 809 parameters, output (1,1,256,256), sigmoid
    enc1 64@256, enc2 128@128, enc3 256@64, enc4 512@32, enc5 512@16 (MaxPool2d(2) between levels)
    up4 512@32 | cat(enc4)=1024 -> dec4 512@32 ; up3 256@64 | cat -> dec3 256@64
    up2 128@128 | cat -> dec2 128@128 ; up1 64@256 | cat -> dec1 64@256 ; head Conv1x1 -> 1@256
    each block: [Conv3x3, InstanceNorm, LeakyReLU(0.2)] x 2 ; ConvTranspose2d k2 s2
  critic (build_critic('patch_critic_70')): 2 762 817 parameters, input cat(cond,img) = (1,2,256,256)
    Conv4x4 s2 64@128 (no norm) + LeakyReLU ; Conv4x4 s2 128@64 + IN + LReLU ;
    Conv4x4 s2 256@32 + IN + LReLU ; Conv4x4 s1 512@31 + IN + LReLU ; Conv4x4 s1 1@30 (no norm, no sigmoid)
    output map (1,1,30,30) -> mean over 900 patches
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
from estilo_tesis import C, TEXTWIDTH_IN, save

W, Hh = 100.0, 90.0
fig, ax = plt.subplots(figsize=(TEXTWIDTH_IN, TEXTWIDTH_IN * Hh / W))
fig.subplots_adjust(0, 0, 1, 1)
ax.set_xlim(0, W); ax.set_ylim(0, Hh); ax.axis('off')

BLUE, ORANGE, GREY = C['unet'], C['cgan'], C['entrada']
CH_CONV, CH_NORM, CH_ACT = 'white', '#DDDDDD', '#999999'
DASH = (0, (3, 2))


def rbox(x0, y0, w, h, fc='white', ec='k', lw=0.7, ls='-', z=3, r=0.5, alpha=1.0):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z, alpha=alpha))


def txt(x, y, s, fs=6.5, ha='center', va='center', z=6, **kw):
    ax.text(x, y, s, fontsize=fs, ha=ha, va=va, zorder=z, **kw)


def arrow(p0, p1, color='k', ls='-', lw=0.7, ms=5):
    ax.annotate('', xy=p1, xytext=p0, zorder=4,
                arrowprops=dict(arrowstyle='-|>', lw=lw, color=color, ls=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=ms))


def seg(xs, ys, color='k', lw=0.7, ls='-', z=4):
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle='butt')


# =========================== (a) U-Net ===========================
txt(0.3, 88.3, '(a)', fs=8, ha='left', fontweight='bold')
txt(10.5, 88.3, 'generador: U-Net de cinco niveles (\\texttt{unet\\_dc\\_5})', fs=7, ha='left')
BW, BH = 6.2, 6.4
YL = {1: 80.0, 2: 71.5, 3: 63.0, 4: 54.5, 5: 46.0}
XE = {1: 11.5, 2: 19.7, 3: 27.9, 4: 36.1, 5: 44.3}
XD = {4: 52.5, 3: 60.7, 2: 68.9, 1: 77.1}
RES = {1: 256, 2: 128, 3: 64, 4: 32, 5: 16}
CHN = {1: 64, 2: 128, 3: 256, 4: 512, 5: 512}


def unet_block(x, y, k):
    rbox(x - BW / 2, y - BH / 2, BW, BH, fc=BLUE, ec=BLUE, alpha=0.30, z=2)
    rbox(x - BW / 2, y - BH / 2, BW, BH, fc='none', ec=BLUE, lw=0.9, z=3)
    txt(x, y + 1.2, f'${RES[k]}^2$', fs=6.5)
    txt(x, y - 1.3, f'{CHN[k]}', fs=6.5, fontweight='bold')


# input
rbox(0.5, YL[1] - BH / 2, 5.0, BH, fc=GREY, ec='k')
txt(3.0, YL[1] + 1.2, '$\\boldsymbol{u}$', fs=7); txt(3.0, YL[1] - 1.3, '$256^2$', fs=6.5)
txt(3.0, YL[1] - BH / 2 - 1.6, '1 canal', fs=6.5)
arrow((5.5, YL[1]), (XE[1] - BW / 2, YL[1]))
for k in range(1, 6):
    unet_block(XE[k], YL[k], k)
for k in range(4, 0, -1):
    unet_block(XD[k], YL[k], k)
# MaxPool elbows
for k in range(1, 5):
    x, y = XE[k], YL[k]
    seg([x, x], [y - BH / 2, YL[k + 1]]); arrow((x, YL[k + 1]), (XE[k + 1] - BW / 2, YL[k + 1]))
# up-conv (leaves the block top), concat circles and skips
CR = 1.15
for k in range(4, 0, -1):
    xd = XD[k]
    cx = xd - BW / 2 - 2.1
    sx = XE[5] if k == 4 else XD[k + 1]
    sy = YL[k + 1] + BH / 2
    yh = sy + 1.0
    seg([sx, sx], [sy, yh]); seg([sx, cx], [yh, yh]); arrow((cx, yh), (cx, YL[k] - CR))
    seg([XE[k] + BW / 2, cx - CR], [YL[k], YL[k]], color=C['linea'], ls=DASH)
    ax.add_patch(Circle((cx, YL[k]), CR, fc='white', ec='k', lw=0.7, zorder=5))
    seg([cx - 0.7, cx + 0.7], [YL[k], YL[k]], lw=0.6, z=6); seg([cx, cx], [YL[k] - 0.7, YL[k] + 0.7], lw=0.6, z=6)
    arrow((cx + CR, YL[k]), (xd - BW / 2, YL[k]))
# labels for operations (once)
txt(XE[1] + 3.6, YL[2] + 3.9, 'MaxPool $2{\\times}2$', fs=6.5, ha='left', va='center')
txt(XD[4] + 3.6, YL[4] - 4.7, 'ConvT $2{\\times}2$, paso 2', fs=6.5, ha='left', va='center')
txt(XD[4] + 3.6, YL[4] - 7.4, r'concat.: 1024$\rightarrow$512, 512$\rightarrow$256,', fs=6.5, ha='left', va='center')
txt(XD[4] + 3.6, YL[4] - 9.4, r'256$\rightarrow$128, 128$\rightarrow$64 (doble bloque)', fs=6.5, ha='left', va='center')
txt(XE[1] + 15.8, YL[1] + 1.9, 'concatenación', fs=6.5, ha='center')
# head
xh = 85.9
rbox(xh - 4.3, YL[1], 8.6, BH / 2, fc=CH_CONV, ec='k')
rbox(xh - 4.3, YL[1] - BH / 2, 8.6, BH / 2, fc='black', ec='k')
txt(xh, YL[1] + BH / 4, 'Conv $1{\\times}1$', fs=6.5)
txt(xh, YL[1] - BH / 4, 'sigmoide', fs=6.5, color='white')
arrow((XD[1] + BW / 2, YL[1]), (xh - 4.3, YL[1]))
rbox(92.4, YL[1] - BH / 2, 6.8, BH, fc=GREY, ec='k')
txt(95.8, YL[1] + 1.4, '$\\hat{\\boldsymbol{y}}$', fs=7); txt(95.8, YL[1] - 1.3, '$256^2$', fs=6.5)
txt(95.8, YL[1] - BH / 2 - 1.6, '$[0,1]$', fs=6.5)
arrow((xh + 4.3, YL[1]), (92.4, YL[1]))
txt(50.0, 85.3, 'inferencia: solo el generador, de $\\boldsymbol{u}$ a $\\hat{\\boldsymbol{y}}$', fs=6.5)
# training-only branches to the critic
rbox(80.0, 56.0, 14.0, 6.0, fc='white', ec=C['linea'], ls=DASH)
txt(87.0, 59.0, 'referencia $\\boldsymbol{y}$', fs=6.5)
YTOP = 40.8
seg([99.6, 99.6], [YL[1], YTOP + 0.3], color=ORANGE, ls=DASH)
seg([99.2, 99.6], [YL[1], YL[1]], color=ORANGE, ls=DASH)
arrow((99.6, YTOP + 1.5), (99.6, YTOP - 0.2), color=ORANGE, ls=DASH, ms=4)
seg([87.0, 87.0], [56.0, YTOP + 1.5], color=ORANGE, ls=DASH); arrow((87.0, YTOP + 1.5), (87.0, YTOP - 0.2), color=ORANGE, ls=DASH, ms=4)
txt(85.5, 53.0, 'al crítico\n(solo entrenamiento)', fs=6.5, ha='right', color=ORANGE)

# =========================== (b) critic ===========================
YB = 23.0
rbox(0.3, 10.8, 99.4, 29.8, fc='none', ec=ORANGE, lw=0.9, ls=DASH, z=1, r=1.0)
txt(0.8, 38.4, '(b)', fs=8, ha='left', fontweight='bold')
txt(7.0, 38.4, 'crítico condicional de parches (\\texttt{patch\\_critic\\_70}), solo entrenamiento', fs=7, ha='left')
for yy, b in [(29.5, 'referencia $\\boldsymbol{y}$'), (16.5, 'predicción $\\hat{\\boldsymbol{y}}$')]:
    rbox(1.5, yy - 3.0, 4.2, 6.0, fc=GREY, ec='k'); txt(3.6, yy, '$\\boldsymbol{u}$', fs=7)
    rbox(5.7, yy - 3.0, 10.4, 6.0, fc='white', ec='k'); txt(10.9, yy, b, fs=6.5)
    arrow((16.1, yy), (17.6, YB + (3.0 if yy > YB else -3.0)))
txt(8.6, YB, 'una pareja\npor evaluación', fs=6.5, style='italic')
rbox(17.6, YB - 6.0, 7.6, 12.0, fc='white', ec='k')
txt(21.4, YB + 3.2, 'concat.', fs=6.5); txt(21.4, YB - 0.2, '$256^2$', fs=6.5); txt(21.4, YB - 3.4, '2 canales', fs=6.5)
layers = [('$128^2$', 64, 2, False, True), ('$64^2$', 128, 2, True, True), ('$32^2$', 256, 2, True, True),
          ('$31^2$', 512, 1, True, True), ('$30^2$', 1, 1, False, False)]
XL0, PIT, LW_ = 32.2, 10.4, 8.6
arrow((25.2, YB), (XL0 - LW_ / 2, YB))
hc, hn, ha_ = 4.4, 2.5, 2.5
for i, (dims, ch, st, norm, act) in enumerate(layers):
    xc = XL0 + i * PIT
    H_tot = hc + norm * hn + act * ha_
    ytop = YB + H_tot / 2
    y = ytop
    rbox(xc - LW_ / 2, y - hc, LW_, hc, fc=CH_CONV, ec='k', r=0.3)
    txt(xc, y - 1.2, 'Conv $4{\\times}4$', fs=6.5); txt(xc, y - 3.1, f'paso {st}', fs=6.5)
    y -= hc
    if norm:
        rbox(xc - LW_ / 2, y - hn, LW_, hn, fc=CH_NORM, ec='k', r=0.3); txt(xc, y - 1.25, 'IN', fs=6.5); y -= hn
    if act:
        rbox(xc - LW_ / 2, y - ha_, LW_, ha_, fc=CH_ACT, ec='k', r=0.3); txt(xc, y - 1.25, 'LReLU', fs=6.5, color='white'); y -= ha_
    txt(xc, ytop + 2.2, dims + '$\\times$' + f'{ch}', fs=6.5)
    if i < len(layers) - 1:
        arrow((xc + LW_ / 2, YB), (xc + PIT - LW_ / 2, YB))
txt(XL0, 13.2, 'sin IN en la primera capa', fs=6.5)
txt(XL0 + 2.2 * PIT, 13.2, 'sin IN ni sigmoide en la última', fs=6.5)
xm = XL0 + 4 * PIT + LW_ / 2
arrow((xm, YB), (xm + 3.0, YB))
xb = xm + 3.0
rbox(xb, YB - 3.5, 7.0, 7.0, fc='white', ec=ORANGE, lw=0.9)
for g in range(1, 4):
    seg([xb + g * 1.75] * 2, [YB - 3.5, YB + 3.5], color=ORANGE, lw=0.3)
    seg([xb, xb + 7.0], [YB - 3.5 + g * 1.75] * 2, color=ORANGE, lw=0.3)
txt(xb + 3.5, YB - 6.3, '$30{\\times}30$', fs=6.5); txt(xb + 3.5, YB - 8.3, 'puntuaciones', fs=6.5)
arrow((xb + 7.0, YB), (xb + 10.4, YB))
txt(xb + 9.0, YB + 6.3, 'promedio de', fs=6.5); txt(xb + 9.0, YB + 4.3, '900 parches', fs=6.5)
rbox(xb + 10.4, YB - 2.6, 99.0 - (xb + 10.4), 5.2, fc='white', ec=ORANGE, lw=0.9)
txt((xb + 10.4 + 99.0) / 2, YB, '$S_\\phi$', fs=7)
txt((xb + 10.4 + 99.0) / 2, YB - 5.4, 'entra en', fs=6.5); txt((xb + 10.4 + 99.0) / 2, YB - 7.4, '$\\mathcal{L}_D$, $\\mathcal{L}_G$', fs=6.5)

# =========================== legend ===========================
txt(0.8, 7.6, 'Leyenda:', fs=6.5, ha='left', fontweight='bold')
x = 11.0
for lab, fc, tc, w in [('Conv', CH_CONV, 'k', 6.0), ('IN (InstanceNorm)', CH_NORM, 'k', 19.0),
                       ('LeakyReLU (pendiente 0,2)', CH_ACT, 'white', 29.0), ('sigmoide', 'black', 'white', 8.0)]:
    rbox(x, 7.6 - 1.4, w, 2.8, fc=fc, ec='k', r=0.3); txt(x + w / 2, 7.6, lab, fs=6.5, color=tc)
    x += w + 1.6
txt(0.8, 4.4, 'Bloque del generador: [Conv $3{\\times}3$, IN, LReLU]$\\times2$. Generador: 20\\,543\\,809 parámetros; crítico: 2\\,762\\,817.',
    fs=6.5, ha='left')
y2 = 1.4
seg([0.8, 6.8], [y2, y2]); txt(7.8, y2, 'continuo: inferencia y entrenamiento', fs=6.5, ha='left')
seg([37.0, 43.0], [y2, y2], color=ORANGE, ls=DASH); txt(44.0, y2, 'discontinuo: solo entrenamiento', fs=6.5, ha='left')
seg([70.0, 75.0], [y2, y2], color=C['linea'], ls=DASH); txt(76.0, y2, 'conexión de salto', fs=6.5, ha='left')
ax.add_patch(Circle((93.0, y2), 1.0, fc='white', ec='k', lw=0.6, zorder=5))
seg([92.4, 93.6], [y2, y2], lw=0.5, z=6); seg([93.0, 93.0], [y2 - 0.6, y2 + 0.6], lw=0.5, z=6)
txt(94.3, y2, 'concat.', fs=6.5, ha='left')
save(fig, 'met_06_generador_critico')

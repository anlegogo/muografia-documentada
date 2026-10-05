"""Figure met_05_normalizacion: transformation T_s and recovery of equivalent counts.

Sources (repo muografia-documentada, origin/main = f1094d7ede5e95056ae59fe073a7a5570ab46e69):
  objetivo-2/implementacion/scripts/training/muography_dataset.py
      normalize_counts: log1p(c) / (log1p(c) + s);  normalize_input: normalize_counts(low / fraction, s);
      inverse_counts: expm1(s * z / (1 - z)); scale = log1p(max(1, train_max))
  objetivo-2/herramientas/datos_ajuste.py   (same transform, fit on the train split only)
  objetivo-2/evidencias/contrato-datos-v1.json
      normalization: fit_split=train, name=train_log_bounded_v1, scale=8.239329427901795, train_max=3786
Notation follows capitulos/03_metodologia.tex (L, f, C, T_s, u, y, G_theta, s, M).
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from estilo_tesis import C, TEXTWIDTH_IN, save, comma_formatter

S = 8.239329427901795
M = 3786
assert abs(np.log1p(M) - S) < 1e-12


def T(c):
    l = np.log1p(c)
    return l / (S + l)


def Tinv(z):
    return np.expm1(S * z / (1 - z))


assert abs(T(M) - 0.5) < 1e-12 and abs(Tinv(0.5) - M) < 1e-6

fig = plt.figure(figsize=(TEXTWIDTH_IN, TEXTWIDTH_IN * 0.78))
gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1.0], left=0.07, right=0.99, top=0.99, bottom=0.08,
                      hspace=0.30, wspace=0.30)

# ---------------- (a) block diagram ----------------
ax = fig.add_subplot(gs[0, :]); ax.axis('off')
ax.set_xlim(0, 100); ax.set_ylim(-4, 40)


def box(x0, x1, yc, text, ec='k', fc='white', ls='-', h=6.0, fs=7.5, lw=0.8):
    p = FancyBboxPatch((x0, yc - h / 2), x1 - x0, h, boxstyle='round,pad=0,rounding_size=0.8',
                       fc=fc, ec=ec, lw=lw, ls=ls, zorder=3)
    ax.add_patch(p)
    ax.text((x0 + x1) / 2, yc, text, ha='center', va='center', fontsize=fs, zorder=4)
    return p


def arrow(p0, p1, color='k', ls='-', lw=0.8):
    ax.annotate('', xy=p1, xytext=p0, zorder=2,
                arrowprops=dict(arrowstyle='-|>', lw=lw, color=color, ls=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=6))


def line(xs, ys, color='k', lw=0.8, ls='-'):
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=2, solid_capstyle='butt')


YI, YR, YS = 31.0, 9.0, 20.0     # input row, reference row, scale row
G, E, V = C['oe2'], C['entrada'], C['oe3']

# normalised-domain band
ax.add_patch(plt.Rectangle((27.5, -2.5), 45.0, 39.5, fc=C['neutro'], ec='none', alpha=0.45, zorder=0))
ax.text(50.0, 37.4, 'dominio normalizado $[0,1)$', ha='center', va='center', fontsize=7)
ax.text(13.0, 37.4, 'dominio de cuentas', ha='center', va='center', fontsize=7)
ax.text(86.0, 37.4, 'dominio de cuentas', ha='center', va='center', fontsize=7)

# input path
box(0.5, 9.5, YI, '$L$', ec=E, fc=E)
box(13.0, 21.0, YI, '$\\div f$', ec='k')
box(30.0, 38.0, YI, '$T_s$', ec=G, fc='white')
box(44.0, 56.0, YI, '$G_\\theta$', ec=G, fc='white')
box(66.0, 75.0, YI, '$T_s^{-1}$', ec=G, fc='white')
box(81.0, 99.5, YI, 'métricas\nregionales', ec=V, h=8.0)
arrow((9.5, YI), (13.0, YI)); arrow((21.0, YI), (30.0, YI)); arrow((38.0, YI), (44.0, YI))
ax.text(41.0, YI + 1.4, '$\\boldsymbol{u}$', ha='center', fontsize=7.5)
ax.text(24.5, YI + 1.4, '$L/f$', ha='center', fontsize=7)
arrow((56.0, YI), (66.0, YI)); ax.text(61.0, YI + 1.4, '$\\hat{\\boldsymbol{y}}$', ha='center', fontsize=7.5)
arrow((75.0, YI), (81.0, YI)); ax.text(78.0, YI + 1.4, '$\\hat{c}$', ha='center', fontsize=7.5)

# reference path
box(0.5, 9.5, YR, '$C$', ec=V, fc='white')
box(30.0, 38.0, YR, '$T_s$', ec=G, fc='white')
arrow((9.5, YR), (30.0, YR))
ax.text(19.5, YR + 1.4, 'referencia', ha='center', fontsize=7)
box(57.0, 73.0, YS - 1.5, 'SSIM, PSNR', ec=V, h=6.0)
line([38.0, 65.0], [YR, YR]); arrow((65.0, YR), (65.0, YS - 4.5))
ax.text(45.5, YR + 1.4, '$\\boldsymbol{y}$', ha='center', fontsize=7.5)
# generator output down to SSIM/PSNR
ax.plot([61.0], [YI], 'o', ms=1.8, color='k', zorder=5)
arrow((61.0, YI), (61.0, YS + 1.5))
# C to regional metrics (count domain), routed below
line([5.0, 5.0], [YR - 3.0, -1.0]); line([5.0, 90.0], [-1.0, -1.0]); arrow((90.0, -1.0), (90.0, YI - 4.0))
ax.text(47.0, -3.0, '$C$ (cuentas de referencia, sin transformar)', ha='center', va='center', fontsize=7)

# scale s: train only
box(1.0, 19.5, YS, 'referencias de\nentrenamiento', ec=G, ls=(0, (3, 2)), h=7.0, fs=7)
box(30.0, 38.0, YS, '$s$', ec=G, fc='white', h=5.0)
arrow((19.5, YS), (30.0, YS))
ax.text(24.8, YS + 1.4, '$M$', ha='center', fontsize=7)
arrow((34.0, YS + 2.5), (34.0, YI - 3.0)); arrow((34.0, YS - 2.5), (34.0, YR + 3.0))
ax.text(40.0, YS + 1.0,'$s=\\log(1+M)$', ha='left', va='center', fontsize=7)
ax.text(40.0, YS - 2.0,'solo entrenamiento', ha='left', va='center', fontsize=6.5, style='italic')
# s also feeds the inverse (dashed branch routed above the metrics box)
ax.plot([34.0], [25.5], 'o', ms=1.8, color='k', zorder=5)
line([34.0, 70.5], [25.5, 25.5], ls=(0, (3, 2)))
arrow((70.5, 25.5), (70.5, YI - 3.0))
ax.text(0.2, 38.6, '(a)', fontweight='bold', va='center', fontsize=8)

# ---------------- (b) T_s(c) ----------------
axb = fig.add_subplot(gs[1, 0])
c = np.concatenate([[0.0], np.logspace(-2, 5, 600)])
axb.plot(c, T(c), color=G, lw=1.2)
axb.set_xscale('symlog', linthresh=1.0, linscale=0.35)
axb.set_xlim(0, 1e5); axb.set_ylim(0, 1)
axb.set_xticks([0, 1, 10, 100, 1000, 10000, 100000])
axb.set_xticklabels(['0', '$10^0$', '$10^1$', '$10^2$', '$10^3$', '$10^4$', '$10^5$'])
axb.axvline(M, color='k', lw=0.6, ls=(0, (3, 2)))
axb.plot([M], [0.5], 'o', ms=3.2, color='k', zorder=5)
axb.hlines(0.5, 0, M, color='k', lw=0.6, ls=(0, (3, 2)))
axb.annotate('$M=3786$\n$T_s(M)=0{,}5$', xy=(M, 0.5), xytext=(2.0, 0.60), fontsize=7, ha='left',
             arrowprops=dict(arrowstyle='-', lw=0.5))
axb.text(2.2e4, 0.08, '$c>M$', fontsize=7, ha='center', va='bottom')
axb.axvspan(M, 1e5, color=C['neutro'], alpha=0.45, lw=0)
axb.text(1.5, 0.80, '$T_s(c)=\\dfrac{\\log(1+c)}{s+\\log(1+c)}$\n$s=8{,}2393$', fontsize=7.5, ha='left')
axb.set_xlabel('$c$ (cuentas equivalentes a la referencia)')
axb.set_ylabel('$z=T_s(c)$')
axb.yaxis.set_major_formatter(comma_formatter())
axb.text(-0.20, 1.02, '(b)', transform=axb.transAxes, fontweight='bold', va='bottom')

# ---------------- (c) inverse ----------------
axc = fig.add_subplot(gs[1, 1])
z = np.linspace(0, 0.6, 600)
axc.plot(z, Tinv(z), color=G, lw=1.2)
axc.set_yscale('symlog', linthresh=1.0, linscale=0.35)
axc.set_xlim(0, 0.6); axc.set_ylim(0, 1e5)
axc.set_yticks([0, 1, 10, 100, 1000, 10000, 100000])
axc.set_yticklabels(['0', '$10^0$', '$10^1$', '$10^2$', '$10^3$', '$10^4$', '$10^5$'])
axc.plot([0.5], [M], 'o', ms=3.2, color='k', zorder=5)
axc.hlines(M, 0, 0.5, color='k', lw=0.6, ls=(0, (3, 2)))
axc.vlines(0.5, 0, M, color='k', lw=0.6, ls=(0, (3, 2)))
axc.annotate('$z=0{,}5$,\n$T_s^{-1}(z)=M=3786$', xy=(0.5, M), xytext=(0.03, 1.3e4), fontsize=7, ha='left',
             arrowprops=dict(arrowstyle='-', lw=0.5))
axc.axhspan(M, 1e5, color=C['neutro'], alpha=0.45, lw=0)
axc.text(0.02, 150.0, '$T_s^{-1}(z)=\\exp\\!\\left(\\dfrac{sz}{1-z}\\right)-1$\n$0\\leq z<1$', fontsize=7.5, ha='left')
axc.set_xlabel('$z$ (salida del generador, dominio normalizado)')
axc.set_ylabel('$T_s^{-1}(z)$ (cuentas)')
axc.xaxis.set_major_formatter(comma_formatter())
axc.text(-0.20, 1.02, '(c)', transform=axc.transAxes, fontweight='bold', va='bottom')
save(fig, 'met_05_normalizacion')

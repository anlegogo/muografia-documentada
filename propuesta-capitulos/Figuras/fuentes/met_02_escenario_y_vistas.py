"""Figure met_02_escenario_y_vistas: idealised cone, anomalies and six views.

Sources (repo muografia-documentada, origin/main = f1094d7ede5e95056ae59fe073a7a5570ab46e69):
  objetivo-1/originales/scripts/simulation/geometry_catalog/geometries/geo-train-08.json
  objetivo-1/originales/scripts/simulation/geant4_app/include/GeometryConfig.hh
      (kDetSideM 1.2, kDetDistanceM 1000, kDetHeightM 1.5, kViewStepDeg 60)
  objetivo-1/originales/scripts/simulation/geant4_app/src/DetectorConstruction.cc
      (detector at azimuth view_index*60 deg, looking toward the axis)
  objetivo-1/FICHA_CONJUNTO_OE1.md and objetivo-1/contratos/receta-operativa-siete-actividades.json
      (nominal panel 1.2 m, computational registration plane 600 m side, plane_half_m 300)
Catalog values are transcribed below (geo-train-08, the only training geometry
with conduit + cavity + dense body).
"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, Rectangle, Polygon, FancyArrowPatch
from matplotlib import cm, colors
import matplotlib.pyplot as plt
from estilo_tesis import C, TEXTWIDTH_IN, save, apply_comma, comma_formatter

# --- geo-train-08 (catalog) ---
R, H, RHO_ROCK = 588.2, 413.4, 2.65
COND = dict(cx=37.2, cy=-23.0, r=35.4, z0=0.0, z1=320.2, rho=1.991)
CAV = dict(cx=-61.7, cy=36.3, cz=217.3, r=20.2, rho=0.468)
BODY = dict(cx=55.1, cy=32.4, cz=160.9, ax=43.2, ay=62.2, az=57.2, rho=3.256)
D_OBS, H_OBS, STEP = 1000.0, 1.5, 60.0

cmap = plt.get_cmap('Greys')
norm = colors.Normalize(vmin=0.0, vmax=3.6)
col = lambda rho: cmap(norm(rho))
NOTE_B = ('Proyección sobre $xz$ a escala real; el cono continúa hasta $\\pm r_b$.\n'
          'C: conducto, 1,991; V: cavidad, 0,468;\n'
          'E: cuerpo denso, 3,256 (g/cm$^3$).')

fig = plt.figure(figsize=(TEXTWIDTH_IN, TEXTWIDTH_IN * 0.74))
gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.0], height_ratios=[1.0, 1.1],
                      left=0.0, right=0.93, top=0.97, bottom=0.01, wspace=0.12, hspace=0.46)

# ---------- (a) schematic cone ----------
ax = fig.add_subplot(gs[0, 0]); ax.set_aspect('equal'); ax.axis('off')
ry = 0.28
t = np.linspace(0, 2 * np.pi, 200)
bx, by = np.cos(t), ry * np.sin(t)
ax.add_patch(Polygon([(-1, 0), (0, 1.2), (1, 0)], closed=True, fc=C['roca'], alpha=0.30, ec='none'))
ax.fill(bx, by, color=C['roca'], alpha=0.30, lw=0)
ax.plot(bx[100:], by[100:], color='k', lw=0.8)
ax.plot(bx[:101], by[:101], color='k', lw=0.6, ls=(0, (3, 2)))
ax.plot([-1, 0, 1], [0, 1.2, 0], color='k', lw=0.8)
o = (-1.45, -0.2)
for dx, dy, lab, off in [(0.5, 0, '$x$', (0.04, -0.07)), (0.28, 0.20, '$y$', (0.03, 0.02)), (0, 0.55, '$z$', (-0.08, 0.03))]:
    ax.add_patch(FancyArrowPatch(o, (o[0] + dx, o[1] + dy), arrowstyle='-|>', mutation_scale=6, lw=0.7, color='k'))
    ax.text(o[0] + dx + off[0], o[1] + dy + off[1], lab, ha='left', va='bottom')
ax.plot([0, 0], [0, 1.2], color='k', lw=0.5, ls=':')
ax.annotate('', xy=(-0.12, 1.2), xytext=(-0.12, 0), arrowprops=dict(arrowstyle='<->', lw=0.6, shrinkA=0, shrinkB=0))
ax.text(-0.15, 0.6, '$h$', ha='right', va='center')
ax.annotate('', xy=(1, -0.02), xytext=(0, -0.02), arrowprops=dict(arrowstyle='<->', lw=0.6, shrinkA=0, shrinkB=0))
ax.text(0.5, -0.09, '$r_b$', ha='center', va='top')
ax.text(0.40, 0.95, 'cono de roca\n$\\rho=2{,}65$ g/cm$^3$', fontsize=7, ha='left', va='center')
ax.set_xlim(-1.7, 1.55); ax.set_ylim(-0.55, 1.4)
ax.text(-1.7, 1.38, '(a)', fontweight='bold', va='top')
ax.text(1.55, -0.50, 'esquema no a escala', fontsize=7, ha='right', va='bottom', style='italic')

# ---------- (b) vertical section (projection onto xz, true scale) ----------
ax = fig.add_subplot(gs[0, 1]); ax.set_aspect('equal')
XM = 300
ax.add_patch(Polygon([(-R, 0), (0, H), (R, 0)], closed=True, fc=col(RHO_ROCK), ec='k', lw=0.8))
ax.add_patch(Rectangle((COND['cx'] - COND['r'], COND['z0']), 2 * COND['r'], COND['z1'] - COND['z0'],
                       fc=col(COND['rho']), ec='k', lw=0.7))
ax.add_patch(Ellipse((BODY['cx'], BODY['cz']), 2 * BODY['ax'], 2 * BODY['az'], fc=col(BODY['rho']), ec='white', lw=0.7))
ax.add_patch(Circle((CAV['cx'], CAV['cz']), CAV['r'], fc=col(CAV['rho']), ec='k', lw=0.7))
ax.text(COND['cx'] - COND['r'] - 8, 60, 'C', fontsize=7.5, color='white', va='center', ha='right', fontweight='bold')
ax.text(CAV['cx'] - CAV['r'] - 8, CAV['cz'], 'V', fontsize=7.5, color='white', va='center', ha='right', fontweight='bold')
ax.text(BODY['cx'] + BODY['ax'] + 8, BODY['cz'], 'E', fontsize=7.5, color='white', va='center', ha='left', fontweight='bold')
ax.axhline(0, color='k', lw=0.6)
ax.set_xlim(-XM, XM); ax.set_ylim(-25, 440)
ax.set_xlabel('$x$ (m)'); ax.set_ylabel('$z$ (m)'); apply_comma(ax)
ax.text(0.01, 0.99, '(b)', transform=ax.transAxes, fontweight='bold', va='top')
ax.text(0.5, -0.25, NOTE_B, transform=ax.transAxes, fontsize=6.5, ha='center', va='top')
cax = fig.add_axes([0.945, 0.60, 0.012, 0.34])
# vector colour bar: stacked rectangles (no raster image)
NSTEP = 90
edges = np.linspace(0.0, 3.6, NSTEP + 1)
for lo, hi in zip(edges[:-1], edges[1:]):
    cax.add_patch(Rectangle((0, lo), 1, hi - lo, fc=col(0.5 * (lo + hi)), ec=col(0.5 * (lo + hi)), lw=0.2))
cax.set_xlim(0, 1); cax.set_ylim(0, 3.6); cax.set_xticks([])
cax.yaxis.tick_right(); cax.yaxis.set_label_position('right')
cax.set_ylabel('densidad (g/cm$^3$)', fontsize=7)
cax.tick_params(labelsize=6.5, width=0.4)
cax.yaxis.set_major_formatter(comma_formatter())

# ---------- (c) plan view ----------
ax = fig.add_subplot(gs[1, 0]); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Circle((0, 0), R, fc=col(RHO_ROCK), ec='k', lw=0.8))
ax.add_patch(Circle((COND['cx'], COND['cy']), COND['r'], fc=col(COND['rho']), ec='k', lw=0.5))
ax.add_patch(Ellipse((BODY['cx'], BODY['cy']), 2 * BODY['ax'], 2 * BODY['ay'], fc=col(BODY['rho']), ec='white', lw=0.5))
ax.add_patch(Circle((CAV['cx'], CAV['cy']), CAV['r'], fc=col(CAV['rho']), ec='k', lw=0.5))
ax.add_patch(Circle((0, 0), D_OBS, fc='none', ec=C['linea'], lw=0.5, ls=(0, (2, 3))))
for k in range(6):
    a = np.deg2rad(k * STEP)
    px, py = D_OBS * np.cos(a), D_OBS * np.sin(a)
    ax.plot(px, py, 's', ms=3.6, color=C['oe1'], mec='k', mew=0.4, zorder=5)
    ax.add_patch(FancyArrowPatch((px * 0.93, py * 0.93), (px * 0.70, py * 0.70), arrowstyle='-|>',
                                 mutation_scale=5, lw=0.6, color=C['oe1']))
    ax.text(px * 1.17, py * 1.17, f'{k}', ha='center', va='center', fontsize=7.5, color=C['oe1'], fontweight='bold')
ax.plot([0, D_OBS * 0.93], [0, 0], color='k', lw=0.4, ls=':')
th = np.linspace(0, np.deg2rad(60), 40)
ax.plot(780 * np.cos(th), 780 * np.sin(th), color='k', lw=0.5)
ax.text(830 * np.cos(np.deg2rad(30)), 830 * np.sin(np.deg2rad(30)), r'$60^{\circ}$', fontsize=7, ha='left', va='center')
ax.text(0, -1420, 'observadores a $1000$ m del eje, altura $1{,}5$ m', fontsize=7, ha='center', va='top')
ax.text(-1450, 1400, '(c)', fontweight='bold', va='top')
ax.set_xlim(-1450, 1450); ax.set_ylim(-1650, 1450)

# ---------- detail: nominal panel vs computational registration plane ----------
ax = fig.add_subplot(gs[1, 1]); ax.set_aspect('equal'); ax.axis('off')
S = 1.0
ax.add_patch(Rectangle((-S, -S), 2 * S, 2 * S, fc='white', ec=C['oe1'], lw=0.9, ls=(0, (4, 2))))
ax.add_patch(Rectangle((-0.06, -0.06), 0.12, 0.12, fc=C['oe1'], ec='k', lw=0.5))
ax.annotate('', xy=(S, -S - 0.12), xytext=(-S, -S - 0.12), arrowprops=dict(arrowstyle='<->', lw=0.6, shrinkA=0, shrinkB=0))
ax.text(0, -S - 0.2, 'plano computacional de registro,\n$600$ m de lado', ha='center', va='top', fontsize=7)
ax.annotate('panel nominal\n($1{,}2$ m)', xy=(0.07, 0.07), xytext=(0.30, 0.35), fontsize=7, ha='left', va='bottom',
            arrowprops=dict(arrowstyle='-', lw=0.5))
ax.text(0, S + 0.1, 'detalle de una observación', ha='center', va='bottom', fontsize=7)
ax.text(S, -S - 0.75, 'esquema no a escala', fontsize=7, ha='right', va='top', style='italic')
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-2.0, 1.4)
save(fig, 'met_02_escenario_y_vistas')

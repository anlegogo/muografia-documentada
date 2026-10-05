"""met_08_regiones_evaluacion: geometric regions and controls for counts and contrast.

geo-train-08, view 0. Selection rule (neutral, fixed before looking at any
model result): geo-train-08 is the only training geometry that contains the
three anomaly kinds (conduit, cavity, dense body); view 0 is the first view.
No prediction is used anywhere: masks come only from the geometry JSON and
the director's evaluator code (rays, masks, match_controls), called exactly as
in objetivo-2/herramientas/evaluar_ajuste.py with protocolo-regiones-v1.json.

Inputs and SHA-256 (file bytes):
  datos-oe1-campana-114/imagenes/geo-train-08_view0.npz (coordinates only)
    59cdd0f318becf06067997e81067c0a0c11e6bfb8d41bb85b128bd8b27db2137
  _codigo_director/geom/geo-train-08.json
    (git show origin/main:objetivo-1/originales/scripts/simulation/
     geometry_catalog/geometries/geo-train-08.json)
    df859ca1ead6e4fca4cad0d877131167a47a4d6443ebed1ee3379189600f7601
  _codigo_director/evaluar_regiones_geometricas.py (origin/main)
    e9d36af400da34338dd27fb2c6325797ad9e5f65ed724d04bd9d22369e994524
  _codigo_director/protocolo-regiones-v1.json (origin/main)
    af543992beb301ed13f9c7b030fc32619ad8a0da20f25c760b07ddabeffd6577
Director code commit: origin/main f1094d7ede5e95056ae59fe073a7a5570ab46e69.
Data source commit: f395570 (muografia-documentada), campaign 114.

The anomaly pixel is the matched pixel of the dense body closest to the
centroid of that region (deterministic rule); its five controls are exactly
the donors returned by match_controls.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import ListedColormap

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / '_codigo_director'))
from estilo_tesis import C, apply_comma, plt  # noqa: E402
from guardar_vector import save_native  # noqa: E402
from evaluar_regiones_geometricas import match_controls, masks, morphology, rays  # noqa: E402

DIR = HERE / '_codigo_director'
GID, VIEW = 'geo-train-08', 0
assert GID.startswith('geo-train')
EXPECT = {
    DIR / 'geom/geo-train-08.json': 'df859ca1ead6e4fca4cad0d877131167a47a4d6443ebed1ee3379189600f7601',
    DIR / 'evaluar_regiones_geometricas.py': 'e9d36af400da34338dd27fb2c6325797ad9e5f65ed724d04bd9d22369e994524',
    DIR / 'protocolo-regiones-v1.json': 'af543992beb301ed13f9c7b030fc32619ad8a0da20f25c760b07ddabeffd6577',
}
for p, h in EXPECT.items():
    assert hashlib.sha256(p.read_bytes()).hexdigest() == h, p
cfg = json.loads((DIR / 'protocolo-regiones-v1.json').read_text(encoding='utf-8'))
g = json.loads((DIR / 'geom/geo-train-08.json').read_text(encoding='utf-8'))
NPZ = Path(os.environ.get('DATOS_OE1', r'C:/Users/etherion/Documents/tesis-ing-sistemas/datos-oe1-campana-114')) / 'imagenes/geo-train-08_view0.npz'
assert hashlib.sha256(NPZ.read_bytes()).hexdigest() == '59cdd0f318becf06067997e81067c0a0c11e6bfb8d41bb85b128bd8b27db2137'
z = np.load(NPZ)
azE, elE, azC, elC = z['az_edges_deg'], z['el_edges_deg'], z['az_centers_deg'], z['el_centers_deg']

# --- evaluator calls, exactly as evaluar_ajuste.py ---
o, d = rays(azC, elC, VIEW, cfg)
L, aa, reg = masks(g, o, d, cfg)
cone = L > 0
names = list(reg)
kinds = {k: k.split('_', 2)[2] for k in names if k.startswith('anomalia')}
KIND_ES = {'conduit': 'conducto', 'cavity': 'cavidad', 'dense_body': 'cuerpo denso'}
res = {}
for i, an in enumerate(g['anomalies']):
    key = f"anomalia_{i}_{an['kind']}"
    m = reg[key].copy()
    for j, ll in enumerate(aa):
        if i != j:
            m &= ~morphology(ll > 0, cfg['rock_sky_margin_pixels'], False)
    t, donors = match_controls(m, reg['roca_sin_anomalia'], L, cfg)
    cov = len(t) / int(m.sum()) if m.any() else 0.0
    ok = len(t) >= cfg['min_matched_pixels'] and cov >= cfg['min_match_fraction']
    res[key] = dict(mask=m, t=t, donors=donors, n_region=int(reg[key].sum()), n_cand=int(m.sum()),
                    n_match=len(t), frac=cov, ok=ok)
anom_keys = [k for k in names if k.startswith('anomalia')]
overlap_an = np.sum([reg[k] for k in anom_keys], axis=0) > 1
overlap_edge = reg['borde_cono'] & np.logical_or.reduce([reg[k] for k in anom_keys])

# --- chosen pixel: matched dense-body pixel closest to the region centroid ---
dk = [k for k in anom_keys if k.endswith('dense_body')][0]
r = res[dk]
ys, xs = np.where(reg[dk])
cy, cx = ys.mean(), xs.mean()
ty, tx = np.divmod(r['t'], 256)
idx = int(np.argmin((ty - cy) ** 2 + (tx - cx) ** 2))
py, px = int(ty[idx]), int(tx[idx])
dy_, dx_ = np.divmod(r['donors'][idx], 256)
assert np.all(dy_ == py) and len(dx_) == cfg['control_donors_per_pixel']
Lp, Ld = L[py, px], L[py, dx_]
assert np.all(np.abs(Ld - Lp) / Lp <= cfg['control_cone_length_relative_tolerance'])
assert all(reg['roca_sin_anomalia'][py, k] for k in dx_)

# ------------------------------------------------------------------ figure
W, H = 15.0, 8.9
fig = plt.figure(figsize=(W / 2.54, H / 2.54))


def ax_cm(x, y, w, h):
    return fig.add_axes([x / W, y / H, w / W, h / H])


PW, PH = 3.7, 2.9
xs0 = [0.95, 5.55, 10.15]
ys0 = [5.4, 1.5]


WX, WY = (-9.0, 12.0), (2.0, 17.0)   # magnified window shared by panels (d) and (e)


def setup(ax, tag, row, colj, zoom=False):
    ax.set_xlim(*(WX if zoom else (-30, 30)))
    ax.set_ylim(*(WY if zoom else (elE[0], elE[-1])))
    ax.set_xticks([-5, 0, 5] if zoom else [-20, 0, 20])
    ax.set_yticks([2, 10, 17] if zoom else [2, 25, 47])
    apply_comma(ax)
    if row == 1:
        ax.set_xlabel('acimut relativo (°)', labelpad=1)
    else:
        ax.tick_params(labelbottom=False)
    if colj == 0:
        ax.set_ylabel('elevación (°)', labelpad=1)
    else:
        ax.tick_params(labelleft=False)
    ax.text(0.03, 0.96, tag, transform=ax.transAxes, va='top', ha='left', fontsize=7.5,
            bbox=dict(fc='white', ec='none', pad=1.2, alpha=0.9))
    ax.contour(azC, elC, cone.astype(float), levels=[0.5], colors=[C['linea']], linewidths=0.4)


def fill(ax, mask, color, **kw):
    ax.pcolormesh(azE, elE, np.ma.masked_where(~mask, mask.astype(float)), cmap=ListedColormap([color]),
                  vmin=0, vmax=1, rasterized=False, linewidth=0, antialiased=False, **kw)


def hatch(ax, mask, color):
    """Hatched overlay (pixels belonging to more than one region), vector contour fill."""
    if mask.any():
        ax.contourf(azC, elC, mask.astype(float), levels=[0.5, 1.5], colors='none', hatches=['//////'])


def pale(hexcolor, k=0.55):
    """Opaque tint of a palette colour (blend with white), avoids alpha seams between cells."""
    rgb = np.array([int(hexcolor[i:i + 2], 16) for i in (1, 3, 5)]) / 255
    return tuple(1 - k * (1 - rgb))


npx = lambda m: int(m.sum())  # noqa: E731
panels = [
    ('(a) cielo', 'cielo', reg['cielo']),
    ('(b) roca sin anomalías', 'roca', reg['roca_sin_anomalia']),
    ('(c) borde del cono', 'borde', reg['borde_cono']),
]
for k, (tag, c, m) in enumerate(panels):
    a = ax_cm(xs0[k], ys0[0], PW, PH)
    setup(a, tag, 0, k)
    fill(a, m, C[c])
    if c == 'borde':
        hatch(a, overlap_edge, C['borde'])

# (d) anomalies
ad = ax_cm(xs0[0], ys0[1], PW, PH)
setup(ad, '(d) anomalías', 1, 0, zoom=True)
fill(ad, np.logical_or.reduce([reg[k] for k in anom_keys]), C['anomalia'])
hatch(ad, overlap_an, C['anomalia'])
styles = {'conduit': '-', 'cavity': ':', 'dense_body': '--'}
for k in anom_keys:
    ad.contour(azC, elC, reg[k].astype(float), levels=[0.5], colors=['#222222'], linewidths=0.6,
               linestyles=styles[kinds[k]])
lab_xy = {'conduit': (11.8, 13.2), 'dense_body': (-8.8, 14.0), 'cavity': (-8.8, 4.2)}
for k in anom_keys:
    yy, xx = np.where(reg[k])
    kd = kinds[k]
    ad.annotate(KIND_ES[kd] + (f' ({len(yy)} px)' if kd == 'cavity' else ''),
                xy=(azC[int(xx.mean())], elC[int(yy.mean())]), xytext=lab_xy[kd], fontsize=6.3,
                ha='right' if kd == 'conduit' else 'left', va='center', arrowprops=dict(arrowstyle='-', lw=0.4, color='#222222'),
                bbox=dict(fc='white', ec='none', pad=0.8))

# (e) pixel and controls
ae = ax_cm(xs0[1], ys0[1], PW, PH)
setup(ae, '(e) píxel y controles', 1, 1, zoom=True)
fill(ae, reg['roca_sin_anomalia'], pale(C['roca']))
fill(ae, reg[dk], pale(C['anomalia']))
ae.plot(WX, [elC[py]] * 2, color='#222222', lw=0.4, ls=(0, (2, 2)))
ae.plot(azC[dx_], elC[dy_], 's', ms=3.4, mfc=C['control'], mec='#222222', mew=0.4, ls='none')
ae.plot([azC[px]], [elC[py]], 'o', ms=4.6, mfc=C['anomalia'], mec='#222222', mew=0.7, ls='none')
ae.annotate('píxel de\nanomalía', xy=(azC[px], elC[py]), xytext=(azC[px] - 1.0, elC[py] - 3.0), fontsize=6.3,
            ha='center', va='top', linespacing=1.0, arrowprops=dict(arrowstyle='-', lw=0.4, color='#222222'),
            bbox=dict(fc='white', ec='none', pad=0.6))
ae.annotate('5 controles', xy=(azC[dx_].mean(), elC[py]), xytext=(azC[dx_].mean() + 3.5, elC[py] + 3.0), fontsize=6.3,
            ha='center', va='bottom', arrowprops=dict(arrowstyle='-', lw=0.4, color='#222222'),
            bbox=dict(fc='white', ec='none', pad=0.6))

# (f) criterion text
af = ax_cm(xs0[2] + 0.1, ys0[1] - 0.45, 4.7, PH + 0.45)
af.axis('off')
lines = [
    ('(f) región no estimable', 7.5),
    (r'Un contraste es no estimable si:', 6.6),
    (r'$\bullet$ píxeles emparejados $<' + str(cfg['min_matched_pixels']) + r'$, o', 6.6),
    (r'$\bullet$ fracción emparejada $<' + str(cfg['min_match_fraction']).replace('.', '{,}') + r'$.', 6.6),
    (r'Emparejado: ' + str(cfg['control_donors_per_pixel']) + r' controles de roca a igual', 6.2),
    (r'elevación y $|\Delta L|/L\leq ' + str(int(cfg['control_cone_length_relative_tolerance'] * 100)) + r'\,\%$,', 6.2),
    (r'con $L$ la longitud de trayecto en el cono.', 6.2),
]
yy = 1.0
ys_ = []
for s, fs in lines:
    af.text(0.0, yy, s, fontsize=fs, va='top', ha='left', transform=af.transAxes)
    yy -= 0.1 if fs > 7 else 0.083
yy -= 0.015
af.text(0.0, yy, 'Resultados en esta vista:', fontsize=6.6, va='top', ha='left', transform=af.transAxes)
yy -= 0.1
for k in anom_keys:
    q = res[k]
    kd = KIND_ES[kinds[k]]
    tag = 'estimable' if q['ok'] else 'no estimable'
    frac = f"{q['frac']:.3f}".replace('.', '{,}')
    af.text(0.0, yy, rf'{kd}: ${q["n_match"]}/{q["n_cand"]}$ (${frac}$), {tag}', fontsize=6.2, va='top', ha='left',
            transform=af.transAxes)
    yy -= 0.083

out_fig = fig
# legend strip (colours and marks) under the top row
note = (r'Marcas: $\bullet$ píxel de anomalía (cuerpo denso, $L=' + f'{Lp:.1f}'.replace('.', '{,}') + r'$ m); '
        '\n' r'\rule{1.1ex}{1.1ex} cinco controles ($L=' + '$ a $'.join([f'{Ld.min():.1f}'.replace('.', '{,}'),
                                                               f'{Ld.max():.1f}'.replace('.', '{,}')]) +
        r'$ m). Rayado: píxeles en más de una región; contorno gris: cono. (d) y (e) ampliados.')
fig.text(0.95 / W, 0.35 / H, note, fontsize=6.3, ha='left', va='center', linespacing=1.15)

out = save_native(out_fig, 'met_08_regiones_evaluacion')
print(out, out.stat().st_size)
print('pixel', py, px, azC[px], elC[py], Lp, Ld, 'overlaps', int(overlap_an.sum()), int(overlap_edge.sum()))
for k, q in res.items():
    print(k, q['n_region'], q['n_cand'], q['n_match'], q['frac'], q['ok'])

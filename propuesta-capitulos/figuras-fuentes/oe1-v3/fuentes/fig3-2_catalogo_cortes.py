"""Figura 3.2 — Cortes verticales de densidad de los 19 escenarios del catálogo.

Entrada: archivos JSON del catálogo (datos/geometrias/), copiados sin cambios del
repositorio del proyecto, y el campo de densidad del motor analítico
(geometria_analitica.py, copia literal de simulation/surrogate/geometry.py):
roca del cono, anomalías recortadas al edificio y, en regiones compartidas, la
densidad de la última anomalía declarada. El corte de cada geometría pasa por el
plano y que atraviesa su primera anomalía (y = 0 en la geometría de control).

Salida: pdf/fig3-2_catalogo_cortes.pdf (vectorial; el campo de densidad se
incrusta a la resolución de la malla de evaluación, sin interpolación).
Uso: python fig3-2_catalogo_cortes.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import cmcrameri.cm as cmc

from estilo_tesis import CM, ANCHO_TEXTO_CM, aplicar_estilo, formato_coma
from geometria_analitica import VolcanoGeometry

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

AQUI = Path(__file__).resolve().parent
GEO_DIR = AQUI.parent / "datos" / "geometrias"
SALIDA = AQUI.parent / "pdf" / "fig3-2_catalogo_cortes.pdf"

ORDEN = [f"geo-train-{i:02d}" for i in range(1, 13)] + \
        [f"geo-val-{i:02d}" for i in range(1, 4)] + \
        [f"geo-test-{i:02d}" for i in range(1, 4)] + ["geo-gen-01"]
ROL = {"train": "entrenamiento", "val": "validación", "test": "prueba", "gen": "generalización"}

X_MAX = 720.0      # m, semiancho común de todos los paneles
Z_MAX = 470.0      # m
PASO = 1.5         # m, resolución de la malla de evaluación
RHO_MAX = 3.3      # g/cm^3


def plano_corte(geo: VolcanoGeometry) -> float:
    return float(geo.anomalies[0].params.get("cy_m", 0.0)) if geo.anomalies else 0.0


def corte(geo: VolcanoGeometry):
    x = np.arange(-X_MAX, X_MAX + PASO, PASO)
    z = np.arange(0.0, Z_MAX + PASO, PASO)
    xx, zz = np.meshgrid(x, z)
    y0 = plano_corte(geo)
    rho = geo.density(xx, np.full_like(xx, y0), zz)
    # Radio del cono en el plano y = y0 (sección hiperbólica si y0 != 0)
    r = np.sqrt(xx**2 + y0**2)
    dentro = zz <= geo.height_m * np.clip(1.0 - r / geo.base_radius_m, 0.0, None)
    rho = np.ma.masked_where(~dentro, rho)          # el aire queda en blanco
    return x, z, rho, y0


def contorno_cono(geo: VolcanoGeometry, y0: float):
    """Silueta del cono en el plano y = y0 (vectorial)."""
    R, H = geo.base_radius_m, geo.height_m
    xm = np.sqrt(max(R**2 - y0**2, 0.0))
    xs = np.linspace(-xm, xm, 400)
    zs = H * np.clip(1.0 - np.sqrt(xs**2 + y0**2) / R, 0.0, None)
    return xs, zs


def main() -> None:
    aplicar_estilo()
    ncol, nfil = 3, 7
    fig, ejes = plt.subplots(nfil, ncol, figsize=(ANCHO_TEXTO_CM * CM, 16.2 * CM),
                             sharex=True, sharey=True,
                             gridspec_kw={"hspace": 0.62, "wspace": 0.10})
    norma = Normalize(vmin=0.0, vmax=RHO_MAX)
    cmap = cmc.batlow.copy()
    cmap.set_bad("white")

    for k, gid in enumerate(ORDEN):
        ax = ejes.flat[k]
        geo = VolcanoGeometry.from_json(GEO_DIR / f"{gid}.json")
        x, z, rho, y0 = corte(geo)
        im = ax.imshow(rho, origin="lower", extent=(x[0], x[-1], z[0], z[-1]),
                       cmap=cmap, norm=norma, interpolation="none", aspect="equal")
        xs, zs = contorno_cono(geo, y0)
        ax.plot(xs, zs, color="black", lw=0.45)
        ax.axhline(0.0, color="black", lw=0.45)
        rol = ROL[gid.split("-")[1]]
        ax.set_title(rf"\texttt{{{gid}}} \,\textcolor{{black!60}}{{\scriptsize ({rol})}}", pad=2.5)
        ax.set_xlim(-X_MAX, X_MAX)
        ax.set_ylim(0.0, Z_MAX)
        ax.set_xticks([-600, -300, 0, 300, 600])
        ax.set_yticks([0, 200, 400])
        ax.xaxis.set_major_formatter(formato_coma())
        ax.yaxis.set_major_formatter(formato_coma())
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)

    # Etiquetas de ejes solo en los bordes exteriores
    for ax in ejes[:, 0]:
        ax.set_ylabel(r"$z$ (m)")
    for ax in ejes[-1, :]:
        ax.set_xlabel(r"$x$ (m)")
    ejes[-2, 1].tick_params(labelbottom=True)
    ejes[-2, 2].tick_params(labelbottom=True)
    ejes[-2, 1].set_xlabel(r"$x$ (m)")
    ejes[-2, 2].set_xlabel(r"$x$ (m)")

    # Los dos espacios restantes alojan la barra de color
    for ax in ejes.flat[len(ORDEN):]:
        ax.set_visible(False)
    pos1, pos2 = ejes[-1, 1].get_position(), ejes[-1, 2].get_position()
    cax = fig.add_axes([pos1.x0 + 0.02, pos1.y0 + 0.45 * pos1.height,
                        (pos2.x1 - pos1.x0) - 0.04, 0.22 * pos1.height])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_ticks([0.0, 1.0, 2.0, 2.65, 3.3])
    cb.ax.xaxis.set_major_formatter(formato_coma())
    cb.set_label(r"Densidad (g\,cm$^{-3}$); aire en blanco")
    cb.outline.set_linewidth(0.4)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA, backend="pgf")
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()

"""Shared physics, grids and loaders for the OE1 physical-justification delivery.

Every number used by the analysis scripts is computed here from the versioned
inputs (historical source code in ``objetivo-1/originales`` and SC3 artifacts
copied into ``datos/``). Only NumPy and the standard library are required.

Physics models (explicit assumptions, documented in the README):
- Sea-level differential flux: Guan et al. (2015), modified Gaisser with the
  Chirkin cos(theta*) correction. Identical formula to
  ``originales/scripts/simulation/surrogate/flux_model.py``.
- Muon stopping power in dry air: Bethe formula with the Sternheimer density
  effect (PDG parameters for air). Radiative losses neglected (< 1 % below
  100 GeV in air).
- Multiple scattering: differential Highland form, Gaussian core only.
- Decay in flight: c*tau = 658.638 m.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np

ENTREGA = Path(__file__).resolve().parents[1]
RAIZ_REPO = ENTREGA.parents[2]
ORIGINALES = RAIZ_REPO / "objetivo-1" / "originales" / "scripts"
TABLAS = ORIGINALES / "simulation" / "geant4_app" / "tables"
GEOMETRIAS = ORIGINALES / "simulation" / "geometry_catalog" / "geometries"
DATOS_SC3 = ENTREGA / "datos" / "sc3"
RESULTADOS = ENTREGA / "resultados"
FIGURAS = ENTREGA / "figuras"

# --- Constants (PDG 2024 unless stated otherwise)
M_MU = 0.1056583755          # GeV
C_TAU_MU_M = 658.638         # m
K_BETHE = 0.307075e-3        # GeV cm^2/mol
M_E = 0.51099895e-3          # GeV
AIR_ZA = 0.49919
AIR_I_GEV = 85.7e-9
AIR_X0_G_CM2 = 36.62
RHO_G4_AIR = 1.20479e-3      # g/cm^3, G4_AIR (NIST) used by Geant4
RHO_SURROGATE_AIR = 1.225e-3  # g/cm^3, surrogate geometry.AIR_DENSITY
# Sternheimer density-effect parameters for dry air (PDG atomic tables)
AIR_DENS = dict(cbar=10.5961, x0=1.7418, x1=4.2759, a=0.10914, k=3.3994)

# --- Detector and grid constants (originales/.../GeometryConfig.hh)
DET_SIDE_M = 1.2
DET_AREA_CM2 = 1.44e4
DET_DISTANCE_M = 1000.0
DET_HEIGHT_M = 1.5
AZ_HALF_DEG = 30.0
EL_MIN_DEG, EL_MAX_DEG = 2.0, 47.0
N_AZ = N_EL = 256
S0_HISTORICO = 36175379.91628132   # tables/meta.json
S0_V1 = 36034069.911914065         # correcciones/malla-angular-v1/README.md


# ------------------------------------------------------------------ utilities
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ruta_relativa(path: Path) -> str:
    return Path(path).resolve().relative_to(RAIZ_REPO).as_posix()


def escribir_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    def numpy_a_python(o):
        if isinstance(o, np.generic):
            return o.item()
        raise TypeError(type(o).__name__)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False, default=numpy_a_python) + "\n",
                    encoding="utf-8")


def entorno() -> dict:
    import platform
    import matplotlib
    return {"python": platform.python_version(), "numpy": np.__version__,
            "matplotlib": matplotlib.__version__}


def binomial_sigma(k: float, n: float) -> float:
    p = k / n
    return math.sqrt(p * (1.0 - p) / n)


# ---------------------------------------------------------------------- grids
def centros_elevacion_deg() -> np.ndarray:
    """Historical elevation centers (kept by az-edges-v1)."""
    return np.linspace(EL_MIN_DEG, EL_MAX_DEG, N_EL)


def centros_azimut_historicos_deg() -> np.ndarray:
    return np.linspace(-AZ_HALF_DEG, AZ_HALF_DEG, N_AZ)


def bordes_azimut_v1_deg() -> np.ndarray:
    return np.linspace(-AZ_HALF_DEG, AZ_HALF_DEG, N_AZ + 1)


def fraccion_columna_historica() -> np.ndarray:
    """Fraction of a uniform +-30 deg azimuth sample landing in each old column.

    Old scorer: idx = round((az + 30) / (60/255)); edge columns are half-wide.
    """
    f = np.full(N_AZ, 1.0 / (N_AZ - 1))
    f[0] = f[-1] = 0.5 / (N_AZ - 1)
    return f


def leer_pesos_fila() -> tuple[np.ndarray, np.ndarray]:
    el, w = np.loadtxt(TABLAS / "row_weights_30d.txt", unpack=True)
    return el, w


def leer_p_cdf() -> tuple[np.ndarray, np.ndarray]:
    edges = None
    filas = []
    for line in (TABLAS / "p_cdf.txt").read_text().splitlines():
        if line.startswith("# band_edges_deg:"):
            edges = np.array([float(v) for v in line.split(":")[1].split()])
        elif line and not line.startswith("#"):
            filas.append([float(v) for v in line.split()])
    return edges, np.array(filas)


def muestras_momento(cdf: np.ndarray, sub: int = 8) -> np.ndarray:
    """Equal-probability momenta reproducing FluxTables::SampleMomentum.

    The generator draws u ~ U(0,1) and interpolates linearly between the 257
    quantiles, so each segment carries probability 1/256 with p uniform inside.
    """
    t = (np.arange(sub) + 0.5) / sub
    return (cdf[:-1, None] + t[None, :] * (cdf[1:] - cdf[:-1])[:, None]).ravel()


def leer_histograma(path: Path) -> np.ndarray:
    """Geant4 histogram CSV: row = elevation index, column = azimuth index."""
    return np.loadtxt(path, delimiter=",", dtype=np.int64)


def leer_geometria(geometry_id: str) -> dict:
    return json.loads((GEOMETRIAS / f"{geometry_id}.json").read_text(encoding="utf-8"))


def leer_metas_campana() -> list[dict]:
    metas = []
    for p in sorted((DATOS_SC3 / "campaign-merged-meta").glob("*.meta.json")):
        metas.append(json.loads(p.read_text(encoding="utf-8")))
    return metas


def leer_sacct(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="|"))


# ------------------------------------------------------------------ Guan flux
def cos_theta_star(c: np.ndarray) -> np.ndarray:
    p1, p2, p3, p4, p5 = 0.102573, -0.068287, 0.958633, 0.0407253, 0.817285
    num = c**2 + p1**2 + p2 * c**p3 + p4 * c**p5
    den = 1.0 + p1**2 + p2 + p4
    return np.sqrt(num / den)


def guan_diff(e_gev: np.ndarray, cos_theta: np.ndarray) -> np.ndarray:
    """Guan et al. (2015) differential flux [cm^-2 s^-1 sr^-1 GeV^-1]."""
    cs = cos_theta_star(np.asarray(cos_theta, dtype=float))
    e = np.asarray(e_gev, dtype=float)
    e_eff = e * (1.0 + 3.64 / (e * cs**1.29))
    term = 1.0 / (1.0 + 1.1 * e * cs / 115.0) + 0.054 / (1.0 + 1.1 * e * cs / 850.0)
    return 0.14 * e_eff**-2.7 * term


def guan_integral(e_min: float, cos_theta: np.ndarray, n: int = 6000,
                  e_max: float = 2.0e5) -> np.ndarray:
    """Integral flux above e_min [cm^-2 s^-1 sr^-1], log-grid trapezoid."""
    e = np.logspace(math.log10(e_min), math.log10(e_max), n)
    phi = guan_diff(e[None, :], np.atleast_1d(cos_theta)[:, None])
    return np.trapezoid(phi, e, axis=1)


# ------------------------------------------------------- air energy loss (CSDA)
def dedx_aire(t_gev: np.ndarray) -> np.ndarray:
    """Mean stopping power of muons in dry air [GeV cm^2/g] (Bethe + delta)."""
    t = np.asarray(t_gev, dtype=float)
    e = t + M_MU
    gamma = e / M_MU
    beta2 = 1.0 - 1.0 / gamma**2
    bg = np.sqrt(gamma**2 - 1.0)
    tmax = 2 * M_E * bg**2 / (1 + 2 * gamma * M_E / M_MU + (M_E / M_MU) ** 2)
    x = np.log10(bg)
    d = AIR_DENS
    delta = np.where(x >= d["x1"], 2 * math.log(10) * x - d["cbar"],
                     np.where(x >= d["x0"],
                              2 * math.log(10) * x - d["cbar"]
                              + d["a"] * np.clip(d["x1"] - x, 0.0, None) ** d["k"],
                              0.0))
    arg = 2 * M_E * bg**2 * tmax / AIR_I_GEV**2
    return K_BETHE * AIR_ZA / beta2 * (0.5 * np.log(arg) - beta2 - delta / 2)


class TablaRangoAire:
    """CSDA range R(T) in g/cm^2 and its inverse, from dedx_aire."""

    def __init__(self, t_min: float = 1e-3, t_max: float = 1e4, n: int = 20000):
        self.t = np.logspace(math.log10(t_min), math.log10(t_max), n)
        inv = 1.0 / dedx_aire(self.t)
        r = np.concatenate([[0.0], np.cumsum(0.5 * (inv[1:] + inv[:-1]) * np.diff(self.t))])
        self.r = r + self.t[0] / dedx_aire(self.t[0])  # linear start below t_min

    def rango(self, t_gev):
        return np.interp(t_gev, self.t, self.r)

    def energia(self, r_g_cm2):
        return np.interp(r_g_cm2, self.r, self.t, left=0.0)


def transporte_aire(p0_gev: np.ndarray, columna_g_cm2: float, rho_g_cm3: float,
                    tabla: TablaRangoAire, n_pasos: int = 400) -> dict:
    """Continuous transport of muons with initial momenta p0 through air.

    Returns survival against range-out, decay survival probability and the
    Gaussian (Highland, differential form) projected lateral displacement rms
    at the end of the path. Muons that range out have zero decay survival.
    """
    p0 = np.asarray(p0_gev, dtype=float)
    t0 = np.sqrt(p0**2 + M_MU**2) - M_MU
    r0 = tabla.rango(t0)
    sobrevive_rango = r0 > columna_g_cm2
    longitud_cm = columna_g_cm2 / rho_g_cm3
    x0_cm = AIR_X0_G_CM2 / rho_g_cm3
    s = (np.arange(n_pasos) + 0.5) / n_pasos * longitud_cm  # midpoints
    ds = longitud_cm / n_pasos
    restante = r0[:, None] - (s[None, :] * rho_g_cm3)
    t = tabla.energia(np.maximum(restante, 0.0))
    t = np.where(restante > 0, t, np.nan)
    e = t + M_MU
    p = np.sqrt(np.maximum(e**2 - M_MU**2, 1e-30))
    beta = p / e
    # decay: dN/N = -ds * m / (p c tau)
    tasa = M_MU / (p * C_TAU_MU_M * 100.0)
    log_surv = -np.nansum(tasa * ds, axis=1)
    p_decay = np.where(sobrevive_rango, np.exp(log_surv), 0.0)
    # Highland differential form with the total-thickness log correction
    corr = (1.0 + 0.038 * math.log(longitud_cm / x0_cm)) ** 2
    dtheta2 = (0.0136 / (beta * p)) ** 2 / x0_cm * corr
    sigma_y2 = np.nansum((longitud_cm - s[None, :]) ** 2 * dtheta2 * ds, axis=1)
    t_final = np.where(sobrevive_rango, tabla.energia(np.maximum(r0 - columna_g_cm2, 0.0)), 0.0)
    return {"sobrevive_rango": sobrevive_rango, "p_decay": p_decay,
            "sigma_y_m": np.sqrt(sigma_y2) / 100.0, "t_final": t_final}


def contencion_cuadrado(sigma_y_m: np.ndarray, sigma_z_m: np.ndarray, half_m: float,
                        panel_half_m: float = DET_SIDE_M / 2) -> np.ndarray:
    """P(final point inside a square of half-side h | nominal impact uniform on panel).

    1-D factor: (1/2a) int_{-a}^{a} [Phi((h-x)/s) - Phi((-h-x)/s)] dx, evaluated
    in closed form with G(u) = u*Phi(u) + phi(u).
    """
    def g(u):
        return u * 0.5 * (1 + _erf(u / math.sqrt(2))) + np.exp(-0.5 * u**2) / math.sqrt(2 * math.pi)

    def factor(sig):
        sig = np.maximum(np.asarray(sig, dtype=float), 1e-9)
        a = panel_half_m
        h = half_m
        val = (g((h + a) / sig) - g((h - a) / sig) - g((-h + a) / sig) + g((-h - a) / sig))
        return np.clip(sig * val / (2 * a), 0.0, 1.0)

    return factor(sigma_y_m) * factor(sigma_z_m)


def _erf(x):
    return np.vectorize(math.erf, otypes=[float])(np.asarray(x, dtype=float))


# ------------------------------------------------- surrogate expectation map
CSDA_A, CSDA_B = 2.17e-3, 4.0e-6           # standard rock, surrogate flux_model
X_AIRE_SURROGATE = 3000.0 * 100.0 * RHO_SURROGATE_AIR   # 367.5 g/cm^2


def e_min_csda(x_g_cm2):
    return (CSDA_A / CSDA_B) * np.expm1(CSDA_B * np.asarray(x_g_cm2, dtype=float))


def angulo_solido_historico(el_deg: np.ndarray) -> np.ndarray:
    """Surrogate per-bin solid angle (sr): spacing 60/255 x 45/255 deg x cos(el)."""
    return (math.radians(2 * AZ_HALF_DEG / (N_AZ - 1)) * math.radians((EL_MAX_DEG - EL_MIN_DEG) / (N_EL - 1))
            * np.cos(np.radians(el_deg)))


def mapa_lambda_surrogado(x_roca: np.ndarray, el_deg: np.ndarray, dias: float = 30.0,
                          n_e: int = 160) -> np.ndarray:
    """Surrogate expected counts per pixel (historical grid) for a rock column map.

    lambda = Phi_int(E_min(X_rock + X_air), zenith) * A * dOmega * T, with the
    integral tabulated per row on a log grid of thresholds and interpolated.
    """
    cz = np.sin(np.radians(el_deg))
    emins = np.logspace(math.log10(e_min_csda(X_AIRE_SURROGATE)), math.log10(2e4), n_e)
    tabla = np.array([guan_integral(e, cz, n=3000) for e in emins]).T  # (rows, n_e)
    em = e_min_csda(x_roca + X_AIRE_SURROGATE)
    phi = np.empty_like(x_roca, dtype=float)
    for i in range(el_deg.size):
        phi[i] = np.exp(np.interp(np.log(em[i]), np.log(emins), np.log(np.maximum(tabla[i], 1e-300)),
                                  right=-700.0))
    d_omega = angulo_solido_historico(el_deg)[:, None]
    return phi * DET_AREA_CM2 * d_omega * dias * 86400.0 * fraccion_columna_historica()[None, :] * (N_AZ - 1)


# ------------------------------------------------------------------- figures
def configurar_matplotlib():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 160, "font.size": 9,
                         "axes.grid": True, "grid.alpha": 0.3, "svg.hashsalt": "oe1",
                         "path.simplify": False})
    coma = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
    return plt, coma


def guardar_figura(fig, nombre: str) -> str:
    FIGURAS.mkdir(parents=True, exist_ok=True)
    ruta = FIGURAS / nombre
    fig.savefig(ruta, bbox_inches="tight", metadata={"Software": None})
    return ruta_relativa(ruta)


# --------------------------------------------------------- geometry ray-march
def opacidad_vista(geo: dict, view_index: int, el_deg: np.ndarray, az_deg: np.ndarray,
                   paso_m: float = 2.0) -> np.ndarray:
    """Rock column [g/cm^2] along each (el, az) ray from the detector.

    Homogeneous cone only (anomalies ignored): used to classify open-sky
    pixels, where the column is exactly zero.
    """
    r_base = geo["edifice"]["base_radius_m"]
    h = geo["edifice"]["height_m"]
    rho = geo["edifice"]["rock_density_g_cm3"]
    va = math.radians(view_index * 60.0)
    origen = np.array([DET_DISTANCE_M * math.cos(va), DET_DISTANCE_M * math.sin(va), DET_HEIGHT_M])
    look = va + math.pi
    t = np.arange(max(0.0, DET_DISTANCE_M - 1.25 * r_base) + paso_m / 2,
                  DET_DISTANCE_M + 1.25 * r_base, paso_m)
    out = np.zeros((el_deg.size, az_deg.size))
    el = np.radians(el_deg)[:, None]
    az = look + np.radians(az_deg)[None, :]
    d = np.stack([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az),
                  np.sin(el) * np.ones_like(az)], axis=-1)
    for i in range(el_deg.size):
        pts = origen[None, None, :] + d[i][:, None, :] * t[None, :, None]
        r = np.hypot(pts[..., 0], pts[..., 1])
        sup = h * np.clip(1 - r / r_base, 0, None)
        dentro = (pts[..., 2] >= 0) & (pts[..., 2] <= sup)
        out[i] = dentro.sum(axis=1) * paso_m * 100.0 * rho
    return out

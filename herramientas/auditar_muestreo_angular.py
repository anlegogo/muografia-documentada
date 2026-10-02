"""Control analítico de la discretización angular, sin transporte Geant4.

Desde la réplica: python herramientas/auditar_muestreo_angular.py --salida SALIDA
Requiere numpy. Las constantes corresponden al código histórico y d8ca749.
No modela dispersión, aceptación espacial ni pérdidas de energía.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--salida', type=Path, required=True)
    args = p.parse_args()
    src = ROOT/'objetivo-1/originales/scripts/simulation/geant4_app'
    names = ['src/PrimaryGeneratorAction.cc', 'src/SteppingAction.cc',
             'src/FluxTables.cc', 'include/GeometryConfig.hh',
             'tables/row_weights_30d.txt']
    hashes = {name: hashlib.sha256((src/name).read_bytes()).hexdigest() for name in names}
    n = 256
    step = 60/(n-1)
    centers = np.linspace(-30, 30, n)
    # Intersección exacta de cada celda de redondeo con soporte del generador.
    widths = np.maximum(0, np.minimum(centers+step/2, 30)
                        - np.maximum(centers-step/2, -30))
    actual = widths/60
    nominal = np.full(n, 1/n)
    # Comprobación independiente: cuadratura uniforme por puntos medios.
    samples = 255*4096
    az = -30+60*(np.arange(samples)+0.5)/samples
    indices = np.floor((az+30)/step+0.5).astype(int)
    numerical = np.bincount(indices, minlength=n)/samples
    np.testing.assert_allclose(actual, numerical, atol=1e-14, rtol=0)
    np.testing.assert_allclose(actual.sum(), 1, atol=1e-14)
    weights = np.loadtxt(src/'tables/row_weights_30d.txt')
    row_prob = weights[:, 1]/weights[:, 1].sum()
    half = (weights[1, 0]-weights[0, 0])/2
    el_step = 45/255
    el_center = np.linspace(2, 47, n)
    lo, hi = weights[:, 0]-half, weights[:, 0]+half
    overlap = np.maximum(0, np.minimum(hi[:, None], el_center[None, :]+el_step/2)
                         - np.maximum(lo[:, None], el_center[None, :]-el_step/2))
    mapped = row_prob @ (overlap/(2*half))
    report = dict(
        alcance='fuente y redondeo angular sin transporte; no correccion de histogramas',
        fuentes_sha256=hashes,
        azimut=dict(numero_pixeles=n, paso_grados=step,
            probabilidad_nominal_por_columna=1/n,
            probabilidad_columna_extrema=float(actual[0]),
            probabilidad_columna_interior=float(actual[1]),
            razon_extremo_nominal=float(actual[0]*n),
            razon_interior_nominal=float(actual[1]*n),
            distancia_variacion_total=float(np.abs(actual-nominal).sum()/2),
            suma_probabilidades=float(actual.sum()),
            puntos_cuadratura=samples,
            error_maximo_cuadratura=float(np.max(abs(actual-numerical)))),
        elevacion=dict(soporte_min_grados=float(lo.min()), soporte_max_grados=float(hi.max()),
            probabilidad_fuera_centros_2_47=float(np.sum(row_prob*(
                np.maximum(0, 2-lo)+np.maximum(0, hi-47))/(2*half))),
            probabilidad_fuera_celdas=float(1-mapped.sum()),
            maxima_diferencia_probabilidad_fila=float(np.max(abs(mapped-row_prob)))),
        decision='documentar y fijar convencion antes de produccion; no cambiar tablas automaticamente')
    args.salida.mkdir(parents=True, exist_ok=True)
    np.savetxt(args.salida/'probabilidades-azimut.csv',
               np.column_stack((np.arange(n), centers, nominal, actual, actual/nominal)),
               delimiter=',', header='columna,centro_grados,p_nominal,p_generador,razon', comments='')
    (args.salida/'auditoria-angular.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

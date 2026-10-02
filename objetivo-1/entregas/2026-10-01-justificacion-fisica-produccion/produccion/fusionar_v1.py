#!/usr/bin/env python3
"""Exact merge of the blocks of each view (stdlib only). Not executed here.

Checks that every manifest block is published with exit code 0, that the
output hashes match, that all blocks of a view share the same inputs
(entradas.sha256 without the per-block paths) and that each block transported
exactly the events of the manifest. Sums the histograms bin by bin and writes
<geo>_view<v>_hist.csv, .meta.json and entradas.sha256 per view, the layout
consumed by herramientas/preparar_imagen_angular_v1.py.

Usage:
    python3 fusionar_v1.py --manifiesto manifiesto-v1-k2.csv --salida /ruta/salida-v1 --destino /ruta/fusion-v1
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifiesto", type=Path, required=True)
    ap.add_argument("--salida", type=Path, required=True)
    ap.add_argument("--destino", type=Path, required=True)
    a = ap.parse_args()
    if a.destino.exists():
        raise SystemExit("el destino ya existe; se exige una carpeta nueva")
    vistas = defaultdict(list)
    with open(a.manifiesto, encoding="utf-8") as fh:
        for f in csv.DictReader(fh):
            vistas[(f["geometria"], int(f["vista"]))].append(f)
    errores = []
    for (geo, v), bloques in sorted(vistas.items()):
        stem = f"{geo}_view{v}"
        suma, metas, entradas = None, [], set()
        for f in bloques:
            d = a.salida / geo / f"view{v}" / f"block{int(f['bloque']):04d}"
            try:
                assert (d / "exit_code.txt").read_text().strip() == "0", "código de salida"
                for linea in (d / "salida.sha256").read_text().splitlines():
                    h, p = linea.split()
                    assert sha(d / Path(p).name) == h, f"huella {Path(p).name}"
                meta = json.loads((d / f"{stem}.meta.json").read_text(encoding="utf-8"))
                assert meta["events_transported"] == int(f["eventos"]), "eventos distintos del manifiesto"
                entradas.add(frozenset(ln.split()[0] for ln in (d / "entradas.sha256").read_text().splitlines()))
                filas = [[int(x) for x in ln.split(",")] for ln in (d / f"{stem}_hist.csv").read_text().splitlines()]
                suma = filas if suma is None else [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(suma, filas)]
                metas.append((f, meta, d))
            except Exception as exc:  # noqa: BLE001
                errores.append(f"{d}: {exc}")
        if len(entradas) > 1:
            errores.append(f"{stem}: bloques con entradas distintas")
        if errores:
            continue
        out = a.destino / geo
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{stem}_hist.csv").write_text("\n".join(",".join(map(str, r)) for r in suma) + "\n")
        base = dict(metas[0][1])
        base["events_transported"] = sum(m["events_transported"] for _, m, _ in metas)
        base["ecomug_draws_total"] = sum(m.get("ecomug_draws_total", 0) for _, m, _ in metas)
        base["detected_in_bins"] = sum(sum(r) for r in suma)
        base["wall_seconds"] = sum(m.get("wall_seconds", 0.0) for _, m, _ in metas)
        base["block_seeds"] = [int(f["semilla"]) for f, _, _ in metas]
        base.pop("seed", None)
        base["merged_blocks"] = len(metas)
        (out / f"{stem}.meta.json").write_text(json.dumps(base, indent=1) + "\n")
        (out / "entradas.sha256").write_bytes((metas[0][2] / "entradas.sha256").read_bytes())
    if errores:
        raise SystemExit("fusión incompleta:\n" + "\n".join(errores))
    print(f"vistas fusionadas: {len(vistas)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idempotent launcher for the az-edges-v1 production manifest (stdlib only).

Submits only rows that are neither published nor queued, never more than the
free submission slots, and serializes concurrent calls with a file lock. This
prevents the duplicated jobs observed in the 2026-08-30 campaign (194 jobs for
114 views). Not executed in this delivery.

Usage (on guane, from the directory that holds this file):
    python3 lanzar_v1.py --manifiesto $PWD/manifiesto-v1-k1.csv --salida /ruta/salida-v1 [--dry-run]
"""

from __future__ import annotations

import argparse
import csv
import fcntl
import getpass
import os
import subprocess
from pathlib import Path

PREFIJO = "oe1v1-"


def publicado(salida: Path, fila: dict) -> bool:
    d = salida / fila["geometria"] / f'view{fila["vista"]}' / f'block{int(fila["bloque"]):04d}'
    codigo = d / "exit_code.txt"
    return codigo.exists() and codigo.read_text().strip() == "0" and (d / "salida.sha256").exists()


def en_cola(excluir: str | None) -> tuple[set[str], int]:
    out = subprocess.run(["squeue", "-h", "-u", getpass.getuser(), "-o", "%i %j"],
                         check=True, capture_output=True, text=True).stdout.split("\n")
    trabajos = [ln.split(maxsplit=1) for ln in out if ln.strip()]
    trabajos = [t for t in trabajos if t[0] != excluir]
    filas = {t[1][len(PREFIJO):] for t in trabajos if len(t) == 2 and t[1].startswith(PREFIJO)}
    return filas, len(trabajos)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifiesto", type=Path, required=True)
    ap.add_argument("--salida", type=Path, required=True)
    ap.add_argument("--max-trabajos", type=int, default=4, help="QoS MaxSubmitPU observado")
    ap.add_argument("--excluir-job", default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    a.salida.mkdir(parents=True, exist_ok=True)
    sbatch = Path(__file__).resolve().with_name("bloque_v1.sbatch")
    with open(a.salida / ".lanzador.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        with open(a.manifiesto, encoding="utf-8") as fh:
            filas = list(csv.DictReader(fh))
        cola, ocupados = en_cola(a.excluir_job)
        pendientes = [f for f in filas if f["fila"] not in cola and not publicado(a.salida, f)]
        libres = max(0, a.max_trabajos - ocupados)
        print(f"filas={len(filas)} pendientes={len(pendientes)} en_cola={len(cola)} libres={libres}")
        arbol = Path(os.environ.get("ARBOL", str(Path.home() / "oe1-trabajo/angular-v1")))
        (arbol / "logs").mkdir(exist_ok=True)   # SLURM does not create the --output directory
        for f in pendientes[:libres]:
            cmd = ["sbatch", f"--job-name={PREFIJO}{f['fila']}",
                   f"--export=ALL,MANIFIESTO={a.manifiesto.resolve()},FILA={f['fila']},"
                   f"SALIDA={a.salida.resolve()},CHAIN=1", str(sbatch)]
            print(" ".join(cmd))
            if not a.dry_run:
                subprocess.run(cmd, check=True, cwd=arbol)


if __name__ == "__main__":
    main()

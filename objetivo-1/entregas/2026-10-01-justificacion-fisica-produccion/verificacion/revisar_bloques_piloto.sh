#!/bin/bash
# Read-only check of the published pilot blocks: launcher records, SLURM logs,
# block metadata, histograms and receipts. Run on guane:
#   bash -l revisar_bloques_piloto.sh
set -uo pipefail
S="$HOME/muography-scratch/oe1-piloto-v2-publicados"
O="$S.operacion"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
MAN="$HOME/oe1-trabajo/integracion-c9442d6/replica/objetivo-1/evidencias/piloto-propuesto-siete-actividades/manifiesto-piloto-propuesto.csv"
echo "== registros"; ls "$O"
echo "== logs"; ls "$O/logs" 2>/dev/null
for f in "$O"/logs/*.out; do echo "-- $f"; tail -3 "$f"; done
echo "== intentos: $(ls "$HOME/muography-scratch/oe1-piloto-v2-intentos" 2>/dev/null | wc -l)"
"$PY" - "$S" "$O" "$MAN" <<'PYEOF'
import csv, glob, json, sys
from pathlib import Path
import numpy as np
S, O, MAN = map(Path, sys.argv[1:4])
rows = {int(r['fila']): r for r in csv.DictReader(open(MAN, encoding='utf-8'))}
for rec in sorted(O.glob('[0-9]*.json'), key=lambda p: int(p.stem)):
    d = json.loads(rec.read_text())
    r = rows[int(rec.stem)]
    b = S / r['geometria'] / f"view{r['vista']}" / f"block{int(r['bloque']):04d}"
    line = f"fila {rec.stem} job {d.get('job_id')} registro {d['status']}"
    if not b.exists():
        print(line, 'SIN BLOQUE PUBLICADO'); continue
    stem = f"{r['geometria']}_view{r['vista']}"
    m = json.loads((b / f'{stem}.meta.json').read_text())
    h = np.loadtxt(b / f'{stem}_hist.csv', delimiter=',')
    s = np.loadtxt(b / f'{stem}_hist_sin_corte.csv', delimiter=',')
    files = sorted(p.name for p in b.iterdir())
    ok = (h.shape == (256, 256) and int(h.sum()) == m['detected_in_bins'] and int(s.sum()) == m['detected_all_energies']
          and (h <= s).all() and m.get('exposure_days') == -1 and str(m.get('seed')) == r['semilla'] and str(m.get('events_transported')) == r['eventos'] and json.loads((b / 'publicacion-verificada.json').read_text()).get('status') in ('published', 'already_verified'))
    print(line, 'OK' if ok else 'REVISAR', {k: m.get(k) for k in ('seed', 'events_transported', 'detected_in_bins', 'detected_all_energies', 'nominal_in_window', 'conventional_exposure_days', 'exposure_days')})
    if rec.stem == '0':
        print('   archivos:', files)
        print('   meta keys:', sorted(m))
PYEOF

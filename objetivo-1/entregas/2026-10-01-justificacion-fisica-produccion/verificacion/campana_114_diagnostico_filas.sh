#!/bin/bash
# Read-only diagnosis of campaign rows whose jobs failed (2026-10-02 20:03-20:04,
# home quota exceeded). For each row: manifest entry, launcher record, SLURM state,
# attempt directories with their failure record, and the state of the publication
# path (absent, partial or verified). Run on guane:
#   bash -l campana_114_diagnostico_filas.sh 120 121 122
set -uo pipefail
BASE="$HOME/oe1-trabajo/campana-114-7c120ce"
REPO="$BASE/replica"
PY="$HOME/oe1-trabajo/entorno/python-oe1"
MAN="$REPO/objetivo-1/evidencias/preparacion-campana-114/manifiesto-114-344M.csv"
SALIDA="$HOME/muography-scratch/oe1-114-344M-publicados"
TEMPORAL="$HOME/muography-scratch/oe1-114-344M-intentos"
cd "$REPO/herramientas" || exit 2
"$PY" - "$MAN" "$SALIDA" "$TEMPORAL" "$@" <<'PYEOF'
import json, subprocess, sys
from pathlib import Path
from fusionar_bloques_angular import manifest_rows
from operar_bloque_angular import existing, relative_block
man, out, tmp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
rows = {r['fila']: r for r in manifest_rows(man)}
state = out.parent / (out.name + '.operacion')
for f in map(int, sys.argv[4:]):
    r = rows[f]; rel = relative_block(r)
    rec = json.loads((state / f'{f}.json').read_text())
    job = rec.get('job_id')
    sa = subprocess.run(['sacct', '-X', '-n', '-P', '-j', str(job), '-o', 'State,ExitCode,Start,End,NodeList'], capture_output=True, text=True).stdout.strip()
    print(f'== fila {f}: {r["geometria"]} vista {r["vista"]} bloque {r["bloque"]} semilla {r["semilla"]}')
    print('   registro:', rec.get('status'), 'job', job, '| sacct:', sa)
    log = sorted(state.glob(f'logs/*-{job}.out'))
    if log:
        tail = log[0].read_text(errors='replace').strip().splitlines()[-4:]
        print('   log:', ' / '.join(tail))
    for a in sorted(tmp.glob(f'intento-*/{rel.as_posix()}')):
        files = sorted(p.name for p in a.iterdir())
        fallo = a / 'fallo.json'
        print('   intento:', a.parent.parent.parent.name, '| exit_code:', (a / 'exit_code.txt').read_text().strip() if (a / 'exit_code.txt').exists() else None,
              '| fallo:', fallo.read_text().strip().replace('\n', ' ') if fallo.exists() else None, '| archivos:', len(files))
    target = out / rel
    if not target.exists():
        print('   publicado: no existe')
    else:
        try:
            print('   publicado: existe; existing() =', existing(man, r, out))
        except Exception as exc:
            print('   publicado: existe pero NO valida:', type(exc).__name__, exc)
        print('   archivos publicados:', sorted(p.name for p in target.iterdir()))
PYEOF
ls -la "$SALIDA.operacion" | grep -vE ' [0-9]+\.json$' | tail -5

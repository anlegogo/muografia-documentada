"""Download the 123 contract files from the public Drive folder and verify SHA-256."""
import hashlib
import sys
import time
from pathlib import Path

import gdown

root = Path(sys.argv[2])
rows = [l.split('\t') for l in Path(sys.argv[1]).read_text().splitlines() if l.strip()]
bad = []
for i, (rel, fid, expected) in enumerate(rows, 1):
    dest = root/rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(4):
        if not dest.exists() or hashlib.sha256(dest.read_bytes()).hexdigest() != expected:
            gdown.download(id=fid, output=str(dest), quiet=True)
        if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() == expected:
            break
        time.sleep(5 * (attempt + 1))
    else:
        bad.append(rel)
    print(f'{i}/{len(rows)} {rel} {"OK" if rel not in bad else "FAIL"}', flush=True)
print('verified', len(rows) - len(bad), 'of', len(rows), 'failed', bad)
sys.exit(1 if bad else 0)

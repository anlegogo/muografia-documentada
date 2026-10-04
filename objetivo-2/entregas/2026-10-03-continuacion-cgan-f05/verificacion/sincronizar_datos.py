"""Download the train/val shards and the initial U-Net weights from the public
Drive copies and verify each file against its expected SHA-256.

Input rows: relative path, Drive file id, expected SHA-256 (fuentes-drive.tsv).
Files already present with the right hash are kept. Exit code 1 if any file
cannot be verified.
  python sincronizar_datos.py fuentes-drive.tsv DESTINO
"""
import hashlib
import sys
import time
import urllib.request
from pathlib import Path

URL = 'https://drive.usercontent.google.com/download?id={}&export=download&confirm=t'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def fetch(fid, dest):
    tmp = dest.with_name(dest.name + '.part')
    with urllib.request.urlopen(URL.format(fid), timeout=300) as r, open(tmp, 'wb') as f:
        for block in iter(lambda: r.read(1 << 20), b''):
            f.write(block)
    tmp.replace(dest)


def main(table, root):
    root = Path(root)
    rows = [l.split('\t') for l in Path(table).read_text().splitlines() if l.strip()]
    failed = []
    for i, (rel, fid, expected) in enumerate(rows, 1):
        dest = root/rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        ok = dest.exists() and sha256(dest) == expected
        for attempt in range(5):
            if ok:
                break
            try:
                fetch(fid, dest)
            except Exception as exc:  # network or quota errors are retried
                print(f'reintento {rel}: {exc}', flush=True)
            ok = dest.exists() and sha256(dest) == expected
            if not ok:
                time.sleep(10 * (attempt + 1))
        if not ok:
            failed.append(rel)
        print(f'{i}/{len(rows)} {rel} {"OK" if ok else "FALLO"}', flush=True)
    print(f'verificados {len(rows) - len(failed)} de {len(rows)}; fallos {failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))

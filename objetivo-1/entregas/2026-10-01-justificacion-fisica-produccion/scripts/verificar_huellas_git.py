"""T-01 check: compare the bytes stored in Git with every SC3 hash manifest.

For each salidas.sha256 / salida.sha256 committed under datos/sc3, the file
it lists is read from the Git object database (`git show <rev>:<path>`), not
from the working tree, so the result does not depend on the local checkout
end-of-line conversion. A second pass applies CRLF->LF to the working-tree
copy to show where a checkout conversion would explain a mismatch.

Output: resultados/huellas-git-sc3.json

Usage (from the repository root):
    python objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/scripts/verificar_huellas_git.py [--rev HEAD]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import comun as c


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=c.RAIZ_REPO, check=True, capture_output=True).stdout


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="HEAD")
    rev = ap.parse_args().rev
    commit = git("rev-parse", rev).decode().strip()
    base = c.ruta_relativa(c.DATOS_SC3)
    archivos = git("ls-tree", "-r", "--name-only", commit, base).decode().splitlines()
    manifiestos = [a for a in archivos if Path(a).name in ("salidas.sha256", "salida.sha256")]
    filas = []
    for man in manifiestos:
        carpeta = Path(man).parent
        for linea in git("show", f"{commit}:{man}").decode().splitlines():
            h, ruta = linea.split(maxsplit=1)
            nombre = ruta.strip().lstrip("*")
            # paths are relative (./x) or absolute SC3 paths; resolve by file name inside the folder tree
            if nombre.startswith("./"):
                candidato = (carpeta / nombre[2:]).as_posix()
            else:
                candidato = (carpeta / Path(nombre).name).as_posix()
            if candidato not in archivos:
                filas.append({"manifiesto": man, "archivo": nombre, "estado": "no_versionado"})
                continue
            blob = git("show", f"{commit}:{candidato}")
            ok_blob = hashlib.sha256(blob).hexdigest() == h
            local = c.RAIZ_REPO / candidato
            ok_local = local.exists() and hashlib.sha256(local.read_bytes()).hexdigest() == h
            ok_local_lf = local.exists() and hashlib.sha256(local.read_bytes().replace(b"\r\n", b"\n")).hexdigest() == h
            filas.append({"manifiesto": man, "archivo": candidato, "sha256_declarado": h,
                          "coincide_blob_git": ok_blob, "coincide_copia_local": ok_local,
                          "coincide_copia_local_crlf_a_lf": ok_local_lf})
    resumen = {
        "commit": commit, "manifiestos": len(manifiestos), "entradas": len(filas),
        "no_versionadas": sum(f.get("estado") == "no_versionado" for f in filas),
        "coinciden_blob_git": sum(bool(f.get("coincide_blob_git")) for f in filas),
        "no_coinciden_blob_git": sum(f.get("coincide_blob_git") is False for f in filas),
        "coinciden_copia_local": sum(bool(f.get("coincide_copia_local")) for f in filas),
    }
    c.escribir_json(c.RESULTADOS / "huellas-git-sc3.json", {"resumen": resumen, "entradas": filas})
    print(json.dumps(resumen, indent=1))


if __name__ == "__main__":
    main()

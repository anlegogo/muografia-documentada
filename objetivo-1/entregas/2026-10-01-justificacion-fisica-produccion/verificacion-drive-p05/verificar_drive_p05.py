"""Verificación P-05: copia de distribución en Drive frente a los inventarios de la rama (f395570)."""
import hashlib, json, os, platform, sys, zlib
from datetime import datetime, timezone
import numpy as np

# Uso: python verificar_drive_p05.py SALIDA.json [CARPETA_COPIA] [REPO_muografia-documentada]
OUT = sys.argv[1]
G = sys.argv[2] if len(sys.argv) > 2 else r"G:\Mi unidad\datos-oe1-campana-114"
REPO = sys.argv[3] if len(sys.argv) > 3 else r"\\wsl.localhost\Ubuntu\home\reinaldo\dev\muografia-documentada"
I = os.path.join(REPO, "objetivo-1", "entregas", "2026-10-01-justificacion-fisica-produccion", "datos", "sc3", "campana-114")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def contenido(a):
    h = hashlib.sha256(); h.update(a.dtype.str.encode()); h.update(str(a.shape).encode())
    h.update(np.ascontiguousarray(a).tobytes()); return h.hexdigest()


def inventario(lista, base):
    """Compara cada línea 'hash  ./ruta' de un .sha256 con el archivo en base."""
    ok, mal, falta = 0, [], []
    for linea in open(lista, encoding="utf-8"):
        if not linea.strip():
            continue
        h, rel = linea.split(maxsplit=1)
        p = os.path.join(base, rel.strip().lstrip("./").replace("/", os.sep))
        if not os.path.exists(p):
            falta.append(rel.strip())
        elif sha(p) == h:
            ok += 1
        else:
            mal.append(rel.strip())
    return {"esperados": ok + len(mal) + len(falta), "coinciden": ok, "distintos": mal, "faltan": falta}


r = {"fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
     "copia": G, "entorno": {"python": sys.version.split()[0], "numpy": np.__version__,
                             "zlib": zlib.ZLIB_RUNTIME_VERSION, "plataforma": platform.platform()}}

# 1. Imágenes y fusión: huella de archivo contra los inventarios de posproceso
r["imagenes"] = inventario(I + r"\posproceso\imagenes.sha256", G + r"\imagenes")
r["fusion"] = inventario(I + r"\posproceso\fusion.sha256", G + r"\fusion")

# 2. Pares: contenido contra huellas-contenido.json; archivo contra el manifest de la propia copia
hc = json.load(open(I + r"\huellas-contenido.json", encoding="utf-8"))
man = {f["name"]: f["sha256"] for f in json.load(open(G + r"\pares\manifest.json", encoding="utf-8"))["files"]}
man_rama = {f["name"]: f["sha256"] for f in json.load(open(I + r"\pares\manifest.json", encoding="utf-8"))["files"]}
pc_ok, pc_mal, pf_ok = 0, [], 0
for name, exp in hc["pairs"].items():
    p = os.path.join(G, "pares", name)
    pf_ok += sha(p) == man.get(name)
    z = np.load(p, allow_pickle=False)
    bad = [k for k in ("counts_ref", "low_counts", "fractions") if contenido(z[k]) != exp[k]]
    pc_ok += not bad
    pc_mal += [(name, k) for k in bad]
r["pares"] = {"archivos": len(hc["pairs"]), "mismos_nombres_que_rama": set(man) == set(man_rama) == set(hc["pairs"]),
              "contenido_coincide": pc_ok, "arreglos_comparados": 3 * len(hc["pairs"]), "contenido_distinto": pc_mal,
              "archivo_coincide_con_manifest_de_la_copia": pf_ok,
              "archivo_coincide_con_manifest_de_la_rama": sum(man[n] == man_rama[n] for n in man_rama)}

# 3. dataset-v2 (derivado fuera del OE1): solo contenido, como información
sp = json.load(open(G + r"\dataset-v2\splits.json", encoding="utf-8"))
sc_ok, sc_mal = 0, []
for g, exp in hc["dataset_v2_shards"].items():
    z = np.load(os.path.join(G, "dataset-v2", "shards", g if g.endswith(".npz") else g + ".npz"), allow_pickle=False)
    bad = [k for k in ("ref_counts", "low_counts", "fractions") if contenido(z[k]) != exp[k]]
    sc_ok += not bad; sc_mal += [(g, k) for k in bad]
r["dataset_v2"] = {"shards": len(hc["dataset_v2_shards"]), "contenido_coincide": sc_ok, "contenido_distinto": sc_mal,
                   "pairs_per_split": sp.get("pairs_per_split")}

# 4. Inventario general de la copia
todos = [os.path.join(d, f) for d, _, fs in os.walk(G) for f in fs]
r["copia_total"] = {"archivos": len(todos), "bytes": sum(os.path.getsize(p) for p in todos),
                    "por_carpeta": {c: sum(1 for p in todos if os.path.relpath(p, G).split(os.sep)[0] == c)
                                    for c in ("imagenes", "fusion", "pares", "dataset-v2")}}
json.dump(r, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for k in ("imagenes", "fusion"):
    print(k, {x: (v if not isinstance(v, list) else len(v)) for x, v in r[k].items()})
print("pares", {k: (v if not isinstance(v, list) else len(v)) for k, v in r["pares"].items()})
print("dataset_v2", {k: (v if not isinstance(v, list) else len(v)) for k, v in r["dataset_v2"].items()})
print("copia", r["copia_total"], "| entorno", r["entorno"])

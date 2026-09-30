#!/usr/bin/env python3
"""Compara el análisis ejecutado en SC3 (etapa1-01) con su reproducción local (reproduccion-local-01).

Uso:
    python comparar_sc3_local.py [--sc3 DIR] [--local DIR] [--out ARCHIVO]

Por defecto usa las carpetas hermanas de este script y escribe el informe en la salida
estándar. Informe en texto plano, UTF-8, finales de línea LF. El archivo
comparacion-sc3-local.txt es la salida de:
    python comparar_sc3_local.py --out comparacion-sc3-local.txt

Criterios: archivos por SHA-256 (byte a byte); JSON por hojas (ruta de cada valor escalar);
.npz por arreglos (nombre, dtype, forma y valores) y por miembros del zip; otros textos por líneas.
Requiere Python >= 3.9 y numpy (solo para leer el .npz).
"""
import argparse
import hashlib
import itertools
import json
import os
import sys
import zipfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
CLAVES_TEXTO = {"fecha_utc": "fecha", "host": "entorno", "python": "entorno", "numpy": "entorno",
                "cwd": "ruta", "comando": "ruta"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def listar(raiz):
    return {os.path.relpath(os.path.join(d, f), raiz).replace(os.sep, "/"): os.path.join(d, f)
            for d, _, fs in os.walk(raiz) for f in fs}


def corto(v, n=90):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= n else s[:n - 3] + "..."


def hojas(o, ruta=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from hojas(v, f"{ruta}.{k}" if ruta else str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from hojas(v, f"{ruta}[{i}]")
    else:
        yield ruta, o


def clase_json(ruta):
    campo = ruta.split(".")[-1].split("[")[0]
    if "fecha" in campo:
        return "fecha"
    if campo in ("ruta", "ruta_usada") or ruta.startswith("figuras["):
        return "ruta"
    if ruta.startswith("herramienta.entorno."):
        return "entorno"
    return "otra"


def comparar_json(pa, pb, out, cuenta):
    a = dict(hojas(json.load(open(pa, encoding="utf-8"))))
    b = dict(hojas(json.load(open(pb, encoding="utf-8"))))
    dif = [k for k in a if k in b and a[k] != b[k]]
    solo_a = [k for k in a if k not in b]
    solo_b = [k for k in b if k not in a]
    out.append(f"  hojas JSON: SC3 {len(a)}, local {len(b)}; distintas {len(dif)}; "
               f"solo en SC3 {len(solo_a)}; solo en local {len(solo_b)}")
    for k in dif:
        c = clase_json(k)
        cuenta[c] = cuenta.get(c, 0) + 1
        out += [f"  hoja distinta [{c}] {k}", f"    SC3:   {corto(a[k])}", f"    local: {corto(b[k])}"]
    for k in solo_a:
        c = clase_json(k)
        cuenta[c] = cuenta.get(c, 0) + 1
        out += [f"  hoja solo en SC3 [{c}] {k}", f"    SC3:   {corto(a[k])}"]
    for k in solo_b:
        c = clase_json(k)
        cuenta[c] = cuenta.get(c, 0) + 1
        out += [f"  hoja solo en local [{c}] {k}", f"    local: {corto(b[k])}"]


def comparar_npz(pa, pb, out):
    with np.load(pa, allow_pickle=False) as za, np.load(pb, allow_pickle=False) as zb:
        claves_a, claves_b = sorted(za.files), sorted(zb.files)
        iguales = [k for k in claves_a if k in zb.files and za[k].dtype == zb[k].dtype
                   and za[k].shape == zb[k].shape and np.array_equal(za[k], zb[k])]
        out.append(f"  arreglos: SC3 {len(claves_a)}, local {len(claves_b)}; mismos nombres: "
                   f"{'sí' if claves_a == claves_b else 'no'}; iguales (dtype, forma y valores): {len(iguales)}; "
                   f"distintos: {len(claves_a) - len(iguales)}")
        for k in claves_a:
            out.append(f"    {k}: {'igual' if k in iguales else 'DISTINTO'} ({za[k].dtype}, {za[k].shape})")
    campos = ("date_time", "compress_type", "create_system", "create_version", "extract_version",
              "flag_bits", "external_attr")
    with zipfile.ZipFile(pa) as ra, zipfile.ZipFile(pb) as rb:
        na, nb = len(ra.namelist()), len(rb.namelist())
        comunes = [i for i in ra.infolist() if i.filename in rb.namelist()]
        mismo = sum(1 for i in comunes if ra.read(i) == rb.read(i.filename))
        dist = {}
        for i in comunes:
            j = rb.getinfo(i.filename)
            for c in campos:
                if getattr(i, c) != getattr(j, c):
                    dist.setdefault(c, (getattr(i, c), getattr(j, c)))
    out.append(f"  miembros .npy del zip: SC3 {na}, local {nb}; "
               f"contenido descomprimido idéntico: {mismo} de {len(comunes)}")
    out.append("  campos del encabezado zip distintos: " +
               ("; ".join(f"{c} (SC3 {a}, local {b})" for c, (a, b) in dist.items()) or "(ninguno)"))
    return len(iguales) == len(claves_a) == len(claves_b) and claves_a == claves_b


def comparar_texto(pa, pb, out, cuenta):
    la = open(pa, "rb").read().decode("utf-8").split("\n")
    lb = open(pb, "rb").read().decode("utf-8").split("\n")
    difs = [(i, x, y) for i, (x, y) in enumerate(itertools.zip_longest(la, lb), 1) if x != y]
    out.append(f"  líneas: SC3 {len(la)}, local {len(lb)}; distintas {len(difs)}")
    for i, x, y in difs:
        clave = (x or y or "").split("=")[0]
        c = CLAVES_TEXTO.get(clave, "otra")
        cuenta[c] = cuenta.get(c, 0) + 1
        out += [f"  línea {i} distinta [{c}] ({clave})", f"    SC3:   {corto(x or '')}", f"    local: {corto(y or '')}"]
        if clave == "comando":
            oa = {t for t in (x or "").split() if t.startswith("--")}
            ob = {t for t in (y or "").split() if t.startswith("--")}
            out.append(f"    opciones solo en SC3: {' '.join(sorted(oa - ob)) or '(ninguna)'}; "
                       f"solo en local: {' '.join(sorted(ob - oa)) or '(ninguna)'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sc3", default=os.path.join(AQUI, "etapa1-01"))
    ap.add_argument("--local", default=os.path.join(AQUI, "reproduccion-local-01"))
    ap.add_argument("--out")
    args = ap.parse_args()
    fa, fb = listar(args.sc3), listar(args.local)
    out = ["COMPARACIÓN DEL ANÁLISIS DE LA ETAPA 1: SC3 FRENTE A LA REPRODUCCIÓN LOCAL", "",
           "Carpeta de SC3 (trabajo 30570): etapa1-01. Carpeta local: reproduccion-local-01.",
           "Generado por comparar_sc3_local.py: python comparar_sc3_local.py --out comparacion-sc3-local.txt",
           "Criterios: archivos por SHA-256; JSON por hojas; .npz por arreglos; otros textos por líneas.",
           "Clases de diferencia (regla fija por nombre de campo): fecha = campo con 'fecha'; ruta = 'ruta',",
           "'ruta_usada', 'figuras', 'cwd' y 'comando'; entorno = 'herramienta.entorno.*', 'host', 'python' y",
           "'numpy'; otra = cualquier diferencia restante.", "", "ARCHIVOS DE LA CARPETA DE SC3", ""]
    cuenta, n_ident, n_dist, csv_ok, npz_ok, sin_par = {}, 0, 0, True, None, []
    for rel in sorted(fa):
        out.append(f"{rel}")
        if rel not in fb:
            out.append("  resultado: solo en SC3 (no existe en la carpeta local)")
            sin_par.append(rel)
            n_dist += 1
            continue
        ha, hb = sha256(fa[rel]), sha256(fb[rel])
        out += [f"  SHA-256 SC3:   {ha}", f"  SHA-256 local: {hb}"]
        if ha == hb:
            out.append("  resultado: IDÉNTICO byte a byte")
            n_ident += 1
            continue
        out.append("  resultado: DISTINTO byte a byte")
        n_dist += 1
        if rel.endswith(".csv"):
            csv_ok = False
        if rel.endswith(".json"):
            comparar_json(fa[rel], fb[rel], out, cuenta)
        elif rel.endswith(".npz"):
            npz_ok = comparar_npz(fa[rel], fb[rel], out)
        else:
            comparar_texto(fa[rel], fb[rel], out, cuenta)
    solo_local = sorted(set(fb) - set(fa))
    out += ["", "ARCHIVOS SOLO EN LA CARPETA LOCAL", ""]
    out += [f"{r} ({os.path.getsize(fb[r])} bytes)" for r in solo_local] or ["(ninguno)"]
    n_csv = sum(1 for r in fa if r.endswith(".csv"))
    out += ["", "RESUMEN", "",
            f"archivos en la carpeta de SC3: {len(fa)}; idénticos byte a byte: {n_ident}; "
            f"distintos byte a byte o ausentes en local: {n_dist}",
            f"tablas CSV de SC3: {n_csv}; todas idénticas byte a byte a las locales: "
            f"{'sí' if csv_ok and not any(r.endswith('.csv') for r in sin_par) else 'no'}",
            f"arreglos de mapas-etapa1.npz iguales a los locales: "
            f"{'sí' if npz_ok else ('no' if npz_ok is False else 'archivo idéntico byte a byte')}",
            "hojas o líneas distintas por clase: " + (", ".join(f"{k} {cuenta[k]}" for k in sorted(cuenta)) or "(ninguna)"),
            f"diferencias de clase 'otra': {cuenta.get('otra', 0)}",
            f"archivos solo en la carpeta local: {len(solo_local)}"]
    texto = "\n".join(out) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)
    else:
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
        sys.stdout.write(texto)


if __name__ == "__main__":
    main()

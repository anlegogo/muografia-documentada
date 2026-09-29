#!/usr/bin/env bash
#SBATCH --job-name=oe1-piloto
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=00:55:00
#SBATCH --output=oe1-piloto-%j.out
# Una variante, tres semillas; revisar recursos con SC3 antes de enviar.
set -euo pipefail
: "${VARIANT:?original o corregida}" "${BIN:?ruta absoluta}" "${GEOMETRY:?ruta absoluta}" "${TABLES:?ruta absoluta}" "${OUTROOT:?ruta absoluta nueva}"
[[ "$VARIANT" == original || "$VARIANT" == corregida ]] || exit 2
[[ "$BIN" = /* && "$GEOMETRY" = /* && "$TABLES" = /* && "$OUTROOT" = /* ]] || exit 2
[[ -x "$BIN" && -f "$GEOMETRY" && -d "$TABLES" ]] || exit 2
mkdir -p "$OUTROOT"
# mkdir sin -p impide sobrescribir una variante ya iniciada.
DEST="$OUTROOT/$VARIANT"
mkdir "$DEST"
date -u > "$DEST/entorno.txt"
printf 'binary=%s\ngeometry=%s\ntables=%s\nthreads=%s\njob=%s\n' "$BIN" "$GEOMETRY" "$TABLES" "${SLURM_CPUS_PER_TASK:-8}" "${SLURM_JOB_ID:-manual}" >> "$DEST/entorno.txt"
{ module list; } >> "$DEST/entorno.txt" 2>&1 || true
{ geant4-config --version; c++ --version; cmake --version; } >> "$DEST/entorno.txt" 2>&1 || true
sha256sum "$BIN" "$GEOMETRY" "$TABLES/row_weights_30d.txt" "$TABLES/p_cdf.txt" "$TABLES/meta.json" > "$DEST/entradas.sha256"
for SEED in 2026092801 2026092802 2026092803; do
    RUN="$DEST/$SEED"
    mkdir "$RUN"
    COMMAND=("$BIN" --geometry "$GEOMETRY" --view 0 --tables "$TABLES" --events 1000000 --seed "$SEED" --threads "${SLURM_CPUS_PER_TASK:-8}" --out "$RUN")
    printf '%q ' "${COMMAND[@]}" > "$RUN/comando.txt"
    printf '\n' >> "$RUN/comando.txt"
    "${COMMAND[@]}" > "$RUN/run.log" 2>&1
    if [[ "$VARIANT" == corregida ]] && grep -Eq 'GeomVol1002|GeomNav' "$RUN/run.log"; then
        echo "Advertencia geométrica en variante corregida: revisar $RUN/run.log" >&2
        exit 3
    fi
    test -s "$RUN/geo-train-06_view0_hist.csv"
    test -s "$RUN/geo-train-06_view0.meta.json"
    (cd "$RUN" && sha256sum geo-train-06_view0_hist.csv geo-train-06_view0.meta.json run.log comando.txt > SHA256SUMS)
done
echo 'Piloto terminado; comparar y revisar físicamente antes de concluir.'

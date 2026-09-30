#!/usr/bin/env bash
# Ejecutar dentro de una asignación SC3; 6 procesos secuenciales de 12 muones.
set -euo pipefail
: "${SLURM_JOB_ID:?Ejecutar dentro de una asignacion SLURM, no en el nodo de acceso}"
: "${BINARY_A:?Ruta absoluta al binario A2}"
: "${BINARY_B:?Ruta absoluta al binario B2}"
: "${GEOMETRY:?Ruta absoluta a geo-train-06.json}"
: "${TABLES:?Ruta absoluta a las tablas de etapa 1}"
: "${ROI_MASK:?Ruta absoluta a R_int.mask.txt congelada}"
: "${INPUT_DIR:?Ruta absoluta a complemento-r2-01-v1}"
: "${OUTPUT_DIR:?Ruta absoluta de salida NUEVA}"
for path in "$BINARY_A" "$BINARY_B" "$GEOMETRY" "$TABLES" "$ROI_MASK" "$INPUT_DIR" "$OUTPUT_DIR"; do
  [[ "$path" == /* ]] || { echo "Se requieren rutas absolutas: $path" >&2; exit 2; }
done
[[ ! -e "$OUTPUT_DIR" ]] || { echo 'La salida ya existe; no se sobrescribe.' >&2; exit 2; }
check_hash() {
  local got
  got=$(sha256sum -- "$1"); got=${got%% *}
  [[ "$got" == "$2" ]] || { echo "SHA-256 inesperado: $1" >&2; exit 3; }
}
check_hash "$BINARY_A" a07d83c443120bb0a7e0d32d73ad8f1c1fa7e7cba771e9fc8331f7218b0728f5
check_hash "$BINARY_B" ae76186647e7cc90796a9504cfa8bc763fc959484c2f78bf647cbe321f996852
check_hash "$GEOMETRY" c8f6c1352af1f7564356cffbd98e26fd6a5881e5ece15a0ab6f2ed60c8ea26ed
check_hash "$ROI_MASK" e76dcbe5926f9f4aeb61c556729d15c64124cd50a8577dca6beee9ffa317c5fd
check_hash "$TABLES/row_weights_30d.txt" 93ce67abe51c59ea3ac5c07dc99fd1615ae147df82c16d1bad64f5c0712d2c0c
check_hash "$TABLES/p_cdf.txt" 7161c8adf11711139840007dff26178221c4cfbff8fc3253cabdda50c533f6ae
check_hash "$TABLES/meta.json" 7ac4b6a9353af701b56e5a97ee783ed59072d58df52d80ddbdc0f5f70147d35d
list="$INPUT_DIR/geo-train-06_v0_r10_r201.primarios.csv"
list_sha=ae8318a704d004989f65faaa5b8fe5624281fefef7c65f370a281d2378402ea1
check_hash "$list" "$list_sha"
(cd "$INPUT_DIR" && sha256sum --check --strict SHA256SUMS.txt)
mkdir -- "$OUTPUT_DIR"
{
  date -u; hostname; printf 'SLURM_JOB_ID=%s\n' "$SLURM_JOB_ID"
  env | LC_ALL=C sort | grep -E '^(G4|SLURM_|OMP_|LOADEDMODULES=)' || true
  sha256sum -- "$BINARY_A" "$BINARY_B" "$GEOMETRY" "$ROI_MASK" "$list"
  sha256sum -- "$TABLES/row_weights_30d.txt" "$TABLES/p_cdf.txt" "$TABLES/meta.json"
} > "$OUTPUT_DIR/entorno.txt"
unset G4FORCENUMBEROFTHREADS G4FORCE_EVENTS_PER_TASK G4FORCE_GRAINSIZE G4RUN_MANAGER_TYPE G4FORCE_RUN_MANAGER_TYPE
"$BINARY_A" --check-primaries "$list" > "$OUTPUT_DIR/check-A2.txt" 2>&1
"$BINARY_B" --check-primaries "$list" > "$OUTPUT_DIR/check-B2.txt" 2>&1
printf 'variante\tsemilla_transporte\tprimarios\testado\n' > "$OUTPUT_DIR/estado.tsv"
for seed in 1026093011 1026093012 1026093013; do
  for variant in A B; do
    binary="$BINARY_A"; [[ "$variant" == A ]] || binary="$BINARY_B"
    dir="$OUTPUT_DIR/$variant/$seed"
    mkdir -p -- "$dir"
    cmd=("$binary" --primaries "$list" --primaries-sha256 "$list_sha"
      --roi-mask "$ROI_MASK" --roi-mask-sha256 e76dcbe5926f9f4aeb61c556729d15c64124cd50a8577dca6beee9ffa317c5fd
      --transport-seed "$seed" --variant "$variant" --case-code 6 --replica 10
      --region-pair 0,1 --muon-log full --geometry "$GEOMETRY" --view 0
      --tables "$TABLES" --seed "$seed" --threads 1)
    printf '%q ' "${cmd[@]}" > "$dir/comando.txt"
    printf '\n' >> "$dir/comando.txt"
    if (cd "$dir" && "${cmd[@]}" > run.log 2>&1); then
      printf '%s\t%s\t12\tPROCESO_OK\n' "$variant" "$seed" >> "$OUTPUT_DIR/estado.tsv"
    else
      rc=$?
      printf '%s\t%s\t12\tFALLO_%s\n' "$variant" "$seed" "$rc" >> "$OUTPUT_DIR/estado.tsv"
      exit "$rc"
    fi
    if [[ "$variant" == B ]] && grep -Eq 'G4Exception|GeomVol1002|GeomNav' "$dir/run.log"; then
      printf 'Aviso en B: revisar %s\n' "$dir/run.log" >&2
      exit 4
    fi
    (cd "$dir" && sha256sum -- *_muones.csv *_hist.csv *.meta.json comando.txt run.log > SHA256SUMS.txt)
  done
done
printf '%s\n' '6 procesos terminados; resultados fisicos pendientes de revision.' > "$OUTPUT_DIR/FINALIZADO.txt"

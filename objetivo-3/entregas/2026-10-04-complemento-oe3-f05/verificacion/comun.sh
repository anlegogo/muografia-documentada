# Variables comunes del complemento OE3-C1 (INSTRUCCIONES_COMPLEMENTO_OE3.md, main 39d8fd3).
W=/workspace
export PATH="$HOME/.local/bin:$PATH"
DATA="$W/insumos"
WEIGHTS="$W/pesos-locales.json"
EXISTING="$W/existente/evaluacion-final-f05"
OUT="$W/trabajo/complemento-oe3-v1"
REG=objetivo-2/evidencias/ef01-c2/controles.json
SCRIPT=objetivo-3/herramientas/complemento_oe3.py
COMMON_ARGS=(--repo . --data "$DATA" --weights "$WEIGHTS" --existing "$EXISTING" --registry "$REG" --output "$OUT")
MODELS=(unet_original cgan_original B1_C0 B1_C1 B2_C0 B2_C1 B3_C0 B3_C1)
marca(){ echo "$(date -u +%FT%TZ) $*" | tee -a "$W/estado.log"; }

# Variables comunes del ensayo de borde E1 (INSTRUCCIONES_BORDE_CGAN.md, main 156d4f5).
W=/workspace
export PATH="$HOME/.local/bin:$PATH"
export DATA="$W/insumos"
export MASKS="$W/trabajo/mascaras-ajuste-v1"
export WEIGHTS="$W/insumos/pesos/cgan-best.pt"
export OUT="$W/trabajo/ensayo-borde-e1"
COMMON=(--datos "$DATA" --mascaras "$MASKS" --pesos "$WEIGHTS" --raiz "$OUT")
ORQ=objetivo-2/herramientas/orquestar_borde_cgan.py
# Asignación fija pareja -> GPU, la misma en técnica y piloto (autorizada por el director).
declare -A GPU=([B1]=0 [B2]=1 [B3]=2)
marca(){ echo "$(date -u +%FT%TZ) $*" | tee -a "$W/estado.log"; }

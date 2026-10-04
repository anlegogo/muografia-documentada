# Variables comunes de la repetición cGAN (INSTRUCCIONES_REPETICION_CGAN_F05.md, main fd20c67).
# Se carga con `source` desde cada etapa.
W=/workspace
export PATH="$HOME/.local/bin:$PATH"
DATA="$W/insumos"
PESOS="$W/insumos/pesos/cgan-best.pt"
MASCARAS="$W/trabajo/mascaras-ajuste-v1"
SALIDAS="$W/trabajo/cgan-repeticion-f05"
COMUN=(--datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS")
# Asignación fija pareja -> GPU (paralelo autorizado por el director en el grupo).
declare -A GPU=([R1]=0 [R2]=1 [R3]=2)
marca(){ echo "$(date -u +%FT%TZ) $*" | tee -a "$W/estado.log"; }

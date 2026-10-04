# Variables comunes de la evaluación final OE2 (INSTRUCCIONES_EVALUACION_FINAL_OE2.md, main d42b763).
W=/workspace
export PATH="$HOME/.local/bin:$PATH"
DATA="$W/insumos"
WEIGHTS="$W/pesos-evaluacion.json"
OUT="$W/trabajo/evaluacion-final-f05"
SCRIPT=objetivo-2/herramientas/evaluacion_final_oe2.py
marca(){ echo "$(date -u +%FT%TZ) $*" | tee -a "$W/estado.log"; }

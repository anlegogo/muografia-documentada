#!/bin/bash
#SBATCH -J oe1-r201 -p legacy -N 1 -n 1 -c 1 --mem=1G -t 00:10:00
#SBATCH -o /home/dapintoo/oe1-trabajo/complemento-r2-01/slurm-%j.out
# OE1 complement R2-01: runs the director's executor (6 sequential processes of 12 muons) inside this allocation.
set -euo pipefail
W=/home/dapintoo/oe1-trabajo; I=$W/complemento-r2-01/insumos
source $W/etapa1/herramientas/env_stage1.sh   # gnu14/14.2.0 + geant4/11.4.2; unset G4FORCE*
export BINARY_A=$W/etapa1/build/A2/muography_sim BINARY_B=$W/etapa1/build/B2/muography_sim
export GEOMETRY=$W/catalogo/geo-train-06.json TABLES=$W/tablas ROI_MASK=$W/etapa1/analisis/roi/R_int.mask.txt
export INPUT_DIR=$I/objetivo-1/ensayos/complemento-r2-01-v1 OUTPUT_DIR=$W/complemento-r2-01/intento-01
bash $I/herramientas/ejecutar_complemento_r2_01.sh

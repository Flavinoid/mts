#!/bin/sh 

DIR="$(pwd)"
cd ../
PARENT_DIR="$(pwd)"
cd ../
GRANDPARENT_DIR="$(pwd)"
cd "${DIR}"

MACROD1_DIR="${PARENT_DIR}/data/in/macrod1"
TARG1_DIR="${PARENT_DIR}/data/in/targ1"
CONFIG_DIR="${DIR}/configs"
PREDICTIONS="${GRANDPARENT_DIR}/build_gene_predictions/data/out/predicted_mito_targeting_genes.txt"
OUTPUT_DIR="${DIR}/data/out"

python ../../../src/volcano.py "${MACROD1_DIR}"  "${CONFIG_DIR}" "${PREDICTIONS}" "${OUTPUT_DIR}"

python ../../../src/volcano.py "${TARG1_DIR}"  "${CONFIG_DIR}" "${PREDICTIONS}" "${OUTPUT_DIR}"
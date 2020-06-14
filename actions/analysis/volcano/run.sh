#!/bin/sh 

DIR="$(pwd)"
cd ../
PARENT_DIR="$(pwd)"
cd ../
GRANDPARENT_DIR="$(pwd)"
cd "${DIR}"

INPUT_CSV="${PARENT_DIR}/data/in/macrod1/TM_over_G270E.csv"
echo "input csv ${PARENT_DIR}"
INPUT_CONFIG="${DIR}/configs/TM_over_G270E.json"
PREDICTIONS="${GRANDPARENT_DIR}/build_gene_predictions/data/out/predicted_mito_targeting_genes.txt"
OUTPUT="${DIR}/data/out/TM_over_G270E.pdf"

python ../../../src/test.py "${INPUT_CSV}" "${INPUT_CONFIG}" "${PREDICTIONS}" "${OUTPUT}"

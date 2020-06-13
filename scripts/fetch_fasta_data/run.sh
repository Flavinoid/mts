#!/bin/sh 

if [ -d data/out/fasta ]; then 
    rm -r data/out/fasta     
fi

mkdir data/out/fasta

INFILE="protein_ids.csv"
OUTFILE="uniprot_results.csv"
python ./src/uniprot.py "data/in/${INFILE}" "data/out/${OUTFILE}"
python ./src/fasta.py "data/out/${OUTFILE}" "data/out/fasta"

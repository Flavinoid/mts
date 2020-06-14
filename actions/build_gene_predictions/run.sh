
GENE_AND_ASSOCIATED_PROTEINS="data/in/gene_and_associated_proteins.csv"

INFILE="../upload_fasta_files/data/out/predictions.txt"
OUTFILE="data/out/mito_targeting_proteinIDs.txt"

python ../../src/simplify_targetP_results.py "${INFILE}" "${OUTFILE}"

PREDICED_GENES="data/out/predicted_mito_targeting_genes.txt"

python ../../src/gene_predictions.py "${GENE_AND_ASSOCIATED_PROTEINS}" "${OUTFILE}" "${PREDICED_GENES}"
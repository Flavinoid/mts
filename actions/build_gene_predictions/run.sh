
GENE_AND_ASSOCIATED_PROTEINS="data/in/gene_and_associated_proteins.csv"
MITOCHONDRIAL_TRANSFER_PEPTIDES="../upload_fasta_files/data/out/mitochondrial_transfer_peptides.txt"
SIGNAL_PEPTIDES="../upload_fasta_files/data/out/signal_peptides.txt"
OUT_DIR="data/out"

python ../../src/gene_predictions.py "${GENE_AND_ASSOCIATED_PROTEINS}" "${MITOCHONDRIAL_TRANSFER_PEPTIDES}" "${SIGNAL_PEPTIDES}" "${OUT_DIR}"
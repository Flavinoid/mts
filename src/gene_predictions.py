import os
import sys

if __name__ == "__main__":

    gene_and_associated_proteins_path = sys.argv[1]
    mitochondrial_transfer_peptide_proteins_path = sys.argv[2]
    signal_peptides_path = sys.argv[3]
    output_dir = sys.argv[4]

    with open(
        mitochondrial_transfer_peptide_proteins_path, "r"
    ) as transfer_matches_file:
        transfer_matches = set(
            map(lambda x: x.strip(), transfer_matches_file.readlines())
        )

    with open(signal_peptides_path, "r") as signal_matches_file:
        signal_matches = set(map(lambda x: x.strip(), signal_matches_file.readlines()))

    matches = transfer_matches.union(signal_matches)
    genes = set()

    with open(gene_and_associated_proteins_path, "r") as f:
        data = map(lambda x: x.strip(), f.readlines())
        next(data)  # ignore header
        for line in data:
            [gene_str, protein_str] = line.split(",")
            gene = gene_str.split(";")[0]
            protein_set = set(protein_str.split(";"))
            if not protein_set.isdisjoint(matches):
                genes.add(gene)

    with open(os.path.join(output_dir, "predicted.txt"), "w") as f:
        for gene in genes:
            f.write("{}\n".format(gene))

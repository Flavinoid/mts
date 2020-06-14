import os
import sys

if __name__ == "__main__":

    gene_and_associated_proteins_path = sys.argv[1]
    mt_targeting_protein_ids_path = sys.argv[2]
    output_file = sys.argv[3]

    with open(mt_targeting_protein_ids_path, "r") as transfer_matches_file:
        matches = set(map(lambda x: x.strip(), transfer_matches_file.readlines()))

    genes = set()

    with open(gene_and_associated_proteins_path, "r") as f:
        data = map(lambda x: x.strip(), f.readlines())
        next(data)  # ignore header
        for line in data:
            [gene_str, protein_str] = line.split(",")
            gene = gene_str.split(";")[0]
            protein_set = set(protein_str.split(";"))
            if not protein_set.isdisjoint(matches):
                if gene:
                    genes.add(gene)

    with open(output_file, "w") as f:
        for gene in genes:
            f.write("{}\n".format(gene))

import json
import os
import sys


def collect_mitochondial_transfer_peptides(dir):
    matches = set()
    misses = set()
    for filename in os.listdir(dir):
        with open(os.path.join(dir, filename), "r") as file:
            asJson = json.load(file)
            sequences = asJson.get("SEQUENCES", [])
            for (gene, data) in sequences.items():
                prediction = data.get("Prediction", None)
                if prediction == "Mitochondrial transfer peptide":
                    matches.add(gene)
                else:
                    misses.add(gene)
    return (matches, misses)


if __name__ == "__main__":
    targetP_json_dir = sys.argv[1]
    output_dir = sys.argv[2]
    (matches, misses) = collect_mitochondial_transfer_peptides(targetP_json_dir)
    matchLen = len(matches)
    missLen = len(misses)
    print(
        "found {} 'Mitochondrial transfer peptide' genes out of {}\n".format(
            matchLen, matchLen + missLen
        )
    )
    with open(
        os.path.join(output_dir, "mitochondrial_transfer_peptides.txt"), "w"
    ) as file:
        for gene in matches:
            file.write("{}\n".format(gene))

import json
import os
import sys


def collect_mitochondial_transfer_peptides(dir):
    mito_matches = set()
    signal_matches = set()
    misses = set()
    for filename in os.listdir(dir):
        with open(os.path.join(dir, filename), "r") as file:
            asJson = json.load(file)
            sequences = asJson.get("SEQUENCES", [])
            for (gene, data) in sequences.items():
                # exctract the 'actual' name that we want to use
                # for example 'sp_Q15118_PDK1_HUMAN' maps to 'PDK1'
                # the rule is <sp|tr>_<UniProtKB>_<GENE>_<HUMAN|Hm>(_<number>)
                gene_name = gene.split("_")[2]
                # we do this for all of them just in case the script changes at some point
                # performance is not an issue!
                prediction = data.get("Prediction", None)
                if prediction == "Mitochondrial transfer peptide":
                    mito_matches.add(gene_name)
                elif prediction == "Signal peptide":
                    signal_matches.add(gene_name)
                else:
                    misses.add(gene_name)
    return (mito_matches, signal_matches, misses)


if __name__ == "__main__":
    targetP_json_dir = sys.argv[1]
    output_dir = sys.argv[2]
    (mito_matches, signal_matches, misses) = collect_mitochondial_transfer_peptides(
        targetP_json_dir
    )
    mito_matchLen = len(mito_matches)
    signal_matchLen = len(signal_matches)
    missLen = len(misses)
    print(
        "found {} 'Mitochondrial transfer peptide' proteins and {} 'Signal peptides' out of {}\n".format(
            mito_matchLen, signal_matchLen, mito_matchLen + signal_matchLen + missLen
        )
    )
    with open(
        os.path.join(output_dir, "mitochondrial_transfer_peptides.txt"), "w"
    ) as file:
        for gene in mito_matches:
            file.write("{}\n".format(gene))
    with open(os.path.join(output_dir, "signal_peptides.txt"), "w") as file:
        for gene in signal_matches:
            file.write("{}\n".format(gene))

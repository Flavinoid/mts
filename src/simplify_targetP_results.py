import os
import sys


def collect_mitochondial_targeting(file_path):
    mito_matches = set()
    signal_matches = set()
    misses = set()
    with open(file_path, "r") as file:
        lines = map(lambda x: x.strip(), file.readlines())
        next(lines)
        next(lines)
        for line in lines:
            [gene, _len, _mtp, _sp, _other, loc, _rc] = line.split()
            # exctract the 'actual' name that we want to use
            # for example 'sp_Q15118_PDK1_HUMAN' maps to 'Q15118'
            # the rule is <sp|tr>_<UniProtKB>_<GENE>_<HUMAN|Hm>(_<number>)
            gene_name = gene.split("_")[1]
            # we do this for all of them just in case the script changes at some point
            # performance is not an issue!
            if loc == "M":
                mito_matches.add(gene_name)
            elif loc == "S":
                signal_matches.add(gene_name)
            else:
                misses.add(gene_name)
    return (mito_matches, signal_matches, misses)


if __name__ == "__main__":
    # written for json input from the v2 api of targetP
    targetP_v1_prediction_path = sys.argv[1]
    output_file = sys.argv[2]
    (mito_matches, signal_matches, misses) = collect_mitochondial_targeting(
        targetP_v1_prediction_path
    )
    mito_matchLen = len(mito_matches)
    signal_matchLen = len(signal_matches)
    missLen = len(misses)
    print(
        "found {} 'Mitochondrial transfer peptide' proteins and {} 'Signal peptides' out of {}\n".format(
            mito_matchLen, signal_matchLen, mito_matchLen + signal_matchLen + missLen
        )
    )
    with open(output_file, "w") as file:
        for gene in mito_matches:
            file.write("{}\n".format(gene))

import csv
import sys
from concurrent.futures import ThreadPoolExecutor as Pool

import requests

FASTA_URL = "https://www.uniprot.org/uniprot/"


def fasta_url(protein_id):
    return "".join([FASTA_URL, protein_id, ".fasta"])


def get_fasta(protein_id):
    try:
        return (protein_id, requests.get(fasta_url(protein_id)).text)
    except requests.exceptions.ConnectionError:
        return (protein_id, None)


def get_fastas(executor, protein_ids):
    xs = executor.map(get_fasta, protein_ids)
    return xs


def fetch_uniprot_data(in_csv, out_csv, protein_ids_to_ignore=None):
    protein_ids_to_ignore = (
        frozenset(protein_ids_to_ignore) if protein_ids_to_ignore else frozenset()
    )
    with open(in_csv, "r") as in_file:
        # write header
        with open(out_csv, "w") as out_file:
            w = csv.writer(out_file)
            w.writerow(["protein_id", "FASTA header", "FASTA seq"])
        # query uniprot
        with Pool(max_workers=8) as executor:
            for line in in_file.readlines():
                line = line.strip()
                if line:
                    # only one column
                    protein_ids = frozenset(
                        x.strip() for x in line.split(";")
                    ).difference(protein_ids_to_ignore)
                    results = get_fastas(executor, protein_ids)
                    with open(out_csv, "a") as out_file:
                        w = csv.writer(out_file)
                        for protein_id, fasta in results:
                            if fasta:
                                fasta = fasta.split("\n")
                                f_head = fasta[0]
                                f_seq = "".join(fasta[1:])
                                w.writerow([protein_id, f_head, f_seq])
                            else:
                                w.writerow([protein_id, "", ""])


if __name__ == "__main__":
    input_csv = sys.argv[1]  # protein ID csv file
    output_csv = sys.argv[2]  # where to save the uniprot csv file
    # dont treat the header as an ID
    fetch_uniprot_data(input_csv, output_csv, ["Protein IDs"])

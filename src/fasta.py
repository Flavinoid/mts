import csv
import sys


def make_fasta_request_files(input_csv, out_dir):
    with open(input_csv, "r") as in_file:
        r = csv.reader(in_file, delimiter=",")
        next(r)  # ignore header
        max_residues = 200000
        max_sequences = 2000
        max_sequence_residues = 4000
        file_n = 1
        file_seqs = 0
        file_residues = 0
        for row in r:
            if row[1] != "":
                h = row[1].split()[0]
                f = row[2][:max_sequence_residues]
                residues = len(f)
                if (residues + file_residues) > max_residues:
                    # need to start in a new file
                    file_n += 1
                    file_seqs = 1
                    file_residues = residues
                elif file_seqs > max_sequences:
                    file_seqs = 1
                    file_residues = residues
                    file_n += 1
                else:
                    file_residues += residues
                    file_seqs += 1
                text = "\n".join([h, f])
                pth = out_dir + "/targetp_input" + str(file_n) + ".fasta"
                with open(pth, "a") as out_file:
                    out_file.write(text + "\n\n")


if __name__ == "__main__":
    input_csv = sys.argv[1]  # the uniprot csv file
    output_dir = sys.argv[2]  # directory for the fasta files to be written to
    make_fasta_request_files(input_csv, output_dir)

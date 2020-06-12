
import csv
import sys
from collections import defaultdict, namedtuple
from concurrent.futures import ThreadPoolExecutor as Pool
from enum import Enum, unique

import requests

FASTA_URL   = 'https://www.uniprot.org/uniprot/'

def fasta_url(protein_id):
    return ''.join([FASTA_URL,protein_id,'.fasta'])

def get_fasta(protein_id):
    try:
        return (protein_id, requests.get(fasta_url(protein_id)).text)
    except requests.exceptions.ConnectionError:
        return (protein_id, None)

def get_fastas(executor, protein_ids):
    xs = executor.map(get_fasta, protein_ids)
    return xs


def run(input_csv):
    with Pool(max_workers=8) as executor:
        xs = get_fastas(executor, ["Q99798", "Q9BQ69"])
        ys = [x.text if x else None for x in xs]
        for y in ys:
            print(y)


def run(in_csv, output, seen=None):
    with open(in_csv, "r") as in_file:
        with open(output, "w") as out_file:
            w = csv.writer(out_file)
            w.writerow(["protein_id", "FASTA header", "FASTA seq"])
        with Pool(max_workers=8) as executor:
            for line in in_file.readlines():
                line = line.strip()
                if line:
                    # only one column
                    protein_ids = [x.strip() for x in line.split(';')]
                    if seen:
                        protein_ids = list(filter(lambda x : x not in seen, protein_ids))
                    results = get_fastas(executor, protein_ids)
                    with open(output, "a") as out_file:
                        w = csv.writer(out_file)
                        for p_id, fasta in results:
                            if fasta:
                                fasta  = fasta.split('\n')
                                f_head = fasta[0]
                                f_seq  = ''.join(fasta[1:])
                                w.writerow([p_id, f_head, f_seq])
                            else:
                                w.writerow([p_id, "", ""])


# if __name__ == '__main__':

#     input_path = sys.argv[1]
#     output_path = sys.argv[2]
#     run(input_path, output_path)

def seen_names(existing_prot_csv):
    with open(existing_prot_csv, "r") as existing:
        checked = set()
        for line in existing.readlines():
            checked.add(line.split(',')[0])
    return checked


def make_fasta_request_files(input_csv, out_dir):
    with open(input_csv, 'r') as in_file:
        r = csv.reader(in_file, delimiter=',')
        next(r) # ignore header
        max_residues  = 200000
        max_sequences = 2000
        max_sequence_residues = 4000
        file_n = 1
        file_seqs = 0
        file_residues = 0
        for row in r:
            if row[1] != '':
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
                text = '\n'.join([h,f])
                pth = out_dir + '/out_file' + str(file_n) + '.fasta'
                with open(pth, 'a') as out_file:
                    out_file.write(text + '\n\n')



def add_predicition_data(protein_csv, prediction_file, new_file):

    d = {}
    csv_header_row = None
    prediction_headers = None

    with open(protein_csv, 'r') as in_csv:
        r = csv.reader(in_csv, delimiter=',')
        csv_header_row = next(r) # ignore header
        for row in r:
            identifier = row[1]
            if identifier:
                identifier = identifier.split('|')
                identifier = identifier[1]
                d[identifier] = row

    with open(prediction_file, 'r') as in_file:
        lines = in_file.readlines()
        prediction_headers = [line.strip() for line in lines[0].split()]
        results = lines[2:]
        for row in results:
            row = row.strip()
            if row:
                data = list(filter(lambda x : x != '', [x.strip() for x in row.split()]))
                label = data[0].split('_')[1]
                # print(data, label)
                if label not in d:
                    print("couldn't find:", label)

                d[label] = d[label] + data

    with open(new_file, 'w') as out_file:
        w = csv.writer(out_file)
        w.writerow(csv_header_row + prediction_headers)
        for row in d.values():
            w.writerow(row)


def csv_as_prediction_dict(input_csv):
    d = {}
    with open(input_csv, 'r') as f:
        r = csv.reader(f)
        next(r) # header
        for row in r:
           localization = row[7]
           d[row[0]] = row[7]
    return d

# pp = "/Users/beoliver/Documents/FlaviaGraphs/genes/data/PROTEIN_PREDICTIONS.csv"
# gp = "/Users/beoliver/Documents/FlaviaGraphs/genes/data/Macrod1_names.csv"
# op = "/Users/beoliver/Documents/FlaviaGraphs/genes/data/MACROD1_GENE_PREDICTIONS.csv"

def gene_predictions(protein_prediction_csv, gene_name_to_proteins_csv, out_csv):
    prediction_dict = csv_as_prediction_dict(protein_prediction_csv)
    header = ["Gene Name", "Protein Ids", "Protein Predictions", "M", "S", "Other", "Unkown"]
    with open(out_csv, 'w') as outf:
        w = csv.writer(outf)
        w.writerow(header)
    with open(gene_name_to_proteins_csv, 'r') as f:
        r = csv.reader(f)
        next(r) # header
        for row in r:
            [gene_names, protein_ids_str] = row
            protein_ids = [x.strip() for x in protein_ids_str.split(';')]
            predictions = [prediction_dict.get(x, '?') for x in protein_ids]
            predicted_n = len(predictions)
            m_n = len(list(filter(lambda x : x == 'M', predictions)))
            s_n = len(list(filter(lambda x : x == 'S', predictions)))
            o_n = len(list(filter(lambda x : x == '_', predictions)))
            u_n = len(list(filter(lambda x : x == '?', predictions)))
            prediction_str = ';'.join(predictions)
            with open(out_csv, 'a') as outf:
                w = csv.writer(outf)
                w.writerow([gene_names, protein_ids_str, prediction_str, m_n, s_n, o_n, u_n])



        # with open(output, "w") as out_file:
        #     out_file.write(','.join(["protein_id", "FASTA header", "FASTA seq", "\n"]))
        # with Pool(max_workers=8) as executor:
        #     for line in in_file.readlines():
        #         l = line.strip()
        #         if l:
        #             data = l.split(',')
        #             if data[3] == '':
        #                 data = data[0:3]
        #             if len(data) == 1:
        #                 with open(output, "a") as out_file:
        #                     writer = csv.writer(out_file)
        #                     writer.writerow([data.split(), "", ""])
        #             elif len(data) == 3:
        #                 with open(output, "a") as out_file:
        #                     [p_id, f_head, f_body] = data
        #                     w = csv.writer(out_file)
        #                     w.writerow([p_id, f_head, f_body])
        #             elif len(data) == 4:
        #                 with open(output, "a") as out_file:
        #                     [p_id, f_head1, f_head2, f_body] = data
        #                     f_head3 = ', '.join([f_head1, f_head2])
        #                     writer = csv.writer(out_file)
        #                     writer.writerow([p_id, f_head3, f_body])








# SIGNAL = 'having a signal peptide' # SIGNAL
# TARGET = 'having a mitochondrial targeting peptide' # MTS
# NOT    = 'not having signal or mitochondrial targeting peptide' # NOT

# @unique
# class ProteinType(Enum):
#     SIGNAL = 1
#     MTS    = 2
#     NOT    = 3

# def infer_signal_or_targeting(*protein_ids):
#     prediction_results = defaultdict(int)
#     for i in protein_ids:
#         f = extract_fasta(requests.get(fasta_url(i)).text)
#         p = requests.post(PREDICT_URL,data=prediction_form(f)).text
#         prediction_str = p.split('\n')[11][57:].split('<')[0]
#         prediction_results[prediction_str] += 1
#         if prediction_str == SIGNAL:
#             return ProteinType.SIGNAL.name
#     if prediction_results[SIGNAL] > 0:
#         return ProteinType.SIGNAL.name
#     elif prediction_results[TARGET] > 0:
#         return ProteinType.MTS.name
#     elif prediction_results[NOT] > 0:
#         return ProteinType.NOT.name
#     else:
#         return None

# ROW = namedtuple('ROW', ['protein_ids', 'labels'])

# def parse_row(line):
#     [labels,ids] = line.strip().split(',')
#     protein_ids = [x.strip() for x in ids.split(';')]
#     labels = [x.strip() for x in labels.split(';')]
#     return ROW(protein_ids, labels)

# def run(csv, output):
#     with open(csv, "r") as in_file:
#         with open(output, "w") as out_file:
#             headers = in_file.readline().strip()
#             out_file.write(','.join([headers, "prediction", "\n"]))

#         for line in in_file.readlines():
#             line = line.strip()
#             if line:
#                 row = parse_row(line)
#                 res = infer_signal_or_targeting(*row.protein_ids)
#                 lbs = ';'.join(row.labels)
#                 ids = ';'.join(row.protein_ids)
#                 print("lbs", lbs)
#                 print("ids",ids)
#                 print("res",res)
#                 with open(output, "a") as out_file:
#                     out_file.write(','.join([lbs, ids, res, '\n']))



# # if __name__ == '__main__':

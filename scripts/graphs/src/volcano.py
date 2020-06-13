# -*- coding: utf-8 -*-
import csv
import json
import sys
from collections import namedtuple

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROW = namedtuple("ROW", ["value", "difference", "label"])
CSV = namedtuple("CSV", ["name", "rows"])

# For sanity csv files should be run through `normalize_csv`
# that allows for some clean-up


def as_csv_path(directory, name):
    return "{}/{}.csv".format(directory, name)


def as_pdf_path(directory, name):
    return "{}/{}.pdf".format(directory, name)


def read_csv(in_csv):
    with open(in_csv, "r") as in_file:
        xs = list(
            filter(lambda s: s != "", map(lambda s: s.strip(), in_file.readlines()))
        )
    rows = []
    for line in xs[1:]:
        [value, difference, label] = line.split(",")
        v = float(value)
        d = float(difference)
        rows.append(ROW(v, d, label))
    return CSV("", rows)


def significant(row):
    return (row.value >= 1.3) and ((row.difference >= 1) or (row.difference <= -1))


# def default_vital_row(row):
#     return (row.label in labels_of_interest_phos) and significant(row)


def show_intersting(row):
    return (row.difference >= 2) and (row.value >= 2)


def save_chart(directory, name, figure):
    figure.savefig(as_pdf_path(directory, name), bbox_inches="tight", format="pdf")


def calulate_shared_labels(csvs):
    xs = map(lambda x: set([row.label for row in x.rows if significant(row)]), csvs)
    s = None
    for x in xs:
        if s == None:
            s = x
        else:
            s = s.intersection(x)
    return s


# def gene_lookup_dict(csv_path, id_col, value_col):
#     d = {}
#     with open(csv_path, "r") as f:
#         r = csv.reader(f)
#         next(r)
#         for row in r:
#             ids = row[id_col].split(";")
#             v = int(row[value_col])
#             v = False if (v == 0) else True
#             for i in ids:
#                 d[renamings.get(i, i)] = v
#     return d


# def make_chart1(
#     csv, is_vital_row=default_vital_row, is_interesting_row=None, figsize=(20, 10)
# ):
#     f = plt.figure(figsize=figsize)
#     # ax.axis(axis[name])
#     plt.xlabel("Difference", fontsize=14)
#     plt.ylabel("-log10(P-Value)", fontsize=14)
#     plt.title(csv.name, fontsize=14)
#     # add fixed horizontal lines
#     plt.axhline(y=1.3, linewidth=1, color="black", linestyle="dotted")
#     plt.axhline(y=2, linewidth=1, color="black", linestyle="dotted")
#     plt.axhline(y=3, linewidth=1, color="black", linestyle="dotted")
#     # add fixed vertical lines
#     plt.axvline(x=-1, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=-2, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=-4, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=1, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=2, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=4, linewidth=1, color="black", linestyle="dotted")
#     for row in csv.rows:
#         if is_vital_row(row):
#             plt.scatter(row.difference, row.value, marker="o", color="red", s=30)
#             allignment = custom_label_allignment[csv.name].get(
#                 row.label, {"ha": "center"}
#             )
#             plt.text(
#                 row.difference,
#                 row.value + 0.1,
#                 row.label,
#                 fontsize=14,
#                 fontweight="bold",
#                 **allignment
#             )
#             continue
#         else:
#             plt.scatter(row.difference, row.value, marker="o", color="lightgrey", s=5)
#             if is_interesting_row and is_interesting_row(row):
#                 allignment = custom_label_allignment[csv.name].get(
#                     row.label, {"ha": "center"}
#                 )
#                 plt.text(
#                     row.difference,
#                     row.value + 0.1,
#                     row.label,
#                     fontsize=10,
#                     **allignment
#                 )
#     return f


# def make_chart2(
#     csv,
#     predictions,
#     is_vital_row=default_vital_row,
#     is_interesting_row=None,
#     figsize=(7, 7),
# ):
#     f = plt.figure(figsize=figsize)
#     axes = plt.gca()
#     # remember axis depend on targ [-6, 16] / macrod1 [-4, 10] inputs!!!
#     axes.set_xlim([-6, 10])
#     axes.set_ylim([0, 7])
#     # ax.axis(axis[name])
#     plt.xlabel("Log2 fold change", fontsize=20)
#     plt.ylabel("-log10(P-Value)", fontsize=20)
#     plt.title(csv.name, fontsize=20)
#     # add fixed horizontal lines
#     plt.axhline(y=1.3, linewidth=1, color="black", linestyle="dotted")
#     plt.axhline(y=2, linewidth=1, color="black", linestyle="dotted")
#     plt.axhline(y=3, linewidth=1, color="black", linestyle="dotted")
#     # add fixed vertical lines
#     plt.axvline(x=-1, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=-2, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=-4, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=1, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=2, linewidth=1, color="black", linestyle="dotted")
#     plt.axvline(x=4, linewidth=1, color="black", linestyle="dotted")
#     for row in csv.rows:
#         if is_vital_row(row):
#             plt.scatter(row.difference, row.value, marker="o", color="red", s=30)
#             allignment = custom_label_allignment[csv.name].get(
#                 row.label, {"ha": "center"}
#             )
#             label = row.label
#             plt.text(
#                 row.difference,
#                 row.value + 0.1,
#                 label,
#                 fontsize=14,
#                 fontweight="bold",
#                 **allignment
#             )
#         elif predictions.get(row.label, False):
#             # M targeting possiblility
#             plt.scatter(row.difference, row.value, marker="o", color="lightblue", s=15)
#             if is_interesting_row and is_interesting_row(row):
#                 print(row.label)
#                 allignment = custom_label_allignment[csv.name].get(
#                     row.label, {"ha": "center"}
#                 )
#                 plt.text(
#                     row.difference,
#                     row.value + 0.1,
#                     row.label,
#                     fontsize=12,
#                     **allignment
#                 )
#         else:
#             plt.scatter(row.difference, row.value, marker="o", color="lightgrey", s=5)
#     custom_lines = [
#         Line2D([0], [0], color="red", lw=4),
#         Line2D([0], [0], color="lightblue", lw=4),
#         Line2D([0], [0], color="lightgrey", lw=4),
#     ]
#     plt.legend(
#         custom_lines,
#         ["Phosphorylation factors", "predicted MTS", "identified"],
#         loc="lower right",
#         prop={"size": 14},
#     )
#     return f


# def write_shared_named(directory, names):
#     csvs = list(map(lambda name: read_csv(directory, name), names))
#     print(len(csvs))
#     labels = calulate_shared_labels(csvs)
#     names = "_intersects_".join(map(lambda x: x.name, csvs))
#     fname = "".join([base_dir, names, ".csv"])
#     print(fname)
#     with open(fname, "w") as f:
#         for l in labels:
#             f.write(l + "\n")


if __name__ == "__main__":

    # this is a script for reading in CSV data and producing graphs.
    # input is expected to be a csv containing 3 columns:
    # VALUE | DIFFERENCE | lABEL

    input_csv_dir = sys.argv[1]
    prediction_file = sys.argv[2]
    settings = sys.argv[3]
    output_csv = sys.argv[4]

    # for (directory, data) in dirs_with_files.items():
    #     prediction_file = data["gene_predictions"]
    #     print(prediction_file)
    #     predictions = gene_lookup_dict(prediction_file, 0, 3)
    #     for name in data["names"]:
    #         csv = read_csv(directory, name)
    #         chart = make_chart2(csv, predictions)
    #         save_chart(directory, "{}-phos".format(name), chart)


# to make life easier you should change this string to
# reflect the directory that you have the csv files.
# base_dir = "/Users/benoliver/Documents/FlaviaGraphs/flavia_data"

# dirs_with_files = {
#     "MACROD1": {
#         "names": ["TM_over_GFP", "TM_over_G270E", "WT_over_GFP", "WT_over_G270E"],
#         "gene_predictions": "/Users/benoliver/Documents/FlaviaGraphs/genes/data/MACROD1_GENE_PREDICTIONS.csv",
#     },
#     "TARG1": {
#         "names": [
#             "TARG1_over_DK84-D123",
#             "TARG1_over_GFP",
#             "TARG1D125A_over_GFP",
#             "TARG1D125A_over_K84-D123",
#         ],
#         "gene_predictions": "/Users/benoliver/Documents/FlaviaGraphs/genes/data/TARG1_GENE_PREDICTIONS.csv",
#     },
# }

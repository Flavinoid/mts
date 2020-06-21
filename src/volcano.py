# -*- coding: utf-8 -*-
import csv
import json
import os
import subprocess
import sys
from collections import namedtuple
from multiprocessing import Pool

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from shared.utils import load_file_as_set

ROW = namedtuple("ROW", ["label", "pvalue", "enrichment"])
CSV = namedtuple("CSV", ["name", "rows"])

# For sanity csv files should be run through `normalize_csv`
# that allows for some clean-up


def makeDisplayCondition(m):
    if m.get("mts", False):
        # print("condition: must have mts")
        return lambda row, predictions: row.label in predictions
    enrichment = m.get("enrichment", None)
    if enrichment:
        gt = enrichment.get("GT", None)
        ge = enrichment.get("GE", None)
        if gt != None:
            # print("condition: must have enrichment > {}".format(gt))
            return lambda row, predictions: row.enrichment > gt
        if ge != None:
            # print("condition: must have enrichment >= {}".format(ge))
            return lambda row, predictions: row.enrichment >= ge
    value = m.get("pvalue", None)
    if value:
        gt = value.get("GT", None)
        ge = value.get("GE", None)
        if gt != None:
            # print("condition: must have value > {}".format(gt))
            return lambda row, predictions: row.pvalue > gt
        if ge != None:
            # print("condition: must have value >= {}".format(ge))
            return lambda row, predictions: row.pvalue >= ge


def conditionalDisplayFn(config):
    xs = config.get("conditionalDisplay", [])
    conditionals = list(map(makeDisplayCondition, xs))

    def f(row, predictions):
        res = list(map(lambda c: c(row, predictions), conditionals))
        return all(res)

    return f


Configured = namedtuple("Configured", ["csv_path", "config_path", "pdf_path"])


def generate_configurations(input_dir, config_dir, out_dir):
    print("Checking for existing PDF files in {}\n".format(out_dir))
    existing_pdfs = set(os.listdir(out_dir))
    print("Found total of {} PDF files".format(len(existing_pdfs)))

    print("Checking for config files in {}".format(config_dir))
    configs = set(os.listdir(config_dir))
    print("Found total of {} config files".format(len(configs)))

    print("Starting for directory: {}".format(input_dir))
    csv_file_names = os.listdir(input_dir)
    print("Found csv files: {}".format(csv_file_names))

    configurations = []
    # filter to find only those configs that should be used
    print("Calculcating config changes since last running...")
    for file_name in os.listdir(input_dir):
        print("\nInput CSV file: {}".format(file_name))
        input_name = file_name.split(".")[0]
        config_name = "{}.json".format(input_name)
        print("Looking for config file: {}".format(config_name))

        if config_name not in configs:
            print("WARNING: could not find config file: {}".format(config_name))
            continue

        config_path = os.path.join(config_dir, config_name)
        config_hash = (
            subprocess.check_output(["git", "hash-object", config_path])
            .decode("utf-8")
            .strip()
        )
        print("Calculated config hash to be: {}".format(config_hash))
        pdf_name = "{}_{}.pdf".format(input_name, config_hash)
        if pdf_name in existing_pdfs:
            print(
                "A pdf has already been generated using this configuration: {}\nSkipping.".format(
                    pdf_name
                )
            )
            continue
        else:
            csv_path = os.path.join(input_dir, file_name)
            out_path = os.path.join(
                out_dir, "{}_{}.pdf".format(input_name, config_hash)
            )
            configurations.append(Configured(csv_path, config_path, out_path))
    return configurations


def make_graph(configuration):
    with open(configuration.csv_path, "r",) as in_file:
        xs = list(
            filter(lambda s: s != "", map(lambda s: s.strip(), in_file.readlines()))
        )

    with open(configuration.config_path, "r",) as f:
        config = json.load(f)

    rows = []
    for line in xs[1:]:
        [pvalue, enrichment, label] = line.split(",")
        v = float(pvalue)
        e = float(enrichment)
        rows.append(ROW(label, v, e))

    predictions = load_file_as_set(prediction_path)
    shouldDisplay = conditionalDisplayFn(config)

    fig = plt.figure(figsize=tuple(config.get("figsize", [10, 10])))
    axes = plt.gca()
    # remember axis depend on targ [-6, 16] / macrod1 [-4, 10] inputs!!!
    axes.set_xlim(config.get("axis", {"x": [-10, 10]}).get("x"))
    axes.set_ylim(config.get("axis", {"y": [0, 10]}).get("y"))
    # ax.axis(axis[name])
    plt.xlabel("Log2 fold(Enrichment)", fontsize=20)
    plt.ylabel("-log10(P-Value)", fontsize=20)
    plt.title(config.get("title", "Untitled"), fontsize=20)
    # add fixed horizontal lines
    plt.axhline(y=1.3, linewidth=1, color="black", linestyle="dotted")
    plt.axhline(y=2, linewidth=1, color="black", linestyle="dotted")
    plt.axhline(y=3, linewidth=1, color="black", linestyle="dotted")
    # add fixed vertical lines
    plt.axvline(x=-1, linewidth=1, color="black", linestyle="dotted")
    plt.axvline(x=-2, linewidth=1, color="black", linestyle="dotted")
    plt.axvline(x=-4, linewidth=1, color="black", linestyle="dotted")
    plt.axvline(x=1, linewidth=1, color="black", linestyle="dotted")
    plt.axvline(x=2, linewidth=1, color="black", linestyle="dotted")
    plt.axvline(x=4, linewidth=1, color="black", linestyle="dotted")
    for row in rows:
        renamed_label = config.get("renamings", {}).get(row.label, row.label)
        allignment = config.get("alignment", {}).get(renamed_label, {"ha": "center"})
        reds = set(config.get("colors", {}).get("red", []))
        if row.label in predictions:
            plt.scatter(
                row.enrichment,
                row.pvalue,
                marker="o",
                color="lightblue",
                s=15,
                zorder=10,
            )
        else:
            plt.scatter(
                row.enrichment,
                row.pvalue,
                marker="o",
                color="lightgrey",
                s=5,
                zorder=0,
            )

        if renamed_label in reds:
            plt.scatter(
                row.enrichment, row.pvalue, marker="o", color="red", s=30, zorder=20
            )
            label = renamed_label
            plt.text(
                row.enrichment,
                row.pvalue + 0.1,
                label,
                fontsize=13,
                fontweight="bold",
                zorder=30,
                **allignment
            )
        else:
            if shouldDisplay(row, predictions):
                plt.text(
                    row.enrichment,
                    row.pvalue + 0.1,
                    renamed_label,
                    fontsize=10,
                    zorder=30,
                    **allignment
                )

    custom_lines = [
        Line2D([0], [0], color="red", lw=4),
        Line2D([0], [0], color="lightblue", lw=4),
        Line2D([0], [0], color="lightgrey", lw=4),
    ]
    plt.legend(
        custom_lines,
        [
            config.get("labels").get("red"),
            config.get("labels").get("blue", "predicted MTS"),
            config.get("labels").get("grey", "identified"),
        ],
        loc="lower right",
        prop={"size": 14},
    )

    fig.savefig(
        configuration.pdf_path, bbox_inches="tight", format="pdf",
    )


if __name__ == "__main__":

    input_dir = sys.argv[1]
    config_dir = sys.argv[2]
    prediction_path = sys.argv[3]
    out_dir = sys.argv[4]

    configurations = generate_configurations(input_dir, config_dir, out_dir)
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    if configurations:
        print("Preparing to generate {} PDFs".format(len(configurations)))
        for configuration in configurations:
            print(configuration.pdf_path)
            make_graph(configuration)
    else:
        print("Nothing to do!")
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

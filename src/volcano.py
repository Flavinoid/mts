# -*- coding: utf-8 -*-
import csv
import json
import os
import subprocess
import sys
from collections import namedtuple

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from shared.utils import load_file_as_set

ROW = namedtuple("ROW", ["label", "pvalue", "enrichment"])
CSV = namedtuple("CSV", ["name", "rows"])

# For sanity csv files should be run through `normalize_csv`
# that allows for some clean-up


def makeDisplayCondition(m):
    if m.get("mts", False):
        print("condition: must have mts")
        return lambda row, predictions: row.label in predictions
    enrichment = m.get("enrichment", None)
    if enrichment:
        gt = enrichment.get("GT", None)
        ge = enrichment.get("GE", None)
        if gt != None:
            print("condition: must have enrichment > {}".format(gt))
            return lambda row, predictions: row.enrichment > gt
        if ge != None:
            print("condition: must have enrichment >= {}".format(ge))
            return lambda row, predictions: row.enrichment >= ge
    value = m.get("pvalue", None)
    if value:
        gt = value.get("GT", None)
        ge = value.get("GE", None)
        if gt != None:
            print("condition: must have value > {}".format(gt))
            return lambda row, predictions: row.pvalue > gt
        if ge != None:
            print("condition: must have value >= {}".format(ge))
            return lambda row, predictions: row.pvalue >= ge


def conditionalDisplayFn(config):
    xs = config.get("conditionalDisplay", [])
    conditionals = list(map(makeDisplayCondition, xs))

    def f(row, predictions):
        res = list(map(lambda c: c(row, predictions), conditionals))
        return all(res)

    return f


if __name__ == "__main__":

    input_dir = sys.argv[1]
    config_dir = sys.argv[2]
    prediction_path = sys.argv[3]
    out_dir = sys.argv[4]

    print("creating PDF's for directory: {}".format(input_dir))

    for file_name in os.listdir(input_dir):
        input_name = file_name.split(".")[0]
        csv_path = os.path.join(input_dir, file_name)

        existing_pdfs = set(os.listdir(out_dir))

        with open(csv_path, "r",) as in_file:
            xs = list(
                filter(lambda s: s != "", map(lambda s: s.strip(), in_file.readlines()))
            )

        with open(os.path.join(config_dir, "{}.json".format(input_name)), "r",) as f:
            config = json.load(f)

        config_hash = (
            subprocess.check_output(["git", "hash-object", csv_path])
            .decode("utf-8")
            .strip()
        )
        pdf_name = "{}_{}.pdf".format(input_name, config_hash)
        if pdf_name in existing_pdfs:
            print(
                "config has not changed since last running program [{}]. Skipping this one!".format(
                    pdf_name
                )
            )
            continue

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
            allignment = config.get("alignment", {}).get(
                renamed_label, {"ha": "center"}
            )
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

        file_to_save = os.path.join(out_dir, pdf_name)
        print("saving to : {}".format(file_to_save))

        fig.savefig(
            file_to_save, bbox_inches="tight", format="pdf",
        )

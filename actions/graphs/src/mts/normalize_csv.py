# -*- coding: utf-8 -*-

import os

renamings = {"PEO1": "TWINKLE", "OARD1": "TARG1"}


def normalize_csv(input_file, invert_difference=False):
    (fname, ext) = os.path.splitext(os.path.basename(input_file))
    fname = fname + "_normalized" + ext
    outpath_base = os.path.dirname(input_file)
    out_path = os.path.join(outpath_base, fname)
    with open(out_path, "w") as out_file:
        with open(input_file, "r") as in_file:
            # write the first line verbatim as we ASSUME it is a header
            l = in_file.readline()
            out_file.write(l + os.linesep)
            for line in in_file.readlines():
                line = line.strip()
                if line:
                    [val, diff, names] = line.split(",")
                    name = names.split(";")[0].strip()
                    name = renamings.get(name, name)
                    if invert_difference:
                        diff = str(float(diff) * -1)
                    line = ",".join([val, diff, name])
                    out_file.write(line + os.linesep)

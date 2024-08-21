#!/usr/bin/env python3
import sys
#import re
from collections import defaultdict

if __name__ == "__main__":
    files = sys.argv[1:]
    print (files)
    npvs = set()
    data = defaultdict(dict)
    for fn in files:
        with open(fn, "r") as f:
            name = ""
            for i, line in enumerate(f):
                if i == 500: break
                fields = line.rstrip().split("\t")
                if name == "": name = fields[0]
                npv = "_".join(field for field in fields[1:-1])
                npvs.add(npv)
                freq = int(fields[-1])
                data[name][npv] = freq
        total = sum(freq for npv, freq in data[name].items() for name in data)
        for name in data:
            for npv in data[name]:
                data[name][npv] /= total
        print (total)
    for name in data:
        with open("natsume-{}-500.tsv".format(name), "w") as f:
            for npv in npvs:
                if npv in data[name]:
                    f.write(npv + "\t" + str(data[name][npv]) + "\n")
                else:
                    f.write(npv + "\t0\n")
    with open("natsume-500-summary.tsv", "w") as f:
        colnames = [name for name in npvs]
        rownames = [name for name in data]
        f.write("{}\n".format("\t".join(colname for colname in colnames)))
        for rowname in rownames:
            f.write("{}\t{}\n".format(rowname, "\t".join(str(data[rowname][colname]) if colname in data[rowname] else "0" for colname in colnames)))

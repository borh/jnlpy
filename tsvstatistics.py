from collections import defaultdict

def extract_columns(data):
    output = set()
    for corpus in data:
        for column in data[corpus]:
            output.add(column)
    return sorted(list(output))

def write_tsv(data, row_names, file, na="0.0"):
    with open(file, "w") as f:
        f.write("Rows\t{}\n".format("\t".join(row for row in row_names)))
        for column_name, record in data.items():
            features = []
            #print(row_names)
            #print(record)
            for row in row_names:
                if row in record:
                    features.append(str(record[row]))
                else:
                    features.append(na)
            f.write("{}\t{}\n".format(column_name, "\t".join(features)))

from customcounters import GenericCounter

def bin2tsv(data, filename, na=0):
    all_comb = extract_columns(data)
    all_dist = set()
    for bin in data:
        for counter in data[bin]:
            for dist in data[bin][counter]:
                all_dist.add(dist)
    for bin, counter in data.items():
        with open("{}-{}.tsv".format(filename, bin), "w") as f:
            f.write("Adv-mod combinations\t{}\n".format("\t".join(str(dist) for dist in all_dist)))
            reverse = defaultdict(GenericCounter)
            features = []
            for comb in all_comb:
                if comb in counter:
                    for dist in counter[comb]:
                        reverse[comb][dist] += 1
            for comb in all_comb:
                features = []
                features = "\t".join(str(reverse[comb][dist] if reverse[comb][dist] != 0 else na) for dist in all_dist)
                f.write("{}\t{}\n".format(comb, features))



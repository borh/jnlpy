#!/usr/bin/python3

import sys
import random

if __name__ == "__main__":
    filename = sys.argv[1]
    sample_size = int(sys.argv[2])

    lines = []
    with open(filename, "r") as f:
        for sentence in f:
            lines.append(sentence.rstrip())

    random.shuffle(lines)
    for i in range(sample_size):
        print (lines[i] + "\t" + filename)

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from customcounters import GenericCounter
from multiprocessing import Pool

from corpora import Corpora


def process(file):
    return sum(len(sentence) for sentence in file.to_sentences())

def main():
    if len(sys.argv) < 2:
        raise Exception("please specify directory or files as input")

    directories = sys.argv[1:]
    corpora = Corpora(directories)

    pool = Pool(7)

    morpheme_counter = GenericCounter()
    for corpus in corpora:
        for count in pool.imap(process, corpus, 500):
            morpheme_counter[corpus.name] += count

    print ("サブコーパス名,頻度")
    for corpus, freq in morpheme_counter.items():
        print ("{},{}".format(corpus, freq))

if __name__ == "__main__":
    sys.exit(main())

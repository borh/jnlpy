#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import pickle
import pickletools
from optparse import OptionParser

from sentence import Sentence
from mecabwrapper import MecabWrapper

def unidic_parse(filename):
    buffer = []
    sentences = []
    sentence_counter = 0
    with open(filename, "r") as file:
        for line in file:
            if line == "EOS\n" or line == "EOS":
                sentences.append(Sentence(buffer, sentence_counter))
                buffer = list()
                sentence_counter += 1
            else: buffer.append(line.rstrip('\n'))
    return sentences

def text_parse(filename):
    sentences = []
    sentence_counter = 0
    mecab = MecabWrapper()
    with open(filename, "r") as file:
        for line in file:
            sentences.append(mecab.parse(line.rstrip("\n"), sentence_counter))
            sentence_counter += 1
    return sentences

def pickle_optimize(object, file):
    with open(file, "wb") as f:
        picklestring = pickle.dumps(object)
        pickle.dump(pickletools.optimize(picklestring), f, pickle.HIGHEST_PROTOCOL)
        #pickle.dump(object, f, pickle.HIGHEST_PROTOCOL)

def main(argv=None):
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="infile",
                      help="read corpus from INFILE", metavar="INFILE")
    parser.add_option("-o", "--output", dest="outfile",
                      help="output pickled corpus to OUTFILE for further processing", metavar="OUTFILE")

    (options, args) = parser.parse_args()

    if not options.infile:
        parser.error("option -i is mandatory")

    filename_base = ""
    sentences = []
    if options.infile[-3:] == "txt":
        filename_base = options.infile[:-4]
        sentences = text_parse(options.infile)
    elif options.infile[-6:] == "unidic":
        filename_base = options.infile[:-6]
        sentences = unidic_parse(options.infile)
    else:
        raise Exception("Invalid input file type: {}".format(options.infile))

    pickle_optimize(sentences, filename_base + ".pickle")

if __name__ == "__main__":
    sys.exit(main())

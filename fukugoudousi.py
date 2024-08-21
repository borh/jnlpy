#!/usr/bin/python3
# -*- coding: utf-8 -*-
#import fileinput
import sys
import re
from collections import Counter

#from sentence import Sentence
from multiverbtable import MultiverbTable
from multiverbtable import CooccurenceTable
from multiverbgenerator import multiverb_data
from corpora import Corpora

exclude = set(["下さる", "為る", "為さる", "頂く", "致す"]) # おる -> +cType check?
#verb_histogram = Counter()

def extract_multiverbs(sentence, table, cooccurences, multiverbs, verb_histogram, file_id):
    if len(sentence.Morphemes) == 1:
        if re.match("動詞-一般", sentence.Morphemes[0].pos):
            if sentence.Morphemes[0].lemma in multiverbs:
                a, b, morpheme = multiverbs[sentence.Morphemes[0].lemma] # a, b always None for now
                morpheme.orth = sentence.Morphemes[0].orth # fix orth back to what it really is
                table.update(a, b, sentence.sentence_id, morpheme, file_id=file_id, type="single")
                cooccurences.update(morpheme.lemma, a, b)
            else:
                verb_histogram[sentence.Morphemes[0].lemma] += 1

    for i in range(len(sentence.Morphemes) - 1):
        if re.match("動詞-(一般|非自立可能)", sentence.Morphemes[i].pos):
            if sentence.Morphemes[i].lemma in multiverbs:
                # 1 morpheme is a multiverb
                a, b, morpheme = multiverbs[sentence.Morphemes[i].lemma] # a, b always None for now
                morpheme.orth = sentence.Morphemes[i].orth # fix orth back to what it really is
                table.update(a, b, sentence.sentence_id, morpheme, file_id=file_id, type="single")
                cooccurences.update(morpheme.lemma, a, b)
            elif (re.match("連用形", sentence.Morphemes[i].cForm) and
                  re.match("動詞", sentence.Morphemes[i + 1].pos) and
                  sentence.Morphemes[i + 1].lemma not in multiverbs and
                  sentence.Morphemes[i + 1].lemma not in exclude):
                # 2 morphemes are a multiverb
                table.update(sentence.Morphemes[i], sentence.Morphemes[i + 1], sentence.sentence_id, file_id=file_id, type="multi")
                ab_lemma = sentence.Morphemes[i].conjugate_base_to_renyou() + sentence.Morphemes[i + 1].lemma
                cooccurences.update(ab_lemma, sentence.Morphemes[i].lemma, sentence.Morphemes[i + 1].lemma)
                i += 1 # already matches next morpheme, skip it in the next iteration
            else:
                # record only the frequency of a single verb
                verb_histogram[sentence.Morphemes[i].lemma] += 1

def main():
    if len(sys.argv) < 2:
        raise Exception("please specify directory or files as input")

    directories = sys.argv[1:]
    corpora = Corpora(directories)

    #buffer = list()
    table = MultiverbTable()
    cooccurences = CooccurenceTable()
    multiverbs = multiverb_data()
    verb_histogram = Counter()

    for corpus in corpora:
        corpus_table = MultiverbTable()
        corpus_cooccurences = CooccurenceTable()
        corpus_multiverbs = multiverb_data()
        corpus_verb_histogram = Counter()
        for file in corpus:
            file_id = file.name
            for sentence in file.to_sentences():
                # extract multiverbs for all corpora
                extract_multiverbs(sentence, table, cooccurences, multiverbs, verb_histogram, file_id)
                # extract multiverbs for this specific corpus
                extract_multiverbs(sentence, corpus_table, corpus_cooccurences, corpus_multiverbs, corpus_verb_histogram, file_id)
        with open(corpus.name + "-multiverbs.tsv", "w") as f:
            f.write(str(corpus_table))
        with open(corpus.name + "-multiverb-cooccurences.tsv", "w") as f:
            f.write(str(corpus_cooccurences))
        histogram = "\n".join("{}\t{}".format(lemma, corpus_verb_histogram[lemma]) for lemma in corpus_verb_histogram)
        with open(corpus.name + "-verb-histogram.tsv", "w") as f:
            f.write(histogram)
            #sentence_counter = 0
            #for line in file:
            #    if line == "EOS":
            #        extract_multiverbs(Sentence(buffer, sentence_counter), table, cooccurences, multiverbs, file_id)
            #        buffer = list()
            #        sentence_counter += 1
            #    else: buffer.append(line.rstrip('\n'))

    #for line in file:
    #    if line == "EOS\n" or line == "EOS":
    #        extract_multiverbs(Sentence(buffer, sentence_counter), table, cooccurences, multiverbs)
    #        buffer = list()
    #        sentence_counter += 1
    #    else: buffer.append(line.rstrip('\n'))

    with open("multiverbs.tsv", "w") as f:
        f.write(str(table))
    with open("multiverb-cooccurences.tsv", "w") as f:
        f.write(str(cooccurences))
    histogram = "\n".join("{}\t{}".format(lemma, verb_histogram[lemma]) for lemma in verb_histogram)
    with open("verb-histogram.tsv", "w") as f:
        f.write(histogram)

if __name__ == "__main__":
    sys.exit(main())

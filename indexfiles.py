#!/usr/bin/env python3

import os
import sys
#import re
import pickle

from collections import defaultdict
from multiprocessing import Pool

from corpus import CorpusFile
from customcounters import GenericCounter
from statemachine import MorphemeMatcher
#from modalitydefinitions import adverb_list, modality_list
#from lexicalfeatures import nishina_features, tsutsuji_features, bunrui_features, adverb_list
from suppositionaladverbs import adverb_list
from tsutsujil8 import tsutsuji_features

#nishina_features_matcher = MorphemeMatcher(nishina_features)
tsutsuji_features_matcher = MorphemeMatcher(tsutsuji_features)
#bunrui_features_matcher = MorphemeMatcher(bunrui_features)
adverb_features_matcher = MorphemeMatcher(adverb_list)
#modality_matcher = MorphemeMatcher(modality_list)

def preprocess_file(file):
    tokens = 0
    pos_distribution = defaultdict(GenericCounter)
    print(file)
    for sentence in file.to_sentences():
        for morpheme in sentence:
            tokens += 1
            #if not re.match("^(名詞|動詞|空白|補助記号|記号)$", morpheme.pos1):
            #    pos_distribution["Morphemes"][morpheme.lemma] += 1
                #if morpheme.pos2 == "":
                #    pos_distribution[morpheme.pos1][morpheme.orthBase] += 1
                #else: pos_distribution[morpheme.pos1 + morpheme.pos2][morpheme.orthBase] += 1
        #nishina_features_matches = nishina_features_matcher.match(sentence)
        #for match in nishina_features_matches:
        #    pos_distribution["言語形式"][match[0]] += 1
        tsutsuji_features_matches = tsutsuji_features_matcher.match(sentence)
        for match in tsutsuji_features_matches:
            pos_distribution["Functional expressions"][match[0]] += 1
        #bunrui_features_matches = bunrui_features_matcher.match(sentence)
        #for match in bunrui_features_matches:
        #    pos_distribution["言語形式"][match[0]] += 1
        adverb_features_matches = adverb_features_matcher.match(sentence)
        for match in adverb_features_matches:
            pos_distribution["Suppositional adverbs"][match[0]] += 1

            #pos_distribution["モダリティ副詞"][match[0]] += 1
            #pos_distribution["モダリティ表現"][match[0]] += 1
        #modality_matches = modality_matcher.match(sentence)
        #for match in modality_matches:
        #    pos_distribution["モダリティ形式"][match[0]] += 1
        #    pos_distribution["モダリティ表現"][match[0]] += 1

    with open(file.basename + ".pickle", "wb") as f:
        pickle.dump((pos_distribution, tokens, file.basename), f, pickle.HIGHEST_PROTOCOL)
    #print (pos_distribution)

def pread(name):
    #(basename, extensions) = name
    preprocess_file(CorpusFile(name[0], name[1]))

if __name__ == "__main__":
    directories = sys.argv[1:]
    if directories == None or directories == []:
        raise Exception("No directories specified!")
    else:
        pool = Pool()
        for directory in directories:
            directory = os.path.abspath(directory)
            file_dict = defaultdict(set)
            #allowed_filetypes = set([".txt", ".unidic", ".cabocha", ".cabo"])
            allowed_filetypes = set([".suw", ".luw"])
            for root, dirs, files in os.walk(directory):
                for file, extension in map(os.path.splitext, files):
                    if extension in allowed_filetypes:
                        file_dict[root + "/" + file].add(extension)
            pool.map(pread, [item for item in file_dict.items()])
            #for basename, extensions in file_dict.items():
            #    preprocess_file(CorpusFile(basename, extensions))

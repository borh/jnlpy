#!/usr/bin/python3
# -*- coding: utf-8 -*-
import fileinput
#import re
#from collections import defaultdict

from sentence import Sentence
#from morpheme import Morpheme

if __name__ == "__main__":
    try:
        buffer = list()
        sentence_counter = 0
        multiple_morphemes = 0
        multiple_hojo_morphemes = 0
        for line in fileinput.input():
            if line == "EOS\n":
                s = Sentence(buffer, sentence_counter)
                if len(s.Morphemes) != 1 and s.Morphemes[-1].pos != "動詞-非自立可能":
                    print (s)
                    multiple_morphemes += 1
                elif len(s.Morphemes) != 1:
                    multiple_hojo_morphemes += 1
                buffer = list()
                sentence_counter += 1
            else: buffer.append(line.rstrip('\n'))
        print (sentence_counter, multiple_morphemes, multiple_hojo_morphemes)
    except:
        raise RuntimeError("Something went wrong when opening the file.")
#m = MeCab.Tagger ("-d /usr/lib64/mecab/dic/unidic -Ochasenu")
#
#for line in fileinput.input():
#    morpheme = m.parseToNode(line)
#    morpheme = morpheme.next
#    while (morpheme):
#        print morpheme.surface
#        featureList = morpheme.feature.split(',')
#        pos1 = featureList[0]
#        pos2 = featureList[5]
#
#        for i in range(len(featureList)):
#            print i, featureList[i]
#        morpheme = morpheme.next

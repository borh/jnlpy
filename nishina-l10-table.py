#!/usr/bin/env python3
import os
import sys
import re

#import operator

from corpus import CorpusFile
#from customcounters import GenericCounter
from collections import defaultdict

#L10_読み物_国際宇宙ステーション.txt
#L10_読む練習_宇宙技術のスピンオフ.txt
nishina_rx = re.compile("L(?P<id>\d{1,2})_(?P<type>.+)_(?P<name>.+)\.txt")

class expFile:
  def __init__(self, dir, level):
    filename = 'nL%d.exp' % level
    path = os.path.join(dir, filename)
    #file = codecs.open(path, 'r', 'utf-8')
    wordList = []
    #for line in file.readlines():
    for line in open(path):
      f = line.rstrip().split('\t')
      accepted = (f[3] == 'a' or f[3] == 'o')
      if accepted:
        wordList.extend(f[0:2])
      else:
        rejected = f[3] == 'd'
        if not rejected:
          raise Exception
          #raise 'not accepted or rejected'
    self.vocabulary = set(wordList)

  def includes(self, word):
    return word in self.vocabulary

def read_level():
    word_level = dict()
    for level in [1,2,3,4]:
        filename = 'nL%d.exp' % level
        print (filename)
        with open(filename, "r") as f:
            for line in f:
                f = line.rstrip().split('\t')
                accepted = (f[3] == 'a' or f[3] == 'o')
                if accepted:
                    word_level[f[0]] = level
                    word_level[f[1]] = level
                    word_level[f[2]] = level
                else: pass
    return word_level


def get_word_level(word, pos, word_level):
    if word in word_level:
        return word_level[word]
    elif re.match("^(記号|補助記号|名詞-数詞|空白|助詞-(格助詞|副助詞)|助動詞).*", pos):
        return 4 # all alphanumerics are level 4
    else:
        return 0


def tabulate(histogram, id, type, name, word_level):
    sorted_histogram = []
    for w in sorted(histogram, key=histogram.get, reverse=True):
        sorted_histogram.append((w, histogram[w]))
    #sorted_histogram = sorted(histogram.iteritems(), key=operator.itemgetter(1))
    return ("\n".join("{}\t{}\t{}\t{}\t{}\t{}級".format(term.split("#")[0], term.split("#")[1], frequency, id, type, get_word_level(term.split("#")[3], term.split("#")[2], word_level)) for (term, frequency) in sorted_histogram))


def write_tsv(basename, histogram, id, type, name, word_level):
    with open(basename + ".tsv", "w") as f:
        f.write("語彙・文法項目\t\t頻度\t課\t読み物/読む練習\t旧能力試験対応級\n")
        f.write("（表記:テキストと同じ）\tフリガナ\t\t\t\t\t\n")
        f.write(tabulate(histogram, id, type, name, word_level))


if __name__ == "__main__":
    word_level = read_level()
    files = sys.argv[1:]
    for f in files:
        basename = os.path.split(f)[1]
        named_matches = nishina_rx.match(basename)
        id = named_matches.group("id")
        type = named_matches.group("type")
        name = named_matches.group("name")

        #morpheme_histogram = GenericCounter()
        morpheme_histogram = defaultdict(int)
        basename, extensions = os.path.splitext(f)
        extensions = set([".txt", ".unidic"])
        c = CorpusFile(basename, extensions)
        for s in c.to_sentences():
            for m in s:
                if not re.match("^(記号|補助記号|名詞-数詞|空白).*", m.pos):
                    morpheme_histogram[m.orth + "#" + m.pron + "#" + m.pos + "#" + m.orthBase] += 1
        #print (tabulate(morpheme_histogram, id, type, name, word_level))
        write_tsv(os.path.splitext(basename)[0], morpheme_histogram, id, type, name, word_level)
        #print (morpheme_histogram)

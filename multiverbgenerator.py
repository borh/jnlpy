#!/usr/bin/python3
# -*- coding: utf-8 -*-

#import trie
#from pprint import pprint
import re
import sys
import getopt
#from multiprocessing import Pool

from morpheme import Morpheme
import pickle

def unidic_to_chasen_format(entry):
    fields = entry.split(",")
    #return "{}\t{}\t{}\t{}\t{}\t{}".format(fields[0], fields[10], fields[11], "-".join(fields[4:6]), fields[8], fields[9])
    return "{}\t{}".format(fields[0], ",".join(fields[4:]))

def extract_dictionary_entries(file="Verb.csv", condition=(lambda x: re.match(".*終止形-一般", x))):
    #with open(dictionary, "r") as file:
    for line in file:
        if condition(line):
            yield Morpheme(unidic_to_chasen_format(line.rstrip("\n")))

def is_final_verb(verb):
    return True if re.match(".*終止形-一般", verb) else False

def multiverb_data():
    with open("multiverbs.pickle", "rb") as f:
        data = pickle.load(f)
    return data

def EmptyMorpheme():
    return Morpheme("?\t?\t?\t?\t?\t?\t?\t?")

hiragana = "[\u3041-\u309F]"
katakana = "[\u30A0-\u30FF]"
kanji = "[\u4E00-\u9FFF]"

#multiverb_regex = re.compile("^({}+|{}+){}+{}{}+$".format(kanji, katakana, hiragana, kanji, hiragana))
multiverb_regex = re.compile("^({}+|{}+|{}+){}{}+$".format(kanji, katakana, hiragana, kanji, hiragana))

def count_kanji(string):
    return sum(1 for char in string if re.match("^{}$".format(kanji), char))

class MultiverbGenerator(object):
    """generate (fake) multiverb trie from verb_list

    """

    def __init__(self, multiverbs_file=None, singleverbs_file=None):
        self.load_unidic()
        if multiverbs_file == None and singleverbs_file == None:
            self.generate_from_list()
        else:
            self.generate_from_files(multiverbs_file, singleverbs_file)

    def load_unidic(self):
        self.unidic_verbs = list() # list of morphemes in verb dictionary
        self.lemma_ab = dict()
        self.lemma2morpheme = dict()
        with open("Verb.csv", "r") as file:
            for line in file:
                if re.match(".*終止形-一般", line):
                    self.unidic_verbs.append(Morpheme(unidic_to_chasen_format(line.rstrip("\n"))))

        for morpheme in self.unidic_verbs:
            self.lemma2morpheme[morpheme.lemma] = morpheme
            if morpheme.orth not in self.lemma2morpheme:
                self.lemma2morpheme[morpheme.orth] = morpheme

        self.verbs = set(verb.orth for verb in self.unidic_verbs) | set(verb.lemma for verb in self.unidic_verbs)
        # set of lemma and surface representations of verbs in the verb dictionary (unidic_verbs)
        self.lemmaverbs = set(verb.lemma for verb in self.unidic_verbs)
        print ("Unidic verb count: {}, lemma only: {}".format(len(self.unidic_verbs), len(self.lemmaverbs)))

        self.nouns = set() # set of lemma and surface representations of nouns in the noun dictionary
        with open("Noun.common.csv", "r") as file:
            for line in file:
                m = Morpheme(unidic_to_chasen_format(line.rstrip("\n")))
                #if len(m.orth) > 1:  self.nouns.add(m.orth)
                self.nouns.add(m.orth)
                #if len(m.lemma) > 1: self.nouns.add(m.lemma)
                self.nouns.add(m.lemma)
        print ("Unidic noun count:", len(self.nouns))

        self.extended_verbs = set() # verbs that do not really exist in the dictionary, but help use match more multiverbs
        for verb in self.unidic_verbs:
            if re.match("五段-.*", verb.cType):
                self.extended_verbs.add(verb.lemma[:-1] + "せる")
                self.extended_verbs.add(verb.orth[:-1] + "せる")
        #print ("adding", len(self.extended_verbs), "to verbs")
        self.verbs |= self.extended_verbs

        # set of renyou case verbs in the verb dictionary
        self.renyou_verbs = set(verb.conjugate_base_to_renyou("orth") for verb in self.unidic_verbs) | set(verb.conjugate_base_to_renyou("lemma") for verb in self.unidic_verbs)


    def generate_from_files(self, multiverbs_file, singleverbs_file):
        self.multiverbs = set()
        with open(multiverbs_file, "r") as f:
            for line in f:
                self.multiverbs.add(line.rstrip("\n"))

        for verb in self.multiverbs:
            #self.lemma_ab[verb] = (EmptyMorpheme(), EmptyMorpheme(), self.lemma2morpheme[verb])
            self.lemma_ab[verb] = (None, None, self.lemma2morpheme[verb])
        check = sorted(list(set(lemma for lemma in self.lemmaverbs if lemma not in self.multiverbs)))
        for item in check:
            print (item)

    def find_morpheme_fragments(self, ab, border):
        this_morpheme = self.lemma2morpheme[ab]
        #bmorpheme = Morpheme("\t\t\t\t\t\t\t")
        #bmorpheme = Morpheme("?\t?\t?\t?\t?\t?\t?\t?")
        #amorpheme = Morpheme("\t\t\t\t\t\t\t")
        #amorpheme = Morpheme("?\t?\t?\t?\t?\t?\t?\t?")
        amorpheme = None
        bmorpheme = None
        return (amorpheme, bmorpheme, this_morpheme)
################################# TODO ##############################
####averb = ab[0:border]
####bverb = ab[border:]
####if bverb in self.lemma2morpheme:
####    bmorpheme = self.lemma2morpheme[bverb]
####else:
####    print ("Failed on b", this_morpheme, averb, bverb)
####    bmorpheme = Morpheme("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(bverb, bverb, "?", "動詞-一般", this_morpheme.cType, "終止形-一般", 0, 0)) # dummy (TODO/FIX)
####
####if (border > 1):
####    if   averb[0:border-1] + "う" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "う"]
####    elif averb[0:border-1] + "ふ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "ふ"]
####    elif averb[0:border-1] + "ぶ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "ぶ"]
####    elif averb[0:border-1] + "る" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "る"]
####    elif averb[0:border-1] + "く" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "く"]
####    elif averb[0:border-1] + "ぐ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "ぐ"]
####    elif averb[0:border-1] + "す" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "す"]
####    elif averb[0:border-1] + "ず" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "ず"]
####    elif averb[0:border-1] + "つ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "つ"]
####    elif averb[0:border-1] + "づ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "づ"]
####    elif averb[0:border-1] + "む" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "む"]
####    elif averb[0:border-1] + "ぬ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "ぬ"]
####    elif averb[0:border-1] + "ゆ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + "ゆ"]
####    ##
####    elif averb[0:border] + "う" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "う"]
####    elif averb[0:border] + "ふ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "ふ"]
####    elif averb[0:border] + "ぶ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "ぶ"]
####    elif averb[0:border] + "る" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "る"]
####    elif averb[0:border] + "く" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "く"]
####    elif averb[0:border] + "ぐ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "ぐ"]
####    elif averb[0:border] + "す" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "す"]
####    elif averb[0:border] + "ず" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "ず"]
####    elif averb[0:border] + "つ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "つ"]
####    elif averb[0:border] + "づ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "づ"]
####    elif averb[0:border] + "む" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "む"]
####    elif averb[0:border] + "ぬ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "ぬ"]
####    elif averb[0:border] + "ゆ" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border] + "ゆ"]
####    else: amorpheme = Morpheme("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(averb[0:border], averb[0:border], "?", "動詞-一般", "?", "終止形-一般", 0, 0)) # dummy (TODO/FIX)
####    #elif averb[0:diff-1] + "" in self.lemmaverbs: amorpheme = self.lemma2morpheme[averb[0:border-1] + ""]
####    if amorpheme.lemma != "?": amorpheme.orth = amorpheme.conjugate_base_to_renyou("lemma")
####else:
####    print ("Failed on a", this_morpheme, averb, bverb)
####    amorpheme = Morpheme("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(averb[0:border], averb[0:border], "?", "動詞-一般", "?", "終止形-一般", 0, 0)) # dummy (TODO/FIX)
####
####return (amorpheme, bmorpheme, this_morpheme)


    def generate_from_list(self):
        self.multiverbs = set() # set of multiverbs in verb dictionary
        self.backwards_multiverbs = set()
        for averb in self.verbs:
            if averb in self.extended_verbs or averb in self.backwards_multiverbs or len(averb) < 4 or averb not in self.lemmaverbs: continue
            for bverb in self.verbs:
                if bverb in self.backwards_multiverbs or bverb == "する": continue
                diff = len(averb) - len(bverb)
                if diff > 1 and averb[diff:] == bverb:
                    self.backwards_multiverbs.add(averb)
                    self.lemma_ab[averb] = self.find_morpheme_fragments(averb, diff)
                    break

        self.multiverbs |= self.backwards_multiverbs
        print ("Multiverbs extracted using the backwards method:", len(self.backwards_multiverbs & self.lemmaverbs))

        self.regex_multiverbs = set()
        self.tsu_multiverbs = set()
        self.renyou_multiverbs = set()
        self.kanji_multiverbs = set()
        for verb in self.verbs:
            if len(verb) < 3 or verb in self.extended_verbs or verb not in self.lemmaverbs: continue

            if multiverb_regex.match(verb):
                self.multiverbs.add(verb)
                self.regex_multiverbs.add(verb)
                i = len(verb) - 1
                while (not re.match("^{}$".format(kanji), verb[i]) and i >= 0):
                    i -= 1
                if i != -1:
                    self.lemma_ab[verb] = self.find_morpheme_fragments(verb, i)
                else:
                    print ("WTF", verb)
                continue
            elif verb[1] == "っ":
                self.multiverbs.add(verb)
                self.tsu_multiverbs.add(verb)
                while (not re.match("^{}$".format(kanji), verb[i]) and i >= 0):
                    i -= 1
                if i != -1:
                    self.lemma_ab[verb] = self.find_morpheme_fragments(verb, i)
                else:
                    print ("WTF", verb)
                continue
            elif count_kanji(verb) > 1:
                self.multiverbs.add(verb)
                self.kanji_multiverbs.add(verb)
                i = len(verb) - 1
                while (not re.match("^{}$".format(kanji), verb[i]) and i >= 0):
                    i -= 1
                if i != -1:
                    self.lemma_ab[verb] = self.find_morpheme_fragments(verb, i)
                else:
                    print ("WTF", verb)
                continue

            for renyou_verb in self.renyou_verbs:
                if (len(verb) > len(renyou_verb) and
                    renyou_verb == verb[0:len(renyou_verb)] and
                    verb[len(renyou_verb):] in self.verbs):
                    self.multiverbs.add(verb)
                    self.renyou_multiverbs.add(verb)
                    self.lemma_ab[verb] = self.find_morpheme_fragments(verb, len(renyou_verb))
                    break
        print ("Multiverbs extracted with regex {}: {}, tsu: {}, kanji: {}".format(multiverb_regex.pattern, len(self.regex_multiverbs & self.lemmaverbs), len(self.tsu_multiverbs & self.lemmaverbs), len(self.kanji_multiverbs & self.lemmaverbs)))
        print ("Multiverbs extracted using the forward (renyou) method:", len(self.renyou_multiverbs & self.lemmaverbs))

        self.nounverbs = set() # set of noun-type multiverbs in verb dictionary
        for verb in self.verbs:
            if len(verb) < 4 or verb in self.extended_verbs or verb in self.multiverbs or verb not in self.lemmaverbs or verb == "する" or verb == "れる" or verb == "る": continue
            for noun in self.nouns:
                if (len(noun) == 1 and re.match("^{}$".format(hiragana), noun)): continue
                if (len(verb) > len(noun) and
                    noun == verb[0:len(noun)] and
                    verb[len(noun):] in self.verbs):
                    self.multiverbs.add(verb)
                    self.nounverbs.add(verb)
                    self.lemma_ab[verb] = self.find_morpheme_fragments(verb, len(noun))
                    break

        self.nounverbs &= self.lemmaverbs
        print ("Multiverbs extracted using the noun+verb method:", len(self.nounverbs & self.lemmaverbs))

        self.multiverbs &= self.lemmaverbs

        print ("Total multiverb count:", len(self.multiverbs & self.lemmaverbs))

        self.singleverbs = set(verb for verb in self.verbs if (verb not in self.multiverbs and verb not in self.extended_verbs and verb in self.lemmaverbs))
        print ("Total singleverb count:", len(self.singleverbs))


    def pickle_multiverbs(self):
        with open("multiverbs.pickle", "wb") as f:
            pickle.dump(self.lemma_ab, f, pickle.HIGHEST_PROTOCOL)


    def write_list(self, list, name="multiverbs.txt"):
        with open(name, 'w') as file:
            for verb in list:
                file.write(verb + "\n")

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error as msg:
             raise Usage(msg)
        # more code, unchanged
        if len(args) != 1:
            mvg = MultiverbGenerator()
            mvg.write_list(sorted(mvg.renyou_verbs), "renyouverbs.txt")
            mvg.write_list(sorted(mvg.multiverbs), "multiverbs.txt")
            mvg.write_list(sorted(mvg.singleverbs), "singleverbs.txt")
            mvg.write_list(sorted(mvg.nounverbs), "nounverbs.txt")
            mvg.pickle_multiverbs()
        else:
            mvg = MultiverbGenerator(args[0])
            mvg.pickle_multiverbs()
    except Usage as err:
        print (err.msg)
        print ("for help use --help")
        return 2
if __name__ == "__main__":
    sys.exit(main())

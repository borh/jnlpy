#!/usr/bin/python3
import os
import shelve
import time

from multiprocessing import Pool
from collections import defaultdict

#from bccwjsources import BCCWJSources
from statemachine import MorphemeMatcher
from modalitydefinitions import adverb_list, modality_list
#from linguisticstructures import DirectedCollocation
from customcounters import GoshuCounter
from customcounters import BinCounter
from customcounters import WritingSystemCounter
from customcounters import POSCounter
from customcounters import TypeCounter
from customcounters import TokenCounter
from customcounters import GenericCounter

adverb_matcher = MorphemeMatcher(adverb_list)
modality_matcher = MorphemeMatcher(modality_list)

#sources = BCCWJSources()
#for item in sources.query_many(["author", "publisher", "sample_id", "genre_1", "genre_2", "genre_3", "genre_4"]):
#    print(item)


class FileStatistics(object):

    __slots__ = ["name", "goshu", "writing_system", "pos", "types", "tokens", "adverbs", "modality", "adverb_modality", "adverb_modality_distance", "sentence_length", "sbins_advmod_dist", "kratki", "dolgi"]

    def __init__(self, file):
        self.name = file.name
        self.goshu = GoshuCounter()
        self.writing_system = WritingSystemCounter()
        self.pos = POSCounter()
        self.types = TypeCounter()
        self.tokens = TokenCounter()
        self.adverbs = GenericCounter()
        self.modality = GenericCounter()
        self.adverb_modality = GenericCounter()
        self.adverb_modality_distance = defaultdict(list)
        self.sentence_length = defaultdict(list)
        self.sbins_advmod_dist = BinCounter()
        lengths = list()


        self.kratki = []
        self.dolgi = []

        # need to make this multiprocess compatible
        #for row in sources.query_many(["author", "publisher", "sample_id", "genre_1", "genre_2", "genre_3", "genre_4"], "sources.sample_id=\"%s\"" % (self.name)):
        #    print(row)

        for sentence in file.to_sentences():

            lengths.append(len(sentence))

            for morpheme in sentence:
                self.update_morpheme_statistics(morpheme)

            adverb_matches = adverb_matcher.match(sentence)
            for match in adverb_matches:
                self.adverbs[match[0]] += 1
            modality_matches = modality_matcher.match(sentence)
            for match in modality_matches:
                self.modality[match[0]] += 1
            if len(modality_matches) > 0 and len(adverb_matches) > 0:
                for (adverb, adverb_end_index, adverb_start_index) in adverb_matches:
                    for (modality, modality_end_index, modality_start_index) in modality_matches:
                        if modality_start_index > adverb_end_index:
                            #iprint (adverb, modality, modality_start_index - adverb_end_index - 1, " ".join("{}{}".format(i, m.orth) for i, m in enumerate(sentence)))
                            self.adverb_modality_distance[adverb + "-" + modality].append(modality_start_index - adverb_end_index - 1) # indexes point to the beginning of an expression
                            self.adverb_modality[adverb + "-" + modality] += 1
                            self.sbins_advmod_dist[int(len(sentence)/5)][adverb + "-" + modality].append(modality_start_index - adverb_end_index - 1)
                            if modality_start_index - adverb_end_index - 1 < 10:
                                self.kratki.append("".join(m.orth for m in sentence) + "({},{}, dist={})".format(adverb, modality, modality_start_index - adverb_end_index - 1))
                            elif modality_start_index - adverb_end_index - 1 > 20:
                                self.dolgi.append("".join(m.orth for m in sentence) + "({},{}, dist={})".format(adverb, modality, modality_start_index - adverb_end_index - 1))
                            break
        self.sentence_length["文の長さ(形態素)"] = lengths


    def update_morpheme_statistics(self, morpheme):
        self.goshu.update(morpheme)
        self.writing_system.update(morpheme)
        self.pos.update(morpheme)
        self.types.update(morpheme)
        self.tokens.update(morpheme)


    def __str__(self):
        output = []
        output.append(str(self.goshu))
        output.append(str(self.writing_system))
        output.append(str(self.pos))
        output.append(str(self.types))
        output.append(str(self.tokens))
        output.append(str(len(self.adverbs)))
        output.append(str(len(self.modality)))
        output.append(str(len(self.adverb_modality)))
        output.append(str(len(self.adverb_modality_distance)))
        return "\n".join(output)


def compute(file):
    return FileStatistics(file)


class CorpusStatistics(object):

    def __init__(self, corpus):
        #self.statistics_by_file = defaultdict(FileStatistics)
        self.name = corpus.name
        self.goshu = GoshuCounter()
        self.writing_system = WritingSystemCounter()
        self.pos = POSCounter()
        self.types = TypeCounter()
        self.tokens = TokenCounter()
        self.adverbs = GenericCounter()
        self.modality = GenericCounter()
        self.adverb_modality = GenericCounter()
        self.adverb_modality_distance = defaultdict(list)
        self.sentence_length = defaultdict(list)
        self.sbins_advmod_dist = BinCounter()
        self.kratki = []
        self.dolgi = []
        self.goshu_db = shelve.open("tmp/{}-{}.db".format(self.name, "goshu"), protocol=3)
        self.writing_system_db = shelve.open("tmp/{}-{}.db".format(self.name, "writing_system"), protocol=3)
        self.pos_db = shelve.open("tmp/{}-{}.db".format(self.name, "pos"), protocol=3)
        self.tokens_db = shelve.open("tmp/{}-{}.db".format(self.name, "tokens"), protocol=3)
        #self.types_db = shelve.open("{}-{}.db".format(self.name, "types"), protocol=3)
        self.adverbs_db = shelve.open("tmp/{}-{}.db".format(self.name, "adverbs"), protocol=3)
        self.modality_db = shelve.open("tmp/{}-{}.db".format(self.name, "modality"), protocol=3)
        self.adverb_modality_db = shelve.open("tmp/{}-{}.db".format(self.name, "adverb-modality"), protocol=3)
        self.adverb_modality_distance_db = shelve.open("tmp/{}-{}.db".format(self.name, "adverb-modality-distance"), protocol=3)
        self.sentence_length_db = shelve.open("tmp/{}-{}.db".format(self.name, "sentence-length"), protocol=3)
        self.sbins_advmod_dist_db = shelve.open("tmp/{}-{}.db".format(self.name, "sbins_advmod_dist"), protocol=3)

        for data_type in ["goshu", "writing-system", "pos", "types", "adverbs", "modality", "adverbs-modality", "adverb-modality-distance", "sentence-length", "sbins_advmod_dist"]:
            try:
                print("deleting", "{}-{}.tsv".format(self.name, data_type))
                os.remove("{}-{}.tsv".format(self.name, data_type))
            except:
                pass

        self.compute_statistics(corpus)
        ##for file in corpus:
        ##    self.statistics_by_file[file.name] = FileStatistics(file, adverb_matcher, modality_matcher)


    def __str__(self):
        output = []
        for file, statistics in self.statistics_by_file:
            output.append("Statistics for file {}:\n{}".format(file.name, statistics))
        return "\n".join(output)


    def compute_statistics(self, corpus):
        print("starting", corpus.name)
        #i = 0
        last_time = time.time()
        pool = Pool()
        for i, stat in enumerate(pool.imap(compute, corpus, 100)):
            if i % 100 == 0:
                curr_time = time.time()
                print(i, curr_time - last_time) # dumb progress counter
                last_time = curr_time
            self.merge_data(stat) # accumulate data for corpus-level statistics, below is for files

            # normalize with tokens or (if full token representation (pos, goshu etc.)), divide by rowsums
            self.goshu_db[stat.name] = stat.goshu.normalize_self()
            self.writing_system_db[stat.name] = stat.writing_system.normalize_self()
            self.pos_db[stat.name] = stat.pos.normalize_self()
            #self.types_db[stat.name] = stat.types
            # check if not normalizing fixes our problem
            self.adverbs_db[stat.name] = stat.adverbs.normalize_by_n(stat.tokens.tokens)
            self.modality_db[stat.name] = stat.modality.normalize_by_n(stat.tokens.tokens)
            self.adverb_modality_db[stat.name] = stat.adverb_modality.normalize_by_n(stat.tokens.tokens)
            self.adverb_modality_distance_db[stat.name] = stat.adverb_modality_distance
            self.sentence_length_db[stat.name] = stat.sentence_length

            self.kratki.extend(stat.kratki)
            self.dolgi.extend(stat.dolgi)
            #print("finished", corpus.name)
        #normalized_distance = GenericCounter()
        #for colloc, freq in stat.adverb_modality.items():
        #    normalized_distance[colloc] = stat.adverb_modality_distance[colloc] / freq
        #    print (stat.adverb_modality_distance[colloc], freq, stat.adverb_modality_distance[colloc] / freq)
        #self.adverb_modality_distance_db[stat.name] = normalized_distance


    def merge_data(self, stat):
        self.goshu.add(         stat.goshu)
        self.writing_system.add(stat.writing_system)
        self.pos.add(           stat.pos)
        self.types.add(         stat.types)
        self.tokens.tokens   += stat.tokens.tokens
        self.adverbs.add(       stat.adverbs)
        self.modality.add(      stat.modality)
        self.adverb_modality.add(stat.adverb_modality)
        self.sbins_advmod_dist.add(stat.sbins_advmod_dist)
        for (colloc, distances) in stat.adverb_modality_distance.items():
            self.adverb_modality_distance[colloc].extend(distances)
        self.sentence_length["文の長さ(形態素)"].extend(stat.sentence_length["文の長さ(形態素)"])
        #for a, b in stat.adverb_modality.items():
        #    self.adverb_modality += stat.adverb_modality


    def normalize(self):
        n = self.tokens.tokens
        n /= 1000000
        print("normalizing with", n)
        self.goshu.normalize_self()
        self.writing_system.normalize_self()
        self.pos.normalize_self()

        self.types.normalize_by_n(n)
        # keep getting strange data with this, maybe better to not normalize?
        self.adverbs.normalize_by_n(n)
        self.modality.normalize_by_n(n)
        self.adverb_modality.normalize_by_n(n)

        #distance_accu = defaultdict(GenericCounter)
        #for (colloc, distances) in self.adverb_modality_distance.items():
        #    distance_accu[colloc] = sum(distances) / len(distances)
        #self.adverb_modality_distance = distance_accu

        print("normalized")


    def clean(self):
        for type in ["goshu", "writing_system", "pos", "types", "adverbs", "modality", "adverb-modality", "adverb-modality-distance", "sentence-length", "sbins_advmod_dist"]:
            try:
                os.remove("tmp/{}-{}.db".format(self.name, type))
            except:
                print("Couldn't delete database:", "tmp/{}-{}.db".format(self.name, type))


#if __name__ == "__main__":
#    sys.exit(main())

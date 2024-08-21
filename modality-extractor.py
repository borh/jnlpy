#!/usr/bin/python3
import sys
import os
import uuid
import pickle

from collections import defaultdict

from corpusstatistics import CorpusStatistics

from corpora import Corpora
from customcounters import GenericCounter
from customcounters import BinCounter
from tsvstatistics import write_tsv, extract_columns
from tsvstatistics import bin2tsv

def main():
    if len(sys.argv) < 2:
        raise Exception("please specify directory or files as input")

    directories = sys.argv[1:]

    corpora = Corpora(directories)

    #adverb_mm = MorphemeMatcher(adverb_list)
    #modality_mm = MorphemeMatcher(modality_list)
    goshu = defaultdict(GenericCounter)
    writing_system = defaultdict(GenericCounter)
    pos = defaultdict(GenericCounter)
    types = defaultdict(GenericCounter)
    tokens = GenericCounter()
    adverbs = defaultdict(GenericCounter)
    modality = defaultdict(GenericCounter)
    adverb_modality = defaultdict(GenericCounter)
    adverb_modality_distance = defaultdict(GenericCounter)
    sbins_advmod_dist = defaultdict(BinCounter)
    sentence_length = dict()
    dolgi = defaultdict(list)
    kratki = defaultdict(list)
    pickle_store = {}
    for corpus in corpora:
        pickle_store[corpus.name] = "tmp/{}.pickle".format(str(uuid.uuid4()))
        stat = CorpusStatistics(corpus)
        print("merging statistics for", corpus.name)
        print("done merging statistics for", corpus.name)
        print("normalizing statistics for", corpus.name)
        stat.normalize()
        print("done normalizing statistics for", corpus.name)
        pickle_data = {}
        pickle_data["goshu"] = stat.goshu
        pickle_data["writing_system"] = stat.writing_system
        pickle_data["pos"] = stat.pos
        pickle_data["types"] = stat.types
        pickle_data["tokens"] = stat.tokens.tokens
        pickle_data["adverbs"] = stat.adverbs
        pickle_data["modality"] = stat.modality
        pickle_data["adverb_modality"] = stat.adverb_modality
        pickle_data["sbins_advmod_dist"] = stat.sbins_advmod_dist

        kratki[corpus.name].extend(stat.kratki)
        dolgi[corpus.name].extend(stat.dolgi)

        distance_accu = defaultdict(GenericCounter)
        #print (stat.adverb_modality_distance_db)
        for (filename, counter) in stat.adverb_modality_distance_db.items():
            for (colloc, distances) in counter.items():
                #print (colloc, distances)
                #print (len(distances))
                #print (sum(distances))
                distance_accu[filename][colloc] = sum(distances) / len(distances)
        #print (distance_accu)
        #print (stat.modality_db)
        pickle_data["adverb_modality_distance"] = stat.adverb_modality_distance

        length_accu = defaultdict(GenericCounter)
        for filename, length_list in stat.sentence_length_db.items():
            if len(length_list['文の長さ(形態素)']) == 0:
                length_accu[filename]['文の長さ(形態素)'] = 0.0
            else:
                length_accu[filename]['文の長さ(形態素)'] = sum(length_list['文の長さ(形態素)']) / len(length_list['文の長さ(形態素)'])
        pickle_data["sentence-length"] = length_accu

        #goshu[corpus.name] = stat.goshu.goshu
        #writing_system[corpus.name] = stat.writing_system.system
        #pos[corpus.name] = stat.pos.pos
        #types[corpus.name] = stat.types.types
        #tokens[corpus.name] = stat.tokens.tokens
        #adverbs[corpus.name] = stat.adverbs
        #modality[corpus.name] = stat.modality
        #for adv in stat.adverb_modality:
        #    for mod in stat.adverb_modality[adv]:
        #        pickle_data["adverb_modality"][adv + "-" + mod] += stat.adverb_modality[adv][mod]
        #        #adverb_modality[corpus.name][adv + "-" + mod] += stat.adverb_modality.data[adv][mod]
        write_tsv(stat.goshu_db, extract_columns(stat.goshu_db), "{}-{}.tsv".format(corpus.name, "goshu"))
        write_tsv(stat.writing_system_db, extract_columns(stat.writing_system_db), "{}-{}.tsv".format(corpus.name, "writing_system"))
        write_tsv(stat.pos_db, extract_columns(stat.pos_db), "{}-{}.tsv".format(corpus.name, "pos"))
        #write_tsv(stat.types_db, extract_columns(stat.types_db), "{}-{}.tsv".format(corpus.name, "types"))
        write_tsv(stat.adverbs_db, extract_columns(stat.adverbs_db), "{}-{}.tsv".format(corpus.name, "adverbs"))
        write_tsv(stat.modality_db, extract_columns(stat.modality_db), "{}-{}.tsv".format(corpus.name, "modality"))
        #print (stat.adverb_modality_db)
        write_tsv(stat.adverb_modality_db, extract_columns(stat.adverb_modality_db), "{}-{}.tsv".format(corpus.name, "adverb-modality"))
        write_tsv(distance_accu, extract_columns(distance_accu), "{}-{}.tsv".format(corpus.name, "adverb-modality-distance"), na="NA")
        write_tsv(length_accu, extract_columns(length_accu), "{}-{}.tsv".format(corpus.name, "sentence-length"), na="0.0")
        print (stat.sbins_advmod_dist)
        bin2tsv(stat.sbins_advmod_dist, "{}-{}.tsv".format(corpus.name, "sbins_advmod_dist"))
        #write_tsv(pickle_data["adverb_modality"], extract_columns(pickle_data["adverb_modality"]), "{}-{}.tsv".format(corpus.name, "adverb-modality"))
        with open(pickle_store[corpus.name], "wb") as f:
            pickle.dump(pickle_data, f, pickle.HIGHEST_PROTOCOL)
        stat.clean()

    for corpus in pickle_store:
        with open(pickle_store[corpus], "rb") as f:
            print("restoring data for", corpus)
            restored_data = pickle.load(f)

            goshu[corpus]           = restored_data["goshu"]
            writing_system[corpus]  = restored_data["writing_system"]
            pos[corpus]             = restored_data["pos"]
            types[corpus]           = restored_data["types"]
            tokens[corpus]          = restored_data["tokens"]
            adverbs[corpus]         = restored_data["adverbs"]
            modality[corpus]        = restored_data["modality"]
            adverb_modality[corpus] = restored_data["adverb_modality"]
            sbins_advmod_dist[corpus] = restored_data["sbins_advmod_dist"]
            temp = restored_data["adverb_modality_distance"]
            accu = GenericCounter()
            for (colloc, distances) in temp.items():
                accu[colloc] = sum(distances) / len(distances)
            adverb_modality_distance[corpus] = accu

            average = list()
            for filename, distances in restored_data["sentence-length"].items():
                average.append(distances['文の長さ(形態素)'])
            sl = dict()
            sl['文の長さ(形態素)'] = sum(average) / len(average)
            sentence_length[corpus] = sl
            print("restored data for", corpus)

        try: os.remove(pickle_store[corpus])
        except: raise Exception("couldn't delete pickle file:", pickle_store[corpus])

    write_tsv(goshu, extract_columns(goshu), "corpora-goshu.tsv")
    write_tsv(writing_system, extract_columns(writing_system), "corpora-writing.tsv")
    write_tsv(pos, extract_columns(pos), "corpora-pos.tsv")
    write_tsv(types, extract_columns(types), "corpora-types.tsv")
    for corpus_name, token_count in tokens.items():
        print("{}:\t{}".format(corpus_name, token_count))
    #write_tsv(tokens, ["frequency"], "corpora-tokens.tsv")
    write_tsv(adverbs, extract_columns(adverbs), "corpora-adverbs.tsv")
    write_tsv(modality, extract_columns(modality), "corpora-modality.tsv")
    write_tsv(adverb_modality, extract_columns(adverb_modality), "corpora-adverb-modality.tsv")
    write_tsv(adverb_modality_distance, extract_columns(adverb_modality_distance), "corpora-adverb-modality-distance.tsv", na="NA")
    write_tsv(sentence_length, extract_columns(sentence_length), "corpora-sentence-length.tsv", na="0.0")

    for corpus in kratki:
        with open("{}-kratki.txt".format(corpus), "w") as f:
            f.write("\n".join(kratki[corpus]))

    for corpus in dolgi:
        with open("{}-dolgi.txt".format(corpus), "w") as f:
            f.write("\n".join(dolgi[corpus]))

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3

import os
import sys
import pickle
import csv

from collections import defaultdict
#from multiprocessing import Pool

from customcounters import GenericCounter


class RegisterTable(object):
    def __init__(self):
        self.read_table()


    def read_table(self):
        self.table = defaultdict(list)
        self.index2corpus = {}
        self.corpus2index = {}
        with open("corpus-register-table-reduced.csv") as f:
            reader = csv.reader(f)
            self.categories = next(reader)
            self.subcategories = next(reader)
            self.possible_values = [set(values.split(",")) for values in next(reader)]
            for j, row in enumerate(reader):
                for i, item in enumerate(row):
                    category = self.categories[i] + "-" + self.subcategories[i]
                    if i > 0:
                        self.table[category].append(set(item.split(",")))
                    else:
                        self.index2corpus[j] = item
                        self.corpus2index[item] = j
        print (self.table)
        print ("index")
        print (self.index2corpus)


    def querry(self, column_match, value_match):
        # find subcorpora that match given column and value
        for i, row in enumerate(self.table[column_match]):
            if value_match in row:
                yield self.index2corpus[i]


    def register_distributions(self, dist):
        aregisters = {} # automatically constructed registers
        idcounter = 0
        self.id2register = {}
        for category, corpora in self.table.items():
            for items in corpora:
                for item in items:
                    if category + "-" + item not in aregisters:
                        aregisters[category + "-" + item] = idcounter
                        self.id2register[idcounter] = category + "-" + item
                        idcounter += 1
        with open("id2register.tsv", "w") as f:
            for id, register in self.id2register.items():
                f.write("%i\t%s\n" % (id, register))

        rv = RegisterDistributions()
        for a in aregisters:
            aggr = ListDictionary()
            for corpus, data in dist.items():
                if a.split("-")[-1] not in self.table["-".join(a.split("-")[0:2])][self.corpus2index[corpus]]:
                    print (a, "not in", self.table["-".join(a.split("-")[0:2])][self.corpus2index[corpus]])
                    continue
                for pos, data2 in data.items():
                    for word, freq in data2.items():
                        aggr[pos][word].append(freq)
                        #print (corpus, self.corpus2index[corpus], pos, word, freq)
            for pos, d in aggr.items():
                for word, freqs in d.items():
                    #print (freqs)
                    rv[str(aregisters[a])][pos][word] = sum(freqs) / len(freqs)

        return rv


class ListDictionary(dict):
    def __missing__(self, key):
        self[key] = rv = defaultdict(list)
        return rv

class RegisterDistributions(dict):
    def __missing__(self, key):
        self[key] = rv = defaultdict(GenericCounter)
        return rv


def aggregate(file):
    with open(file, "rb") as f:
        return pickle.load(f)

import math

#t_df = 2.94671 # t significance cutoff for 15 df.
t_df = 2.97684 # 14
t_df = 4.60409 # 14

def find_register_specific_words(rd):
    registers = rd.keys()
    poses = set()
    for register in registers:
        for pos, counter in rd[register].items():
            poses.add(pos)
    for pos in poses:
        with open(pos + "_distributions.tsv", "w") as f:
            #print ("POS: ", pos)
            words = set(w for w in rd[register][pos] for register in registers)
            for word in words:
                average = sum(rd[register][pos][word] or 0 for register in registers) / len(registers)
                std = math.sqrt((1/len(registers) * sum(math.pow(rd[register][pos][word] - average, 2) for register in registers)))
                t_scores = {}
                #chi_scores = {}
                #ronbun_score = rd["論文"][pos][word]
                for register in registers:
                    #t_scores[register] = (rd[register][pos][word] - ronbun_score) / (std / math.sqrt(len(registers)))
                    t_scores[register] = (rd[register][pos][word] - average) / (std / math.sqrt(len(registers)))
                    #chi_scores[register] = sum(math.pow(rd[register][pos][word] - average, 2) / average for register in registers)
                positive = set()
                negative = set()
                for register, t in t_scores.items():
                    if t > t_df:
                        positive.add(register)
                    elif math.fabs(t) > t_df:
                        negative.add(register)

                print (average, std, t_scores, word)
                print ("positive:", positive)
                print ("negative:", negative)
                f.write("{}\t{}\t{}\n".format(word, ", ".join(positive), ", ".join(negative)))
                #average = 0.0
                #zero_registers = set()
                #punique_registers = set()
                #nunique_registers = set()
                #unique_registers = set()
                #average_registers = set()
                #for register in registers:
                #    if word in rd[register][pos]:
                #        average += rd[register][pos][word]
                #    else: zero_registers.add(register)
                #average /= len(registers)
                #if len(registers - zero_registers) == 1:
                #    unique_registers = registers - zero_registers
                #else:
                #    for register in (registers - zero_registers):
                #        if abs(rd[register][pos][word] - average) / average > 2:
                #            if rd[register][pos][word] > average:
                #                punique_registers.add(register)
                #            else: nunique_registers.add(register)
                #        else: average_registers.add(register)
                #f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(word, ", ".join(unique_registers), ", ".join(punique_registers), ", ".join(average_registers), ", ".join(nunique_registers), ", ".join(zero_registers)))
                #print ("For word '{}'\tunique=[{}]\tpositive=[{}]\tnegative=[{}]\tzero=[{}]\taverage=[{}]".format(word, ", ".join(unique_registers), ", ".join(punique_registers), ", ".join(nunique_registers), ", ".join(zero_registers), ", ".join(average_registers)))


def write_pos_distributions(d, dirname=""):
    poslist = set()
    poswordlist = defaultdict(set)
    #print (d)
    for register, dist in d.items():
        for pos, counter in dist.items():
            poslist.add(pos)
            for word in counter:
                poswordlist[pos].add(word)
            #poswordlist[pos].add(word for word in counter)
    #print (poslist, poswordlist)

    for pos in poslist:
        print (pos)
        if pos == "Morphemes": continue # need more memory for this!
        with open(dirname + pos + "-clusterdata.tsv", "w") as f:
            f.write("\t".join(str(word) for word in poswordlist[pos]) + "\n")
            for register, dist in d.items():
                f.write(os.path.split(register)[1] + "\t" + "\t".join(str(dist[pos][word]) or "0" for word in poswordlist[pos]) + "\n")
                #for word in poswordlist[pos]:
                #    #for orthBase, freq in dist[pos].items():
                #    if word in dist[pos]:
                #        f.write(str(dist[pos][word]))


def normalize_dict(d, register_tokens):
    normal_distribution = defaultdict(GenericCounter)
    for pos, counter in d.items():
        for orthBase, freq in counter.items():
            normal_distribution[pos][orthBase] = freq / register_tokens * 1000000
    return normal_distribution


if __name__ == "__main__":
    #rt = RegisterTable()
    directories = sys.argv[1:]
    latextable = []
    if directories == None or directories == []:
        raise Exception("No directories specified!")
    else:
        #pool = Pool()
        rd = RegisterDistributions()
        for directory in directories:
            nrd = RegisterDistributions()
            directory = os.path.abspath(directory)
            file_accu = set()
            allowed_filetypes = set([".pickle"])
            for root, dirs, files in os.walk(directory):
                for file, extension in map(os.path.splitext, files):
                    if extension in allowed_filetypes:
                        file_accu.add(root + "/" + file + extension)
            register_distribution = defaultdict(GenericCounter)
            register_tokens = 0
            #for filedata in pool.imap(aggregate, file_accu, 500):
            for filedata in map(aggregate, file_accu):
                (distribution, tokens, basename) = filedata


                nrd[basename] = normalize_dict(distribution, tokens)

                register_tokens += tokens
                for pos, counter in distribution.items():
                    for orthBase, freq in counter.items():
                        register_distribution[pos][orthBase] += freq
            write_pos_distributions(nrd, dirname=os.path.split(directory)[-1]+"-")
            print ("data read in")
            normal_distribution = defaultdict(GenericCounter)
            for pos, counter in register_distribution.items():
                for orthBase, freq in counter.items():
                    normal_distribution[pos][orthBase] = freq / register_tokens * 1000000
            print ("corpus {} has {} tokens".format(directory, register_tokens))
            latextable.append((directory, register_tokens))
            print ("normalized")
            directory = os.path.split(directory)[1]
            rd[directory] = normal_distribution
        print ("Register / Corpus name & Tokens \\\\")
        for (name, tokens) in latextable:
            name = os.path.split(name)[1]
            print ("{} & {} \\\\".format(name, format(tokens, 'd')))
        #for register, distribution in rd.items():
        #    print (register)
        #    for pos, counter in distribution.items():
        #        print ("=" * 80)
        #        print ("POS: {} [{}]".format(pos, ", ".join("{}: {}".format(orthBase, freq) for (orthBase, freq) in counter.items())))
        #find_register_specific_words(rd)
        #print(rd)
        write_pos_distributions(rd)
        #find_register_specific_words(rt.register_distributions(rd))

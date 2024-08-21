#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from collections import setdefault

class ArrayDict(dict):
    def __missing__(self, key):
        self[key] = rv = ["", "", 0, 0, 0, dict()]
        return rv

class MultiverbTable(object):
    """Ouput table format:
    AB multiverb lemma as key to Python dictionary
    each value has the following list structure:
    0: A lemma
    1: B lemma
    2: AB frequency
    3: dictionary of surface forms with their frequency and sentence ids

    """

    __slots__ = ["data"]

    def __init__(self):
        #self.data = dict()
        self.data = ArrayDict()

    def update(self, a, b, sentence_id, ab=None, file_id=None, type=None):
        """update table with multiverb ab occuring in sentence_id"""
        ab_lemma = ""
        surface_form = ""
        # a and b only supplied with 2 morpheme multiverbs
        # unidic verbs have them set to None
        if ab != None:
            ab_lemma = ab.lemma
            surface_form = ab.orth
        elif a != None and b != None:
            ab_lemma = a.conjugate_base_to_renyou("lemma") + b.lemma
            surface_form = a.orth + b.orth
        else: raise Exception("a, b and ab all None")

        if surface_form in self.data[ab_lemma][5]:
            if file_id in self.data[ab_lemma][5][surface_form][1]:
                file_dict = self.data[ab_lemma][5][surface_form][1]
                file_dict[file_id] += [sentence_id]
                #print(file_dict)
                self.data[ab_lemma][5][surface_form] = (self.data[ab_lemma][5][surface_form][0] + 1, file_dict)
            else:
                file_dict = self.data[ab_lemma][5][surface_form][1]
                file_dict[file_id] = [sentence_id]
                self.data[ab_lemma][5][surface_form] = (self.data[ab_lemma][5][surface_form][0] + 1, file_dict)
                #self.data[ab_lemma][3][surface_form] = (self.data[ab_lemma][3][surface_form][0] + 1, {file_id: [sentence_id]})
        else:
            self.data[ab_lemma][5][surface_form] = (1, {file_id: [sentence_id]})

        if (self.data[ab_lemma][0] == "" and self.data[ab_lemma][1] == "") and (a != None and b != None):
            self.data[ab_lemma][0] = a.lemma
            self.data[ab_lemma][1] = b.lemma
        if type == "single":
            self.data[ab_lemma][2] += 1
        elif type == "multi":
            self.data[ab_lemma][3] += 1
        else:
            raise Exception("Undefined type:", type)
        self.data[ab_lemma][4] += 1
        #try:
        #    if surface_form in self.data[ab_lemma][3]:
        #        self.data[ab_lemma][3][surface_form] = (self.data[ab_lemma][3][surface_form][0] + 1, self.data[ab_lemma][3][surface_form][1] + [sentence_id])
        #    else:
        #        self.data[ab_lemma][3][surface_form] = (1, [sentence_id])
        #    self.data[ab_lemma][2] += 1
        #except KeyError:
        #    if a == None or b == None:
        #        self.data[ab_lemma] = ["", "", 1, {surface_form: (1, [sentence_id])}]
        #    else:
        #        self.data[ab_lemma] = [a.lemma, b.lemma, 1, {surface_form: (1, [sentence_id])}]

    def __str__(self):
        string_list = []
        for ab_lemma, info in self.data.items():
            #print (info)
            #print (" ".join(map(str, [" ".join(map(str, info[3][surface_form][1])) for surface_form in info[3]])))
            s = []
            for (surface_form, value) in info[5].items():
                l = []
                #print(value[1])
                for file_id in value[1]:
                    #print(file_id, sentences)
                    l.append("{}: ({})".format(file_id, ", ".join(str(sen) for sen in value[1][file_id])))
                s.append("{}: {} ({})".format(surface_form, value[0], ", ".join(l)))

            #s = ", ".join(["{}: {} ({})".format(surface_form, info[3][surface_form][0], " ".join(map(str, "{}: {}".format(file_id, sentences) for info[3][surface_form][1]))) for surface_form in info[3]])
            #s = ["{}: {} {}".format(surface_form, info[3][surface_form][0], " ".join(sentence for sentence in info[3][surface_form][1])) for surface_form in info[3]]
            #string_list.append("{}\t{}\t{}\t{}\t{}".format(ab_lemma, info[0], info[1], info[2], s))
            string_list.append("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(ab_lemma, info[0], info[1], info[2], info[3], info[4], ", ".join(s)))
        return "\n".join(string_list)

class CooccurenceTable(object):

    __slots__ = ["data"]

    def __init__(self):
        self.data = dict()

    def update(self, ab, a, b):
        if a == None and b == None: # unidic multiverb
            a = ""
            b = ""
        try:
            self.data[ab][2] += 1
        except KeyError:
            self.data[ab] = [a, b, 1]

        #try:
        #    self.data[a][(ab, b)] += 1
        #except KeyError:
        #    try:
        #        self.data[a][(ab, b)] = 1
        #    except KeyError:
        #        self.data[a] = {(ab, b): 1}

    def __str__(self):
        string_list = []
        for ab in self.data:
            string_list.append("{}\t{}\t{}\t{}".format(ab, self.data[ab][0], self.data[ab][1], self.data[ab][2]))
        return "\n".join(string_list)

    def multiverb_count(self, a, b):
        if a not in self.data and b not in self.data[a]: return None
        else: return self.data[a][b]

    def total_count(self, a):
        if a not in self.data: return None
        else: return sum(value for key in self.data[a] for value in key)

    def single_count(self, a):
        if a not in self.data and "" not in self.data[a]: return None
        else: return self.data[a][""]

    def other_count(self, a, b):
        if a not in self.data: return None
        else: sum(value for key in self.data[a] for value in key if key != b)

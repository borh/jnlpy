# -*- coding: utf-8 -*-
import re

class Morpheme(object):
    """instatiates an object of class Morpheme

    The Morpheme class requires a POSset equivalent to the one used in UniDic.
    If one is not used, conjugation will not work.
    """

    __slots__ = ["orth", "pron", "pronBase", "orthBase", "lemma", "pos", "pos1", "pos2", "pos3", "pos4", "cType", "cForm", "goshu", "position", "index"]
    #__slots__ = ["orth", "pos", "pos1", "pos2", "pos3", "pos4",
    #             "cType", "cForm", "lForm", "lemma", "pron", "kana",
    #             "goshu", "orthBase", "pronBase", "kanaBase", "formBase",
    #             "iType", "iForm", "iConType", "fType", "fForm", "fConType",
    #             "aType", "aConType", "aModType", "position", "index"]

    def __init__(self, mecab_line, position=0, index=0): # need to expand this to support all fields as in Unidic manual p. 14
        self.position = position
        self.index = index
        orth_features = mecab_line.split("\t")
        #print (orth_features)
        self.orth = orth_features[0]
        self.pron = orth_features[1]
        self.pronBase = orth_features[2]
        self.lemma = orth_features[3]
        self.orthBase = orth_features[4]
        self.pos = orth_features[5]
        pos_list = self.pos.split('-')
        self.pos1 = pos_list[0]
        self.pos2 = pos_list[1] if len(pos_list) > 1 else ''
        self.pos3 = pos_list[2] if len(pos_list) > 2 else ''
        self.pos4 = pos_list[3] if len(pos_list) > 3 else ''
        self.cType = orth_features[6] if orth_features[6] != '*' else ''
        self.cForm = orth_features[7] if orth_features[6] != '*' else ''
        self.goshu = orth_features[8]
        #if chasenFormatString == None: pass
        #featureList = chasenFormatString.split('\t')
        #self.orth  = featureList[0]
        #self.lForm = featureList[1] # 音声
        #self.lemma = featureList[2]
        #self.pos   = featureList[3]
        #self.cType = featureList[4] # 動詞の種類（5段など）
        #self.cForm = featureList[5] # 活用形
        #self.position = position
        #self.index = index


    #def __getstate__(self):
    #    return self.orth, self.pos1, self.pos2, self.pos3, self.pos4, self.cType, self.cForm, self.lForm, self.lemma, self.pron, self.kana, self.goshu, self.orthBase, self.pronBase, self.kanaBase, self.formBase, self.iType, self.iForm, self.fConType, self.aType, self.aConType, self.aModType, self.pos, self.position, self.index


    #def __setstate__(self, state):
    #    self.orth, self.lForm, self.lemma, self.pos, self.cType, self.cForm, self.position, self.index = state


    def __eq__(self, rhs):
        if not isinstance(rhs, Morpheme): return False
        if (self.orth == rhs.orth and
            self.lForm == rhs.lForm and
            self.lemma == rhs.lemma and
            self.pos == rhs.pos and
            self.cType == rhs.cType and
            self.cForm == rhs.cForm):
            return True
        else:
            return False


    def __str__(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.orth, self.pronBase, self.lemma, self.pos, self.cType, self.cForm, self.position, self.index)


    def __repr__(self):
        return "{}\t{}\t{}\t{}\t{}\t{}".format(self.orth, self.pronBase, self.lemma, self.pos, self.cType, self.cForm)


    def __add__(self, rhs):
        return Morpheme(self.orth + rhs.orth,
                        self.pronBase + rhs.pronBase,
                        self.pos + rhs.pos,
                        self.cType + rhs.cType,
                        self.cForm + rhs.cForm,
                        0,
                        0)


    def get_feature(self, feature):
        if feature == "orth": return self.orth
        elif feature == "lForm": return self.lFrom
        elif feature == "lemma": return self.lemma
        elif feature == "pos": return self.pos
        elif feature == "pos1": return self.pos1
        elif feature == "pos3": return self.pos3
        elif feature == "cType": return self.cType
        elif feature == "cForm": return self.cForm
        elif feature == "pron": return self.pron
        else: raise Exception("Invalid feature:", feature)


    def get_features(self, features):
        return "".join(self.get_feature(feature) for feature in features)

import re

from collections import defaultdict

class GenericCounter(dict):
    def __missing__(self, key):
        self[key] = rv = 0
        return rv


    def add(self, other):
        for key, value in other.items():
            self[key] += value


    def normalize_by_n(self, n):
        keys = sorted(self.keys())
        for key in keys:
            self[key] /= n
        return self


    def normalize_self(self):
        rowsum = sum(value for value in self.values())
        self.normalize_by_n(rowsum)
        return self


#from tokyo.cabinet import HDB, HDBOWRITER, HDBOCREAT, HDBOTRUNC
from tokyo.cabinet import HDB, HDBOWRITER, HDBOTRUNC, HDBTTCBS

class TokyoHashCounter(dict):
    __slots__ = ["_hdb"]
    def __init__(self, name, compression=False):
        self._hdb = HDB()
        if compression == False:
            self._hdb.tune(0, -1, -1, 0)
        else: self._hdb.tune(0, -1, -1, HDBTTCBS)
        self._hdb.setcache(0)
        self._hdb.setxmsiz(0)
        self._hdb.setdfunit(0)
        self._hdb.open("{}.tch".format(name), HDBOWRITER | HDBOTRUNC)

    def update(self, key, value):
        self._hdb[key.encode("utf-8")] = value.encode("utf-8")

    def add_one(self, key):
        self._hdb.addint(key.encode("utf-8"), 1)

    def __iter__(self):
        for key in self._hdb:
            yield (key.decode("utf-8"), int(self._hdb[key].encode("utf-8")))


    def __getitem__(self, key):
        try:
            return int(self._hdb[key].decode("utf-8"))
        except KeyError:
            return 0

    def __setitem__(self, key, value):
        self._hdb[key.encode("utf-8")] = value.encode("utf-8")



class BinCounter(dict):
    def __missing__(self, key):
        self[key] = rv = defaultdict(list)
        return rv


    def add(self, other):
        for bin, defdict in other.items():
            for comb, lst in defdict.items():
                self[bin][comb].extend(lst)


class GoshuCounter(GenericCounter):

    def update(self, morpheme):
        #if morpheme.goshu == "unknown": print(morpheme)
        self[morpheme.goshu] += 1

    #def __str__(self):
    #    return "\n".join("{}: {}".format(goshu, frequency) for (goshu, frequency) in self.data.items())


hiragana = re.compile("[\u3041-\u309F]")
katakana = re.compile("[\u30A0-\u30FF]")
kanji = re.compile("[\u4E00-\u9FFF]")

class WritingSystemCounter(GenericCounter):

    def update(self, morpheme):
        for char in morpheme.orth:
            self[self.get_system(char)] += 1


    def get_system(self, char):
        if hiragana.match(char):
            return "hiragana"
        elif katakana.match(char):
            return "katakana"
        elif kanji.match(char):
            return "kanji"
        else:
            return "romaji"


class TypeCounter(GenericCounter):

    def update(self, morpheme):
        self[morpheme.lemma] += 1


    def __str__(self):
        return "types: {}".format(len(self))


class TokenCounter(object):
    def __init__(self):
        self.tokens = 0


    def update(self, morpheme):
        self.tokens += 1


    def __str__(self):
        #return "tokens: {}".format(len(self.tokens))
        return "tokens: {}".format(self.tokens)


class POSCounter(GenericCounter):

    def update(self, morpheme):
        self[morpheme.pos1] += 1

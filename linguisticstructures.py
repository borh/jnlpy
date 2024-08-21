#from collections import Counter
from collections import defaultdict

from customcounters import GenericCounter

class UndirectedCollocation(object):
    def __init__(self):
        self.data = defaultdict(GenericCounter)


    def update(self, a, b):
        self.data[a][b] += 1
        if a != b: self.data[b][a] += 1

    def frequency(self, a, b):
        try:
            return self.data[a][b]
        except KeyError:
            try:
                return self.data[b][a]
            except KeyError:
                return 0


    def __iter__(self):
        for key1, value1 in self.data.items():
            for key2, value2 in value1.items():
                yield (key1, key2, value2)


    def __str__(self):
        histogram = []
        for a in self.data:
            for b in self.data[a]:
                histogram.append("%s\t%s\t%i" % (a, b, self.data[a][b]))
        return "\n".join(histogram)


class DirectedCollocation(dict):
    def __missing__(self, key):
        self[key] = rv = GenericCounter()
        return rv
    #self.data = defaultdict(GenericCounter)


    def __add__(self, other):
        result = DirectedCollocation()
        akeys = list(self.keys())
        for akey in akeys:
            bkeys = list(self[akey].keys())
            for bkey in bkeys:
                result[akey][bkey] += self[akey][bkey]
        akeys = list(other.keys())
        for akey in akeys:
            bkeys = list(other[akey].keys())
            for bkey in bkeys:
                result[akey][bkey] += other[akey][bkey]
        return result


    def normalize_by_n(self, n):
        akeys = list(self.keys())
        for akey in akeys:
            self[akey].normalize_by_n(n)
            #bkeys = list(self.data[akey].keys())
            #for bkey in bkeys:
            #    self.data[akey][bkey] /= n


    #def __iter__(self):
    #    for key1, value1 in self.data.items():
    #        for key2, value2 in value1.items():
    #            yield (key1, key2, value2)


    #def __str__(self):
    #    histogram = []
    #    for a in self.data:
    #        for b in self.data[a]:
    #            histogram.append("%s\t%s\t%i" % (a, b, self.data[a][b]))
    #    return "\n".join(histogram)

#!/usr/bin/env python3
UNIDIC_VERSION = "1312"
IPADIC_VERSION = "20070801"


class MetaPosSet(object):
    """instantiates a meta POS-set object capable of converting to and from
    differing POS-sets. Currently, only Ipadic and UniDic are supported.
    """
    def __init__(self):
        self._unidic = UnidicPosSet()
        self._ipadic = IpadicPosSet()


class UnidicPosSet(object):
    def __init__(self):
        self.read()

    def read(self):
        with open("unidic-{}-left-id.def".format(UNIDIC_VERSION)) as f:
            for line in f:
                despaced = line.rstrip().split(" ")
                print (" ".join(record for record in despaced[1].split(",")))

class IpadicPosSet(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    unidic = UnidicPosSet()

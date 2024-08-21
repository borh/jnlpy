# -*- coding: utf-8 -*-
import MeCab

from sentence import Sentence

class MecabWrapper(object):
    """Simple mecab conveniance wrapper.

    TODO: pyrex

    """

    __slots__ = ["parser"]


    def __init__(self, dicdir="/usr/lib64/mecab/dic/unidic", flags="-Ounidic"):#"-Ocsv"):
        self.parser = MeCab.Tagger ("-d %s %s" % (dicdir, flags))


    def parse(self, string, sentence_id=0):
        return Sentence(self.parser.parse(string).rstrip("\n").split("\n")[:-1], sentence_id)


    def parse_to_lines(self, string):
        return self.parser.parse(string).rstrip("\n").split("\n")

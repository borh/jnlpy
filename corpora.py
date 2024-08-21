import os
import re

from corpus import Corpus

class Corpora(object):

    def __init__(self, corpora):
        if corpora == None:
            raise Exception("cannot instantiate Corpora class: 'corpora' not defined")

        corpora = [directory[:-1] if re.match("/$", directory) else directory for directory in corpora]

        for directory in corpora:
            if not os.path.isdir(directory):
                raise Exception("'{}' is not a directory".format(directory))

        self.corpora = [Corpus(directory=directory) for directory in corpora]


    def __iter__(self):
        for corpus in self.corpora:
            yield corpus

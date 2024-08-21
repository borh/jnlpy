import os
import sqlite3
from collections import defaultdict

# need to fix mecab for python 3.2
#from mecabwrapper import MecabWrapper
from sentence import Sentence

class CorpusFile(object):

    __slots__ = ["basename", "name", "types"]

    def __init__(self, basename, extensions):
        self.basename = basename
        self.name = basename.split("/")[-1]
        self.types = set(extensions)
        #print("CorpusFile initialized with", self.basename, self.types)


    def __iter__(self):
        if ".unidic" in self.types:
            with open(self.basename + ".unidic", "r") as f:
                for line in f:
                    yield line.rstrip("\n")
        elif ".suw" in self.types:
            with open(self.basename + ".suw", "r") as f:
                for line in f:
                    yield line.rstrip("\n")
        elif ".luw" in self.types:
            with open(self.basename + ".luw", "r") as f:
                for line in f:
                    yield line.rstrip("\n")
        elif ".txt" in self.types:
            from mecabwrapper import MecabWrapper
            mecab = MecabWrapper()
            with open(self.basename + ".txt", "r", errors="ignore") as f:
                for line in f:
                    for parsed_line in mecab.parse_to_lines(line.rstrip("\n")):
                        yield parsed_line


    def to_sentences(self):
        sentence_id = 0
        buffer = []
        for line in self:
            if line == "EOS":
                yield Sentence(buffer, sentence_id)
                buffer = []
                sentence_id += 1
            else:
                buffer.append(line)


    def __repr__(self):
        return "[{}]".format(", ".join(self.basename + extension for extension in self.types))


class Corpus(object):

    def __init__(self, name=None, directory=None, files=None):
        if directory == None and files == None:
            raise Exception("cannot initialize Corpus class: one of 'directory' or 'files' must be specified")
        elif directory is not None and files is not None:
            raise Exception("cannot initialize Corpus class: both 'directory' and 'files' specified")
        elif directory is not None and not os.path.isdir(directory):
            raise Exception("cannot initialize Corpus class: directory '{}' is not a directory".format(directory))

        self.directory = directory
        self.name = os.path.split(directory)[1]
        self.files = files
        self.read_metainfo(directory)
        self.name = self.genre[1]

    def read_metainfo(self, directory):
        corpus_dir = os.path.abspath(directory)
        try:
            with open(corpus_dir + "/" + "genres.def", "r") as f:
                for line in f:
                    self.genre = line.rstrip().split("\t")
                    break
        except IOError:
            print("Genre info file not found:", corpus_dir + "/" + "genres.def, defaulting to directory name")
            self.genre = [0, self.name]
        try:
            with open(corpus_dir + "/" + "sources.def", "r") as f:
                self.connection = sqlite3.connect(":memory:")
                c = self.connection.cursor()
                c.execute("""CREATE TABLE sources (
                         source_id INTEGER PRIMARY KEY ASC AUTOINCREMENT, -- maybe don't need the latter part?
                         title TEXT,
                         author TEXT,
                         year INTEGER,
                         reference_id TEXT,
                         genre_id INTEGER,
                         permission INTEGER
                         )""")

                i = 0
                for line in f:
                    sources_entry = line.rstrip("\n").split("\t")
                    sources_entry = sources_entry[:4] + [self.genre[0]] + [sources_entry[4]]
                    c.execute("INSERT INTO sources VALUES (?,?,?,?,?,?,?)", [i] + sources_entry)
                    i += 1
                #c.execute("SELECT * FROM sources")
                #for row in c:
                #    print(row)
        except IOError:
            print("Sources info file not found:", corpus_dir + "/" + "sources.def")


    def __iter__(self):
        if self.directory == None:
            for file in self.files:
                basename, extension = os.path.splitext(file)
                yield CorpusFile(basename, extension)
        else:
            directory = os.path.abspath(self.directory)
            file_dict = defaultdict(set)
            #allowed_filetypes = set([".txt", ".unidic", ".luw", ".cabocha", ".cabo"])
            allowed_filetypes = set([".unidic", ".luw"])
            for root, dirs, files in os.walk(directory):
                for file, extension in map(os.path.splitext, files):
                    if extension in allowed_filetypes:
                        file_dict[root + "/" + file].add(extension)
            for basename, extensions in file_dict.items():
                yield CorpusFile(basename, extensions)
            #self.contents = [CorpusFile(basename, extensions) for (basename, extensions) in file_dict.items()]
       #for file in self.contents:
       #     yield file


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            corpus = Corpus(directory=sys.argv[1])
        else:
            corpus = Corpus(files=[sys.argv[1]])
    elif len(sys.argv) > 2:
        corpus = Corpus(files=sys.argv[1:])
    else:
        raise Exception("please specify directory or files as input")

from morpheme_suw import Morpheme

class Sentence(object):

    __slots__ = ["sentence_id", "Morphemes"]

    def __init__(self, morpheme_list, sentence_id):
        self.sentence_id = sentence_id
        self.Morphemes = []
        position = 0
        for i in range(len(morpheme_list)):
            m = Morpheme(morpheme_list[i], position, i)
            position += len(m.orth)
            self.Morphemes.append(m)


    def __getstate__(self):
        return self.Morphemes, self.sentence_id


    def __setstate__(self, state):
        self.Morphemes, self.sentence_id = state


    def __iter__(self):
        for morpheme in self.Morphemes:
            yield morpheme


    def __eq__(self, rhs):
        if len(rhs.Morphemes) != len(self.Morphemes):
            return False
        elif self.Morphemes == rhs.Morphemes:
            return True
        else:
            return False


    def __str__(self):
        return "id={}\n{}".format(self.sentence_id, self.Morphemes)


    def __repr__(self):
        return str(self.Morphemes)


    def __getitem__(self, index):
        return self.Morphemes[index]


    def __len__(self):
        return len(self.Morphemes)

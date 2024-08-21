from morphemes import Morpheme

class Node(object):

    __slots__ = ["node_id", "kakari_id", "Morphemes"]


    def __init__(self, morpheme_list, start_position):
        header = morpheme_list[0].split(" ")
        self.node_id = header[1]
        self.kakari_id = header[2][:-1]
        self.Morphemes = []
        position = start_position
        morpheme_list = morpheme_list[1:]
        for i in range(len(morpheme_list)):
            m = Morpheme(morpheme_list[i], position, i)
            position += len(m.orth)
            self.Morphemes.append(m)


    def __getstate__(self):
        return self.Morphemes, self.node_id, self.kakari_id


    def __setstate__(self, state):
        self.Morphemes, self.node_id, self.kakari_id = state


    def __iter__(self):
        for morpheme in self.Morphemes:
            yield morpheme


    def __getitem__(self, index):
        return self.Morphemes[index]


    def __eq__(self, rhs):
        if len(rhs.Morphemes) != len(self.Morphemes):
            return False
        elif self.Morphemes == rhs.Morphemes:
            return True
        else:
            return False


    def __str__(self):
        return "{} {}\n{}".format(self.node_id, self.kakari_id, "\n".join(self.Morphemes))


    def __repr__(self):
        return str(self.Morphemes)

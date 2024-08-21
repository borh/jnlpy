#from cabochasentence import Sentence

class SentenceComplexity(object):

    def __init__(self, sentence):
        self.sentence = sentence


    def sentence_depth(self):
        depth_by_node = [0]
        level = 1
        for i in range(1, len(self.sentence)):
            depth_by_node.append(level)
            level += 1

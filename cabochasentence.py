from cabochanode import Node

# TODO: check which version is faster
#header_regex = re.compile("^\*[^\t]+")

class Sentence(object):

    __slots__ = ["sentence_id", "Nodes"]


    def __init__(self, node_list, sentence_id):
        self.sentence_id = sentence_id
        self.Nodes = []
        position = 0
        for i in range(len(node_list)):
            node_buffer = []
            if len(node_list.split(" ")) == 5:
                node_buffer.append(node_list[i])
                i += 1
            while i < len(node_list) and len(node_list[i].split(" ")) != 5:
                node_buffer.append(node_list[i])
                i += 1
            if len(node_buffer) != 0:
                node = Node(node_buffer, position)
                position = node.end_position
                self.Nodes.append(node)


    def __getstate__(self):
        return self.Nodes, self.sentence_id


    def __setstate__(self, state):
        self.Nodes, self.sentence_id = state


    def __iter__(self):
        for node in self.Nodes:
            yield node


    def __getitem__(self, index):
        return self.Nodes[index]


    def __eq__(self, rhs):
        if len(rhs.Nodes) != len(self.Nodes):
            return False
        elif self.Nodes == rhs.Nodes:
            return True
        else:
            return False


    def __str__(self):
        return "id={}\n{}".format(self.sentence_id, self.Nodes)


    def __repr__(self):
        return str(self.Nodes)

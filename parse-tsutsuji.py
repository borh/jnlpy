#!/usr/bin/env python3

from xml.etree.ElementTree import parse
from collections import defaultdict
#from xml.etree.ElementTree import dump

from graph.base import Graph


dotheader = """digraph test {
        //compound=true;
        //nodesep=0.05; //size=",4";
        //ordering=out;
        //ratio=compress;
        ranksep=0.75;
        node [shape=box];
"""

dotfooter = """
}
"""

class ExpressionClass(object):
    def __init__(self, expressions, leveldict, meaning, mclass, id):
        self.expressions = expressions
        self.leveldict = leveldict
        self.meaning = meaning
        self.mclass = mclass
        self.style = style
        self.uncommon = uncommon
        self.id = id


    def __str__(self):
        return "{}:{}:{}".format(self.mclass, self.meaning, ", ".join(exp for exp in self.expressions))


def find_similar1(mclass, id, expressions):
    for exp in expressions:
        if id != exp.id and mclass == exp.mclass:
            yield exp

def find_similar2(mclass, id, expressions):
    for exp in expressions:
        if id != exp.id and mclass != exp.mclass and mclass[0:2] == exp.mclass[0:2]:
            yield exp

def find_similar3(mclass, id, expressions):
    for exp in expressions:
        if id != exp.id and mclass[0] == exp.mclass[0] and mclass[1] != exp.mclass[1]:
            yield exp

def load_frequencies():
    with open("functional-expressions-11.tsv", "r") as f:
        firstline = True
        header = []
        frequencies = defaultdict(dict)
        for line in f:
            if firstline:
                header = line.rstrip().split("\t")
                firstline = False
            else:
                fields = line.rstrip().split("\t")
                for i, field in enumerate(fields[1:]):
                    frequencies[header[i]][fields[0]] = float(field)

        return frequencies


def clusterize(id, name, nodes, type="morph"):
    if type == "morph": type = "{}: morphological hierarchy".format(name)
    else: type = "{}: semantic hierarchy".format(name)
    return "subgraph cluster_{} {\nrank=same;\nlabel=\"{}\";\nfontsize=22;\n{}}}\n".format(id, type, nodes)

def connect_clusters(a, b, formatting=",headport=n,tailport=n,constraint=false"):
    return "{} -> {} [ltail=\"cluster_{}\",lhead=\"cluster_{}\"{}];\n".format(a, b, a, b, formatting)

def create_node(name, uid, freq, active=True, selected=False):
    color = ""
    if active: color = "black"
    else: color = "grey"
    if selected: color = "red"
    return "{} [label=\"{}\\n({:.2f})\",color={},fontcolor={}];\n".format(name + str(uid), name, float(freq), color, color)

def create_level_node(name, level):
    return "{}L{} [label=\"L{}\",shape=none,fontsize=20];\n".format(name, level, level)

def connect_nodes(a, b, formatting=" [arrowhead=none]"):
    return "{} -> {}{};\n".format(a, b, formatting)

def chain_nodes(name, levels):
    return " -> ".join("{}L{}".format(name, level) for level in range(1, levels + 1)) + " [color=white];\n"

def group(nodes):
    return "{{\n{}}}\n".format("".join(node for node in nodes))

def create_subgraph(name, mclass, meaning, nodes, type="morph"):
    if type == "morph": type = "{}: morphological hierarchy ({}-{})".format(name, mclass, meaning)
    else: type = "{}: semantic hierarchy".format(mclass)
    header = "subgraph cluster_{} {{\nrank=same;\nlabel=\"{}\";\n".format(name, type)
    footer = "}\n"
    return header + nodes + footer

def find_graph(headword, graph_list):
    for (graph, root, mclass, meaning) in graph_list:
        if root.spell.strip() == headword:
            return (graph, root, mclass, meaning)


def bottom_similarity(target_mclass, target_graph, graph_list):
    for (graph, root, mclass, meaning) in graph_list.items():
        if mclass == target_mclass and target_graph != graph:
            yield (graph, root, mclass, meaning)
# which is better?

def find_similar_graphs_1(graph_to_match, graph_list):
    (m_graph, m_root, m_mclass, m_meaning) = graph_to_match
    for (graph, root, mclass, meaning) in graph_list:
        if root.spell != m_root.spell and m_mclass == mclass:
            yield (graph, root, mclass, meaning)

def find_similar_graphs_2(graph_to_match, graph_list):
    (m_graph, m_root, m_mclass, m_meaning) = graph_to_match
    for (graph, root, mclass, meaning) in graph_list:
        if root.spell != m_root.spell and m_mclass != mclass and m_mclass[0:2] == mclass[0:2]:
            yield (graph, root, mclass, meaning)

def find_similar_graphs_3(graph_to_match, graph_list):
    (m_graph, m_root, m_mclass, m_meaning) = graph_to_match
    for (graph, root, mclass, meaning) in graph_list:
        if root.spell != m_root.spell and m_mclass[0] == mclass[0] and m_mclass[1] != mclass[1]:
            yield (graph, root, mclass, meaning)



def print_graphviz_graph(graph_data, corpus):
    (graph, root, mclass, meaning) = graph_data
    level_node_mapping = defaultdict(list)
    for node in graph.nodes:
        level_node_mapping[node.level].append(node)
    final_clusters = []
    final_node_connections = []
    selected = 0
    for level, level_nodes in level_node_mapping.items():
        level_label = create_level_node(root.spell, level)
        final_nodes = [level_label]
        final_nodes.extend([create_node(node.spell, node.name, node.frequencies[corpus] if corpus in node.frequencies else 0.0, True if (node.frequencies[corpus] if corpus in node.frequencies else 0) > 0 else False, selected) for node in level_nodes])
        for node in level_nodes:
            for outgoing_node in node.outgoing:
                final_node_connections.append(connect_nodes(node.spell + str(node.name), outgoing_node.end.spell + str(outgoing_node.end.name)))
        #final_node_connections.extend([connect_nodes(node.spell + str(node.name), outgoing.end.spell + str(outgoing.end.name), formatting="") for outgoing in node.outgoing for node in level_nodes])
        final_clusters.append(group(final_nodes))
    connect_levels = chain_nodes(root.spell, 9)
    nodes_text = "".join(cluster for cluster in final_clusters) + connect_levels + "".join(connection for connection in final_node_connections)
    print (create_subgraph(root.spell, mclass, meaning, nodes_text))

if __name__ == "__main__":
    ns = "{http://sslab.nuee.nagoya-u.ac.jp/~matuyosi/simpleXML}"
    tree = parse("tsutsuji1.1.xml")
    elem = tree.getroot()

    frequencies = load_frequencies()

    graph_list = []
    for level1 in tree.getiterator(ns + "L1"):
        mclass = ""
        meaning = ""
        G = Graph()
        node_levels = dict()
        nodes_info = dict()
        graph_nodes = dict()
        style = "normal"
        uncommon = 0
        previous_branching_level = 0
        for i, child in enumerate(level1.getiterator(), start=1):
            # record position of child node
            nodes_info[i] = (style, uncommon)
            current_level = int(child.tag.replace(ns, "")[1])
            node_levels[i] = current_level

            name = ""
            if "BASE" in child.attrib: name = child.attrib["BASE"].strip().replace(".", "")
            else: name = child.text.strip().replace(".", "")

            if current_level == 2:
                # mclass and meaning information appears at level 2
                mclass = child.attrib["MCLASS"].replace(".", "")
                meaning = child.attrib["MEANING"].replace(".", "")

            if current_level <= previous_branching_level:
                # find last known branching position
                j = i - 1
                while (j > 0 and node_levels[j] != current_level - 1):
                    j -= 1

                # replace inheritable attributes with last known good values
                if "STYLE" in child.attrib: style = child.attrib["STYLE"]
                else: style = nodes_info[j][0]
                if "UNCOMMON" in child.attrib: uncommon = int(child.attrib["UNCOMMON"])
                else: uncommon = nodes_info[j][1]

                graph_nodes[i] = G.add_node(spell=name, frequencies=frequencies[name], style=style, uncommon=uncommon, level=current_level, active=True)
                G.add_edge(graph_nodes[j], graph_nodes[i], is_directed=True)
                #print ("branching... making edge from {} to {}".format(graph_nodes[j], graph_nodes[i]))
            else:
                if "STYLE" in child.attrib: style = child.attrib["STYLE"]
                if "UNCOMMON" in child.attrib: uncommon = int(child.attrib["UNCOMMON"])

                if i > 1:
                    graph_nodes[i] = G.add_node(spell=name, frequencies=frequencies[name], style=style, uncommon=uncommon, level=current_level, active=False)
                    G.add_edge(graph_nodes[i - 1], graph_nodes[i], is_directed=True)
                    #print ("making edge from {} to {}".format(graph_nodes[i-1], graph_nodes[i]))
                else: # root node exception -> no edges
                    graph_nodes[i] = G.add_node(spell=name, frequencies=frequencies[name], style=style, uncommon=uncommon, level=current_level, active=True)

            previous_branching_level = current_level

        graph_list.append((G, graph_nodes[1], mclass, meaning))

    corpus = "Research Papers"
    phrase = "なければならない"
    print (dotheader)
    print_graphviz_graph(find_graph(phrase, graph_list), corpus)
    #for similar1_graph in find_similar_graphs_1(find_graph(phrase, graph_list), graph_list):
    #    print_graphviz_graph(similar1_graph, corpus)
    #for similar2_graph in find_similar_graphs_2(find_graph(phrase, graph_list), graph_list):
    #    print_graphviz_graph(similar2_graph, corpus)
    #for similar3_graph in find_similar_graphs_3(find_graph(phrase, graph_list), graph_list):
    #    print_graphviz_graph(similar3_graph, corpus)
    #print_graphviz_graph(find_graph("ために", graph_list), corpus)
    print (dotfooter)
    #for (graph, root, mclass, meaning) in graph_list:
    #    #print (graph)
    #    #for node in graph.depth_first_traversal(root):
    #    if root.spell.strip() != "からみると":
    #        continue
    #    level_node_mapping = defaultdict(list)
    #    for node in graph.nodes:
    #        level_node_mapping[node.level].append(node)
    #    final_clusters = []
    #    final_node_connections = []
    #    selected = 0
    #    for level, level_nodes in level_node_mapping.items():
    #        level_label = create_level_node(root.spell, level)
    #        final_nodes = [level_label]
    #        final_nodes.extend([create_node(node.spell, node.name, frequencies[node.spell]["Research paper: Chemistry"] if "Research paper: Chemistry" in frequencies[node.spell] else 0, True if (float(frequencies[node.spell]["Research paper: Chemistry"]) if "Research paper: Chemistry" in frequencies[node.spell] else 0) > 0 else False, selected) for node in level_nodes])
    #        for node in level_nodes:
    #            for outgoing_node in node.outgoing:
    #                final_node_connections.append(connect_nodes(node.spell + str(node.name), outgoing_node.end.spell + str(outgoing_node.end.name)))
    #        #final_node_connections.extend([connect_nodes(node.spell + str(node.name), outgoing.end.spell + str(outgoing.end.name), formatting="") for outgoing in node.outgoing for node in level_nodes])
    #        final_clusters.append(group(final_nodes))
    #    connect_levels = chain_nodes(root.spell, 9)
    #    nodes_text = "".join(cluster for cluster in final_clusters) + connect_levels + "".join(connection for connection in final_node_connections)
    #    print (dotheader + create_subgraph(root.spell, mclass, meaning, nodes_text) + dotfooter)

            #print (node)
            #print (frequencies[node.spell])
        #break # testing




    #with open("test.dot", "w") as f:
    #    exp = expressions[1]
    #    print (exp.leveldict)

    #    i = 0
    #    subgraphs1 = ""
    #    subgraphs1 += graphviz_subcluster(exp.expressions, frequencies, exp.mclass + "_" + exp.meaning)
    #    i += 1
    #    print (exp)
    #    for e in find_similar1(exp.mclass, exp.id, expressions):
    #        print (e)
    #        subgraphs1 += graphviz_subcluster(e.expressions, frequencies, e.mclass + "_" + e.meaning)
    #        i += 1

    #    connections = ""
    #    #for n in range(1, i):
    #    #    connections += "edge [lhead = \"cluster_{}\", ltail = \"cluster_{}\"];\n".format(n, n-1)

    #    subgraph_s1 = clusterize(subgraphs1, 0)

    #    connections += " -> ".join("cluster_" + str(n) for n in range(i)) + ";\n"
    #    f.write(dotheader + subgraph_s1 + connections + dotfooter)


    #for exp in expressions:
    #    print (exp, "is similar to")
    #    for sim in find_similar1(exp.mclass, exp.id, expressions):
    #        print (sim)
    #    print ("and less similar to")
    #    for sim in find_similar2(exp.mclass, exp.id, expressions):
    #        print (sim)
    #    print ("and even less similar to")
    #    for sim in find_similar3(exp.mclass, exp.id, expressions):
    #        print (sim)
    #    print ("=====")

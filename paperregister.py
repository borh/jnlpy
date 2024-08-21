#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs

from mecabwrapper import MecabWrapper

def read_dist():
    pos_list = [u"代名詞",
                u"副詞",
                u"助動詞",
                u"助詞",
                u"形容詞",
                u"形状詞",
                u"感動詞",
                u"接尾辞",
                u"接続詞",
                u"接頭辞",
                u"補助記号",
                u"記号",
                u"連体詞"]

    data = {}
    for pos in pos_list:
        data[pos] = {}
        with codecs.open(pos + "_distributions.tsv", encoding='utf-8', mode="r") as f:
            for line in f:
                fields = line.rstrip("\n").split("\t")
                data[pos][fields[0]] = fields[1:]
    return data


def tag_data(dist):
    otags = ""
    ctags = ""
    if dist[0] != "":
        otags += "<span class=\"unique\">" + "(%s)" % dist[0]
        ctags += "</span>"
    elif dist[1] != "":
        otags += "<span class=\"positive\">" + "(%s)" % dist[1]
        ctags += "</span>"
    elif dist[3] != "":
        otags += "<span class=\"negative\">" + "(%s)" % dist[3]
        ctags += "</span>"
    elif dist[4] != "":
        otags += "<span class=\"zero\">" + "(%s)" % dist[4]
        ctags += "</span>"

    return (otags, ctags)


def process(text):
    m = MecabWrapper()
    data = read_dist()
    output = ""
    for line in text:
        output += "<p />\n"
        for morpheme in m.parse(line):
            if morpheme.pos1 in data:
                if morpheme.orthBase in data[morpheme.pos1]:
                    otags, ctags = tag_data(data[morpheme.pos1][morpheme.orthBase])
                    output += otags + morpheme.orth + ctags #"(" + "), (".join(data[morpheme.pos1][morpheme.orthBase][0:1]) + ")",
            else:
                output += morpheme.orth
    return output

if __name__ == "__main__":
    import sys
    m = MecabWrapper()
    data = read_dist()
    for line in sys.stdin.readlines():
        print "<p />"
        for morpheme in m.parse(line):
            if morpheme.pos1 in data:
                if morpheme.orthBase in data[morpheme.pos1]:
                    otags, ctags = tag_data(data[morpheme.pos1][morpheme.orthBase])
                    print otags + morpheme.orth + ctags,#"(" + "), (".join(data[morpheme.pos1][morpheme.orthBase][0:1]) + ")",
            else:
                print morpheme.orth,

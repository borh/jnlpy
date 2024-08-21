#!/usr/bin/python3

from collections import defaultdict
from itertools import zip_longest

from lxml import etree
#from lxml import objectify

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

class ConnectIDtable(object):
    def __init__(self):
        with open("connectID", "r") as f:
            self._data = {}
            for line in f:
                (id, poslist) = line.strip().split("\t")
                self._data[id] = poslist.split(";")
            self.data = defaultdict(list)
            for id, pos in self._data.items():
                print (id, pos)
                #print (self.check(pos))
                if len(pos) == 1 and len(pos[0]) != 2:
                    #print (":", pos[0])
                    #print (id, pos)
                    self.data[id] = pos
                else:
                    #print(id, self.check(pos))
                    self.data[id] = self.check(pos)
                print ("->", id, self.data[id])
            #print (self.data)

    def check(self, pos):
        accu = []
        for p in pos:
            if p in self._data:
                #print (p, "not actual pos")
                accu.append(self._data[p][0])
            else: accu.append(p)
        #print (accu)
        return accu

ctable = ConnectIDtable()

class ConnectID(object):
    def __init__(self, id):
        self.id = id
        self.idlist = [str(g[0])+ str(g[1]) for g in grouper(2, self.id)]

    def __str__(self):
        #print (id for id in self.idlist)
        #print (ctable.data)
        #for id in self.idlist:
        #    if id == "90":
        #        print ("bogus matching, setting to all matches")
        #        return str(ctable.data[id])
        return "[" + ", ".join(str(ctable.data[id]) for id in self.idlist) + "]"

class TsutsujiExpression(object):
    def __init__(self, expression, meaning, right=None, left=None):
        self.expression = expression
        self.meaning = meaning
        self.right = ConnectID(right)
        self.left = left

    def __str__(self):
        #return "(\"{}\",\t\"{}\",\tright={}\tleft={})".format(self.expression.replace(".", ""), meaning, self.right, self.left)
        return "(\"{}\",\t\"{}\",\t{})".format(self.expression.replace(".", ""), meaning, self.right)

if __name__ == "__main__":
    #with open("tsutsuji1.1.xml", "r", encoding="euc-jp") as f:

    with open("tsutsuji1.1.xml", "r") as f:
        parser = etree.XMLParser(dtd_validation=False, ns_clean=True)
        tree   = etree.parse(f, parser)
        #print (etree.tostring(tree.getroot(), xml_declaration=False))
        print (tree.docinfo.encoding)
        xpath_meaning = etree.XPath('//*[@MEANING]')
        #xpath_meaning = etree.XPath('//*[@MEANING="適当"]')
        for match in xpath_meaning(tree):
            meaning = match.get("MEANING")
            print (meaning)
            right = match.find(".//*[@RIGHT]").get("RIGHT")
            left = None
            #left = match.find(".//*[@LEFT]").get("LEFT")
            for el in match.iter():
                #print (el.find(".//*[@RIGHT]"))
                #if right == None:
                #    r = el.find(".//*[@RIGHT]")
                #    if r != None:
                #        right = r.get("RIGHT")
                if el.tag == "{http://sslab.nuee.nagoya-u.ac.jp/~matuyosi/simpleXML}L9":
                    print (TsutsujiExpression(el.text.strip(), meaning, right, left))
            #for subel in el:
            #    print (subel)
        #print (xpath_meaning(tree))


        #tree = objectify.fromstring(f.read())
        #print (objectify.dump(tree))
        #find = objectify.ObjectPath
        #print(tree.getroot())
        #find = objectify.ObjectPath(".")
        #print (tree["{http://sslab.nuee.nagoya-u.ac.jp/~matuyosi/simpleXML}ENTRIES.L1"].tag)
        #print (find(tree).tag)
        #print (tree)
        #print(isinstance(tree.getroot(), objectify.ObjectifiedElement))

#!/usr/bin/python3

import csv
import re

from mecabwrapper import MecabWrapper

mw = MecabWrapper()

add_ikou   = re.compile("^う[とにも]")
add_itta   = re.compile("^た([となばらもすあ]|(っけ|って|かと|とこ|とた|うえ))")
add_itte   = re.compile("^て")
add_oyoide = re.compile("^で([な]|もち)")
add_oyoida = re.compile("^だ([となばらもすあ]|(っけ|って|かと|とこ|とた|うえ))")
add_iku    = re.compile("^まい")

def filter(s):
    if len(s) < 4: return s
    stem = s[0:2]
    rem = s[2:]
    if stem == "行こ": return rem
    if stem == "行っ" and rem[0:1] == "た": return rem
    if stem == "行っ" and rem[0:1] == "て": return rem
    if stem == "泳い" and rem[0:1] == "だ": return rem
    if stem == "泳い" and rem[0:1] == "で": return rem
    if stem == "行く": return rem
    if stem == "やっ": return rem

    #if stem == "行こ": return "V-HOR+" + rem
    #if stem == "行っ" and rem[0:1] == "た": return "V-PAST+" + rem[1:]
    #if stem == "行っ" and rem[0:1] == "て": return "V-te+" + rem[1:]
    #if stem == "泳い" and rem[0:1] == "だ": return "V-PAST+" + rem[1:]
    #if stem == "泳い" and rem[0:1] == "で": return "V-te+" + rem[1:]
    #if stem == "行く": return "V+" + rem
    #if stem == "やっ": return "V+" + rem

    return s

class TsutsujiExpression(object):
    def __init__(self, expression, meaning, style, right=None, left=None):
        self.expression = expression
        self.meaning = meaning
        self.right = right
        self.left = left
        self.style = style
        self.pos_matchings = self.process()

    def __str__(self):
        #return "(\"{}\",\t\"{}\",\tright={}\tleft={})".format(self.expression.replace(".", ""), meaning, self.right, self.left)
        if self.pos_matchings == None: return ""
        #return "tsutsuji_features.append((\"{}\",\t\t\t\t\"{}の機能表現\",\t[{}]))".format(self.expression, self.style, ", ".join(morpheme for morpheme in self.pos_matchings))
        return "tsutsuji_features.append((\"{}\",\t\t\t\t\"{}\",\t[{}]))".format(self.expression, filter(self.expression), ", ".join(morpheme for morpheme in self.pos_matchings))

    def process(self):
        if len(self.expression) <= 1:
            return None
        if add_ikou.match(self.expression): self.expression = "行こ" + self.expression
        elif add_itta.match(self.expression): self.expression = "行っ" + self.expression
        elif add_itte.match(self.expression): self.expression = "行っ" + self.expression
        elif add_oyoida.match(self.expression): self.expression = "泳い" + self.expression
        elif add_oyoide.match(self.expression): self.expression = "泳い" + self.expression
        elif add_iku.match(self.expression): self.expression = "行く" + self.expression
        elif self.expression[0:1] == "ち": self.expression = "やっ" + self.expression
        elif self.expression[0:1] == "ず": self.expression = "帰ら" + self.expression
        elif self.expression[0:3] == "ほかし": self.expression = "行く" + self.expression
        parsed = mw.parse(self.expression)
        accu = []
        for morpheme in parsed:
            if morpheme.pos1 == "助詞" or morpheme.pos1 == "助動詞":
                accu.append("[\"orth\"]")
                #accu.append("[\"orth\", \"pos1\"]")
            elif morpheme.pos1 == "接続詞":
                accu.append("[\"orth\"]")
            elif morpheme.pos1 == "動詞":
                if morpheme.orth[0:1] == "行" or morpheme.orth[0:1] == "泳" or (len(morpheme.orth) > 1 and morpheme.orth[0:2] == "やっ") or morpheme.orth[0:1] == "帰":
                    accu.append("[\"pos1\", \"cType\"]")
                else:
                    #accu.append("[\"lemma\", \"pos1\", \"cType\"]")
                    accu.append("[\"pron\", \"pos1\", \"cType\"]")
            else:
                accu.append("[\"lemma\", \"pos1\", \"pron\"]")
        return accu
        print (accu)

if __name__ == "__main__":
    meaning_id_map = {}
    with open("meaning_id_mappings.csv") as f:
        for row in csv.reader(f):
            meaning_id_map[row[0]] = row[1]
    with open("L8.list") as f:
        for fields in csv.reader(f):
            #print (fields)
            expression = fields[0]
            meaning_id = fields[3]
            style = fields[5]
            left_id = fields[6]
            right_id = fields[7]
            print (TsutsujiExpression(expression, meaning_id_map[meaning_id], style, right_id, left_id))

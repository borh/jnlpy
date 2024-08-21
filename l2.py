#!/usr/bin/python3

import csv
#import re

class TsutsujiExpression(object):
    def __init__(self, expression, meaning, right=None, left=None):
        self.expression = expression
        self.meaning = meaning
        self.right = right
        self.left = left

    def __str__(self):
        #return "(\"{}\",\t\"{}\",\tright={}\tleft={})".format(self.expression.replace(".", ""), meaning, self.right, self.left)
        return "{}\t{}".format(self.meaning, self.expression)

if __name__ == "__main__":
    meaning_id_map = {}
    with open("meaning_id_mappings.csv") as f:
        for row in csv.reader(f):
            meaning_id_map[row[0]] = row[1]
    all_expressions = []
    all_meanings = set()
    with open("L2.list") as f:
        for fields in csv.reader(f):
            #print (fields)
            expression = fields[0]
            meaning_id = fields[3]
            left_id = fields[6]
            right_id = fields[7]
            all_meanings.add(meaning_id_map[meaning_id])
            all_expressions.append(TsutsujiExpression(expression, meaning_id_map[meaning_id], right_id, left_id))
            #print (TsutsujiExpression(expression, meaning_id_map[meaning_id], right_id, left_id))
    for meaning in all_meanings:
        items = []
        for exp in all_expressions:
            if len(exp.expression) <= 1: continue
            if exp.meaning == meaning:
                items.append(exp.expression)
        print (meaning + " & " + "，".join(item for item in items) + "\\\\")


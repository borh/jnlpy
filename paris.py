#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import re
import os

hiragana = re.compile("[\u3041-\u309F]")
katakana = re.compile("[\u30A0-\u30FF]")
kanji = re.compile("[\u4E00-\u9FFF]")

def translate(string):
    counts = [0, 0, 0, 0, 0, 0]
    for char in string:
        if hiragana.match(char):
            #accu += "H"
            counts[0] += 1
        elif katakana.match(char):
            #accu += "K"
            counts[1] += 1
        elif kanji.match(char):
            #accu += "C"
            counts[2] += 1
        elif re.match("^[a-zA-Z]$", char):
            #accu += "R"
            counts[3] += 1
        elif re.match("^[0-9]$", char):
            counts[4] += 1
        else:
            #accu += "P"
            counts[5] += 1
    return counts

def main():
    if len(sys.argv) < 2:
        raise Exception("please specify directory or files as input")

    directories = sys.argv[1:]
    for directory in directories:
        directory = os.path.abspath(directory)
        file_dict = set()
        allowed_filetypes = set([".txt"])
        for root, dirs, files in os.walk(directory):
            for file, extension in map(os.path.splitext, files):
                if extension in allowed_filetypes:
                    file_dict.add(root + "/" + file + extension)
        for file in file_dict:
            with open(file, "r") as f:
                for line in f:
                    if len(line) > 50:
                        continue
                    counts = translate(line)
                    good_sentence = 1
                    for count in counts:
                        if count == 0:
                            good_sentence = 0
                    if good_sentence:
                        print (line)

if __name__ == "__main__":
    sys.exit(main())

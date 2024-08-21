#!/usr/bin/env python3

import sys
import os
import shutil

from collections import defaultdict

name_map = {"LB" : "書籍",
            "PB" : "書籍",
            "OB" : "書籍",
            "OW" : "白書",
            "OM" : "国会会議録",
            "PN" : "新聞",
            "PM" : "雑誌",
            "OT" : "検定教科書",
            "OY" : "Yahoo!ブログ",
            "OC" : "Yahoo!知恵袋"}

def read_db():
    basename_to_category = {}
    with open("Join_all.txt", "r") as f:
        for row in f:
            cells = row.split("\t")
            basename = cells[0]
            category = cells[11]
            basename_to_category[basename] = category
    return basename_to_category

basename_to_category = read_db()

def move_to_category(basename, extensions, outdir):
    #dir = os.path.dirname(basename)
    base = os.path.basename(basename)
    outbase = "{}/{}-{}".format(outdir, name_map[base[0:2]], basename_to_category[base])
    if not os.path.exists(outbase):
        os.makedirs(outbase)
    for ext in extensions:
        print("moving {}{} to {}".format(basename, ext, "{}/{}{}".format(outbase, base, ext)))
        shutil.copy(basename + ext, "{}/{}{}".format(outbase, base, ext))

if __name__ == "__main__":
    outdir = "registerCategories"
    directories = sys.argv[1:]
    if directories == None or directories == []:
        raise Exception("No directories specified!")
    else:
        for directory in directories:
            directory = os.path.abspath(directory)
            file_dict = defaultdict(set)
            allowed_filetypes = set([".txt", ".unidic", ".cabocha", ".cabo"])
            for root, dirs, files in os.walk(directory):
                for file, extension in map(os.path.splitext, files):
                    if extension in allowed_filetypes:
                        file_dict[root + "/" + file].add(extension)
            for basename, extensions in file_dict.items():
                move_to_category(basename, extensions, outdir)

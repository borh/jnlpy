#!/usr/bin/env python3

import re

from xml.etree.ElementTree import iterparse
#from collections import defaultdict
#from xml.etree.ElementTree import dump

from mecabwrapper import MecabWrapper

#allowed_pos = re.compile("(v|n|a|).*)")
reject_pos = re.compile(".*(xpression|(pre|suf)fix|particle).*")


def process(word):
    if len(word) == 0:
        return None
    return ["\"pos1\", \"pron\"]" for morpheme in word]

def jmdict_wordlist():
    mecab = MecabWrapper()

    curr_keb = set()
    curr_pos = ""
    curr_pos = set()
    d = list()
    #not_in_unidic = 0
    #in_unidic = 0
    #rejected_count = 0
    for (ev, el) in iterparse("JMdict_e"):
        #print (ev)
        #print (el)
        if el.tag == "entry" and ev == "end":
            if sum(1 for pos in curr_pos if reject_pos.match(pos)) == 0 and len(curr_keb) != 0:
                for ckeb in curr_keb:
                    #print (curr_pos)
                    morphemes = mecab.parse(ckeb)
                    if len(morphemes) > 1:
                        #print ("MM ", ckeb)
                        #print (morphemes)
                        #not_in_unidic += 1

                        skip = False
                        for i, morpheme in enumerate(morphemes):
                            if i != 0 and i != (len(morphemes) - 1) and morpheme.pos1 == "助詞" and re.match("^[がをへにのはてとでも]$", morpheme.orth):
                                skip = True
                                #print ("Reject: ", ckeb, curr_pos)
                                break
                            #elif morpheme.pos1 == "助詞":
                            #    if i < len(morphemes) - 1:
                            #        print ("Check: ", ckeb, curr_pos)
                            #        skip = True
                            #        break

                        if not skip:
                            if "".join(m.orth for m in morphemes) == "泣かされる":
                                print ("!!!!!!!泣かされる", morphemes, curr_pos)
                            if morphemes[-1].pos1 == "動詞" and morphemes[-1].cForm == "終止形-一般" and re.match(".*(noun|counter|numeric).*", " ".join(pos for pos in curr_pos), re.IGNORECASE):
                                continue
                            if morphemes[-1].pos1 == "助動詞" and (morphemes[-1].orth == "た" or morphemes[-1].orth == "だ"):
                                continue
                            all_verbs = all((m.pos1 == "動詞" or m.pos1 == "助動詞") for m in morphemes)
                            is_noun = any(re.match(".*(noun|counter|numeric).*", pos, re.IGNORECASE) for pos in curr_pos)
                            if is_noun and all_verbs and morphemes[-1].cForm == "終止形-一般":
                                curr_pos = set(["verb"])
                                print ("".join(m.orth for m in morphemes))
                            d.append((morphemes, curr_pos))
                            #print ("Probably OK: ", ckeb, curr_pos)
                    #else:
                    #    in_unidic += 1
            curr_keb = set()
            curr_pos = set()
        if el.tag == "keb":
            curr_keb.add(el.text)
        if el.tag == "pos":
            curr_pos.add(el.text)
    #print (d)
    #print (d[0])
    #print (len(d))
    #print ("Rejected:", rejected_count)
    #print ("In Unidic:", in_unidic)
    #print ("Not in Unidic:", not_in_unidic)
    return (d)

def write_flat_lemma_list(entries):
    with open("jmdict-lemma-list.txt", "w") as f:
        for (morphemes, pos) in entries:
            lemma = "".join(morpheme.lemma for morpheme in morphemes)
            f.write(lemma + "\n")


def read_flat_lemma_list():
    r = set()
    with open("jmdict-lemma-list.txt", "r") as f:
        for line in f:
            r.add(line.rstrip())
    return r

if __name__ == "__main__":
    #tree = parse("JMdict_e")
    #elem = tree.getroot()
    #print (elem)
    wordlist = jmdict_wordlist()
    write_flat_lemma_list(wordlist)

    with open("jmdictlist.py", "w") as f:
        f.write("jmdict_list = []\n")
        for (word, posset) in wordlist:
            orth = "".join(morpheme.orth for morpheme in word)
            #print (posset)

            pos = ""
            #print (word[-1].pos1, word[-1].cForm)
            for p in posset:
                #if not (word[-1].pos1 == "動詞" and word[-1].cForm == "終止形-一般") and re.match(".*(noun|counter|numeric).*", p, re.IGNORECASE):
                if re.match(".*(noun|counter|numeric).*", p, re.IGNORECASE):
                    pos = "名詞"
                    break
            else:
                for p in posset:
                    if re.match(".*adverb.*", p, re.IGNORECASE):
                        pos = "副詞"
                        break
                else:
                    for p in posset:
                        if re.match(".*verb.*", p, re.IGNORECASE):
                            pos = "動詞"
                            break
                    else:
                        for p in posset:
                            if re.match(".*adjective.*", p, re.IGNORECASE):
                                pos = "形容詞"
                                break
                        else:
                            for p in posset:
                                if re.match(".*conju.*", p, re.IGNORECASE):
                                    pos = "接続詞"
                                    break
                            else:
                                for p in posset:
                                    if re.match(".*interjection.*", p, re.IGNORECASE):
                                        pos = "感動詞"
                                        break
                                else:
                                    for p in posset:
                                        if re.match(".*auxiliary.*", p, re.IGNORECASE):
                                            pos = "助動詞"
                                            break
                                    else:
                                        for p in posset:
                                            if re.match(".*(pre|suf)fix.*", p, re.IGNORECASE):
                                                pos = "接辞"
                                                break
                                        else: raise Exception("unknown pos:", posset, word)
            #pos = word[-1].pos1
            #if pos == "代名詞":
            #    pos = "名詞"
            #elif pos == "補助記号":
            #    pos = "記号"
            #elif pos == "名詞" and word[-1].pos2 == "固有名詞":
            #    pos = "固有名詞"
            #elif pos == "接頭辞" or pos == "接尾辞":
            #    pos = "接辞"
            if pos == "名詞" or pos == "動詞":
                f.write("jmdict_list.append((\"{}\",\t\t\t\t\"{}\",\t[{}]))\n".format(orth, pos, ", ".join("[\"pos1\", \"lemma\"]" for morpheme in word)))
            elif pos == "形容詞" or pos == "副詞":
                f.write("jmdict_list.append((\"{}\",\t\t\t\t\"{}\",\t[{}]))\n".format(orth, pos, ", ".join("[\"pos1\", \"lemma\"]" if morpheme.pos1 != "助詞" else "[\"pron\"]" for morpheme in word[0:-1]) + ", [\"lemma\", \"cForm\"]"))
            else:
                f.write("jmdict_list.append((\"{}\",\t\t\t\t\"{}\",\t[{}]))\n".format(orth, pos, ", ".join("[\"pos1\", \"lemma\"]" if morpheme.pos1 != "助詞" else "[\"pron\"]" for morpheme in word)))

#!/usr/bin/env python3
#レコードＩＤ番号
#見出し番号
#レコード種別
#類
#部門
#中項目
#分類項目
#分類番号
#段落番号
#小段落番号
#語番号
#見出し
#見出し本体
#読み
#逆読み

from mecabwrapper import MecabWrapper

if __name__ == "__main__":
    mw = MecabWrapper()
    with open("bunruidb.txt", "r") as f:
        for line in f:
            fields = line.split(",")
            word = mw.parse(fields[12])
            if word[0].pos1 == "副詞":
                #if fields[3] == "体" and word[0].pos1 == "副詞":
                pos_matchings = []
                for morpheme in word:
                    pos_matchings.append("[\"lemma\", \"pos1\"]")
                print ("bunrui_features.append((\"{}\",\t\t\t\t\"{}\",\t[{}]))".format("".join(w.orth for w in word), "-".join(fl or "*" for fl in fields[4:6]), ", ".join(morpheme for morpheme in pos_matchings)))
            #print (fields)

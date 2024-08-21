adverb_list = []
#adverb_list.append(("あるいは",       "(Epistemic)あるいは", [["lemma"]]))
adverb_list.append(("案外",           "案外", [["lemma", "pos"]]))
adverb_list.append(("恐らく",         "(Epistemic)恐らく", [["lemma"]]))
adverb_list.append(("おおかた",       "おおかた", [["lemma"]]))
adverb_list.append(("必ず",           "(Epistemic/Deontic)必ず", [["lemma"]]))
adverb_list.append(("必ずしも",       "必ずしも", [["lemma"], ["lemma", "pos"]]))
adverb_list.append(("きっと",         "(Epistemic)きっと", [["lemma"]]))
adverb_list.append(("ことによると",   "ことによると", [["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
adverb_list.append(("によれば",       "(Evidential)〜によれば", [["lemma"], ["lemma"], ["lemma"]]))
adverb_list.append(("に従えば",       "(Evidential)〜に従えば", [["lemma"], ["lemma"], ["lemma"]]))
adverb_list.append(("さぞ",           "さぞ", [["lemma"]]))
adverb_list.append(("さぞかし",       "さぞ", [["lemma"]]))
adverb_list.append(("大概",           "大概", [["lemma", "pos"]]))
adverb_list.append(("大抵",           "大抵", [["lemma", "pos"]]))
adverb_list.append(("多分",           "(Epistemic)多分",   [["lemma"]])) # should really be able to specify more than one feature per morpheme
adverb_list.append(("どうも",         "(Evidential)どうも", [["lemma", "pos1"], ["lemma", "pos1"]]))
adverb_list.append(("どうやら",       "(Evidential)どうやら", [["lemma", "pos1"], ["lemma", "pos1"]]))
adverb_list.append(("どうしても",     "(Deontic/Boulomaic(+NEG))どうしても", [["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
adverb_list.append(("何とか",         "(Boulomaic)何とか", [["lemma"], ["lemma"], ["lemma"]]))
adverb_list.append(("ぜひ",           "(Boulomaic)ぜひ", [["lemma", "pos1"]]))
adverb_list.append(("なるべく",       "(Boulomaic)なるべく", [["lemma", "pos1"]]))
adverb_list.append(("もしかしたら",   "(Epistemic)もしかしたら", [["lemma"], ["lemma"], ["lemma"], ["lemma", "cForm"]]))
adverb_list.append(("もしかして",     "(Epistemic)もしかしたら", [["lemma"], ["lemma"], ["lemma"], ["lemma", "cForm"]]))
adverb_list.append(("ひょっとしたら", "(Epistemic)ひょっとしたら", [["lemma"], ["lemma"], ["lemma", "cForm"]]))
adverb_list.append(("よほど",         "よほど", [["lemma"]]))
adverb_list.append(("絶対",           "絶対", [["lemma"]]))
adverb_list.append(("絶対に",         "絶対に", [["lemma"], ["lemma"]]))
adverb_list.append(("さあ",           "(Inducement)さあ", [["lemma", "pos1"]]))
adverb_list.append(("はたして",       "(Interrogative)はたして", [["lemma", "pos1"]]))
adverb_list.append(("いったい",       "(Interrogative)いったい", [["lemma", "pos1"]]))
adverb_list.append(("もし",           "(Conditional)もし", [["lemma"]]))
adverb_list.append(("万一",           "(Conditional)万一", [["lemma"]]))
adverb_list.append(("仮に",           "(Conditional)仮に", [["lemma"], ["lemma"]]))
adverb_list.append(("たとえ",         "(Conditional)たとえ", [["lemma", "pos1"]]))
adverb_list.append(("どうぞ",         "(Request)どうぞ", [["lemma", "pos1"]]))
adverb_list.append(("どうか",         "(Request)どうか", [["lemma", "pos1"], ["pos1", "lemma"]]))
adverb_list.append(("なにぶん",       "(Request)なにぶん", [["lemma", "pos1", "pos3"]]))
modality_list = []
modality_list.append(("かもしれない",        "(Epistemic)かも知れない", [["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("かもしれません",      "(Epistemic)かも知れない", [["lemma"], ["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("かも",                "(Epistemic)かも知れない", [["lemma"], ["lemma"]]))
modality_list.append(("かな",                "かな",         [["lemma", "pos"], ["lemma", "pos"]]))
modality_list.append(("かしら",              "かしら",       [["lemma", "pos"]]))
modality_list.append(("ことではない",        "ことではない", [["lemma"], ["orth"], ["lemma"], ["lemma"]]))
modality_list.append(("ことじゃない",        "ことではない", [["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("でしょう",            "(Epistemic)だろう",       [["orth", "cType", "cForm"]]))
modality_list.append(("だろう",              "(Epistemic)だろう",       [["orth"]]))
modality_list.append(("であろう",            "(Epistemic)だろう",       [["orth"], ["orth", "lemma", "cType", "cForm"]]))
modality_list.append(("らしい",              "(Evidential)らしい",       [["lemma", "cType"]]))
modality_list.append(("いかざるをえない",    "(Deontic)ざるを得ない", [["pos"], ["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("いかざるをえません",  "(Deontic)ざるを得ない", [["pos"], ["lemma"], ["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("表しざるを得ない",    "(Deontic)ざるを得ない", [["pos"], ["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("表しざるを得ません",  "(Deontic)ざるを得ない", [["pos"], ["lemma"], ["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("行くそう",            "(Evidential)そうだ",       [["cForm"], ["lemma", "pos"]]))
modality_list.append(("だそうだ",            "(Evidential)そうだ",       [["lemma"], ["lemma", "pos"], ["lemma"]]))
modality_list.append(("わけだ",              "わけだ",       [["lemma"], ["orth"]]))
modality_list.append(("わけない",            "わけない",     [["lemma"], ["orth"]]))
modality_list.append(("と思う",              "と思う",       [["orth"], ["lemma"]]))
modality_list.append(("と思います",          "と思う",       [["orth"], ["lemma"], ["lemma"]]))
modality_list.append(("とは限らない",        "とは限らない", [["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("とは限りません",      "とは限らない", [["lemma"], ["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("のだ",                "のだ", [["lemma", "pos1"], ["orth", "lemma", "pos1"]]))
modality_list.append(("のです",              "のだ", [["lemma", "pos1"], ["lemma", "pos1", "orth"]]))
modality_list.append(("のである",            "のだ", [["lemma", "pos1"], ["lemma", "pos1"], ["lemma", "pos1"]]))
modality_list.append(("に違いない",          "(Epistemic)に違いない",   [["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("に違いありません",    "(Epistemic)に違いない",   [["lemma"], ["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("はずだ",              "(Epistemic)はずだ",       [["lemma"], ["lemma"]]))
modality_list.append(("はずです",            "(Epistemic)はずだ",       [["lemma"], ["lemma"]]))
modality_list.append(("はずない",            "(Epistemic)はずない",     [["lemma"], ["lemma"]]))
modality_list.append(("はずではありません",  "(Epistemic)はずない",     [["lemma"], ["lemma"], ["lemma"], ["lemma"], ["lemma"], ["lemma"]]))
modality_list.append(("べきだ",              "(Deontic)べきだ",       [["cType"], ["orth"]]))
modality_list.append(("べきではない",        "(Deontic)べきではない", [["cType"], ["orth"], ["lemma"], ["lemma"]]))
modality_list.append(("みたいだ",            "(Evidential)みたいだ",     [["lemma", "pos"], ["lemma"]]))
modality_list.append(("みたいです",          "(Evidential)みたいだ",     [["lemma", "pos"], ["lemma"]]))
modality_list.append(("ようだ",              "(Evidential)ようだ",       [["lemma", "pos"], ["orth"]]))
modality_list.append(("ようです",            "(Evidential)ようだ",       [["lemma", "pos"], ["orth"]]))

modality_list.append(("行かなければならない",   "(Deontic)行かなければならない",   [["pos1", "cForm"], ["lemma", "cType", "cForm"], ["lemma", "pos1"], ["lemma", "cType", "cForm"], ["lemma"]]))
modality_list.append(("行かなければなりません", "(Deontic)行かなければなりません", [["pos1", "cForm"], ["lemma", "cType", "cForm"], ["lemma", "pos1"], ["lemma", "cType", "cForm"], ["lemma"], ["lemma"]]))

modality_list.append(("行くしかない",           "(Deontic)〜しかない",             [["pos1", "cForm"], ["lemma", "pos1"], ["lemma", "pos1"]]))
modality_list.append(("行くしかありません",     "(Deontic)〜しかない",             [["pos1", "cForm"], ["lemma", "pos1"], ["lemma"], ["lemma"], ["lemma"]]))

modality_list.append(("行った方がいい",         "(Deontic)〜た方がいい",           [["pos1", "cForm"], ["cType"], ["lemma", "pos1"], ["lemma"], ["lemma"]]))

modality_list.append(("行くがいい",             "(Deontic)〜がいい",               [["pos1", "cForm"], ["lemma", "pos1"], ["lemma"]]))

modality_list.append(("行くといい",           "(Deontic)〜と／れば／たらいい",     [["pos1"], ["lemma", "pos1"], ["lemma"]]))
modality_list.append(("行けばいい",           "(Deontic)〜と／れば／たらいい",     [["pos1"], ["lemma", "pos1"], ["lemma"]]))
modality_list.append(("行ったらいい",         "(Deontic)〜と／れば／たらいい",     [["pos1"], ["lemma", "cForm"], ["lemma"]]))


modality_list.append(("行ってもいい",         "(Deontic)〜て（も）いい",     [["pos1"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma"]]))
modality_list.append(("行っていい",           "(Deontic)〜て（も）いい",     [["pos1"], ["lemma", "pos1"], ["lemma"]]))


modality_list.append(("行ってはいけない",     "(Deontic)〜てはいけない",     [["pos1"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma"], ["lemma"]]))
modality_list.append(("行ってはいけません",   "(Deontic)〜てはいけない",     [["pos1"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma"], ["lemma"], ["lemma"]]))


modality_list.append(("わけにはいかない",     "(Deontic)わけにはいかない",     [["lemma"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma"], ["lemma"]]))
modality_list.append(("わけにはいきません",   "(Deontic)わけにはいかない",     [["lemma"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma"], ["lemma"], ["lemma"]]))

modality_list.append(("行くものだ",               "(Deontic)〜ものだ",             [["pos1"], ["lemma"], ["lemma", "pos1"]]))
modality_list.append(("行くものです",             "(Deontic)〜ものだ",             [["pos1"], ["lemma"], ["lemma", "pos1"]]))
modality_list.append(("行くものである",           "(Deontic)〜ものだ",             [["pos1"], ["lemma"], ["lemma", "pos1"], ["lemma", "pos1"]]))

modality_list.append(("行くことだ",               "(Deontic)〜ことだ",             [["pos1"], ["lemma"], ["lemma", "pos1"]]))
modality_list.append(("行くことです",             "(Deontic)〜ことだ",             [["pos1"], ["lemma"], ["lemma", "pos1"]]))
modality_list.append(("行くことである",           "(Deontic)〜ことだ",             [["pos1"], ["lemma"], ["lemma", "pos1"], ["lemma", "pos1"]]))

modality_list.append(("行ってほしい",         "(Boulomaic)〜てほしい",         [["pos1"], ["lemma", "pos1"], ["lemma", "pos1"]]))

modality_list.append(("行ってもらいたい",     "(Boulomaic)〜てもらいたい",     [["pos1"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma", "pos1"]]))


modality_list.append(("行くつもり",         "(Boulomaic)〜（た）つもり",         [["pos1"], ["lemma", "pos1"]]))
modality_list.append(("行ったつもり",       "(Boulomaic)〜（た）つもり",         [["pos1"], ["lemma", "pos1"], ["lemma", "pos1"]]))


modality_list.append(("可能性がある",       "(Epistemic)可能性がある",         [["pos1", "lemma"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma"]]))
modality_list.append(("可能性があります",   "(Epistemic)可能性がある",         [["pos1", "lemma"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma"], ["lemma"]]))


modality_list.append(("行くことができる",     "(Dynamic)〜ことができる",         [["pos1"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma"]]))
modality_list.append(("行くことができます",   "(Dynamic)〜ことができる",         [["pos1"], ["lemma", "pos1"], ["lemma", "pos1"], ["lemma"], ["lemma"]]))

modality_list.append(("行きかねない",           "(Epistemic)〜かねない",             [["pos1"], ["pos1", "lemma"], ["lemma", "pos1"]]))
modality_list.append(("行きかねません",         "(Epistemic)〜かねない",             [["pos1"], ["pos1", "lemma"], ["lemma", "pos1"], ["lemma", "pos1"]]))

modality_list.append(("行きかねる",           "(Dynamic)〜かねる",             [["pos1"], ["pos1", "lemma"]]))
modality_list.append(("行きかねます",         "(Dynamic)〜かねる",             [["pos1"], ["pos1", "lemma"], ["lemma", "pos1"]]))

#modality_list.append(("行くまい",         "〜まい",             [["pos1"], ["pos1", "lemma"]]))

#modality_list.append(("行くしかない",           "〜しかない",             [["pos1", "cForm"], ["lemma", "pos1"], ["lemma", "pos1"]]))


if __name__ == "__main__":
    adverbs = set(lemma for (orth, lemma, pos) in adverb_list)
    for adverb in adverbs:
        print (adverb)
    modalities = set(lemma for (orth, lemma, pos) in modality_list)
    for modality in modalities:
        print (modality)

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import re
from collections import defaultdict
from customcounters import GenericCounter
#from multiprocessing import Pool

#from sentence import Sentence
from corpora import Corpora

hiragana = re.compile("[\u3041-\u309F]")
katakana = re.compile("[\u30A0-\u30FF]")
kanji = re.compile("[\u4E00-\u9FFF]")

def translate(string):
    accu = ""
    for char in string:
        if hiragana.match(char):
            accu += "H"
        elif katakana.match(char):
            accu += "K"
        elif kanji.match(char):
            accu += "C"
        elif re.match("^[a-zA-Z]$", char):
            accu += "R"
        else:
            accu += "P"
    i = 1
    prev = accu[0]
    counter = 1
    new = ""

    if len(accu) == 1:
        return str(1) + accu

    while i < len(accu):
        #print ("accu={}\taccu[i]={}\tprev={}\tnew={}\tcounter={}".format(accu, accu[i], prev, new, counter))
        # check for corner case
        if i == len(accu) - 1:
            if prev != accu[i]:
                new += str(counter) + prev
                new += str(1) + accu[i]
            else:
                new += str(counter+1) + prev
            break
        elif prev != accu[i]:
            new += str(counter) + prev
            counter = 1
        else:
            counter += 1

        prev = accu[i]
        i += 1
    #print(string, new)
    return new

class TempDict(dict):
    def __missing__(self, key):
        self[key] = rv = GenericCounter()
        return rv

class POSCounter(dict):
    def __missing__(self, key):
        self[key] = rv = TempDict()
        return rv

#####from jmdictlist import jmdict_list
#####from parsejmdict import read_flat_lemma_list
#####from statemachine import MorphemeMatcher
#####
#####jmdict_matcher = MorphemeMatcher(jmdict_list)
#####jmdict_flat_set = read_flat_lemma_list()

extra_rx = re.compile("-.*")

def process_file(file):
    morpheme_counter = 0
    pos_counter = POSCounter()
    orth_pron = {}
    #####lemma_goshu = {}
    code_histogram = TempDict()
    for sentence in file.to_sentences():
        #####already_matched = set()
        #####jmdict_matches = jmdict_matcher.match(sentence)
        #####for match in jmdict_matches:
        #####    lemma = "".join(re.sub(extra_rx, "", m.lemma) for m in sentence[match[2]:match[1]+1])
        #####    #orth = "".join(m.orth for m in sentence[match[2]:match[1]+1])
        #####    orthBase = "".join(m.orth for m in sentence[match[2]:match[1]]) + sentence[match[1]].orthBase
        #####    pronBase = "".join(m.pron for m in sentence[match[2]:match[1]]) + sentence[match[1]].pronBase
        #####    #print (match, "|".join(m.orth for m in sentence), "\n->\t", "".join(m.orth for m in sentence[match[2]:match[1]+1]), lemma)
        #####    pos = match[0]
        #####    lemma_goshu[lemma] = sentence[-1].goshu
        #####    pos_counter[pos][lemma][orthBase] += 1
        #####    code_histogram[pos][translate(orthBase)] += 1
        #####    orth_pron[orthBase] = pronBase
        #####    #print (list(range(match[2], match[1]+1)))
        #####    already_matched |= set(i for i in range(match[2], match[1]+1))
        #####    morpheme_counter += 1
        ######print("should skip:", already_matched)
        for i, morpheme in enumerate(sentence.Morphemes):
            ######## NEW PROPOSAL #########
            # Group compound nouns that are
            # in JMDict. This also applies
            # to count scores, but perhaps
            # having several would be
            # prudent
            ###############################
            # JMDict Deprecation Warning
            #####if i in already_matched:
            #####    #print ("skipping", morpheme.orth)
            #####    continue
            #####if morpheme.goshu == "unknown": continue
            # count compound nouns as 1 entry (with edict and friends)
            # also record goshu for every lemma
            #####lemma_goshu[re.sub(extra_rx, "", morpheme.lemma)] = morpheme.goshu
            morpheme_counter += 1
            #pos12 = morpheme.pos1 + "-" + morpheme.pos2
            pos12 = morpheme.pos1
            if pos12 == "代名詞":
                pos12 = "名詞"
            elif pos12 == "補助記号":
                pos12 = "記号"
            elif pos12 == "名詞" and morpheme.pos2 == "固有名詞":
                pos12 = "固有名詞"
            elif pos12 == "接頭辞" or pos12 == "接尾辞":
                pos12 = "接辞"
            # kigou into one
            # personal nouns seperate
            # suffix+prefix into one
            pos_counter[pos12][re.sub(extra_rx, "", morpheme.lemma)][morpheme.orthBase] += 1
            code_histogram[pos12][translate(morpheme.orthBase)] += 1
            orth_pron[morpheme.orthBase] = morpheme.pronBase
    return (morpheme_counter, pos_counter, orth_pron, code_histogram)#, lemma_goshu)


def codify(code_counter):
    total_freq = sum(freq for (code, freq) in code_counter.items())
    simple_codes = set(code for code in code_counter if re.match("^[0-9]+[CRKHP]$", code))
    r_codes = set(code for code in simple_codes if re.match(".*R.*", code))
    k_codes = set(code for code in simple_codes if re.match(".*K.*", code))
    h_codes = set(code for code in simple_codes if re.match(".*H.*", code))
    c_codes = set(code for code in simple_codes if re.match(".*C.*", code))
    p_codes = set(code for code in simple_codes if re.match(".*P.*", code))
    m_codes = set(code for code in code_counter if code not in simple_codes)
    r_freq = sum(code_counter[code] for code in r_codes)
    k_freq = sum(code_counter[code] for code in k_codes)
    h_freq = sum(code_counter[code] for code in h_codes)
    c_freq = sum(code_counter[code] for code in c_codes)
    p_freq = sum(code_counter[code] for code in p_codes)
    m_freq = sum(code_counter[code] for code in m_codes)
    return (r_codes, k_codes, h_codes, c_codes, p_codes, m_codes, r_freq, k_freq, h_freq, c_freq, p_freq, m_freq, total_freq)

#from multiprocessing import Pool


def main():
    if len(sys.argv) < 2:
        raise Exception("please specify directory or files as input")

    directories = sys.argv[1:]
    corpora = Corpora(directories)

    pos_counter = POSCounter()
    corpus_pos_counter = defaultdict(POSCounter)
    code_histogram = TempDict()
    corpus_code_histogram = defaultdict(TempDict)
    morpheme_counter = 0
    orth_pron = {}
    #####lemma_goshu = {}

    #pool = Pool()
    for corpus in corpora:
        # calculate by genre, pos
        #for packed_data in pool.imap(process_file, corpus, 500):
        for packed_data in map(process_file, corpus):
            morpheme_counter += packed_data[0]
            for pos in packed_data[1]:
                for lemma in packed_data[1][pos]:
                    for orthBase in packed_data[1][pos][lemma]:
                        pos_counter[pos][lemma][orthBase] += packed_data[1][pos][lemma][orthBase]
                        corpus_pos_counter[corpus.name][pos][lemma][orthBase] += packed_data[1][pos][lemma][orthBase]
            for (orthBase, pron) in packed_data[2].items():
                orth_pron[orthBase] = pron
            for pos in packed_data[3]:
                for trans in packed_data[3][pos]:
                    code_histogram[pos][trans] += packed_data[3][pos][trans]
                    corpus_code_histogram[corpus.name][pos][trans] += packed_data[3][pos][trans]
            #####for (lemma, goshu) in packed_data[4].items():
            #####    lemma_goshu[lemma] = goshu

        #for file in corpus:
        #    for sentence in file.to_sentences():
        #        for morpheme in sentence.Morphemes:
        #            if morpheme.goshu == "unknown": continue
        #            # count compound nouns as 1 entry (with edict and friends)
        #            # also record goshu for every lemma
        #            morpheme_counter += 1
        #            pos12 = morpheme.pos1 + "-" + morpheme.pos2
        #            pos_counter[pos12][morpheme.lemma][morpheme.orthBase] += 1
        #            code_histogram[pos12][translate(morpheme.orthBase)] += 1
        #            orth_pron[morpheme.orthBase] = morpheme.pronBase

    for pos in pos_counter:
        with open("lemma-orth-relations-{}.tsv".format(pos), "w") as f:
            #####f.write("lemma\tvariations\tgoshu\ttotal frequency\torthBase\tpronBase\torthBase length\tcode\torthBase frequency\tratio (orthBase frequency / total frequency)\t{}\n".format(" frequency\t".join(corpusname for corpusname in corpus_pos_counter)))
            f.write("lemma\tvariations\ttotal frequency\torthBase\tpronBase\torthBase length\tcode\torthBase frequency\tratio (orthBase frequency / total frequency)\t{}\n".format(" frequency\t".join(corpusname for corpusname in corpus_pos_counter)))
            # add orthbase freq. count by subcorpus
            #print (pos_counter)
            for goiso in pos_counter[pos]:
                #print(pos)
                #print(goiso)
                #print(pos_counter[pos])
                #print(pos_counter[pos]["西洋蒲公英"])
                total_freq = sum(freq for (orthBase, freq) in pos_counter[pos][goiso].items())
                variations = len(pos_counter[pos][goiso])
                # add data by subcorpus
                #####f.write("".join("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(goiso, variations, lemma_goshu[goiso], total_freq,
                f.write("".join("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(goiso, variations, total_freq,
                                                                              orthBase, orth_pron[orthBase], len(orthBase),
                                                                              translate(orthBase), freq, freq / total_freq,
                                                                              "\t".join(str(corpus_pos_counter[corpus][pos][goiso][orthBase]) for corpus in corpus_pos_counter))
                        for (orthBase, freq) in pos_counter[pos][goiso].items()))
        with open("lemma-orth-relations-rank-{}.tsv".format(pos), "w") as f:
            #####f.write("lemma\tvariations\tfrequency\tvariation type\tJMDict\n")
            f.write("lemma\tvariations\tfrequency\tvariation type")
            for goiso in pos_counter[pos]:
                variations = len(pos_counter[pos][goiso])
                total_freq = sum(freq for (orthBase, freq) in pos_counter[pos][goiso].items())
                variation_type = ""
                most_frequent = max(freq for (orthBase, freq) in pos_counter[pos][goiso].items())
                if (most_frequent / total_freq) >= 0.9:
                    variation_type = ">=0.9"
                elif (most_frequent / total_freq) >= 0.8:
                    variation_type = "0.9 > ... > 0.8"
                elif (most_frequent / total_freq) >= 0.7:
                    variation_type = "0.8 > ... > 0.7"
                elif (most_frequent / total_freq) >= 0.6:
                    variation_type = "0.7 > ... > 0.6"
                elif (most_frequent / total_freq) >= 0.5:
                    variation_type = "0.6 > ... > 0.5"
                else:# (freq / total_freq) >= 0.4:
                    variation_type = "<0.5"

                #for (orthBase, freq) in pos_counter[pos][goiso].items():
                #    if (freq / total_freq) >= 0.9:
                #        variation_type = ">=0.9"
                #    elif (freq / total_freq) >= 0.8:
                #        variation_type = "0.9 > ... > 0.8"
                #    elif (freq / total_freq) >= 0.7:
                #        variation_type = "0.8 > ... > 0.7"
                #    elif (freq / total_freq) >= 0.6:
                #        variation_type = "0.7 > ... > 0.6"
                #    elif (freq / total_freq) >= 0.5:
                #        variation_type = "0.6 > ... > 0.5"
                #    else:# (freq / total_freq) >= 0.4:
                #        variation_type = "<0.5"
                #####f.write("{}\t{}\t{}\t{}\t{}\n".format(goiso, variations, total_freq, variation_type, 1 if goiso in jmdict_flat_set else 0))
                f.write("{}\t{}\t{}\t{}\n".format(goiso, variations, total_freq, variation_type))
        with open("type-frequency-{}.tfl".format(pos), "w") as f:
            f.write("f\tk\ttype\n")
            index = 1
            for goiso in pos_counter[pos]:
                total_freq = sum(freq for (orthBase, freq) in pos_counter[pos][goiso].items())
                f.write("{}\t{}\t{}\n".format(total_freq, index, goiso))
                index += 1
        with open("type-variations-{}.tfl".format(pos), "w") as f:
            f.write("f\tk\ttype\n")
            index = 1
            for goiso in pos_counter[pos]:
                variations = len(pos_counter[pos][goiso])
                f.write("{}\t{}\t{}\n".format(variations, index, goiso))
                index += 1

    goiso_count = len(set(lemma for (pos, lemmas) in pos_counter.items() for (lemma, orths) in lemmas.items()))
    orth_count = len(set(orth   for (pos, lemmas) in pos_counter.items() for (lemma, orths) in lemmas.items() for orth in orths))
    code_count = len(set(lemma  for (pos, lemmas) in code_histogram.items() for lemma in lemmas))
    print ("Lemma count: {}\tOrth count:{}\tCode count:{}\tMorphemes:{}".format(goiso_count, orth_count, code_count, morpheme_counter))
    with open("lemma-orth-relations.tsv", "w") as f:
        f.write("POS type\ttotal frequency\tlemma types\torthbase types\tlemma / orthbase type ratio\t% of 1:1 lemma-orthbase ratios\tcode types\tR\tK\tH\tC\tP\tM\n")
        code_counter = defaultdict(int)
        for pos_type in pos_counter:
            # Fishy numbers?!
            pos_lemma_count = sum(1 for (lemmas, orths) in pos_counter[pos_type].items())
            #pos_lemma_tokens = sum(len(lemmas) for (lemmas, orths) in pos_counter[pos_type].items())

            pos_orth_count = sum(len(orths) for (lemmas, orths) in pos_counter[pos_type].items())
            pos_code_count = sum(1 for (codes, freq) in code_histogram[pos_type].items())
            pos_one_count  = sum(1 for (lemmas, orths) in pos_counter[pos_type].items() if len(orths) == 1)
            frequency = sum(freq for (lemmas, orths) in pos_counter[pos_type].items() for (orth, freq) in orths.items())
            (r_codes, k_codes, h_codes, c_codes, p_codes, m_codes, r_freq, k_freq, h_freq, c_freq, p_freq, m_freq, total_freq) = codify(code_histogram[pos_type])
            f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(pos_type, frequency, pos_lemma_count, pos_orth_count, pos_lemma_count / pos_orth_count, pos_one_count / pos_lemma_count, pos_code_count, r_freq, k_freq, h_freq, c_freq, p_freq, m_freq))
            #f.write("{}\t{}\t{}\t{}\n".format(pos_type, pos_lemma_count, pos_orth_count, pos_code_count, pos_lemma_tokens, pos_orth_tokens))
            for (code, freq) in code_histogram[pos_type].items():
                code_counter[code] += freq
        f.write("Summary:\ttotal morphemes: {}\tlemma types: {}\torthbase types:{}\t\tcode types:{}\n".format(morpheme_counter, goiso_count, orth_count, code_count))
        f.write("\ncode\tfrequency\tratio\tvariations\n")
        # aggregate by only chinese char., katakana, .., + mixed tokens
        # this should go up, columns
        (r_codes, k_codes, h_codes, c_codes, p_codes, m_codes, r_freq, k_freq, h_freq, c_freq, p_freq, m_freq, total_freq) = codify(code_counter)
        f.write("R\t{}\t{}\t{}\n".format(r_freq, r_freq / total_freq, ", ".join("{0} ({1:0.00%})".format(code, code_counter[code] / r_freq) for code in r_codes)))
        f.write("K\t{}\t{}\t{}\n".format(k_freq, k_freq / total_freq, ", ".join("{0} ({1:0.00%})".format(code, code_counter[code] / k_freq) for code in k_codes)))
        f.write("H\t{}\t{}\t{}\n".format(h_freq, h_freq / total_freq, ", ".join("{0} ({1:0.00%})".format(code, code_counter[code] / h_freq) for code in h_codes)))
        f.write("C\t{}\t{}\t{}\n".format(c_freq, c_freq / total_freq, ", ".join("{0} ({1:0.00%})".format(code, code_counter[code] / c_freq) for code in c_codes)))
        f.write("P\t{}\t{}\t{}\n".format(p_freq, p_freq / total_freq, ", ".join("{0} ({1:0.00%})".format(code, code_counter[code] / p_freq) for code in p_codes)))
        f.write("M\t{}\t{}\t{}\n".format(m_freq, m_freq / total_freq, ", ".join("{0} ({1:0.00%})".format(code, code_counter[code] / m_freq) for code in m_codes)))
        #for (code, freq) in code_counter.items():
        #    f.write("{}\t{}\t{}\n".format(code, freq, freq / total_codes))
    # TODO: find highly polysemous lemmas, find lemmas with the same pronounciation or orthBase(!)

if __name__ == "__main__":
    ## PROFILING
    #import cProfile, pstats
    ##import lsprofcalltree
    #prof = cProfile.Profile()
    #prof = prof.runctx("main()", globals(), locals())
    ##print ("<pre>")
    #stats = pstats.Stats(prof)
    #stats.sort_stats("time")  # Or cumulative
    #stats.print_stats(80)  # 80 = how many to print
    ##k = lsprofcalltree.KCacheGrind(p)
    ##data = open("profile.tmp", 'w+')
    ##k.output(data)
    ##data.close()
    ## The rest is optional.
    ## stats.print_callees()
    ## stats.print_callers()
    ##print ("</pre>")
    ##import cProfile
    ##cProfile.run(sc.main(sys.argv), 'prof.txt')
    sys.exit(main())

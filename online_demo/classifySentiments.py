#!/home/s1010205/bin/python2.7
from collections import defaultdict
try:
    import cPickle as pickle
except ImportError:
    import _pickle as cPickle

import nltk
from nltk.corpus import wordnet as wn
from bag_of_words import train_bag_of_words, classify_polarity


def word_similarity(word1, word2):
    w1synsets = wn.synsets(word1)
    w2synsets = wn.synsets(word2)
    maxsim = 0
    for w1s in w1synsets:
        for w2s in w2synsets:
            current = wn.path_similarity(w1s, w2s)
            if (current > maxsim and current > 0):
                maxsim = current
    return maxsim


def disambiguateWordSenses(sentence, word):
    wordsynsets = wn.synsets(word)
    bestScore = 0.0
    result = None
    for synset in wordsynsets:
        for w in nltk.word_tokenize(sentence):
            score = 0.0
            for wsynset in wn.synsets(w):
                sim = wn.path_similarity(wsynset, synset)
                if sim is None:
                    continue
                else:
                    score += sim
            if (score > bestScore):
                bestScore = score
                result = synset
    return result


def line_wn(line):
    line_wsd = ""
    for w in line.split():
        if disambiguateWordSenses(line, w):
            line_wsd += " " + disambiguateWordSenses(line, w).name
        else:
            line_wsd += " " + w
    return line_wsd.strip()


def SentiWordNet_to_pickle(swn):
    synsets_scores = defaultdict(list)
    for senti_synset in swn.all_senti_synsets():
        if not synsets_scores.has_key(senti_synset.synset.name):
            synsets_scores[senti_synset.synset.name] = defaultdict(float)
        synsets_scores[senti_synset.synset.name]['pos'] += senti_synset.pos_score
        synsets_scores[senti_synset.synset.name]['neg'] += senti_synset.neg_score
    return synsets_scores


def classify(text, synsets_scores, bag_of_words):
    #synsets_scores = pickled object in data/SentiWN.p
    pos = neg = 0
    for line in text:
        if not line.strip() or line.startswith('#'):
            continue
        for sentence in line.split('.'):
            sentence = sentence.strip()
            sent_score_pos = sent_score_neg = 0
            for word in sentence.split():
                if disambiguateWordSenses(sentence, word):
                    disamb_syn = disambiguateWordSenses(sentence, word).name
                    if disamb_syn in synsets_scores:
                        #uncomment the disamb_syn.split... if also want to check synsets polarity
                        if word.lower() in bag_of_words['neg']:
                            sent_score_neg += synsets_scores[disamb_syn]['neg']
                        if word.lower() in bag_of_words['pos']:
                            sent_score_pos += synsets_scores[disamb_syn]['pos']
            pos += sent_score_pos
            neg += sent_score_neg
    return pos, neg


def call_classifier(lines_list):
    results = []
    synsets_scores = pickle.load(open('/home/s1010205/public_html/cgi-bin/senti_classifier/SentiWn.p','rb'))
    bag_of_words = pickle.load(open('/home/s1010205/public_html/cgi-bin/senti_classifier/bag_of_words.p','rb'))
    bag_of_words = classify_polarity(bag_of_words)
    scorer = defaultdict(list)
    pos, neg = classify(lines_list, synsets_scores, bag_of_words)
    return pos, neg


if __name__ == "__main__":
    pass



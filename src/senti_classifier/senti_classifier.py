#!/usr/bin/env python
from __future__ import print_function
import re
import sys
import codecs
from collections import defaultdict
try:
    import cPickle as pickle
except ImportError:
    import _pickle as pickle

import nltk
from nltk.corpus import wordnet as wn
from pkg_resources import resource_stream
import nltk.classify.util
from nltk.corpus import movie_reviews

"""
Interface to SentiWordNet using the NLTK WordNet classes.

---Chris Potts

Sentiment Classifier & WSD Module

--Pulkit Kathuria
"""
__note__ = "Don not follow the following links I am not a JAIST STUDENT anymore"
__documentation__ = "http://www.jaist.ac.jp/~s1010205/sentiment_classifier"
__url__ = "http://www.jaist.ac.jp/~s1010205/"
__online_demo__ = "http://www.jaist.ac.jp/~s1010205/sentiment_classifier"


class SentiWordNetCorpusReader:
    def __init__(self, filename):
        """
        Argument:
        filename -- the name of the text file containing the
                    SentiWordNet database
        """
        self.filename = filename
        self.db = {}
        self.parse_src_file()

    def parse_src_file(self):
        lines = codecs.open(self.filename, "r", "utf8").read().splitlines()
        lines = filter((lambda x: not re.search(r"^\s*#", x)), lines)
        for i, line in enumerate(lines):
            fields = re.split(r"\t+", line)
            fields = map(lambda s: s.strip(), fields)
            try:
                pos, offset, pos_score, neg_score, synset_terms, gloss = fields
            except:
                sys.stderr.write("Line %s formatted incorrectly: %s\n" % (i, line))
            if pos and offset:
                offset = int(offset)
                self.db[(pos, offset)] = (float(pos_score), float(neg_score))

    def senti_synset(self, *vals):
        if tuple(vals) in self.db:
            pos_score, neg_score = self.db[tuple(vals)]
            pos, offset = vals
            synset = wn._synset_from_pos_and_offset(pos, offset)
            return SentiSynset(pos_score, neg_score, synset)
        else:
            synset = wn.synset(vals[0])
            pos = synset.pos
            offset = synset.offset
            if (pos, offset) in self.db:
                pos_score, neg_score = self.db[(pos, offset)]
                return SentiSynset(pos_score, neg_score, synset)
            else:
                return None

    def senti_synsets(self, string, pos=None):
        sentis = []
        synset_list = wn.synsets(string, pos)
        for synset in synset_list:
            sentis.append(self.senti_synset(synset.name))
        sentis = filter(lambda x: x, sentis)
        return sentis

    def all_senti_synsets(self):
        for key, fields in self.db.iteritems():
            pos, offset = key
            pos_score, neg_score = fields
            synset = wn._synset_from_pos_and_offset(pos, offset)
            yield SentiSynset(pos_score, neg_score, synset)


class SentiSynset(object):
    def __init__(self, pos_score, neg_score, synset):
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = 1.0 - (self.pos_score + self.neg_score)
        self.synset = synset

    def __str__(self):
        """Prints just the Pos/Neg scores for now."""
        s = ""
        s += self.synset.name + "\t"
        s += "PosScore: %s\t" % self.pos_score
        s += "NegScore: %s" % self.neg_score
        return s

    def __repr__(self):
        return "Senti" + repr(self.synset)


def count_features(bag_of_words, features, polarity):
    for lst in features:
        for word in lst[0].keys():
            bag_of_words[polarity][word] += 1
    return bag_of_words


def train_bag_of_words():
    """
    @return: dictionary
      bag_of_words['neg']['word'] ==> count
      bag_of_words['pos']['word'] ==> count
    """

    def word_feats(words):
        return dict([(word, True) for word in words])
    bag_of_words = {}
    bag_of_words['neg'] = defaultdict(int)
    bag_of_words['pos'] = defaultdict(int)
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg')
                for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos')
                for f in posids]
    bag_of_words = count_features(bag_of_words, negfeats, 'neg')
    bag_of_words = count_features(bag_of_words, posfeats, 'pos')
    return bag_of_words


def classify_polarity(bag_of_words):
    """
    Pops word from bag_of_words['neg'/'pos'] if the word appears
    more in 'pos/'neg' respectively
    """
    for word, count in bag_of_words['neg'].copy().items():
        if count > bag_of_words['pos'][word]:
            bag_of_words['pos'].pop(word)
        else:
            bag_of_words['neg'].pop(word)
    return bag_of_words

"""
Word Disambiguator using nltk
Sentiment Classifier as a combination of
  -Bag of Words (nltk movie review corpus, words as features)
  -Heuristics

--KATHURIA Pulkit
"""


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
            if score > bestScore:
                bestScore = score
                result = synset
    return result


def SentiWordNet_to_pickle(swn):
    synsets_scores = defaultdict(list)
    for senti_synset in swn.all_senti_synsets():
        if senti_synset.synset.name not in synsets_scores:
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
                    disamb_syn = disambiguateWordSenses(sentence, word).name()
                    if disamb_syn in synsets_scores:
                        #uncomment the disamb_syn.split... if also want to check synsets polarity
                        if word.lower() in bag_of_words['neg']:
                            sent_score_neg += synsets_scores[disamb_syn]['neg']
                        if word.lower() in bag_of_words['pos']:
                            sent_score_pos += synsets_scores[disamb_syn]['pos']
            pos += sent_score_pos
            neg += sent_score_neg
    return pos, neg


#==========  Skipping pickle for a while  ==========*/

senti_pickle = resource_stream('senti_classifier', 'data/SentiWn.p')
bag_of_words_pickle = resource_stream('senti_classifier', 'data/bag_of_words.p')
synsets_scores = pickle.load(senti_pickle)
bag_of_words = pickle.load(bag_of_words_pickle)
bag_of_words = classify_polarity(bag_of_words)


def polarity_scores(lines_list):
    pos, neg = classify(lines_list, synsets_scores, bag_of_words)
    return pos, neg


if __name__ == "__main__":
    pickles = ['SentiWn.p']
    print(classify(["The movie was the worst movie bad super worst"],
                   synsets_scores, bag_of_words))

    #=====================================
    #            Debug Code           =
    #====================================*/

    # parser = argparse.ArgumentParser(add_help = True)
    # parser = argparse.ArgumentParser(description= 'Sentiment classification')
    # parser.add_argument('-p','--pickle', action="store", dest="SentiWN_path", type=str, help='SentiWordNet_*.txt')
    # parser.add_argument('-c','--classify', action="store", nargs = '*', dest="files", type=argparse.FileType('rt'), help='-c reviews')
    # myarguments = parser.parse_args()
    # synsets_scores = SentiWordNet_to_pickle(SentiWordNetCorpusReader(myarguments.SentiWN_path))
    # pickle.dump(synsets_scores, open(pickles[0],'wb'))

    # Fix me: TypeError: can't pickle instancemethod objects
    # Not able to dump the pickle somehow. http://stackoverflow.com/questions/16439301/cant-pickle-defaultdict
    # pickle.dump(synsets_scores, open(pickles[0],'wb'))
    # 
    # Temporary Fix, just don't pickle them (it takes long time ! its better to pickle)
    
    # bag_of_words = train_bag_of_words()
    # bag_of_words = classify_polarity(bag_of_words)

    



    # pickle.dump(synsets_scores, open(pickles[0],'wb'))
    # if myarguments.SentiWN_path or not os.path.exists(pickles[0]):
    #     if not myarguments.SentiWN_path:
    #         print '1) python setup.py install'
    #         print '2) classifySentiments --pickle SentiWordNet_3.0.0_20100908.txt'
    #         exit()
    #     synsets_scores = SentiWordNet_to_pickle(SentiWordNetCorpusReader(myarguments.SentiWN_path))
        # pickle.dump(synsets_scores, open(pickles[0],'wb'))
    # if os.path.exists(pickles[0]) and myarguments.files:
    #     synsets_scores = pickle.load(open(pickles[0],'rb'))
    #     bag_of_words = train_bag_of_words()
    #     bag_of_words = classify_polarity(bag_of_words)
    #     scorer = defaultdict(list)
    #     for file in myarguments.files:
    #         pos, neg = classify(file.readlines(), synsets_scores, bag_of_words)
    #         if not scorer.has_key(file.name): scorer[file.name] = defaultdict(float)
    #         scorer[file.name]['positive'] = pos
    #         scorer[file.name]['negative'] = neg
    #         file.close()
    #     for key in scorer.keys():
    #         total_pos = scorer[key].items()[0][1]
    #         total_neg = scorer[key].items()[1][1]
    #         sentiment, score = max(scorer[key].iteritems(), key=operator.itemgetter(1))
    #         #print '{0:<50}{1:<6}{2:<10}{3:<10}{4:<10}{5:<10}'.format(' ','TOTAL','POSITIVE=',total_pos,'NEGATIVE=',total_neg)
    #         if sentiment == 'negative': print key,'=', sentiment.upper(), 'score =' ,score
    #         else: print key,'=', sentiment.upper(),'score =' ,score
    #     #if len(scorer.keys()) > 1:
    #         #for key in scorer.keys():

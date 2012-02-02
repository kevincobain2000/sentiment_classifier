#!/usr/bin/env python
import re
import os
import sys
import codecs
import nltk
from nltk.corpus import wordnet as wn
import argparse
from collections import defaultdict
import cPickle as pickle
import operator
from pkg_resources import resource_string
try:
    from senti_classifier.bag_of_words import train_bag_of_words, classify_polarity
except ImportError:
    from bag_of_words import train_bag_of_words, classify_polarity

"""
Interface to SentiWordNet using the NLTK WordNet classes.

---Chris Potts

Sentiment Classifier

--Pulkit Kathuria
"""
__thisfile__ = "http://www.jaist.ac.jp/~s1010205/pybits/pybits.html.LyXconv/pybits.html#x1-40003"
__url__ = "http://www.jaist.ac.jp/~s1010205/home"

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
        lines = filter((lambda x : not re.search(r"^\s*#", x)), lines)
        for i, line in enumerate(lines):
            fields = re.split(r"\t+", line)
            fields = map(unicode.strip, fields)
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
        sentis = filter(lambda x : x, sentis)
        return sentis

    def all_senti_synsets(self):
        for key, fields in self.db.iteritems():
            pos, offset = key
            pos_score, neg_score = fields
            synset = wn._synset_from_pos_and_offset(pos, offset)
            yield SentiSynset(pos_score, neg_score, synset)

class SentiSynset:
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
               if(sim == None):
                   continue
               else:
                   score += sim
           if (score > bestScore):
              bestScore = score
              result = synset
   return result

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
        if not line.strip() or line.startswith('#'):continue
        for sentence in line.split('.'):
            sentence = sentence.strip()
            sent_score_pos = sent_score_neg = 0
            for word in sentence.split():
                if disambiguateWordSenses(sentence, word): 
                    disamb_syn = disambiguateWordSenses(sentence, word).name
                    if synsets_scores.has_key(disamb_syn):
                        #uncomment the disamb_syn.split... if also want to check synsets polarity
                        if bag_of_words['neg'].has_key(word.lower()):#disamb_syn.split('.')[0]):
                            sent_score_neg += synsets_scores[disamb_syn]['neg']
                        if bag_of_words['pos'].has_key(word.lower()):#disamb_syn.split('.')[0]):
                            sent_score_pos += synsets_scores[disamb_syn]['pos']
            print '{0:<50}{1:<6}{2:<10}{3:<10}{4:<10}{5:<10}'.format(sentence[:40],'...', 'positive=',sent_score_pos,'negative=',sent_score_neg)
            #Following 2 are custom settings as per the SentiWordNet scores
            #Change it as per domain adaptation
            pos += sent_score_pos
            neg += sent_score_neg
    return pos, neg
    
if __name__ == "__main__":
    pickles = ['SentiWn.p']
    parser = argparse.ArgumentParser(add_help = True)
    parser = argparse.ArgumentParser(description= 'Sentiment classification')
    parser.add_argument('-p','--pickle', action="store", dest="SentiWN_path", type=str, help='SentiWordNet_*.txt')
    parser.add_argument('-c','--classify', action="store", nargs = '*', dest="files", type=argparse.FileType('rt'), help='-c reviews')
    myarguments = parser.parse_args()
    if myarguments.SentiWN_path or not os.path.exists(pickles[0]):
        if not myarguments.SentiWN_path:
            print '\x1b[%sm%s\x1b[0m' % (';'.join(['31','1']), 'Run following commands FIRST')
            print '1) python setup.py install'
            print '2) senti_classifier --pickle SentiWordNet_3.0.0_20100908.txt'
            exit()
        synsets_scores = SentiWordNet_to_pickle(SentiWordNetCorpusReader(myarguments.SentiWN_path))
        pickle.dump(synsets_scores, open(pickles[0],'wb'))
        print '\x1b[%sm%s\x1b[0m' % (';'.join(['32','1']), 'Success, Pickled Sentiwordnet to --> '), pickles[0]
    if os.path.exists(pickles[0]) and myarguments.files:
        print '\x1b[%sm%s\x1b[0m' % (';'.join(['31','1']),'loading pickle...........')
        print '\x1b[%sm%s\x1b[0m' % (';'.join(['32','1']),'loading pickle successful')
        synsets_scores = pickle.load(open(pickles[0],'rb'))
        print '\x1b[%sm%s\x1b[0m' % (';'.join(['31','1']),'Training Bag Of Words...........')
        bag_of_words = train_bag_of_words()
        bag_of_words = classify_polarity(bag_of_words)
        print '\x1b[%sm%s\x1b[0m' % (';'.join(['32','1']),'Training Bag Of Words successful')
        print '--------------------------------'
        scorer = defaultdict(list)
        for file in myarguments.files:
            pos, neg = classify(file.readlines(), synsets_scores, bag_of_words)
            if not scorer.has_key(file.name): scorer[file.name] = defaultdict(float)
            scorer[file.name]['positive'] = pos
            scorer[file.name]['negative'] = neg
            file.close()
        for key in scorer.keys():
            total_pos = scorer[key].items()[0][1]
            total_neg = scorer[key].items()[1][1]
            sentiment, score = max(scorer[key].iteritems(), key=operator.itemgetter(1))
            print '{0:<50}{1:<6}{2:<10}{3:<10}{4:<10}{5:<10}'.format('','','-'*10,'-'*10,'-'*10,'-'*5)
            print '{0:<50}{1:<6}{2:<10}{3:<10}{4:<10}{5:<10}'.format(' ','TOTAL','POSITIVE=',total_pos,'NEGATIVE=',total_neg)
            score = '\x1b[%sm%s\x1b[0m' % (';'.join(['1']),str(score))
            if sentiment == 'negative': print key,'is','\x1b[%sm%s\x1b[0m' % (';'.join(['31','1']), sentiment.upper()),'with score' ,score
            else: print key,'is','\x1b[%sm%s\x1b[0m' % (';'.join(['32','1']), sentiment.upper()),'with score' ,score
        print '-'*30
        if len(scorer.keys()) > 1:
            for key in scorer.keys():
                print key,'is','\x1b[%sm%s\x1b[0m' % (';'.join(['32','1']), sentiment.upper()),'with score' ,score
            

            



        



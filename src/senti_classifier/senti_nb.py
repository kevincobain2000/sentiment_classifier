#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, warnings
from __init__ import *
from senti_classifier import *

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from reverend.thomas import Bayes

def process_line(line):
    line = " ".join([i.lower() for i in line.split() if i not in PUNCTUATION])
    line = " ".join([i for i in line.split() if i not in STOPWORDS])
    return line

def train_nb(guesser, fpaths_list, label = None):
    for f in fpaths_list:
        with open(f) as buff:
            for line in buff.readlines():
                line = process_line(line)
                guesser.train(label, line)
    return guesser

def classify_pos_neg(SCORES):
    if SCORES: pos, neg = SCORES
    else: return "Neutral/Hard To Classify"
    
    if pos[1] - neg[1] <= 0.15: return "Neutral/Hard To Classify"
    elif pos[1] > neg[1]: return "Positive"
    return "Negative"

def line_wn(line):
    line_wsd = ""
    for w in line.split():
        if disambiguateWordSenses(line, w):
            line_wsd += " " + disambiguateWordSenses(line, w).name
        else: line_wsd += " "+ w
    return line_wsd.strip()

def wsd_lexicon(fpaths_list):
    #converts list of files to wordnet features
    fw = open('data/pos_wn','w')
    for i,f in enumerate(fpaths_list, 1):
        print str(i) + ' out of ' + str(len(fpaths_list))
        with open(f) as buff:
            for line in buff.readlines():
                if not line.strip(): continue
                line = line_wn(line)
                fw.write(line)
                fw.write('\n')
    return
if __name__ == '__main__':
    query = "I did not loose profits"
    query = process_line(query)
    guesser = Bayes()
    data_path = 'data/'
    #neg_files = [data_path + 'neg/' + i for i in os.listdir('%sneg/'%data_path)]
    #pos_files = [data_path + 'pos/' + i for i in os.listdir('%s/pos/'%data_path)]
    ##wsd_lexicon(pos_files)
    neg_files = ['data/neg_wn']
    pos_files = ['data/pos_wn']
    
    guesser = train_nb(guesser, neg_files, label = "neg")
    guesser = train_nb(guesser, pos_files, label = "pos")
    query = line_wn(query)
    SCORES = guesser.guess(query)
    print classify_pos_neg(SCORES), SCORES
    

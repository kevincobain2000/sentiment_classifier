#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from collections import defaultdict

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
    def word_feats(words): return dict([(word, True) for word in words])
    bag_of_words = {}
    bag_of_words['neg'] = defaultdict(int)
    bag_of_words['pos'] = defaultdict(int)
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
    bag_of_words = count_features(bag_of_words, negfeats, 'neg')
    bag_of_words = count_features(bag_of_words, posfeats, 'pos')
    return bag_of_words

def classify_polarity(bag_of_words):
    """
    Pops word from bag_of_words['neg'/'pos'] if the word appears
    more in 'pos/'neg' respectively
    """
    for word, count in bag_of_words['neg'].items():
        if count > bag_of_words['pos'][word]: bag_of_words['pos'].pop(word)
        else: bag_of_words['neg'].pop(word)
    return bag_of_words

if __name__ == '__main__':
    bag_of_words = train_bag_of_words()
    bag_of_words = classify_polarity(bag_of_words)
    print bag_of_words

    
    



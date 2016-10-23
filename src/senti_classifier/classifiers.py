#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import pickle

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier, MaxentClassifier
from nltk.classify.util import accuracy


def extract_words(text):
    # For English, although Porter Stemmer is not good
    # Replace it with morpha (Lemmatizer)
    stemmer = PorterStemmer()
    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(text)

    bigram_finder = BigramCollocationFinder.from_words(tokens)
    bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)
    for bigram_tuple in bigrams:
        x = "%s %s" % bigram_tuple
        tokens.append(x)
    result = [stemmer.stem(x.lower()) for x in tokens
              if x not in stopwords.words('english') and len(x) > 1]
    return result


def extract_words_japanese(text):
    #content words, syntactic relations
    pass


def get_feature(word):
    return dict([(word, True)])


def bag_of_words(words):
    return dict([(word, True) for word in words])


def create_training_dict(text, sense):
    tokens = extract_words(text)
    return [(bag_of_words(tokens), sense)]


def get_train_set(texts):
    # Change to buffer `texts`
    train_set = []
    for sense, file in texts.iteritems():
        print("training %s " % sense)
        text = open(file, 'r').read()  # Change later
        features = extract_words(text)
        train_set = train_set + [(get_feature(word), sense) for word in features]
    return train_set


if __name__ == '__main__':
    texts = {}
    domain = "movies"
    #domain = "tweets"
    #classifier_name = "NaiveBayes"
    #classifier_name = "MaxentClassifier"
    
    texts['neg'] = 'data/neg-%s-tokens'%domain
    texts['pos'] = 'data/pos-%s-tokens'%domain
    
    pickled_classifier = 'classifier-%s.%s.pickle'%(classifier_name, domain)
    if not os.path.exists(pickled_classifier):
        print("Training on Files", texts)
        print("Will be pickling", pickled_classifier)
        train_set = get_train_set(texts)
        #classifier = NaiveBayesClassifier.train(train_set)
        #classifier = MaxentClassifier.train(train_set)
        pickle.dump(classifier, open(pickled_classifier,'w'))
    else: classifier = pickle.load(open(pickled_classifier,'r'))
    #classifier.show_most_informative_features(20)

    for line in open("data/sample_review.txt", 'r'):
        tokens = bag_of_words(extract_words(line))
        print(classifier.prob_classify(tokens).prob('neg'))
        print(classifier.prob_classify(tokens).prob('pos'))
        decision = classifier.classify(tokens)
        result = "%s - %s" % (decision, line)
        print(result)

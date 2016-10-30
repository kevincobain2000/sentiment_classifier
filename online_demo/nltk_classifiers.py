from __future__ import print_function
import os
import pickle

from __init__ import *
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier


def extract_words(text):
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


def get_feature(word):
    return dict([(word, True)])


def bag_of_words(words):
    return dict([(word, True) for word in words])


def create_training_dict(text, sense):
    ''' returns a dict ready for a classifier's test method '''
    tokens = extract_words(text)
    return [(bag_of_words(tokens), sense)]


def get_train_set(texts):
    train_set = []
    for sense, file in texts.iteritems():
        print("training %s " % sense)
        text = open(file, 'r').read()
        features = extract_words(text)
        train_set = train_set + [(get_feature(word), sense)
                                 for word in features]
    return train_set


if __name__ == '__main__':
    texts = {}

    texts['neg'] = 'data/neg-tokens'
    texts['pos'] = 'data/pos-tokens'
    if not os.path.exists('classifier.pickle'):
        train_set = get_train_set(texts)
        classifier = NaiveBayesClassifier.train(train_set)
        pickle.dump(classifier, open('classifier.pickle', 'w'))
    else:
        classifier = pickle.load(open('classifier.pickle', 'r'))

    #classifier.show_most_informative_features(20)

    for line in open("data/sample_review.txt", 'r'):
        tokens = bag_of_words(extract_words(line))
        decision = classifier.classify(tokens)
        result = "%s - %s" % (decision, line)
        print(result)

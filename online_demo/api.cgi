#!/home/s1010205/bin/python2.7
# -*- coding: utf-8 -*
from __future__ import division

"""
USAGE
http://www.jaist.ac.jp/~s1010205/cgi-bin/sent_classifier/api.cgi?string=Bad Movie is&classifier=NaiveBayes
"""
from __init__ import *
import datetime
import cPickle as pickle
from nltk_classifiers import *

def app(environ, start_response):
  start_response('200 OK', [('Content-Type', 'text/plain')])
  parameters = parse_qs(environ.get('QUERY_STRING', ''))
  yield " "
  string = ''
  classifier_name = 'MaxentClassifier'
  domain = 'movies'
  if 'string' in parameters: 
     string = escape(parameters['string'][0])
  if 'classifier' in parameters: 
     classifier_name = escape(parameters['classifier'][0])
  if 'domain' in parameters: 
     domain = escape(parameters['domain'][0])

  results_json = {}
  if string.strip():
    pos = neg = 0
    f = open("logs/log",'a+')
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M")
    if not string.startswith('Input bad movie'):
       f.write("\nEntry:%s"%date_time)
       f.write(' Via Api %s'%classifier_name) 
       f.write("\n%s\n"%string)
    
    r = re.compile("[,.?()\\d]+ *")
    lines_list = r.split(string)
    
    #Classify Opinion Starts Here ----------------------------------------->
    classifier = pickle.load(open('classifier-MaxentClassifier.rotten.pickle', 'r'))
    tokens = bag_of_words(extract_words(string))
    decision = classifier.classify(tokens)
    subjective = classifier.prob_classify(tokens).prob('subjective')
    objective = classifier.prob_classify(tokens).prob('objective')
    results_json['Subjectivity'] = subjective
    results_json['Objectivity'] = objective
    #Classify Opinion Ends Here ----------------------------------------->

    #NLTK Classifiers Starts Here ----------------------------------------->
    if not classifier_name == "WSD-SentiWordNet" or len(classifier_name.split()) > 1:
       pickled_classifiers = ['classifier-%s.%s.pickle'%(c_name, domain) for c_name in classifier_name.split()]
       for pickled_classifier in pickled_classifiers:
       	   if not os.path.exists(pickled_classifier): 
	      continue
       	   classifier = pickle.load(open(pickled_classifier, 'r'))
       	   tokens = bag_of_words(extract_words(string))
       	   decision = classifier.classify(tokens)
       	   neg = classifier.prob_classify(tokens).prob('neg')
       	   pos = classifier.prob_classify(tokens).prob('pos')
    #NLTK Classifiers Ends Here ----------------------------------------->

    #WSD Hue Starts Here ----------------------------------------->
    if classifier_name == "WSD-SentiWordNet" or len(classifier_name.split()) > 1:
       from classifySentiments import call_classifier, line_wn
       pos, neg = call_classifier(lines_list)
       normalize_wsd = pos + neg + 1
       pos = pos/normalize_wsd
       neg = neg/normalize_wsd
    results_json['Pos'] = pos
    results_json['Neg'] = neg
    print json.dumps(results_json)
    #WSD Hue ENDS Here ----------------------------------------->
    
if __name__ == "__main__":
    WSGIServer(app).run() 

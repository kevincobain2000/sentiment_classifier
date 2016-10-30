#!/home/s1010205/bin/python2.7
# -*- coding: utf-8 -*
from __future__ import division, print_function

from __init__ import *
import cPickle as pickle
import datetime
from nltk_classifiers import *


def out_results(pos, neg, print_score=False):
    if abs(pos - neg) <= 0.15 and neg != 0 and pos != 0:
        print("<br>Text is <tt>Neutral/Hard To Classify</tt></br>")
        print('<tt>Positive = %s<b><br>Negative = %s</b></tt>'%(pos, neg))
    elif pos > neg:
        print(" Text is <tt><FONT COLOR=\"green\">POSITIVE</FONT></tt> <br>")
        if print_score:
            print('<tt><b>Positive = %s</b><br>Negative = %s</tt>'%(pos,neg))
    else:
        print(" Text is <tt><FONT COLOR=\"red\">NEGATIVE</FONT></tt> <br>")
        if print_score:
            print('<tt>Positive = %s<b><br>Negative = %s</b></tt>'%(pos,neg))
    print('<br>')


form = cgi.FieldStorage()


def app(environ, start_response):
  start_response('200 OK', [('Content-Type', 'text/html')])
  parameters = parse_qs(environ.get('QUERY_STRING', ''))
  yield " "
  if 'subject' in parameters: 
     subject = escape(parameters['subject'][0])

  FORM = open('senti_form.html').read()
  if not form.has_key("textcontent"): yield FORM #will be printed at the begining
  sent1 = form.getvalue("textcontent")
  classifier = pickle.load(open('classifier-MaxentClassifier.rotten.pickle', 'r'))
  if form.has_key("textcontent"):
    domain = form["dropdown"].value
    classifier_name = form["classifier"].value
    pos = neg = 0
    f = open("logs/log",'a+')
    if not sent1.startswith('It was one of the bad'):
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M")
        f.write("\nEntry:%s"%date_time)
        f.write(" %s %s"%(domain,classifier_name))
        f.write("\n%s\n"%sent1)
    print(FORM)
    r = re.compile("[,.?()\\d]+ *")
    lines_list = r.split(sent1)
    
    #Classify Opinion Starts Here ----------------------------------------->
    tokens = bag_of_words(extract_words(sent1))
    decision = classifier.classify(tokens)
    subjective = classifier.prob_classify(tokens).prob('subjective')
    objective = classifier.prob_classify(tokens).prob('objective')
    if subjective > objective:
       print("<br><tt><b>Subjectivity = %s</b><br>Objectivity &nbsp;= %s</tt>"%(subjective, objective))
    else: print("<br><tt>Subjectivity = %s<br><b>Objectivity &nbsp;= %s</b></tt>"%(subjective, objective))
    print("<hr><br>")
    #Classify Opinion Ends Here ----------------------------------------->

    #NLTK Classifiers Starts Here ----------------------------------------->
    if not classifier_name == "WSD-SentiWordNet" or len(classifier_name.split()) > 1:
       pickled_classifiers = ['classifier-%s.%s.pickle'%(c_name, domain) for c_name in classifier_name.split()]
       for pickled_classifier in pickled_classifiers:
       	   if not os.path.exists(pickled_classifier): 
	      continue
       	   classifier = pickle.load(open(pickled_classifier, 'r'))
       	   tokens = bag_of_words(extract_words(sent1))
       	   decision = classifier.classify(tokens)
       	   neg = classifier.prob_classify(tokens).prob('neg')
       	   pos = classifier.prob_classify(tokens).prob('pos')

       	   print("<br>Results from %s on <tt>%s</tt> Corpus</br>"%(pickled_classifier.split('.')[0],domain))
       	   out_results(pos,neg, print_score=True)
    #NLTK Classifiers Ends Here ----------------------------------------->

    #WSD Hue Starts Here ----------------------------------------->
    if classifier_name == "WSD-SentiWordNet" or len(classifier_name.split()) > 1:
       from classifySentiments import call_classifier, line_wn
       pos, neg = call_classifier(lines_list)
       normalize_wsd = pos + neg + 1
       pos = pos/normalize_wsd
       neg = neg/normalize_wsd
    
       print("<br>Results from WSD SentiWordNet on <tt>%s</tt> Corpus</br>"%domain)
       out_results(pos,neg, print_score=True)
    #WSD Hue ENDS Here ----------------------------------------->
    
if __name__ == "__main__":
  WSGIServer(app).run() 

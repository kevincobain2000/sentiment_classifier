.. raw:: html

  <HEAD>
    <LINK href="http://www.jaist.ac.jp/~s1010205/gh-buttons.css" rel="stylesheet" type="text/css">
  </HEAD>

.. raw:: html

  <br><a href="http://www.jaist.ac.jp/~s1010205" class="button icon home">Back to Home</a>
  <p><iframe src="http://www.jaist.ac.jp/~s1010205/github-btn.html?user=kevincobain2000&repo=sentiment_classifier&type=watch&count=true&size=large" allowtransparency="true" frameborder="0" scrolling="0" width="165px" height="30px"></iframe></p>
  
iPhone App for Twitter Sentiments is Out
----------------------------------------

https://itunes.apple.com/us/app/emotion-calculator-for-twitter/id591404584?ls=1&mt=8

App no longer available



Sentiment Classification using WSD, Maximum Entropy & Naive Bayes Classifiers
=============================================================================

- pip install sentiment_classifier
- `Home <http://www.jaist.ac.jp/~s1010205/>`_
- `pypi package <http://pythonpackages.com/package/sentiment_classifier>`_
- `Github <https://github.com/kevincobain2000/sentiment_classifier>`_

Overview
--------

Sentiment Classifier using Word Sense Disambiguation using ``wordnet`` and word occurance
statistics from movie review corpus ``nltk``. For twitter sentiment analysis bigrams are used as 
features on Naive Bayes and Maximum Entropy Classifier from the twitter data. Classifies into positive and negative labels.
Next is use senses instead of tokens from the respective data.

.. raw:: html

  <br><a href="https://github.com/downloads/kevincobain2000/sentiment_classifier/sentiment_classifier-0.5.tar.gz" class="button icon arrowdown">sentiment_classifier-0.5.tar.gz</a>
  <br><iframe src="http://www.jaist.ac.jp/~s1010205/cgi-bin/pypi-git-stats/stats.cgi?pypi=sentiment_classifier&gituser=kevincobain2000&repo=sentiment_classifier" allowtransparency="true" frameborder="0" scrolling="0" width="180px" height="45px"></iframe>

`Download Stats Provided by` `pypi-github-stats <http://www.jaist.ac.jp/~s1010205/pypi-git-stats/>`_

Sentiment Classifiers and Data
------------------------------

   The above online demo uses movie review corpus from nltk, twitter and Amazon,on which Naive Bayes classifier is trained. Classifier using WSD SentiWordNet is based on heuristics and uses WordNet and SentiWordNet. Test results on sentiment analysis on twitter and amazon customer reviews data & features used for NaiveBayes will be `Github <https://github.com/kevincobain2000/sentiment_classifier>`_.

Requirements
------------

In ``Version 0.5`` all the following requirements are installed automatically. In case of troubles install those manually.

- You must have Python 2.6.
- NLTK http://www.nltk.org  2.0 installed. 
- NumPy http://numpy.scipy.org
- SentiWordNet http://sentiwordnet.isti.cnr.it 


How to Install
--------------

Shell command ::

  python setup.py install

Documentation
-------------

- http://readthedocs.org/docs/sentiment_classifier/en/latest/

Script Usage
------------

Shell Commands::

  senti_classifier -c file/with/review.txt

Python Usage
------------

Shell Commands ::

  cd sentiment_classifier/src/senti_classifier/
  python senti_classifier.py -c reviews.txt

Library Usage
-------------

.. code-block:: python
  
    from senti_classifier import senti_classifier
    sentences = ['The movie was the worst movie', 'It was the worst acting by the actors']
    pos_score, neg_score = senti_classifier.polarity_scores(sentences)
    print pos_score, neg_score

    ... 0.0 1.75

.. code-block:: python

  from senti_classifier.senti_classifier import synsets_scores
  print synsets_scores['peaceful.a.01']['pos']
  
  ... 0.25


History
=======

- ``0.6`` Bug Fixed upon nltk upgrade
- ``0.5`` No additional data required trained data is loaded automatically. Much faster/Optimized than previous versions.
- ``0.4`` Added Bag of Words as a Feature as occurance statistics
- ``0.3`` Sentiment Classifier First app, Using WSD module


.. include:: run_time.rst
.. include:: disqus_jnlp.html.rst

.. raw:: html

  <HEAD>
    <LINK href="http://www.jaist.ac.jp/~s1010205/gh-buttons.css" rel="stylesheet" type="text/css">
  </HEAD>

.. raw:: html

  <br><a href="http://www.jaist.ac.jp/~s1010205" class="button icon home">Back to Home</a>


Sentiment Classification using WSD
==================================

- ``pip install sentiment_classifier``
- `Home <http://www.jaist.ac.jp/~s1010205/>`_
- `Download <http://pythonpackages.com/package/sentiment_classifier>`_
- `Github <https://github.com/kevincobain2000/sentiment_classifier>`_
- `Try Online <http://www.jaist.ac.jp/~s1010205/sentiment_classifier/>`_


Overview
--------

Sentiment Classifier using Word Sense Disambiguation using ``wordnet`` and word occurance
statistics from movie review corpus ``nltk``. Classifies into positive and negative categories.

Online Demo
-----------

.. raw:: html

   <script language="JavaScript"> 
   <!-- 
   function calcHeight() 
   { //find the height of the internal page 
   var the_height= document.getElementById('the_iframe').contentWindow. 
   document.body.scrollHeight;  
   //change the height of the iframe 
   document.getElementById('the_iframe').height= 
   the_height; 
   } 
   //--> 
   </script>

   <iframe width="100%" id="the_iframe" onLoad="calcHeight();" src="http://www.jaist.ac.jp/~s1010205/cgi-bin/senti_classifier/sentiment_classifier.cgi" scrolling="NO" frameborder="0" height="2"></iframe>


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
- `Try Online <http://www.jaist.ac.jp/~s1010205/sentiment_classifier/>`_
  

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



History
=======

- ``0.5`` No additional data required trained data is loaded automatically. Much faster/Optimized than previous versions.
- ``0.4`` Added Bag of Words as a Feature as occurance statistics
- ``0.3`` Sentiment Classifier First app, Using WSD module


.. include:: run_time.rst
.. include:: disqus_jnlp.html.rst

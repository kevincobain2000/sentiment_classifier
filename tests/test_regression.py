# The idea of those tests is that we have some
# results obtained from the previous runs of the classifier
# and we make sure that they do not change from time to time

import json
import unittest

from senti_classifier import senti_classifier


class RegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reviews_file = "reviews.json"
        cls.reviews_data = cls._read_reviews_data(cls.reviews_file)

    @classmethod
    def _read_reviews_data(cls, reviews_file):
        data = {"reviews": []}
        with open(reviews_file) as f:
            data = json.load(f)
        return data

    def test_against_data(self):
        for r in self.reviews_data['reviews']:
            sentences = [s.strip() for s in r['text'].split(".")]
            pos_score, neg_score = senti_classifier.polarity_scores(sentences)
            self.assertEqual(pos_score, r['pos'])
            self.assertEqual(neg_score, r['neg'])


if __name__ == '__main__':
    unittest.main()

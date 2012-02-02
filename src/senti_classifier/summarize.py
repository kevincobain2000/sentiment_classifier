#!/usr/bin/python
from collections import defaultdict
from itertools import repeat
import re

class Summary(object):
    def __init__(self):
        pass

    def tokenize(self, text):
        return text.split()

    def split_to_sentences(self, text):
        sentences = []
        start = 0
        for match in re.finditer("(\s*[.!?]\s*)|(\n{2,})", text):
            sentences.append(text[start:match.end()].strip())
            start = match.end()
        if start < len(text):
            sentences.append(text[start:].strip())
        return sentences

    def token_frequency(self, text):
        '''Return frequency (count) for each token in the text'''
        frequencies = defaultdict(repeat(0).next)
        for token in self.tokenize(text):
            frequencies[token] += 1
        return frequencies

    def sentence_score(self, sentence, frequencies):
        return sum((frequencies[token] for token in self.tokenize(sentence)))

    def create_summary(self, sentences, max_length):
        summary = []
        size = 0
        for sentence in sentences:
            size += len(sentence)
            if size >= max_length: break
            summary.append(sentence)
        return "\n".join(summary)

    def summarize(self, text, max_summary_size):
        frequencies = self.token_frequency(text)
        sentences = self.split_to_sentences(text)
        sentences.sort(key=lambda s: self.sentence_score(s, frequencies), reverse=1)
        summary = self.create_summary(sentences, max_summary_size)
        return summary

if __name__ == "__main__":
    
    raw_text = """you know , i've seen network before , and it's a much better film . bulworth is , in the kindest of words , an " homage " to that picture , and at least it has an excellent role model . simply take the story about a tv newsman who goes nuts , stirs up controversy , and fatally angers the establishment and change it to a us senator who does the same thing , and you've got bulworth . warren beatty's title role performance is the only reason bulworth has anything going for it at all . much like tom cruise in jerry maguire , beatty takes a difficult character and makes it his own , and while beatty as a foul-mouthed politician is not exactly playing against type , it's still his very aggressive performance that carries the picture . everything else , from the dismal supporting cast ( halle berry has never looked so lost ) to the throw-away one-liners ( you've seen all the best over and over again on the trailers ) is cut-and-pasted from network or clearly dredged from some late night rewrite session . still , beatty's in fine form , and his outrageous wackiness takes the film halfway to where it could have been . ( and geez , he directed , produced , wrote , and starred in the film . . . maybe someone was a little too busy ? ) but overall , the missed opportunities , the overtly silly anti-pc message backed up by nothing , and the all-too-forseeable ending make bulworth little more than a fable that we already knew : that anyone involved with politics is totally insane . """
    s= Summary()
    MAX_SUMMARY_SIZE = len(raw_text)/3
    print s.summarize(raw_text, MAX_SUMMARY_SIZE)

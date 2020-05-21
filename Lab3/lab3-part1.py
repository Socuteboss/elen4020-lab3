
# Determines the number of times a word occurs in a text, 
# Ignores stop words. It is case sensitive"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r"[\w']+")


class WordFreqCount(MRJob):
    FILES = ['stop_words.txt']

    def mapper_init(self):
        stop_words_path = 'stop_words.txt'

        with open(stop_words_path) as f:
            self.stop_words = set(line.strip() for line in f) #get all relevant stop words

    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            word = word.lower() #to make case-insensitive
            if word not in self.stop_words:
                yield (word, 1) #checks for word in a line

    def reducer(self, word, counts):
        yield (word, sum(counts))

if __name__ == '__main__':
    WordFreqCount.run()


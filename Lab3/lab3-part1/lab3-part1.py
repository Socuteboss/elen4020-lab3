
from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r"[\w']+")


class WordCount(MRJob):

    """Determines the number of times a word occurs in a text, 
    Ignores stop words. It is case sensitive"""

    def mapper(self, _, line):
        stop_words_file = '/Users/reegz/Documents/ELEC ENG 2020/BigData/Labs/Lab3/code/elen4020-lab3/Lab3/lab3-part1/stopwords.txt'

        # Obtain stop words
        with open(stop_words_file) as f:
            self.stop_words = set(line.strip() for line in f)
            for word in WORD_RE.findall(line):
                if word not in self.stop_words:
                   yield (word, 1)
   

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))

if __name__ == '__main__':
    WordCount.run()


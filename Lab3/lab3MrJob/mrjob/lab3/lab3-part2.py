
# Determine the K most used words in an body of text, ignoring common "stop" words.

import re

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.protocol import JSONProtocol
from mrjob.step import MRStep

WORD_RE = re.compile(r"[\w']+")


class TopKQuery(MRJob):
    FILES = ['stop_words.txt']

    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper_init(self):
        stop_words_path = 'stop_words.txt'
        # obtain stop words
        with open(stop_words_path) as f:
            self.stop_words = set(line.strip() for line in f)

    def get_words_map(self, _, line):
        # allocate count to each word in the line
        for word in WORD_RE.findall(line):
            word = word.lower()
            if word not in self.stop_words:
                yield (word, 1)

    def combiner(self, word, counts):
        # combine words sum count into a tuple
        yield (word, sum(counts))

    def reducer(self, word, counts):
        # reduce map and sums results
        yield None, (sum(counts), word)

    def reducer_K_words(self, _, word_count_pairs):
        try:
            yield None, sorted(word_count_pairs, key=lambda t: t[0], reverse=True)[:20] #limits number of words returned
        except ValueError:
            pass

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.get_words_map,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_K_words)
        ]


if __name__ == '__main__':
    TopKQuery.run()

from mrjob.job import MRJob
import re


class InvertedIndex(MRJob):
    FILES = ['search_words.txt']

    def mapper_init(self):
        search_words_path = 'search_words.txt'

        with open(search_words_path) as f:
            self.search_words = set(line.strip() for line in f)

    def mapper_pre_filter(self):
        return 'grep -n ""' #Used to add line numbers when reading in the file

    def mapper(self, _, line):
        line_number = line.split(':')[0]
        clean_line = line[line.index(':')+1:]
        clean_line = re.sub(r'[^\w\s]','',clean_line) #remove punctuation from line
        for word in clean_line.split():
            word = word.lower()
            if word in self.search_words:
                yield word, line_number

    def reducer(self, key, values):
        yield key, list(values)[:50] #limit to 50 outputs


if __name__ == '__main__':
    InvertedIndex.run()
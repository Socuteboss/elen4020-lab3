import mrs
import string

class WordCount(mrs.MapReduce):
    """Determines the number of times a word occurs in a text

    Ignores stop words and is not case sensitive

    To run use: python3 lab3-part1.py "very_large.txt" out
    you will find your output in the output directory out
    """
    def map(self, key, value):
        for word in value.split():
            word = word.strip(string.punctuation)
            if word not in ['for', 'as', 'the', 'is', 'at', 'which', 'on']:
                yield (word, 1)

    def reduce(self, key, values):
        yield sum(values)

if __name__ == '__main__':
    mrs.main(WordCount)


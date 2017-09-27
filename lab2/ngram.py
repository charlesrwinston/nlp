# ngram.py
#   Lab 2 for COMP 150 NLP
#   by Charles Winston
#   9/25/17
#
#   Main program for Lab 2. Computes a bigram model from the Bible
#   and compares the writings of Shakespeare and Herman Melville to
#   the Bible based on that model. The "loser" of the prediction then
#   gets a model made for himself, and then the remaining two works
#   are compared to his writing the same way.

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import gutenberg
import models
import predictions
import sys

# Converts text string read by gutenberg to name to print
def corpusstr2name(str):
    if (str == 'bible-kjv.txt'):
        return "The Bible"
    elif (str == 'shakespeare-hamlet.txt'):
        return "Shakespeare"
    elif (str == 'melville-moby_dick.txt'):
        return "Herman Melville"

def losers_turn(model_text, compare_text1, compare_text2, n):
    # Create model
    table, vocab_size = models.ngram(gutenberg.words(model_text), n)
    model = {
        'table': table,
        'vocab_size': vocab_size
    }

    # Make predictions
    compare1 = gutenberg.sents(compare_text1)
    compare2 = gutenberg.sents(compare_text2)

    if (predictions.prediction(model, compare1, compare2, n) == compare1):
        print(corpusstr2name(compare_text1) + " can sit with " + corpusstr2name(model_text))
    else:
        print(corpusstr2name(compare_text2) + " can sit with " + corpusstr2name(model_text))


def main():
    n = int(sys.argv[1])
    # Create bigram model from Bible
    table, vocab_size = models.ngram(gutenberg.words('bible-kjv.txt'), n)
    bible_model = {
        'table': table,
        'vocab_size': vocab_size
    }

    # Make predictions
    shakespeare = gutenberg.sents('shakespeare-hamlet.txt')
    melville = gutenberg.sents('melville-moby_dick.txt')

    if (predictions.prediction(bible_model, shakespeare, melville, n) == shakespeare):
        print("Shakespeare can sit with the Bible")
        losers_turn('melville-moby_dick.txt', 'shakespeare-hamlet.txt', 'bible-kjv.txt', n)
    else:
        print("Herman Melville can sit with the Bible")
        losers_turn('shakespeare-hamlet.txt', 'melville-moby_dick.txt', 'bible-kjv.txt', n)



if __name__ == '__main__':
    main()

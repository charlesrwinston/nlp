from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import gutenberg

def main():
    shakespeare = gutenberg.words('shakespeare-hamlet.txt')
    melville = gutenberg.words('melville-moby_dick.txt')
    bible = gutenberg.words('bible-kjv.txt')

    words = word_tokenize("I I am am a a a sucker stupid ass ass ass ass ass I am I am I am hey.")

    print(bigram(words))

# Text is a list of words
def bigram(text):
    countTable = {}

    for i in range(len(text)):
        countTable.setdefault(text[i], {})
        countTable[text[i]].setdefault(text[i-1], 0)
        if (i != 0):
            count = countTable[text[i]][text[i-1]] + 1
            countTable[text[i]][text[i-1]] = count

    return calcProbs(countTable, laplace)

def calcProbs(countTable, smoothing):
    vocab = len(countTable)
    for key1 in countTable:
        total = 0
        # add up the totals
        for key2 in countTable[key1]:
            total += countTable[key1][key2]
        # compute probabilities using Laplace smoothing
        for key2 in countTable[key1]:
            countTable[key1][key2] = smoothing(countTable[key1][key2], total, vocab)

    return countTable

def laplace(count, n, v):
    return (count + 1) / float(n + v)

if __name__ == '__main__':
    main()

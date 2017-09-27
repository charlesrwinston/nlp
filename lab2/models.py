# models.py
#   Lab 2 for COMP 150 NLP
#   by Charles Winston
#   9/25/17
#
#   Definitions for ngram model procedures

def ngram(words, n):
    countTable = {}
    vocab = set(words)

    for i in range(n - 1, len(words)):
        if (n == 2):
            key = words[i-1]
        else:
            key = ()
            for j in range(1, n):
                key += (words[i-j],)
        countTable.setdefault(key, {})
        countTable[key].setdefault(words[i], 0)
        count = countTable[key][words[i]] + 1
        countTable[key][words[i]] = count

    return calcProbs(countTable, laplace, len(vocab)), len(vocab)

def calcProbs(countTable, smoothing, vocab_size):
    for key1 in countTable:
        total = 0
        # add up the totals
        for key2 in countTable[key1]:
            total += countTable[key1][key2]
        # compute probabilities
        for key2 in countTable[key1]:
            countTable[key1][key2] = smoothing(countTable[key1][key2], total, vocab_size)

    return countTable

def laplace(count, n, v):
    return (count + 0.1) / float(n + v * 0.1)

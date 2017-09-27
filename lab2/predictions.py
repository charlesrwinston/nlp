# predictions.py
#   Lab 2 for COMP 150 NLP
#   by Charles Winston
#   9/25/17
#
#   Definitions for author similarity prediction procedures

import numpy as np
import sys
from models import laplace


def prediction(model, author1, author2, n):
    if (likelihood(model, author1, n) > likelihood(model, author2, n)):
        return author1
    else:
        return author2

def likelihood(model, sents, n):
    probabilities = np.empty(len(sents))
    for i in range(len(sents)):
        words = sents[i]
        probabilities[i] = prob(model, words, n)

    result = np.mean(probabilities, dtype=np.float64)
    print(result)
    return result

def prob(model, words, n):
    if ((n - 1) >= len(words)):
        probability = laplace(0, 0, model['vocab_size'])
    else:
        probability = 1.0
    for i in range(n - 1, len(words)):
        if (n == 2):
            key = words[i-1]
        else:
            key = ()
            for j in range(1, n):
                key += (words[i-j],)
        if (key in model['table']) and (words[i] in model['table'][key]):
            probability *= model['table'][key][words[i]]
        else:
            probability *= laplace(0, 0, model['vocab_size'])
    #print(probability)

    return probability

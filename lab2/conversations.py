# conversations.py
#   Lab 2 for COMP 150 NLP
#   by Charles Winston
#   9/25/17
#
#   Generate sample conversations based on bigram models
import models
import random
import re
from nltk import pos_tag
from nltk.corpus import gutenberg


def is_noun_or_verb(word_pos):
    return ((word_pos[1] == 'NN') or (word_pos[1] == 'VB'))

def wordlist2sentence(words):
    punctuation = re.compile(r'[.,;:!?)]')
    sentence = words[0]
    for w in words[1:]:
        if punctuation.match(w):
            sentence += w
        else:
            sentence += " " + w
    return sentence

def predict_word(words, nouns_n_verbs):
    # random floats between 0 and 1
    rand1 = random.random()
    rand2 = random.random()
    total = 0
    for key in words:
        total += words[key]
        if nouns_n_verbs:
            if (key in nouns_n_verbs) and (rand1 <= rand2):
                return key
        if (rand1 <= total):
            return key

    return key

def generate_sentence(model, nouns_n_verbs):
    random.seed()
    words = []
    word = predict_word(model['.'], nouns_n_verbs)
    while (word != '.'):
        words.append(word)
        word = predict_word(model[word], nouns_n_verbs)

    words.append(word)
    sentence = wordlist2sentence(words)
    return sentence, pos_tag(words)

def generate_conversation(model1, model2, name1, name2, length):
    convo = ""
    nouns_n_verbs = None
    for i in range(int(length / 2)):
        sentence, pos_tags = generate_sentence(model1, nouns_n_verbs)
        nouns_n_verbs = [x[0] for x in pos_tags if is_noun_or_verb(x)]
        convo += name1.upper() + ":\n" + sentence + "\n"
        sentence, pos_tags = generate_sentence(model2, nouns_n_verbs)
        nouns_n_verbs = [x[0] for x in pos_tags if is_noun_or_verb(x)]
        convo += name2.upper() + ":\n" + sentence + "\n"
    return convo

def main():
    # A conversation between The Bible and Shakespeare
    convo1 = open('convo1.txt', 'w')
    convo1.write(generate_conversation(models.ngram(gutenberg.words('bible-kjv.txt'), 2)[0], models.ngram(gutenberg.words('shakespeare-hamlet.txt'), 2)[0], "The Bible", "Shakespeare", 6))
    # A conversation between Herman Melville and Shakespeare
    convo2 = open('convo2.txt', 'w')
    convo2.write(generate_conversation(models.ngram(gutenberg.words('melville-moby_dick.txt'), 2)[0], models.ngram(gutenberg.words('shakespeare-hamlet.txt'), 2)[0], "Herman Melville", "Shakespeare", 6))



if __name__ == '__main__':
    main()

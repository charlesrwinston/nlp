# Winston_Lab0.py
# Charles Winston
# September 7 2017

from nltk.corpus import gutenberg

def flip2flop():
    flip = open("flip.txt", "r")
    flop = open("flop.txt", "w")
    flip_text = flip.read()

    flop.write(reverse_chars(flip_text) + "\n")
    flop.write(reverse_words(flip_text) + "\n")

    emma = gutenberg.words('austen-emma.txt')
    flop.write(str(len(emma)) + "\n")

    flop.write("Word.\n")
    flop.write("It's lit.\n")

def reverse_chars(sentence):
    length = len(sentence)
    new_sentence = ""
    for i in range(length):
        new_sentence += sentence[length - 1 - i]
    return new_sentence

def reverse_words(sentence):
    words = get_words(sentence)
    len_words = len(words)
    new_sentence = ""
    for i in range(len_words):
        new_sentence += words[len_words - 1 - i]
        if (i != (len_words - 1)):
            new_sentence += " "
    return new_sentence

def get_words(sentence):
    length = len(sentence)
    words = []
    temp_word = ""
    for i in range(length):
        if sentence[i].isspace():
            words.append(temp_word)
            temp_word = ""
        elif (i == (length - 1)):
            temp_word += sentence[i]
            words.append(temp_word)
        else:
            temp_word += sentence[i]
    return words


if __name__ == '__main__':
    flip2flop()

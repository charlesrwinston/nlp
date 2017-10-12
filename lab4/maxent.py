# maxent.py
import sys
import xml.etree.ElementTree as et
from nltk.classify import MaxentClassifier, accuracy
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import random
import operator

# constants
REVIEW_TEXT_TRAIN = 10
REVIEW_TEXT_TEST = 9
TITLE_TRAIN = 6
TITLE_TEST = 5
RATING = 5
ASIN = 1

# returns list of most common adjectives and adverbs used in negative/positive
# reviews, paired with a negative or positive count which represents the word's
# net negative or positive use
def get_top_adjs_n_advs(train_labels, threshold):
    adjs_n_advs = {}    # list of adjectives and adverbs
    prev = ''           # previous word, used for capturing negation
    negation = [        # list of negation words
        'not',
        'n\'t',
        'never',
    ]
    for pair in train_labels:
        review = pair[0]
        label = pair[1]
        text = review[TITLE_TRAIN].text + ' ' + review[REVIEW_TEXT_TRAIN].text
        words = word_tokenize(text)
        for pair in pos_tag(words):
            word = pair[0]
            tag = pair[1]
            # capture negation
            if word.lower() in negation:
                prev = word + ' '
            else:
                # capture adjectives and adverbs
                if (tag == 'RB') or (tag == 'JJ'):
                    word = prev + word
                    count = adjs_n_advs.setdefault(word, 0)
                    # add if label positive, subtract if label negative
                    #   this results in counts which represent a word's
                    #   net positive or negative use
                    if label == '+':
                        adjs_n_advs[word] += 1
                    else:
                        adjs_n_advs[word] -= 1
                prev = ''
    # filter for only words with abs(count) >= threshold, meaning that the word appears
    # at least threshold more times in negative reviews than positive reviews, or vice versa
    return [ word for word, count in adjs_n_advs.items() if abs(count) > threshold ]

def get_sentiment(rating):
    sentiment = {
        1: 'Negative',
        2: 'Negative',
        4: 'Positive',
        5: 'Positive'
    }
    rating = int(float(rating))
    return sentiment[rating]

def get_review_text(review, train_or_test):
    if train_or_test == 'train':
        return review[REVIEW_TEXT_TRAIN]
    else:
        return review[REVIEW_TEXT_TEST]

def get_label(review, train_or_test):
    if train_or_test == 'train':
        return review, get_sentiment(review[RATING].text)
    else:
        return review

# features are the counts of individual adjectives and adverbs that appear in
# the review's text and title
def get_features(review, train_or_test, top_adjs_and_advs):
    if train_or_test == 'train':
        text = review[TITLE_TRAIN].text + ' ' + review[REVIEW_TEXT_TRAIN].text
    else:
        text = review[TITLE_TEST].text + ' ' + review[REVIEW_TEXT_TEST].text

    words = word_tokenize(text)
    features = {}
    adjs_n_advs = []    # list of adjectives and adverbs
    prev = ''           # previous word, used for capturing negation
    negation = [        # list of negation words
        'not',
        'n\'t',
        'never',
    ]
    for pair in pos_tag(words):
        word = pair[0]
        tag = pair[1]
        # capture negation
        if word.lower() in negation:
            prev = word + ' '
        else:
            # capture adjectives and adverbs
            if (tag == 'RB') or (tag == 'JJ'):
                word = prev + word      # prev is empty unless previous word was negation
                adjs_n_advs.append(word)
            prev = ''

    for w in adjs_n_advs:
        if w in top_adjs_and_advs:
            features[w] = text.count(w)
    return features

def print_results(classifier, test_set):
    for pair in test_set:
        features = pair[0]
        review_id = pair[1]
        # the [1:-1] is used to cut off the newlines at the beginning and end of the ID string
        print(review_id[1:-1] + '\t' + classifier.classify(features))

def main():
    # grab xml trees
    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    train_tree = et.parse(train_filename)
    test_tree = et.parse(test_filename)
    train_root = train_tree.getroot()
    test_root = test_tree.getroot()

    # labeled reviews
    train_labels = [get_label(review, 'train') for review in train_root]
    test_labels = [get_label(review, 'test') for review in train_root]

    top_adjs_and_advs = get_top_adjs_n_advs(train_labels, 2)

    # randomize
    random.shuffle(train_labels)
    random.shuffle(test_labels)

    # feature sets
    train_set = [(get_features(review, 'train', top_adjs_and_advs), label) for review, label in train_labels]
    test_set = [(get_features(review, 'test', top_adjs_and_advs), review[ASIN].text) for review in test_labels]

    # train classifier
    classifier = MaxentClassifier.train(train_set, trace=0)

    # print results
    print_results(classifier, test_set)


if __name__ == "__main__":
    main()

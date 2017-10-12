# maketest.py
import random
import xml.etree.ElementTree as et


def get_rand_review(train_reviews):
    random.seed()
    rand = random.randint(0, len(train_reviews) - 1)
    return train_reviews[rand]

def get_train_n_test_text(full, num_test):
    full_root = full.getroot()

    test_reviews = []
    train_reviews = []

    for child in full_root:
        train_reviews.append(child)

    for i in range(num_test):
        review = get_rand_review(train_reviews)
        test_reviews.append(review)
        train_reviews.remove(review)

    train = et.Element('reviews')
    test = et.Element('reviews')

    for review in train_reviews:
        train.append(review)

    for review in test_reviews:
        review.remove(review.find('rating'))
        test.append(review)


    return et.tostring(train, encoding='utf-8'), et.tostring(test, encoding='utf-8')

def main():
    full = et.parse("FullSet.xml")
    train = open("TrainingSet.xml", "wb")
    test = open("TestSet.xml", "wb")

    num_test = 950
    train_text, test_text = get_train_n_test_text(full, num_test)

    train.write(train_text)
    test.write(test_text)


if __name__ == "__main__":
    main()

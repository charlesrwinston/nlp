# regxml.py
#   Lab 1 for COMP 150 NLP
#   by Charles Winston
#   9/20/17
#
#   Uses regular expressions and sentence tokenizing from nltk
#   to convert raw text format of The Blithedale Romance by
#   Nathaniel Hawthorne to xml format with helpful tags that
#   identify structural components of the novel. Also tags
#   sentences that mention important characters and themes.

import re
from nltk.tokenize import sent_tokenize
from tagging import insertTag, sub, split, sent

# Tags each structural component
def structuralTags(blithedale_xml):
    # pattern objects for each xml tag
    book = re.compile(r"(^.+$)", re.DOTALL)
    booktitle = re.compile(r"(The Blithedale Romance)")
    author = re.compile(r"(Nathanial Hawthorne)")
    chapter = re.compile(r"(\n\n\n)")
    chaptertitle = re.compile(r"([A-Z][A-Z ',]{4,})")
    paragraph = re.compile(r"(\n\n)")
    quote = re.compile(r"(\"[^\"]+\")")

    # dictionary mapping patterns to a triple of the form:
    #       (openTag, closeTag, tagging_method)
    patterns = {
        book: ("<book>", "</book>", sub),
        booktitle: ("<booktitle>", "</booktitle>", sub),
        author: ("<author>", "</author>", sub),
        chapter: ("<chapter>", "</chapter>", split),
        chaptertitle: ("<chaptertitle>", "</chaptertitle>", sub),
        paragraph: ("<paragraph>", "</paragraph>", split),
        quote: ("<quote>", "</quote>", sub)
    }

    for p in patterns:
        blithedale_xml = insertTag(p, blithedale_xml, patterns[p][0], patterns[p][1], patterns[p][2])

    return blithedale_xml

# Tags sentences that mention each main character
def contentTags(blithedale_xml):
    # pattern objects for content tags:

    # characters
    miles_coverdale = re.compile(r"(Mr\. )?(Miles )?Coverdale")
    old_moodie = re.compile(r"([Oo]ld )?(Mr\. )?Moodie")
    veiled_lady = re.compile(r"([Tt]he )?Veiled Lady")
    hollingsworth = re.compile(r"(Hollingsworth)")
    silas_foster = re.compile(r"(Mr\. )?(Silas )?Foster")
    mrs_foster = re.compile(r"(Mrs\. Foster)")
    zenobia = re.compile(r"(Zenobia)")
    priscilla = re.compile(r"(Priscilla)")
    prof_westervelt = re.compile(r"(Professor )?Westervelt")

    # symbols
    flower = re.compile(r"flower")
    veil = re.compile(r"veil")
    sickness = re.compile(r"(sick|[\n \"]ill[\n \.,\"])")
    dreams = re.compile(r"dream")

    # dictionary mapping character patterns to a pair of their xml tags
    content = {
        # main characters
        miles_coverdale: ("<miles_coverdale>", "</miles_coverdale>"),
        old_moodie: ("<old_moodie>", "</old_moodie>"),
        veiled_lady: ("<veiled_lady>", "</veiled_lady>"),
        hollingsworth: ("<hollingsworth>", "</hollingsworth>"),
        silas_foster: ("<silas_foster>", "</silas_foster>"),
        mrs_foster: ("<mrs_foster>", "</mrs_foster>"),
        zenobia: ("<zenobia>", "</zenobia>"),
        priscilla: ("<priscilla>", "</priscilla>"),
        prof_westervelt: ("<prof_westervelt>", "</prof_westervelt>"),

        # symbols
        flower: ("<flower>", "</flower>"),
        veil: ("<veil>", "</veil>"),
        sickness: ("<sickness>", "</sickness>"),
        dreams: ("<dreams>", "</dreams>")
    }

    blithedale_sents = sent_tokenize(blithedale_xml)

    for c in content:
        blithedale_xml = insertTag(c, blithedale_xml, content[c][0], content[c][1], sent, blithedale_sents)

    return blithedale_xml


def main():
    # get blithedale romance string
    blithedale_file = open("Blithedale_Romance.txt", "r")
    blithedale_xml = blithedale_file.read()

    # Content tags (characters, symbols), part 3
    blithedale_xml = contentTags(blithedale_xml)

    # Structural tags, parts 1 and 2
    blithedale_xml = structuralTags(blithedale_xml)

    output = open("blithedale.xml", "w")
    output.write(blithedale_xml)



if __name__ == '__main__':
    main()

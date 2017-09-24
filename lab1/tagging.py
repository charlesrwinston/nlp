# tagging.py
#   Lab 1 for COMP 150 NLP
#   by Charles Winston
#   9/20/17
#
#   Definitions for tagging procedures

import re

# Wrapper for tagging method
def insertTag(pattern, blithedale_xml, openTag, closeTag, tagging_method, rest=None):
    return tagging_method(pattern, blithedale_xml, openTag, closeTag, rest)

# Tag by substituting string
def sub(pattern, blithedale_xml, openTag, closeTag, rest):
    return pattern.sub(openTag + r"\1" + closeTag, blithedale_xml)

# Tag by splitting string
def split(pattern, blithedale_xml, openTag, closeTag, rest):
    lst = pattern.split(blithedale_xml)
    temp = lst[0]
    for e in lst[1:]:
        if pattern.match(e):
            temp += e
        else:
            temp += openTag + e + closeTag
    return temp

# Tags whole sentence if pattern is found
def sent(pattern, blithedale_xml, openTag, closeTag, sentences):
    # this is necessary because the nltk sentence tokenize will include
    # chapter titles in sentences, so we need to exclude those
    exception = "\n\n"

    for s in sentences:
        if pattern.search(s) and exception not in s:
            blithedale_xml = blithedale_xml.replace(s, openTag + s + closeTag)
    return blithedale_xml

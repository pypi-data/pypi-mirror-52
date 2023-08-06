"""
Python module responsible for searching the Moby thesarus
"""

import re
import os


def synonyms(word):
    """Returns Moby thesaurus synonyms for a given word.
    Returns an empty list if word is not found"""
    with open("{}/words.txt".format(os.path.dirname(os.path.abspath(__file__)))) as f:
        wordRegex = re.compile(r"\n{},[\w+|,|  | -]+".format(word))
        words = re.findall(wordRegex, f.read())
        return words[0].replace("{},".format(word), "").replace("\n", "").split(",") if len(words) > 0 else []


def short_synonyms(word):
    """Return Moby thesaurus synonyms shorter than 5
    or equal to characters for a given word"""
    return [word for word in synonyms(word) if len(word) <= 5]

def long_synonyms(word):
    """Return Moby thesaurus synonyms longer than 5
    characters for a given word"""
    return [word for word in synonyms(word) if len(word) > 5]

def reverse_search(word):
    """
    Returns a list of words for which the given
    word is a synonym
    """
    matches = []
    with open("{}/words.txt".format(os.path.dirname(os.path.abspath(__file__)))) as f:
        wordRegex = re.compile(r",{}".format(word))
        firstWordRegex = re.compile(r"\n{},[\w+|,|  | -]+".format(word))
        for line in f.readlines():
            if len(re.findall(wordRegex, line)) > 1:
                matches.append(line.split(',')[0])
        return matches

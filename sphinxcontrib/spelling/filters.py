# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Spelling checker extension for Sphinx.
"""

import imp

from enchant.tokenize import Filter, tokenize, unit_tokenize

from six import moves
builtins = moves.builtins
xmlrpc_client = moves.xmlrpc_client

# TODO - Words with multiple uppercase letters treated as classes and ignored


class AcronymFilter(Filter):
    """If a word looks like an acronym (all upper case letters),
    ignore it.
    """
    def _skip(self, word):
        return (
            word.isupper() or  # all caps
            # pluralized acronym ("URLs")
            (word[-1].lower() == 's' and word[:-1].isupper())
        )


class list_tokenize(tokenize):

    def __init__(self, words):
        tokenize.__init__(self, '')
        self._words = words

    def next(self):
        if not self._words:
            raise StopIteration()
        word = self._words.pop(0)
        return (word, 0)


class ContractionFilter(Filter):
    """Strip common contractions from words.
    """
    splits = {
        "i'm": ["I", "am"],
        "i'll": ["I", "will"],
        "i'd": ["I", "would"],
        "i've": ["I", "have"],
        "you're": ["you", "are"],
        "you'll": ["you", "will"],
        "you'd": ["you", "would"],
        "you've": ["you", "have"],
        "he's": ["he", "is"],
        "he'll": ["he", "will"],
        "he'd": ["he", "would"],
        "she's": ["she", "is"],
        "she'll": ["she", "will"],
        "she'd": ["she", "would"],
        "it's": ["it", "is"],
        "it'll": ["it", "will"],
        "it'd": ["it", "would"],
        "we're": ["we", "are"],
        "we'll": ["we", "will"],
        "we'd": ["we", "would"],
        "we've": ["we", "have"],
        "they're": ["they", "are"],
        "they'll": ["they", "will"],
        "they'd": ["they", "would"],
        "they've": ["they", "have"],
        "that's": ["that", "is"],
        "that'll": ["that", "will"],
        "that'd": ["that", "would"],
        "who's": ["who", "is"],
        "who'll": ["who", "will"],
        "who'd": ["who", "would"],
        "what's": ["what", "is"],
        "what're": ["what", "are"],
        "what'll": ["what", "will"],
        "what'd": ["what", "would"],
        "where's": ["where", "is"],
        "where'll": ["where", "will"],
        "where'd": ["where", "would"],
        "when's": ["when", "is"],
        "when'll": ["when", "will"],
        "when'd": ["when", "would"],
        "why's": ["why", "is"],
        "why'll": ["why", "will"],
        "why'd": ["why", "would"],
        "how's": ["how", "is"],
        "how'll": ["how", "will"],
        "how'd": ["how", "would"],
        "isn't": ["is", "not"],
        "aren't": ["are", "not"],
        "wasn't": ["was", "not"],
        "weren't": ["were", "not"],
        "haven't": ["have", "not"],
        "hasn't": ["has", "not"],
        "hadn't": ["had", "not"],
        "won't": ["will", "not"],
        "wouldn't": ["would", "not"],
        "don't": ["do", "not"],
        "doesn't": ["does", "not"],
        "didn't": ["did", "not"],
        "can't": ["can", "not"],
        "couldn't": ["could", "not"],
        "shouldn't": ["should", "not"],
        "mightn't": ["might", "not"],
        "mustn't": ["must", "not"],
        "would've": ["would", "have"],
        "should've": ["should", "have"],
        "could've": ["could", "have"],
        "might've": ["might", "have"],
        "must've": ["must", "have"],
        "o'": ["of"],
        "o'clock": ["of", "the", "clock"],
        "ma'am": ["madam"],
    }

    def _split(self, word):
        # Fixed responses
        if word.lower() in self.splits:
            return list_tokenize(self.splits[word.lower()])

        # Possessive
        if word.lower().endswith("'s"):
            return unit_tokenize(word[:-2])

        # * not
        if word.lower().endswith("n't"):
            return unit_tokenize(word[:-3])

        return unit_tokenize(word)


class IgnoreWordsFilter(Filter):
    """Given a set of words, ignore them all.
    """

    def __init__(self, tokenizer, word_set):
        self.word_set = set(word_set)
        Filter.__init__(self, tokenizer)

    def _skip(self, word):
        return word in self.word_set


class IgnoreWordsFilterFactory(object):

    def __init__(self, words):
        self.words = words

    def __call__(self, tokenizer):
        return IgnoreWordsFilter(tokenizer, self.words)


class PyPIFilterFactory(IgnoreWordsFilterFactory):
    """Build an IgnoreWordsFilter for all of the names of packages on PyPI.
    """
    def __init__(self):
        client = xmlrpc_client.ServerProxy('https://pypi.python.org/pypi')
        IgnoreWordsFilterFactory.__init__(self, client.list_packages())


class PythonBuiltinsFilter(Filter):
    """Ignore names of built-in Python symbols.
    """
    def _skip(self, word):
        try:
            return hasattr(builtins, word)
        except UnicodeEncodeError:
            return False


class ImportableModuleFilter(Filter):
    """Ignore names of modules that we could import.
    """
    def __init__(self, tokenizer):
        Filter.__init__(self, tokenizer)
        self.found_modules = set()
        self.sought_modules = set()

    def _skip(self, word):
        if word not in self.sought_modules:
            self.sought_modules.add(word)
            try:
                imp.find_module(word)
            except UnicodeEncodeError:
                return False
            except ImportError:
                return False
            else:
                self.found_modules.add(word)
                return True
        return word in self.found_modules

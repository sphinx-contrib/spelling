#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Spelling checker extension for Sphinx.
"""

import imp

from enchant.tokenize import Filter, tokenize, unit_tokenize

from six.moves import builtins
from six.moves import xmlrpc_client

# TODO - Words with multiple uppercase letters treated as classes and ignored


class AcronymFilter(Filter):
    """If a word looks like an acronym (all upper case letters),
    ignore it.
    """
    def _skip(self, word):
        return (word == word.upper()  # all caps
                or
                # pluralized acronym ("URLs")
                (word[-1].lower() == 's'
                 and
                 word[:-1] == word[:-1].upper()
                 )
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
        "won't": ['will', 'not'],
        "isn't": ['is', 'not'],
        "can't": ['can', 'not'],
        "i'm": ['I', 'am'],
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
        client = xmlrpc_client.ServerProxy('http://pypi.python.org/pypi')
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

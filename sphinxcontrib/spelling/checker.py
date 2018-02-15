# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Spelling checker extension for Sphinx.
"""

import enchant
from enchant.tokenize import get_tokenizer


class SpellingChecker(object):
    """Checks the spelling of blocks of text.

    Uses options defined in the sphinx configuration file to control
    the checking and filtering behavior.
    """

    def __init__(self, lang, suggest, word_list_filename,
                 tokenizer_lang='en_US', filters=None):
        if filters is None:
            filters = []
        self.dictionary = enchant.DictWithPWL(lang, word_list_filename)
        self.tokenizer = get_tokenizer(tokenizer_lang, filters)
        self.original_tokenizer = self.tokenizer
        self.suggest = suggest

    def push_filters(self, new_filters):
        """Add a filter to the tokenizer chain.
        """
        t = self.tokenizer
        for f in new_filters:
            t = f(t)
        self.tokenizer = t

    def pop_filters(self):
        """Remove the filters pushed during the last call to push_filters().
        """
        self.tokenizer = self.original_tokenizer

    def check(self, text):
        """Yields bad words and suggested alternate spellings.
        """
        for word, pos in self.tokenizer(text):
            correct = self.dictionary.check(word)
            if correct:
                continue
            yield word, self.dictionary.suggest(word) if self.suggest else []
        return

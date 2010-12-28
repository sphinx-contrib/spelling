#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for SpellingChecker.
"""

import os

from sphinxcontrib.spelling import SpellingChecker

def test_errors_only():
    checker = SpellingChecker(lang='en_US',
                              suggest=False,
                              word_list_filename=None,
                              )
    for word, suggestions in checker.check('This txt is wrong'):
        assert not suggestions, 'Suggesting'
        assert word == 'txt'
    return

def test_with_suggestions():
    checker = SpellingChecker(lang='en_US',
                              suggest=True,
                              word_list_filename=None,
                              )
    for word, suggestions in checker.check('This txt is wrong'):
        assert suggestions, 'Not suggesting'
        assert word == 'txt'
    return

def test_with_wordlist():
    checker = SpellingChecker(lang='en_US',
                              suggest=False,
                              word_list_filename=os.path.join(os.path.dirname(__file__),
                                                              'test_wordlist.txt')
                              )
    words = [ w for w, s in checker.check('This txt is wrong') ]
    assert not words, 'Did not use personal word list file'
    return

#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for SpellingChecker.
"""

import os

from sphinxcontrib.spelling.checker import SpellingChecker, line_of_index


def test_errors_only():
    checker = SpellingChecker(lang='en_US',
                              suggest=False,
                              word_list_filename=None,
                              )
    for word, suggestions, line, offset in checker.check('This txt is wrong'):
        assert not suggestions, 'Suggesting'
        assert word == 'txt'
        assert line == ""
        assert offset == 0


def test_with_suggestions():
    checker = SpellingChecker(lang='en_US',
                              suggest=True,
                              word_list_filename=None,
                              )
    for word, suggestions, line, offset in checker.check('This txt is wrong'):
        assert suggestions, 'Not suggesting'
        assert word == 'txt'
        assert line == ""
        assert offset == 0

def test_with_wordlist():
    checker = SpellingChecker(
        lang='en_US',
        suggest=False,
        word_list_filename=os.path.join(os.path.dirname(__file__),
                                        'test_wordlist.txt')
    )
    words = [w for w, s, l, o in checker.check('This txt is wrong')]
    assert not words, 'Did not use personal word list file'


def test_with_context_line():
    checker = SpellingChecker(lang='en_US',
                              suggest=False,
                              word_list_filename=None,
                              context_line=True,
                              )

    text = 'Line one\nThis txt is wrong\nLine two'
    for word, suggestions, line, offset in checker.check(text):
        assert not suggestions, 'Suggesting'
        assert word == 'txt'
        assert line == "This txt is wrong"
        assert offset == 1


def test_line_of_index_one_line():
    text = "foo bar baz"
    assert line_of_index(text, 0) == text
    assert line_of_index(text, 5) == text
    assert line_of_index(text, len(text)) == text


def test_line_of_index_multi_line():
    text = "\nfoo\n\nbar baz\n"

    assert line_of_index(text, 0) == ""

    assert line_of_index(text, 1) == "foo"
    assert line_of_index(text, 2) == "foo"
    assert line_of_index(text, 3) == "foo"
    assert line_of_index(text, 4) == "foo"

    assert line_of_index(text, 5) == ""

    assert line_of_index(text, 6) == "bar baz"
    assert line_of_index(text, 12) == "bar baz"
    assert line_of_index(text, 13) == "bar baz"

    assert line_of_index(text, 14) == ""

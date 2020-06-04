# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for SpellingChecker.
"""

import os
import unittest

from sphinxcontrib.spelling.checker import SpellingChecker, line_of_index


class TestChecker(unittest.TestCase):

    def test_errors_only(self):
        checker = SpellingChecker(lang='en_US',
                                  suggest=False,
                                  word_list_filename=None,
                                  )
        for word, suggestions, line in checker.check('This txt is wrong'):
            assert not suggestions, 'Suggesting'
            assert word == 'txt'
            assert line == ""
        return

    def test_with_suggestions(self):
        checker = SpellingChecker(lang='en_US',
                                  suggest=True,
                                  word_list_filename=None,
                                  )
        for word, suggestions, line in checker.check('This txt is wrong'):
            assert suggestions, 'Not suggesting'
            assert word == 'txt'
            assert line == ""
        return

    def test_with_wordlist(self):
        checker = SpellingChecker(
            lang='en_US',
            suggest=False,
            word_list_filename=os.path.join(os.path.dirname(__file__),
                                            'test_wordlist.txt')
        )
        words = [w for w, s, l in checker.check('This txt is wrong')]
        assert not words, 'Did not use personal word list file'
        return

    def test_with_context_line(self):
        checker = SpellingChecker(lang='en_US',
                                  suggest=False,
                                  word_list_filename=None,
                                  context_line=True,
                                  )

        text = 'Line one\nThis txt is wrong\nLine two'
        for word, suggestions, line in checker.check(text):
            assert not suggestions, 'Suggesting'
            assert word == 'txt'
            assert line == "This txt is wrong"
        return

    # NOTE(dhellmann): Fails after updating to testrepository.
    #
    # def test_non_english(self):
    #     checker = SpellingChecker(lang='de_DE',
    #                               suggest=False,
    #                               word_list_filename=None,
    #                               )
    #     for word, suggestions in checker.check('Dieser Txt ist falsch'):
    #         assert word == 'Txt'
    #     return


class TestLineOfIndex(unittest.TestCase):

    def test_one_line(self):
        text = "foo bar baz"
        assert line_of_index(text, 0) == text
        assert line_of_index(text, 5) == text
        assert line_of_index(text, len(text)) == text

    def test_multi_line(self):
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

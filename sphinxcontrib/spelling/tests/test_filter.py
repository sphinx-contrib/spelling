# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for filters.
"""

import unittest

from enchant.tokenize import get_tokenizer

from sphinxcontrib.spelling import filters


def test_builtin_unicode():
    f = filters.PythonBuiltinsFilter(None)
    assert not f._skip(u'passé')


def test_builtin_regular():
    f = filters.PythonBuiltinsFilter(None)
    assert f._skip('print')


def test_acronym():
    text = 'a front-end for DBM-style databases'
    t = get_tokenizer('en_US', [])
    f = filters.AcronymFilter(t)
    words = [w[0] for w in f(text)]
    assert 'DBM' not in words, 'Failed to filter out acronym'


def test_acronym_unicode():
    text = u'a front-end for DBM-style databases'
    t = get_tokenizer('en_US', [])
    f = filters.AcronymFilter(t)
    words = [w[0] for w in f(text)]
    assert u'DBM' not in words, 'Failed to filter out acronym'

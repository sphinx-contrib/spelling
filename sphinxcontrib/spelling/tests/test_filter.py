#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for filters.
"""

from sphinxcontrib.spelling import filters


def test_unicode_builtin():
    f = filters.PythonBuiltinsFilter(None)
    assert not f._skip(u'passé')


def test_regular_builtin():
    f = filters.PythonBuiltinsFilter(None)
    assert f._skip('print')

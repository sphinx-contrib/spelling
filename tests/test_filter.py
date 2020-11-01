#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for filters.
"""

import pytest
from enchant.tokenize import get_tokenizer

from sphinxcontrib.spelling import filters


def test_builtin_unicode():
    f = filters.PythonBuiltinsFilter(None)
    assert not f._skip('passé')


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
    text = 'a front-end for DBM-style databases'
    t = get_tokenizer('en_US', [])
    f = filters.AcronymFilter(t)
    words = [w[0] for w in f(text)]
    assert 'DBM' not in words, 'Failed to filter out acronym'


@pytest.mark.parametrize(
    "name",
    [
        "Alex",
        "Atlakson",
        "Avram",
        "Baumgold",
        "Berman",
        "Daniele",
        "Doug",
        "Finucane",
        "Gaynor",
        "Gonsiorowski",
        "Hong",
        "Hong",
        "Huon",
        "Kampik",
        "Kolosov",
        "Lubkin",
        "Marti",
        "Minhee",
        "Olausson",
        "Raggam",
        "Raudsepp",
        "sdelliot",
        "Sergey",
        "Sevilla",
        "Timotheus",
        "Tobias",
        "Tricoli",
    ]
)
def test_contributors(name):
    f = filters.ContributorFilter(None)
    assert f._skip(name)


@pytest.mark.parametrize(
    "word,expected",
    [
        ('os', True),
        ('os.name', False),
        ('__main__', False),
    ]
)
def test_importable_module_skip(word, expected):
    f = filters.ImportableModuleFilter(None)
    assert f._skip(word) is expected


def test_importable_module_with_side_effets(tmpdir):
    with tmpdir.as_cwd():
        path = tmpdir.join('setup.py')
        path.write('raise SystemExit\n')
        f = filters.ImportableModuleFilter(None)
        assert f._skip('setup.cfg') is False

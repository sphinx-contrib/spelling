#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for filters.
"""

import contextlib
import logging
import os
import sys

import pytest
from enchant.tokenize import get_tokenizer

from sphinxcontrib.spelling import filters # isort:skip
from tests import helpers # isort:skip

# Replace the sphinx logger with a normal one so pytest can collect
# the output.
filters.logger = logging.getLogger('test.filters')


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


@helpers.require_git_repo
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
        ("don't", False),
    ]
)
def test_importable_module_skip(word, expected):
    f = filters.ImportableModuleFilter(None)
    assert f._skip(word) is expected


@contextlib.contextmanager
def import_path(new_path):
    "Temporarily change sys.path for imports."
    before = sys.path
    try:
        sys.path = new_path
        yield
    finally:
        sys.path = before


def test_importable_module_with_side_effets(tmpdir):
    logging.debug('tmpdir %r', tmpdir)
    logging.debug('cwd %r', os.getcwd())

    parentdir = tmpdir.join('parent')
    parentdir.mkdir()

    parentdir.join('__init__.py').write(
        'raise SystemExit("exit as side-effect")\n'
    )
    parentdir.join('child.py').write('')

    with import_path([str(tmpdir)] + sys.path):
        f = filters.ImportableModuleFilter(None)
        skip_parent = f._skip('parent')
        skip_both = f._skip('parent.child')

    # The parent module name is valid because it is not imported, only
    # discovered.
    assert skip_parent is True
    assert 'parent' in f.found_modules

    # The child module name is not valid because the parent is
    # imported to find the child and that triggers the side-effect.
    assert skip_both is False
    assert 'parent.child' not in f.found_modules


def test_importable_module_with_system_exit(tmpdir):
    path = tmpdir.join('mytestmodule.py')
    path.write('raise SystemExit("exit as side-effect")\n')

    with import_path([str(tmpdir)] + sys.path):
        f = filters.ImportableModuleFilter(None)
        skip = f._skip('mytestmodule')

    # The filter does not actually import the module in this case, so
    # it shows up as a valid word.
    assert skip is True
    assert 'mytestmodule' in f.found_modules

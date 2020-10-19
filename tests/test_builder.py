#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for SpellingBuilder
"""
import codecs
import io
import os
import textwrap

import pytest
from sphinx.application import Sphinx


@pytest.fixture
def sphinx_project(tmpdir):
    srcdir = tmpdir.mkdir('src')
    outdir = tmpdir.mkdir('out')
    add_file(srcdir, 'conf.py', '''
    extensions = [ 'sphinxcontrib.spelling' ]
    ''')
    yield (srcdir, outdir)


def add_file(thedir, filename, content):
    with open(thedir.join(filename), 'w') as f:
        f.write(textwrap.dedent(content))


def get_sphinx_output(srcdir, outdir, docname):
    stdout = io.StringIO()
    stderr = io.StringIO()
    app = Sphinx(
        srcdir, srcdir, outdir, outdir, 'spelling',
        status=stdout, warning=stderr,
        freshenv=True,
    )
    app.build()
    path = os.path.join(outdir, docname + '.spelling')
    try:
        with open(path, 'r') as f:
            output_text = f.read()
    except FileNotFoundError:
        output_text = None
    return (stdout, stderr, output_text)


def test_setup(sphinx_project):
    srcdir, outdir = sphinx_project
    stdout = io.StringIO()
    stderr = io.StringIO()
    # If the spelling builder is not properly initialized,
    # trying to use it with the Sphinx app class will
    # generate an exception.
    Sphinx(
        str(srcdir), str(srcdir), str(outdir), str(outdir), 'spelling',
        status=stdout, warning=stderr,
        freshenv=True,
    )


def test_title(sphinx_project):
    srcdir, outdir = sphinx_project
    add_file(srcdir, 'contents.rst', '''
    Welcome to Speeling Checker documentation!
    ==========================================
    ''')
    stdout, stderr, output_text = get_sphinx_output(srcdir, outdir, 'contents')
    assert '(Speeling)' in output_text


def test_body(sphinx_project):
    srcdir, outdir = sphinx_project
    add_file(srcdir, 'contents.rst', '''
    Welcome to Spelling Checker documentation!
    ==========================================

    There are several mispelled words in this txt.
    ''')
    stdout, stderr, output_text = get_sphinx_output(srcdir, outdir, 'contents')
    assert '(mispelled)' in output_text
    assert '(txt)' in output_text


def test_ignore_literals(sphinx_project):
    srcdir, outdir = sphinx_project
    add_file(srcdir, 'contents.rst', '''
    Welcome to Spelling Checker documentation!
    ==========================================

    There are several misspelled words in this text.

    ::

        Literal blocks are ignoreed.

    Inline ``litterals`` are ignored, too.

    ''')
    stdout, stderr, output_text = get_sphinx_output(srcdir, outdir, 'contents')
    # The 'contents.spelling' output file should not have been
    # created, because the errors are ignored.
    assert output_text is None


def test_several_word_lists(sphinx_project):
    srcdir, outdir = sphinx_project
    add_file(srcdir, 'conf.py', '''
    extensions = ['sphinxcontrib.spelling']
    spelling_word_list_filename=['test_wordlist.txt','test_wordlist2.txt']
    ''')

    add_file(srcdir, 'contents.rst', '''
    Welcome to Spelling Checker documentation!
    ==========================================

    There are several mispelled words in tihs txt.
    ''')

    add_file(srcdir, 'test_wordlist.txt', '''
    txt
    ''')

    add_file(srcdir, 'test_wordlist2.txt', '''
    mispelled
    ''')
    stdout, stderr, output_text = get_sphinx_output(srcdir, outdir, 'contents')
    # Both of these should be fine now
    assert '(mispelled)' not in output_text
    assert '(txt)' not in output_text
    # But not this one
    assert '(tihs)' in output_text


def test_ignore_file(sphinx_project):
    srcdir, outdir = sphinx_project
    add_file(srcdir, 'conf.py', '''
    extensions = ['sphinxcontrib.spelling']
    spelling_exclude_patterns=['con*']
    ''')

    add_file(srcdir, 'contents.rst', '''
    Welcome to Speeling Checker documentation!
    ==========================================
    ''')

    stdout, stderr, output_text = get_sphinx_output(srcdir, outdir, 'contents')
    # The 'contents.spelling' output file should not have been
    # created, because the file is ignored.
    assert output_text is None

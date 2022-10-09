#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for SpellingBuilder
"""
import contextlib
import io
import os
import sys
import textwrap

import pytest
import sphinx
from sphinx.application import Sphinx

from tests import helpers # isort:skip


def _make_sphinx_project(tmpdir):
    srcdir = tmpdir.mkdir('src')
    outdir = tmpdir.mkdir('out')
    add_file(srcdir, 'conf.py', '''
    extensions = [ 'sphinxcontrib.spelling' ]
    ''')
    return (srcdir, outdir)


@pytest.fixture
def sphinx_project(tmpdir):
    yield _make_sphinx_project(tmpdir)


@contextlib.contextmanager
def working_dir(targetdir):
    "Temporarily change the working directory of the process."
    before = os.getcwd()
    os.chdir(targetdir)
    try:
        yield os.getcwd()
    finally:
        os.chdir(before)


@contextlib.contextmanager
def import_path(new_path):
    "Temporarily change sys.path for imports."
    before = sys.path
    try:
        sys.path = new_path
        yield
    finally:
        sys.path = before


def add_file(thedir, filename, content):
    with open(thedir.join(filename), 'w') as f:
        f.write(textwrap.dedent(content))


def get_sphinx_app(srcdir, outdir, docname, builder='spelling'):
    stdout = io.StringIO()
    stderr = io.StringIO()
    app = Sphinx(
        srcdir, srcdir, outdir, outdir, builder,
        status=stdout, warning=stderr,
        freshenv=True,
    )
    return (stdout, stderr, app)


def get_sphinx_output(srcdir, outdir, docname, builder='spelling'):
    stdout, stderr, app = get_sphinx_app(srcdir, outdir, docname, builder)
    app.build()
    path = os.path.join(outdir, f'{docname}.spelling')
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


def _wordlist_sphinx_project(tmpdir, conf_contents):
    srcdir, outdir = _make_sphinx_project(tmpdir)
    add_file(srcdir, 'conf.py', conf_contents)
    add_file(srcdir, 'test_wordlist.txt', '''
    txt
    ''')
    add_file(srcdir, 'test_wordlist2.txt', '''
    mispelled
    ''')
    stdout, stderr, app = get_sphinx_app(srcdir, outdir, 'contents')
    return (srcdir, outdir, stdout, stderr, app)


def test_word_list_default(tmpdir):
    srcdir, outdir, stdout, stderr, app = _wordlist_sphinx_project(
        tmpdir,
        '''
        extensions = ['sphinxcontrib.spelling']
        ''',
    )
    results = app.builder.get_configured_wordlist_filenames()
    assert len(results) == 1
    assert os.path.basename(results[0]) == 'spelling_wordlist.txt'


def test_one_word_list_str(tmpdir):
    srcdir, outdir, stdout, stderr, app = _wordlist_sphinx_project(
        tmpdir,
        '''
        extensions = ['sphinxcontrib.spelling']
        spelling_word_list_filename='test_wordlist.txt'
        ''',
    )
    results = app.builder.get_configured_wordlist_filenames()
    assert len(results) == 1
    assert os.path.basename(results[0]) == 'test_wordlist.txt'


def test_multiple_word_list_str(tmpdir):
    # We don't expect anyone to set up their conf.py this way but it
    # simulates passing the configuration option from the command line
    # using -D.
    srcdir, outdir, stdout, stderr, app = _wordlist_sphinx_project(
        tmpdir,
        '''
        extensions = ['sphinxcontrib.spelling']
        spelling_word_list_filename='test_wordlist.txt,test_wordlist2.txt'
        ''',
    )
    results = app.builder.get_configured_wordlist_filenames()
    assert len(results) == 2
    assert os.path.basename(results[0]) == 'test_wordlist.txt'
    assert os.path.basename(results[1]) == 'test_wordlist2.txt'


def test_multiple_word_list_list(tmpdir):
    srcdir, outdir, stdout, stderr, app = _wordlist_sphinx_project(
        tmpdir,
        '''
        extensions = ['sphinxcontrib.spelling']
        spelling_word_list_filename=['test_wordlist.txt', 'test_wordlist2.txt']
        ''',
    )
    results = app.builder.get_configured_wordlist_filenames()
    assert len(results) == 2
    assert os.path.basename(results[0]) == 'test_wordlist.txt'
    assert os.path.basename(results[1]) == 'test_wordlist2.txt'


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


@helpers.require_git_repo
def test_docstrings(sphinx_project):
    srcdir, outdir = sphinx_project

    add_file(srcdir, 'conf.py', '''
    extensions = ['sphinxcontrib.spelling', 'sphinx.ext.autodoc']
    ''')

    add_file(srcdir / '..', 'the_source.py', '''
    #!/usr/bin/env python3

    def public_function(arg_name):
        """Does something useful.

        :param arg_name: Pass a vaule
        """
        return 1
    ''')

    add_file(srcdir, 'contents.rst', '''
    The Module
    ==========

    .. automodule:: the_source
       :members:

    ''')

    with working_dir(srcdir / '..'):
        with import_path(['.'] + sys.path):
            stdout, stderr, output_text = get_sphinx_output(
                srcdir,
                outdir,
                'contents',
            )

    # Sphinx 5.1.0 and later reports line numbers for docstring
    # content.
    line_num = 'None:'
    if sphinx.version_info[:3] >= (5, 1, 0):
        line_num = '1:'

    # Expected string is too long for one line
    expected = (
        'the_source.py:'
        'docstring of the_source.public_function:'
    ) + line_num + (
        ' (vaule)'
    )
    assert expected in output_text


def test_get_suggestions_to_show_all(sphinx_project):
    srcdir, outdir = sphinx_project
    add_file(srcdir, 'conf.py', '''
    extensions = ['sphinxcontrib.spelling']
    spelling_show_suggestions = True
    spelling_suggestion_limit = 0
    ''')
    stdout, stderr, app = get_sphinx_app(srcdir, outdir, 'contents')
    results = app.builder.get_suggestions_to_show(['a', 'b', 'c'])
    assert len(results) == 3


def test_get_suggestions_to_show_limit(sphinx_project):
    srcdir, outdir = sphinx_project
    add_file(srcdir, 'conf.py', '''
    extensions = ['sphinxcontrib.spelling']
    spelling_show_suggestions = True
    spelling_suggestion_limit = 1
    ''')
    stdout, stderr, app = get_sphinx_app(srcdir, outdir, 'contents')
    results = app.builder.get_suggestions_to_show(['a', 'b', 'c'])
    assert len(results) == 1


def test_get_suggestions_to_show_disabled(sphinx_project):
    srcdir, outdir = sphinx_project
    add_file(srcdir, 'conf.py', '''
    extensions = ['sphinxcontrib.spelling']
    spelling_show_suggestions = False
    spelling_suggestion_limit = 0
    ''')
    stdout, stderr, app = get_sphinx_app(srcdir, outdir, 'contents')
    results = app.builder.get_suggestions_to_show(['a', 'b', 'c'])
    assert len(results) == 0


def test_captions(sphinx_project):
    srcdir, outdir = sphinx_project

    add_file(srcdir, 'contents.rst', '''
    The Module
    ==========

    .. figure:: blah.gif

       Teh caption

    ''')

    stdout, stderr, output_text = get_sphinx_output(
        srcdir,
        outdir,
        'contents',
    )
    assert '(Teh)' in output_text


def test_legacy_directive(sphinx_project):
    srcdir, outdir = sphinx_project

    add_file(srcdir, 'contents.rst', '''
    The Module
    ==========

    .. spelling::

       teh

    teh is OK

    ''')

    stdout, stderr, output_text = get_sphinx_output(
        srcdir,
        outdir,
        'contents',
    )
    assert output_text is None


def test_domain_directive(sphinx_project):
    srcdir, outdir = sphinx_project

    add_file(srcdir, 'contents.rst', '''
    The Module
    ==========

    .. spelling:word-list::

       teh

    teh is OK

    ''')

    stdout, stderr, output_text = get_sphinx_output(
        srcdir,
        outdir,
        'contents',
    )
    assert output_text is None


def test_domain_role(sphinx_project):
    srcdir, outdir = sphinx_project

    add_file(srcdir, 'contents.rst', '''
    The Module
    ==========

    :spelling:word:`teh` is OK

    ''')

    stdout, stderr, output_text = get_sphinx_output(
        srcdir,
        outdir,
        'contents',
    )
    assert output_text is None


def test_domain_role_multiple_words(sphinx_project):
    srcdir, outdir = sphinx_project

    add_file(srcdir, 'contents.rst', '''
    The Module
    ==========

    :spelling:word:`teh is KO`

    ''')

    stdout, stderr, output_text = get_sphinx_output(
        srcdir,
        outdir,
        'contents',
    )
    assert output_text is None

def test_domain_role_output(sphinx_project):
    srcdir, outdir = sphinx_project

    add_file(srcdir, 'contents.rst', '''
    The Module
    ==========

    :spelling:word:`teh` is OK

    ''')

    stdout, stderr, output_text = get_sphinx_output(
        srcdir,
        outdir,
        'contents',
        'text',
    )

    path = os.path.join(outdir, 'contents.txt')
    try:
        with open(path, 'r') as f:
            output_text = f.read()
    except FileNotFoundError:
        output_text = None

    assert output_text == "The Module\n**********\n\nteh is OK\n"

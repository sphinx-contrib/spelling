#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for SpellingBuilder
"""

import codecs
import os
import shutil
import tempfile
from cStringIO import StringIO

from sphinxcontrib import spelling

from sphinx.application import Sphinx
from sphinx.config import Config

def setup():
    global _tempdir, _srcdir, _outdir
    _tempdir = tempfile.mkdtemp()
    _srcdir = os.path.join(_tempdir, 'src')
    _outdir = os.path.join(_tempdir, 'out')
    os.mkdir(_srcdir)
    os.mkdir(_outdir)

def teardown():
    shutil.rmtree(_tempdir)

def test_setup():
    with open(os.path.join(_srcdir, 'conf.py'), 'w') as f:
        f.write('''
extensions = [ 'sphinxcontrib.spelling' ]
''')
    stdout = StringIO()
    stderr = StringIO()
    # If the spelling builder is not properly initialized,
    # trying to use it with the Sphinx app class will
    # generate an exception.
    app = Sphinx(_srcdir, _srcdir, _outdir, _outdir, 'spelling',
                 status=stdout, warning=stderr,
                 freshenv=True,
                 )
    return

def test_title():
    with open(os.path.join(_srcdir, 'conf.py'), 'w') as f:
        f.write('''
extensions = [ 'sphinxcontrib.spelling' ]
''')
    with open(os.path.join(_srcdir, 'contents.rst'), 'w') as f:
        f.write('''
Welcome to Speeling Checker documentation!
==========================================
''')
    stdout = StringIO()
    stderr = StringIO()
    app = Sphinx(_srcdir, _srcdir, _outdir, _outdir, 'spelling',
                 status=stdout, warning=stderr,
                 freshenv=True,
                 )
    app.build()
    with codecs.open(app.builder.output_filename, 'r') as f:
        output_text = f.read()

    def check_one(word):
        print output_text
        assert word in output_text
    for word in [ '(Speeling)', ]:
        yield check_one, word
    return


def test_body():
    with open(os.path.join(_srcdir, 'conf.py'), 'w') as f:
        f.write('''
extensions = [ 'sphinxcontrib.spelling' ]
''')
    with open(os.path.join(_srcdir, 'contents.rst'), 'w') as f:
        f.write('''
Welcome to Spelling Checker documentation!
==========================================

There are several mispelled words in this txt.
''')
    stdout = StringIO()
    stderr = StringIO()
    app = Sphinx(_srcdir, _srcdir, _outdir, _outdir, 'spelling',
                 status=stdout, warning=stderr,
                 freshenv=True,
                 )
    app.build()
    print 'reading from %s' % app.builder.output_filename
    with codecs.open(app.builder.output_filename, 'r') as f:
        output_text = f.read()

    def check_one(word):
        assert word in output_text
    for word in [ '(mispelled)', '(txt)' ]:
        yield check_one, word
    return


def test_ignore_literals():
    with open(os.path.join(_srcdir, 'conf.py'), 'w') as f:
        f.write('''
extensions = [ 'sphinxcontrib.spelling' ]
''')
    with open(os.path.join(_srcdir, 'contents.rst'), 'w') as f:
        f.write('''
Welcome to Spelling Checker documentation!
==========================================

There are several misspelled words in this text.

::

  Literal blocks are ignoreed.

Inline ``litterals`` are ignored, too.

''')
    stdout = StringIO()
    stderr = StringIO()
    app = Sphinx(_srcdir, _srcdir, _outdir, _outdir, 'spelling',
                 status=stdout, warning=stderr,
                 freshenv=True,
                 )
    app.build()
    print 'reading from %s' % app.builder.output_filename
    with codecs.open(app.builder.output_filename, 'r') as f:
        output_text = f.read()

    def check_one(word):
        assert word not in output_text
    for word in [ '(ignoreed)', '(litterals)' ]:
        yield check_one, word
    return


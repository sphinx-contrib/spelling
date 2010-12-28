#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for SpellingBuilder
"""

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
    assert '"Speeling"' in app.builder.output[0]
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
    output_text = app.builder.output[0]
    assert '"mispelled"' in output_text
    assert '"txt"' in output_text
    return


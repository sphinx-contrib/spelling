# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Tests for SpellingBuilder
"""

from __future__ import print_function

import codecs
import os
import textwrap

import fixtures
from six import StringIO
import testtools

from sphinx.application import Sphinx


class BuilderTest(testtools.TestCase):

    def setUp(self):
        super(BuilderTest, self).setUp()
        self.tempdir = self.useFixture(fixtures.TempDir()).path
        self.srcdir = os.path.join(self.tempdir, 'src')
        self.outdir = os.path.join(self.tempdir, 'out')
        os.mkdir(self.srcdir)
        os.mkdir(self.outdir)

    def test_setup(self):
        with open(os.path.join(self.srcdir, 'conf.py'), 'w') as f:
            f.write(textwrap.dedent('''
            extensions = [ 'sphinxcontrib.spelling' ]
            '''))
        stdout = StringIO()
        stderr = StringIO()
        # If the spelling builder is not properly initialized,
        # trying to use it with the Sphinx app class will
        # generate an exception.
        Sphinx(
            self.srcdir, self.srcdir, self.outdir, self.outdir, 'spelling',
            status=stdout, warning=stderr,
            freshenv=True,
        )

    def test_title(self):
        with open(os.path.join(self.srcdir, 'conf.py'), 'w') as f:
            f.write(textwrap.dedent('''
            extensions = [ 'sphinxcontrib.spelling' ]
            '''))
        with open(os.path.join(self.srcdir, 'contents.rst'), 'w') as f:
            f.write(textwrap.dedent('''
            Welcome to Speeling Checker documentation!
            ==========================================
            '''))
        stdout = StringIO()
        stderr = StringIO()
        app = Sphinx(
            self.srcdir, self.srcdir, self.outdir, self.outdir, 'spelling',
            status=stdout, warning=stderr,
            freshenv=True,
        )
        app.build()
        with codecs.open(app.builder.output_filename, 'r') as f:
            output_text = f.read()

        self.assertIn('(Speeling)', output_text)

    def test_body(self):
        with open(os.path.join(self.srcdir, 'conf.py'), 'w') as f:
            f.write(textwrap.dedent('''
            extensions = ['sphinxcontrib.spelling']
            '''))
        with open(os.path.join(self.srcdir, 'contents.rst'), 'w') as f:
            f.write(textwrap.dedent('''
            Welcome to Spelling Checker documentation!
            ==========================================

            There are several mispelled words in this txt.
            '''))
        stdout = StringIO()
        stderr = StringIO()
        app = Sphinx(
            self.srcdir, self.srcdir, self.outdir, self.outdir, 'spelling',
            status=stdout, warning=stderr,
            freshenv=True,
        )
        app.build()
        print('reading from %s' % app.builder.output_filename)
        with codecs.open(app.builder.output_filename, 'r') as f:
            output_text = f.read()

        self.assertIn('(mispelled)', output_text)
        self.assertIn('(txt)', output_text)

    def test_ignore_literals(self):
        with open(os.path.join(self.srcdir, 'conf.py'), 'w') as f:
            f.write(textwrap.dedent('''
            extensions = ['sphinxcontrib.spelling']
            '''))
        with open(os.path.join(self.srcdir, 'contents.rst'), 'w') as f:
            f.write(textwrap.dedent('''
            Welcome to Spelling Checker documentation!
            ==========================================

            There are several misspelled words in this text.

            ::

                Literal blocks are ignoreed.

            Inline ``litterals`` are ignored, too.

            '''))
        stdout = StringIO()
        stderr = StringIO()
        app = Sphinx(
            self.srcdir, self.srcdir, self.outdir, self.outdir, 'spelling',
            status=stdout, warning=stderr,
            freshenv=True,
        )
        app.build()
        print('reading from %s' % app.builder.output_filename)
        with codecs.open(app.builder.output_filename, 'r') as f:
            output_text = f.read()

        self.assertNotIn('(ignoreed)', output_text)
        self.assertNotIn('(litterals)', output_text)

    def test_several_word_lists(self):
        with open(os.path.join(self.srcdir, 'conf.py'), 'w') as f:
            f.write(textwrap.dedent('''
            extensions = ['sphinxcontrib.spelling']
            spelling_word_list_filename=['test_wordlist.txt','test_wordlist2.txt']

            '''))

        with open(os.path.join(self.srcdir, 'contents.rst'), 'w') as f:
            f.write(textwrap.dedent('''
            Welcome to Spelling Checker documentation!
            ==========================================

            There are several mispelled words in tihs txt.
            '''))

        with open(os.path.join(self.srcdir, 'test_wordlist.txt'), 'w') as f:
            f.write(textwrap.dedent('''
            txt
            '''))

        with open(os.path.join(self.srcdir, 'test_wordlist2.txt'), 'w') as f:
            f.write(textwrap.dedent('''
            mispelled
            '''))

        stdout = StringIO()
        stderr = StringIO()
        app = Sphinx(
            self.srcdir, self.srcdir, self.outdir, self.outdir, 'spelling',
            status=stdout, warning=stderr,
            freshenv=True,
        )
        app.build()
        print('reading from %s' % app.builder.output_filename)
        with codecs.open(app.builder.output_filename, 'r') as f:
            output_text = f.read()

        # Both of these should be fine now
        self.assertNotIn('(mispelled)', output_text)
        self.assertNotIn('(txt)', output_text)
        # But not this one
        self.assertIn('(tihs)', output_text)

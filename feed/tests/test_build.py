# -*- coding: utf-8 -*-
"""
    test_build
    ~~~~~~~~~~

    Test the entire build process with the test root.

    :copyright: Copyright 2007-2009 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import os
from os.path import exists
import re
import sys
import difflib
import htmlentitydefs
from StringIO import StringIO
import assert_operators as ops
from util import test_root, raises, raises_msg, Struct,\
  ListOutput, TestApp, with_app, gen_with_app, path, with_tempdir,\
  write_file, sprint

import feedparser

import nose.tools

def teardown_module():
    (test_root / '_build').rmtree(True)

feed_warnfile = StringIO()

ENV_WARNINGS = ""
# """\
# %(root)s/includes.txt:4: WARNING: download file not readable: nonexisting.png
# """

FEED_WARNINGS = ENV_WARNINGS + ""
# """\
# %(root)s/images.txt:20: WARNING: no matching candidate for image URI u'foo.*'
# """

def exists(p):
    assert os.path.exists(p)
    
@gen_with_app(buildername='html', warning=feed_warnfile, cleanenv=True)
def test_feed(app):
    app.build(all_files=True, filenames=[]) #build_all misses the crucial finish signal
    feed_warnings = feed_warnfile.getvalue().replace(os.sep, '/')
    feed_warnings_exp = FEED_WARNINGS % {'root': app.srcdir}
    yield ops.eq, feed_warnings, feed_warnings_exp
    rss_path = os.path.join(app.outdir, 'rss.xml')
    yield exists, rss_path
    yield ops.eq, app.builder.env.feed_items.keys(), ['older', 'most_aged', 'latest']
    # see http://www.feedparser.org/
    f = feedparser.parse(rss_path)
    entries = f.entries
    yield ops.eq, entries[0].updated_parsed, (2001, 8, 11)
    yield ops.eq, entries[0].title, "The latest blog post"
    yield ops.eq, entries[1].updated_parsed, (2001, 8, 1)
    yield ops.eq, entries[1].title, "An older blog post"
    yield ops.eq, entries[2].updated_parsed, (1979, 1, 1)
    yield ops.eq, entries[2].title, "The oldest blog post"


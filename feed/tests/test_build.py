# -*- coding: utf-8 -*-

import os
from os.path import exists
import re
import sys
import difflib
import htmlentitydefs
from StringIO import StringIO
from util import test_root, raises, raises_msg, Struct,\
  ListOutput, TestApp, with_app, gen_with_app, path, with_tempdir,\
  write_file, sprint

import feedparser

from nose.tools import assert_equals

def setup_module():
    if not (test_root / '_static').exists():
        (test_root / '_static').mkdir() #this empty dir is not included in version control

def teardown_module():
    (test_root / '_build').rmtree(True)

feed_warnfile = StringIO()

ENV_WARNINGS = "" #none at the moment. if needed, they will look like:
# """\
# %(root)s/includes.txt:4: WARNING: download file not readable: nonexisting.png
# """

FEED_WARNINGS = ENV_WARNINGS + "" # nothing here either yet

@gen_with_app(buildername='html', warning=feed_warnfile, cleanenv=True)
def test_feed(app):
    app.build(all_files=True, filenames=[]) #build_all misses the crucial finish signal
    feed_warnings = feed_warnfile.getvalue().replace(os.sep, '/')
    feed_warnings_exp = FEED_WARNINGS % {'root': app.srcdir}
    yield assert_equals, feed_warnings, feed_warnings_exp
    rss_path = os.path.join(app.outdir, 'rss.xml')
    yield exists, rss_path
    yield assert_equals, app.builder.env.feed_items.keys(), ['older', 'most_aged', 'latest']
    # see http://www.feedparser.org/
    f = feedparser.parse(rss_path)
    yield assert_equals, f.bozo, 0 #feedparser well-formedness detection
    entries = f.entries
    yield assert_equals, entries[0].updated_parsed[0:3], (2001, 8, 11)
    yield assert_equals, entries[0].title, "The latest blog post"
    yield assert_equals, entries[1].updated_parsed[0:3], (2001, 8, 1)
    yield assert_equals, entries[1].title, "An older blog post"
    yield assert_equals, entries[2].updated_parsed[0:3], (1979, 1, 1)
    yield assert_equals, entries[2].title, "The oldest blog post"


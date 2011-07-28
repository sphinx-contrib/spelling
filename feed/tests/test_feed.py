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
from path import path
from BeautifulSoup import BeautifulSoup
import feedparser
from datetime import datetime
from nose.tools import assert_equals, assert_true, assert_false

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

def test_feed():
    app = TestApp(buildername='html', warning=feed_warnfile, cleanenv=True)  
    app.build(force_all=True, filenames=[]) #build_all misses the crucial finish signal
    feed_warnings = feed_warnfile.getvalue().replace(os.sep, '/')
    feed_warnings_exp = FEED_WARNINGS % {'root': app.srcdir}
    yield assert_equals, feed_warnings, feed_warnings_exp
    rss_path = os.path.join(app.outdir, 'rss.xml')
    yield exists, rss_path
    
    base_path = unicode("file:/" + app.outdir)
    
    # see http://www.feedparser.org/
    f = feedparser.parse(rss_path)
    yield assert_equals, f.bozo, 0 #feedparser well-formedness detection. We want this.
    yield assert_equals, f.feed['title'], 'Sphinx Syndicate Test Title'
    entries = f.entries
    yield assert_equals, entries[0].updated_parsed[0:6], (2001, 8, 11, 13, 0, 0)
    yield assert_equals, entries[0].title, "The latest blog post"
    
    yield assert_equals, entries[0].link, base_path + '/B_latest.html'
    yield assert_equals, entries[0].guid, base_path + '/B_latest.html'
    yield assert_equals, entries[1].updated_parsed[0:6], (2001, 8, 11, 9, 0, 0)
    yield assert_equals, entries[1].title, "An older blog post"
    yield assert_equals, entries[1].link, base_path + '/A_older.html'
    yield assert_equals, entries[1].guid, base_path + '/A_older.html'
    yield assert_equals, entries[2].updated_parsed[0:6], (1979, 1, 1, 0, 0, 0,)
    yield assert_equals, entries[2].title, "The oldest blog post"
    yield assert_equals, entries[2].link, base_path + '/C_most_aged.html'
    yield assert_equals, entries[2].guid, base_path + '/C_most_aged.html'
    #Now we do it all again to make sure that things work when handling stale files
    app2 = TestApp(buildername='html', warning=feed_warnfile)  
    app2.build(force_all=False, filenames=['most_aged'])
    f = feedparser.parse(rss_path)
    yield assert_equals, f.bozo, 0 #feedparser well-formedness detection. We want this.
    entries = f.entries
    yield assert_equals, entries[0].updated_parsed[0:6], (2001, 8, 11, 13, 0, 0)
    yield assert_equals, entries[0].title, "The latest blog post"
    yield assert_equals, entries[1].updated_parsed[0:6], (2001, 8, 11, 9, 0, 0)
    yield assert_equals, entries[1].title, "An older blog post"
    yield assert_equals, entries[2].updated_parsed[0:6], (1979, 1, 1, 0, 0, 0)
    yield assert_equals, entries[2].title, "The oldest blog post"
    
    #Tests for relative URIs. note that these tests only work because there is
    # no xml:base - otherwise feedparser will supposedly fix them up for us - 
    # http://www.feedparser.org/docs/resolving-relative-links.html
    links = BeautifulSoup(entries[0].description).findAll('a')
    # These links will look like:
    #[<a class="headerlink" href="#the-latest-blog-post" title="Permalink to this headline">¶</a>, <a class="reference internal" href="older.html"><em>a relative link</em></a>, <a class="reference external" href="http://google.com/">an absolute link</a>]
    yield assert_equals, links.pop()['href'], "http://google.com/"
    yield assert_equals, links.pop()['href'], base_path + '/A_older.html'
    yield assert_equals, links.pop()['href'], entries[0].link + '#the-latest-blog-post'
    
    index_path  = os.path.join(app.outdir, 'index.html')
    soup = BeautifulSoup(open(index_path).read())
    #latest_tree = soup.find('div', 'toctree-wrapper')
    #latest_items = soup.findAll('li', 'toctree-l1')
    #These will look like this:
    # <div class="toctree-wrapper compound">
    # <ul>
    # <li class="toctree-l1"><a class="reference internal" href="B_latest.html">The latest blog post</a></li>
    # <li class="toctree-l1"><a class="reference internal" href="A_older.html">An older blog post</a></li>
    # <li class="toctree-l1"><a class="reference internal" href="C_most_aged.html">The oldest blog post</a></li>
    # </ul>
    # </div>
    #yield assert_equals, latest_tree, 'weirdness'
    # import pdb; pdb.set_trace()
    
    app.cleanup()
    app2.cleanup()

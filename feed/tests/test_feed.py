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
import unittest



class TestFeedStructure(unittest.TestCase):
    def setUp(self):
        self.ENV_WARNINGS = "" #none at the moment. if needed, they will look like:
        # """\
        # %(root)s/includes.txt:4: WARNING: download file not readable: nonexisting.png
        # """
        self.FEED_WARNINGS = self.ENV_WARNINGS + "" # nothing here either yet
        
        if not (test_root / '_static').exists():
            (test_root / '_static').mkdir() #this empty dir is not included in version control
        self.feed_warnfile = StringIO()
    
    def tearDown(self):
        (test_root / '_build').rmtree(True)

    def test_feed_by_parsing_it(self):
        feed_warnfile = self.feed_warnfile
        app = TestApp(buildername='html', warning=feed_warnfile, cleanenv=True)  
        app.build(force_all=True, filenames=[]) #build_all misses the crucial finish signal
        feed_warnings = feed_warnfile.getvalue().replace(os.sep, '/')
        feed_warnings_exp = self.FEED_WARNINGS % {'root': app.srcdir}
        self.assertEqual(feed_warnings, feed_warnings_exp)
        rss_path = os.path.join(app.outdir, 'rss.xml')
        self.assertTrue(exists(rss_path))
    
        base_path = unicode("file:/" + app.outdir)
    
        # see http://www.feedparser.org/
        f = feedparser.parse(rss_path)
        #feedparser well-formedness detection. We want this.
        self.assertEqual(f.bozo, 0 )
        self.assertEqual(f.feed['title'], 'Sphinx Syndicate Test Title')
        entries = f.entries
        self.assertEqual(entries[0].updated_parsed[0:6], (2001, 8, 11, 13, 0, 0))
        self.assertEqual(entries[0].title, "The latest blog post")
    
        self.assertEqual(entries[0].link, base_path + '/B_latest.html')
        self.assertEqual(entries[0].guid, base_path + '/B_latest.html')
        self.assertEqual(entries[1].updated_parsed[0:6], (2001, 8, 11, 9, 0, 0))
        self.assertEqual(entries[1].title, "An older blog post")
        self.assertEqual(entries[1].link, base_path + '/A_older.html')
        self.assertEqual(entries[1].guid, base_path + '/A_older.html')
        self.assertEqual(entries[2].updated_parsed[0:6], (1979, 1, 1, 0, 0, 0,))
        self.assertEqual(entries[2].title, "The oldest blog post")
        self.assertEqual(entries[2].link, base_path + '/C_most_aged.html')
        self.assertEqual(entries[2].guid, base_path + '/C_most_aged.html')
        #Now we do it all again to make sure that things work when handling stale files
        app2 = TestApp(buildername='html', warning=feed_warnfile)  
        app2.build(force_all=False, filenames=['most_aged'])
        f = feedparser.parse(rss_path)
        self.assertEqual(f.bozo, 0)
        entries = f.entries
        self.assertEqual(entries[0].updated_parsed[0:6], (2001, 8, 11, 13, 0, 0))
        self.assertEqual(entries[0].title, "The latest blog post")
        self.assertEqual(entries[1].updated_parsed[0:6], (2001, 8, 11, 9, 0, 0))
        self.assertEqual(entries[1].title, "An older blog post")
        self.assertEqual(entries[2].updated_parsed[0:6], (1979, 1, 1, 0, 0, 0))
        self.assertEqual(entries[2].title, "The oldest blog post")
    
        #Tests for relative URIs. note that these tests only work because there is
        # no xml:base - otherwise feedparser will supposedly fix them up for us - 
        # http://www.feedparser.org/docs/resolving-relative-links.html
        links = BeautifulSoup(entries[0].description).findAll('a')
        # These links will look like:
        #[<a class="headerlink" href="#the-latest-blog-post" title="Permalink to this headline">¶</a>, <a class="reference internal" href="older.html"><em>a relative link</em></a>, <a class="reference external" href="http://google.com/">an absolute link</a>]
        self.assertEqual(links.pop()['href'], "http://google.com/")
        self.assertEqual(links.pop()['href'], base_path + '/A_older.html')
        self.assertEqual(links.pop()['href'], entries[0].link + '#the-latest-blog-post')
    
        index_path  = os.path.join(app.outdir, 'index.html')
        soup = BeautifulSoup(open(index_path).read())
        latest_tree = soup.find('div', 'latest-wrapper')
        latest_items = latest_tree.findAll('li')
        actual_links = [entry.contents[0]['href'] for entry in latest_items]
        ideal_links = [
            u'B_latest.html',
            u'A_older.html',
            u'C_most_aged.html',
        ]
        
        self.assertListEqual(actual_links, ideal_links)
        
        app.cleanup()
        app2.cleanup()

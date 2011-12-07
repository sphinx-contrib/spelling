# -*- coding: utf-8 -*-
"""
    sphinxcontrib.nicovideo
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2011 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
import urllib2
from xml.dom import minidom

from docutils import nodes, utils
from docutils.parsers.rst import directives

from sphinx.util.nodes import split_explicit_title
from sphinx.util.compat import Directive


class NicoVideo(object):
    """ Utility class for access movie info in nicovideo """

    def __init__(self, movie_id):
        movie_id = NicoVideo.regulate_movie_id(movie_id)
        url = 'http://www.nicovideo.jp/api/getthumbinfo/' + movie_id
        resp = urllib2.urlopen(url).read()
        self.__info = minidom.parseString(resp)

    @staticmethod
    def regulate_movie_id(movie_id):
        if re.search('^sm\d+$', movie_id):
            return movie_id
        elif re.search('^\d+$', movie_id):
            return 'sm' + movie_id
        else:
            return movie_id

    @property
    def url(self):
        return 'http://www.nicovideo.jp/watch/' + self.video_id

    @property
    def thumb_url(self):
        return 'http://ext.nicovideo.jp/thumb/' + self.video_id

    @property
    def thumbjs_url(self):
        return 'http://ext.nicovideo.jp/thumb_watch/' + self.video_id

    def __getattr__(self, name):
        try:
            tags = self.__info.getElementsByTagName(name)
            return tags[0].childNodes[0].nodeValue
        except:
            return None


class nicovideo(nodes.General, nodes.Element):
    pass


class NicoVideoDirective(Directive):
    """Directive for embedding nico-videos"""

    has_content = False
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'thumb': directives.flag,
    }

    def run(self):
        node = nicovideo(movie_id=self.arguments[0], thumb=('thumb' in self.options)) 
        return [node]


def visit_nicovideo_node(self, node):
    movie = NicoVideo(node['movie_id'])

    try:
        if node['thumb']:
            # embed movie as thumbnail
            attrs = dict(width=312, height=176, src=movie.thumb_url,
                         scrolling='no', style='border:solid 1px #CCC;',
                         frameborder='0')
            self.body.append(self.starttag(node, 'iframe', **attrs))
            self.body.append(self.starttag(node, 'noscript'))
            self.body.append(self.starttag(node, 'a', href=movie.url))
            self.body.append(movie.title)
            self.body.append('</a></noscript></iframe>')
        else:
            # embed movie using player
            attrs = dict(type='text/javascript', src=movie.thumbjs_url)
            self.body.append(self.starttag(node, 'script', **attrs))
            self.body.append('</script>')
            self.body.append(self.starttag(node, 'noscript'))
            self.body.append(self.starttag(node, 'a', href=movie.url))
            self.body.append(movie.title)
            self.body.append('</a></noscript>')
    except:
        self.builder.warn('fail to load nicovideo: %r' % node['movie_id'])
        raise nodes.SkipNode


def depart_nicovideo_node(self, node):
    pass


def nicovideo_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for linking to nicovideo pages."""
    text = utils.unescape(text)
    has_explicit, title, movie_id = split_explicit_title(text)

    try:
        movie = NicoVideo(movie_id)
        if has_explicit == False:
            title = movie.title

        ref = nodes.reference(rawtext, title, refuri=movie.url)
        return [ref], []
    except:
        msg = inliner.reporter.error('fail to load nicovideo: %s' % movie_id,
                                     line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]


def setup(app):
    app.add_role('nicovideo', nicovideo_role)
    app.add_node(nicovideo, html=(visit_nicovideo_node, depart_nicovideo_node))
    app.add_directive('nicovideo', NicoVideoDirective)

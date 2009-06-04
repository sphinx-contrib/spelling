# -*- coding: utf-8 -*-
"""
    sphinxcontrib.aafig
    ~~~~~~~~~~~~~~~~~~~

    Allow embeded ASCII art to be rendered as nice looking images
    using the aafigure reStructuredText extension.

    See the README file for details.

    :copyright: Copyright 2009 by Leandro Lucarella <llucax@gmail.com> \
        (based on sphinxcontrib.mscgen).
    :license: BSD, see LICENSE for details.
"""

import posixpath
from os import path
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.errors import SphinxError
from sphinx.util import ensuredir
from sphinx.util.compat import Directive

import aafigure

DEFAULT_PREFIX = 'aafig'

class AafigError(SphinxError):
    category = 'aafig error'


class aafig(nodes.General, nodes.Element):
    pass


class Aafig(Directive):
    """
    Directive to insert an ASCII art figure to be rendered by aafigure.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = dict(
        scale        = float,
        line_width   = float,
        background   = str,
        foreground   = str,
        fill         = str,
        aspect       = float,
        textual      = directives.flag,
        proportional = directives.flag,
    )

    def run(self):
        node = aafig()
        node['text'] = '\n'.join(self.content)
	if 'textual' in self.options: self.options['textual'] = True
	if 'proportional' in self.options: self.options['proportional'] = True
        node['options'] = self.options
        return [node]


def render_aafigure(self, text, options, prefix):
    """
    Render an ASCII art figure into the requested format output file.
    """
    hashkey = text.encode('utf-8') + str(options)
    id = sha(hashkey).hexdigest()
    fname = '%s-%s.%s' % (prefix, id, options['format'])
    if hasattr(self.builder, 'imgpath'):
        # HTML
        relfn = posixpath.join(self.builder.imgpath, fname)
        outfn = path.join(self.builder.outdir, '_images', fname)
    else:
        # LaTeX
        relfn = fname
        outfn = path.join(self.builder.outdir, fname)

    if path.isfile(outfn):
        return relfn, outfn, id

    ensuredir(path.dirname(outfn))

    try:
        aafigure.render(text, outfn, options)
    except aafigure.UnsupportedFormatError, e:
        raise MscgenError(str(e))

    return relfn, outfn, id


def render_html(self, node, text, options, prefix=DEFAULT_PREFIX, imgcls=None):
    try:
        options['format'] = self.builder.config.aafig_format['html']
        fname, outfn, id = render_aafigure(self, text, options, prefix)
    except AafigError, exc:
        self.builder.warn('aafigure error: ' + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'p', CLASS='aafigure'))
    if fname is None:
        self.body.append(self.encode(text))
    else:
        imgcss = imgcls and 'class="%s"' % imgcls or ''
        # nothing in image map
        self.body.append('<img src="%s" alt="%s" %s/>\n' %
                         (fname, self.encode(text).strip(), imgcss))
    self.body.append('</p>\n')
    raise nodes.SkipNode


def html_visit(self, node):
    render_html(self, node, node['text'], node['options'])


def render_latex(self, node, text, options, prefix=DEFAULT_PREFIX):
    try:
        options['format'] = self.builder.config.aafig_format['latex']
        fname, outfn, id = render_aafigure(self, text, options, prefix)
    except AafigError, exc:
        self.builder.warn('aafigure error: ' + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\includegraphics[]{%s}' % fname)
    raise nodes.SkipNode


def latex_visit(self, node):
    render_latex(self, node, node['text'], node['options'])


def setup(app):
    app.add_node(aafig, html=(html_visit, None), latex=(latex_visit, None))
    app.add_directive('aafig', Aafig)
    app.add_config_value('aafig_format', dict(html='svg', latex='pdf'), 'html')


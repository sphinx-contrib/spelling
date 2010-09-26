# -*- coding: utf-8 -*-
"""
    blockdiag.sphinx_ext
    ~~~~~~~~~~~~~~~~~~~~

    Allow blockdiag-formatted diagrams to be included in Sphinx-generated
    documents inline.

    :copyright: Copyright 2010 by Takeshi Komiya.
    :license: BSDL.
"""

from __future__ import absolute_import
import posixpath
import os
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.errors import SphinxError
from sphinx.util.osutil import ensuredir, ENOENT, EPIPE
from sphinx.util.compat import Directive

from blockdiag.blockdiag import *
from blockdiag.diagparser import *


class BlockdiagError(SphinxError):
    category = 'Blockdiag error'


class blockdiag(nodes.General, nodes.Element):
    pass


class Blockdiag(Directive):
    """
    Directive to insert arbitrary dot markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'alt': directives.unchanged,
    }

    def run(self):
        dotcode = '\n'.join(self.content)
        if not dotcode.strip():
            return [self.state_machine.reporter.warning(
                'Ignoring "blockdiag" directive without content.',
                line=self.lineno)]
        node = blockdiag()
        node['code'] = dotcode
        node['options'] = []
        if 'alt' in self.options:
            node['alt'] = self.options['alt']
        return [node]


def render_dot(self, code, options, prefix='blockdiag'):
    """
    Render blockdiag code into a PNG output file.
    """
    hashkey = code.encode('utf-8') + str(options)
    fname = '%s-%s.png' % (prefix, sha(hashkey).hexdigest())
    if hasattr(self.builder, 'imgpath'):
        # HTML
        relfn = posixpath.join(self.builder.imgpath, fname)
        outfn = os.path.join(self.builder.outdir, '_images', fname)
    else:
        # LaTeX
        relfn = fname
        outfn = os.path.join(self.builder.outdir, fname)

    if os.path.isfile(outfn):
        return relfn, outfn

    ensuredir(os.path.dirname(outfn))

    # blockdiag expects UTF-8 by default
    if isinstance(code, unicode):
        code = code.encode('utf-8')

    ttfont = None
    fontpath = self.builder.config.blockdiag_fontpath
    if fontpath and not hasattr(self.builder, '_blockdiag_fontpath_warned'):
        try:
            ttfont = ImageFont.truetype(fontpath, 11)
        except IOError:
            self.builder.warn('blockdiag cannot load "%s" as truetype font, '
                              'check the blockdiag_path setting' % fontpath)
            self.builder._blockdiag_fontpath_warned = True

    try:
        tree = parse(tokenize(code))
        screen = ScreenNodeBuilder.build(tree)

        draw = DiagramDraw.DiagramDraw()
        draw.draw(screen, font=ttfont)
        draw.save(outfn, 'PNG')
    except Exception, e:
        raise BlockdiagError('blockdiag error:\n%s\n' % e)

    return relfn, outfn


def render_dot_html(self, node, code, options, prefix='blockdiag',
                    imgcls=None, alt=None):
    try:
        fname, outfn = render_dot(self, code, options, prefix)
    except BlockdiagError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'p', CLASS='blockdiag'))
    if fname is None:
        self.body.append(self.encode(code))
    else:
        if alt is None:
            alt = node.get('alt', self.encode(code).strip())

        self.body.append('<img src="%s" alt="%s"/>\n' % (fname, alt))

    self.body.append('</p>\n')
    raise nodes.SkipNode


def html_visit_blockdiag(self, node):
    render_dot_html(self, node, node['code'], node['options'])


def render_dot_latex(self, node, code, options, prefix='sdedit'):
    try:
        fname, outfn = render_dot(self, code, options, prefix)
    except SdeditError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\includegraphics{%s}' % fname)
    raise nodes.SkipNode


def latex_visit_blockdiag(self, node):
    render_dot_latex(self, node, node['code'], node['options'])


def setup(app):
    app.add_node(blockdiag,
                 html=(html_visit_blockdiag, None),
                 latex=(latex_visit_blockdiag, None))
    app.add_directive('blockdiag', Blockdiag)
    app.add_config_value('blockdiag_fontpath', None, 'html')

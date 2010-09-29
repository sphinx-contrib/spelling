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
        'maxwidth': directives.nonnegative_int,
    }

    def run(self):
        dotcode = '\n'.join(self.content)
        if not dotcode.strip():
            return [self.state_machine.reporter.warning(
                'Ignoring "blockdiag" directive without content.',
                line=self.lineno)]
        node = blockdiag()
        node['code'] = dotcode
        node['options'] = {}
        if 'alt' in self.options:
            node['alt'] = self.options['alt']
        if 'maxwidth' in self.options:
            node['options']['maxwidth'] = self.options['maxwidth']
        return [node]


def get_image_filename(self, code, options, prefix='blockdiag'):
    """
    Get path of output file.
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

    return relfn, outfn


def create_blockdiag(self, code, options, prefix='blockdiag'):
    """
    Render blockdiag code into a PNG output file.
    """
    # blockdiag expects UTF-8 by default
    if isinstance(code, unicode):
        code = code.encode('utf-8')

    if self.builder.config.blockdiag_antialias:
        scale = 2
    else:
        scale = 1

    ttfont = None
    fontpath = self.builder.config.blockdiag_fontpath
    if fontpath and not hasattr(self.builder, '_blockdiag_fontpath_warned'):
        if not os.path.isfile(fontpath):
            self.builder.warn('blockdiag cannot load "%s" as truetype font, '
                              'check the blockdiag_path setting' % fontpath)
            self.builder._blockdiag_fontpath_warned = True

    draw = None
    try:
        tree = parse(tokenize(code))
        screen = ScreenNodeBuilder.build(tree)

        draw = DiagramDraw.DiagramDraw(scale=scale, font=fontpath)
        draw.draw(screen)
    except Exception, e:
        raise BlockdiagError('blockdiag error:\n%s\n' % e)

    return draw


def render_dot_html(self, node, code, options, prefix='blockdiag',
                    imgcls=None, alt=None):
    has_thumbnail = False
    try:
        relfn, outfn = get_image_filename(self, code, options, prefix)

        image = create_blockdiag(self, code, options, prefix)
        image.save(outfn, 'PNG')

        image_size = image.image.size
        if 'maxwidth' in options and options['maxwidth'] < image_size[0]:
            has_thumbnail = True
            thumb_prefix = prefix + '_thumb'
            trelfn, toutfn = get_image_filename(self, code,
                                                options, thumb_prefix)

            thumb_size = (options['maxwidth'], image_size[1])
            image.save(toutfn, 'PNG', thumb_size)
            thumb_size = image.image.size

    except BlockdiagError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'p', CLASS='blockdiag'))
    if relfn is None:
        self.body.append(self.encode(code))
    else:
        if alt is None:
            alt = node.get('alt', self.encode(code).strip())

        imgtag_format = '<img src="%s" alt="%s" width="%s" height="%s" />\n'
        if has_thumbnail:
            self.body.append('<a href="%s">' % relfn)
            self.body.append(imgtag_format %
                             (trelfn, alt, thumb_size[0], thumb_size[1]))
            self.body.append('</a>')
        else:
            self.body.append(imgtag_format %
                             (relfn, alt, image_size[0], image_size[1]))

    self.body.append('</p>\n')
    raise nodes.SkipNode


def html_visit_blockdiag(self, node):
    render_dot_html(self, node, node['code'], node['options'])


def render_dot_latex(self, node, code, options, prefix='sdedit'):
    try:
        fname, outfn = get_image_filename(self, code, options, prefix)

        image = create_blockdiag(self, code, options, prefix)
        image.save(fname, 'PNG')

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
    app.add_config_value('blockdiag_antialias', False, 'html')

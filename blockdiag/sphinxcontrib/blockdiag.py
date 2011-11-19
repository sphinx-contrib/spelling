# -*- coding: utf-8 -*-
"""
    blockdiag.sphinx_ext
    ~~~~~~~~~~~~~~~~~~~~

    Allow blockdiag-formatted diagrams to be included in Sphinx-generated
    documents inline.

    :copyright: Copyright 2010 by Takeshi Komiya.
    :license: BSDL.
"""

import posixpath
import os
import codecs
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.errors import SphinxError
from sphinx.util.osutil import ensuredir, ENOENT, EPIPE
from sphinx.util.compat import Directive

from blockdiag_sphinxhelper import command, diagparser, builder, DiagramDraw
from blockdiag_sphinxhelper import collections, FontMap
from blockdiag_sphinxhelper import blockdiag, BlockdiagDirective
namedtuple = collections.namedtuple


class BlockdiagError(SphinxError):
    category = 'Blockdiag error'


class Blockdiag(BlockdiagDirective):
    def node2image(self, node, diagram):
        return node


def get_image_filename(self, code, format, options, prefix='blockdiag'):
    """
    Get path of output file.
    """
    if format not in ('PNG', 'PDF'):
        raise BlockdiagError('blockdiag error:\nunknown format: %s\n' % format)

    if format == 'PDF':
        try:
            import reportlab
        except ImportError:
            msg = 'blockdiag error:\n' + \
                  'colud not output PDF format; Install reportlab\n'
            raise BlockdiagError(msg)

    hashkey = code.encode('utf-8') + str(options)
    fname = '%s-%s.%s' % (prefix, sha(hashkey).hexdigest(), format.lower())
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


def get_fontmap(self):
    try:
        fontmappath = self.builder.config.blockdiag_fontmap
        fontmap = FontMap(fontmappath)
    except:
        attrname = '_blockdiag_fontmap_warned'
        if not hasattr(self.builder, attrname):
            msg = ('blockdiag cannot load "%s" as fontmap file, '
                   'check the blockdiag_fontmap setting' % fontmappath)
            self.builder.warn(msg)
            setattr(self.builder, attrname, True)

        fontmap = FontMap(None)

    try:
        fontpath = self.builder.config.blockdiag_fontpath
        if isinstance(fontpath, (str, unicode)):
            fontpath = [fontpath]

        if fontpath:
            config = namedtuple('Config', 'font')(fontpath)
            _fontpath = command.detectfont(config)
            fontmap.set_default_font(_fontpath)
    except:
        attrname = '_blockdiag_fontpath_warned'
        if not hasattr(self.builder, attrname):
            msg = ('blockdiag cannot load "%s" as truetype font, '
                   'check the blockdiag_fontpath setting' % fontpath)
            self.builder.warn(msg)
            setattr(self.builder, attrname, True)

    return fontmap


def create_blockdiag(self, code, format, filename, options, prefix='blockdiag'):
    """
    Render blockdiag code into a PNG output file.
    """
    draw = None
    fontmap = get_fontmap(self)
    try:
        tree = diagparser.parse(diagparser.tokenize(code))
        screen = builder.ScreenNodeBuilder.build(tree)

        antialias = self.builder.config.blockdiag_antialias
        draw = DiagramDraw.DiagramDraw(format, screen, filename, fontmap=fontmap,
                                       antialias=antialias)
    except Exception, e:
        raise BlockdiagError('blockdiag error:\n%s\n' % e)

    return draw


def render_dot_html(self, node, code, options, prefix='blockdiag',
                    imgcls=None, alt=None):
    has_thumbnail = False
    try:
        format = self.builder.config.blockdiag_html_image_format
        relfn, outfn = get_image_filename(self, code, format, options, prefix)

        image = create_blockdiag(self, code, format, outfn, options, prefix)
        if not os.path.isfile(outfn):
            image.draw()
            image.save()

        # generate thumbnails
        image_size = image.pagesize()
        if 'maxwidth' in options and options['maxwidth'] < image_size[0]:
            has_thumbnail = True
            thumb_prefix = prefix + '_thumb'
            trelfn, toutfn = get_image_filename(self, code, format,
                                                options, thumb_prefix)

            ratio = float(options['maxwidth']) / image_size[0]
            thumb_size = (options['maxwidth'], image_size[1] * ratio)
            if not os.path.isfile(toutfn):
                image.filename = toutfn
                image.draw()
                image.save(thumb_size)

    except UnicodeEncodeError, e:
        msg = ("blockdiag error: UnicodeEncodeError caught "
               "(check your font settings)")
        self.builder.warn(msg)
        raise nodes.SkipNode
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


def render_dot_latex(self, node, code, options, prefix='blockdiag'):
    try:
        format = self.builder.config.blockdiag_tex_image_format
        fname, outfn = get_image_filename(self, code, format, options, prefix)

        image = create_blockdiag(self, code, format, outfn, options, prefix)
        if not os.path.isfile(outfn):
            image.draw()
            image.save()

    except BlockdiagError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\par\\includegraphics{%s}\\par' % fname)
    raise nodes.SkipNode


def latex_visit_blockdiag(self, node):
    render_dot_latex(self, node, node['code'], node['options'])


def on_doctree_resolved(self, doctree, docname):
    if self.builder.name in ('html', 'latex'):
        return

    for node in doctree.traverse(blockdiag):  
        code = node['code']
        prefix = 'blockdiag'
        format = 'PNG'
        options = node['options']
        relfn, outfn = get_image_filename(self, code, format, options, prefix)

        image = create_blockdiag(self, code, format, outfn, options, prefix)
        if not os.path.isfile(outfn):
            image.draw()
            image.save()

        image = nodes.image(uri=outfn)
        node.parent.replace(node, image)


def setup(app):
    app.add_node(blockdiag,
                 html=(html_visit_blockdiag, None),
                 latex=(latex_visit_blockdiag, None))
    app.add_directive('blockdiag', Blockdiag)
    app.add_config_value('blockdiag_fontpath', None, 'html')
    app.add_config_value('blockdiag_fontmap', None, 'html')
    app.add_config_value('blockdiag_antialias', False, 'html')
    app.add_config_value('blockdiag_html_image_format', 'PNG', 'html')
    app.add_config_value('blockdiag_tex_image_format', 'PNG', 'html')
    app.connect("doctree-resolved", on_doctree_resolved)

# -*- coding: utf-8 -*-
"""
    nwdiag.sphinx_ext
    ~~~~~~~~~~~~~~~~~~~~

    Allow nwdiag-formatted diagrams to be included in Sphinx-generated
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

from nwdiag_sphinxhelper import command, diagparser, builder, DiagramDraw
from nwdiag_sphinxhelper import collections, FontMap
from nwdiag_sphinxhelper import nwdiag, NwdiagDirective
namedtuple = collections.namedtuple


class NwdiagError(SphinxError):
    category = 'Nwdiag error'


class Nwdiag(NwdiagDirective):
    def node2image(self, node, diagram):
        return node


def get_image_filename(self, code, format, options, prefix='nwdiag'):
    """
    Get path of output file.
    """
    if format not in ('PNG', 'PDF'):
        raise NwdiagError('nwdiag error:\nunknown format: %s\n' % format)

    if format == 'PDF':
        try:
            import reportlab
        except ImportError:
            msg = 'nwdiag error:\n' + \
                  'colud not output PDF format; Install reportlab\n'
            raise NwdiagError(msg)

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
        fontmappath = self.builder.config.nwdiag_fontmap
        fontmap = FontMap(fontmappath)
    except:
        attrname = '_nwdiag_fontmap_warned'
        if not hasattr(self.builder, attrname):
            msg = ('nwdiag cannot load "%s" as fontmap file, '
                   'check the nwdiag_fontmap setting' % fontmappath)
            self.builder.warn(msg)
            setattr(self.builder, attrname, True)

        fontmap = FontMap(None)

    try:
        fontpath = self.builder.config.nwdiag_fontpath
        if isinstance(fontpath, (str, unicode)):
            fontpath = [fontpath]

        if fontpath:
            config = namedtuple('Config', 'font')(fontpath)
            _fontpath = command.detectfont(config)
            fontmap.set_default_font(_fontpath)
    except:
        attrname = '_nwdiag_fontpath_warned'
        if not hasattr(self.builder, attrname):
            msg = ('nwdiag cannot load "%s" as truetype font, '
                   'check the nwdiag_fontpath setting' % fontpath)
            self.builder.warn(msg)
            setattr(self.builder, attrname, True)

    return fontmap


def create_nwdiag(self, code, format, filename, options, prefix='nwdiag'):
    """
    Render nwdiag code into a PNG output file.
    """
    draw = None
    fontmap = get_fontmap(self)
    try:
        tree = diagparser.parse(diagparser.tokenize(code))
        screen = builder.ScreenNodeBuilder.build(tree)

        antialias = self.builder.config.nwdiag_antialias
        draw = DiagramDraw.DiagramDraw(format, screen, filename, fontmap=fontmap,
                                       antialias=antialias)
    except Exception, e:
        raise NwdiagError('nwdiag error:\n%s\n' % e)

    return draw


def render_dot_html(self, node, code, options, prefix='nwdiag',
                    imgcls=None, alt=None):
    has_thumbnail = False
    try:
        format = self.builder.config.nwdiag_html_image_format
        relfn, outfn = get_image_filename(self, code, format, options, prefix)

        image = create_nwdiag(self, code, format, outfn, options, prefix)
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
        msg = ("nwdiag error: UnicodeEncodeError caught "
               "(check your font settings)")
        self.builder.warn(msg)
        raise nodes.SkipNode
    except NwdiagError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'p', CLASS='nwdiag'))
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


def html_visit_nwdiag(self, node):
    render_dot_html(self, node, node['code'], node['options'])


def render_dot_latex(self, node, code, options, prefix='nwdiag'):
    try:
        format = self.builder.config.nwdiag_tex_image_format
        fname, outfn = get_image_filename(self, code, format, options, prefix)

        image = create_nwdiag(self, code, format, outfn, options, prefix)
        if not os.path.isfile(outfn):
            image.draw()
            image.save()

    except NwdiagError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\par\\includegraphics{%s}\\par' % fname)
    raise nodes.SkipNode


def latex_visit_nwdiag(self, node):
    render_dot_latex(self, node, node['code'], node['options'])


def on_doctree_resolved(self, doctree, docname):
    if self.builder.name in ('html', 'latex'):
        return

    for node in doctree.traverse(nwdiag):  
        code = node['code']
        prefix = 'nwdiag'
        format = 'PNG'
        options = node['options']
        relfn, outfn = get_image_filename(self, code, format, options, prefix)

        image = create_nwdiag(self, code, format, outfn, options, prefix)
        if not os.path.isfile(outfn):
            image.draw()
            image.save()

        image = nodes.image(uri=outfn)
        node.parent.replace(node, image)


def setup(app):
    app.add_node(nwdiag,
                 html=(html_visit_nwdiag, None),
                 latex=(latex_visit_nwdiag, None))
    app.add_directive('nwdiag', Nwdiag)
    app.add_config_value('nwdiag_fontpath', None, 'html')
    app.add_config_value('nwdiag_fontmap', None, 'html')
    app.add_config_value('nwdiag_antialias', False, 'html')
    app.add_config_value('nwdiag_html_image_format', 'PNG', 'html')
    app.add_config_value('nwdiag_tex_image_format', 'PNG', 'html')
    app.connect("doctree-resolved", on_doctree_resolved)

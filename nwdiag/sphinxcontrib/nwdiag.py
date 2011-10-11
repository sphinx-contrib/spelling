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

from nwdiag_sphinxhelper import diagparser, builder, DiagramDraw


class NwdiagError(SphinxError):
    category = 'Nwdiag error'


class nwdiag(nodes.General, nodes.Element):
    pass


class Nwdiag(Directive):
    """
    Directive to insert arbitrary dot markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'alt': directives.unchanged,
        'desctable': directives.flag,
        'maxwidth': directives.nonnegative_int,
    }

    def run(self):
        if self.arguments:
            document = self.state.document
            if self.content:
                return [document.reporter.warning(
                    'nwdiag directive cannot have both content and '
                    'a filename argument', line=self.lineno)]
            env = self.state.document.settings.env
            rel_filename, filename = relfn2path(env, self.arguments[0])
            env.note_dependency(rel_filename)
            try:
                fp = codecs.open(filename, 'r', 'utf-8')
                try:
                    dotcode = fp.read()
                finally:
                    fp.close()
            except (IOError, OSError):
                return [document.reporter.warning(
                    'External nwdiag file %r not found or reading '
                    'it failed' % filename, line=self.lineno)]
        else:
            dotcode = '\n'.join(self.content)
            if not dotcode.strip():
                return [self.state_machine.reporter.warning(
                    'Ignoring "nwdiag" directive without content.',
                    line=self.lineno)]

        node = nwdiag()
        node['code'] = dotcode
        node['options'] = {}
        if 'alt' in self.options:
            node['alt'] = self.options['alt']
        if 'maxwidth' in self.options:
            node['options']['maxwidth'] = self.options['maxwidth']
        if 'desctable' in self.options:
            node['options']['desctable'] = self.options['desctable']
        return [node]


# compatibility to sphinx 1.0 (ported from sphinx trunk)
def relfn2path(env, filename, docname=None):
    if filename.startswith('/') or filename.startswith(os.sep):
        rel_fn = filename[1:]
    else:
        docdir = os.path.dirname(env.doc2path(docname or env.docname,
                                              base=None))
        rel_fn = os.path.join(docdir, filename)
    try:
        return rel_fn, os.path.join(env.srcdir, rel_fn)
    except UnicodeDecodeError:
        # the source directory is a bytestring with non-ASCII characters;
        # let's try to encode the rel_fn in the file system encoding
        enc_rel_fn = rel_fn.encode(sys.getfilesystemencoding())
        return rel_fn, os.path.join(env.srcdir, enc_rel_fn)


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


def get_fontpath(self):
    fontpath = None
    if self.builder.config.nwdiag_fontpath:
        nwdiag_fontpath = self.builder.config.nwdiag_fontpath

        if isinstance(nwdiag_fontpath, (str, unicode)):
            nwdiag_fontpath = [nwdiag_fontpath]

        for path in nwdiag_fontpath:
            if os.path.isfile(path):
                fontpath = path

        if fontpath is None:
            attrname = '_nwdiag_fontpath_warned'
            if not hasattr(self.builder, attrname):
                msg = ('nwdiag cannot load "%s" as truetype font, '
                       'check the nwdiag_path setting' % fontpath)
                self.builder.warn(msg)

                setattr(self.builder, attrname, True)

    return fontpath


def create_nwdiag(self, code, format, filename, options, prefix='nwdiag'):
    """
    Render nwdiag code into a PNG output file.
    """
    draw = None
    fontpath = get_fontpath(self)
    try:
        tree = diagparser.parse(diagparser.tokenize(code))
        screen = builder.ScreenNodeBuilder.build(tree)

        antialias = self.builder.config.nwdiag_antialias
        draw = DiagramDraw.DiagramDraw(format, screen, filename, font=fontpath,
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

            thumb_size = (options['maxwidth'], image_size[1])
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

    render_desctable(self, image, options)

    self.body.append('</p>\n')
    raise nodes.SkipNode


def render_desctable(self, diagram, options):
    if 'desctable' not in options:
         return

    def cmp_number(a, b):
        if a[1] and a[1].isdigit():
            n1 = int(a[1])
        else:
            n1 = 65535

        if b[1] and b[1].isdigit():
            n2 = int(b[1])
        else:
            n2 = 65535

        return cmp(n1, n2)

    from xml.sax.saxutils import escape

    descriptions = []
    for n in diagram.diagram.traverse_nodes():
        if hasattr(n, 'description') and n.description:
            label = n.label or n.id
            descriptions.append((label, n.numbered, n.address, n.description))
    descriptions.sort(cmp_number)

    if descriptions:
        numbered = [x for x in descriptions if x[1]]

        self.body.append('<table border="1" class="docutils">')
        self.body.append('<thead valign="bottom">')
        if numbered:
            self.body.append('<tr><th class="head">No</th><th class="head">Name</th><th class="head">Address</th><th class="head">Description</th></tr>')
        else:
            self.body.append('<tr><th class="head">Name</th><th class="head">Address</th><th class="head">Description</th></tr>')
        self.body.append('</thead>')
        self.body.append('<tbody valign="top">')

        for desc in descriptions:
            id, number, address, text = desc
            self.body.append('<tr>')
            if numbered:
                if number is not None:
                    self.body.append('<td>%s</td>' % escape(number))
                else:
                    self.body.append('<td></td>')
            self.body.append('<td>%s</td>' % id)
            self.body.append('<td>%s</td>' % "<br />".join(escape(v) for k, v in address.items()))
            self.body.append('<td>%s</td>' % escape(text))
            self.body.append('</tr>')

        self.body.append('</tbody>')
        self.body.append('</table>')


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


def setup(app):
    app.add_node(nwdiag,
                 html=(html_visit_nwdiag, None),
                 latex=(latex_visit_nwdiag, None))
    app.add_directive('nwdiag', Nwdiag)
    app.add_config_value('nwdiag_fontpath', None, 'html')
    app.add_config_value('nwdiag_antialias', False, 'html')
    app.add_config_value('nwdiag_html_image_format', 'PNG', 'html')
    app.add_config_value('nwdiag_tex_image_format', 'PNG', 'html')

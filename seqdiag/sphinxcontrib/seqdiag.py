# -*- coding: utf-8 -*-
"""
    seqdiag.sphinx_ext
    ~~~~~~~~~~~~~~~~~~~~

    Allow seqdiag-formatted diagrams to be included in Sphinx-generated
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

from seqdiag_sphinxhelper import diagparser, builder, DiagramDraw


class SeqdiagError(SphinxError):
    category = 'Seqdiag error'


class seqdiag(nodes.General, nodes.Element):
    pass


class Seqdiag(Directive):
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
                    'seqdiag directive cannot have both content and '
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
                    'External seqdiag file %r not found or reading '
                    'it failed' % filename, line=self.lineno)]
        else:
            dotcode = '\n'.join(self.content)
            if not dotcode.strip():
                return [self.state_machine.reporter.warning(
                    'Ignoring "seqdiag" directive without content.',
                    line=self.lineno)]

        node = seqdiag()
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


def get_image_filename(self, code, format, options, prefix='seqdiag'):
    """
    Get path of output file.
    """
    if format not in ('PNG', 'PDF'):
        raise SeqdiagError('seqdiag error:\nunknown format: %s\n' % format)

    if format == 'PDF':
        try:
            import reportlab
        except ImportError:
            msg = 'seqdiag error:\n' + \
                  'colud not output PDF format; Install reportlab\n'
            raise SeqdiagError(msg)

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
    if self.builder.config.seqdiag_fontpath:
        seqdiag_fontpath = self.builder.config.seqdiag_fontpath

        if isinstance(seqdiag_fontpath, (str, unicode)):
            seqdiag_fontpath = [seqdiag_fontpath]

        for path in seqdiag_fontpath:
            if os.path.isfile(path):
                fontpath = path

        if fontpath is None:
            attrname = '_seqdiag_fontpath_warned'
            if not hasattr(self.builder, attrname):
                msg = ('seqdiag cannot load "%s" as truetype font, '
                       'check the seqdiag_path setting' % fontpath)
                self.builder.warn(msg)

                setattr(self.builder, attrname, True)

    return fontpath


def create_seqdiag(self, code, format, filename, options, prefix='seqdiag'):
    """
    Render seqdiag code into a PNG output file.
    """
    draw = None
    fontpath = get_fontpath(self)
    try:
        tree = diagparser.parse(diagparser.tokenize(code))
        screen = builder.ScreenNodeBuilder.build(tree)

        antialias = self.builder.config.seqdiag_antialias
        draw = DiagramDraw.DiagramDraw(format, screen, filename, font=fontpath,
                                       antialias=antialias)
    except Exception, e:
        raise SeqdiagError('seqdiag error:\n%s\n' % e)

    return draw


def render_dot_html(self, node, code, options, prefix='seqdiag',
                    imgcls=None, alt=None):
    has_thumbnail = False
    try:
        format = self.builder.config.seqdiag_html_image_format
        relfn, outfn = get_image_filename(self, code, format, options, prefix)

        image = create_seqdiag(self, code, format, outfn, options, prefix)
        if not os.path.isfile(outfn):
            image.draw()
            image.save()

        # generate thumbnails
        image_size = image.drawer.image.size
        if 'maxwidth' in options and options['maxwidth'] < image_size[0]:
            has_thumbnail = True
            thumb_prefix = prefix + '_thumb'
            trelfn, toutfn = get_image_filename(self, code, format,
                                                options, thumb_prefix)

            thumb_size = (options['maxwidth'], image_size[1])
            if not os.path.isfile(toutfn):
                image.draw()
                image.save(toutfn, thumb_size)
            thumb_size = image.drawer.image.size

    except SeqdiagError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'p', CLASS='seqdiag'))
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
            descriptions.append((n.id, n.numbered, n.description))
    descriptions.sort(cmp_number)


    if descriptions:
        numbered = [x for x in descriptions if x[1]]

        self.body.append('<table border="1" class="docutils">')
        self.body.append('<thead valign="bottom">')
        if numbered:
            self.body.append('<tr><th class="head">No</th><th class="head">Name</th><th class="head">Description</th></tr>')
        else:
            self.body.append('<tr><th class="head">Name</th><th class="head">Description</th></tr>')
        self.body.append('</thead>')
        self.body.append('<tbody valign="top">')

        for desc in descriptions:
            id, number, text = desc
            self.body.append('<tr>')
            if numbered:
                if number is not None:
                    self.body.append('<td>%s</td>' % escape(number))
                else:
                    self.body.append('<td></td>')
            self.body.append('<td>%s</td>' % escape(id))
            self.body.append('<td>%s</td>' % escape(text))
            self.body.append('</tr>')

        self.body.append('</tbody>')
        self.body.append('</table>')


def html_visit_seqdiag(self, node):
    render_dot_html(self, node, node['code'], node['options'])


def render_dot_latex(self, node, code, options, prefix='seqdiag'):
    try:
        format = self.builder.config.seqdiag_tex_image_format
        fname, outfn = get_image_filename(self, code, format, options, prefix)

        image = create_seqdiag(self, code, format, outfn, options, prefix)
        if not os.path.isfile(outfn):
            image.draw()
            image.save()

    except SeqdiagError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\par\\includegraphics{%s}\\par' % fname)
    raise nodes.SkipNode


def latex_visit_seqdiag(self, node):
    render_dot_latex(self, node, node['code'], node['options'])


def setup(app):
    app.add_node(seqdiag,
                 html=(html_visit_seqdiag, None),
                 latex=(latex_visit_seqdiag, None))
    app.add_directive('seqdiag', Seqdiag)
    app.add_config_value('seqdiag_fontpath', None, 'html')
    app.add_config_value('seqdiag_antialias', False, 'html')
    app.add_config_value('seqdiag_html_image_format', 'PNG', 'html')
    app.add_config_value('seqdiag_tex_image_format', 'PNG', 'html')

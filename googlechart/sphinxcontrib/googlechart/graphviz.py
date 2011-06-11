# -*- coding: utf-8 -*-
"""
    sphinxcontrib.googlechart.graphviz
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Allow graphviz-formatted diagrams to be included in Sphinx-generated
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

from sphinxcontrib.googlechart.core import GoogleChart


class GraphvizError(SphinxError):
    category = 'Graphviz error'


class graphviz(nodes.General, nodes.Element):
    pass


class GraphvizBase(Directive):
    """
    Directive to insert arbitrary dot markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'type': directives.unchanged,
        'size': directives.unchanged,
    }

    codeheadings = None

    def run(self):
        if self.arguments and not self.codeheadings:
            document = self.state.document
            if self.content:
                return [document.reporter.warning(
                    'graphviz directive cannot have both content and '
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
                    'External graphviz file %r not found or reading '
                    'it failed' % filename, line=self.lineno)]
        else:
            dotcode = '\n'.join(self.content)
            if not dotcode.strip():
                return [self.state_machine.reporter.warning(
                    'Ignoring "graphviz" directive without content.',
                    line=self.lineno)]

        if self.codeheadings:
            if self.arguments:
                graph_name = self.arguments[0]
                dotcode = "%s %s { %s }" % (self.codeheadings, graph_name, dotcode)
            else:
                dotcode = "%s { %s }" % (self.codeheadings, dotcode)

        node = graphviz()
        node['code'] = dotcode
        node['options'] = {}
        if 'type' in self.options:
            node['options']['type'] = self.options['type']
        if 'size' in self.options:
            node['options']['size'] = self.options['size']

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


class Graphviz(GraphvizBase):
    pass


class Graphviz_Graph(GraphvizBase):
    required_arguments = 0
    codeheadings = 'graph'


class Graphviz_Digraph(GraphvizBase):
    required_arguments = 0
    codeheadings = 'digraph'


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


def get_image_filename(self, code, options, prefix='graphviz'):
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


def create_graphviz(self, code, format, filename, options, prefix='graphviz'):
    """
    Render graphviz code into a image file.
    """
    try:
        chart = GoogleChart(code, 'graphviz', type=options.get('type', 'dot'), size=options.get('size'))
        chart.save(filename)
    except:
        raise GraphvizError('graphviz error: a malformed or illegal request:')


def render_dot_html(self, node, code, options, prefix='graphviz',
                    imgcls=None, alt=None):
    has_thumbnail = False
    try:
        relfn, outfn = get_image_filename(self, code, options, prefix)
        if not os.path.isfile(outfn):
            create_graphviz(self, code, format, outfn, options, prefix)
    except GraphvizError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'p', CLASS='graphviz'))
    if relfn is None:
        self.body.append(self.encode(code))
    else:
        if alt is None:
            alt = node.get('alt', self.encode(code).strip())

        imgtag_format = '<img src="%s" alt="%s" />\n'
        self.body.append(imgtag_format % (relfn, alt))

    self.body.append('</p>\n')
    raise nodes.SkipNode


def html_visit_graphviz(self, node):
    render_dot_html(self, node, node['code'], node['options'])


def render_dot_latex(self, node, code, options, prefix='graphviz'):
    try:
        fname, outfn = get_image_filename(self, code, options, prefix)
        create_graphviz(self, code, format, outfn, options, prefix)
    except GraphvizError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\par\\includegraphics{%s}\\par' % fname)
    raise nodes.SkipNode


def latex_visit_graphviz(self, node):
    render_dot_latex(self, node, node['code'], node['options'])


def setup(app):
    app.add_node(graphviz,
                 html=(html_visit_graphviz, None),
                 latex=(latex_visit_graphviz, None))
    app.add_directive('graphviz', Graphviz)
    app.add_directive('graph', Graphviz_Graph)
    app.add_directive('digraph', Graphviz_Digraph)

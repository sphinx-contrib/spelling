# -*- coding: utf-8 -*-
"""
    sphinxcontrib.googlechart
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Allow DOT like formatted charts to be included in Sphinx-generated
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

from sphinxcontrib.googlechart import core


__import__('pkg_resources').declare_namespace(__name__)


class GoogleChartError(SphinxError):
    category = 'GoogleChart error'


class google_chart(nodes.General, nodes.Element):
    pass


class GoogleChartBase(Directive):
    """
    Directive to insert arbitrary dot markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'size': directives.unchanged,
    }

    codeheadings = None

    def run(self):
        dotcode = '\n'.join(self.content)
        if not dotcode.strip():
            return [self.state_machine.reporter.warning(
                'Ignoring "chart" directive without content.',
                line=self.lineno)]

        if self.codeheadings:
            if self.arguments:
                graph_name = self.arguments[0]
                dotcode = "%s %s { %s }" % (self.codeheadings, graph_name, dotcode)
            else:
                dotcode = "%s { %s }" % (self.codeheadings, dotcode)

        node = google_chart()
        node['code'] = dotcode
        node['options'] = {}
        if 'size' in self.options:
            node['options']['size'] = self.options['size']

        return [node]


class GoogleChart(GoogleChartBase):
    pass


class PieChart(GoogleChartBase):
    codeheadings = 'piechart'


class PieChart3D(GoogleChartBase):
    codeheadings = 'piechart_3d'


class LineChart(GoogleChartBase):
    codeheadings = 'linechart'


class LineChartXY(GoogleChartBase):
    codeheadings = 'linechartxy'


class HolizontalBarChart(GoogleChartBase):
    codeheadings = 'holizontal_barchart'


class VerticalBarChart(GoogleChartBase):
    codeheadings = 'vertical_barchart'


class HolizontalBarGraph(GoogleChartBase):
    codeheadings = 'holizontal_bargraph'


class VerticalBarGraph(GoogleChartBase):
    codeheadings = 'vertical_bargraph'


class VennDiagram(GoogleChartBase):
    codeheadings = 'venndiagram'


class PlotChart(GoogleChartBase):
    codeheadings = 'plotchart'


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


def get_image_filename(self, code, options, prefix='google_chart'):
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


def create_google_chart(self, code, format, filename, options, prefix='google_chart'):
    """
    Render google_chart code into a image file.
    """
    kwargs = {}
    if options.has_key('size'):
        kwargs['size'] = options['size']

    try:
        chart = core.GoogleChart(code, 'chart', **kwargs)
        chart.save(filename)
    except Exception, e:
        raise GoogleChartError(e)


def render_dot_html(self, node, code, options, prefix='google_chart',
                    imgcls=None, alt=None):
    has_thumbnail = False
    try:
        relfn, outfn = get_image_filename(self, code, options, prefix)
        if not os.path.isfile(outfn):
            create_google_chart(self, code, format, outfn, options, prefix)
    except GoogleChartError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'p', CLASS='google_chart'))
    if relfn is None:
        self.body.append(self.encode(code))
    else:
        if alt is None:
            alt = node.get('alt', self.encode(code).strip())

        imgtag_format = '<img src="%s" alt="%s" />\n'
        self.body.append(imgtag_format % (relfn, alt))

    self.body.append('</p>\n')
    raise nodes.SkipNode


def html_visit_google_chart(self, node):
    render_dot_html(self, node, node['code'], node['options'])


def render_dot_latex(self, node, code, options, prefix='google_chart'):
    try:
        fname, outfn = get_image_filename(self, code, options, prefix)
        create_google_chart(self, code, format, outfn, options, prefix)
    except GoogleChartError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\par\\includegraphics{%s}\\par' % fname)
    raise nodes.SkipNode


def latex_visit_google_chart(self, node):
    render_dot_latex(self, node, node['code'], node['options'])


def setup(app):
    app.add_node(google_chart,
                 html=(html_visit_google_chart, None),
                 latex=(latex_visit_google_chart, None))
    app.add_directive('chart', GoogleChart)
    app.add_directive('piechart', PieChart)
    app.add_directive('piechart3d', PieChart3D)
    app.add_directive('linechart', LineChart)
    app.add_directive('linechartxy', LineChartXY)
    app.add_directive('holizontal_barchart', HolizontalBarChart)
    app.add_directive('vertical_barchart', VerticalBarChart)
    app.add_directive('holizontal_bargraph', HolizontalBarGraph)
    app.add_directive('vertical_bargraph', VerticalBarGraph)
    app.add_directive('venndiagram', VennDiagram)
    app.add_directive('plotchart', PlotChart)

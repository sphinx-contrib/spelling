# -*- coding: utf-8 -*-
"""
    sphinxcontrib.mscgen
    ~~~~~~~~~~~~~~~~~~~~

    Allow mscgen-formatted :abbr:`MSC (Message Sequence Chart)` graphs to be
    included in Sphinx-generated documents inline.

    See the README file for details.

    :copyright: Copyright 2009 by Leandro Lucarella <llucax@gmail.com> \
        (based on sphinx.ext.graphviz).
    :license: BSD, see LICENSE for details.
"""

import sys
import posixpath
from os import path
from subprocess import Popen, PIPE
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes

from sphinx.errors import SphinxError
from sphinx.util import ensuredir
from sphinx.util.compat import Directive


class MscgenError(SphinxError):
    category = 'mscgen error'


class mscgen(nodes.General, nodes.Element):
    pass


class Mscgen(Directive):
    """
    Directive to insert arbitrary mscgen markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        node = mscgen()
        node['code'] = '\n'.join(self.content)
        return [node]


class MscgenSimple(Directive):
    """
    Directive to insert mscgen markup that goes inside ``msc { ... }``.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        node = mscgen()
        node['code'] = 'msc {\n%s\n}\n' % ('\n'.join(self.content))
        return [node]


def run_cmd(builder, cmd, cmd_name, cfg_name, stdin=''):
    try:
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    except OSError, err:
        if err.errno != 2:   # No such file or directory
            raise
        builder.warn('%s command %r cannot be run (needed for mscgen '
                          'output), check the %s setting' %
                          (cmd_name, builder.config.mscgen, cfg_name))
        builder._mscgen_warned = True
        return False
    stdout, stderr = p.communicate(stdin)
    if p.returncode != 0:
        raise MscgenError('%s exited with error:\n[stderr]\n%s\n'
                            '[stdout]\n%s' % (cmd_name, stderr, stdout))
    return True


def eps_to_pdf(builder, epsfn, pdffn):
    epstopdf_args = [builder.config.mscgen_epstopdf]
    epstopdf_args.extend(builder.config.mscgen_epstopdf_args)
    epstopdf_args.extend(['--outfile=' + pdffn, epsfn])
    return run_cmd(builder, epstopdf_args, 'epstopdf', 'mscgen_epstopdf')


def get_map_code(mapfn, id):
    mapfile = open(mapfn)
    try:
        lines = mapfile.readlines()
    finally:
        mapfile.close()
    mapcode = '<map id="%s" name="%s">' % (id, id)
    for line in lines:
        (type, name, coords) = line.split(' ', 2)
        mapcode += '<area shape="%s" href="%s" alt="" coords="%s" />' % (
                    type, name, coords)
    mapcode += '</map>'
    return mapcode


def render_msc(self, code, format, prefix='mscgen'):
    """
    Render mscgen code into a PNG or PDF output file.
    """
    hashkey = code.encode('utf-8') + str(self.builder.config.mscgen_args)
    id = sha(hashkey).hexdigest()
    fname = '%s-%s.%s' % (prefix, id, format)
    if hasattr(self.builder, 'imgpath'):
        # HTML
        relfn = posixpath.join(self.builder.imgpath, fname)
        outfn = path.join(self.builder.outdir, '_images', fname)
        tmpfn = outfn
        mapfn = outfn + '.map'
    else:
        # LaTeX
        relfn = fname
        outfn = path.join(self.builder.outdir, fname)
        format = 'eps'
        tmpfn = outfn[:-3] + format

    if path.isfile(outfn):
        return relfn, outfn, id

    if hasattr(self.builder, '_mscgen_warned'):
        return None, None, None

    ensuredir(path.dirname(outfn))

    # mscgen don't support encodings very well. ISO-8859-1 seems to work best,
    # at least for PNG.
    if isinstance(code, unicode):
        code = code.encode('iso-8859-1')

    mscgen_args = [self.builder.config.mscgen]
    mscgen_args.extend(self.builder.config.mscgen_args)
    mscgen_args.extend(['-T', format, '-o', tmpfn])
    if not run_cmd(self.builder, mscgen_args, 'mscgen', 'mscgen', code):
        return None, None, None

    if format == 'png':
        mscgen_args = mscgen_args[:-4] + ['-T', 'ismap', '-o', mapfn]
        if not run_cmd(self.builder, mscgen_args, 'mscgen', 'mscgen', code):
            return None, None, None
    else: # PDF/EPS
        if not eps_to_pdf(self.builder, tmpfn, outfn):
            return None, None, None

    return relfn, outfn, id


def render_msc_html(self, node, code, prefix='mscgen', imgcls=None):
    try:
        fname, outfn, id = render_msc(self, code, 'png', prefix)
    except MscgenError, exc:
        self.builder.warn('mscgen code %r: ' % code + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'p', CLASS='mscgen'))
    if fname is None:
        self.body.append(self.encode(code))
    else:
        imgmap = get_map_code(outfn + '.map', id)
        imgcss = imgcls and 'class="%s"' % imgcls or ''
        if not imgmap:
            # nothing in image map
            self.body.append('<img src="%s" alt="%s" %s/>\n' %
                             (fname, self.encode(code).strip(), imgcss))
        else:
            # has a map
            self.body.append('<img src="%s" alt="%s" usemap="#%s" %s/>\n' %
                             (fname, self.encode(code).strip(), id, imgcss))
            self.body.extend(imgmap)
    self.body.append('</p>\n')
    raise nodes.SkipNode


def html_visit_mscgen(self, node):
    render_msc_html(self, node, node['code'])


def render_msc_latex(self, node, code, prefix='mscgen'):
    try:
        fname, outfn, id = render_msc(self, code, 'pdf', prefix)
    except MscgenError, exc:
        self.builder.warn('mscgen code %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\includegraphics[]{%s}' % fname)
    raise nodes.SkipNode


def latex_visit_mscgen(self, node):
    render_msc_latex(self, node, node['code'])

def setup(app):
    app.add_node(mscgen,
                 html=(html_visit_mscgen, None),
                 latex=(latex_visit_mscgen, None))
    app.add_directive('mscgen', Mscgen)
    app.add_directive('msc', MscgenSimple)
    app.add_config_value('mscgen', 'mscgen', 'html')
    app.add_config_value('mscgen_args', [], 'html')
    app.add_config_value('mscgen_epstopdf', 'epstopdf', 'html')
    app.add_config_value('mscgen_epstopdf_args', [], 'html')


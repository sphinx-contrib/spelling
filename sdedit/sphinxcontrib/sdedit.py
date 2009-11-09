# -*- coding: utf-8 -*-
"""
    sdedit extension

    Generate sequence diagram via sdedit and insert it into Sphinx-generated
    documents.

    :copyright: Copyright 2009, SHIBUKAWA Yoshiki
    :license: BSD, see LICENSE for details.
"""

import re
import posixpath
import os
from subprocess import Popen, PIPE
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.errors import SphinxError
from sphinx.util import ensuredir
from sphinx.util.compat import Directive

from PIL import (Image, ImageFilter)


def boolean_input(argument):
    return directives.choice(argument.lower() , ('true', 'false')) == 'true'


class SdeditError(SphinxError):
    category = 'Sdedit error'


class sequence_diagram(nodes.General, nodes.Element):
    pass


class SequenceDiagram(Directive):
    """
    Directive to insert arbitrary dot markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'maxwidth': directives.nonnegative_int,
        'linewrap': boolean_input,
        'threadnumber': boolean_input,
    }

    def run(self):
        sdeditcode = '\n'.join(self.content)
        if not sdeditcode.strip():
            return [self.state_machine.reporter.warning(
                'Ignoring "sequence_diagram" directive without content.',
                line=self.lineno)]
        node = sequence_diagram()
        node['code'] = sdeditcode
        node['options'] = self.options
        return [node]


def render_sdx(self, code, options, format, prefix='sdedit'):
    """
    Render sequence diagram into a PNG or PDF output file.
    """
    hashkey = code.encode('utf-8') + str(options) + \
              str(self.builder.config.sdedit_args)
    ofname = '%s-%s.%s' % (prefix, sha(hashkey).hexdigest(), format)
    ifname = '%s-%s.sd' % (prefix, sha(hashkey).hexdigest())
    infn = os.path.join(self.builder.outdir, ifname)
    if hasattr(self.builder, 'imgpath'):
        # HTML
        relfn = posixpath.join(self.builder.imgpath, ofname)
        outfn = os.path.join(self.builder.outdir, '_images', ofname)
    else:
        # LaTeX
        relfn = ofname
        outfn = os.path.join(self.builder.outdir, ofname)
    if os.path.isfile(outfn):
        return relfn, outfn

    if hasattr(self.builder, '_sdedit_warned'):
        return None, None

    ensuredir(os.path.dirname(outfn))
    ensuredir(os.path.dirname(infn))
    inputfile = open(infn, "w")
    if isinstance(code, unicode):
        code = code.encode('utf-8')
    inputfile.write(code)
    inputfile.close()

    path = self.builder.config.sdedit_path
    if path.endswith(".jar"):
        sdedit_args = [self.builder.config.sdedit_java_path, "-jar", path]
    else:
        sdedit_args = [path]
    sdedit_args.extend(self.builder.config.sdedit_args)
    sdedit_args.extend(['-t', format, '-o', outfn, infn])
    if options.get("linewrap"):
        sdedit_args.extend(['--lineWrap', 'true'])
    if options.get("threadnumber"):
        sdedit_args.extend(['--threadNumbersVisible', 'true'])
    try:
        p = Popen(sdedit_args, stdout=PIPE, stdin=None, stderr=PIPE)
    except OSError, err:
        if err.errno != 2:   # No such file or directory
            raise
        self.builder.warn('sdedit command %r cannot be run (needed for '
                          'sequence diagram output), check the sdedit_path '
                          ' setting' %
                          self.builder.config.sdedit_path)
        self.builder._sdedit_warned = True
        return None, None

    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise SdeditError('sdedit exited with error:\n[stderr]\n%s\n'
                            '[stdout]\n%s' % (stderr, stdout))
    os.remove(infn)
    return relfn, outfn


def render_sdx_html(self, node, code, options, prefix='sdedit', imgcls=None):
    try:
        fname, outfn = render_sdx(self, code, options, 'png', prefix)
    except SdeditError, exc:
        self.builder.warn('sdedit code %r: ' % code + str(exc))
        raise nodes.SkipNode
    self.body.append(self.starttag(node, 'p', CLASS='sdedit'))
    if fname is None:
        self.body.append(self.encode(code))
    else:
        image = Image.open(outfn)
        width, height = image.size
        max_width = options.get('maxwidth')
        if not max_width:
            defaults = self.builder.config.sdedit_default_options
            max_width = defaults.get('maxwidth') 
        if width <= max_width:
            html_tag(self, code, fname, max_width, image, imgcls)
        else:
            html_tag_with_thumbnail(self, code, fname, max_width, image, imgcls)
    self.body.append('</p>\n')
    raise nodes.SkipNode


def html_tag(self, code, fname, max_width, image, imgcls):
    imgcss = imgcls and 'class="%s"' % imgcls or ''
    width, height = image.size
    self.body.append('<img src="%s" alt="%s" width="%s" height="%s" %s/>\n' %
        (fname, self.encode(code).strip(), width, height, imgcss))


def html_tag_with_thumbnail(self, code, fname, new_width, image, imgcls):
    width, height = image.size
    new_height = height * new_width / width 
    image.resize((new_width, new_height), Image.ANTIALIAS)
    image.filter(ImageFilter.DETAIL)
    dir, file = os.path.split(fname)
    ofname = os.path.basename(fname)
    relfn = posixpath.join(self.builder.imgpath, "thumbnail", ofname)
    outfn = os.path.join(self.builder.outdir, '_images', "thumbnail", ofname)
    ensuredir(os.path.dirname(outfn))
    image.save(outfn, "PNG")
    imgcss = imgcls and 'class="%s"' % imgcls or ''
    self.body.append('<a href="%s">' % relfn)            
    self.body.append('<img src="%s" alt="%s" width="%s" height="%s" %s/>\n' %
        (fname, self.encode(code).strip(), new_width, new_height, imgcss))
    self.body.append('</a>')


def html_visit_sequence_diagram(self, node):
    render_sdx_html(self, node, node['code'], node['options'])


def render_sdx_latex(self, node, code, options, prefix='sdedit'):
    try:
        fname, outfn = render_sdx(self, code, options, 'pdf', prefix)
    except SdeditError, exc:
        self.builder.warn('sdedit code %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\includegraphics{%s}' % fname)
    raise nodes.SkipNode


def latex_visit_sequence_diagram(self, node):
    render_sdx_latex(self, node, node['code'], node['options'])

def setup(app):
    app.add_node(sequence_diagram,
                 html=(html_visit_sequence_diagram, None),
                 latex=(latex_visit_sequence_diagram, None))
    app.add_directive('sequence-diagram', SequenceDiagram)
    app.add_config_value('sdedit_path', 'sdedit.jar', 'html')
    app.add_config_value('sdedit_java_path', 'java', 'html')
    app.add_config_value('sdedit_args', [], 'html')
    app.add_config_value('sdedit_default_options', 
                         {'maxwidth':700}, 'html')

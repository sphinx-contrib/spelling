# -*- coding: utf-8 -*-
"""
    sphinxcontrib.gnuplot
    ~~~~~~~~~~~~~~~~~~~~~

    Allow gnuplot commands be rendered as nice looking images
    

    See the README file for details.

    :author: Vadim Gubergrits <vadim.gubergrits@gmail.com>
    :license: BSD, see LICENSE for details

    Inspired by ``sphinxcontrib-aafig`` by Leandro Lucarella.
"""

import posixpath
from os import path
from subprocess import Popen,PIPE

try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.errors import SphinxError
from sphinx.util import ensuredir, relative_uri
from sphinx.util.compat import Directive



DEFAULT_FORMATS = dict(html='png', latex='pdf', text=None)



def get_hashid(text,options):
    hashkey = text.encode('utf-8') + str(options)
    hashid = sha(hashkey).hexdigest()
    return hashid


class GnuplotError(SphinxError):
    category = 'gnuplot error'


class GnuplotDirective(directives.images.Image):
    """
    Directive that builds plots using gnuplot.
    """
    has_content = True
    required_arguments = 0
    own_option_spec = dict(
        size = str,
        title = str,
        datafiles = str,

    )

    option_spec = directives.images.Image.option_spec.copy()
    option_spec.update(own_option_spec)
  
    def run(self):
        self.arguments = ['']
        gnuplot_options = dict([(k,v) for k,v in self.options.items() 
                                  if k in self.own_option_spec])

        (image_node,) = directives.images.Image.run(self)
        if isinstance(image_node, nodes.system_message):
            return [image_node]
        text = '\n'.join(self.content)
        image_node.gnuplot = dict(text=text,options=gnuplot_options)
        return [image_node]


def render_gnuplot_images(app, doctree):
    for img in doctree.traverse(nodes.image):
        if not hasattr(img, 'gnuplot'):
            continue

        text = img.gnuplot['text']
        options = img.gnuplot['options']
        try:
            fname, outfn, hashid = render_gnuplot(app, text, options)
            img['uri'] = fname
        except GnuplotError, exc:
            app.builder.warn('gnuplot error: ' + str(exc))
            img.replace_self(nodes.literal_block(text, text))
            continue


def render_gnuplot(app, text, options):
    """
    Render an ASCII art figure into the requested format output file.
    """
    format_map = DEFAULT_FORMATS.copy()
    format_map.update(app.builder.config.gnuplot_format)

    hashid = get_hashid(text,options)
    term = format_map[app.builder.format]
    if app.builder.format == 'html':
        fname = 'plot-%s.%s' % (hashid, term)
        # HTML
        imgpath = relative_uri(app.builder.env.docname,'_images')
        relfn = posixpath.join(imgpath,fname)
        outfn = path.join(app.builder.outdir, '_images', fname)
    else:
        # Non-HTML
        if app.builder.format != 'latex':
            app.builder.warn('gnuplot: the builder format %s '
                'is not officially supported.' % app.builder.format)
        fname = 'plot-%s.%s' % (hashid, term)
        relfn = fname
        outfn = path.join(app.builder.outdir, fname)

    if path.isfile(outfn):
        return relfn, outfn, hashid
    
    ensuredir(path.dirname(outfn))

    docdir = (path.dirname(app.builder.env.docname))
    try:
        plot = Popen('gnuplot -persist', shell=True, bufsize=64, stdin=PIPE)
        if docdir:
            plot.stdin.write('cd "%s"\n' % docdir)
        plot.stdin.write("set terminal %s " % (term,))
        if 'size' in options:
            plot.stdin.write("size %s\n" % options['size'])
        else:
            plot.stdin.write("\n")
        if 'title' in options:
            plot.stdin.write('set title "%s"\n' % options['title'])
        plot.stdin.write("set output '%s'\n" % (outfn,))
        plot.stdin.write("%s\n" % text)
        plot.stdin.write("\nquit\n")
        plot.stdin.flush()
    except Exception, e:
        raise GnuplotError(str(e))

    return relfn, outfn, hashid


def setup(app):
    app.add_directive('gnuplot', GnuplotDirective)
    app.connect('doctree-read', render_gnuplot_images)
    app.add_config_value('gnuplot_format', DEFAULT_FORMATS, 'html')

# -*- coding: utf-8 -*-
"""
    sphinxcontrib.aafig
    ~~~~~~~~~~~~~~~~~~~

    Allow embeded ASCII art to be rendered as nice looking images
    using the aafigure reStructuredText extension.

    See the README file for details.

    :copyright: Copyright 2009 by Leandro Lucarella <llucax@gmail.com> \
        (based on sphinxcontrib.mscgen).
    :license: BSD, see LICENSE for details.
"""

import posixpath
from os import path
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.errors import SphinxError
from sphinx.util import ensuredir
from sphinx.util.compat import Directive

import aafigure


def merge_defaults(options, config):
    # merge default options
    for (k, v) in config.aafig_default_options.items():
        if k not in options:
            options[k] = v
    return options


def get_basename(text, options, prefix='aafig'):
    options = options.copy()
    if 'format' in options:
        del options['format']
    hashkey = text.encode('utf-8') + str(options)
    id = sha(hashkey).hexdigest()
    return '%s-%s' % (prefix, id)


class AafigError(SphinxError):
    category = 'aafig error'


class AafigDirective(directives.images.Image):
    """
    Directive to insert an ASCII art figure to be rendered by aafigure.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    own_option_spec = dict(
        line_width   = float,
        background   = str,
        foreground   = str,
        fill         = str,
        aspect       = directives.nonnegative_int,
        textual      = directives.flag,
        proportional = directives.flag,
    )
    option_spec = directives.images.Image.option_spec.copy()
    option_spec.update(own_option_spec)

    def run(self):
        aafig_options = dict()
        image_attrs = dict()
        own_options_keys = self.own_option_spec.keys() + ['scale']
        for (k, v) in self.options.items():
            if k in own_options_keys:
                # convert flags to booleans
                if v is None:
                    v = True
                # convert percentage to float
                if k == 'scale' or k == 'aspec':
                    v = float(v) / 100
                aafig_options[k] = v
                del self.options[k]
        self.arguments = ['']
        (image_node,) = directives.images.Image.run(self)
        if isinstance(image_node, nodes.system_message):
            return [image_node]
        text = '\n'.join(self.content)
	image_node.aafig = dict(options = aafig_options, text = text)
        return [image_node]


def render_aafig_images(app, doctree):
    for img in doctree.traverse(nodes.image):
        if not hasattr(img, 'aafig'):
            continue

        options = img.aafig['options']
        text = img.aafig['text']
        format = app.builder.format
        merge_defaults(options, app.builder.config)
        try:
            try:
                options['format'] = app.builder.config.aafig_format[format]
            except:
                app.builder.warn('unsupported builder format "%s", please '
                        'add a custom entry in aafig_format config option '
                        'for this builder' % format)
                continue
            fname, outfn, id, extra = render_aafigure(app, text, options)
        except AafigError, exc:
            app.builder.warn('aafigure error: ' + str(exc))
            current_node.replace_self([])
            # TODO: replace with the ascii art itself
        img['uri'] = fname
        # FIXME: find some way to avoid this hack in aafigure
        if extra:
            (width, height) = [x.split('"')[1] for x in extra.split()]
            (img['width'], img['height']) = (width, height)


def render_aafigure(app, text, options):
    """
    Render an ASCII art figure into the requested format output file.
    """

    fname = get_basename(text, options)
    fname = '%s.%s' % (get_basename(text, options), options['format'])
    if hasattr(app.builder, 'imgpath'):
        # HTML
        relfn = posixpath.join(app.builder.imgpath, fname)
        outfn = path.join(app.builder.outdir, '_images', fname)
    else:
        # LaTeX
        relfn = fname
        outfn = path.join(app.builder.outdir, fname)
    metadata_fname = '%s.aafig' % outfn

    try:
        if path.isfile(outfn):
            extra = None
            if options['format'].lower() == 'svg':
                f = None
                try:
                    try:
                        f = file(metadata_fname, 'r')
                        extra = f.read()
                    except:
                        raise AafigError()
                finally:
                    if f is not None:
                        f.close()
            return relfn, outfn, id, extra
    except AafigError:
        pass

    ensuredir(path.dirname(outfn))

    try:
        (visitor, output) = aafigure.render(text, outfn, options)
	output.close()
    except aafigure.UnsupportedFormatError, e:
        raise AafigError(str(e))

    extra = None
    if options['format'].lower() == 'svg':
        extra = visitor.get_size_attrs()
        f = file(metadata_fname, 'w')
        f.write(extra)
        f.close()

    return relfn, outfn, id, extra


def setup(app):
    app.add_directive('aafig', AafigDirective)
    app.connect('doctree-read', render_aafig_images)
    app.add_config_value('aafig_format', dict(html='svg', latex='pdf'), 'html')
    app.add_config_value('aafig_default_options', dict(), 'html')


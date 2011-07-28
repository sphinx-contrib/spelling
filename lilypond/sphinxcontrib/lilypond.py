# -*- coding: utf-8 -*-
"""
    Sphinx Extension lilypond
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Allow Lilypond music notes to be included in Sphinx-generated documents
    inline and outline. 

    :copyright: Copyright ©2009 by Wei-Wei Guo.
    :license: BSD, see LICENSE for details.

    The extension is modified from mathbase.py and pngmath.py by Sphinx team. 

    Note: The extension has only very basic support for LaTeX builder.
"""

import shutil
import tempfile
import posixpath
from os import path
from subprocess import Popen, PIPE
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes, utils
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

from sphinx.errors import SphinxError
from sphinx.util import ensuredir

class LilyExtError(SphinxError):
    category = 'Lilypond extension error'

DOC_HEAD = r'''
\paper{
  indent=0\mm
  line-width=120\mm
  oddFooterMarkup=##f
  oddHeaderMarkup=##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
'''

Inline_HEAD = r'''
\markup \abs-fontsize #%s { 
'''

# Inline_HEAD = r'''
# \markup \abs-fontsize #%s { \musicglyph 
# '''

Inline_BACK = r'''
}
'''

Directive_HEAD = r"""
\new Score \with {
  fontSize = #%s
  \override StaffSymbol #'staff-space = #(magstep %s)
}{ <<
"""

Directive_BACK = r"""
>> }
"""

class lily(nodes.Inline, nodes.TextElement):
    pass

class displaylily(nodes.Part, nodes.Element):
    pass

def lily_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    music = utils.unescape(text, restore_backslashes=True)
    return [lily(music=music)], []

class LilyDirective(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'nowrap': directives.flag,
    }

    def run(self):
        music = '\n'.join(self.content)
        node = displaylily()
        node['music'] = music
        node['docname'] = self.state.document.settings.env.docname
        node['nowrap'] = 'nowrap' in self.options
        return [node]

def render_lily(self, lily):
    """
    Render the Lilypond music expression *lily* using lilypond.
    """
    shasum = "%s.png" % sha(lily.encode('utf-8')).hexdigest()
    relfn = posixpath.join(self.builder.imgpath, 'lily', shasum)
    outfn = path.join(self.builder.outdir, '_images', 'lily', shasum)
    if path.isfile(outfn):
        return relfn

    if hasattr(self.builder, '_lilypng_warned'):
        return None, None

    music = DOC_HEAD + self.builder.config.pnglily_preamble + lily
    if isinstance(music, unicode):
        music = music.encode('utf-8')

    # use only one tempdir per build -- the use of a directory is cleaner
    # than using temporary files, since we can clean up everything at once
    # just removing the whole directory (see cleanup_tempdir_lily)
    if not hasattr(self.builder, '_lilypng_tempdir'):
        tempdir = self.builder._lilypng_tempdir = tempfile.mkdtemp()
    else:
        tempdir = self.builder._lilypng_tempdir

    tf = open(path.join(tempdir, 'music.ly'), 'w')
    tf.write(music)
    tf.close()

    ensuredir(path.dirname(outfn))
    # use some standard lilypond arguments
    lilypond_args = [self.builder.config.pnglily_lilypond]
    #lilypond_args += ['-o', tempdir, '--png']
    lilypond_args += ['-dbackend=eps', '-dno-gs-load-fonts', '-dinclude-eps-fonts',
                      '-o', tempdir, '--png']
    # add custom ones from config value
    lilypond_args.extend(self.builder.config.pnglily_lilypond_args)

    # last, the input file name
    lilypond_args.append(path.join(tempdir, 'music.ly'))
    try:
        p = Popen(lilypond_args, stdout=PIPE, stderr=PIPE)
    except OSError, err:
        if err.errno != 2:   # No such file or directory
            raise
        self.builder.warn('lilypond command %r cannot be run (needed for music '
                          'display), check the pnglily_lilypond setting' %
                          self.builder.config.pnglily_lilypond)
        self.builder._lilypng_warned = True
        return None, None
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise LilyExtError(u'lilypond exited with error:\n[stderr]\n%s\n'
                           '[stdout]\n%s' % (stderr.decode('utf-8'), stdout.decode('utf-8')))

    shutil.copyfile(path.join(tempdir, 'music.png'), outfn)
    #Popen(['mogrify', '-trim', outfn], stdout=PIPE, stderr=PIPE)

    return relfn

def cleanup_tempdir_lily(app, exc):
    if exc:
        return
    if not hasattr(app.builder, '_lilypng_tempdir'):
        return
    try:
        shutil.rmtree(app.builder._lilypng_tempdir)
    except Exception:
        pass

def latex_visit_lily(self, node):
    self.body.append('{' + node['music'] + '}')
    raise nodes.SkipNode

def latex_visit_displaylily(self, node):
    self.body.append(node['music'])
    raise nodes.SkipNode

def html_visit_lily(self, node):
    music = Inline_HEAD % self.builder.config.pnglily_fontsize[0]
    music += node['music'] + Inline_BACK
    #music += '#"' + node['music'] + '"' + Inline_BACK
    try:
        fname = render_lily(self, music)
    except LilyExtError, exc:
        sm = nodes.system_message(unicode(exc), type='WARNING', level=2,
                                  backrefs=[], source=node['music'])
        sm.walkabout(self)
        self.builder.warn('display lilypond %r: ' % node['music'] + unicode(exc))
        raise nodes.SkipNode
    if fname is None:
        # something failed -- use text-only as a bad substitute
        self.body.append('<span class="lily">%s</span>' %
                         self.encode(node['music']).strip())
    else:
        self.body.append(
            '<img class="lily" src="%s" alt="%s" align="absbottom"/>' %
            (fname, self.encode(node['music']).strip()))
    raise nodes.SkipNode


def html_visit_displaylily(self, node):
    if node['nowrap']:
        music = node['music']
    else:
        music = Directive_HEAD % (self.builder.config.pnglily_fontsize[1],
                                  self.builder.config.pnglily_fontsize[1])
        music += node['music'] + Directive_BACK
    try:
        fname = render_lily(self, music)
    except LilyExtError, exc:
        sm = nodes.system_message(unicode(exc), type='WARNING', level=2,
                                  backrefs=[], source=node['music'])
        sm.walkabout(self)
        self.builder.warn('inline lilypond %r: ' % node['music'] + unicode(exc))
        raise nodes.SkipNode
    self.body.append(self.starttag(node, 'div', CLASS='lily'))
    self.body.append('<p>')
    if fname is None:
        # something failed -- use text-only as a bad substitute
        self.body.append('<span class="lily">%s</span>' %
                         self.encode(node['music']).strip())
    else:
        self.body.append('<img src="%s" alt="%s" />\n</div>' %
                         (fname, self.encode(node['music']).strip()))
    self.body.append('</p>')
    raise nodes.SkipNode


def setup(app):
    app.add_node(lily,
                 latex=(latex_visit_lily, None),
                 html=(html_visit_lily, None))
    app.add_node(displaylily,
                 latex=(latex_visit_displaylily, None),
                 html=(html_visit_displaylily, None))
    app.add_role('lily', lily_role)
    app.add_directive('lily', LilyDirective)
    app.add_config_value('pnglily_preamble', '', False)
    app.add_config_value('pnglily_fontsize', ['10', '-3'], False)
    app.add_config_value('pnglily_lilypond', 'lilypond', False)
    app.add_config_value('pnglily_lilypond_args', [], False)
    app.connect('build-finished', cleanup_tempdir_lily)

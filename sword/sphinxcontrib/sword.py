# -*- coding: utf-8 -*-
"""
    Sphinx Extension Sword
    ~~~~~~~~~~~~~~~~~~~~~~

    Allow Bible verses to be included in Sphinx-generated documents inline.

    :copyright: Copyright ©2009 by Wei-Wei Guo.
    :license: BSD, see LICENSE for details.

    Note: The extension has no support for LaTeX builder right now.
"""

from subprocess import Popen, PIPE

from docutils import nodes, utils

from sphinx.errors import SphinxError

class SwordExtError(SphinxError):
    category = 'Sword extension error'

class sword(nodes.Inline, nodes.TextElement):
    pass

class bible(nodes.Inline, nodes.TextElement):
    pass

def sword_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    skey = utils.unescape(text, restore_backslashes=True)
    return [sword(skey=skey)], []

def bible_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    skey = utils.unescape(text, restore_backslashes=True)
    return [bible(skey=skey)], []

def render_sword(self, skey):
    """
    Render the Bible verse by Sword.
    """
    sverse = {}
    snumber = []
    bkey = []
    shead = []

    # use some standard sword arguments
    sword_book = self.builder.config.sword_args[0]
    sword_command = ['diatheke', '-b', sword_book, '-k', skey]

    def verse_split (verse, sverse, shead):
        verselist = verse.split(':',2)
        sverse[verselist[1]] = verselist[2].strip()
        shead.append(verselist[0].strip())
        return sverse, shead

    try:
        p = Popen(sword_command, stdout=PIPE, stderr=PIPE)
    except OSError, err:
        self.builder.warn('sword command %r cannot be run.')

    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise SwordExtError('sword exited with error:\n[stderr]\n%s\n'
                           '[stdout]\n%s' % (stderr, stdout))

    verses = stdout.split('\n')
    [verse_split(x, sverse, shead) for x in verses if x.find(':')>0]
    [snumber.append(int(x)) for x in sverse.keys()]
    snumber.sort()
    [bkey.append(str(x)) for x in snumber]

    return sverse, shead, bkey

def latex_visit_sword(self, node):
    sverse, shead, bkey = render_sword(self, node['skey'])

    if len(set(shead)) != 1:
        raise SwordExtError('Verses not in the same chapter.')
    else:
        bhead = '[' + shead[0] + ':' + node['skey'].split(':')[1] + ']'

    self.body.append(bhead)
    raise nodes.SkipNode

def latex_visit_bible(self, node):
    sverse, shead, bkey = render_sword(self, node['skey'])

    if len(set(shead)) != 1:
        raise SwordExtError('Verses not in the same chapter.')
    else:
        bhead = '[' + shead[0] + ':' + node['skey'].split(':')[1] + ']'

    self.body.append(bhead)
    raise nodes.SkipNode

def html_visit_sword(self, node):
    try:
        self.sword_index += 1
    except AttributeError:
        self.sword_index = 0

    sverse, shead, bkey = render_sword(self, node['skey'])

    if len(set(shead)) != 1:
        raise SwordExtError('Verses not in the same chapter.')
    else:
        bhead = '[' + shead[0] + ':' + node['skey'].split(':')[1] + ']'

    bverse = []

    if self.builder.config.sword_args[1] == 'folder':
        for x in bkey:
            bverse.append('<strong class="sword" style="color:gray;vertical-align:super">%s</strong>' %
                          x + sverse.get(x).decode('utf-8'))
    elif self.builder.config.sword_args[1] == 'tooltip':
        for x in bkey:
            bverse.append('[%s]%s' % (x, sverse.get(x).decode('utf-8')))
    else:
        pass             

    if bkey == []:
        self.body.append('<span class="sword">%s</span>' %
                         '[' + node['skey'] + ']')
    else:
        if self.builder.config.sword_args[1] == 'folder':
            self.body.append('<span id="%s" class="open-fold">' % ('fold' + str(self.sword_index)))
            self.body.append('''<a class="toggle-open" href="javascript:toggleFold('%s')">%s</a>''' %
                             (('fold' + str(self.sword_index)), bhead))
            self.body.append('''<a class="toggle-closed" href="javascript:toggleFold('%s')">%s</a>''' %
                             (('fold' + str(self.sword_index)), bhead))
            self.body.append('<span class="Folded">' + ''.join(bverse) + '</span></span>')
        elif self.builder.config.sword_args[1] == 'tooltip':
            self.body.append('<a title="%s">%s</a>' % (''.join(bverse), bhead))
        else:
            raise SwordExtError('Style "%s" is not accepted. Check your sword_args.' %
                                self.builder.config.sword_args[1])

    raise nodes.SkipNode

def html_visit_bible(self, node):
    sverse, shead, bkey = render_sword(self, node['skey'])

    if len(set(shead)) != 1:
        raise SwordExtError('Verses not in the same chapter.')
    else:
        bhead = '[' + shead[0] + ':' + node['skey'].split(':')[1] + ']'

    if bkey == []:
        # something failed -- use text-only as a bad substitute
        self.body.append('<span class="sword">%s</span>' %
                         '[' + node['skey'] + ']')
    else:
        for x in bkey:
            self.body.append(
                '<strong class="sword" style="color:gray;vertical-align:super">%s</strong>' %
                x + '<span class="bible" style="font-family:%s">%s</span>' %
                (self.builder.config.sword_args[2], sverse.get(x).decode('utf-8')))
        self.body.append(bhead)

    raise nodes.SkipNode

def setup(app):
    app.add_node(sword,
                 latex=(latex_visit_sword, None),
                 html=(html_visit_sword, None))
    app.add_node(bible,
                 latex=(latex_visit_bible, None),
                 html=(html_visit_bible, None))
    app.add_role('sword', sword_role)
    app.add_role('bible', bible_role)
    app.add_config_value('sword_args', [], False)
    app.add_javascript('sword_folder.js')

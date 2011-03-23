# -*- coding: utf-8 -*-
import sys
from sphinx.errors import SphinxWarning
from sphinx.util.compat import Directive
from docutils.parsers.rst import directives
from docutils import nodes

import sadisplay


class SaNode(nodes.General, nodes.Element):
    pass


class SadisplayDirective(Directive):
    """Directive to display SQLAlchemy models

    Example::

        .. sadisplay::
           :module: myapp.model

    """
    has_content = False
    option_spec = {
        'alt': directives.unchanged,
        'render': directives.unchanged,
        'module': directives.unchanged,
        'include': directives.unchanged,
        'exclude': directives.unchanged,
    }

    def run(self):
        node = SaNode()
        #node['uml'] = '\n'.join(self.content)
        node['alt'] = self.options.get('alt', None)
        node['render'] = self.options.get('render', u'plantuml')
        node['module'] = self.options.get('module', u'')

        def tolist(val):
            if val:
                return map(lambda i: i.strip(), val.split(','))
            return []

        node['include'] = tolist(self.options.get('include', None))
        node['exclude'] = tolist(self.options.get('exclude', None))

        if node['include'] and node['exclude']:
            raise SphinxWarning(u'sadisplay directive error - \
                    both defined :include: and :exclude:')

        return [node]


def render(self, node):

    __import__(node['module'], globals(), locals(), [], -1)
    module = sys.modules[node['module']]

    all_names = [getattr(module, attr) for attr in dir(module)]

    names = []

    if node['exclude']:
        for i in all_names:
            try:
                if i.__name__ not in node['exclude']:
                    names.append(i)
            except AttributeError:
                pass

    elif node['include']:
        for i in all_names:
            try:
                if i.__name__ in node['include']:
                    names.append(i)
            except AttributeError:
                pass

    else:
        names = all_names

    desc = sadisplay.describe(names)

    if node['render'] == u'plantuml':

        from sphinxcontrib import plantuml
        plantuml_node = plantuml.plantuml()
        plantuml_node['uml'] = sadisplay.plantuml(desc)
        plantuml_node['alt'] = node['alt']
        return plantuml.render_plantuml(self, plantuml_node)

    elif node['render'] == u'graphviz':
        pass


def html_visit(self, node):
    try:
        refname = render(self, node)
    except Exception, err:
        self.builder.warn(str(err))
        raise nodes.SkipNode
    self.body.append(self.starttag(node, 'p', CLASS='sadisplay'))
    self.body.append('<img src="%s" alt="%s" />\n'
                     % (self.encode(refname),
                        self.encode(node['alt'] or node['module'])))
    self.body.append('</p>\n')
    raise nodes.SkipNode


def latex_visit(self, node):
    try:
        refname = render(self, node)
    except Exception, err:
        self.builder.warn(str(err))
        raise nodes.SkipNode
    self.body.append('\\includegraphics{%s}' % self.encode(refname))
    raise nodes.SkipNode


def setup(app):
    app.add_node(SaNode,
                 html=(html_visit, None),
                 latex=(latex_visit, None))
    app.add_directive('sadisplay', SadisplayDirective)

# -*- coding: utf-8 -*-
"""
    sphinx.writers.context
    ~~~~~~~~~~~~~~~~~~~~~~

    Custom docutils writer for ConTeXt.

    :copyright: Copyright ©2009 by Wei-Wei Guo.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes, writers

from sphinx import addnodes
from sphinx.util.texescape import tex_escape_map
from sphinx.environment import BuildEnvironment

class ConTeXtWriter(writers.Writer):
    supported = ('context',)
    settings_spec = ('No options yet.', '', ())
    settings_defaults = {}

    output = None

    def __init__(self, builder):
        writers.Writer.__init__(self)
        self.builder = builder

    def translate(self):
        visitor = ConTeXtTranslator(self.document, self.builder)
        self.document.walkabout(visitor)
        self.output = visitor.body


class ConTeXtTranslator(nodes.NodeVisitor):

    def __init__(self, document, builder):
        nodes.NodeVisitor.__init__(self, document)

        self.builder = builder
        self.body = []

        self.sectionlevel = 0

    def visit_document(self, node):
        doclist = node['doclist']
        if len(doclist) == 1:
            self.body.append('\\startproject %s\n\n\\environment %s\n\n' %
                             (self.builder.document_data[1], self.builder.document_data[4]))
        elif len(doclist) == 2:
            if doclist[1] == 'index':
                self.body.append('\\startproduct %s\n\n\\project %s\n\n' %
                                 (doclist[0], self.builder.document_data[1]))
                self.sectionlevel = 1
            else:
                self.body.append('\\startcomponent %s\n\n\\project %s\n\\product %s\n\n' %
                                 (doclist[1], self.builder.document_data[1], doclist[0]))
                self.sectionlevel = 2
        else:
            raise SwordExtError('Only two directory levels is accepted.')
    def depart_document(self, node):
        doclist = node['doclist']
        if len(doclist) == 1:
            self.body.append('\\stopproject')
        elif len(doclist) == 2:
            if doclist[1] == 'index':
                self.body.append('\\stopproduct')
            else:
                self.body.append('\\stopcomponent')
        else:
            pass

    def visit_section(self, node):
        self.sectionlevel += 1
    def depart_section(self, node):
        self.sectionlevel -= 1

    def visit_title(self, node):
        text = node.astext()
        if self.sectionlevel == 1:
            self.body.append('\\booktitle{%s}\n\n' % text)
        elif self.sectionlevel == 2:
            self.body.append('\\part{%s}\n\n' % text)
        elif self.sectionlevel == 3:
            self.body.append('\\chapter{%s}\n\n' % text)
        elif self.sectionlevel == 4:
            self.body.append('\\section{%s}\n\n' % text)
        elif self.sectionlevel == 5:
            self.body.append('\\subsection{%s}\n\n' % text)
        elif self.sectionlevel == 6:
            self.body.append('\\subsubsection{%s}\n\n' % text)
        else:
            raise SwordExtError('Only five section levels is accepted.')
    def depart_title(self, node):
        pass

    def visit_Text(self, node):
        pass
    def depart_Text(self, node):
        pass

    def visit_paragraph(self, node):
        text = node.astext()
        self.body.append(text)
    def depart_paragraph(self, node):
        self.body.append('\n\n')

    def visit_toctree(self, node):
        entry = [x[1].split('/') for x in node['entries']]
        doclist = node.document['doclist']
        if len(doclist) == 1:
            [self.body.append('\\product %s\n' % (y[0] + '/' + y[0])) for y in entry]
        elif len(doclist) == 2:
            if doclist[1] == 'index':
                [self.body.append('\\component %s\n' % y[1]) for y in entry]
        else:
            raise node.SkipNode
    def depart_toctree(self, node):
        self.body.append('\n')

    def visit_bullet_list(self, node):
        self.body.append('\n\\startitemize\n')
    def depart_bullet_list(self, node):
        self.body.append('\\stopitemize')

    def visit_list_item(self, node):
        self.body.append('\\item ')
    def depart_list_item(self, node):
        self.body.append('\n')

    # # def visit_environ(self, node):
    # #     self.body.insert(0, '\\localenvironment')

    # def visit_reference(self, node):
    #     pass
    # def depart_reference(self, node):
    #     pass
    
    def unknown_visit(self, node):
        raise NotImplementedError('Unknown node: ' + node.__class__.__name__)

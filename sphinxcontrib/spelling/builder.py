# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Spelling checker extension for Sphinx.
"""

import codecs
import collections
import os

import docutils.nodes
from sphinx.builders import Builder
from sphinx.util.console import darkgreen, red

from enchant.tokenize import EmailFilter, WikiWordFilter

import six

from . import checker
from . import filters

# TODO - Words with multiple uppercase letters treated as classes and ignored


class SpellingBuilder(Builder):
    """
    Spell checks a document
    """
    name = 'spelling'

    def init(self):
        self.docnames = []
        self.document_data = []

        # Initialize the per-document filters
        if not hasattr(self.env, 'spelling_document_filters'):
            self.env.spelling_document_filters = collections.defaultdict(list)

        # Initialize the global filters
        f = [
            filters.ContractionFilter,
            EmailFilter,
        ]
        if self.config.spelling_ignore_wiki_words:
            f.append(WikiWordFilter)
        if self.config.spelling_ignore_acronyms:
            f.append(filters.AcronymFilter)
        if self.config.spelling_ignore_pypi_package_names:
            self.info('Adding package names from PyPI to local dictionary...')
            f.append(filters.PyPIFilterFactory())
        if self.config.spelling_ignore_python_builtins:
            f.append(filters.PythonBuiltinsFilter)
        if self.config.spelling_ignore_importable_modules:
            f.append(filters.ImportableModuleFilter)
        f.extend(self.config.spelling_filters)

        project_words = os.path.join(self.srcdir,
                                     self.config.spelling_word_list_filename)
        self.checker = checker.SpellingChecker(
            lang=self.config.spelling_lang,
            suggest=self.config.spelling_show_suggestions,
            word_list_filename=project_words,
            filters=f,
        )
        self.output_filename = os.path.join(self.outdir, 'output.txt')
        if six.PY2:
            self.output = codecs.open(self.output_filename,
                                      'w',
                                      encoding='UTF-8')
        else:
            self.output = open(self.output_filename, 'w', encoding='UTF-8')

    def get_outdated_docs(self):
        return 'all documents'

    def prepare_writing(self, docnames):
        return

    def get_target_uri(self, docname, typ=None):
        return ''

    def format_suggestions(self, suggestions):
        if not self.config.spelling_show_suggestions or not suggestions:
            return u''
        return u'[' + u', '.join(u'"%s"' % s for s in suggestions) + u']'

    TEXT_NODES = set([
        'block_quote',
        'paragraph',
        'list_item',
        'term',
        'definition_list_item',
        'title',
    ])

    def write_doc(self, docname, doctree):
        self.checker.push_filters(self.env.spelling_document_filters[docname])

        for node in doctree.traverse(docutils.nodes.Text):
            if (node.tagname == '#text'
                    and node.parent
                    and node.parent.tagname in self.TEXT_NODES):

                # Figure out the line number for this node by climbing the
                # tree until we find a node that has a line number.
                lineno = None
                parent = node
                seen = set()
                while lineno is None:
                    #self.info('looking for line number on %r' % node)
                    seen.add(parent)
                    parent = node.parent
                    if parent is None or parent in seen:
                        break
                    lineno = parent.line

                # Check the text of the node.
                for word, suggestions in self.checker.check(node.astext()):
                    msg_parts = [docname + '.rst']
                    if lineno:
                        msg_parts.append(darkgreen(str(lineno)))
                    msg_parts.append(red(word))
                    msg_parts.append(self.format_suggestions(suggestions))
                    msg = ':'.join(msg_parts)
                    self.info(msg)
                    self.output.write(u"%s:%s: (%s) %s\n" % (
                        self.env.doc2path(docname, None),
                        lineno, word,
                        self.format_suggestions(suggestions),
                    ))

                    # We found at least one bad spelling, so set the status
                    # code for the app to a value that indicates an error.
                    self.app.statuscode = 1

        self.checker.pop_filters()
        return

    def finish(self):
        self.output.close()
        self.info('Spelling checker messages written to %s' %
                  self.output_filename)
        return

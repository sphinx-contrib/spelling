#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Spelling checker extension for Sphinx.
"""

import codecs
import imp
import itertools
import os
import re
import textwrap

#from docutils import core
from docutils.frontend import OptionParser
from docutils.io import StringOutput
import docutils.nodes
from docutils.nodes import GenericNodeVisitor
from docutils.writers import Writer
from sphinx.builders import Builder
from sphinx.util.console import bold, darkgreen
from sphinx.util.console import purple, red, darkgreen, darkgray
from sphinx.util.nodes import inline_all_toctrees

import enchant
from enchant.tokenize import get_tokenizer

# TODO - Directive (or comment syntax?) to allow words to be ignored in a document
# TODO - Words with multiple uppercase letters treated as classes and ignored

class SpellingChecker(object):
    """Checks the spelling of blocks of text.

    Uses options defined in the sphinx configuration file to control
    the checking and filtering behavior.
    """
    
    def __init__(self, lang, suggest, word_list_filename):
        # TODO - filters
        self.dictionary = enchant.DictWithPWL(lang, word_list_filename)
        self.tokenizer = get_tokenizer(lang)
        self.suggest = suggest
        
    _class_name_pattern = re.compile(r'[A-Z]+[a-z0-9]+[A-Z]+[a-z0-9]+')
    _spelling_word_pattern = re.compile(r'\w+', re.UNICODE|re.MULTILINE|re.DOTALL)
    def check(self, text):
        """Generator function that yields bad words and suggested alternate spellings.
        """
        for word, pos in self.tokenizer(text):
            correct = self.dictionary.check(word)
            if correct:
                continue

            # TODO - filter to ignore acronyms
#             if word.upper() == word:
#                 # assume acronyms are right
#                 continue
#             if word.rstrip('s').upper() == word.rstrip('s'):
#                 # plural acronyms, too
#                 continue

            # TODO - filter to ignore python builtins
#             if word in __builtins__:
#                 # python built-in
#                 continue

            # TODO - filter to ignore "code-like" patterns, maybe via an option defining regex?
#             if '_' in word:
#                 # probably something from code
#                 continue

            # TODO - option to ignore importable modules
#             try:
#                 imp.find_module(word)
#             except ImportError:
#                 pass
#             else:
#                 # importable module name
#                 try:
#                     SPELLER.addtoSession(word)
#                 except aspell.AspellSpellerError:
#                     pass
#                 continue

            # TODO - option to include suggestions
            yield word, self.dictionary.suggest(word) if self.suggest else []

        return

        
TEXT_NODES = set([ 'block_quote',
                   'paragraph',
                   'list_item',
                   'term',
                   'definition_list_item',
                   ])


class SpellingBuilder(Builder):
    """
    Spell checks a document
    """
    name = 'spelling'

    def init(self):
        self.docnames = []
        self.document_data = []

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

    def write_doc(self, docname, doctree):
        word_list_filename = os.path.join(self.srcdir, self.config.spelling_word_list_filename)
        checker = SpellingChecker(lang=self.config.spelling_lang,
                                  suggest=self.config.spelling_show_suggestions,
                                  word_list_filename=word_list_filename,
                                  )
        
        for node in doctree.traverse(docutils.nodes.Text):
            if node.tagname == '#text' and  node.parent.tagname in TEXT_NODES:

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
                filename = self.env.doc2path(docname, base=None)

                # Check the text of the node.
                for word, suggestions in checker.check(node.astext()):
                    msg_parts = []
                    if lineno:
                        msg_parts.append(darkgreen('(line %3d)' % lineno))
                    msg_parts.append(red(word))
                    msg_parts.append(self.format_suggestions(suggestions))
                    msg = ' '.join(msg_parts)
                    self.info(msg)
                    self.write_entry(docname, lineno, word, suggestions)

                    # We found at least one bad spelling, so set the status
                    # code for the app to a value that indicates an error.
                    self.app.statuscode = 1
        return

    def write_entry(self, docname, lineno, word, suggestions):
        output = codecs.open(os.path.join(self.outdir, 'output.txt'), 'a', encoding='UTF-8')
        try:
            output.write(u"%s:%s: [%s] %s\n" % (self.env.doc2path(docname, None),
                                                lineno, word,
                                                self.format_suggestions(suggestions),
                                                )
                         )
        finally:
            output.close()
            
    def finish(self):
        output_filename = os.path.join(self.outdir, 'output.txt')
        self.info('Spelling checker messages written to %s' % output_filename)
        return

def setup(app):
    app.info('Initializing Spelling Checker')
    app.add_builder(SpellingBuilder)
    app.add_config_value('spelling_show_suggestions', False, 'env')
    app.add_config_value('spelling_lang', 'en_US', 'env')
    app.add_config_value('spelling_word_list_filename', 'spelling_wordlist.txt', 'env')
    return

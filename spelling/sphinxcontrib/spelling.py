#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Spelling checker extension for Sphinx.
"""

from docutils.nodes import GenericNodeVisitor
#from docutils import core
from docutils.writers import Writer
from sphinx.builders import Builder
from sphinx.util.console import bold, darkgreen
from docutils.frontend import OptionParser
from sphinx.util.nodes import inline_all_toctrees
from docutils.io import StringOutput

import itertools
import re
import textwrap
import imp

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

class Section(object):
    
    def __init__(self, spelling_checker):
        self.title = ''
        self.spelling_checker = spelling_checker
        self.errors = []
        self.subsections = []
        
    def get_text_lines(self):
        lines = self.errors[:]

        for subsection in self.subsections:
            lines.extend(' ' + line
                         for line in subsection.get_text_lines()
                         )

        if lines:
            lines.insert(0, self.title)
            lines.insert(0, '')
        return lines
    
    def add_subsection(self, subsection):
        self.subsections.append(subsection)
        return
    
    def set_title(self, title):
        self.title = title
        self.check_spelling(title)
        
    def astext(self):
        lines = itertools.chain(*tuple(section.get_text_lines()
                                       for section in self.subsections
                                       )
                                 )
        # May want this formatting when suggestions are added
        real_lines = []
        for line in lines:
            initial_indent = line[:len(line)-len(line.lstrip())]
            if line.lstrip().startswith('-'): # error line
                subsequent_indent = initial_indent + '  '
            else:
                subsequent_indent = initial_indent
            line = textwrap.fill(line.lstrip(), width=70,
                                 initial_indent=initial_indent,
                                 subsequent_indent=subsequent_indent,
                                 )
            real_lines.append(line)
        return '\n'.join(real_lines)

    def add_text(self, text):
        self.check_spelling(text)
    
    def check_spelling(self, text):
        for word, suggestions in self.spelling_checker.check(text):
            msg = '- "%s"' % word
            if suggestions:
                msg = '%s: %s' % (msg, ', '.join(suggestions))
            self.errors.append(msg)
        return
        
TEXT_NODES = set([ 'block_quote', 'paragraph',
                   'list_item', 'term', 'definition_list_item', ])
    

class SpellingVisitor(GenericNodeVisitor):
    """A Visitor class; see the docutils for more details.
    """
    def __init__(self, checker, *args, **kw):
        GenericNodeVisitor.__init__(self, *args, **kw)
        self.spelling_checker = checker
        self.sections = [ Section(self.spelling_checker) ]

    def visit_title(self, node):
        # Set the title for the current section.
        if not self.sections[-1].title:
            self.sections[-1].set_title(node.astext())

    def visit_section(self, node):
        # Start a new section
        new_section = Section(self.spelling_checker)
        self.sections[-1].add_subsection(new_section)
        self.sections.append(new_section)
        
    def depart_section(self, node):
        # Pop the section stack
        self.sections.pop()

    def visit_Text(self, node):
        if node.parent.tagname in TEXT_NODES:
            self.sections[-1].add_text(node.astext())

    def default_visit(self, node): pass
    def default_departure(self, node): pass

    # Ignore inline literal text
    def visit_literal(self, node): pass
    def depart_literal(self, node): pass
    def visit_emphasis(self, node): pass
    def depart_emphasis(self, node): pass

    # Ignore comment blocks
    def visit_comment(self, node): pass
    def depart_comment(self, node): pass

    # Ignore literal blocks
    def visit_literal_block(self, node): pass

    def astext(self):
        body = '\n'.join(section.astext()
                         for section in self.sections
                         )
        return body


class SpellingWriter(Writer):
    """Boilerplate attaching our Visitor to a docutils document."""
    def __init__(self, checker, *args, **kwds):
        self.spelling_checker = checker
        Writer.__init__(self, *args, **kwds)
    def translate(self):
        visitor = SpellingVisitor(self.spelling_checker, self.document)
        self.document.walkabout(visitor)
        self.output = '\n' + visitor.astext() + '\n'


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

    def write(self, *ignored):
        self.output = []

        checker = SpellingChecker(lang=self.config.spelling_lang, #'en_US',
                                  suggest=self.config.spelling_show_suggestions,
                                  word_list_filename=self.config.spelling_word_list_filename,
                                  )
        
        master = self.config.master_doc
        docwriter = SpellingWriter(checker=checker)
        docsettings = OptionParser(
            defaults=self.env.settings,
            components=(docwriter,)).get_default_values()
            
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set(), master, tree, darkgreen)
        tree['docname'] = master

        destination = StringOutput(encoding='utf-8')
        text = docwriter.write(tree, destination).strip()
        if text:
            self.output.append(text)

        return
    
    def finish(self):
        # TODO - Use color output?
        print
        print
        for text in self.output:
            print text
            print
        self.info('done')

def setup(app):
    print 'Initializing Spelling Checker'
    app.add_builder(SpellingBuilder)
    app.add_config_value('spelling_show_suggestions', False, 'env')
    app.add_config_value('spelling_lang', 'en_US', 'env')
    app.add_config_value('spelling_word_list_filename', 'spelling_wordlist.txt', 'env')
    return

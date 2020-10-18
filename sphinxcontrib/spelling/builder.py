#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Spelling checker extension for Sphinx.
"""

import collections
import importlib
import os
import tempfile

import docutils.nodes
from sphinx.builders import Builder
from sphinx.util import logging
from sphinx.util.console import darkgreen, red
from sphinx.util.matching import Matcher
from sphinx.util.osutil import ensuredir

try:
    from enchant.tokenize import EmailFilter, WikiWordFilter
except ImportError as imp_exc:
    enchant_import_error = imp_exc
else:
    enchant_import_error = None

from . import checker, filters

logger = logging.getLogger(__name__)

# TODO - Words with multiple uppercase letters treated as classes and ignored


class SpellingBuilder(Builder):
    """
    Spell checks a document
    """
    name = 'spelling'

    def init(self):
        if enchant_import_error is not None:
            raise RuntimeError(
                'Cannot initialize spelling builder '
                'without PyEnchant installed') from enchant_import_error
        self.misspelling_count = 0

        self.env.settings["smart_quotes"] = False
        # Initialize the per-document filters
        if not hasattr(self.env, 'spelling_document_words'):
            self.env.spelling_document_words = collections.defaultdict(list)

        # Initialize the global filters
        f = [
            filters.ContractionFilter,
            EmailFilter,
        ]
        if self.config.spelling_ignore_wiki_words:
            logger.info('Ignoring wiki words')
            f.append(WikiWordFilter)
        if self.config.spelling_ignore_acronyms:
            logger.info('Ignoring acronyms')
            f.append(filters.AcronymFilter)
        if self.config.spelling_ignore_pypi_package_names:
            logger.info('Adding package names from PyPI to local dictionary…')
            f.append(filters.PyPIFilterFactory())
        if self.config.spelling_ignore_python_builtins:
            logger.info('Ignoring Python builtins')
            f.append(filters.PythonBuiltinsFilter)
        if self.config.spelling_ignore_importable_modules:
            logger.info('Ignoring importable module names')
            f.append(filters.ImportableModuleFilter)
        if self.config.spelling_ignore_contributor_names:
            logger.info('Ignoring contributor names')
            f.append(filters.ContributorFilter)
        f.extend(self._load_filter_classes(self.config.spelling_filters))

        if not os.path.isdir(self.outdir):
            os.mkdir(self.outdir)

        word_list = self.get_wordlist_filename()
        logger.info(f'Looking for custom word list in {word_list}')

        self.checker = checker.SpellingChecker(
            lang=self.config.spelling_lang,
            tokenizer_lang=self.config.tokenizer_lang,
            suggest=self.config.spelling_show_suggestions,
            word_list_filename=word_list,
            filters=f,
            context_line=self.config.spelling_show_whole_line,
        )

    def _load_filter_classes(self, filters):
        # Filters may be expressed in the configuration file using
        # names, so look through them and import the referenced class
        # and use that in the checker.
        for filter in filters:
            if not isinstance(filter, str):
                yield filter
                continue
            module_name, _, class_name = filter.rpartition('.')
            mod = importlib.import_module(module_name)
            yield getattr(mod, class_name)

    def get_wordlist_filename(self):
        word_list = self.config.spelling_word_list_filename
        if word_list is None:
            word_list = 'spelling_wordlist.txt'

        if not isinstance(word_list, list):
            filename = os.path.join(self.srcdir, word_list)
            return filename

        # In case the user has multiple word lists, we combine them
        # into one large list that we pass on to the checker.
        return self._build_combined_wordlist()

    def _build_combined_wordlist(self):
        # If we have a list, the combined list is the first list plus all words
        # from the other lists. Otherwise, word_list is assumed to just be a
        # string.
        temp_dir = tempfile.mkdtemp()
        combined_word_list = os.path.join(temp_dir,
                                          'spelling_wordlist.txt')

        word_list = self.config.spelling_word_list_filename

        with open(combined_word_list, 'w', encoding='UTF-8') as outfile:
            for word_file in word_list:
                # Paths are relative
                long_word_file = os.path.join(self.srcdir, word_file)
                logger.info('Adding contents of {} to custom word list'.format(
                    long_word_file))
                with open(long_word_file, encoding='UTF-8') as infile:
                    infile_contents = infile.readlines()
                outfile.writelines(infile_contents)

                # Check for newline, and add one if not present
                if infile and not infile_contents[-1].endswith('\n'):
                    outfile.write('\n')

        return combined_word_list

    def get_outdated_docs(self):
        return 'all documents'

    def prepare_writing(self, docnames):
        return

    def get_target_uri(self, docname, typ=None):
        return ''

    def format_suggestions(self, suggestions):
        if not self.config.spelling_show_suggestions or not suggestions:
            return ''
        return '[' + ', '.join('"%s"' % s for s in suggestions) + ']'

    TEXT_NODES = {
        'block_quote',
        'paragraph',
        'list_item',
        'term',
        'definition_list_item',
        'title',
    }

    def write_doc(self, docname, doctree):
        lines = list(self._find_misspellings(docname, doctree))
        self.misspelling_count += len(lines)
        if lines:
            output_filename = os.path.join(self.outdir, docname + '.spelling')
            logger.info('Writing %s', output_filename)
            ensuredir(os.path.dirname(output_filename))
            with open(output_filename, 'w', encoding='UTF-8') as output:
                output.writelines(lines)

    def _find_misspellings(self, docname, doctree):

        excluded = Matcher(self.config.spelling_exclude_patterns)
        if excluded(self.env.doc2path(docname, None)):
            return
        # Build the document-specific word filter based on any good
        # words listed in spelling directives. If we have no such
        # words, we want to push an empty list of filters so that we
        # can always safely pop the filter stack when we are done with
        # this document.
        doc_filters = []
        good_words = self.env.spelling_document_words.get(docname)
        if good_words:
            logger.info('Extending local dictionary for %s', docname)
            doc_filters.append(filters.IgnoreWordsFilterFactory(good_words))
        self.checker.push_filters(doc_filters)

        for node in doctree.traverse(docutils.nodes.Text):
            if (node.tagname == '#text' and
                    node.parent and
                    node.parent.tagname in self.TEXT_NODES):

                # Figure out the line number for this node by climbing the
                # tree until we find a node that has a line number.
                lineno = None
                parent = node
                seen = set()
                while lineno is None:
                    # logger.info('looking for line number on %r' % node)
                    seen.add(parent)
                    parent = node.parent
                    if parent is None or parent in seen:
                        break
                    lineno = parent.line

                # Check the text of the node.
                misspellings = self.checker.check(node.astext())
                for word, suggestions, context_line in misspellings:
                    msg_parts = [docname + '.rst']
                    if lineno:
                        msg_parts.append(darkgreen(str(lineno)))
                    msg_parts.append(red(word))
                    msg_parts.append(self.format_suggestions(suggestions))
                    msg_parts.append(context_line)
                    msg = ':'.join(msg_parts)
                    logger.info(msg)
                    yield "%s:%s: (%s) %s %s\n" % (
                        self.env.doc2path(docname, None),
                        lineno, word,
                        self.format_suggestions(suggestions),
                        context_line,
                    )

        self.checker.pop_filters()
        return

    def finish(self):
        if self.misspelling_count:
            logger.warning('Found %d misspelled words' %
                           self.misspelling_count)
        return

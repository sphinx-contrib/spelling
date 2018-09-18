# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Spelling checker extension for Sphinx.
"""

import collections

from docutils.parsers import rst
from sphinx.util import logging

from . import filters

logger = logging.getLogger(__name__)


class SpellingDirective(rst.Directive):
    """Custom directive for passing instructions to the spelling checker.

    .. spelling::

       word1
       word2

    """

    option_spec = {}
    has_content = True

    def run(self):
        env = self.state.document.settings.env

        # Initialize the per-document filters
        if not hasattr(env, 'spelling_document_filters'):
            env.spelling_document_filters = collections.defaultdict(list)

        good_words = []
        for entry in self.content:
            if not entry:
                continue
            good_words.extend(entry.split())
        if good_words:
            logger.debug(
                'Extending local dictionary for %s with %s' % (
                    env.docname, str(good_words))
            )
            env.spelling_document_filters[env.docname].append(
                filters.IgnoreWordsFilterFactory(good_words)
            )
        return []

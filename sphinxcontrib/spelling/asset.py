# encoding: utf-8
#
# Copyright (c) 2020 Doug Hellmann.  All rights reserved.
#
"""Asset collector for additional spelling terms
"""

import collections

from sphinx.environment.collectors import EnvironmentCollector
from sphinx.util import logging

logger = logging.getLogger(__name__)


class SpellingCollector(EnvironmentCollector):

    def clear_doc(self, app, env, docname) -> None:
        if docname in getattr(env, 'spelling_document_words', {}):
            del env.spelling_document_words[docname]

    def merge_other(self, app, env, docnames, other):
        other_words = getattr(other, 'spelling_document_words', {})
        if not hasattr(env, 'spelling_document_words'):
            env.spelling_document_words = collections.defaultdict(list)
        env.spelling_document_words.update(other_words)

    def process_doc(self, app, doctree):
        pass

# -*- coding: utf-8 -*-
"""
    sphinxcontrib.feed.directives
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2007-2011 the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
    
    Latest is based on sphinx.directives.other.TocTree
"""

import os

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx.locale import _
from sphinx.util import url_re, docname_join
from sphinx.util.nodes import explicit_title_re
from sphinx.util.matching import patfilter
from sphinx.directives.other import TocTree

class Latest(TocTree):
    """
    Directive to notify Sphinx about the hierarchical structure of the docs,
    and to include a table-of-contents-like tree in the current document.
    """
    def run(self):
        ret = super(Latest, self).run()
        tocnode = ret[0][0]
        tocnode['by_pub_date'] = True
        return ret

directives.register_directive('latest', Latest)


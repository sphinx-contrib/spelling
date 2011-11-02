# -*- coding: utf-8 -*-
"""
    sphinxcontrib.feed.feeddirectives
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2007-2011 the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
    
    Latest is based on sphinx.directives.other.TocTree
"""

import os

from docutils import nodes

from sphinx.directives.other import TocTree

from feednodes import latest

class Latest(TocTree):
    """
    Directive to notify Sphinx about the hierarchical structure of the docs,
    and to include a table-of-contents-like tree in the current document.
    
    Possibly this should not subclass the TocTree node, but just invoke the
    same method.
    """
    def run(self):
        ret = super(Latest, self).run()
        #extract the tocnode. We not want.
        #Could we even expand it to a full hierarchy here?
        tocnode = ret[0][0]
        tocatts = tocnode.non_default_attributes()
        latestnode = latest()
        for key, val in tocatts.iteritems():
            latestnode[key] = val
        wrappernode = nodes.compound(classes=['latest-wrapper'])
        wrappernode.append(latestnode)
        ret.append(wrappernode)
        return ret


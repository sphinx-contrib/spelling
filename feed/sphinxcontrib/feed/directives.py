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

from sphinx import addnodes
from sphinx.locale import _
from sphinx.util import url_re, docname_join
from sphinx.util.nodes import explicit_title_re
from sphinx.util.matching import patfilter

def int_or_nothing(argument):
    if not argument:
        return 999
    return int(argument)


class Latest(Directive):
    """
    Directive to notify Sphinx about the hierarchical structure of the docs,
    and to include a table-of-contents-like tree in the current document.
    
    Originally absed on the `sphinx.directives.other.TocTree` class.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'maxdepth': int,
        'glob': directives.flag,
        'hidden': directives.flag,
        'numbered': int_or_nothing,
        'titlesonly': directives.flag,
    }

    def run(self):
        env = self.state.document.settings.env
        suffix = env.config.source_suffix
        glob = 'glob' in self.options

        ret = []
        # (title, ref) pairs, where ref may be a document, or an external link,
        # and title may be None if the document's title is to be used
        entries = []
        includefiles = []
        all_docnames = env.found_docs.copy()
        # don't add the currently visited file in catch-all patterns
        all_docnames.remove(env.docname)
        for entry in self.content:
            if not entry:
                continue
            if not glob:
                # look for explicit titles ("Some Title <document>")
                m = explicit_title_re.match(entry)
                if m:
                    ref = m.group(2)
                    title = m.group(1)
                    docname = ref
                else:
                    ref = docname = entry
                    title = None
                # remove suffixes (backwards compatibility)
                if docname.endswith(suffix):
                    docname = docname[:-len(suffix)]
                # absolutize filenames
                docname = docname_join(env.docname, docname)
                if url_re.match(ref) or ref == 'self':
                    entries.append((title, ref))
                elif docname not in env.found_docs:
                    ret.append(self.state.document.reporter.warning(
                        'toctree contains reference to nonexisting '
                        'document %r' % docname, line=self.lineno))
                    env.note_reread()
                else:
                    entries.append((title, docname))
                    includefiles.append(docname)
            else:
                patname = docname_join(env.docname, entry)
                docnames = sorted(patfilter(all_docnames, patname))
                for docname in docnames:
                    all_docnames.remove(docname) # don't include it again
                    entries.append((None, docname))
                    includefiles.append(docname)
                if not docnames:
                    ret.append(self.state.document.reporter.warning(
                        'toctree glob pattern %r didn\'t match any documents'
                        % entry, line=self.lineno))
        subnode = addnodes.toctree()
        subnode['parent'] = env.docname
        # entries contains all entries (self references, external links etc.)
        subnode['entries'] = entries
        # includefiles only entries that are documents
        subnode['includefiles'] = includefiles
        subnode['maxdepth'] = self.options.get('maxdepth', -1)
        
        subnode['glob'] = glob
        subnode['hidden'] = 'hidden' in self.options
        subnode['numbered'] = self.options.get('numbered', 0)
        subnode['titlesonly'] = 'titlesonly' in self.options
        wrappernode = nodes.compound(classes=['toctree-wrapper'])
        wrappernode.append(subnode)
        ret.append(wrappernode)
        return ret

directives.register_directive('latest', Latest)


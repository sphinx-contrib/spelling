# -*- coding: utf-8 -*-
"""
    sphinxcontrib.whoosh
    ~~~~~~~~~~~~~~~~~~~~

    Whoosh search index builder.

    :copyright: Copyright 2009 Pauli Virtanen
    :license: BSD, see LICENSE for details.
"""

import os

from sphinx.util import SEP
from sphinx.builders.html import StandaloneHTMLBuilder

import whoosh.index
import whoosh.fields
import whoosh.analysis

class WhooshBuilder(StandaloneHTMLBuilder):
    """
    Builds Whoosh index.

    """
    name = "whoosh"
    format = "whoosh"

    def init(self):
        self.config_hash = ''
        self.tags_has = ''
        self.theme = None # no theme
        self.templates = None # no templates
        self.init_translator_class()
        self.init_highlighter()

        self.schema = whoosh.fields.Schema(
            name=whoosh.fields.ID(stored=True),
            title=whoosh.fields.TEXT(stored=True),
            body=whoosh.fields.TEXT(analyzer=whoosh.analysis.StemmingAnalyzer()))
        self.index = whoosh.index.create_in(self.outdir, self.schema)
        self.writer = self.index.writer()

    def get_target_uri(self, docname, typ=None):
        if docname == 'index':
            return ''
        if docname.endswith(SEP + 'index'):
            return docname[:-5] # up to sep
        return docname + SEP

    def handle_page(self, pagename, ctx, templatename='page.html',
                    outfilename=None, event_arg=None):
        ctx['current_page_name'] = pagename
        sidebarfile = self.config.html_sidebars.get(pagename)
        if sidebarfile:
            ctx['customsidebar'] = sidebarfile

        self.app.emit('html-page-context', pagename, templatename,
                      ctx, event_arg)

        # Push to index
        self.writer.add_document(name=unicode(ctx['current_page_name']),
                                 title=unicode(ctx.get('title', '')),
                                 body=unicode(ctx.get('body', '')))

    def finish(self):
        self.writer.commit()


def setup(app):
    app.add_builder(WhooshBuilder)


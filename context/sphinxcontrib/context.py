# -*- coding: utf-8 -*-
"""
    sphinx.builders.context
    ~~~~~~~~~~~~~~~~~~~~~~~

    ConTeXt Sphinx builder.

    :copyright: Copyright ©2009 by Wei-Wei Guo.
    :license: BSD, see LICENSE for details.

    The file is modeified from builders/text.py by the Sphinx team.
"""

import codecs
from os import path

from docutils.io import StringOutput

from sphinx.util import ensuredir
from sphinx.util.console import bold, darkgreen

from sphinx.builders import Builder
#from sphinx.writers.context import ConTeXtWriter
from writers.context import ConTeXtWriter

class ConTeXtBuilder(Builder):
    name = 'context'
    format = 'context'
    out_suffix = '.tex'

    def init(self):
        pass

    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = self.env.doc2path(docname, self.outdir,
                                           self.out_suffix)
            try:
                targetmtime = path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                # source doesn't exist anymore
                pass

    def get_target_uri(self, docname, typ=None):
        return ''

    def prepare_writing(self, docnames):
        self.writer = ConTeXtWriter(self)
        self.document_data = map(list, self.config.context_documents)[0]

    def handle_filename(self, docname):
        entry = path.split(docname)
        if entry[0] == '':
            filename = path.join(self.outdir, self.document_data[1])
        elif entry[1] == 'index':
            filename = path.join(self.outdir, entry[0], entry[0])
        else:
            filename = path.join(self.outdir, docname)
        return filename

    def assemble_doctree(self, infile):
        tree = self.env.get_doctree(infile)
        tree['doclist'] = infile.split('/')

        return tree

    def write_doc(self, docname, doctree):
        doctree = self.assemble_doctree(docname)
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)
        outfilename = self.handle_filename(docname) + self.out_suffix
        ensuredir(path.dirname(outfilename))
        try:
            f = codecs.open(outfilename, 'w', 'utf-8')
            try:
                f.write(''.join(self.writer.output))
            finally:
                f.close()
        except (IOError, OSError), err:
            self.warn("error writing file %s: %s" % (outfilename, err))

    def finish(self):
        pass

def setup(app):
    app.add_builder(ConTeXtBuilder)
    app.add_config_value('context_documents', [], False)

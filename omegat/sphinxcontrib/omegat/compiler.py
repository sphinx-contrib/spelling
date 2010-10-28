# -*- coding: utf-8 -*-
"""
    sphinxcontrib.omegat.compiler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    MessageCatalogCompiler class.

    :copyright: Copyright 2007-2010 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""


import os
import struct
import array

from os import path

from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir
from sphinx.util.console import red

class MessageCatalogCompiler(Builder):
    """
    Message catalog compiler.

    original code is written by Martin v. L? <loewis@informatik.hu-berlin.de>
    """
    name = 'msgfmt'

    def init(self):
        Builder.init(self)
        errors = False
        if not self.config.omegat_translated_path:
            self.info(red("'omegat_translated_path' should not be empty."))
            errors = True
        if not self.config.omegat_project_path:
            self.info(red("'omegat_project_path' should not be empty."))
            errors = True
        if self.config.omegat_translated_path not in self.config.locale_dirs:
            self.info(red("'omegat_translated_path' should be in locale_dirs."))
            errors = True
        if not self.config.language:
            self.info(red("'language' should be set."))
            errors = True
        if errors:
            self.info(red("    -> Please check conf.py"))
            raise RuntimeError("lack setting")

    def get_target_uri(self, docname, typ=None):
        return ''

    def get_outdated_docs(self):
        return self.env.found_docs

    def prepare_writing(self, docnames):
        return

    def write_doc(self, docname, doctree):
        return

    def finish(self):
        Builder.finish(self)
        output_path = path.join(
            self.config.omegat_translated_path,
            self.config.language,
            "LC_MESSAGES")
        ensuredir(output_path)
        sourcedir = path.join(self.config.omegat_project_path, 'target')
        for filename in os.listdir(sourcedir):
            if not filename.endswith(".po"):
                continue
            infile = path.join(sourcedir, filename)
            outfile = path.join(output_path,
                path.splitext(filename)[0] + '.mo')
            if path.exists(outfile):
                if path.getmtime(infile) < path.getmtime(outfile):
                    continue
            self._make(infile, outfile)

    def _add(self, messages, id, str, fuzzy):
        if not fuzzy and str:
            messages[id] = str

    def _generate(self, messages):
        keys = sorted(messages.keys())
        offsets = []
        ids = strs = ''
        for id in keys:
            offsets.append((len(ids), len(id), len(strs), len(messages[id])))
            ids += id + '\0'
            strs += messages[id] + '\0'
        output = ''
        keystart = 7*4+16*len(keys)
        valuestart = keystart + len(ids)
        koffsets = []
        voffsets = []
        for o1, l1, o2, l2 in offsets:
            koffsets += [l1, o1+keystart]
            voffsets += [l2, o2+valuestart]
        offsets = koffsets + voffsets
        output = struct.pack("Iiiiiii",
                             0x950412deL,       # Magic
                             0,                 # Version
                             len(keys),         # # of entries
                             7*4,               # start of key index
                             7*4+len(keys)*8,   # start of value index
                             0, 0)              # size and offset of hash table
        output += array.array("i", offsets).tostring()
        output += ids
        output += strs
        return output

    def _make(self, infile, outfile):
        ID = 1
        STR = 2
        messages = {}
        section = None
        fuzzy = 0
        lno = 0
        for l in open(infile):
            lno += 1
            if l[0] == '#' and section == STR:
                self._add(messages, msgid, msgstr, fuzzy)
                section = None
                fuzzy = 0
            if l[:2] == '#,' and 'fuzzy' in l:
                fuzzy = 1
            if l[0] == '#':
                continue
            if l.startswith('msgid') and not l.startswith('msgid_plural'):
                if section == STR:
                    self._add(messages, msgid, msgstr, fuzzy)
                section = ID
                l = l[5:]
                msgid = msgstr = ''
                is_plural = False
            elif l.startswith('msgid_plural'):
                if section != ID:
                    self.info(red(('gid_plural not preceeded by msgid'
                                   ' on %s:%d' % (infile, lno))))
                    sys.exit(1)
                l = l[12:]
                msgid += '\0' # separator of singular and plural
                is_plural = True
            elif l.startswith('msgstr'):
                section = STR
                if l.startswith('msgstr['):
                    if not is_plural:
                        self.info(red(('plural without msgid_plural'
                                       ' on %s:%d' % (infile, lno))))
                        sys.exit(1)
                    l = l.split(']', 1)[1]
                    if msgstr:
                        msgstr += '\0' # Separator of the various plural forms
                else:
                    if is_plural:
                        self.info(red(('indexed msgstr required for plural'
                                       ' on %s:%d' % (infile, lno))))
                        sys.exit(1)
                    l = l[6:]
            l = l.strip()
            if not l:
                continue
            l = eval(l)
            if section == ID:
                msgid += l
            elif section == STR:
                msgstr += l
            else:
                self.info(red(('Syntax error on %s:%d' % (infile, lno))))
                self.info(red(('  before: %s' % l)))
                sys.exit(1)
        if section == STR:
            self._add(messages, msgid, msgstr, fuzzy)
        output = self._generate(messages)
        try:
            open(outfile,"wb").write(output)
        except IOError,msg:
            print >> sys.stderr, msg

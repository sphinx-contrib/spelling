# -*- coding: utf-8 -*-
"""
    sphinxcontrib.omegat.builder
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The MessageCatalogBuilder class.

    :copyright: Copyright 2010 by SHIBUKAWA Yoshiki<yoshiki at shibu.jp>
    :license: BSD, see LICENSE for details.
"""

import os
import datetime

from os import path
from codecs import open
from datetime import datetime

from sphinx.util.osutil import copyfile
from sphinx.util.console import red, darkgreen
from sphinx.builders.intl import I18nBuilder, POHEADER


class OmegaTProjectBuilder(I18nBuilder):
    """
    Builds OmegaT project folder that includes .po file.
    """
    name = 'omegat'

    def init(self):
        I18nBuilder.init(self)
        errors = False
        if not self.config.omegat_project_path:
            self.info(red("'omegat_project_path' should not be empty."))
            self.info(red("    -> Please check conf.py"))
            raise RuntimeError("lack setting")
    
    def finish(self):
        I18nBuilder.finish(self)
        data = dict(
            version = self.config.version,
            copyright = self.config.copyright,
            project = self.config.project,
            # XXX should supply tz
            ctime = datetime.now().strftime('%Y-%m-%d %H:%M%z'),
        )
        self._create_project_folder()
        for section, messages in self.status_iterator(
                self.catalogs.iteritems(), "writing message catalogs... ",
                lambda (section, _):darkgreen(section), len(self.catalogs)):

            pofn = path.join(self.config.omegat_project_path,
                             "source", section + '.po')
            pofile = open(pofn, 'w', encoding='utf-8')
            try:
                pofile.write(POHEADER % data)
                for message, positions in messages.iteritems():
                    # message contains *one* line of text ready for translation
                    position = ", ".join(["%s(%s)" % (source, line) 
                                              for (source, line) in positions])
                    message = message.replace(u'\\', ur'\\'). \
                                      replace(u'"', ur'\"')
                    pomsg = u'#%s\nmsgid "%s"\nmsgstr ""\n\n' % (position, message)
                    pofile.write(pomsg)
            finally:
                pofile.close()
    
    def _create_project_folder(self):
        if not path.exists(self.config.omegat_project_path):
            os.mkdir(self.config.omegat_project_path)

        dirs = ["dictionary", "glossary", "omegat", "source", "target", "tm"]
        for dirname in dirs:
            dirpath = path.join(self.config.omegat_project_path, dirname)
            if not path.exists(dirpath):
                os.mkdir(dirpath)
        
        dest_path = path.join(self.config.omegat_project_path, "omegat.project")
        source_path = path.join(path.abspath(path.dirname(__file__)), "omegat.project")

        if not path.exists(dest_path):
            copyfile(source_path, dest_path)

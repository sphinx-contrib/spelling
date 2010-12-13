# -*- coding: utf-8 -*-
"""
    sphinxcontrib.omegat
    ~~~~~~~~~~~~~~~~~~~~

    Sphinx extension for collaboration with OmegaT

    :copyright: Copyright 2010 by SHIBUKAWA Yoshiki<yoshiki at shibu.jp>
    :license: BSD, see LICENSE for details.
"""

from builder import OmegaTProjectBuilder
from compiler import MessageCatalogCompiler


def setup(app):
    app.add_config_value('omegat_project_path', '', 'env')
    app.add_config_value('omegat_translated_path', '', 'env')
    app.add_builder(OmegaTProjectBuilder)
    app.add_builder(MessageCatalogCompiler)


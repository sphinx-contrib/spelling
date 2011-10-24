# -*- coding: utf-8 -*-
"""
    sphinx.environment
    ~~~~~~~~~~~~~~~~~~

    Global creation environment.

    :copyright: Copyright 2007-2011 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
# 
# import re
# import os
# import sys
# import time
# import types
# import codecs
# import imghdr
# import string
# import unicodedata
# import cPickle as pickle
from os import path
# from glob import glob
# from itertools import izip, groupby
# 
# from docutils import nodes
# from docutils.io import FileInput, NullOutput
# from docutils.core import Publisher
# from docutils.utils import Reporter, relative_path, new_document, \
#      get_source_line
# from docutils.readers import standalone
# from docutils.parsers.rst import roles, directives, Parser as RSTParser
# from docutils.parsers.rst.languages import en as english
# from docutils.parsers.rst.directives.html import MetaBody
# from docutils.writers import UnfilteredWriter
from docutils.transforms import Transform
# from docutils.transforms.parts import ContentsFilter

from feednodes import latesttree

class SortLastestTree(Transform):
    """
    Replace translatable nodes with their translated doctree.
    """
    default_priority = 800
    
    def apply(self):
        env = self.document.settings.env
        settings, source = self.document.settings, self.document['source']
        # XXX check if this is reliable
        assert source.startswith(env.srcdir)
        docname = path.splitext(path.relpath(source, env.srcdir))[0]

        for node in self.document.traverse(latesttree):
            import pdb; pdb.set_trace()
            
            if len(node['ids']) > 1 and node['ids'][0].startswith('id'):
                node['ids'] = node['ids'][1:] + [node['ids'][0]]

        # for child in patch.children: # update leaves
        #     child.parent = node
        # node.children = patch.children


# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

html_use_modindex = False
html_use_index = False
extensions = ['sphinxcontrib.googlechart', 'sphinxcontrib.googlechart.graphviz']
source_suffix = '.rst'
master_doc = 'index'

project = u'sphinxcontrib.googlchart quick reference'
copyright = u'2011, Takeshi KOMIYA'

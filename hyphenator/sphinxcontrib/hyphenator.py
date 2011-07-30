# -*- coding: utf-8 -*-
"""
    sphinx hyphenator extension
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Extension to add support for hyphenation to HTML using hyphenator.js
"""

from __future__ import with_statement

import os

from sphinx.application import ExtensionError


def builder_inited(app):
    if not app.config.hyphenator_path:
        raise ExtensionError('hyphenator extension: "hyphenator_path" must be'
                             ' set in "conf.py"')
    app.add_javascript(os.path.join(app.config.hyphenator_path,
                                    'Hyphenator.js'))
    if app.config.hyphenator_language:
        language = app.config.hyphenator_language
    elif app.config.language:
        language = app.config.language
    else:
        raise ExtensionError('hyphenator extension: no language found'
                             ', please set "hyphenator_language"'
                             ' in your conf.py')
    start_script = ("var hyphenatorSettings = {\n"
                    "  selectorfunction: function() {\n"
                    "          return $('.document, .sphinxsidebar').get()},\n"
                    "  displaytogglebox: true,\n"
                    "  defaultlanguage: '%s'\n"
                    "  };\n"
                    "Hyphenator.config(hyphenatorSettings);\n"
                    "Hyphenator.run();" % language)
    script_name = "run_hyphenation.js"
    script_path = os.path.join(app.confdir,
                               app.config.html_static_path[0],
                               script_name)
    with open(script_path, "w") as script_file:
        script_file.write(start_script)
    print app.confdir
    print app.config.html_static_path
    app.add_javascript(script_name)


def setup(app):
    app.add_config_value('hyphenator_path',
                         #'hyphenator_3.3.0', '')
                         'http://hyphenator.googlecode.com/svn/trunk/', '')
    app.add_config_value('hyphenator_language',
                         None, '')
    app.connect('builder-inited', builder_inited)

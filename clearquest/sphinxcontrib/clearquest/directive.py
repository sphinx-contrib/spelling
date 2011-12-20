# Copyright (c) 2009 by the contributors (see AUTHORS file).
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
import ConfigParser
from os import path

from docutils.parsers.rst.directives.tables import Table
from docutils.parsers.rst import directives, DirectiveError
from docutils import statemachine, nodes, frontend
from sphinxcontrib.clearquest.connection import ClearQuestConnection
from sphinx.util import console
from docutils.utils import Reporter


SUBST_REF_REX = re.compile(r'\|(.+?)\|', re.DOTALL)

#------------------------------------------------------------------------------
class CQReporter(Reporter):
    """
    Subclass of docutils.util.Reporter with default values
    """
    def __init__(self):
        settings = frontend.OptionParser().get_default_values()
        settings.report_level = 1
        Reporter.__init__(
            self,
            source='sphinxcontrib.clearquest',
            report_level=settings.report_level,
            halt_level=settings.halt_level,
            stream=settings.warning_stream,
            debug=settings.debug,
            encoding=settings.error_encoding,
            error_handler=settings.error_encoding_error_handler
        )

#------------------------------------------------------------------------------
class ClearQuest(Table):
    """
    .. clearquest:: directive
    """

    option_spec = {
        'username': directives.unchanged,
        'password': directives.unchanged,
        'db_name': directives.unchanged,
        'db_set': directives.unchanged,
        'params': directives.unchanged,
    }

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    reporter = CQReporter()

    connection = None

    def run(self):
        try:
            self.resolve_substitutions_refs()
            queryName = self.arguments[0]
            queryParams = self.extract_query_params()

            if ClearQuest.connection is None:
                settings = self.get_settings()
                if None in settings.values():
                    missing = [ name for name, value in settings.items() if value is None ]
                    ClearQuest.reporter.warning(console.red( #@UndefinedVariable
                        'Missing settings "%s". ' % '", "'.join(missing) +
                        'Looked in ~/.sphinxcontrib and in directive options.'
                    ))
                ClearQuest.reporter.info('Opening ClearQuest session...')
                ClearQuest.connection = ClearQuestConnection(**settings)

            ClearQuest.reporter.info('Executing ClearQuest query "%s"...' % queryName)
            columns, records = ClearQuest.connection.run_query(queryName, queryParams)
            
            if len(records) == 0:
                # No results from ClearQuest query, we fill one line with dashes
                records.append(["--"] * len(columns))
            
            col_widths = self.get_column_widths(header=columns, content=records)
            table_head = [ self.create_row(columns) ]
            table_body = [ self.create_row(line) for line in records ]

        except Exception, detail:
            if isinstance(detail, DirectiveError):
                message = detail.msg
            else:
                message = str(detail)
            error = ClearQuest.reporter.error(
                'Error with query data in "%s" directive:\n%s' % (self.name, message),
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]

        table = (col_widths, table_head, table_body)
        table_node = self.state.build_table(table, self.content_offset)
        table_node['classes'] += self.options.get('class', [])

        return [table_node]

    def create_row(self, line):
        row = []
        for cell_text in line:
            row.append( (0, 0, 0, statemachine.StringList(cell_text.splitlines())) )
        return row

    def get_column_widths(self, header, content):
        widths = [0] * len(header)

        for i in range(len(header)):
            if header[i] is not None and len(header[i]) > widths[i]:
                widths[i] = len(header[i])

        for row in content:
            for i in range(len(row)):
                if row[i] is not None and len(row[i]) > widths[i]:
                    widths[i] = len(row[i])

        return widths

    def extract_query_params(self):
        params_dict = {}
        params = self.options.get("params")
        if params:
            for p in params.split(","):
                p_name, p_value = p.split("=")
                params_dict[p_name.strip()] = p_value.strip()
        return params_dict

    def resolve_substitutions_refs(self):
        def _subst_ref_match(match):
            return self.state.document.substitution_defs[match.group(1)].astext()

        for opt_name in self.options.keys():
            opt_val = unicode(self.options[opt_name])
            opt_val, _ = SUBST_REF_REX.subn(_subst_ref_match, opt_val)
            self.options[opt_name] = opt_val


    def get_settings(self):
        settings = {
            'username': None,
            'password': None,
            'db_name': None,
            'db_set': None,
        }
        config = ConfigParser.RawConfigParser()

        # first, we try to read settings from ~/.sphinxcontrib
        config.read(path.normpath(path.expanduser('~/.sphinxcontrib')))
        # then, from ~/sphinxcontrib for windows users
        config.read(path.normpath(path.expanduser('~/sphinxcontrib')))
        
        if config.has_section('clearquest'):
            for name in settings.keys():
                if config.has_option('clearquest', name):
                    settings[name] = config.get('clearquest', name)

        # then, we override the settings if they are given in the directive
        for name in settings.keys():
            if self.options.has_key(name) and self.options[name] is not None:
                settings[name] = self.options[name]

        return settings




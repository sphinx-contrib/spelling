#!/usr/bin/env python
"""SQLTable extension for Sphinx.
"""

from docutils import nodes
from docutils.parsers.rst.directives.tables import Table
from docutils.parsers.rst import directives

import sqlalchemy

class SQLTable(Table):

    option_spec = {'widths': directives.positive_int_list,
                   'class': directives.class_option,
                   'name': directives.unchanged,
                   'connection_string':directives.unchanged,
                   }

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        config = app.config

        # Make sure we have some content, which for now we assume is a
        # query.
        if not self.content:
            error = self.state_machine.reporter.error(
                'No query in sqltable directive',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        # Make sure the user told us about a database.
        connection_string = self.options.get('connection_string',
                                             config.sqltable_connection_string,
                                             )
        if not connection_string:
            error = self.state_machine.reporter.error(
                'No connection_string or sqltable_connection_string was specified for sqltable',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        # Make sure we can get the specified database.
        try:
            app.info('Connecting to %s' % connection_string)
            engine = sqlalchemy.create_engine(connection_string)
        except Exception, err:
            error = self.state_machine.reporter.error(
                'Could not connect to %s for sqltable' % (
                    connection_string,
                    ),
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        # Run the query
        try:
            query = '\n'.join(self.content)
            app.info('Running query %r' % query)
            results = engine.execute(query)
        except Exception, err:
            error = self.state_machine.reporter.error(
                u'Error with query %s for sqltable: %s' % (
                    query,
                    err,
                    ),
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        # Extract some values we need for building the table.
        table_headers = results.keys()
        table_body = results
        max_cols = len(table_headers)
        max_header_cols = max_cols

        # Handle the width settings and title
        try:
            col_widths = self.get_column_widths(max_cols)
            title, messages = self.make_title()
        except SystemMessagePropagation, detail:
            return [detail.args[0]]
        except Exception, err:
            error = self.state_machine.reporter.error(
                'Error processing sqltable directive:\n%s' % err,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
                )
            return [error]

        # Build the node containing the table content
        table_node = self.build_table(table_body, col_widths, table_headers)
        table_node['classes'] += self.options.get('class', [])
        self.add_name(table_node)
        if title:
            table_node.insert(0, title)
        return [table_node] + messages

    def build_table(self, table_data, col_widths, headers):
        table = nodes.table()

        # Set up the column specifications
        # based on the widths.
        tgroup = nodes.tgroup(cols=len(col_widths))
        table += tgroup
        tgroup.extend(nodes.colspec(colwidth=col_width)
                      for col_width in col_widths)

        # Set the headers
        thead = nodes.thead()
        tgroup += thead
        row_node = nodes.row()
        thead += row_node
        row_node.extend(
            nodes.entry(h, nodes.paragraph(text=h))
            for h in headers
            )

        # The body of the table is made up of rows.
        # Each row contains a series of entries,
        # and each entry contains a paragraph of text.
        tbody = nodes.tbody()
        tgroup += tbody
        rows = []
        for row in table_data:
            trow = nodes.row()
            for cell in row:
                entry = nodes.entry()
                para = nodes.paragraph(text=unicode(cell))
                entry += para
                trow += entry
            rows.append(trow)
        tbody.extend(rows)

        #print table
        return table

def setup(app):
    app.info('Initializing SQLTable')
    app.add_config_value('sqltable_connection_string', '', 'env')
    app.add_directive('sqltable', SQLTable)

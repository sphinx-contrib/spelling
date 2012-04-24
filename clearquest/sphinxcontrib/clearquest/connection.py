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

import win32com.client as COM


PRIVATE_SESSION = 2

class ClearQuestConnection():

    def __init__(self, username, password, db_name, db_set):
        self.username = str(username)
        self.password = str(password)
        self.db_name = str(db_name)
        self.db_set = str(db_set)
        #self.db_encoding = str(db_encoding)
        self.session = None

    def run_query(self, queryName, parameters):
        """
        Runs a ClearQuest query and returns the result as a list of lists.

        example:

        [ ['column_1',  'column_2',  'column_3'],
          ['value_1_1', 'value_1_2', 'value_1_3'],
          ['value_2_1', 'value_2_2', 'value_2_3'],
          ['value_3_1', 'value_3_2', 'value_3_3'],
          ['value_4_1', 'value_4_2', 'value_4_3'], ]

        If the query returns nothing, only one row containing dashes is returned.

        """
        if self.session is None:
            self.open_session()

        workspace = self.session.GetWorkSpace
        query = workspace.GetQueryDef(queryName)
        resultSet = self.session.BuildResultSet(query)
        numberOfParams = resultSet.GetNumberOfParams

        if numberOfParams:
            errors = []

            for i in range(1, numberOfParams + 1):
                param_name = resultSet.GetParamLabel(i)
                try:
                    param_value = parameters[param_name]
                    resultSet.AddParamValue(i, param_value)
                except:
                    errors.append("'%s'" % param_name)

            if errors:
                params = ", ".join(errors)
                raise ValueError("Missing parameters %s to query '%s'" % (params, queryName))

        resultSet.Execute()

        status = resultSet.MoveNext

        # this is silly, but first column is reserved
        nbcol = resultSet.GetNumberOfColumns - 1

        records = []
        columns = [ field.Label for field in query.QueryFieldDefs if field.IsShown ][1:]


        while status == 1:
            records.append([ resultSet.GetColumnValue(i) for i in range(2, nbcol + 2) ])
            status = resultSet.MoveNext

        return columns, records

    def open_session(self):
        self.session = COM.dynamic.Dispatch("CLEARQUEST.SESSION")
        self.session.UserLogon(self.username, self.password, self.db_name,
                               PRIVATE_SESSION, self.db_set)


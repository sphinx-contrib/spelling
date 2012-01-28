==========
 Examples
==========

The following examples use a SQLite database containing:

.. literalinclude:: sampledata.sql

Local Connection String
=======================

Use the ``connection_string`` option to specify the database to be
used for a single query.

::

  .. sqltable:: List of Users
     :connection_string: sqlite:///sampledata.db

     select name as 'Name', email as 'E-mail' from users
     order by Name asc

produces this table:

.. sqltable:: List of Users
   :connection_string: sqlite:///sampledata.db

   select name as 'Name', email as 'E-mail' from users
   order by Name asc

Missing Connection String
=========================

Leaving out the ``connection_string`` option produces an error:

::

  .. sqltable:: List of Users

     select name as 'Name', email as 'E-mail' from users
     order by Name asc

results in

::

  $ sphinx-build -b html -d _build/doctrees   . _build/html
  Running Sphinx v1.1.2
  Initializing SQLTable
  loading pickled environment... done
  building [html]: targets for 1 source files that are out of date
  updating environment: 0 added, 1 changed, 0 removed
  Connecting to sqlite:///sampledata.db                                           
  Running query u"select name as 'Name', email as 'E-mail' from users\norder by Name asc"

  .../docs/example.rst:45: ERROR: No connection_string or sqltable_connection_string was specified for sqltable

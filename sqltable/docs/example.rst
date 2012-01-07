==========
 Examples
==========

Given a SQLite database containing:

.. literalinclude:: sampledata.sql

this reStructuredText input:

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

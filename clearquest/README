.. -*- restructuredtext -*-

=============================
Sphinx "ClearQuest" extension 
=============================

Description
===========

A sphinx extension that adds a ``clearquest`` directive for converting 
ClearQuest__ requests to reStructuredText tables.

__ http://www-01.ibm.com/software/awdtools/clearquest/

Dependencies
============

Sphinx
   http://sphinx.pocoo.org/
PyWin32
   http://sourceforge.net/projects/pywin32/ (**PyWin32** will not be automatically 
   installed by ``easy_install`` or ``pip install`` as ``egg`` packages are not
   available on **pypi**)

Installation & Usage
====================

You can install the ``sphinxcontrib.clearquest`` package with ``easy_install`` 
or ``pip``: ::

   $ easy_install sphinxcontrib-clearquest

Or with the windows installer available on this page.

.. important:: You must manually install **PyWin32** for the directive to work.

Append ``'sphinxcontrib.clearquest'`` to extensions parameter, and run Sphinx.

Directive Syntax
================

The syntax of the directive is as follows: ::

   .. clearquest:: <full name/of the clearquest query> (mandatory)
      :params: <parameters to pass to the query> (optional)
      :username: <your username> (optional)
      :password: <your password> (optional)
      :db_name: <the name of the db> (optional)
      :db_set: <the name of the db set> (optional)

The parameters to pass to the query must respect the following syntax: ::

   <param1_name>=<param1_value>,<param2_name>=<param2_value>, ...

You can provide them in any order as long as you don't forget one. 
The query call will fail if you do.

The connection credentials can either be provided as directive options or 
in a ``clearquest`` section in the ``~/.sphinxcontrib`` file which is a 
standard ``.ini`` configuration file. 

Here is an example of ``~/.sphinxcontrib`` file: ::

   [clearquest]
   username = john
   password = doe
   db_name = prod
   db_set = cqsrv


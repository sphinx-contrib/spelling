.. sdedit extension documentation master file, created by
   sphinx-quickstart on Sat Oct 10 21:07:08 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to sdedit extension's
=============================

This is a sphinx extension which render sequence diagrams by using
`Quick Sequence Diagram Editor <http://sdedit.sourceforge.net/>`_ (sdedit).

rendered:

.. sequence-diagram::
   :maxwidth: 300

   actor:Actor
   sphinx:Sphinx[a]
   dot:Graphviz
   sdedit:Quick Sequence Diagram Editor

   actor:sphinx.make html
   sphinx:dot.render_diagram()
   sphinx:sdedit.render_diagram()

source:

.. code-block:: text

   .. sequence-diagram::

      actor:Actor
      sphinx:Sphinx[a]
      dot:Graphviz
      sdedit:Quick Sequence Diagram Editor

      actor:sphinx.make html
      sphinx:dot.render_diagram()
      sphinx:sdedit.render_diagram()

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

Directive
=========

.. describe:: .. sequence-diagram::

   This directive insert a sequence diagram into the generated document.
   This code block has a source script of Quick Sequence Diagram Editor.
   
   .. seealso::

    `how to enter text <http://sdedit.sourceforge.net/enter_text/index.html>`_
        This page describes sdedit's syntax. 

Configuration File Options
==========================

.. confval:: sdedit_path

   This is a path for sdedit program. You can use .exe, .jar, .sh and .bat
   file path.

.. confval:: sdedit_java_path

   If you set .jar files at :confval:`sdedit_path`, use this option to run
   .jar file. Default value is 'java'.

.. confval:: sdedit_args

   If you want to add options when sdedit is run, use this option.

   This value is a list of parameters. Default value is [].

Repository
==========

This code is hosted by Bitbucket.

  http://bitbucket.org/shibu/sdeditext_for_sphinx/

ChangeLog
=========

.. include:: ../CHANGES

License
=======

.. include:: ../LICENSE
    :literal:

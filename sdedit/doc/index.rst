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

License
=======

This software is under MIT/X License.

Copyright (c) 2009 SHIBUKAWA Yoshiki <yoshiki at shibu.jp>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

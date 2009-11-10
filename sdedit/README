sdedit extension README
=======================

This is a sphinx extension which render sequence diagrams by using
`Quick Sequence Diagram Editor <http://sdedit.sourceforge.net/>`_ (sdedit).

rendered:

.. sequence-diagram::
   :maxwidth: 500
   :linewrap: false
   :threadnumber: true

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
      :maxwidth: 500
      :linewrap: false
      :threadnumber: true

      actor:Actor
      sphinx:Sphinx[a]
      dot:Graphviz
      sdedit:Quick Sequence Diagram Editor

      actor:sphinx.make html
      sphinx:dot.render_diagram()
      sphinx:sdedit.render_diagram()

Setting
=======

.. You can see available package at `PyPI <http://pypi.python.org/pypi/sphinxcontrib-sdedit>`_.

You can get archive file at http://bitbucket.org/shibu/sdeditext_for_sphinx/

Required components
-------------------

* `Quick Sequence Diagram Editor <http://sdedit.sourceforge.net/>`_

  You can use .exe or .jar file (.sh, .bat is not tested yet).

* `PIL <http://www.pythonware.com/products/pil/>`_ to create thumbnail

Install
-------

.. code-block:: bash

   > easy_install sphinxcontrib-sdedit


Configure Sphinx
----------------

To enable this extension, add ``sphinxcontrib.sdedit`` module to extensions 
option at :file:`conf.py`. 

.. code-block:: python

   import os, sys

   # Path to the folder where sdedit.py is
   # NOTE: not needed if the package is installed in traditional way
   # using setup.py or easy_install
   sys.path.append(os.path.abspath('/path/to/sphinxcontrib.sdedit'))

   # Enabled extensions
   extensions = ['sphinxcontrib.sdedit']

   # Path to sedit -setup (http://sdedit.sourceforge.net/)
   # you can use .jar, .exe, .bat, .sh
   sdedit_path = '/path/to/sdedit-3.0.5.jar'


On Windows, you can also use the ``.exe`` version of sdedit. 
The configuration key :confval:`sdedit_path` is required.
See also the :ref:`complete list of the configuration keys <config>`.

Directive
=========

.. describe:: .. sequence-diagram::

   This directive insert a sequence diagram into the generated document.
   This code block has a source script of Quick Sequence Diagram Editor.
  
   * ``maxwidth``: This is a integer option. default value is 700:

   * ``linewrap``: This is a boolean option.

   * ``threadnumber``: This is a boolean option.
 
   .. seealso::

    `how to enter text <http://sdedit.sourceforge.net/enter_text/index.html>`_
        This page describes sdedit's syntax. 

    `how to enter text(Japanese) <http://www.shibu.jp/sdedit-jp/>`_
        This is Japanese translation of above document.

.. _config:

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

.. confval:: sdedit_default_options

   This option is a dictionary. In this version, it has following option:

   * ``maxwidth``: If generated image's width is larger than this value, 
     create thumbnail image. Default value is 700.

     You can overwrite it if you use directive's option ``maxwidth``.

   .. versionadded:: 0.2

Repository
==========

This code is hosted by Bitbucket.

  http://bitbucket.org/shibu/sdeditext_for_sphinx/

  http://bitbucket.org/birkenfeld/sphinx-contrib/
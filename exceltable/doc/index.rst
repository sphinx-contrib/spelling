==========
Exceltable
==========
Module sphinxcontrib.exceltable is an extension for Sphinx_. Exceltable add support for including spreadsheets, or part
of it, into Sphinx document.




This is document describes :ref:`how to install <setup>`, :ref:`use <usage>` and :ref:`contribute to the development <devel>` of
the :mod:`sphinx.exceltable` module.

.. contents::
   :local:

.. _setup:

Setup
=====

.. container:: exceltable

    :doc:`rusty.exceltable <exceltable>`
      Creates table from selected part of the Excel -document.

      Requires `xlrd`_ -module.

Here you can find the minimum steps for installation and usage of the module:

#. Install module along with its dependencies using `pip`:

     pip install sphinxcontrib.exceltable

#. Start new Sphinx powered documentation project or continue with existing
   documentation::

     sphinx-quicstart

#. Configure directive of your choice into Sphinx :file:`conf.py`
   configuration file.

   .. code-block:: python

     # Add ``sphinxcontrib.exceltable`` into extension list
     extensions = ['sphinxcontrib.exceltable']

#. Place directive/role in your document:

   .. code-block:: rst

      My document
      ===========
      The contents of the setup script:

    .. exceltable:: Table caption
       :file: path/to/document.xls
       :header: 1
       :selection: A1:B3

#. Build the document::

     sphinx-build -b html doc dist/html

#. That's it!

.. _usage:

Usage
=====


.. toctree::
   :maxdepth: 2
   :numbered:

   ext
   changelog
   devel
   faq
   glossary

.. toctree::
   :hidden:

   global

.. include:: global.rst



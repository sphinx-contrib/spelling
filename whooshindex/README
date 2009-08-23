.. -*- restructuredtext -*-

===================================
Whoosh indexer extension for Sphinx
===================================

:author: Pauli Virtanen <pav@iki.fi>

.. module:: sphinxcontrib.whooshindex
   :synopsis: Index Sphinx documents with the Whoosh indexing engine

This extension adds an additional builder, the :class:`WhooshBuilder`.
It indexes all documents using the Whoosh_ pure-Python indexing
engine, and places the resulting index in the output directory.

The name of the builder is ``whoosh``.

.. _Whoosh: http://whoosh.ca/

Building
========

Requirements
------------

* Whoosh_ (0.3 or later).
* reportlab_ (for LaTeX/PDF output)
* PIL_ (for any image format other than SVG or PDF)

From source (tar.gz or checkout)
--------------------------------

Unpack the archive, enter the sphinxcontrib-aafig-x.y directory and run::

    python setup.py install


Setuptools/PyPI_
----------------

Alternatively it can be installed from PyPI_, either manually downloading the
files and installing as described above or using:

easy_install -U sphinxcontrib-whoosh

Enabling the extension in Sphinx_
---------------------------------

Just add ``sphinxcontrib.whooshindex`` to the list of extensions in the
``conf.py`` file. For example::

    extensions = ['sphinxcontrib.whooshindex']

Usage
=====

Give a builder name ``whoosh`` to ``sphinxbuild``. The Whoosh index will
be placed to the output directory.

.. Links:
.. _aafigure: http://launchpad.net/aafigure
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org/
.. _reportlab: http://www.reportlab.org/
.. _PIL: http://www.pythonware.com/products/pil/
.. _PyPI: http://pypi.python.org/pypi


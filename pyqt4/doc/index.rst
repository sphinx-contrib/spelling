.. highlight:: rest
.. default-domain:: rst

:py:mod:`lunar.sphinx.ext.pyqt4` -- Document Qt4 APIs
=====================================================

.. py:module:: lunar.sphinx.ext.pyqt4
   :synopsis: Special directives for Qt4 APIs

This Sphinx_ 1.0 extension provides markup to document PyQt4_ specific
objects.  Currently it only supports signals.

The extension is available under the terms of the BSD license, see LICENSE_
for more information.


Installation
------------

This extension can be installed from the Python Package Index::

   pip install sphinx-contrib.pyqt4

Alternatively, you can clone the sphinx-contrib_ repository from BitBucket,
and install the extension directly from the repository::

   hg clone http://bitbucket.org/birkenfeld/sphinx-contrib
   cd sphinx-contrib/pyqt4
   python setup.py install


Usage
-----

This extension provides the ``pyqt4`` domain, which extends the standard
python domain with the new :dir:`pyqt4:signal` directive:

.. directive:: pyqt4:signal

   This directive documents a signal.  It behaves like the standard
   :dir:`py:method` directive, except that the resulting markup marks the
   generated signature a signal.

Though the ``pyqt4`` domain is derived from the Python domain and can thus
work as drop-in replacement for it, you should not use this directive as
default domain, unless you are documenting a project consisting solely of
PyQt4 APIs.

As the term "signal" is rather common, other domains may add a directive of
this name to the python domain, too.  Therefore, it is strongly advisable to
document signals by using the fully qualified name of the directive.  This
clearly marks the signal as PyQt4 signal, avoiding any disambiguities.


Contribution
------------

Please contact the author or create an issue in the issue tracker of the
sphinx-contrib_ repository, if you have found any bugs or miss some
functionality (e.g. integration of some other issue tracker).  Patches are
welcome!


.. toctree::
   :maxdepth: 2
   :hidden:

   changes.rst


.. _Sphinx: http://sphinx.pocoo.org/
.. _PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt/intro/
.. _`sphinx-contrib`: http://bitbucket.org/birkenfeld/sphinx-contrib
.. _`issue tracker`: http://bitbucket.org/birkenfeld/sphinx-contrib/issues
.. _LICENSE: http://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/LICENSE
